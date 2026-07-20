"""
Template Model

Represents a course template stored in the database.
"""

from sqlalchemy import Column, String, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid
from app.database import Base


class CourseTemplate(Base):
    """
    Course Template Model

    Attributes:
        id: Unique identifier (UUID)
        title: Template title/name
        language: Language code/name
        description: Template description
        template: Template content as JSONB (chapters, lessons, etc.)
        created_at: Timestamp of creation
    """

    __tablename__ = "course_templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(150), nullable=False)
    language = Column(String(80), nullable=True)
    description = Column(Text, nullable=True)
    template = Column(JSONB, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<CourseTemplate(id={self.id}, title={self.title}, language={self.language})>"
