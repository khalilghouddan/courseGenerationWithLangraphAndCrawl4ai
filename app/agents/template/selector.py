"""
Template Repository

Responsibilities:
- Retrieve course templates from the database.
"""



from app.models.template import CourseTemplate


def get_templates_by_language(language: str) -> list[CourseTemplate]:
    pass


