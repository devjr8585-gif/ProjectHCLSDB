# Project Documentation — ProjectHCLSDB

## Project Overview
- Project: HclsPro (Healthcare Clinic/Employee Management)
- Location: workspace root
- Purpose: Web application providing admin dashboards, user/session management, and a REST API for hospital resources (admin types, employees, doctors, patients).

## High-level Features Implemented
- Admin registration, activation, login, logout and session management (1-hour expiry).
- Admin types with role-based redirects: MAdmin (manager) and OpAdmin (operational).
- Access control via decorators (`already_authenticated` and `login_required`).
- REST API endpoints for AdminType, AdminLogin, Department, Employee, Doctor, Receptionist, Helper, Patient, CheckLogin.
- Swagger/OpenAPI docs available via `/swagger/` and `/redoc/`.
- Passwords are hashed in model `save()` methods.
- File upload support for avatars (media/avatars/).

## Technologies Used
- Python
- Django 6.0.2 (project created with this version)
- Django REST Framework (`rest_framework`) for API
- drf_yasg for Swagger/OpenAPI documentation
- Database configured: MySQL (in `HclsPro/HclsPro/settings.py`) — DB name `hclsdb`, user `root` (credentials stored in settings). Note: `db.sqlite3` exists in the repo root but current settings use MySQL.
- Frontend assets: Bootstrap CSS/JS (static files in `static/`), custom templates in `templates/`.
- Virtual environment: `prohclsenv` (contains `Scripts/activate`)

## Important Files & Where to Find Them
- Implementation guide: [SESSION_IMPLEMENTATION_GUIDE.md](SESSION_IMPLEMENTATION_GUIDE.md)
- Django settings: [HclsPro/HclsPro/settings.py](HclsPro/HclsPro/settings.py)
- Project URLs + Swagger setup: [HclsPro/HclsPro/urls.py](HclsPro/HclsPro/urls.py)
- Main apps:
  - UI app: [HclsApp](HclsApp)
  - API app: [HclsWebApi](HclsWebApi)
- API serializers: [HclsWebApi/Serializer.py](HclsWebApi/Serializer.py)
- API models: [HclsWebApi/models.py](HclsWebApi/models.py)
- Templates: `templates/Admin/` (subfolders `Anonymous`, `MAdmin`, `OpAdmin`)
- Static assets: `static/css`, `static/js`, `static/Images`
- Media uploads: `media/avatars/`

## Project Structure (concise)
- `HclsPro/` — Django project
  - `HclsPro/settings.py` — settings (INSTALLED_APPS includes `rest_framework`, `drf_yasg`, `HclsApp`, `HclsWebApi`)
  - `urls.py` — includes app routes and Swagger endpoints
- `HclsApp/` — views/templates and session/auth decorators
- `HclsWebApi/` — models, serializers, API views and routes
- `templates/` — HTML templates for admin UI
- `static/` — Bootstrap and custom styles/scripts
- `media/` — uploaded user images
- `prohclsenv/` — virtual environment

## Data Models (summary)
- AdminType, AdminLogin, Department, Employee, Doctor, Receptionist, Helper, Patient, CheckLogin, PasswordResetToken
- Notable behaviors:
  - Password fields are hashed in `save()` for `AdminLogin`, `Employee`, `CheckLogin`.
  - `CheckLogin` holds registration/admin profile data used by UI registration flow.

## API Highlights
- APIView-based endpoints in `HclsWebApi/views.py` with `swagger_auto_schema` docs.
- Endpoints are routed under `api/` via `HclsWebApi.Hclswebapiurls`.
- Example behaviors: list/create/update/delete for AdminType and AdminLogin, register/login endpoints for `CheckLogin`/`AdminLogin` flows.

## Security & Config Notes
- Sessions: Session middleware is enabled (`SessionMiddleware`) and session data is used for dashboards. Session expiry set in code to 3600 seconds (1 hour).
- Password hashing implemented at model level.
- Current settings store `SECRET_KEY` and DB credentials in plaintext in `settings.py` — remove or move to environment variables before production.
- Email backend is set to console for development (`EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`).

## How to Run (development)
1. Activate virtualenv:

```powershell
prohclsenv\Scripts\Activate.ps1   # PowerShell
# or
prohclsenv\Scripts\activate.bat    # cmd
```

2. Install dependencies (create a `requirements.txt` if missing). Minimal required packages:

```text
Django==6.0.2
djangorestframework
drf-yasg
mysqlclient   # if using MySQL
```

Install with:

```bash
pip install -r requirements.txt
```

3. Run migrations (if DB configured and available):

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Run dev server:

