from flask import Flask, request, redirect, make_response, render_template
from itsdangerous import TimestampSigner
from shared_key import SECRET_KEY
from logger_master import log_master
from detection_engine import DetectionEngine

app = Flask(__name__)
signer = TimestampSigner(SECRET_KEY)
engine = DetectionEngine()

LEGIT_USERS = {"alice": "Password123", "john": "SecurePass99"}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    ip = request.remote_addr
    user = request.form.get("username")
    pwd = request.form.get("password")
    ua = request.headers.get("User-Agent")
    log_master(ip, user, pwd, ua)
    engine.analyze(ip, user, pwd)
    if user in LEGIT_USERS and LEGIT_USERS[user] == pwd:
        token = signer.sign(user.encode()).decode()
        response = make_response(redirect("http://real.local/"))
        response.set_cookie("honeypot_session", token, httponly=True, secure=False, samesite="Lax")
        return response
    return render_template("login.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)