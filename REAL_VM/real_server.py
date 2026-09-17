from flask import Flask, request, render_template
from itsdangerous import TimestampSigner, BadSignature, SignatureExpired
from shared_key import SECRET_KEY

app = Flask(__name__)
signer = TimestampSigner(SECRET_KEY)

VALID_USERS = {"alice": "Password123", "john": "SecurePass99"}

@app.route("/", methods=["GET"])
def index():
    token = request.cookies.get("honeypot_session")
    if token:
        try:
            username = signer.unsign(token, max_age=120).decode()
            return render_template("dashboard.html", user=username)
        except SignatureExpired:
            pass
        except BadSignature:
            pass
    return render_template("login.html")

@app.route("/", methods=["POST"])
def real_login():
    user = request.form.get("username")
    pwd = request.form.get("password")
    if user in VALID_USERS and VALID_USERS[user] == pwd:
        return render_template("dashboard.html", user=user)
    return render_template("login.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)