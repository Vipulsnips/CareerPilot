import re

from app.schemas.resume import ResumeSchema


def extract_email(text: str) -> str | None:
    match = re.search(r"\S+@\S+", text)
    if match:
        return match.group()
    return None


def extract_phone(text: str) -> str | None:
    match = re.search(r"\+91[- ]?\d{10}", text)
    if match:
        return match.group()
    return None


def parse_resume(text: str) -> ResumeSchema:
    resume = ResumeSchema()
    resume.email = extract_email(text)
    resume.phone = extract_phone(text)
    return resume
