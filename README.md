# Stack-Battle KE — Backend API

A gamified competitive programming platform for Kenyan students.
Built with Flask, PostgreSQL (Supabase), JWT auth, and the Piston code execution API.

---

## Tech Stack

| Layer          | Technology                        |
|----------------|-----------------------------------|
| Framework      | Flask 3.0                         |
| Database       | PostgreSQL via Supabase            |
| ORM            | Flask-SQLAlchemy                  |
| Migrations     | Flask-Migrate (Alembic)           |
| Serialization  | Marshmallow                       |
| Authentication | Flask-JWT-Extended                |
| Passwords      | Werkzeug                          |
| Code Execution | Piston API                        |
| Deployment     | Render.com + Gunicorn             |

---

## Quickstart

### 1. Clone and create a virtual environment

```bash
git clone <repo-url>
cd stack_battle_ke
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Fill in DATABASE_URL, SECRET_KEY, JWT_SECRET_KEY
```

### 3. Run database migrations

```bash
flask db init        # only once — initialises the migrations/ folder
flask db migrate -m "initial tables"
flask db upgrade
```

### 4. Seed the database

```bash
python seed.py
```

### 5. Start the development server

```bash
python run.py
# API available at http://localhost:5000
```

---

## Running Tests

```bash
pytest tests/ -v
```

Tests use an in-memory SQLite database — your development DB is never touched.

---

## API Reference

### Auth

| Method | Endpoint              | Auth     | Description                        |
|--------|-----------------------|----------|------------------------------------|
| POST   | /auth/check-email     | Public   | Check if email is registered       |
| POST   | /auth/register        | Public   | Register a new user                |
| POST   | /auth/login           | Public   | Log in, receive JWT                |
| GET    | /auth/me              | JWT      | Get current user profile           |

### Users

| Method | Endpoint              | Auth | Description                        |
|--------|-----------------------|------|------------------------------------|
| GET    | /users/profile        | JWT  | Get own full profile               |
| PUT    | /users/profile        | JWT  | Update name, bio, avatar           |
| GET    | /users/\<id\>         | JWT  | Get any user's public profile      |

### Institutions

| Method | Endpoint              | Auth   | Description                        |
|--------|-----------------------|--------|------------------------------------|
| GET    | /institutions/        | Public | List all institutions              |

### Challenges

| Method | Endpoint                  | Auth | Description                        |
|--------|---------------------------|------|------------------------------------|
| GET    | /challenges/              | JWT  | List all challenges (paginated)    |
| GET    | /challenges/practice      | JWT  | Practice challenges only           |
| GET    | /challenges/weekly        | JWT  | Active weekly challenge            |
| GET    | /challenges/\<id\>        | JWT  | Single challenge with test cases   |

### Submissions

| Method | Endpoint                  | Auth | Description                        |
|--------|---------------------------|------|------------------------------------|
| POST   | /submit-code              | JWT  | Submit code for a challenge        |
| GET    | /results                  | JWT  | Own submission history (paginated) |
| GET    | /results/\<id\>           | JWT  | Single submission result           |

### Groups

| Method | Endpoint                  | Auth | Description                        |
|--------|---------------------------|------|------------------------------------|
| POST   | /groups/                  | JWT  | Create a new group                 |
| GET    | /groups/                  | JWT  | List groups you belong to          |
| POST   | /groups/join              | JWT  | Join a group by invite code        |
| GET    | /groups/\<id\>            | JWT  | Group details + member list        |

### Friends

| Method | Endpoint                        | Auth | Description                      |
|--------|---------------------------------|------|----------------------------------|
| POST   | /friends/request                | JWT  | Send a friend request            |
| PUT    | /friends/\<id\>/status          | JWT  | Accept or reject a request       |
| GET    | /friends/                       | JWT  | List all accepted friends        |

### Leaderboard

| Method | Endpoint                        | Auth | Description                      |
|--------|---------------------------------|------|----------------------------------|
| GET    | /leaderboard/                   | JWT  | Global ranking by points         |
| GET    | /leaderboard/groups             | JWT  | Groups ranked by total points    |
| GET    | /leaderboard/weekly/\<week\>    | JWT  | Weekly challenge rankings        |

### Notifications

| Method | Endpoint                        | Auth | Description                      |
|--------|---------------------------------|------|----------------------------------|
| GET    | /notifications/                 | JWT  | Last 50 notifications            |
| PUT    | /notifications/\<id\>/read      | JWT  | Mark a notification as read      |

---

## Scoring System

| Difficulty | Points |
|------------|--------|
| Easy       | 50     |
| Medium     | 100    |
| Hard       | 200    |
| Weekly bonus (full marks) | +50 |

Partial credit: `score = (passed_tests / total_tests) × points_reward`

### Rank Tiers

| Tier         | Points Range |
|--------------|--------------|
| Beginner     | 0 – 200      |
| Intermediate | 201 – 500    |
| Advanced     | 501 – 1000   |
| Elite        | 1000+        |

---

## Folder Structure

```
backend/
├── app/
│   ├── __init__.py          ← App factory
│   ├── config.py            ← Dev / Prod / Test configs
│   ├── extensions/          ← db, migrate, jwt, ma instances
│   ├── models/              ← SQLAlchemy models (10 models)
│   ├── schemas/             ← Marshmallow schemas
│   ├── routes/              ← Flask Blueprints (9 blueprints)
│   ├── services/            ← Business logic layer
│   ├── utils/               ← Pagination, rate limiter, helpers
│   ├── middleware/          ← CORS, logging hooks
│   ├── errors/              ← JSON error handlers
│   └── seeds/               ← Seed data scripts
├── tests/                   ← pytest test suite
├── migrations/              ← Auto-generated by Flask-Migrate
├── run.py                   ← Dev entry point
├── seed.py                  ← Run seeds: python seed.py
├── render.yaml              ← Render.com deployment config
└── requirements.txt
```

---

## Deployment (Render.com)

1. Push code to GitHub
2. Create a new **Web Service** on Render, connect your repo
3. Set these environment variables in the Render dashboard:
   - `DATABASE_URL` — your Supabase pooler connection string
   - `SECRET_KEY` — a long random string
   - `JWT_SECRET_KEY` — another long random string
   - `FLASK_ENV` — `production`
4. Render auto-detects Python and runs `gunicorn "run:app"`
5. After first deploy, run `flask db upgrade` from the Render shell

---

## Security Notes

- Passwords are hashed with Werkzeug's `generate_password_hash` — never stored plain
- `password_hash` is excluded from all Marshmallow schemas
- JWT tokens expire after 7 days
- Never commit `.env` — it is listed in `.gitignore`
- Rate limiting on `/submit-code`: max 10 submissions per minute per user
# Bck-Test
