import requests

def test_idor(base_url, endpoint):
    findings = []

    if "{id}" not in endpoint["path"]:
        return findings

    for i in range(1, 6):
        url = base_url + endpoint["path"].replace("{id}", str(i))
        r = requests.get(url)

        if r.status_code == 200:
            findings.append({
                "type": "IDOR",
                "url": url,
                "severity": "HIGH"
            })

    return findings
