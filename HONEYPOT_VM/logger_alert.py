import os
from datetime import datetime

LOG_DIR = "logs/alerts"

def log_alert(message):
    os.makedirs(LOG_DIR, exist_ok=True)
    logfile = os.path.join(LOG_DIR, f"{datetime.now().date()}_alerts.log")
    with open(logfile, "a") as f:
        f.write(f"{datetime.now()} | ALERT: {message}\n")