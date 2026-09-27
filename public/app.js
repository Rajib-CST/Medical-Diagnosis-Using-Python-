const SYMPTOMS = [
  ["headache", "Headache"],
  ["back_pain", "Back pain"],
  ["chest_pain", "Chest pain"],
  ["cough", "Cough"],
  ["fainting", "Fainting"],
  ["sore_throat", "Sore throat"],
  ["fatigue", "Fatigue"],
  ["sunken_eyes", "Sunken eyes"],
  ["low_body_temp", "Low body temperature"],
  ["restlessness", "Restlessness"],
  ["fever", "Fever"],
  ["nausea", "Nausea"],
  ["blurred_vision", "Blurred vision"],
];

const LEVEL_LABELS = {
  no: "No",
  low: "Mild",
  high: "Severe",
  yes: "Yes",
};

const grid = document.getElementById("symptom-grid");
const form = document.getElementById("symptom-form");
const resultEl = document.getElementById("result");

for (const [key, label] of SYMPTOMS) {
  const field = document.createElement("div");
  field.className = "symptom-field";

  const fieldLabel = document.createElement("label");
  fieldLabel.setAttribute("for", key);
  fieldLabel.textContent = label;

  const select = document.createElement("select");
  select.id = key;
  select.name = key;
  for (const [value, text] of Object.entries(LEVEL_LABELS)) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = text;
    select.appendChild(option);
  }

  field.appendChild(fieldLabel);
  field.appendChild(select);
  grid.appendChild(field);
}

function renderResult(data) {
  resultEl.hidden = false;

  if (data.error) {
    resultEl.innerHTML = `<p class="error">${data.error}</p>`;
    return;
  }

  const { result, description, treatment, alternatives } = data;

  const matchedList = result.matched_symptoms.length
    ? `<ul class="matched-symptoms">${result.matched_symptoms.map((s) => `<li>${s}</li>`).join("")}</ul>`
    : "<p>No matched symptoms.</p>";

  const alternativesHtml = alternatives.length
    ? `<div class="alternatives">
        <h3>Other possibilities</h3>
        <ul>${alternatives.map((alt) => `<li>${alt.disease} &mdash; ${alt.score}% match</li>`).join("")}</ul>
      </div>`
    : "";

  resultEl.innerHTML = `
    <h2>${result.disease}<span class="score-badge">${result.score}% match</span></h2>
    <p>${description}</p>
    <h3>Matched symptoms</h3>
    ${matchedList}
    <h3>Suggested next steps</h3>
    <p>${treatment}</p>
    ${alternativesHtml}
  `;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const answers = Object.fromEntries(formData.entries());

  try {
    const response = await fetch("/api/diagnose", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(answers),
    });
    const data = await response.json();
    renderResult(data);
  } catch (err) {
    renderResult({ error: "Something went wrong reaching the diagnosis service. Please try again." });
  }
});