```bash
python manage.py runserver
```

5. Open:
- UI: `http://127.0.0.1:8000/`
- Swagger: `http://127.0.0.1:8000/swagger/`
- Redoc: `http://127.0.0.1:8000/redoc/`

## Files Changed / Custom Implementations (from implementation guide)
- `HclsWebApi/models.py` — `admin_type` / `CheckLogin` model fields and password hashing
- `HclsApp/views.py` — session creation, login/logout, decorators applied
- `HclsApp/decorators.py` — `login_required`, `already_authenticated`
- `HclsApp/HclsAppurls.py` — added logout route
- `templates/Admin/Anonymous/*.html` — login/register templates updated
- `templates/Admin/logout_snippet.html` — logout UI snippet

## Recent Work (April 2026)
These are changes made while converting admin handling and adding an initial Abstract Repository Pattern implementation.

- **UI / CSS**: added circular status badge styles and updated MAdmin dashboard to show OpAdmin Active/Inactive as circle badges.
  - File: [HclsPro/static/css/mystyles.css](HclsPro/static/css/mystyles.css#L1-L200)
  - File: [HclsPro/templates/Admin/MAdmin/dashboard.html](HclsPro/templates/Admin/MAdmin/dashboard.html#L1-L400)

- **Keep admin data in one table**: `CheckLogin`-based registrations and MAdmin-created OpAdmins now also create corresponding rows in `AdminLogin` so all admins are stored in the `AdminLogin` table.
  - File: [HclsPro/HclsApp/views.py](HclsPro/HclsApp/views.py#L1-L520)

- **Repository pattern (starter)**: added an abstract repository interface and a Django ORM implementation to centralize admin operations.
  - File: [HclsPro/HclsApp/repositories/base.py](HclsPro/HclsApp/repositories/base.py#L1-L200)
  - File: [HclsPro/HclsApp/repositories/django_admin_repository.py](HclsPro/HclsApp/repositories/django_admin_repository.py#L1-L200)

- **Backfill command**: management command to backfill `AdminLogin` rows from existing `CheckLogin` records using the repository logic.
  - File: [HclsPro/HclsWebApi/management/commands/backfill_adminlogin.py](HclsPro/HclsWebApi/management/commands/backfill_adminlogin.py#L1-L200)

- **Notes from running backfill**: when the backfill was run, some rows failed due to database constraints:
  - MySQL error: "Data too long for column 'Gender'" — some `CheckLogin.gender` values exceed the `AdminLogin.Gender` `max_length` (10). The repository truncates long gender strings to avoid this.
  - Some rows failed with "Column 'AdminType' cannot be null" when no matching `AdminType` row existed; the repository attempts sensible mapping (1=MAdmin, 2=OpAdmin) but missing DB rows will still fail.

### How to run the backfill
1. Back up your database.
2. From project root run:
```bash
python manage.py backfill_adminlogin
```

If you want, I can:
- run the backfill here and fix the remaining data issues, or
- add a Django signal-based approach to automatically keep `AdminLogin` in sync with `CheckLogin`, or
- continue converting more views/models to use repository interfaces.

## Known Discrepancies / Notes to Fix
- Repo contains `db.sqlite3` but `settings.py` config uses MySQL. Confirm intended DB and update `settings.py` or remove `db.sqlite3` if obsolete.
- `SECRET_KEY` and DB credentials are in `settings.py` — move to environment variables.
- Some `HclsApp/models.py` is empty; most models live in `HclsWebApi/models.py`.

## Recommended Next Steps
- Move secrets to environment variables and update `settings.py` to read them.
- Add `requirements.txt` listing exact package versions.
- Add unit tests for auth/session flows and API endpoints.
- Implement email-based account activation and password-reset flows (currently token model exists).
- Review and tighten permission checks on API views (use DRF permissions/classes).
- Remove debug settings and enable HTTPS/CORS/CSRF hardening for production.

## Where to Read More in This Repo
- Implementation details and feature list: [SESSION_IMPLEMENTATION_GUIDE.md](SESSION_IMPLEMENTATION_GUIDE.md)
- Settings & config: [HclsPro/HclsPro/settings.py](HclsPro/HclsPro/settings.py)
- API models: [HclsWebApi/models.py](HclsWebApi/models.py)
- API serializers: [HclsWebApi/Serializer.py](HclsWebApi/Serializer.py)
- API views: [HclsWebApi/views.py](HclsWebApi/views.py)

---

If you want, I can:
- Generate `requirements.txt` from current environment,
- Add a `README.md` with run instructions,
- Move secrets into environment variables and patch `settings.py`.

Which of these would you like me to do next?