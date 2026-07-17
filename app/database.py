"""
Database Configuration and Setup

Responsibilities:
- Initialize SQLAlchemy engine and session factory
- Provide database connection utilities
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.utils.config import settings

# Build database URL
DATABASE_URL = (
    f"postgresql://{settings.DEEP_AGENT_DB_USER}:{settings.DEEP_AGENT_DB_PASSWORD}"
    f"@{settings.DEEP_AGENT_DB_HOST}:{settings.DEEP_AGENT_DB_PORT}/deep_agent_db"
)

# Create engine
engine = create_engine(DATABASE_URL, echo=False)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
