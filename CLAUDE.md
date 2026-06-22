# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository contains two independent projects plus standalone scripts:

1. **智能数学解题智能体 (Math Solver)** — A FastAPI + DeepSeek API math problem-solving app with a streaming SSE frontend.
2. **Score Management System** — A JWT-authenticated Express + Vue 3 score tracking app with role-based access.
3. **Standalone scripts** — Reference docs (`reference/`) and retrieval utilities (`Retrieve.py`).

---

## Project 1: Math Solver (Root)

A FastAPI app that sends math problems to DeepSeek's reasoning model and displays the thinking process + final answer via Server-Sent Events.

### Stack
- **Backend**: Python 3.10+ / FastAPI / Uvicorn / OpenAI SDK (DeepSeek API)
- **Frontend**: Static HTML / vanilla CSS / vanilla JS + MathJax 3
- **Testing**: pytest + httpx
- **Config**: `.env` file with `DEEPSEEK_API_KEY`

### Getting Started

```bash
pip install -r requirements.txt
cp .env.example .env    # then fill in DEEPSEEK_API_KEY
uvicorn app.main:app --reload
# Open http://localhost:8000
```

### Tests

```bash
pytest tests/              # All tests (no real API calls — uses fakes)
pytest tests/test_solver.py -v  # Run a specific test file
```

### Architecture

```
app/
  main.py     — FastAPI entry: GET / (HTML), POST /api/solve (JSON), GET /api/solve/stream (SSE)
  solver.py   — DeepSeek API client: solve() for non-stream, solve_stream() for SSE streaming
  schemas.py  — Pydantic models (SolveRequest, SolveResponse)
  config.py   — Env-based DeepSeek config with require_api_key() guard
static/
  index.html  — Two-panel layout (reasoning / answer) with MathJax rendering
  app.js      — EventSource client that streams reasoning_content + content
  style.css   — Clean responsive grid layout
tests/
  conftest.py — FakeDelta/FakeChoice/FakeChunk/FakeClient test doubles
  test_solver.py — Unit tests for solver logic (no network calls)
```

### API

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Serves `index.html` |
| `/api/solve` | POST | Non-streaming: `{"problem": "..."}` → `{"reasoning", "answer"}` |
| `/api/solve/stream` | GET | SSE stream: `?problem=...` → typed events (`reasoning` / `answer` / `done` / `error`) |

- Math formulas use LaTeX (`\(...\)` / `\[...\]`); the frontend renders with MathJax 3.
- DeepSeek's `thinking` mode is enabled via `extra_body` for chain-of-thought reasoning.
- `SYSTEM_PROMPT` in `solver.py` asks for step-by-step deduction, LaTeX formatting, and a `\boxed{}` final answer.

---

## Project 2: Score Management System (`score-system/`)

A full-stack score tracking app with JWT auth, role-based routing, and Excel export.

### Stack
- **Backend**: Node.js / Express / MySQL (mysql2) / JWT (jsonwebtoken) / bcryptjs / excel4node
- **Frontend**: Vue 3 / Vite / Vue Router / Pinia / Axios / Element Plus
- **Backend port**: 3001 (configurable via `PORT` env var)

### Getting Started

```bash
# Backend
cd score-system/backend
cp .env.example .env   # configure DB + JWT_SECRET
npm install
npm run dev            # with nodemon, or npm start

# Frontend
cd score-system/frontend
npm install
npm run dev            # Vite dev server, typically :5173
npm run build          # Production build
```

### Architecture

```
score-system/backend/
  src/
    index.js                  — Express entry, CORS + JSON middleware, route mounting
    db/pool.js                — MySQL2 connection pool
    db/init.js                — Schema initialization
    middleware/auth.js        — JWT verification middleware
    routes/
      auth.js                 — login / register
      scores.js               — CRUD scores + report + Excel export
      admin.js                — User/student/course management
score-system/frontend/
  src/
    main.js                   — Vue app bootstrap
    App.vue                   — Root component
    router/index.js           — Route defs with auth/role guards
    store/auth.js             — Pinia auth store
    api/index.js              — Axios client with Bearer token interceptor
    views/
      Login.vue               — Auth page
      Dashboard.vue           — Post-login dashboard
      Scores.vue              — Score entry/list (teacher, student)
      Report.vue              — Reporting (teacher, admin)
      Admin.vue               — Admin panel (admin only)
      countdown/CountdownPage.vue  — Standalone countdown timer
```

### Route Guards

| Route | Auth Required | Role |
|---|---|---|
| `/login` | No | — |
| `/dashboard` | Yes | any |
| `/scores` | Yes | teacher, student |
| `/report` | Yes | teacher, admin |
| `/admin` | Yes | admin |
| `/countdown` | No | — |

### Backend Routes

| Prefix | Module |
|---|---|
| `/api/auth` | login, register |
| `/api/scores` | CRUD, report, Excel export |
| `/api/admin` | user/student/course management |
| `/api/utils` | strlen, utilities |

---

## Standalone Scripts

- **`Retrieve.py`** — Apify-based Baidu homepage scraper with CLI args (`--output json`, `--simple`, `--save`)
- **`reference/Catetory-guide.md`** — SQL statement type classification rules (memory-style doc)
