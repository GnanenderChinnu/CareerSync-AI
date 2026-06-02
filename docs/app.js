const exams = [
  {
    name: "AptiReady Test",
    focus: "Aptitude",
    duration: "60 minutes",
    score: 68,
    summary: "Quantitative aptitude, logical reasoning, verbal ability, and workplace problem solving.",
    topics: ["Percentages", "Ratios", "Logical reasoning", "Verbal ability"],
  },
  {
    name: "CodeStart Test",
    focus: "Basic Coding",
    duration: "75 minutes",
    score: 74,
    summary: "Programming fundamentals for loops, arrays, strings, and functions.",
    topics: ["Variables", "Loops", "Arrays", "Strings"],
  },
  {
    name: "CodePro Test",
    focus: "Advanced Coding",
    duration: "120 minutes",
    score: 42,
    summary: "Data structures, algorithms, recursion, complexity, and dynamic programming.",
    topics: ["Complexity", "Recursion", "Trees", "Dynamic programming"],
  },
];

function examCard(exam) {
  return `
    <article>
      <span class="pill">${exam.focus}</span>
      <h2>${exam.name}</h2>
      <p>${exam.summary}</p>
      <div class="progress"><span style="width:${exam.score}%"></span></div>
      <p><strong>${exam.score}% ready</strong> · ${exam.duration}</p>
      <ul>${exam.topics.map((topic) => `<li>${topic}</li>`).join("")}</ul>
    </article>
  `;
}

document.getElementById("examCards").innerHTML = exams.map(examCard).join("");
document.getElementById("materialCards").innerHTML = exams.map(examCard).join("");

document.querySelectorAll(".nav").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".nav").forEach((item) => item.classList.remove("active"));
    document.querySelectorAll(".page").forEach((page) => page.classList.remove("active"));
    button.classList.add("active");
    document.getElementById(button.dataset.page).classList.add("active");
  });
});
