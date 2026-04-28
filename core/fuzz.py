import requests

PAYLOADS = [
    "1",
    "999999",
    "'",
    "\"",
    "' OR 1=1",
    "<script>alert(1)</script>",
    "../../etc/passwd",
    "%00",
    "${7*7}",
    "null"
]

def fuzz_endpoint(base_url, endpoint):
    findings = []

    if "{id}" not in endpoint["path"]:
        return findings

    baseline_url = base_url + endpoint["path"].replace("{id}", "1")

    try:
        baseline = requests.get(baseline_url)
        baseline_len = len(baseline.text)
    except:
        baseline_len = 0

    for p in PAYLOADS:
        url = base_url + endpoint["path"].replace("{id}", str(p))

        try:
            r = requests.get(url)

            # 🔥 DETECCIÓN 1: SERVER ERRORS
            if r.status_code >= 500:
                findings.append({
                    "type": "SERVER_ERROR",
                    "url": url,
                    "severity": "HIGH"
                })

            # 🔥 DETECCIÓN 2: SQLi hint
            if any(x in r.text.lower() for x in ["sql", "syntax", "error"]):
                findings.append({
                    "type": "POSSIBLE_SQLI",
                    "url": url,
                    "severity": "HIGH"
                })

            # 🔥 DETECCIÓN 3: RESPONSE ANOMALY
            if abs(len(r.text) - baseline_len) > 20:
                findings.append({
                    "type": "RESPONSE_DIFF",
                    "url": url,
                    "severity": "MEDIUM"
                })

        except:
            continue

    return findings
