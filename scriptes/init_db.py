



import json
import os
import re
from typing import Any

import psycopg2
from psycopg2.extras import Json
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

DB_HOST = os.getenv("DEEP_AGENT_DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DEEP_AGENT_DB_PORT", "5433")
DB_USER = os.getenv("DEEP_AGENT_DB_USER", "postgres")
DB_PASS = os.getenv("DEEP_AGENT_DB_PASSWORD", "root")
DB_NAME = os.getenv("DEEP_AGENT_DB_NAME", "deep_agent_db")


TEMPLATE_PROFILES: dict[str, dict[str, str]] = {
    "callcenterspanish": {
        "title": "Spanish Call Center Customer Service",
        "subject": "Spanish call center customer service",
        "language": "Spanish",
        "description": "A practical course for building professional call center communication in Spanish.",
    },
    "default-eng": {
        "title": "Default English Course Template",
        "subject": "general course topic",
        "language": "English",
        "description": "A flexible default course template for creating structured lessons in English.",
    },
    "default-spanish": {
        "title": "Plantilla de curso predeterminada en español",
        "subject": "tema general del curso",
        "language": "Spanish",
        "description": "Una plantilla de curso flexible y predeterminada para crear lecciones estructuradas en español.",
    },
    "default-francais": {
        "title": "Modèle de cours par défaut en français",
        "subject": "sujet général du cours",
        "language": "Frenchcc",
        "description": "Un modèle de cours flexible et par défaut pour créer des leçons structurées en français.",
    },
    "databasedesign": {
        "title": "Database Design and SQL",
        "subject": "database design and SQL",
        "language": "English",
        "description": "A structured introduction to designing databases and writing effective SQL queries.",
    },
    "devops": {
        "title": "DevOps Fundamentals",
        "subject": "DevOps fundamentals",
        "language": "English",
        "description": "A hands-on course template for learning modern DevOps workflows, tools, and practices.",
    },
    "gestiondesressourceshumaines": {
        "title": "Human Resources Management",
        "subject": "human resources management",
        "language": "French",
        "description": "A practical template covering core HR processes, people management, and workplace policies.",
    },
    "managment": {
        "title": "Management Fundamentals",
        "subject": "management fundamentals",
        "language": "English",
        "description": "A course template focused on leadership, planning, communication, and team performance.",
    },
    "programing": {
        "title": "Programming Fundamentals",
        "subject": "programming fundamentals",
        "language": "English",
        "description": "A beginner-friendly programming course template covering syntax, logic, and problem-solving.",
    },
    "securityinsidecompany": {
        "title": "Workplace Security Awareness",
        "subject": "workplace security awareness",
        "language": "English",
        "description": "A security awareness course for helping employees recognize, prevent, and report workplace risks.",
    },
    "securitedeentreprise": {
        "title": "Securite en Entreprise",
        "subject": "la securite en entreprise",
        "language": "French",
        "description": "Un modele de cours pour sensibiliser les equipes aux risques, aux bonnes pratiques et a la prevention.",
    },
}


def normalize_stem(filename: str) -> str:
    return os.path.splitext(filename)[0].lower()


def infer_subject_label(filename: str, data: dict[str, Any]) -> str:
    stem = normalize_stem(filename)
    profile = TEMPLATE_PROFILES.get(stem)
    if profile:
        return profile["title"]
    if "program" in stem:
        return "Programming Fundamentals"
    if "lang" in stem:
        return "Language Learning"
    if "management" in stem:
        return "Management Fundamentals"
    if data.get("title"):
        return re.sub(r"\s+", " ", str(data["title"])).strip()
    return re.sub(r"[_-]+", " ", os.path.splitext(filename)[0]).strip().title()


def infer_language_label(filename: str, data: dict[str, Any]) -> str:
    profile = TEMPLATE_PROFILES.get(normalize_stem(filename))
    if profile and profile.get("language"):
        return profile["language"]

    language = str(data.get("language") or "").strip()
    if language:
        return language

    stem = normalize_stem(filename)
    if "program" in stem:
        return "English"
    if "lang" in stem:
        return "the target language"
    if "management" in stem:
        return "English"
    return "English"


def format_duration(minutes: int) -> str:
    hours, mins = divmod(max(0, minutes), 60)
    if hours and mins:
        return f"about {hours}h {mins}m"
    if hours:
        return f"about {hours}h"
    return f"about {mins} minutes"


def estimated_study_time_minutes(data: dict[str, Any]) -> int:
    chapters = data.get("chapters") or []
    lesson_count = sum(len(ch.get("lessons", [])) for ch in chapters if isinstance(ch, dict))
    chapter_count = len(chapters)
    # A simple estimate based on reading and reviewing each lesson prompt.
    return max(45, lesson_count * 10 + chapter_count * 5)


def build_description(filename: str, data: dict[str, Any]) -> str:
    subject = infer_subject_label(filename, data)
    language = infer_language_label(filename, data)
    profile = TEMPLATE_PROFILES.get(normalize_stem(filename), {})
    summary = profile.get("description")
    chapter_count = len(data.get("chapters") or [])
    lesson_count = sum(
        len(ch.get("lessons", [])) for ch in (data.get("chapters") or []) if isinstance(ch, dict)
    )
    time_text = format_duration(estimated_study_time_minutes(data))
    if summary:
        return (
            f"{summary} "
            f"It includes {chapter_count} chapters and {lesson_count} lessons, "
            f"with an estimated study time of {time_text}."
        )
    return (
        f"A {language} course template for {subject}. "
        f"Includes {chapter_count} chapters and {lesson_count} lessons, "
        f"with an estimated study time of {time_text}."
    )


