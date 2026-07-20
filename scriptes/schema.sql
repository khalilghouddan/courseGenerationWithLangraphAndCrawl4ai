-- Drop all previous tables to cleanly recreate the schema
DROP TABLE IF EXISTS users, modules, lessons, quizzes, exercises, course_resources, courses, course_templates, scraped_data CASCADE;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 1. Create the course templates table
CREATE TABLE IF NOT EXISTS course_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(150) NOT NULL,
    language VARCHAR(80),
    description TEXT,
    template JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);

-- 2. Create the courses table
CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    headline VARCHAR(255),
    description TEXT,
    objectives JSONB,
    prerequisites JSONB,
    target_audiences VARCHAR(255),
    primary_category_title VARCHAR(100),
    primary_subcategory_title VARCHAR(100),
    duration VARCHAR(100),
    language VARCHAR(50) DEFAULT 'English',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    url_scraped JSONB,                -- Array of URLs scraped during generation
    realcoursebody TEXT,              -- Full generated course content as JSON
    generation_time FLOAT             -- Time taken to generate in seconds
);

-- 3. Create the scraped_data table
CREATE TABLE IF NOT EXISTS scraped_data (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL UNIQUE,
    title VARCHAR(500),
    content TEXT,
    clean_content TEXT,
    markdown TEXT,
    time_of_scraping TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
