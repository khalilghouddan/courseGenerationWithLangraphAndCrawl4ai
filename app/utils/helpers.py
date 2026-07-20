### Helpers

#Responsibilities:
#- Provide reusable utility functions across the application.


#Strip markdown code fences from a string (e.g. ```json ... ```)
def strip_markdown_fences(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()
    return raw
