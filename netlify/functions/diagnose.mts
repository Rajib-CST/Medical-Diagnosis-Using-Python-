import type { Config } from '@netlify/functions'
import KNOWLEDGE_DATA from '../../data/knowledge.json'

// Mirrors the symptom order used by the original Flask app (app.py) and the public/ frontend.
const SYMPTOMS: Array<[string, string]> = [
  ['headache', 'Headache'],
  ['back_pain', 'Back pain'],
  ['chest_pain', 'Chest pain'],
  ['cough', 'Cough'],
  ['fainting', 'Fainting'],
  ['sore_throat', 'Sore throat'],
  ['fatigue', 'Fatigue'],
  ['sunken_eyes', 'Sunken eyes'],
  ['low_body_temp', 'Low body temperature'],
  ['restlessness', 'Restlessness'],
  ['fever', 'Fever'],
  ['nausea', 'Nausea'],
  ['blurred_vision', 'Blurred vision'],
]

const LEVELS = new Set(['no', 'low', 'high', 'yes'])

type Knowledge = {
  profile: string[]
  description: string
  treatment: string
}

// Educational placeholder knowledge base (not medical advice), shared with app.py via data/knowledge.json,
// since the original "Disease symptoms/descriptions/treatments" data files were never committed.
const KNOWLEDGE: Record<string, Knowledge> = KNOWLEDGE_DATA

type RankedResult = {
  disease: string
  matches: number
  positive_matches: number
  score: number
  matched_symptoms: string[]
}

function rankDiseases(answers: Record<string, string>): RankedResult[] {
  const normalized = SYMPTOMS.map(([key]) => (answers[key] ?? 'no').toLowerCase())
  const results: RankedResult[] = []

  for (const [disease, record] of Object.entries(KNOWLEDGE)) {
    const profile = record.profile
    let matches = 0
    let positiveMatches = 0
    const matchedSymptoms: string[] = []

    normalized.forEach((answer, index) => {
      const expected = profile[index]
      if (answer === expected) {
        matches += 1
        if (answer !== 'no') {
          positiveMatches += 1
          matchedSymptoms.push(SYMPTOMS[index][1])
        }
      }
    })

    results.push({
      disease,
      matches,
      positive_matches: positiveMatches,
      score: Math.round((matches / SYMPTOMS.length) * 100),
      matched_symptoms: matchedSymptoms,
    })
  }

  return results.sort((a, b) => b.positive_matches - a.positive_matches || b.matches - a.matches)
}

export default async (req: Request) => {
  let payload: Record<string, unknown> = {}
  try {
    payload = await req.json()
  } catch {
    payload = {}
  }

  const answers: Record<string, string> = {}
  for (const [key] of SYMPTOMS) {
    const value = String(payload[key] ?? 'no').toLowerCase()
    if (LEVELS.has(value)) {
      answers[key] = value
    }
  }

  if (!Object.values(answers).some((value) => value !== 'no')) {
    return Response.json({ error: 'Select at least one symptom before assessing.' }, { status: 400 })
  }

  const ranked = rankDiseases(answers)
  const top = ranked[0]
  const record = KNOWLEDGE[top.disease]

  return Response.json({
    result: top,
    description: record.description,
    treatment: record.treatment,
    alternatives: ranked.slice(1, 4),
  })
}

export const config: Config = {
  path: '/api/diagnose',
  method: 'POST',
}
