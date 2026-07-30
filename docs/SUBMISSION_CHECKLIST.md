# Submission Checklist — SERS Summative (due 30 July 2026)

Work top to bottom. Each item maps to a rubric line so nothing costs you
points silently.

## Code & repo (5 pts — "Code availability requirements")

- [ ] Push this project to a **public** GitHub repo.
- [ ] Repo name is clear (e.g. `sers-smart-energy-routing`).
- [ ] README setup steps tested on a clean clone — you already have this;
      just re-verify after pushing (clone into a fresh folder and follow
      your own README exactly).
- [ ] `.gitignore` is committed so `sers.db`, `venv/`, `.env` never land in
      the repo (already set up).

```bash
cd sers
git init
git add .
git commit -m "Initial commit: SERS prototype"
git branch -M main
git remote add origin <YOUR_NEW_GITHUB_REPO_URL>
git push -u origin main
```

Then on GitHub: **Settings → General → Danger Zone** is NOT needed — a new
repo is public by default unless you chose private at creation. Double-check
the repo visibility badge says "Public."

## Deployment (5 pts — "Solution Deployment")

- [ ] Deploy via `render.yaml` (see README §3) or an equivalent host.
- [ ] Confirm the public URL loads **in an incognito window** (so you're
      testing it the way a grader with no session/cookies will see it).
- [ ] Confirm login/signup work on the deployed version, not just localhost.

## Video (5 pts presentation + 10 pts requirements coverage)

5–10 minutes, covering in order:

1. **System description** (30–60s) — SERS routes power automatically
   between solar, battery, and grid for Kiyovu and Agatare Cells in Kigali.
2. **Problem statement** — why manual/static switching between power
   sources is inefficient or unreliable for these communities.
3. **Why it's a problem** — cost of grid dependence, wasted solar capacity,
   battery mismanagement, outages.
4. **Proposed solution** — the rule-based routing engine, explained in
   plain terms (solar first, battery second, grid fallback).
5. **Demo** — screen-share the deployed URL:
   - Sign up for a new account (shows the signup flow working).
   - Log in.
   - Show the dashboard: point out Kiyovu on solar vs. Agatare on grid,
     and explain *why* (read the reason text on screen).
   - Go into a community, deactivate a source, refresh, show the engine
     re-route around it.
   - Show the routing history table as your audit trail.
- [ ] Audio is clear, you narrate rather than read silently.
- [ ] Screen recording software confirmed working (test a 10-second clip
      first) before recording the full take.

## Documents (rolled into the rubric criteria above — but zero points if missing/broken links)

- [ ] Create the Google Doc: `personNames_Summative_07302026`
- [ ] Paste: video link (grant "Anyone with the link can view")
- [ ] Paste: GitHub repo link (public)
- [ ] Paste: SRS document link (grant view access)
- [ ] Paste: deployed public URL
- [ ] Open every link in an incognito window before submitting — this is
      the single most common way people lose points on this rubric.

## Operation (5 pts)

- [ ] Login works.
- [ ] Signup works.
- [ ] Source activate/deactivate buttons work and visibly change state.
- [ ] Page redirects (login → dashboard, logout → login) work.
- [ ] If anything is buggy and you don't have time to fix it, **say so
      explicitly in the video** — the rubric penalizes unmentioned bugs
      harder than disclosed ones.

## Final gate before you submit on Canvas

- [ ] Google Doc sharing is set to "Anyone with the link"
- [ ] Every link opens in a fresh incognito tab with no errors
- [ ] Canvas submission is the Google Doc link, submitted before the
      30 July 2026 deadline
