# Hard Copy 📀

A full-stack web application for managing a DVD collection. Built with FastAPI, PostgreSQL, and vanilla HTML/CSS/JavaScript.

> Built as a learning project and gift for my wife.

---

## Features

- Add DVDs to your collection with title and purchase location
- Remove DVDs from your collection
- Search your collection by title (live search)
- View total collection count in the header
- Duplicate detection — won't let you add the same movie twice
- Responsive design — works on mobile and desktop
- RESTful API with interactive documentation

---

## Tech Stack

**Backend**
- Python 3.11+
- FastAPI — web framework
- PostgreSQL — database
- SQLAlchemy — ORM (Python to SQL translator)
- Pydantic — request/response validation
- psycopg2 — PostgreSQL driver
- python-dotenv — environment variable management

**Frontend**
- HTML5
- CSS3 (with mobile responsive styles)
- Vanilla JavaScript (fetch API)
- Bootstrap Icons

---

## Project Structure

```
dvd_tracker/
├── app/                    # FastAPI application
│   ├── main.py             # App entry point, CORS, routers
│   ├── database.py         # SQLAlchemy engine and session
│   ├── models.py           # Database table definitions
│   ├── schemas.py          # Pydantic request/response schemas
│   └── routers/
│       └── dvds.py         # All DVD API endpoints
│
├── cli/                    # Original CLI version (legacy)
│   ├── main.py             # Menu-driven interface
│   ├── dvd_repo.py         # Database functions
│   └── db.py               # psycopg2 connection
│
├── frontend/               # Web interface
│   ├── index.html          # Main page structure
│   ├── css/
│   │   ├── style.css       # Main styles
│   │   └── mobile.css      # Responsive overrides
│   ├── js/
│   │   ├── api.js          # All fetch() calls to FastAPI
│   │   ├── app.js          # Main page logic and rendering
│   │   └── utils.js        # Helper functions
│   └── images/
│       └── logo.png
│
├── tests/                  # Future test files
├── .env                    # Environment variables (never committed)
├── .env.example            # Safe template showing required variables
├── .gitignore
├── requirements.txt        # Python dependencies
├── run.py                  # API server entry point
└── HardCopy.bat            # Windows launcher (starts Postgres + FastAPI)
```

---

## Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 18+
- Git

### Installation

1. Clone the repository
```bash
git clone <your-repo-url>
cd dvd_tracker
```

2. Create and activate virtual environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create your `.env` file
```bash
cp .env.example .env
# Edit .env with your actual database credentials
```

5. Create the database in PostgreSQL
```sql
CREATE DATABASE movies;
-- Tables are created automatically by SQLAlchemy on first run
```

6. Start the application

**Windows — double-click `HardCopy.bat`** (starts PostgreSQL + FastAPI)

Or manually:
```bash
python run.py
```

---

## API Documentation

Once running, visit:
- Interactive docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/health`

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dvds` | Get all DVDs |
| GET | `/api/dvds/{id}` | Get one DVD by ID |
| GET | `/api/dvds/search?title=` | Search by title |
| GET | `/api/dvds/count` | Get total count |
| GET | `/api/dvds/stats/summary` | Collection statistics |
| GET | `/api/dvds/location/{location}` | Filter by location |
| POST | `/api/dvds` | Add a new DVD |
| PUT | `/api/dvds/{id}` | Update a DVD |
| DELETE | `/api/dvds/{id}` | Remove a DVD |

---

## Environment Variables

Copy `.env.example` to `.env` and fill in your values. Never commit `.env` to Git.

```
DATABASE_URL=postgresql://username:password@localhost/movies
DB_HOST=localhost
DB_PORT=5432
DB_NAME=movies
DB_USER=postgres
DB_PASSWORD=your_password_here
API_HOST=0.0.0.0
API_PORT=8000
```

---

## Running the Frontend

Open `frontend/index.html` with VS Code's Live Server extension.

Make sure `API_BASE` in `frontend/js/api.js` points to your running server:
```javascript
const API_BASE = "http://localhost:8000";
```

---

## Deployment Roadmap

| Stage | Frontend | Backend | Status |
|-------|----------|---------|--------|
| Local | Live Server | python run.py | ✅ Current |
| Partial | File / GitHub Pages | Railway or Render | 🔜 Next |
| Full | GitHub Pages | Railway or Render | 🔜 After bootcamp |
| Production | S3 + CloudFront | AWS EC2 + RDS | 🔜 After AWS certs |

---

## Version History

- v1.0.0 — CLI application with PostgreSQL (psycopg2)
- v2.0.0 — FastAPI REST API with SQLAlchemy
- v2.1.0 — Frontend with HTML, CSS, and JavaScript (current)
- v3.0.0 — Deployment + user accounts (planned)

---

## Author

Jordan — Junior Data Engineer