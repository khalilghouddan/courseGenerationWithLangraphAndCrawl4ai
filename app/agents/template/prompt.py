### Template Selection Prompt

# Responsibilities:
#- Build the prompt used by the Template Agent.
#- Present only the candidate templates.
#- Ask the LLM to return the best template ID.


from textwrap import dedent

#function to build the template prompt
def build_template_prompt(metadata, templates) -> str:
    
    template_list = []

    for template in templates:
        template_list.append(
            dedent(
                f"""
                Template ID: {template.id}
                Title: {template.title}
                Language: {template.language}
                Description: {template.description}
                """
            ).strip()
        )

    available_templates = "\n\n".join(template_list)

    return dedent(
        f"""
        You are an expert instructional designer.

        Your task is to select the SINGLE best course template.

        ------------------------------------------------------------------------
        COURSE METADATA
        ------------------------------------------------------------------------

        Title:
        {metadata.title}

        Topic:
        {metadata.topic}

        Difficulty:
        {metadata.difficulty}

        Target Audience:
        {metadata.target_audience}

        Duration:
        {metadata.duration}

        Learning Goal:
        {metadata.learning_goal}

        Language:
        {metadata.language}

        ------------------------------------------------------------------------
        AVAILABLE TEMPLATES
        ------------------------------------------------------------------------

        {available_templates}

        ------------------------------------------------------------------------
        INSTRUCTIONS
        ------------------------------------------------------------------------

        Carefully compare the course metadata with the available templates.

        Consider:

        - Course difficulty level
        - Intended audience
        - Course goal and learning objectives
        - Teaching style and structure
        - Estimated duration and course size
        - Language compatibility

        Select ONLY ONE template that best matches the course requirements.

        Prioritize templates that:
        1. Match the course language
        2. Have a similar scope and structure
        3. Support the course's difficulty level
        4. Align with the target audience

        ------------------------------------------------------------------------
        RESPONSE FORMAT
        ------------------------------------------------------------------------

        Return ONLY a JSON object with no additional text.

        Example:

        {{
            "template_id": "550e8400-e29b-41d4-a716-446655440000",
            "reason": "Best suited for a beginner-friendly programming course in English."
        }}

        Do not return markdown.
        Do not explain anything outside the JSON.
        Do not include any text before or after the JSON object.
        """
    ).strip()