import requests

def test_rate_limit(base_url, endpoint):
    findings = []

    url = base_url + endpoint["path"]

    success = 0

    for _ in range(20):
        r = requests.get(url)
        if r.status_code == 200:
            success += 1

    if success == 20:
        findings.append({
            "type": "NO_RATE_LIMIT",
            "url": url,
            "severity": "MEDIUM"
        })

    return findings
