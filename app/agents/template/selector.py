"""
Template Repository

Responsibilities:
- Retrieve course templates from the database.
- Retrieve a template by its ID.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import SessionLocal
from app.models.template import CourseTemplate


def get_templates_by_language(language: str) -> list[CourseTemplate]:
    """
    Retrieve all templates for a given language.

    Args:
        language: Language code/name (e.g., 'English', 'Spanish', 'French')

    Returns:
        List of CourseTemplate objects matching the language
    """
    with SessionLocal() as session:
        statement = (
            select(CourseTemplate)
            .where(CourseTemplate.language == language)
            .order_by(CourseTemplate.title)
        )

        return list(session.scalars(statement).all())


def get_template_by_id(template_id: str | UUID) -> CourseTemplate | None:
    """
    Retrieve a template by its UUID.

    Args:
        template_id: UUID of the template

    Returns:
        CourseTemplate object or None if not found
    """
    with SessionLocal() as session:
        return session.get(CourseTemplate, template_id)