# Titan Desert Solidario Backend

This is the backend for the Titan Desert Solidario project, built with FastAPI, SQLAlchemy, and SQLite.

## Features

- FastAPI for building RESTful APIs
- SQLAlchemy for database ORM
- SQLite as the database
- CORS enabled for localhost during development

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd titanDesertSolidario/backend
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
uvicorn app.main:app --reload
```

4. Access the API documentation at:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Environment Variables

- `SQLITE_DB_PATH`: Path to the SQLite database file. Defaults to `../runtime/db/titan_desert_solidario.db` if not set.

## API Endpoints

### Health Check
- `GET /api/v1/health`

### Stats
- `GET /api/v1/stats`

### Warriors
- `GET /api/v1/warriors`
- `GET /api/v1/warriors/{id}`

### Challenges
- `GET /api/v1/challenges`
- `GET /api/v1/challenges/{id}`

### Participations
- `POST /api/v1/participations`