import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import { ArrowRight, BarChart3, BookOpen, Brain, CheckCircle2, FileText, GraduationCap, LogIn, LogOut, Upload, User } from "lucide-react";
import { apiRequest } from "./api";
import { loginWithEmail, logout, observeAuth, signupWithEmail } from "./firebase";
import "./styles.css";

const fallbackExams = [
  {
    id: "aptiready",
    name: "AptiReady Test",
    type: "Aptitude",
    level: "Foundation",
    duration: "60 minutes",
    summary: "Aptitude readiness for mandatory IT role screening.",
    score: 68,
    color: "teal",
    topics: ["Quantitative aptitude", "Logical reasoning", "Verbal ability", "Workplace problem solving"],
    materials: [
      { title: "Number systems and percentages", type: "Guide", duration: "35 min" },
      { title: "Logical arrangements practice", type: "Practice", duration: "45 min" },
      { title: "Reading comprehension basics", type: "Guide", duration: "25 min" },
    ],
  },
  {
    id: "codestart",
    name: "CodeStart Test",
    type: "Basic Coding",
    level: "Beginner",
    duration: "75 minutes",
    summary: "Basic coding exam for programming fundamentals.",
    score: 74,
    color: "blue",
    topics: ["Variables", "Loops", "Arrays", "Strings", "Functions"],
    materials: [
      { title: "Programming flow and syntax", type: "Guide", duration: "30 min" },
      { title: "Arrays and strings drills", type: "Practice", duration: "50 min" },
      { title: "Function-based problem solving", type: "Guide", duration: "40 min" },
    ],
  },
  {
    id: "codepro",
    name: "CodePro Test",
    type: "Advanced Coding",
    level: "Advanced",
    duration: "120 minutes",
    summary: "Advanced coding exam for data structures and algorithms.",
    score: 42,
    color: "amber",
    topics: ["Complexity", "Recursion", "Stacks and queues", "Trees", "Dynamic programming"],
    materials: [
      { title: "Big O and optimization patterns", type: "Guide", duration: "45 min" },
      { title: "Stacks, queues, and tree traversal", type: "Practice", duration: "70 min" },
      { title: "Dynamic programming starter set", type: "Challenge", duration: "90 min" },
    ],
  },
];

const defaultProfile = {
  name: "Demo Candidate",
  skills: ["Python", "SQL", "HTML", "CSS"],
  education: "B.Tech Computer Science",
  target_role: "Junior Software Engineer",
  experience_level: "fresher",
};

function App() {
  const demoPage = new URLSearchParams(window.location.search).get("demo");
  const [isLoggedIn, setIsLoggedIn] = useState(Boolean(demoPage));
  const [authUser, setAuthUser] = useState(null);
  const [page, setPage] = useState(demoPage || "dashboard");
  const [profile, setProfile] = useState(defaultProfile);
  const [dashboard, setDashboard] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [exams, setExams] = useState(fallbackExams);
  const [status, setStatus] = useState("");

  useEffect(() => {
    if (demoPage) {
      localStorage.setItem("careersync_token", "demo-token");
      return undefined;
    }

    return observeAuth(async (user) => {
      setAuthUser(user);
      setIsLoggedIn(Boolean(user));
      if (user) {
        localStorage.setItem("careersync_token", await user.getIdToken());
      } else {
        localStorage.removeItem("careersync_token");
      }
    });
  }, [demoPage]);

  useEffect(() => {
    if (!isLoggedIn) return;
    loadInitialData();
  }, [isLoggedIn]);

  async function loadInitialData() {
    setStatus("Loading backend data...");
    try {
      const [profileData, dashboardData, examsData, analysisData] = await Promise.all([
        apiRequest("/profile/"),
        apiRequest("/dashboard/"),
        apiRequest("/exams/"),
        apiRequest("/resume/analysis/"),
      ]);
      setProfile({ ...defaultProfile, ...profileData });
      setDashboard(dashboardData);
      setExams(normalizeExams(examsData, dashboardData));
      setAnalysis(analysisData);
      setStatus("Connected to Django API");
    } catch (error) {
      setStatus("Using demo data until the backend is running");
    }
  }

  if (!isLoggedIn) {
    return <LoginPage exams={exams} setStatus={setStatus} />;
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <Brain size={28} />
          <div>
            <strong>CareerSync AI</strong>
            <span>IT Readiness Prep</span>
          </div>
        </div>
        <NavButton active={page === "dashboard"} icon={<BarChart3 />} label="Dashboard" onClick={() => setPage("dashboard")} />
        <NavButton active={page === "profile"} icon={<User />} label="Profile" onClick={() => setPage("profile")} />
        <NavButton active={page === "resume"} icon={<FileText />} label="Resume AI" onClick={() => setPage("resume")} />
        <NavButton active={page === "interview"} icon={<GraduationCap />} label="Interview Prep" onClick={() => setPage("interview")} />
        <NavButton active={page === "materials"} icon={<BookOpen />} label="Exam Materials" onClick={() => setPage("materials")} />
        <button className="nav-button logout-button" onClick={async () => { await logout(); setPage("dashboard"); }}>
          <LogOut size={18} /><span>Logout</span>
        </button>
      </aside>

      <main className="content">
        <div className="status-line">{status}</div>
        {page === "dashboard" && <Dashboard dashboard={dashboard} exams={exams} profile={profile} />}
        {page === "profile" && <Profile authUser={authUser} profile={profile} setProfile={setProfile} onSaved={loadInitialData} setStatus={setStatus} />}
        {page === "resume" && <ResumeAnalysis analysis={analysis} onAnalyzed={loadInitialData} profile={profile} setStatus={setStatus} />}
        {page === "interview" && <InterviewPrep exams={exams} profile={profile} setStatus={setStatus} />}
        {page === "materials" && <Materials exams={exams} />}
      </main>
    </div>
  );
}

