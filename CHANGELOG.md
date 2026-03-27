# Changelog

All notable changes to TimeScoper will be documented in this file.

## [Unreleased]

### Added
- Django 5.x backend with Django REST Framework
- Custom user model with email-based auth and role system (Developer, Team Lead, PM, Admin)
- JWT authentication via SimpleJWT (register, login, refresh, me)
- Team and membership management API
- Project and category management API with budget tracking
- Task management API with subtasks, labels, and comments
- Time entry API with 24h daily constraint validation
- Reporting API: daily summaries, weekly summaries, project utilisation, team activity
- Role-based permission classes (IsAdmin, IsTeamLeadOrAbove, IsProjectManagerOrAbove)
- OpenAPI schema generation via drf-spectacular
- Vue.js 3 frontend with Composition API
- Pinia stores for auth, projects, tasks, timelog, and reporting
- Axios API client with JWT token refresh interceptor
- Custom design system with Nexus-inspired tokens (light + dark mode)
- Responsive app shell: sidebar (desktop), collapsible (tablet), bottom nav (mobile)
- Dashboard with KPI cards, quick add form, weekly chart, daily log, and task widget
- Time log view with weekly calendar layout
- Tasks view with Kanban board and list view toggle
- Projects view with budget burn bars
- Reports view with weekly chart and summary stats
- Team management view with member list
- Admin panel with user management table
- Custom base components: Button, Input, Modal, Card, Badge, Select, Spinner, Tooltip
- Skeleton loaders and empty states for all data-loading views
- Docker Compose setup with PostgreSQL, Django, and Vite
- GitHub Actions CI for backend (Black, isort, flake8, pytest) and frontend (ESLint, Vitest)
- Comprehensive README with architecture diagram, API reference, and role permissions
