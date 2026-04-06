# AI_Services_Django

this project is a django backend for a recruitment flow.
it keeps your full learning scope (jwt, redis, celery, celery beat, custom user model), but organized in a cleaner beginner structure.


## 2) project structure 

`AI_Services_Django/` (project config package)
- `settings.py`: global config (db, jwt, redis, celery, installed apps)
- `urls.py`: top-level urls (`/api/public/`, `/api/internal/`, `/api/`, jwt, admin)
- `celery.py`: celery app bootstrap
- `asgi.py` / `wsgi.py`: deployment entrypoints
- `__init__.py`: exposes celery app

`recruitment/` (main business app)
- `models.py`: Organization, JobPosting, Candidate, Resume, DailyStats
- `views.py`: public/internal views + drf viewsets
- `serializers.py`: candidate/resume serializers
- `tasks.py`: resume parsing task + daily stats task
- `middleware.py`: logs user id + ip when resume endpoints are accessed
- `permissions.py`: `IsDepartmentHead`
- `drf_urls.py`: router for `candidates` and `resumes`
- `urls_public.py`: public routes
- `urls_internal.py`: internal routes
- `admin.py`: admin customization + bulk action + read-only stats admin
- `migrations/`: schema history

`users/` (custom auth app)
- `models.py`: custom user model with email login
- `managers.py`: create_user/create_superuser logic
- `admin.py`: user admin configuration
- `apps.py`, `migrations/`, `__init__.py`: app package setup

root files:
- `manage.py`: django command entry
- `Dockerfile`: image build steps
- `docker-compose.yml`: web + db + redis + celery worker + celery beat
- `.env` / `.env.dev`: environment configs
- `requirements.txt`: minimal dependencies for current features
- `learning_document.md`: your learning notes

## 3) current feature checklist

- models + orm + jsonfield for ai skills
- migration with `RunPython` for `priority_score`
- admin customization + bulk status action
- custom user model with email login
- middleware logging user id and ip on resume access
- cbvs for public jobs and apply endpoint
- url namespacing for public/internal
- drf viewset/serializer with file upload
- simplejwt auth
- redis cache + celery broker/result backend
- celery task for resume parsing
- celery beat daily stats task at midnight
- docker + docker compose
- environment-based config via `.env`

## 4) run locally

1. install dependencies
```bash
pip install -r requirements.txt
```
2. start docker services
```bash
docker compose up --build
```
3. apply migrations
```bash
python manage.py migrate
```
4. run server (if not using web container command)
```bash
python manage.py runserver
```

## 5) api summary

public:
- `GET /api/public/jobs/`
- `POST /api/public/apply/`

internal:
- `GET /api/internal/jobs/`

drf (jwt required):
- `/api/candidates/`
- `/api/resumes/`

auth:
- `POST /api/token/`
- `POST /api/token/refresh/`

utility:
- `GET /test-cache/`
