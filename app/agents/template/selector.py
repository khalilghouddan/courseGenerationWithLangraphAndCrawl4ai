"""
Template Selector

Responsibilities:
- Retrieve course templates from the database.
- Filter templates by language and return them as structured objects.
"""

from types import SimpleNamespace
from app.db.templateDB import get_all_templates


def get_templates_by_language(language: str) -> list:
    """
    Retrieve candidate templates filtered by language.

    First tries to find templates matching the requested language.
    If none are found, falls back to returning ALL templates so the
    LLM still has options to choose from.

    Args:
        language: The course language (e.g. "English", "French").

    Returns:
        A list of SimpleNamespace objects with attributes:
        id, title, language, description
        (compatible with build_template_prompt in prompt.py)
    """
    rows = get_all_templates()

    def row_to_ns(row) -> SimpleNamespace:
        return SimpleNamespace(
            id=str(row["id"]),
            title=row["title"] or "",
            language=row["language"] or "",
            description=row["description"] or "",
        )

    # Filter by language (case-insensitive)
    matched = [
        row_to_ns(row)
        for row in rows
        if (row.get("language") or "").lower() == language.lower()
    ]

    if matched:
        return matched

    # Fallback: return all templates so the LLM can still pick the best one
    return [row_to_ns(row) for row in rows]
