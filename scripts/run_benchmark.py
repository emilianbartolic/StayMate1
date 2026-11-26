"""Run the deterministic agent acceptance catalog against the shared hub."""
import json
from urllib.request import Request, urlopen
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "trinity/agents/staymate/tests/test_cases.json").read_text())
passed = 0
for case in CASES:
    payload = json.dumps({"property_id":"design-maisonette", "question":case["question"]}).encode()
    request = Request("http://127.0.0.1:8000/api/cli/chat", data=payload, headers={"Content-Type":"application/json", "Origin":"http://127.0.0.1:8000"}, method="POST")
    with urlopen(request, timeout=20) as response:
        result = json.load(response)
    actual = result["decision"]
    ok = actual == case["expected"]
    ok = ok and result.get("model_used") is True and "skills_applied" not in result and "skill_results" not in result
    passed += int(ok)
    print(f"{'PASS' if ok else 'FAIL'} {case['id']}: expected={case['expected']} actual={actual}")
print(f"{passed}/{len(CASES)} acceptance cases passed")
raise SystemExit(0 if passed == len(CASES) else 1)
