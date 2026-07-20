import os
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Docs"])


@router.get(
    "/api-docs",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def api_docs():
    return """
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <title>DeepAgent Course Generator API Docs</title>
        <style>
          body { font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; line-height: 1.6; padding: 0 20px; }
          code, pre { background: #f5f5f5; padding: 2px 6px; border-radius: 4px; }
          pre { padding: 16px; overflow: auto; }
        </style>
      </head>
      <body>
        <h1>DeepAgent Course Generator API Docs</h1>
        <p>Interactive documentation is available at <code>/docs</code> and <code>/redoc</code>.</p>
        <h2>Endpoints</h2>
        <ul>
          <li><code>GET /health</code> - health check for DB, Crawl4AI, SearXNG, and LLM</li>
          <li><code>POST /courses/generate</code> - generate a structured course from a prompt</li>
        </ul>
      </body>
    </html>
    """


@router.get(
    "/",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def home_page():
    """
    Dynamically read and return the frontend index.html so that
    any UI updates (like Mermaid and Markdown rendering fixes)
    are immediately reflected at the root endpoint.
    """
    current_dir = os.path.dirname(__file__)
    index_path = os.path.normpath(os.path.join(current_dir, "..", "..", "frontend", "index.html"))
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Frontend index.html not found</h1>", status_code=404)
