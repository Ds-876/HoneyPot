import os
import secrets

# Folder structure
folders = [
    "HONEYPOT_VM",
    "HONEYPOT_VM/templates",
    "REAL_VM",
    "REAL_VM/templates"
]

# Templates content
templates = {
    "HONEYPOT_VM/templates/login.html": """<!DOCTYPE html>
<html>
<head>
<title>Bank Login</title>
<style>
body { font-family:Arial; background:#f2f2f2; }
.login-box { width:300px; margin:100px auto; background:white; padding:20px; border-radius:6px; }
input, button { width:100%; padding:10px; margin-top:10px; }
</style>
</head>
<body>
<div class="login-box">
<h2>Bank of Example - Login</h2>
<form method="POST">
<input type="text" name="username" placeholder="User ID" required>
<input type="password" name="password" placeholder="Password" required>
<button>Login</button>
</form>
</div>
</body>
</html>""",

    "REAL_VM/templates/login.html": """<!DOCTYPE html>
<html>
<head><title>Real Login</title></head>
<body>
<h2>Real Login Page</h2>
<form method="POST">
<input name="username" placeholder="User ID"><br><br>
<input name="password" type="password" placeholder="Password"><br><br>
<button>Login</button>
</form>
</body>
</html>""",

    "REAL_VM/templates/dashboard.html": """<!DOCTYPE html>
<html>
<head><title>Dashboard</title></head>
<body style="font-family:Arial;text-align:center;margin-top:40px;">
<h1>Welcome {{ user }}!</h1>
<p>You are now logged into the REAL banking dashboard.</p>
</body>
</html>"""
}

# Honeypot VM files
honeypot_files = {
    "HONEYPOT_VM/shared_key.py": f'SECRET_KEY = "{secrets.token_hex(32)}"\n',
    "HONEYPOT_VM/logger_master.py": """
import os
from datetime import datetime

LOG_DIR = "logs/master"

def log_master(ip, user, password, user_agent):
    os.makedirs(LOG_DIR, exist_ok=True)
    logfile = os.path.join(LOG_DIR, f"{datetime.now().date()}_master.log")
    with open(logfile, "a") as f:
        f.write(f"{datetime.now()} | IP: {ip} | USER: {user} | PASS: {password} | UA: {user_agent}\\n")
""",
    "HONEYPOT_VM/logger_alert.py": """
import os
from datetime import datetime

LOG_DIR = "logs/alerts"

def log_alert(message):
    os.makedirs(LOG_DIR, exist_ok=True)
    logfile = os.path.join(LOG_DIR, f"{datetime.now().date()}_alerts.log")
    with open(logfile, "a") as f:
        f.write(f"{datetime.now()} | ALERT: {message}\\n")
""",
    "HONEYPOT_VM/emailer.py": """
import smtplib
from email.mime.text import MIMEText
from config import SECURITY_TEAM_EMAIL, SMTP_SERVER, SMTP_USER, SMTP_PASS

def send_alert_email(message):
    msg = MIMEText(message)
    msg["Subject"] = "HONEYPOT SECURITY ALERT"
    msg["From"] = SMTP_USER
    msg["To"] = SECURITY_TEAM_EMAIL
    with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
""",
    "HONEYPOT_VM/config.py": """
SECURITY_TEAM_EMAIL = "security@example.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_USER = "your_email@gmail.com"
SMTP_PASS = "your_app_password"
""",
    "HONEYPOT_VM/detection_engine.py": """
from logger_alert import log_alert
from emailer import send_alert_email

class DetectionEngine:
    def __init__(self):
        self.failed_attempts = {}  # IP -> count

    def analyze(self, ip, username, password):
        alerts = []

        # Rule 1: brute force
        self.failed_attempts[ip] = self.failed_attempts.get(ip, 0) + 1
        if self.failed_attempts[ip] > 5:
            alerts.append(f"Bruteforce detected from {ip}")

        # Rule 2: suspicious usernames
        suspicious_keywords = ["admin", "root", "test", "bankadmin"]
        if username.lower() in suspicious_keywords:
            alerts.append(f"Suspicious username used: {username} from {ip}")

        # Rule 3: weak password
        if len(password) < 3:
            alerts.append(f"Weak password attempt from {ip}")

        for alert in alerts:
            log_alert(alert)
            send_alert_email(alert)

        return len(alerts) > 0
""",
    "HONEYPOT_VM/honeypot_main.py": """
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
"""
}

# Real VM files
real_files = {
    "REAL_VM/shared_key.py": honeypot_files["HONEYPOT_VM/shared_key.py"],
    "REAL_VM/real_server.py": """
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
"""
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Write template files
for path, content in templates.items():
    with open(path, "w") as f:
        f.write(content.strip())

# Write Honeypot files
for path, content in honeypot_files.items():
    with open(path, "w") as f:
        f.write(content.strip())

# Write Real VM files
for path, content in real_files.items():
    with open(path, "w") as f:
        f.write(content.strip())

print("All Honeypot and Real VM files with templates created successfully!")
