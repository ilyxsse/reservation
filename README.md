# Meeting-Room Reservation System

A lightweight Django application that lets agency staff reserve meeting rooms in hourly slots during working hours (08:00 – 18:00) and allows administrators to manage rooms and view all bookings through a dedicated dashboard.

---

## Quick-start (development)

```bash
# 1. Create & activate a virtualenv
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables (optional for dev)
cp .env.sample .env

# 4. Initialise the database
python manage.py migrate

# 5. Create the first super-user (admin)
python manage.py createsuperuser

# 6. Run the dev server
python manage.py runserver
```

Visit [**http://127.0.0.1:8000**](http://127.0.0.1:8000/), log in with your admin credentials, and start adding rooms or booking them via the UI.

---

## Project layout

```
meetingroom_reservation/
│
├── config/           ← Django project settings & root URLs  
├── accounts/         ← Authentication (login, signup) & role helpers  
├── rooms/            ← CRUD for meeting rooms  
├── reservations/     ← CRUD + conflict checking for hourly bookings  
├── templates/        ← Shared layout & dashboards  
└── static/           ← CSS / JS (Bootstrap or Tailwind) and vendor assets  
```

Each app ships with its own templates for clarity; Django’s loader can still collect them globally.

---

## Environment variables

| Variable               | Default                   | Purpose                                      |
|------------------------|---------------------------|----------------------------------------------|
| `DJANGO_SETTINGS_MODULE` | `config.settings.dev`    | Selects the settings flavour                 |
| `SECRET_KEY`           | `dev-unsafe-change-me`    | Cryptographic key (override in production)   |
| `DEBUG`                | `1`                       | Development convenience; set to `0` in prod  |
| `ALLOWED_HOSTS`        | `*`                       | Comma-separated list of allowed hostnames in prod |

Copy `.env.sample` to `.env` and adjust values as needed.

---

## Running tests

```bash
pytest
```

*(No tests yet—add them as you build features.)*

---

## Deployment notes

- **Static files** are served by WhiteNoise in production—run:

  ```bash
  python manage.py collectstatic
  ```

- A production WSGI/ASGI server (e.g., Gunicorn/Uvicorn) should point at:

  ```python
  config.wsgi  # or config.asgi
  ```
