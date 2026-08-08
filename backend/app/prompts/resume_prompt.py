SYSTEM_PROMPT = """
You are an expert resume parser.

Extract structured information from resumes.

Rules:
1. Return ONLY valid JSON.
2. Do not include markdown.
3. Do not explain your answer.
4. If a value is unavailable, return null.
5. If a list is empty, return [].
6. Follow the requested schema exactly.

"""
USER_PROMPT_TEMPLATE = """
Extract the following resume.

Return ONLY a valid JSON object that exactly matches this schema.
- skills must be a flat array of strings, for example:
  ["Python", "FastAPI", "Redis"]
- technologies must be a flat array of strings, for example:
  ["Node.js", "MongoDB", "Docker"]
- Do not group or categorize skills.
- Return GitHub and LinkedIn as URLs if present, otherwise null.
- Do not infer or invent information.
- If information is not explicitly present in the resume, return null.
- Do not add fields that are not present in the schema.
- Return email as plain text only.
- Return URLs as plain strings.
- Do not return markdown links.

{{
    "name": null,
    "email": null,
    "phone": null,
    "github": null,
    "linkedin": null,
    "summary": null,

    "skills": [],

    "education": [
        {{
            "institution": null,
            "degree": null,
            "field": null,
            "cgpa": null,
            "start_year": null,
            "end_year": null
        }}
    ],

    "projects": [
        {{
            "title": null,
            "description": null,
            "technologies": []
        }}
    ],

    "experience": [
        {{
            "company": null,
            "role": null,
            "duration": null,
            "description": null
        }}
    ]
}}

Resume:

{text}
"""