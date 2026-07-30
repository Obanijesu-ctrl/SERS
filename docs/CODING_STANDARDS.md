# SERS Coding Standards

Keep this short enough that people actually follow it. If a rule needs a
paragraph of justification, it's probably the wrong rule for a student
project on a deadline.

## 1. Structure

- **One responsibility per file.** Models describe data (`app/models/`).
  Routes handle HTTP in/out only — no business logic in a route function
  beyond calling into `routing_engine.py` or a model method
  (see `dashboard.py` for the pattern).
- **Blueprints by feature, not by HTTP verb.** `auth`, `dashboard`, `api` —
  not `get_routes.py` / `post_routes.py`.
- **No logic in templates beyond loops/conditionals.** If a template needs a
  calculation, compute it in the route and pass it in.

## 2. Naming

- `snake_case` for functions, variables, files. `PascalCase` for classes.
- Route functions named after what they return, not the HTTP verb:
  `community_detail`, not `get_community`.
- Boolean fields/flags read as a yes/no question: `is_active`, not `active`
  or `status`.

## 3. Python style

- Follow PEP 8. Run `black .` before committing if you want it automatic —
  not enforced by CI here, but keeps diffs clean in a group project.
- Type hints on function signatures where the type isn't obvious from the
  name (skip them for simple Flask view functions — not worth the noise).
- Docstrings on any function whose logic isn't self-evident from its name —
  see `routing_engine.py` for the level of detail expected. Skip docstrings
  on simple CRUD-style routes.

## 4. Database & models

- Every model gets a `__tablename__` — don't rely on Flask-SQLAlchemy's
  auto-naming, it gets confusing once you have 5+ models.
- Foreign keys are explicit (`db.ForeignKey("communities.id")`), not
  inferred.
- Migrations: for this prototype scope, `db.create_all()` on startup is
  fine. If the schema outlives this course, switch to Flask-Migrate before
  the second schema change — don't wait until it hurts.

## 5. Git workflow

- Branch per feature: `feature/routing-engine`, `fix/login-redirect`.
- Commit messages: imperative mood, one line summary under 50 chars —
  `Add battery safety floor to routing engine`, not
  `fixed some stuff with battery`.
- No commits directly to `main` once more than one person is on the repo —
  PR + one reviewer, even informally.
- **Never commit `sers.db`, `.env`, or `venv/`** — already covered by
  `.gitignore`, but double check `git status` before your first push.

## 6. Testing

- Every new routing rule gets a test in `tests/test_routing_engine.py`
  before it's considered done — the routing engine is the one part of this
  system a grader/user will poke at hardest, so it's the one part with the
  least room for silent bugs.
- Test names describe the scenario, not the function:
  `test_grid_selected_when_battery_low`, not `test_route_community_3`.

## 7. Secrets & config

- Nothing environment-specific is hardcoded — see `config.py`. Local dev
  uses defaults; production sets `SECRET_KEY` and `DATABASE_URL` as real
  environment variables on the host (Render env vars, not in the repo).

## 8. Commenting philosophy

- Comment *why*, not *what*. `# never drain battery below this` next to
  `BATTERY_SAFETY_FLOOR_PCT` is useful; `# set charge to 20` is noise.
- If a function needs a comment to explain what it does line-by-line,
  consider whether it should be two functions instead.
