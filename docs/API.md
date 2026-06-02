# API Reference

All protected endpoints expect a Firebase bearer token.

## Profile

`GET /api/profile/`

Returns the logged-in user's profile.

`POST /api/profile/`

```json
{
  "name": "Nikhil Sharma",
  "skills": ["Python", "SQL", "HTML"],
  "education": "B.Tech Computer Science",
  "target_role": "Junior Software Engineer",
  "experience_level": "fresher"
}
```

## Resume

`POST /api/resume/upload/`

Multipart form data:

- `file`: PDF/DOCX resume
- `extracted_text`: optional text until real parsing is added

`GET /api/resume/analysis/`

Returns score, strengths, weaknesses, missing skills, suggested improvements, and interview questions.

## Interview

`POST /api/interview/generate-questions/`

```json
{
  "job_role": "Junior Software Engineer",
  "exam_id": "codestart"
}
```

`POST /api/interview/submit-answer/`

```json
{
  "session_id": 1,
  "answer": "I solved a string reversal problem by..."
}
```

## Dashboard

`GET /api/dashboard/`

Returns resume score, completed interviews, skills to improve, progress percentage, and exam content.

## Exams

`GET /api/exams/`

Returns the three MVP exam tracks and their learning materials.
