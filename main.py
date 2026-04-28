import json
from parser import load_spec, extract_endpoints

from core.scanner import test_endpoint
from core.idor import test_idor
from core.rate import test_rate_limit
from core.fuzz import fuzz_endpoint

BASE_URL = "http://127.0.0.1:5000"
SPEC_FILE = "api.yaml"

print("\n[+] API SECURITY SCANNER PRO v2")
print("=" * 50)

# -------------------------
# LOAD SPEC
# -------------------------
spec = load_spec(SPEC_FILE)
endpoints = extract_endpoints(spec)

print(f"[+] Endpoints encontrados: {len(endpoints)}")

# -------------------------
# RESULT STORAGE
# -------------------------
results = []
vulnerabilities = []

# -------------------------
# SCAN LOOP
# -------------------------
for ep in endpoints:
    print("\n" + "-" * 50)
    print(f"[SCAN] {ep['method']} {ep['path']}")

    # HTTP TEST
    res = test_endpoint(BASE_URL, ep)
    results.append(res)

    # IDOR
    idor_findings = test_idor(BASE_URL, ep)
    vulnerabilities.extend(idor_findings)

    # RATE LIMIT
    rate_findings = test_rate_limit(BASE_URL, ep)
    vulnerabilities.extend(rate_findings)

    # FUZZING
    fuzz_findings = fuzz_endpoint(BASE_URL, ep)
    vulnerabilities.extend(fuzz_findings)

# -------------------------
# SAVE REPORT (JSON)
# -------------------------
report = {
    "target": BASE_URL,
    "endpoints": len(endpoints),
    "results": results,
    "vulnerabilities": vulnerabilities
}

with open("reports/report.json", "w") as f:
    json.dump(report, f, indent=4)

print("\n[+] SCAN COMPLETADO")
print("[+] Report guardado en reports/report.json")

# -------------------------
# SUMMARY
# -------------------------
print("\n[RESUMEN]")

high = len([v for v in vulnerabilities if v.get("severity") == "HIGH"])
medium = len([v for v in vulnerabilities if v.get("severity") == "MEDIUM"])
low = len([v for v in vulnerabilities if v.get("severity") == "LOW"])

print(f"HIGH: {high}")
print(f"MEDIUM: {medium}")
print(f"LOW: {low}")

print("\n[✔] Done")
