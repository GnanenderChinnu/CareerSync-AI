import json
import urllib.error
import urllib.request

from django.conf import settings


def analyze_career_readiness(resume_text="", target_role="", user_skills=None):
    """
    AI integration boundary for OpenAI/Gemini.
    TODO: Use settings.AI_PROVIDER and settings.AI_API_KEY to call a real AI API.
    The MVP returns deterministic mock results when no API key is configured.
    """
    user_skills = user_skills or []
    if settings.AI_PROVIDER.lower() == "gemini" and settings.AI_API_KEY:
        ai_response = _call_gemini_for_analysis(resume_text, target_role, user_skills)
        if ai_response:
            return ai_response

    return _mock_analysis(resume_text, target_role, user_skills)


def _mock_analysis(resume_text="", target_role="", user_skills=None):
    user_skills = user_skills or []
    normalized_skills = {skill.lower() for skill in user_skills}
    role = target_role or "IT Associate"

    core_missing = []
    for skill in ["sql", "python", "data structures", "communication"]:
        if skill not in normalized_skills:
            core_missing.append(skill.title())

    score = 72
    if resume_text and len(resume_text) > 500:
        score += 8
    if len(user_skills) >= 4:
        score += 7

    return {
        "resume_score": min(score, 95),
        "strengths": [
            "Clear interest in IT roles",
            "Good foundation for fresher-level opportunities",
            "Profile can be aligned quickly with mandatory screening tests",
        ],
        "weaknesses": [
            "Resume needs stronger project impact statements",
            "Technical skills should be grouped by confidence level",
        ],
        "missing_skills": core_missing[:4],
        "suggested_improvements": [
            "Add 2-3 measurable project outcomes",
            "Prepare AptiReady topics for daily 30-minute practice",
            f"Map coding projects to {role} responsibilities",
        ],
        "interview_questions": generate_interview_questions(role, user_skills),
    }


def generate_interview_questions(job_role, user_skills=None, exam_id=""):
    user_skills = user_skills or []
    if settings.AI_PROVIDER.lower() == "gemini" and settings.AI_API_KEY:
        ai_questions = _call_gemini_for_questions(job_role, user_skills, exam_id)
        if ai_questions:
            return ai_questions

    skills = ", ".join(user_skills or ["programming fundamentals"])
    role = job_role or "IT Associate"
    exam_prompt = {
        "aptiready": "Explain how you solve aptitude questions under time pressure.",
        "codestart": "Write a simple program and explain each step clearly.",
        "codepro": "Explain the tradeoff between time complexity and memory usage.",
    }.get(exam_id, "Describe how you prepare for a new technical assessment.")

    return [
        f"What skills make you ready for a {role} role?",
        f"How have you used {skills} in a project or practice problem?",
        exam_prompt,
        "Tell me about a mistake you made while solving a problem and how you fixed it.",
        "How would you explain a technical concept to a non-technical teammate?",
    ]


def _call_gemini_for_analysis(resume_text, target_role, user_skills):
    prompt = f"""
You are an AI career coach for freshers preparing for IT roles.
Analyze the candidate profile and return only valid JSON with this exact shape:
{{
  "resume_score": 0,
  "strengths": [],
  "weaknesses": [],
  "missing_skills": [],
  "suggested_improvements": [],
  "interview_questions": []
}}

Target role: {target_role or "IT Associate"}
Skills: {", ".join(user_skills) or "Not provided"}
Resume text: {resume_text[:4000] or "No resume text provided yet."}

Keep each list to 3-5 practical points. Make advice suitable for AptiReady, CodeStart, and CodePro preparation.
"""
    data = _call_gemini(prompt)
    if not data:
        return None

    return {
        "resume_score": _safe_score(data.get("resume_score")),
        "strengths": _safe_list(data.get("strengths")),
        "weaknesses": _safe_list(data.get("weaknesses")),
        "missing_skills": _safe_list(data.get("missing_skills")),
        "suggested_improvements": _safe_list(data.get("suggested_improvements")),
        "interview_questions": _safe_list(data.get("interview_questions")),
    }


def _call_gemini_for_questions(job_role, user_skills, exam_id):
    prompt = f"""
Generate five interview questions for an IT fresher.
Return only valid JSON with this exact shape:
{{"interview_questions": []}}

Target role: {job_role or "IT Associate"}
Skills: {", ".join(user_skills) or "programming fundamentals"}
Exam focus: {exam_id or "general IT readiness"}
Include a mix of aptitude explanation, basic coding, advanced coding, and behavioral questions.
"""
    data = _call_gemini(prompt)
    if not data:
        return None
    questions = _safe_list(data.get("interview_questions"))
    return questions[:5] if questions else None


def _call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.AI_MODEL}:generateContent"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.4,
            "responseMimeType": "application/json",
        },
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": settings.AI_API_KEY,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            response_data = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError):
        return None

    text = _extract_gemini_text(response_data)
    if not text:
        return None

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        cleaned_text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        try:
            return json.loads(cleaned_text)
        except json.JSONDecodeError:
            return None


def _extract_gemini_text(response_data):
    candidates = response_data.get("candidates", [])
    if not candidates:
        return ""
    parts = candidates[0].get("content", {}).get("parts", [])
    if not parts:
        return ""
    return parts[0].get("text", "")


def _safe_list(value):
    if isinstance(value, list):
        return [str(item) for item in value if item]
    return []


def _safe_score(value):
    try:
        return max(0, min(100, int(value)))
    except (TypeError, ValueError):
        return 72
