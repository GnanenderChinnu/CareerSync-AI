# CareerSync AI

CareerSync AI is a career preparation platform for freshers and job seekers applying for IT roles. It combines exam preparation, resume analysis, profile tracking, and interview question generation in one dashboard.

This version is built as a realistic local-first MVP. It works with Firebase Authentication, a Django REST API, SQLite for local storage, and a React dashboard. PostgreSQL and cloud deployment files are included for future production deployment.

## Core Idea

Many IT hiring processes test candidates on aptitude, basic coding, and advanced coding. CareerSync AI keeps those areas together so a candidate can prepare, track readiness, upload a resume, and practice interview answers.

## Exams Included

| Exam | Focus | Topics |
| --- | --- | --- |
| AptiReady Test | Aptitude | Quantitative aptitude, logical reasoning, verbal ability |
| CodeStart Test | Basic coding | Variables, loops, arrays, strings, functions |
| CodePro Test | Advanced coding | Complexity, recursion, trees, dynamic programming |

## Features

- Firebase email/password signup and login
- User profile with name, skills, education, target role, and experience level
- Dashboard with resume score, mock interview count, skill gaps, and progress
- Resume upload with PDF, DOCX, and TXT text extraction
- Gemini-powered resume analysis with fallback handling
- Interview question generator based on role and exam focus
- Interview answer submission with backend feedback
- Exam material library for the three IT readiness tests
- Flutter mobile MVP skeleton for future mobile work

## Tech Stack

| Layer | Technology |
| --- | --- |
| Backend | Django REST Framework |
| Local Database | SQLite |
| Production Database Target | PostgreSQL |
| Web Dashboard | React + Vite |
| Mobile App | Flutter |
| Authentication | Firebase Authentication |
| AI Provider | Gemini API |
| Deployment Target | Render for backend, Vercel for frontend |

## Project Structure

```text
CareerSync-AI/
|-- backend-django/
|   |-- career/
|   |-- config/
|   |-- manage.py
|   |-- requirements.txt
|   `-- Dockerfile
|-- web-react/
|   |-- src/
|   |-- package.json
|   `-- vercel.json
|-- mobile-flutter/
|-- docs/
|-- screenshots/
|-- architecture/
|-- render.yaml
|-- .gitignore
`-- README.md
```

## Backend Overview

The Django backend provides protected API endpoints. Each request must include a Firebase ID token in the `Authorization` header.

Firebase token verification is handled in:

```text
backend-django/career/authentication.py
```

Resume analysis and interview question generation are handled through:

```text
backend-django/career/services.py
```

Resume text extraction is handled through:

```text
backend-django/career/resume_parser.py
```

## API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/api/profile/` | Fetch user profile |
| POST | `/api/profile/` | Create or update user profile |
| POST | `/api/resume/upload/` | Upload and analyze resume |
| GET | `/api/resume/analysis/` | Fetch latest resume analysis |
| POST | `/api/interview/generate-questions/` | Generate interview questions |
| POST | `/api/interview/submit-answer/` | Submit interview answer |
| GET | `/api/dashboard/` | Fetch dashboard metrics |
| GET | `/api/exams/` | Fetch exam content |

## Environment Files

Real `.env` files are ignored by Git. Use `.env.example` files as templates.

Backend environment file:

```text
backend-django/.env
```

Important backend variables:

```env
DJANGO_SECRET_KEY=your_secret_key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
USE_SQLITE=True

FIREBASE_PROJECT_ID=your_firebase_project_id

AI_PROVIDER=gemini
AI_MODEL=gemini-2.5-flash
AI_API_KEY=your_gemini_api_key
```

React environment file:

```text
web-react/.env
```

Important React variables:

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_FIREBASE_API_KEY=your_firebase_web_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_APP_ID=your_web_app_id
VITE_FIREBASE_STORAGE_BUCKET=your_project.firebasestorage.app
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
```

## Firebase Setup

1. Create a Firebase project.
2. Create a Firebase Web App.
3. Enable Email/Password authentication.
4. Add Firebase web config values to `web-react/.env`.
5. Add the Firebase project ID to `backend-django/.env`.

For local MVP testing, the backend verifies Firebase ID tokens using Google's public certificates. For production, a Firebase Admin SDK service account can be added through `FIREBASE_CREDENTIALS_PATH`.

## AI Setup

CareerSync AI uses Gemini through the backend service layer. If a Gemini API key is configured, resume analysis and question generation can use Gemini. If the AI call fails, the backend still returns a safe fallback response.

AI service file:

```text
backend-django/career/services.py
```

## Screenshots

Screenshots are stored in:

```text
screenshots/
```

Included screenshots:

- Web dashboard
- Resume analysis
- Interview preparation
- Exam materials

## Flutter App

The Flutter folder contains a mobile MVP skeleton with:

- Login screen
- Dashboard
- Resume screen
- Interview screen
- Profile screen

Run Flutter later with:

```bash
cd mobile-flutter
flutter pub get
flutter run
```

## Production Deployment Plan

The current project is ready for local use. For public users, deploy the backend and frontend:

1. Deploy `backend-django/` on Render or another backend host.
2. Use PostgreSQL for production database storage.
3. Deploy `web-react/` on Vercel.
4. Set `VITE_API_BASE_URL` to the deployed backend API URL.
5. Add the frontend domain to Firebase authorized domains.
6. Add Firebase, Gemini, and database environment variables in the hosting platforms.

## Future Improvements

- Full production PostgreSQL deployment
- Admin dashboard for managing exam content
- More practice questions and timed tests
- Better AI scoring rubrics
- Resume history and version comparison
- Flutter app API integration
- Email verification and password reset
- User progress analytics

## How To Run The Website Locally

You need to run **backend** and **frontend** in two separate PowerShell windows.

### Terminal 1: Start Django Backend

Open PowerShell and run:

```powershell
cd "C:\Users\Gnanender\Desktop\AI Prep Platform\CareerSync-AI\backend-django"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv-codex\Scripts\activate
python manage.py runserver
```

Keep this terminal open.

You should see:

```text
Starting development server at http://127.0.0.1:8000/
```

### Terminal 2: Start React Website

Open a second PowerShell window and run:

```powershell
cd "C:\Users\Gnanender\Desktop\AI Prep Platform\CareerSync-AI\web-react"
& "C:\Program Files\nodejs\npm.cmd" run dev
```

Keep this terminal open too.

You should see:

```text
Local: http://localhost:5173/
```

### Open The Website

Open this URL in your browser:

```text
http://localhost:5173
```

Then:

1. Create an account using Firebase signup.
2. Log in.
3. Save your profile.
4. Upload a resume in PDF, DOCX, or TXT format.
5. Generate interview questions.
6. Submit an interview answer.

If the website opens but API actions fail, make sure the Django backend terminal is still running.
