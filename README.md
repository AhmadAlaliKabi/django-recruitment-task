# AI_Services_Django

this project is a django backend for recruitment flow.
simple version of what it does:
- stores companies and job posts
- lets people apply
- uploads resumes
- parses resume pdf text in background
- exposes APIs for public use and internal use
- saves daily stats per job

## 1) Project Structure (what each part is)

`AI_Services_Django/`
- project config package
- global settings, global urls, celery bootstrap, asgi/wsgi entrypoints

`recruitment/`
- main business app
- models, serializers, views, tasks, urls, admin, migrations

`staticfiles/`
- collected static assets (mostly framework/vendor files)
- not core business logic

`manage.py`
- command entrypoint for runserver/migrate/etc

`docker-compose.yml` + `Dockerfile`
- container setup for local run

`requirements.txt`
- python dependencies

## 2) Data Model (how everything connects)

`Organization` -> has many `JobPosting`

`JobPosting` -> belongs to one `Organization`

`Candidate` -> applicant profile

`Resume` -> belongs to one `Candidate`, can optionally point to one `JobPosting`
- stores uploaded file
- stores extracted text
- stores extracted skills (json list)

`DailyStats` -> one row per (`job_posting`, `date`)
- stores application count for that day

## 3) API Map

Public:
- `GET /api/public/jobs/` -> active jobs list
- `POST /api/public/apply/` -> create candidate from json

Internal:
- `GET /api/internal/jobs/` -> all jobs with active/inactive state

DRF:
- `/api/candidates/` -> candidate CRUD (JWT required)
- `/resumes/` -> resume CRUD via DRF router (multipart upload supported)

Auth:
- `POST /api/token/`
- `POST /api/token/refresh/`

Utility:
- `GET /test-cache/` -> writes/reads redis cache key

## 4) Main Flow (end-to-end)

1. Candidate resume is uploaded to Resume endpoint.
2. `ResumeSerializer.create()` saves the row.
3. Serializer sends `parse_resume_task.delay(resume_id)` to celery.
4. Celery worker opens pdf, extracts text, parses skills with regex.
5. Resume row is updated with `extracted_text` and `ai_extracted_skills`.

Periodic flow:
1. Celery beat triggers `generate_daily_stats` every minute.
2. Task counts resumes per job.
3. Writes/updates `DailyStats` for today.

## 5) Stack Explanation (simple and practical)

### Django
django is the main web framework.
used here to define models, urls, views, admin, and overall project settings.

### Django REST Framework (DRF)
drf is for building APIs fast with serializers + viewsets.
used here for candidate and resume CRUD APIs.

### JWT (SimpleJWT)
jwt gives token-based auth for APIs.
used here to protect internal DRF routes (example: candidates endpoint).

### PostgreSQL
postgres is the relational database.
used here to store all models (organization/job/candidate/resume/daily stats).

### Redis
redis is an in-memory data store.
used here for:
- django cache backend (`CACHES`)
- celery broker/result backend (`REDIS_URL`)
- quick sanity check endpoint (`/test-cache/`)

### Celery
celery is a background task queue.
used here to run resume parsing outside request cycle so API stays responsive.

### Celery Beat
celery beat is a scheduler for periodic tasks.
used here to run daily stats generation every minute.

### pypdf
pypdf reads PDF files.
used here to extract raw text from uploaded resume files.

### Docker / Docker Compose
docker packages runtime environment.
compose runs services locally.
used here to run the web app in containerized local setup.

## 6) Important Notes (current state)

- `settings.py` references `users` app (`AUTH_USER_MODEL = 'users.User'`) but `users/` app is not in this repo.
- `.env` has db vars, but database config is currently hardcoded in `settings.py`.
- compose file currently starts only `web`; redis/celery/postgres services are not defined there yet.
- tests are still empty (`recruitment/tests.py`).

## 7) How to Run (current local idea)

1. install dependencies
```bash
pip install -r requirements.txt
```
2. run migrations
```bash
python manage.py migrate
```
3. start api
```bash
python manage.py runserver
```
4. (optional but needed for async features) run celery worker + beat in separate terminals
```bash
celery -A AI_Services_Django worker -l info
celery -A AI_Services_Django beat -l info
```

## 8) Quick Mental Model

think of this project as:
- django = core app shell
- recruitment app = business logic
- drf = clean api layer
- postgres = truth storage
- redis + celery = async engine
- beat = scheduled stats updates

that is the full picture of how it all connects.
