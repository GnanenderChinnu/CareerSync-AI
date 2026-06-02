# CareerSync AI

CareerSync AI is a realistic MVP for IT career preparation. It helps freshers and job seekers prepare for three mandatory IT readiness exams, improve resumes with AI feedback, and practice interview questions.

The first version stays intentionally small: it works like a real platform, but uses compact sample content instead of a huge database.

## Exams

| Exam | Focus | MVP Content |
| --- | --- | --- |
| AptiReady Test | Aptitude | Quantitative aptitude, logical reasoning, verbal ability |
| CodeStart Test | Basic coding | Loops, arrays, strings, functions |
| CodePro Test | Advanced coding | Data structures, algorithms, complexity, dynamic programming |

## Tech Stack

- Backend: Django REST Framework
- Database: PostgreSQL
- Web dashboard: React + Vite
- Mobile app: Flutter
- Authentication: Firebase Authentication with local demo-token support
- AI: Gemini API integration with mock fallback

## Project Structure

```text
CareerSync-AI/
|-- backend-django/
|-- mobile-flutter/
|-- web-react/
|-- docs/
|-- screenshots/
|-- architecture/
`-- README.md
```

## Static Web Demo

The hosted version is intended for recruiters and portfolio visitors to preview the CareerSync AI web dashboard. It does not require a running local server to view the frontend.

Live static demo:

https://gnanenderchinnu.github.io/CareerSync-AI/

Main web dashboard files:

```text
web-react/src/main.jsx
web-react/src/styles.css
web-react/src/firebase.js
web-react/src/api.js
```

The static demo supports:

- Firebase login/signup screen.
- Dashboard preview.
- Profile, resume analysis, interview prep, and exam material pages.
- API-ready frontend structure for the Django backend.

## Backend Setup

```bash
cd backend-django
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py runserver
```

Update `.env` with your PostgreSQL credentials. For local API testing, use:

```text
Authorization: Bearer demo-token
```

If PostgreSQL is not installed yet, set this in `backend-django/.env` for local testing:

```env
USE_SQLITE=True
```

## React Dashboard Setup

```bash
cd web-react
npm install
copy .env.example .env
npm run dev
```

Open `http://localhost:5173`.

On Windows, if `npm` is not available directly but Node is installed, use:

```powershell
& "C:\Program Files\nodejs\npm.cmd" run dev
```

## Flutter App Setup

```bash
cd mobile-flutter
flutter pub get
flutter run
```

Before production login, run `flutterfire configure` and add Firebase configuration.

## API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| POST | `/api/profile/` | Create or update profile |
| GET | `/api/profile/` | Fetch profile |
| POST | `/api/resume/upload/` | Upload resume |
| GET | `/api/resume/analysis/` | Fetch latest AI resume analysis |
| POST | `/api/interview/generate-questions/` | Generate role-based questions |
| POST | `/api/interview/submit-answer/` | Submit interview answer |
| GET | `/api/dashboard/` | Fetch dashboard metrics |
| GET | `/api/exams/` | Fetch AptiReady, CodeStart, and CodePro material |

## Firebase Notes

- Backend Firebase Admin config belongs in `backend-django/.env`.
- React Firebase web config belongs in `web-react/.env`.
- Flutter Firebase config should be generated using FlutterFire.
- Do not commit real API keys or Firebase service account files.

For the web dashboard, enable **Email/Password** in Firebase Authentication and add these values to `web-react/.env`:

```env
VITE_FIREBASE_API_KEY=your_web_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_APP_ID=your_web_app_id
VITE_FIREBASE_STORAGE_BUCKET=your_project.firebasestorage.app
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
```

For the backend, set the same project ID:

```env
FIREBASE_PROJECT_ID=your_project_id
```

`FIREBASE_CREDENTIALS_PATH` is optional for local MVP testing because the backend can verify Firebase ID tokens with Google's public certificates. For production, use a Firebase Admin SDK service account file.

## AI Notes

The backend uses `career/services.py` as the AI boundary. Gemini is supported through the REST `generateContent` API when these values are set in `backend-django/.env`:

```env
AI_PROVIDER=gemini
AI_MODEL=gemini-2.5-flash
AI_API_KEY=your_key_here
```

If `AI_API_KEY` is missing or the Gemini call fails, it returns mock responses so the MVP still works.

## Screenshots

Screenshots are available in `screenshots/`:

- Web dashboard
- Resume analysis
- Interview preparation
- Exam materials

## Future Scope

- Real PDF/DOCX resume parsing
- Deployed Django backend for production API access
- Admin dashboard for exam content management
- Practice tests with timers and scoring
- Learning path recommendations
- Payment or subscription module
- Deployment with Docker and CI
