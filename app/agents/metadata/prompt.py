


from langchain_core.prompts import PromptTemplate

METADATA_PROMPT = PromptTemplate(
    template="""
You are an expert instructional designer.

Analyze the user's learning request and generate accurate metadata for an online course.

Guidelines:

- Create a concise, engaging course title.
- Write a one-sentence headline describing the course value.
- Write a clear description (3–6 sentences).
- Generate realistic learning objectives.
- Generate realistic prerequisites (leave empty if none are required).
- Identify the target audience.
- Choose the most appropriate primary category.
- Choose the most appropriate primary subcategory.
- Estimate a realistic course duration.
- Determine the course language:
  - Use the language specified by the user.
  - Otherwise default to English.
  - Allowed values: English, Spanish, French, Arabic.

Return only the structured output.

User request:
{prompt}

{format_instructions}
""",
    input_variables=["prompt"],
    partial_variables={
        "format_instructions": "{format_instructions}"
    },
)