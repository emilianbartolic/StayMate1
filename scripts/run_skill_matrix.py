"""Check all internal skill stages against every configured accommodation.

This deterministic contract matrix is fast and does not spend model tokens.
It verifies that each scenario produces a result for every skill and that
property retrieval stays scoped to the selected property's own facts.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "backend"))
from app import (  # noqa: E402
    ALL_PROPERTIES, SKILLS, classify_intent, evaluate_skills, find_facts,
)

CASES = {
    "intent-routing": "Gibt es Parkplätze?",
    "property-retrieval": "Gibt es Parkplätze?",
    "empathetic-response": "Ich bin enttäuscht und die Heizung funktioniert nicht.",
    "deescalation": "I am unhappy and the heater is broken.",
    "multilingual": "Is parking available?",
    "clarifying-question": "Does the apartment include a piano?",
    "technical-triage": "Die Heizung funktioniert nicht.",
    "urgency-priority": "Ich fühle mich unsicher.",
    "host-handoff": "Kann ich früher einchecken?",
    "faq-improvement": "Please add a piano question to the FAQ.",
    "conversation-summary": "Please summarize my issue.",
}
SKILL_IDS = [item["id"] for item in SKILLS["skills"]]
failures = []
checks = 0
for property_data in ALL_PROPERTIES:
    for skill_id, question in CASES.items():
        matches = find_facts(question, property_data)
        category, priority = classify_intent(question, matches)
        escalated = category in {"host_decision", "safety", "technical_support", "unknown"}
        active, results = evaluate_skills(question, property_data, matches, category, priority, escalated)
        checks += 1
        expected = set(SKILL_IDS)
        ok = set(results) == expected and results["property-retrieval"].startswith(property_data["id"]) and skill_id in active
        if not ok:
            failures.append(f"{property_data['id']}/{skill_id}")
        print(f"{'PASS' if ok else 'FAIL'} {property_data['id']}/{skill_id} · {len(results)} skills evaluated · {category}/{priority}")
print(f"{checks-len(failures)}/{checks} skill/property matrix cells passed")
raise SystemExit(1 if failures else 0)
