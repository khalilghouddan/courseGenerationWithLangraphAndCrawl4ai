


#json to dict python
import json
#time and date fuctions
from datetime import datetime, date
#logs
from app.utils.logger import log_message
#database connection
from app.db.checkDbConection import get_db_connection

try:
    from psycopg2.extras import DictCursor  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    DictCursor = None


class _SafeEncoder(json.JSONEncoder):
    """JSON encoder that converts datetime/date to ISO strings."""
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)


def save_scraped_data(
    url: str,
    title: str | None = None,
    content: str | None = None,
    clean_content: str | None = None,
    markdown: str | None = None,
) -> int | None:
    """
    Insert a scraped page into the `scraped_data` table.

    Returns the new row id, or None on failure (logged, not raised).
    """
    if title:
        title = title.replace("\x00", "")
    if content:
        content = content.replace("\x00", "")
    if clean_content:
        clean_content = clean_content.replace("\x00", "")
    if markdown:
        markdown = markdown.replace("\x00", "")

    with log_message("DATABASE", "#B87363", f"INSERT INTO scraped_data — url='{url}'"):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO scraped_data
                    (url, title, content, clean_content, markdown, time_of_scraping)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (url) DO UPDATE SET
                    title = EXCLUDED.title,
                    content = EXCLUDED.content,
                    clean_content = EXCLUDED.clean_content,
                    markdown = EXCLUDED.markdown,
                    time_of_scraping = EXCLUDED.time_of_scraping
                RETURNING id
                """,
                (url, title, content, clean_content, markdown, datetime.now()),
            )
            row_id = cursor.fetchone()[0]
            conn.commit()
            return row_id
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


def save_course(course, generation_time_s: float = 0.0, urls_used: list[str] | None = None) -> int | None:
    """
    Insert a generated course into the `courses` table.

    `course` is a CourseOutput pydantic model.
    Returns the new row id, or None on failure (logged, not raised).
    """
    with log_message("DATABASE", "#B87363", f"INSERT INTO courses — title='{course.title}'"):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Ensure we serialize only the actual chapters/sections structure
            real_body = course.realcoursebody
            if isinstance(real_body, dict):
                while isinstance(real_body, dict) and "realcoursebody" in real_body and not ("chapters" in real_body or "sections" in real_body):
                    real_body = real_body["realcoursebody"]
            else:
                real_body = {}
            course_body_json = json.dumps(real_body, cls=_SafeEncoder, ensure_ascii=False)

            cursor.execute(
                """
                INSERT INTO courses
                    (title, headline, description,
                     objectives, prerequisites, target_audiences,
                     primary_category_title, primary_subcategory_title,
                     duration, language, created_at,
                     url_scraped, realcoursebody, generation_time)
                VALUES (%s, %s, %s,
                        %s, %s,
                        %s, %s, %s,
                        %s, %s, %s,
                        %s, %s, %s)
                RETURNING id
                """,
                (
                    course.title[:255],
                    course.headline[:255],
                    course.description[:2000],
                    json.dumps(course.objectives, ensure_ascii=False),
                    json.dumps(course.prerequisites, ensure_ascii=False),
                    course.target_audiences[:500] if course.target_audiences else None,
                    course.primary_category_title[:100],
                    course.primary_subcategory_title[:100],
                    course.duration[:50],
                    course.language[:50],
                    course.created_at or datetime.now(),
                    json.dumps(urls_used or course.urls_scraped, ensure_ascii=False),
                    course_body_json,
                    generation_time_s,
                ),
            )
            row_id = cursor.fetchone()[0]
            conn.commit()
            return row_id
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


def get_all_courses() -> list[dict]:
    """Retrieve all courses from the database, ordered by created_at desc."""

    try:
        conn = get_db_connection()
        if DictCursor is None:
            return []
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute(
            """
            SELECT id, title, headline, description,
                   objectives, prerequisites, target_audiences,
                   primary_category_title, primary_subcategory_title,
                   duration, language, created_at, generation_time
            FROM courses
            ORDER BY created_at DESC
            """
        )
        rows = cursor.fetchall()
        return [dict(r) for r in rows]
    except Exception:
        return []
    finally:
        conn.close()


def get_course_by_id(course_id: int) -> dict | None:
    """Retrieve a full course record by id."""
    try:
        conn = get_db_connection()
        if DictCursor is None:
            return None
        cursor = conn.cursor(cursor_factory=DictCursor)
        cursor.execute(
            """
            SELECT id, title, headline, description,
                   objectives, prerequisites, target_audiences,
                   primary_category_title, primary_subcategory_title,
                   duration, language, created_at, url_scraped,
                   realcoursebody, generation_time
            FROM courses
            WHERE id = %s
            """,
            (course_id,),
        )
        row = cursor.fetchone()
        return dict(row) if row else None
    except Exception:
        return None
    finally:
        conn.close()
