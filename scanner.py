import requests
import time

HEADERS = {
    "Content-Type": "application/json"
}


# ----------------------------
# REQUEST INTELLIGENT ENGINE
# ----------------------------
def test_endpoint(base_url, endpoint):
    url = base_url + endpoint["path"]
    method = endpoint["method"]

    try:
        # POST LOGIN FIX
        if method == "POST" and "/login" in url:
            payload = {"user": "test", "password": "test"}
            r = requests.post(url, json=payload, headers=HEADERS)

        # DEFAULT REQUEST
        else:
            r = requests.request(method, url, headers=HEADERS)

        return {
            "url": url,
            "method": method,
            "status": r.status_code,
            "length": len(r.text)
        }

    except Exception as e:
        return {"url": url, "error": str(e)}


# ----------------------------
# IDOR DETECTOR (MEJORADO)
# ----------------------------
def test_idor(base_url, endpoint):
    path = endpoint["path"]

    if "{id}" not in path:
        return

    print("[IDOR] testing...")

    baseline = None

    for i in range(1, 6):
        url = base_url + path.replace("{id}", str(i))

        r = requests.get(url)

        # guardar baseline
        if baseline is None:
            baseline = len(r.text)

        # si responde diferente → posible IDOR
        if r.status_code == 200:
            print(f"[!] IDOR posible: {url}")

        # diferencia de contenido
        if abs(len(r.text) - baseline) > 10:
            print(f"[!] RESPUESTA DIFERENTE (IDOR fuerte): {url}")


# ----------------------------
# RATE LIMIT TEST
# ----------------------------
def test_rate_limit(url):
    print("[RATE LIMIT] testing...")

    success = 0
    start = time.time()

    for _ in range(30):
        r = requests.get(url)
        if r.status_code == 200:
            success += 1

    duration = time.time() - start

    if success == 30:
        print("[!] NO rate limit detectado (alto riesgo)")
    else:
        print("[+] rate limit activo")

    print(f"[i] {success}/30 requests OK en {round(duration,2)}s")


# ----------------------------
# AUTH CHECK BÁSICO
# ----------------------------
def test_auth_required(url):
    r = requests.get(url)

    if r.status_code == 200:
        print(f"[!] Endpoint sin auth: {url}")
