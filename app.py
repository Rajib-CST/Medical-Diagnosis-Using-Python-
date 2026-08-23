from pathlib import Path

from flask import Flask, jsonify, render_template, request


BASE_DIR = Path(__file__).resolve().parent
SYMPTOMS = [
    ("headache", "Headache"),
    ("back_pain", "Back pain"),
    ("chest_pain", "Chest pain"),
    ("cough", "Cough"),
    ("fainting", "Fainting"),
    ("sore_throat", "Sore throat"),
    ("fatigue", "Fatigue"),
    ("sunken_eyes", "Sunken eyes"),
    ("low_body_temp", "Low body temperature"),
    ("restlessness", "Restlessness"),
    ("fever", "Fever"),
    ("nausea", "Nausea"),
    ("blurred_vision", "Blurred vision"),
]
LEVELS = {"no", "low", "high", "yes"}


def load_knowledge():
    diseases = [
        item.strip()
        for item in (BASE_DIR / "diseases.txt").read_text(encoding="utf-8").splitlines()
        if item.strip()
    ]
    knowledge = {}
    for disease in diseases:
        symptom_path = BASE_DIR / "Disease symptoms" / f"{disease}.txt"
        knowledge[disease] = {
            "profile": [line.strip().lower() for line in symptom_path.read_text(encoding="utf-8").splitlines()],
            "description": (BASE_DIR / "Disease descriptions" / f"{disease}.txt").read_text(encoding="utf-8").strip(),
            "treatment": (BASE_DIR / "Disease treatments" / f"{disease}.txt").read_text(encoding="utf-8").strip(),
        }
    return knowledge


KNOWLEDGE = load_knowledge()
app = Flask(__name__)


def rank_diseases(answers):
    normalized = [answers.get(key, "no").lower() for key, _ in SYMPTOMS]
    results = []
    for disease, record in KNOWLEDGE.items():
        profile = record["profile"]
        matches = sum(answer == expected for answer, expected in zip(normalized, profile))
        positive_matches = sum(
            answer == expected and answer != "no"
            for answer, expected in zip(normalized, profile)
        )
        results.append(
            {
                "disease": disease,
                "matches": matches,
                "positive_matches": positive_matches,
                "score": round(matches / len(SYMPTOMS) * 100),
                "matched_symptoms": [
                    label
                    for (key, label), answer, expected in zip(SYMPTOMS, normalized, profile)
                    if answer == expected and answer != "no"
                ],
            }
        )
    return sorted(results, key=lambda result: (result["positive_matches"], result["matches"]), reverse=True)


@app.get("/")
def index():
    return render_template("index.html", symptoms=SYMPTOMS)


@app.post("/api/diagnose")
def diagnose():
    payload = request.get_json(silent=True) or {}
    answers = {
        key: str(payload.get(key, "no")).lower()
        for key, _ in SYMPTOMS
        if str(payload.get(key, "no")).lower() in LEVELS
    }
    if not any(value != "no" for value in answers.values()):
        return jsonify({"error": "Select at least one symptom before assessing."}), 400
    ranked = rank_diseases(answers)
    top = ranked[0]
    record = KNOWLEDGE[top["disease"]]
    return jsonify(
        {
            "result": top,
            "description": record["description"],
            "treatment": record["treatment"],
            "alternatives": ranked[1:4],
        }
    )


if __name__ == "__main__":
    app.run(debug=True)