# AI Resume Screening Automation System

A beginner-friendly full-stack Django project for recruiters. It lets recruiters create jobs, upload PDF resumes, parse candidate data, score resumes against job requirements, manage candidate status, send email notifications, and view analytics.

## Tech Stack

- **Python + Django**: backend framework, routing, templates, authentication, ORM, and admin.
- **Django Templates + Bootstrap**: server-rendered UI with responsive styling.
- **PostgreSQL**: production database for users, jobs, candidates, scores, and statuses.
- **Celery + Redis**: background jobs for PDF parsing, scoring, and email sending.
- **pdfplumber**: extracts text from uploaded PDF resumes.
- **SMTP Email**: sends shortlist and rejection notifications.
- **Render/GitHub ready**: includes `requirements.txt`, `Procfile`, `render.yaml`, and environment-based settings.

## Project Structure

```text
resume_screening/
  settings.py          # Django configuration, PostgreSQL, static files, Celery, email
  urls.py              # Main URL router
  celery.py            # Celery app setup
accounts/              # Registration, login, custom recruiter user
recruiter/             # Job openings and required skills
resumes/               # Resume upload, parsing, scoring, status, email tasks
dashboard/             # Analytics dashboard
templates/             # Bootstrap HTML templates
static/                # CSS and frontend assets
```

## Phase 1: Django Setup

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and update values. Django reads secrets and service URLs from environment variables so passwords are not committed to GitHub.

For quick local learning, this workspace includes a `.env` that uses `sqlite:///db.sqlite3` and `CELERY_TASK_ALWAYS_EAGER=True`. That lets you try the app without installing PostgreSQL and Redis first. For the required production-style setup, switch `DATABASE_URL` back to PostgreSQL and set `CELERY_TASK_ALWAYS_EAGER=False`.

## Phase 2: Authentication

The `accounts` app defines a custom `User` model in `accounts/models.py`. It extends Django's `AbstractUser` and adds recruiter-specific fields such as `role` and `company_name`.

The registration form in `accounts/forms.py` uses Django's `UserCreationForm`, which already knows how to validate passwords securely.

## Phase 3: Job Management

The `recruiter` app stores job openings. Each `JobOpening` belongs to one recruiter and contains:

- title
- description
- required skills
- minimum experience
- active/inactive status

The `skill_list()` method converts comma-separated skills into lowercase Python lists for matching.

## Phase 4: Resume Upload

The `resumes` app stores each uploaded PDF in the `media/` folder using Django's `FileField`. Each `Candidate` is linked to a job opening with a foreign key.

When a recruiter uploads a resume, the view creates a candidate record and queues a Celery task:

```python
process_resume.delay(candidate.id)
```

## Phase 5: PDF Parsing

`resumes/parser.py` uses `pdfplumber` to read every page of a PDF and extract text. It then uses simple beginner-friendly regular expressions to find:

- email address
- likely candidate name
- common skills
- years of experience

In real hiring systems, you can improve this with NLP models and larger skill dictionaries.

## Phase 6: Candidate Scoring

`resumes/scoring.py` gives 80 points for skill overlap and 20 points for experience match.

Example: if a job needs 4 skills and the resume has 3 of them, skill score is `3 / 4 * 80 = 60`. If the candidate meets the experience requirement, they get the full 20 experience points.

## Phase 7: Async Processing With Celery

Celery runs slow work outside the web request. Redis acts as the message broker.

Start Redis, then run:

```bash
celery -A resume_screening worker --loglevel=info
```

Start Django in another terminal:

```bash
python manage.py runserver
```

Now resume parsing and email sending happen in the background.

## Phase 8: Dashboard Analytics

The `dashboard` app aggregates candidate data with Django ORM queries:

- total resumes
- shortlisted count
- rejected count
- review count
- average score
- top candidates

Chart.js renders the status chart in the dashboard template.

## Phase 9: Email Automation

When a recruiter changes a candidate to `Shortlisted` or `Rejected`, the app queues `send_candidate_status_email`.

Configure SMTP in `.env`. For Gmail, use an app password instead of your normal password.

For local learning, you can use Django's console email backend:

```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

This prints emails in the terminal instead of sending real messages.

## Phase 10: Deployment

For Render:

1. Push this project to GitHub.
2. Create a Render Blueprint using `render.yaml`, or create services manually.
3. Add PostgreSQL and Redis services.
4. Set environment variables from `.env.example`.
5. Run migrations during deploy.
6. Create a superuser from the Render shell:

```bash
python manage.py createsuperuser
```

## Local Database Setup

Create a PostgreSQL database named `resume_screening`, then set:

```env
DATABASE_URL=postgres://postgres:postgres@localhost:5432/resume_screening
```

Run:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Important Beginner Concepts

**Django app**: a focused module. This project uses separate apps so authentication, jobs, resumes, and analytics stay organized.

**Model**: a Python class that becomes a database table.

**View**: a function that handles a web request and returns a response.

**Template**: an HTML file that displays data from a view.

**URL route**: connects a browser path such as `/jobs/` to a view function.

**ORM**: Django's Python way to query the database without writing raw SQL.

**Celery task**: a function that runs in a separate worker process so users do not wait while PDFs are parsed or emails are sent.

**Environment variable**: a secret or setting stored outside the code, such as `SECRET_KEY`, `DATABASE_URL`, and email passwords.

## Next Improvements

- Add pagination for large candidate lists.
- Add unit tests for parsing and scoring.
- Add richer skill extraction using NLP.
- Store resumes in S3 for production.
- Add recruiter teams and permissions.
