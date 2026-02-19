# 🏜️ Titan Desert Solidario

Plataforma web para crear **retos solidarios tipo mini-apuestas**
asociados a la participación de corredores en la Titan Desert.

El proyecto permite:

-   Visualizar retos por categoría
-   Realizar participaciones solidarias
-   Consultar estadísticas agregadas
-   Gestionar corredores y desafíos desde el backend

------------------------------------------------------------------------

# 🧱 Arquitectura

TitanDesertSolidario/ │ ├── backend/ → API REST (FastAPI + SQLite) ├──
frontend/ → SPA React (servida con NGINX) ├── titanDB/ → Base de datos
SQLite persistente └── docker-compose.yml

------------------------------------------------------------------------

# ⚙️ Stack Tecnológico

## Backend

-   Python 3.11
-   FastAPI
-   SQLAlchemy
-   SQLite
-   Uvicorn
-   Docker

## Frontend

-   React
-   React Router
-   NGINX (servidor estático en producción)
-   Docker

------------------------------------------------------------------------

# 🗄️ Base de Datos

Base de datos SQLite persistente ubicada en:

titanDB/data/titan_desert_solidario.db

Modelos principales:

-   Warrior
-   Challenge
-   ChallengeOption
-   Participation

------------------------------------------------------------------------

# 🚀 Cómo ejecutar el proyecto

## Requisitos

-   Docker
-   Docker Compose

## Construir y levantar contenedores

Desde la raíz del proyecto:

docker compose up --build

Acceso:

Frontend: http://localhost:8080

Backend (Swagger): http://localhost:8000/docs

------------------------------------------------------------------------

# 🌱 Seed de Datos

Para cargar datos iniciales:

docker exec -it titan_desert_backend python -m app.db.seed

------------------------------------------------------------------------

# 🔌 API Endpoints

Base URL: /api/v1

## Challenges

-   GET /challenges/
-   GET /challenges/{challenge_id}

## Warriors

-   GET /warriors/

## Participations

-   POST /participations/

## Stats

-   GET /stats/

------------------------------------------------------------------------

# 🧠 Flujo de Participación

1.  Usuario selecciona reto
2.  Elige opción
3.  Introduce nombre, email, predicción, importe y mensaje
4.  Se envía POST a /participations/
5.  Se guarda en SQLite
6.  Stats se actualizan dinámicamente

------------------------------------------------------------------------

# 🐳 Docker

Servicios:

-   titan_desert_backend
-   titan_desert_frontend

Persistencia SQLite:

./titanDB/data:/data

------------------------------------------------------------------------

# 🔮 Posibles mejoras

-   Panel admin
-   Autenticación
-   Integración con pagos
-   Estadísticas avanzadas
-   Tests automatizados

------------------------------------------------------------------------

Proyecto desarrollado como iniciativa solidaria para apoyar la
participación en Titan Desert.
