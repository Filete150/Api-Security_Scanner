import json
import yaml

def load_spec(file_path):
    with open(file_path, 'r') as f:
        if file_path.endswith('.json'):
            return json.load(f)
        else:
            return yaml.safe_load(f)

def extract_endpoints(spec):
    endpoints = []

    paths = spec.get("paths", {})

    for path, methods in paths.items():
        for method in methods:
            endpoints.append({
                "path": path,
                "method": method.upper()
            })

    return endpoints
