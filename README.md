



# DeepAgent Course Generator

---

## Running with Docker (Recommended)

The easiest way to run the application and its dependencies (PostgreSQL, SearxNG) is via Docker Compose.

### 1. Configure the Environment
Create a `.env` file in the root directory (you can copy from `.env.example`).

**Key Environment Variables in `.env`:**
```env
# LLM Configuration
OPENAI_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-your-api-key
OPENAI_BASE_URL=

# External Tools
SEARXNG_URL=http://searxng:8080/search
CRAWL4AI_URL=http://127.0.0.1:8000

# Database Configuration
DEEP_AGENT_DB_HOST=db
DEEP_AGENT_DB_PORT=5432
DEEP_AGENT_DB_USER=postgres
DEEP_AGENT_DB_PASSWORD=root
```

### 2. Start the Services
Ensure Docker Desktop or your Docker daemon is running, then execute:
```bash
docker compose up --build -d
```

This command spins up:
- The FastAPI backend on port `8011`
- PostgreSQL on port `5433` mapped to `5432`
- SearxNG on port `8080`

---

## Running Locally Without Docker

If you want to run the project directly on your machine, you can use Python instead of Docker.

### 1. Create and activate a virtual environment
From the project root:
```powershell
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies
```powershell
pip install -r requirements.txt
```

### 3. Configure `.env`
Copy `.env.example` to `.env`, then update it for your machine.

Minimum local values:
```env
OPENAI_MODEL=gpt-4o-mini
OPENAI_API_KEY=your-api-key

DEEP_AGENT_DB_HOST=127.0.0.1
DEEP_AGENT_DB_PORT=5433
DEEP_AGENT_DB_USER=postgres
DEEP_AGENT_DB_PASSWORD=root
```

If you want search and scraping features to work locally, make sure these services are also available:
```env
SEARXNG_URL=http://127.0.0.1:8080/search
CRAWL4AI_URL=http://127.0.0.1:8000
```

### 4. Start PostgreSQL locally
The database bootstrap script expects PostgreSQL to be running on the port defined above, and the default local setup uses:
- host: `127.0.0.1`
- port: `5433`
- user: `postgres`
- password: `root`

### 5. Initialize the database
Run:
```powershell
python scriptes/init_db.py
```

This creates the `deep_agent_db` database if needed and applies the schema from `scriptes/schema.sql`.

### 6. Start the API server
Run:
```powershell
uvicorn src.main:app --host 0.0.0.0 --port 8011 --reload
```

You can also use the helper script:
```powershell
sh start.sh
```

### 7. Open the app
Once the server is up, open:
- `http://localhost:8011/docs`
- `http://localhost:8011/health`
- `http://localhost:8011/app`

---

## Exposed Endpoints

Once the server is running, the API is available at `http://localhost:8011`.

### API Endpoints
- `POST /courses/generate` takes a natural-language prompt and triggers the 3-agent pipeline to generate a full course.
- `GET /courses` retrieves a list of all generated courses stored in the database.
- `GET /courses/{course_id}` retrieves the full structured details and content of a specific course.

### System Endpoints
- `GET /docs` interactive API documentation
- `GET /redoc` alternative API documentation interface
- `GET /health` check the health and uptime of the API
- `/app` mount point for the React frontend static files

---

## How To Test The API

After starting the stack, you can test every API route in a few different ways.

### 1. Check the health endpoint
Use this first to confirm the backend, database, search, crawl, and LLM services are reachable:
```bash
curl http://localhost:8011/health
```

Expected result:
- a JSON response with `"status": "healthy"` when all services are up

### 2. Open the interactive API docs
Open one of these in your browser:
- `http://localhost:8011/docs`
- `http://localhost:8011/redoc`
- `http://localhost:8011/api-docs`

The Swagger UI at `/docs` is the easiest place to test requests manually.

### 3. Generate a course
Send a `POST` request to `/courses/generate`:
```bash
curl -X POST "http://localhost:8011/courses/generate" \
  -H "Content-Type: application/json" \
  -d "{\"prompt\":\"Create a beginner course about Python programming for absolute beginners.\"}"
```

Expected result:
- a generated course object
- an `id` field if the course was saved to the database

### 4. List all saved courses
```bash
curl http://localhost:8011/courses
```

Expected result:
- an array of saved courses

### 5. Get one course by ID
Replace `1` with a real course id from the list endpoint:
```bash
curl http://localhost:8011/courses/1
```

Expected result:
- the full course record, including `realcoursebody`

### 6. Test the frontend
Open:
- `http://localhost:8011/app`

From there you can generate a course and browse saved courses in the UI.

---

## Stopping the Services
To stop the application and clean up the containers, run:
```bash
docker compose down
```
Add the `-v` flag if you want to wipe the local database and SearxNG volumes.
