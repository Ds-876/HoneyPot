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