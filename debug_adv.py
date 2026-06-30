import json
from src.phase_c_guard import run_adversarial_suite

with open("adversarial_set_20.json", encoding="utf-8") as f:
    adv_set = json.load(f)

results = run_adversarial_suite(adv_set)
for r in results:
    if not r["passed"]:
        print(f"FAILED ID={r['id']}: Expected={r['expected']}, Actual={r['actual']} (Blocked by {r['blocked_by']})")
        print(f"  Input: {r['input']}")
