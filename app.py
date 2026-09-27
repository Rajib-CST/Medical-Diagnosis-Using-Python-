import json
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory


BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"
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
    return json.loads((BASE_DIR / "data" / "knowledge.json").read_text(encoding="utf-8"))


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
    return send_from_directory(PUBLIC_DIR, "index.html")


@app.get("/<path:filename>")
def static_asset(filename):
    return send_from_directory(PUBLIC_DIR, filename)


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