import requests

# Payloads básicos de seguridad
PAYLOADS = [
    "1",
    "999999",
    "'",
    "\"",
    "' OR '1'='1",
    "../../etc/passwd",
    "<script>alert(1)</script>",
    "%00",
    "${{7*7}}"
]


def fuzz_endpoint(base_url, endpoint):
    path = endpoint["path"]
    method = endpoint["method"]

    if "{id}" not in path:
        return

    print(f"\n[FUZZING] {path}")

    for payload in PAYLOADS:
        url = base_url + path.replace("{id}", str(payload))

        try:
            r = requests.request(method, url)

            # DETECCIÓN DE ANOMALÍAS
            if r.status_code >= 500:
                print(f"[!] SERVER ERROR con payload: {payload}")

            if "sql" in r.text.lower():
                print(f"[!] POSIBLE SQLi: {payload}")

            if len(r.text) < 10:
                print(f"[!] RESPUESTA VACÍA: {payload}")

        except Exception as e:
            print(f"[ERROR] {payload} -> {e}")
