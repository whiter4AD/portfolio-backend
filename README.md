# Portfolio Backend v2 — FastAPI + Supabase + JWT Auth

## What's new in v2
- **JWT authentication** — POST/PATCH/DELETE endpoints are protected. Only you can write data.
- **Live frontend** — `portfolio.html` now fetches projects directly from the API.

## Stack
- **FastAPI** — Python web framework
- **Supabase** — PostgreSQL database (free tier)
- **python-jose** — JWT token creation & verification
- **passlib/bcrypt** — password hashing

## Project Structure
```
portfolio-backend/
├── app/
│   ├── main.py                  # FastAPI app + CORS
│   ├── core/
│   │   ├── config.py            # env vars
│   │   ├── supabase.py          # Supabase client
│   │   └── security.py          # JWT + bcrypt utils
│   ├── routers/
│   │   ├── auth.py              # Login, /me, /hashpw
│   │   ├── projects.py          # CRUD (GET=public, writes=🔒)
│   │   └── blog.py              # CRUD (GET=public, writes=🔒)
│   └── schemas/
│       ├── project.py
│       └── post.py
├── portfolio.html               # Frontend — fetches live data
├── supabase_schema.sql          # Run once in Supabase SQL Editor
├── requirements.txt
└── .env.example
```

## Quick Start

### 1. Set up Supabase
1. Go to [supabase.com](https://supabase.com) → New Project
2. Open **SQL Editor** and run `supabase_schema.sql`
3. Copy your `URL` and `anon` key from **Project Settings → API**

### 2. Configure environment
```bash
cp .env.example .env
# Fill in SUPABASE_URL, SUPABASE_KEY, JWT_SECRET, ADMIN_USERNAME
```

### 3. Generate your password hash
```bash
# Install deps & start server first
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# In browser, visit:
# http://localhost:8000/api/auth/hashpw?password=YourChosenPassword
# Copy the "hash" value → paste into ADMIN_PASSWORD_HASH in .env
# Then restart the server
```

### 4. Run
```bash
uvicorn app.main:app --reload --port 8000
```
Open [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API docs.

## Authentication Flow

```
1. POST /api/auth/login  { username, password }
         ↓
   Returns: { access_token: "eyJ..." }
         ↓
2. Add header to protected requests:
   Authorization: Bearer eyJ...
         ↓
3. GET /api/auth/me  →  confirms you're logged in
```

## API Endpoints

### Auth
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/auth/login` | ❌ | Get JWT token |
| GET | `/api/auth/me` | 🔒 | Verify token |
| GET | `/api/auth/hashpw?password=x` | ❌ | Generate bcrypt hash (disable in prod!) |

### Projects
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/projects/` | ❌ | List projects (`?featured=true&tag=React`) |
| GET | `/api/projects/{id}` | ❌ | Get one project |
| POST | `/api/projects/` | 🔒 | Create project |
| PATCH | `/api/projects/{id}` | 🔒 | Update project |
| DELETE | `/api/projects/{id}` | 🔒 | Delete project |

### Blog
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/blog/` | ❌ | List published posts |
| GET | `/api/blog/{slug}` | ❌ | Get one post |
| POST | `/api/blog/` | 🔒 | Create post |
| PATCH | `/api/blog/{id}` | 🔒 | Update post |
| DELETE | `/api/blog/{id}` | 🔒 | Delete post |

## Frontend Connection
Open `portfolio.html` — it auto-fetches from `http://localhost:8000`.
Change the `const API = '...'` line at the top of the script to your deployed URL.

## Deployment (Railway)
1. Push to GitHub
2. [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Add your `.env` variables in Railway dashboard
4. Update `const API` in `portfolio.html` to your Railway URL