function LoginPage({ exams, setStatus }) {
  const [mode, setMode] = useState("login");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function submitAuth(event) {
    event.preventDefault();
    setError("");
    setStatus("");
    try {
      if (mode === "signup") {
        await signupWithEmail(name, email, password);
      } else {
        await loginWithEmail(email, password);
      }
    } catch (authError) {
      setError(readableAuthError(authError.code));
    }
  }

  return (
    <main className="login-page">
      <section className="login-panel">
        <div className="brand large">
          <Brain size={34} />
          <div>
            <strong>CareerSync AI</strong>
            <span>Mandatory IT exam preparation</span>
          </div>
        </div>
        <h1>Prepare for AptiReady, CodeStart, and CodePro in one focused workspace.</h1>
        <p>Create your account with Firebase Authentication and keep your preparation data connected to your profile.</p>
        <form className="auth-form" onSubmit={submitAuth}>
          {mode === "signup" && (
            <label>
              <span>Name</span>
              <input value={name} onChange={(event) => setName(event.target.value)} placeholder="Your name" />
            </label>
          )}
          <label>
            <span>Email</span>
            <input required type="email" value={email} onChange={(event) => setEmail(event.target.value)} placeholder="you@example.com" />
          </label>
          <label>
            <span>Password</span>
            <input required minLength={6} type="password" value={password} onChange={(event) => setPassword(event.target.value)} placeholder="At least 6 characters" />
          </label>
          {error && <div className="error-line">{error}</div>}
          <button className="primary" type="submit">
            <LogIn size={18} /> {mode === "signup" ? "Create Account" : "Login"}
          </button>
          <button className="link-button" type="button" onClick={() => setMode(mode === "signup" ? "login" : "signup")}>
            {mode === "signup" ? "Already have an account? Login" : "New here? Create an account"}
          </button>
        </form>
      </section>
      <section className="exam-strip">
        {exams.map((exam) => (
          <article className={`exam-card ${exam.color}`} key={exam.id}>
            <span>{exam.type}</span>
            <h2>{exam.name}</h2>
            <p>{exam.duration} · {exam.level}</p>
          </article>
        ))}
      </section>
    </main>
  );
}

function Dashboard({ dashboard, exams, profile }) {
  const progress = dashboard?.progress_percentage || Math.round(exams.reduce((sum, exam) => sum + exam.score, 0) / exams.length);
  return (
    <>
      <Header title={`Welcome, ${profile.name}`} subtitle="Track your mandatory IT role readiness in a clean weekly plan." />
      <section className="metrics">
        <Metric label="Resume score" value={`${dashboard?.resume_score || 72}%`} icon={<FileText />} />
        <Metric label="Mock interviews" value={dashboard?.completed_mock_interviews || 0} icon={<GraduationCap />} />
        <Metric label="Overall progress" value={`${progress}%`} icon={<BarChart3 />} />
      </section>
      {dashboard?.skills_to_improve?.length > 0 && (
        <section className="insight-band">
          <strong>Skills to improve</strong>
          <span>{dashboard.skills_to_improve.join(", ")}</span>
        </section>
      )}
      <section className="exam-grid">
        {exams.map((exam) => (
          <ExamProgressCard exam={exam} key={exam.id} />
        ))}
      </section>
    </>
  );
}

