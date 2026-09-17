import os
from datetime import datetime

LOG_DIR = "logs/master"

def log_master(ip, user, password, user_agent):
    os.makedirs(LOG_DIR, exist_ok=True)
    logfile = os.path.join(LOG_DIR, f"{datetime.now().date()}_master.log")
    with open(logfile, "a") as f:
        f.write(f"{datetime.now()} | IP: {ip} | USER: {user} | PASS: {password} | UA: {user_agent}\n")