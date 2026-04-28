import requests

def test_endpoint(base_url, endpoint):
    url = base_url + endpoint["path"]

    try:
        r = requests.request(endpoint["method"], url)

        return {
            "url": url,
            "method": endpoint["method"],
            "status": r.status_code
        }

    except Exception as e:
        return {"url": url, "error": str(e)}
