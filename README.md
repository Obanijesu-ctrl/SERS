# SERS — Smart Energy Routing System

An automated routing prototype that decides, in real time, whether a community
should draw power from **solar**, **battery**, or the **grid** — built for
Kiyovu Cell and Agatare Cell in Kigali, Rwanda.

## What it does

- Runs a rule-based routing engine that picks the best available power
  source for each community based on live solar output, battery charge, and
  grid availability (see `app/routing_engine.py`).
- Logs every routing decision with a human-readable reason, so the dashboard
  can show *why* a source was chosen, not just *which* one.
- Lets an operator manually activate/deactivate a source (e.g. to simulate
  maintenance or a fault) and watch the engine re-route around it.
- User accounts (signup/login) so the dashboard isn't public.

## Tech stack

Python 3.11+, Flask, Flask-SQLAlchemy, Flask-Login, SQLite (dev) — no
frontend framework, server-rendered Jinja templates.

---

## 1. Setup — run it locally

These are the exact steps to get SERS running on your machine from a clean
clone. Tested on macOS/Linux; on Windows use `venv\Scripts\activate` instead
of `source venv/bin/activate`.

```bash
# 1. Clone the repo
git clone <YOUR_GITHUB_REPO_URL>
cd sers

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python run.py
```

The app starts at **http://127.0.0.1:5000**. On first run it automatically
creates the SQLite database (`sers.db`) and seeds:

- An admin account — `username: admin`, `password: admin123`
- Two communities (Kiyovu Cell, Agatare Cell), each with solar, battery, and
  grid sources pre-configured so the routing engine has something to decide
  on immediately.

Log in, land on the dashboard, click into a community, and toggle a source
on/off to see the engine re-route.

## 2. Run the tests

```bash
pip install pytest   # if not already installed via requirements.txt
pytest tests/ -v
```

7 tests cover the routing engine's decision rules and the auth flow.

## 3. Deploy (public URL)

The repo ships with a `render.yaml` and `Procfile` for a one-click deploy on
[Render](https://render.com) (free tier):

1. Push this repo to GitHub (public).
2. On Render: **New → Blueprint**, connect the repo, Render reads
   `render.yaml` automatically.
3. Render builds with `pip install -r requirements.txt` and starts with
   `gunicorn run:app`.
4. Once deployed, Render gives you a public URL like
   `https://sers-xxxx.onrender.com` — that's what goes in your submission doc.

Any other Python-friendly host (Railway, Fly.io, PythonAnywhere) works the
same way — just point it at `run.py` / `gunicorn run:app`.

> **Note on the database:** the app ships with SQLite for simplicity, which
> is fine for this demo. On Render's free tier the filesystem is ephemeral,
> so the seed data re-populates on every restart — that's expected behavior
> for this prototype, not a bug.

## 4. Project structure

```
sers/
├── app/
│   ├── __init__.py          # app factory
│   ├── extensions.py        # db, login_manager instances
│   ├── routing_engine.py    # core solar/battery/grid decision logic
│   ├── seed.py               # demo data (admin user, communities, sources)
│   ├── models/
│   │   ├── user.py
│   │   └── energy.py         # Community, EnergySource, RoutingLog
│   ├── routes/
│   │   ├── auth.py           # signup / login / logout
│   │   ├── dashboard.py      # main views + source toggling
│   │   └── api.py            # JSON endpoints
│   ├── templates/
│   └── static/css/
├── tests/
├── config.py
├── run.py
├── requirements.txt
├── render.yaml
├── Procfile
└── docs/
    ├── CODING_STANDARDS.md
    └── SUBMISSION_CHECKLIST.md
```

## 5. Mapping to the SRS

| SRS requirement | Where it's implemented |
|---|---|
| Automated routing between solar/battery/grid | `app/routing_engine.py::route_community` |
| Actors: community, system operator | `User.role` (admin/operator), `Community` model |
| Manual override / maintenance mode | `dashboard.toggle_source` — deactivate a source |
| Decision logging / auditability | `RoutingLog` model + community history table |
| Multi-community support (Kiyovu, Agatare) | Seeded in `app/seed.py`, extensible via `Community` model |
| User authentication | `app/routes/auth.py` (Flask-Login) |

## 6. Known limitations (prototype scope)

- Solar output, battery charge, and grid status are simulated seed values,
  not connected to real sensors/IoT hardware — swapping in live telemetry
  would mean replacing the static fields on `EnergySource` with a polling
  source, without changing `routing_engine.py`'s decision logic.
- Single environment (no staging/prod split) — fine for a course prototype.
