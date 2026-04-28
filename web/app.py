from flask import Flask, render_template, jsonify
import json
import os
import subprocess

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
REPORT_FILE = os.path.join(BASE_DIR, "reports", "report.json")


@app.route("/")
def dashboard():
    return render_template("index.html")


@app.route("/api/report")
def report():
    if not os.path.exists(REPORT_FILE):
        return jsonify({"vulnerabilities": []})

    with open(REPORT_FILE, "r") as f:
        return jsonify(json.load(f))


@app.route("/api/stats")
def stats():
    if not os.path.exists(REPORT_FILE):
        return jsonify({"severity": {}, "types": {}})

    with open(REPORT_FILE, "r") as f:
        data = json.load(f)

    vulns = data.get("vulnerabilities", [])

    severity = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    types = {}

    for v in vulns:
        sev = v.get("severity", "LOW")
        vtype = v.get("type", "UNKNOWN")

        severity[sev] = severity.get(sev, 0) + 1
        types[vtype] = types.get(vtype, 0) + 1

    return jsonify({
        "severity": severity,
        "types": types
    })


# 🚀 START SCAN BUTTON
@app.route("/api/scan", methods=["POST"])
def scan():
    try:
        subprocess.run(
            ["python", "main.py"],
            cwd=BASE_DIR,
            check=True
        )
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


# ⚡ LIVE DATA
@app.route("/api/live")
def live():
    if not os.path.exists(REPORT_FILE):
        return jsonify({"last": None, "count": 0})

    with open(REPORT_FILE, "r") as f:
        data = json.load(f)

    vulns = data.get("vulnerabilities", [])

    return jsonify({
        "last": vulns[-1] if vulns else None,
        "count": len(vulns)
    })


if __name__ == "__main__":
    app.run(debug=True, port=8000)
