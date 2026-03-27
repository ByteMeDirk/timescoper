# TimeScoper

**Time & Task Tracking for Software Development Teams**

TimeScoper enables developers, team leads, and project managers to log daily work, track time against tasks, and generate productivity insights for business reporting.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                              │
│              Vue.js 3 + Vite + Tailwind CSS v4              │
│     Pinia (state) · Vue Router (SPA) · Axios (HTTP)        │
│              Chart.js (charts) · Lucide (icons)             │
├──────────────────────┬──────────────────────────────────────┤
│        REST API      │      /api/v1/                        │
├──────────────────────┴──────────────────────────────────────┤
│                         Backend                              │
│         Django 5 + Django REST Framework + SimpleJWT        │
│    drf-spectacular (OpenAPI) · django-filter · cors-headers │
├─────────────────────────────────────────────────────────────┤
│                        Database                              │
│          PostgreSQL 16 (prod) · SQLite (local dev)          │
└─────────────────────────────────────────────────────────────┘
```

## Features

- **Daily Time Logs** — submit time entries linked to tasks, projects, and categories
- **Task Management** — create, assign, and track tasks with Kanban board and list views
- **Project Management** — group tasks under projects with budgets and timelines
- **Dashboard & Reporting** — KPI cards, weekly charts, burn-down visualisations
- **User Roles & Permissions** — Developer, Team Lead, Project Manager, Admin
- **Multi-user Team Support** — teams with member management and role assignment
- **Mobile-Responsive UI** — full functionality from 375px to 1280px+
- **Dark Mode** — toggle between light and dark themes
- **OpenAPI Schema** — auto-generated docs at `/api/v1/schema/`

---

## Local Development Setup

### Prerequisites

- Python 3.12+
- Node.js 20+
- Docker & Docker Compose (optional, for containerised dev)

### Option 1: Docker (Recommended)

```bash
cp .env.example .env
docker-compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost:5173
- API Docs: http://localhost:8000/api/v1/schema/swagger/

### Option 2: Manual Setup

**Backend:**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements/development.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `DJANGO_SECRET_KEY` | Django secret key | `insecure-dev-key-change-me` |
| `DJANGO_DEBUG` | Enable debug mode | `True` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `DATABASE_URL` | PostgreSQL connection string | SQLite fallback |
| `CORS_ALLOWED_ORIGINS` | Allowed CORS origins | `http://localhost:5173` |
| `JWT_ACCESS_TOKEN_LIFETIME_MINUTES` | JWT access token lifetime | `60` |
| `JWT_REFRESH_TOKEN_LIFETIME_DAYS` | JWT refresh token lifetime | `7` |
| `VITE_API_BASE_URL` | API base URL for frontend | `http://localhost:8000` |

---

## API Overview

Base URL: `/api/v1/`

| Endpoint | Methods | Description |
|---|---|---|
| `/auth/register/` | POST | Register a new user |
| `/auth/login/` | POST | Obtain JWT token pair |
| `/auth/token/refresh/` | POST | Refresh access token |
| `/auth/me/` | GET, PATCH | Current user profile |
| `/teams/` | GET, POST | List/create teams |
| `/teams/{id}/members/` | GET, POST | Team members |
| `/projects/` | GET, POST | List/create projects |
| `/projects/{id}/time-summary/` | GET | Project time summary |
| `/tasks/` | GET, POST | List/create tasks |
| `/tasks/{id}/comments/` | GET, POST | Task comments |
| `/time-entries/` | GET, POST | List/create time entries |
| `/time-entries/my-log/` | GET | Personal daily log |
| `/reports/daily-summary/` | GET | Daily time summary |
| `/reports/weekly-summary/` | GET | Weekly time summary |
| `/reports/project-utilisation/` | GET | Project utilisation |
| `/reports/team-activity/` | GET | Team activity report |
| `/auth/admin/users/` | GET | Admin: list users |

Full OpenAPI schema: `/api/v1/schema/`

---

## Role Permissions

| Action | Developer | Team Lead | PM | Admin |
|---|:---:|:---:|:---:|:---:|
| Log own time | ✅ | ✅ | ✅ | ✅ |
| View own reports | ✅ | ✅ | ✅ | ✅ |
| Create/edit tasks | Own | Team | Team | ✅ |
| Create/manage projects | ❌ | ✅ | ✅ | ✅ |
| View team reports | ❌ | ✅ | ✅ | ✅ |
| Manage team members | ❌ | ✅ | ❌ | ✅ |
| View all teams/projects | ❌ | ❌ | ✅ | ✅ |
| Admin panel access | ❌ | ❌ | ❌ | ✅ |

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit using [conventional commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `chore:`, etc.
4. Push and open a Pull Request

### PR Checklist

- [ ] Code passes linting (`black`, `isort`, `eslint`, `prettier`)
- [ ] Tests pass (`pytest`, `vitest`)
- [ ] New features include tests
- [ ] No hardcoded secrets
- [ ] Mobile-responsive

---

## Running Tests

**Backend:**
```bash
cd backend
pytest --tb=short
```

**Frontend:**
```bash
cd frontend
npm run test -- --run
```

---

## Licence

MIT