def build_metadata(filename: str, data: dict[str, Any]) -> dict[str, Any]:
    chapters = data.get("chapters") or []
    lesson_count = sum(len(ch.get("lessons", [])) for ch in chapters if isinstance(ch, dict))
    return {
        "source_file": filename,
        "chapter_count": len(chapters),
        "lesson_count": lesson_count,
        "has_content": bool(chapters),
        "estimated_study_time_minutes": estimated_study_time_minutes(data),
    }


def expand_lesson_prompt(chapter_title: str, lesson: dict[str, Any], chapter_summary: str, filename: str) -> str:
    title = lesson.get("title", "Untitled lesson")
    base = lesson.get("content_markdown", "").strip()
    topic_label = infer_subject_label(filename, {})
    chapter_focus = chapter_title.lower()
    is_control_flow = "control flow" in chapter_focus
    language_hint = ""
    if is_control_flow:
        language_hint = (
            "Language-specific accuracy note: use the correct control-flow keywords and syntax for the target language/framework. "
            "Do not mix keywords from other languages. For example, in Ruby use `if`, `elsif`, `else`, `unless`, `case`, `when`, `end`, "
            "`while`, `until`, `for`, `each`, `times`, `break`, `next`, and `redo` only when they are valid in context.\n\n"
        )
    return (
        f"## {title}\n\n"
        f"Write a complete, detailed lesson for the course template '{topic_label}'.\n"
        f"Chapter context: {chapter_title}\n"
        f"Chapter summary: {chapter_summary}\n\n"
        f"{language_hint}"
        f"Requirements:\n"
        f"1. Output length: 800-1,500 words.\n"
        f"2. Output structure: 50-100 lines in markdown, using headings, short paragraphs, lists, and code blocks where helpful.\n"
        f"3. Overview: 2-3 sentences explaining what this lesson covers and why it matters.\n"
        f"4. Core explanation: at least 4 substantial paragraphs with concrete examples.\n"
        f"5. Step-by-step guidance: practical sequence, checklist, or procedure.\n"
        f"6. Example section: include a worked example or code sample if relevant, and make it syntactically correct for the target language.\n"
        f"7. Common mistakes: list 3-5 pitfalls and how to avoid them.\n"
        f"8. Quick check: include 2-4 short questions or an exercise.\n"
        f"9. Key takeaway: one concise closing sentence.\n"
        f"10. Tone: friendly, clear, beginner-friendly, practical, and accurate.\n\n"
        f"Original seed guidance:\n{base}"
    )
    

def enrich_template_payload(filename: str, data: dict[str, Any]) -> dict[str, Any]:
    enriched = dict(data)
    chapters = []
    for chapter in data.get("chapters", []):
        chapter_title = chapter.get("title", "Untitled chapter")
        chapter_summary = chapter.get("summary", "")
        lessons = []
        for lesson in chapter.get("lessons", []):
            lesson_copy = dict(lesson)
            lesson_copy["content_markdown"] = expand_lesson_prompt(
                chapter_title=chapter_title,
                lesson=lesson,
                chapter_summary=chapter_summary,
                filename=filename,
            )
            lessons.append(lesson_copy)
        chapter_copy = dict(chapter)
        chapter_copy["lessons"] = lessons
        chapters.append(chapter_copy)
    enriched["chapters"] = chapters
    enriched["metadata"] = build_metadata(filename, data)
    return enriched


def init_db():
    print(f"Connecting to default postgres db at {DB_HOST}:{DB_PORT} as {DB_USER} to create database '{DB_NAME}' if it doesn't exist...")

    try:
        conn_default = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database="postgres",
        )
        conn_default.autocommit = True
        cursor_default = conn_default.cursor()

        cursor_default.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (DB_NAME,))
        if not cursor_default.fetchone():
            cursor_default.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"Database '{DB_NAME}' created successfully!")
        else:
            print(f"Database '{DB_NAME}' already exists.")

        cursor_default.close()
        conn_default.close()

        print(f"Connecting to DB {DB_NAME} to apply schema...")
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
        )
        conn.autocommit = True
        cursor = conn.cursor()

        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        print(f"Applying schema from {schema_path}...")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()
        cursor.execute(schema_sql)
        print("Schema applied successfully!")

        print("Seeding course_templates from Templates...")
        templates_dir = os.path.join(os.path.dirname(__file__), "Templates")
        if os.path.exists(templates_dir):
            for filename in os.listdir(templates_dir):
                if not filename.lower().endswith(".json"):
                    continue

                filepath = os.path.join(templates_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if not data or not isinstance(data, dict) or not data.get("chapters"):
                    print(f"Skipping empty or invalid template: {filename}")
                    continue

                enriched_template = enrich_template_payload(filename, data)

                insert_query = """
                    INSERT INTO course_templates (title, language, description, template)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """
                cursor.execute(
                    insert_query,
                    (
                        infer_subject_label(filename, data),
                        infer_language_label(filename, data),
                        data.get("description") or build_description(filename, data),
                        Json(enriched_template),
                    ),
                )
                print(f"Seeded template from: {filename}")
        else:
            print(f"Directory {templates_dir} not found. Skipping template seeding.")

        cursor.close()
        conn.close()
        print("Database initialization complete.")

    except Exception as e:
        print(f"Failed to initialize database: {e}")


if __name__ == "__main__":
    init_db()


