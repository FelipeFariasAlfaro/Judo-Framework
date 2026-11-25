"""
Failure triage: classify failed steps from ``judo_reports/result.json`` into likely causes
with the evidence found and a concrete next action. Heuristic, no LLM involved.
"""
import re
from typing import Any, Dict, List

CATEGORIES = {
    "undefined_step": "A step in the feature does not exist",
    "environment": "The API was unreachable or too slow (network, DNS, TLS, timeout)",
    "auth": "Authentication or authorization problem (401/403)",
    "not_found": "Endpoint or data not found (404)",
    "api_bug": "The API answered with a server error (5xx)",
    "validation_error": "The API rejected the request (400/422)",
    "assertion_mismatch": "The API answered, but not with what the test expects",
    "test_data": "A variable/file/data needed by the test is missing",
    "test_bug": "The step itself raised an unexpected Python error",
}


def classify_step(step: Dict[str, Any]) -> Dict[str, Any]:
    error = step.get("error", "") or ""
    ex = step.get("exchange") or {}
    status = ((ex.get("response") or {}).get("status_code")) if ex else None
    low = error.lower()
    ev: List[str] = []

    if error == "Undefined step":
        cat, action = "undefined_step", "Run `judo validate` and use `judo steps --search` to find the right step."
    elif any(k in low for k in ("connectionerror", "timeout", "timed out", "name or service not known",
                                "max retries exceeded", "sslerror", "connection refused")):
        cat, action = "environment", "Check the base URL, network/VPN, TLS settings and `I set the timeout`."
    elif status in (401, 403):
        cat, action = "auth", "Verify credentials/token (env vars, expiry) and the auth steps used."
    elif status == 404:
        cat, action = "not_found", "Check the path, base URL and that the test data exists in this environment."
    elif status is not None and status >= 500:
        cat, action = "api_bug", "Likely an API defect: capture the request/response and report it."
    elif status in (400, 422):
        cat, action = "validation_error", "Compare the request body with the API contract (required fields, types)."
    elif any(k in low for k in ("variable", "no such file", "filenotfound", "not found:", "undefined variable")):
        cat, action = "test_data", "Define the variable/file or extract it in a previous step."
    elif any(k in error for k in ("AttributeError", "TypeError", "KeyError", "NameError", "IndexError")):
        cat, action = "test_bug", "Unexpected error inside a step; check the arguments and the step's requirements."
    elif status is not None:
        cat, action = "assertion_mismatch", "Review the expected value vs the actual response (API change or stale test?)."
    else:
        cat, action = "assertion_mismatch", "Review the error message and the step arguments."

    if status is not None:
        ev.append(f"HTTP status {status}")
    m = re.search(r"expected (.+?), but got (.+)", error)
    if m:
        ev.append(f"expected {m.group(1)} / actual {m.group(2)[:120]}")
    if error:
        ev.append(error[:200])
    return {"category": cat, "meaning": CATEGORIES[cat], "evidence": ev, "suggested_action": action}


def explain(result: Dict[str, Any]) -> Dict[str, Any]:
    findings = []
    for feat in result.get("features", []):
        for sc in feat.get("scenarios", []):
            if sc.get("status") != "failed":
                continue
            for st in sc["steps"] if isinstance(sc["steps"], list) else []:
                if st.get("status") == "failed":
                    c = classify_step(st)
                    findings.append({"feature": feat["name"], "scenario": sc["name"], "step": st["step"],
                                     "line": st.get("line"), **c})
                    break
    counts: Dict[str, int] = {}
    for f in findings:
        counts[f["category"]] = counts.get(f["category"], 0) + 1
    return {"failed_scenarios": len(findings), "by_category": counts, "findings": findings}