function Profile({ authUser, profile, setProfile, onSaved, setStatus }) {
  const [draft, setDraft] = useState(toProfileForm(profile));

  useEffect(() => {
    setDraft(toProfileForm(profile));
  }, [profile]);

  const update = (field, value) => setDraft((current) => ({ ...current, [field]: value }));

  async function saveProfile() {
    setStatus("Saving profile...");
    const payload = {
      name: draft.name,
      skills: draft.skills.split(",").map((skill) => skill.trim()).filter(Boolean),
      education: draft.education,
      target_role: draft.target_role,
      experience_level: draft.experience_level,
    };
    try {
      const saved = await apiRequest("/profile/", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      setProfile(saved);
      setStatus("Profile saved");
      await onSaved();
    } catch (error) {
      setStatus("Profile save failed. Check backend server.");
    }
  }

  return (
    <>
      <Header title="Profile" subtitle="Keep this aligned with your target IT role and current skills." />
      <section className="form-card">
        {authUser?.email && <div className="profile-email">Signed in as {authUser.email}</div>}
        <label>
          <span>Name</span>
          <input value={draft.name} onChange={(event) => update("name", event.target.value)} />
        </label>
        <label>
          <span>Target role</span>
          <input value={draft.target_role} onChange={(event) => update("target_role", event.target.value)} />
        </label>
        <label>
          <span>Education</span>
          <input value={draft.education} onChange={(event) => update("education", event.target.value)} />
        </label>
        <label>
          <span>Skills</span>
          <input value={draft.skills} onChange={(event) => update("skills", event.target.value)} />
        </label>
        <label>
          <span>Experience level</span>
          <select value={draft.experience_level} onChange={(event) => update("experience_level", event.target.value)}>
            <option value="fresher">Fresher</option>
            <option value="entry">Entry Level</option>
            <option value="mid">Mid Level</option>
          </select>
        </label>
        <button className="primary" onClick={saveProfile}><CheckCircle2 size={18} /> Save Profile</button>
      </section>
    </>
  );
}

function ResumeAnalysis({ analysis, onAnalyzed, profile, setStatus }) {
  const [file, setFile] = useState(null);
  const [resumeText, setResumeText] = useState("Built a student management app using Python, SQL, HTML, and CSS.");

  async function uploadResume() {
    setStatus("Analyzing resume...");
    const formData = new FormData();
    if (file) formData.append("file", file);
    formData.append("extracted_text", resumeText);
    try {
      await apiRequest("/resume/upload/", {
        method: "POST",
        body: formData,
      });
      await onAnalyzed();
      setStatus("Resume analyzed with backend AI service");
    } catch (error) {
      setStatus("Resume upload failed. Select a file or check backend server.");
    }
  }

  const feedback = analysis || {
    resume_score: 78,
    strengths: ["Good fresher profile direction", `Relevant skills for ${profile.target_role}`],
    suggested_improvements: ["Add project outcomes", "Group skills by confidence", "Add CodeStart and CodePro practice links"],
    weaknesses: ["Resume needs stronger project impact statements"],
    missing_skills: ["Data Structures", "Communication"],
  };

  return (
    <>
      <Header title="AI Resume Analysis" subtitle="Upload a resume and let the backend AI service create focused feedback." />
      <section className="two-column">
        <article className="form-card">
          <h2>Resume Upload</h2>
          <label>
            <span>Resume file</span>
            <input type="file" accept=".pdf,.doc,.docx,.txt" onChange={(event) => setFile(event.target.files?.[0] || null)} />
          </label>
          <label>
            <span>Resume text preview</span>
            <textarea value={resumeText} onChange={(event) => setResumeText(event.target.value)} />
          </label>
          <button className="primary" onClick={uploadResume}><Upload size={18} /> Analyze Resume</button>
        </article>
        <article className="prep-card">
          <h2>AI Feedback</h2>
          <Metric label="Resume score" value={`${feedback.resume_score}%`} icon={<FileText />} />
          <FeedbackList title="Strengths" items={feedback.strengths} />
          <FeedbackList title="Weaknesses" items={feedback.weaknesses} />
          <FeedbackList title="Missing skills" items={feedback.missing_skills} />
          <FeedbackList title="Improve" items={feedback.suggested_improvements} />
        </article>
      </section>
    </>
  );
}

function InterviewPrep({ exams, profile, setStatus }) {
  const [examId, setExamId] = useState("codepro");
  const [questions, setQuestions] = useState([
    `Why are you interested in the ${profile.target_role} role?`,
    "Explain one project where you solved a coding problem.",
    "How do you manage time during AptiReady-style questions?",
  ]);
  const [sessionId, setSessionId] = useState(null);
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState("");

  async function generateQuestions() {
    setStatus("Generating interview questions...");
    try {
      const data = await apiRequest("/interview/generate-questions/", {
        method: "POST",
        body: JSON.stringify({ job_role: profile.target_role, exam_id: examId }),
      });
      setQuestions(data.questions || []);
      setSessionId(data.session_id);
      setFeedback("");
      setStatus("Questions generated");
    } catch (error) {
      setStatus("Question generation failed. Check backend server.");
    }
  }

  async function submitAnswer() {
    if (!sessionId || !answer.trim()) {
      setStatus("Generate questions and write an answer first");
      return;
    }
    try {
      const data = await apiRequest("/interview/submit-answer/", {
        method: "POST",
        body: JSON.stringify({ session_id: sessionId, answer }),
      });
      setFeedback(data.feedback);
      setAnswer("");
      setStatus(data.completed ? "Mock interview completed" : "Answer submitted");
    } catch (error) {
      setStatus("Answer submit failed. Check backend server.");
    }
  }

  return (
    <>
      <Header title="Interview Preparation" subtitle="Generate role-based questions and practice structured answers." />
      <section className="prep-card">
        <div className="card-top">
          <div>
            <h2>{profile.target_role}</h2>
            <select value={examId} onChange={(event) => setExamId(event.target.value)}>
              {exams.map((exam) => <option value={exam.id} key={exam.id}>{exam.name}</option>)}
            </select>
          </div>
          <button className="secondary" onClick={generateQuestions}><ArrowRight size={18} /> Generate</button>
        </div>
        <div className="question-list">
          {questions.map((question) => <p key={question}>{question}</p>)}
        </div>
        <textarea value={answer} onChange={(event) => setAnswer(event.target.value)} placeholder="Write your answer here..." />
        <div className="actions">
          <button className="primary" onClick={submitAnswer}><CheckCircle2 size={18} /> Submit Answer</button>
          {feedback && <span className="inline-feedback">{feedback}</span>}
        </div>
      </section>
    </>
  );
}

function Materials({ exams }) {
  return (
    <>
      <Header title="Exam Materials" subtitle="A compact resource library for the three required IT readiness exams." />
      <section className="exam-grid">
        {exams.map((exam) => (
          <article className="prep-card" key={exam.id}>
            <span className={`pill ${exam.color}`}>{exam.type}</span>
            <h2>{exam.name}</h2>
            <p>{exam.summary}</p>
            <h3>Topics</h3>
            <ul>{exam.topics.map((topic) => <li key={topic}>{topic}</li>)}</ul>
            <h3>Materials</h3>
            <ul>{exam.materials.map((item) => <li key={item.title}>{item.title} · {item.type} · {item.duration}</li>)}</ul>
          </article>
        ))}
      </section>
    </>
  );
}

function ExamProgressCard({ exam }) {
  return (
    <article className="prep-card">
      <div className="card-top">
        <span className={`pill ${exam.color}`}>{exam.type}</span>
        <strong>{exam.duration}</strong>
      </div>
      <h2>{exam.name}</h2>
      <p>{exam.summary}</p>
      <div className="progress-line"><span style={{ width: `${exam.score}%` }} /></div>
      <p>{exam.score}% ready</p>
      <ul>{exam.topics.slice(0, 3).map((topic) => <li key={topic}>{topic}</li>)}</ul>
    </article>
  );
}

function FeedbackList({ title, items = [] }) {
  if (!items.length) return null;
  return (
    <>
      <h3>{title}</h3>
      <ul>{items.map((item) => <li key={item}>{item}</li>)}</ul>
    </>
  );
}

function Header({ title, subtitle }) {
  return <header className="header"><h1>{title}</h1><p>{subtitle}</p></header>;
}

function Metric({ label, value, icon }) {
  return <article className="metric"><div>{icon}</div><span>{label}</span><strong>{value}</strong></article>;
}

function NavButton({ active, icon, label, onClick }) {
  return <button className={`nav-button ${active ? "active" : ""}`} onClick={onClick}>{React.cloneElement(icon, { size: 18 })}<span>{label}</span></button>;
}

function normalizeExams(apiExams, dashboard) {
  const scores = { aptiready: 68, codestart: 74, codepro: 42 };
  const types = { aptiready: "Aptitude", codestart: "Basic Coding", codepro: "Advanced Coding" };
  const colors = { aptiready: "teal", codestart: "blue", codepro: "amber" };
  const source = apiExams?.length ? apiExams : dashboard?.recommended_exams || fallbackExams;
  return source.map((exam) => ({
    ...exam,
    type: exam.type || types[exam.id] || exam.level,
    color: colors[exam.id] || "teal",
    score: scores[exam.id] || 60,
    materials: exam.materials || [],
  }));
}

function toProfileForm(profile) {
  return {
    ...defaultProfile,
    ...profile,
    skills: Array.isArray(profile.skills) ? profile.skills.join(", ") : profile.skills,
  };
}

function readableAuthError(code) {
  const messages = {
    "auth/email-already-in-use": "This email already has an account. Try login instead.",
    "auth/invalid-email": "Enter a valid email address.",
    "auth/invalid-credential": "Email or password is incorrect.",
    "auth/weak-password": "Use a password with at least 6 characters.",
  };
  return messages[code] || "Authentication failed. Please try again.";
}

createRoot(document.getElementById("root")).render(<App />);
