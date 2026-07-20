### Query Builder

#Responsibilities:
#- Resolve [SUBJECT] placeholders in lesson titles using the real course subject.
#- Ask the LLM to generate focused, high-quality search queries for a lesson.

from typing import List

from app.services.llm import get_llm
from app.utils.logger import log_message, log_info


def resolve_subject(text: str, subject: str) -> str:
    """Replace the [SUBJECT] template placeholder with the real subject."""
    return text.replace("[SUBJECT]", subject)


def _parse_queries(raw: str) -> List[str]:
    """
    Parse LLM plain-text response into a clean list of query strings.
    Strips numbering (1. 2. -), quotes, blank lines, and markdown formatting.
    """
    lines = []
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        #strip common list prefixes: "1.", "2.", "3.", "-", "*", "•"
        for prefix in ("1.", "2.", "3.", "4.", "5.", "-", "*", "•"):
            if line.startswith(prefix):
                line = line[len(prefix):].strip()
                break
        #strip surrounding quotes if any
        if (line.startswith('"') and line.endswith('"')) or (line.startswith("'") and line.endswith("'")):
            line = line[1:-1].strip()
        #skip lines that look like headers, descriptions, or list items
        if (
            line.startswith("#")
            or len(line) < 5
            or line.endswith(":")
            or "Variable" in line
            or "Este capítulo" in line
            or "estudiantes podrán" in line
            or "Al finalizar" in line
        ):
            continue
        lines.append(line)
    return lines


def build_search_queries(
    lesson_title: str,
    lesson_objective: str,
    subject: str,
    course_title: str,
    previous_sources: List[str],
    language: str = "English",
) -> List[str]:
    """
    Generate exactly 3 focused search queries for a lesson.

    [SUBJECT] placeholders are resolved before the LLM sees them so
    queries are always about the real topic (e.g. Python, not [SUBJECT]).
    Uses plain llm.invoke() + manual parsing — more reliable than
    with_structured_output for simple list generation.
    """
    #resolve placeholders
    resolved_title = resolve_subject(lesson_title, subject)
    resolved_objective = resolve_subject(lesson_objective, subject)

    log_info("QUERY_BUILDER", "#00BCD4", f"Building queries | subject='{subject}' | lesson='{resolved_title}'")

    prompt = f"""You are a search query generator.

Your ONLY task is to output exactly 3 web search queries, one per line.
Do NOT write any explanations, headers, introductory sentences, lesson content, or markdown.
Do NOT number the lines.
Do NOT wrap the queries in quotes.
Write all queries in {language}.

Context:
- Subject: {subject}
- Course: {course_title}
- Lesson: {resolved_title}
- Goal: {resolved_objective}
- Language: {language}
- Avoid these already-searched sources: {previous_sources if previous_sources else "none"}

Output exactly 3 search queries in {language}, one per line, nothing else:"""

    with log_message("QUERY_BUILDER", "#00BCD4", f"LLM generating queries for: '{resolved_title}'"):
        response = get_llm().invoke(prompt)

    queries = _parse_queries(response.content)

    # Make sure we only have queries
    queries = [q for q in queries if len(q.split()) > 1]

    if not queries:
        queries = [f"{subject} {resolved_title}"]

    log_info("QUERY_BUILDER", "#00BCD4", f"Generated {len(queries)} queries: {queries}")
    return queries[:3]  # cap at 3
