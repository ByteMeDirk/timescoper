"""Reporting views — aggregated metrics computed from annotated querysets."""

from datetime import datetime, timedelta

from django.db.models import Count, Q, Sum
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsTeamLeadOrAbove
from apps.timelog.models import TimeEntry


class DailySummaryView(APIView):
    """Return a daily time summary for a user."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_id = request.query_params.get("user_id", request.user.id)
        date = request.query_params.get("date", datetime.now().date().isoformat())

        entries = TimeEntry.objects.filter(user_id=user_id, date=date)
        agg = entries.aggregate(
            total_hours=Sum("hours"),
            billable_hours=Sum("hours", filter=Q(is_billable=True)),
            entry_count=Count("id"),
        )

        return Response({
            "date": date,
            "user_id": str(user_id),
            "total_hours": float(agg["total_hours"] or 0),
            "billable_hours": float(agg["billable_hours"] or 0),
            "entry_count": agg["entry_count"],
        })


class WeeklySummaryView(APIView):
    """Return a weekly time summary (Mon–Sun) for a user."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_id = request.query_params.get("user_id", request.user.id)
        week_start = request.query_params.get("week_start")

        if week_start:
            start = datetime.strptime(week_start, "%Y-%m-%d").date()
        else:
            today = datetime.now().date()
            start = today - timedelta(days=today.weekday())  # Monday

        end = start + timedelta(days=6)

        entries = TimeEntry.objects.filter(
            user_id=user_id,
            date__gte=start,
            date__lte=end,
        )
        agg = entries.aggregate(
            total_hours=Sum("hours"),
            billable_hours=Sum("hours", filter=Q(is_billable=True)),
            entry_count=Count("id"),
        )

        # Per-day breakdown
        daily = []
        for i in range(7):
            day = start + timedelta(days=i)
            day_agg = entries.filter(date=day).aggregate(total=Sum("hours"))
            daily.append({
                "date": day.isoformat(),
                "hours": float(day_agg["total"] or 0),
            })

        return Response({
            "week_start": start.isoformat(),
            "week_end": end.isoformat(),
            "user_id": str(user_id),
            "total_hours": float(agg["total_hours"] or 0),
            "billable_hours": float(agg["billable_hours"] or 0),
            "entry_count": agg["entry_count"],
            "daily": daily,
        })


class ProjectUtilisationView(APIView):
    """Return utilisation metrics for a project."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from apps.projects.models import Project

        project_id = request.query_params.get("project_id")
        if not project_id:
            return Response(
                {"error": "project_id is required.", "code": "missing_param"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return Response(
                {"error": "Project not found.", "code": "not_found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        entries = TimeEntry.objects.filter(project=project)
        agg = entries.aggregate(
            total_hours=Sum("hours"),
            billable_hours=Sum("hours", filter=Q(is_billable=True)),
            entry_count=Count("id"),
        )

        total = float(agg["total_hours"] or 0)
        budget = float(project.budget_hours or 0)

        return Response({
            "project_id": str(project.id),
            "project_name": project.name,
            "total_hours": total,
            "billable_hours": float(agg["billable_hours"] or 0),
            "budget_hours": budget,
            "budget_remaining": budget - total if budget else None,
            "utilisation_pct": round((total / budget) * 100, 1) if budget else None,
            "entry_count": agg["entry_count"],
        })


class TeamActivityView(APIView):
    """Return activity metrics for a team within a date range."""

    permission_classes = [permissions.IsAuthenticated, IsTeamLeadOrAbove]

    def get(self, request):
        team_id = request.query_params.get("team_id")
        from_date = request.query_params.get("from")
        to_date = request.query_params.get("to")

        if not team_id:
            return Response(
                {"error": "team_id is required.", "code": "missing_param"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        entries = TimeEntry.objects.filter(project__team_id=team_id)
        if from_date:
            entries = entries.filter(date__gte=from_date)
        if to_date:
            entries = entries.filter(date__lte=to_date)

        agg = entries.aggregate(
            total_hours=Sum("hours"),
            billable_hours=Sum("hours", filter=Q(is_billable=True)),
            entry_count=Count("id"),
        )

        # Per-member breakdown
        member_stats = (
            entries.values("user__id", "user__first_name", "user__last_name", "user__email")
            .annotate(hours=Sum("hours"), entries=Count("id"))
            .order_by("-hours")
        )

        return Response({
            "team_id": team_id,
            "total_hours": float(agg["total_hours"] or 0),
            "billable_hours": float(agg["billable_hours"] or 0),
            "entry_count": agg["entry_count"],
            "members": [
                {
                    "user_id": str(m["user__id"]),
                    "name": f'{m["user__first_name"]} {m["user__last_name"]}',
                    "email": m["user__email"],
                    "hours": float(m["hours"] or 0),
                    "entries": m["entries"],
                }
                for m in member_stats
            ],
        })
