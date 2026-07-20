# DeepAgent Course Generator

A powerful, AI-driven backend for automatically generating complete, structured courses using a multi-agent pipeline with LangGraph. It leverages an external Web Research API (SearXNG + Crawl4AI) and Remote Ollama/LLM APIs to gather context, structure the course, and generate the final content.

---

## 🚀 Features
- **Multi-Agent Architecture**: Built with LangGraph to orchestrate complex reasoning and planning.
- **Web Research Integration**: Automates finding accurate and relevant curriculum data.
- **RESTful API**: Fast and robust API built with FastAPI.
- **PostgreSQL**: Stores generated courses for persistent access.
- **Docker Ready**: One command to start the entire environment.

---

## 🛠️ Prerequisites
- **Docker & Docker Compose** (Recommended for easiest setup)
- **Python 3.11+** and [**uv**](https://github.com/astral-sh/uv) (for local development)

---

## ⚙️ Environment Configuration

Before running the application, you must configure your environment variables. 
Create a `.env` file in the root directory by copying the example file:

```bash
cp .env.example .env
```

**Key Environment Variables in `.env`:**
```env
# ── LLM: Remote API ────────────────────────────────────────────────────
QUEN_MODEL=qwen3:8b
MISTRAL_MODEL=mistral-small3.2:latest
MODEL_API_KEY=your_api_key_here
MODEL_BASE_URL=http://your_llm_host/api/v1

# ── Web Research API (remote SearXNG + Crawl4AI) ────────────────────────
WEB_RESEARCH_BASE_URL=http://your_research_api_host:port
WEB_RESEARCH_API_KEY=your_research_api_key

# ── PostgreSQL ────────────────────────────────────────────────────────────────
DEEP_AGENT_DB_HOST=db      # Use "db" for Docker, or "127.0.0.1" for local
DEEP_AGENT_DB_PORT=5432    # Use 5432 for Docker, or 5433 for local port forwarding
DEEP_AGENT_DB_USER=postgres
DEEP_AGENT_DB_PASSWORD=root

# ── APP ────────────────────────────────────────────────────────────────
APP_PORT=8011
SCRAPED_IN_ONE_TIME=3
SearXNG_max_url=1
```

---

## 🐳 Running with Docker (Recommended)

The easiest way to run the application (API and PostgreSQL Database) is via Docker Compose.

### Start the Services
Ensure Docker Desktop or your Docker daemon is running, then execute:
```bash
docker-compose up --build
```
*(Add `-d` to run in detached mode).*

This command automatically:
1. Provisions a PostgreSQL container (`db`).
2. Builds and starts the FastAPI backend (`api`).
3. Waits for the database to be ready and automatically initializes the schema.

The API will be available at: **http://localhost:8011**

---

## 💻 Running Locally Without Docker

If you prefer to run the project directly on your machine without Docker containers:

### 1. Install dependencies using `uv`
This project uses `uv` for lightning-fast package management instead of a traditional `requirements.txt`.
```bash
uv sync
```
*(Alternatively, you can activate a standard virtual environment and run `pip install -e .`)*

### 2. Configure Local Database
Ensure you have a PostgreSQL server running locally, or use Docker just for the database:
```bash
docker run --name deepagent_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=root -e POSTGRES_DB=postgres -p 5433:5432 -d postgres:15-alpine
```

Update your `.env` to point to the local database:
```env
DEEP_AGENT_DB_HOST=127.0.0.1
DEEP_AGENT_DB_PORT=5433
DEEP_AGENT_DB_USER=postgres
DEEP_AGENT_DB_PASSWORD=root
```

### 3. Initialize the database
Run the initialization script to create tables:
```bash
python scriptes/init_db.py
```

### 4. Start the API server
Run the FastAPI development server:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8011 --reload
```
*(Or use the provided `sh start.sh` helper script)*

---

## 📡 API Endpoints & Testing

Once the server is running, you can access the API at `http://localhost:8011`.

### Interactive Documentation
- **Swagger UI**: [http://localhost:8011/docs](http://localhost:8011/docs) *(Easiest way to test endpoints manually)*
- **ReDoc**: [http://localhost:8011/redoc](http://localhost:8011/redoc)

### Core Endpoints
- `GET /health` : Check the health and uptime of the API services.
- `POST /courses/generate` : Takes a natural-language prompt and triggers the 3-agent pipeline to generate a full course.
- `GET /courses` : Retrieves a list of all generated courses stored in the database.
- `GET /courses/{course_id}` : Retrieves the full structured details and content of a specific course.

### Testing Generation via cURL
```bash
curl -X POST "http://localhost:8011/courses/generate" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a beginner course about Python programming for absolute beginners."}'
```

---

## 🛑 Stopping the Services
To stop the Docker application and clean up the containers, run:
```bash
docker-compose down
```
Add the `-v` flag if you want to wipe the local database volume (WARNING: This deletes your saved courses).
