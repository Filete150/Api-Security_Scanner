from flask import Flask, request, jsonify

app = Flask(__name__)

# "Base de datos" simulada
users = {
    1: {"id": 1, "name": "Alex", "role": "admin"},
    2: {"id": 2, "name": "Maria", "role": "user"},
    3: {"id": 3, "name": "John", "role": "user"}
}

products = [
    {"id": 1, "name": "Laptop"},
    {"id": 2, "name": "Phone"},
    {"id": 3, "name": "Tablet"}
]

# ❌ LOGIN INSEGURO (token fijo)
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if data.get("user") and data.get("password"):
        return jsonify({"token": "123456"})  # siempre igual
    return jsonify({"error": "invalid"}), 401


# ❌ IDOR VULNERABILITY
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    # NO hay control de permisos
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "not found"}), 404


# ❌ SIN AUTH
@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)


# ❌ RATE LIMITING INEXISTENTE
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong"})


# 👀 ENDPOINT ADMIN OCULTO
@app.route("/admin/secret", methods=["GET"])
def admin():
    return jsonify({"flag": "CTF-SECRET-1234"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
