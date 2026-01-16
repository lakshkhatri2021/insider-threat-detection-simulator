import csv
from datetime import datetime

import log_generator
log_generator.write_logs()

import json

# ---- Load configuration ----
with open("config.json", "r") as f:
    config = json.load(f)

WORK_START = config["work_start"]
WORK_END = config["work_end"]
ACTION_THRESHOLD = config["action_threshold"]
ROLE_PERMISSIONS = config["role_permissions"]

# Terminal colors
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"

# Input & output files
log_file = "logs/activity_logs.csv"
alert_file = "alerts.log"

# ---- Summary Counters ----
total_alerts = 0
severity_count = {
    "HIGH": 0,
    "MEDIUM": 0,
    "LOW": 0
}

flagged_users = set()

# ---- Pretty Alert Formatter ----
def log_alert(alert_type, details, severity):
    global total_alerts
    total_alerts += 1
    severity_count[severity] += 1
    flagged_users.add(details.get("User", "Unknown"))

    # Pick color based on severity
    if severity == "HIGH":
        color = RED
    elif severity == "MEDIUM":
        color = YELLOW
    else:
        color = GREEN

    block = []
    block.append("=" * 30)
    block.append(f"{color}🚨 INSIDER THREAT ALERT 🚨{RESET}")
    block.append(f"{color}Type: {alert_type}{RESET}")
    for key, value in details.items():
        block.append(f"{color}{key}: {value}{RESET}")
    block.append(f"{color}Severity: {severity}{RESET}")
    block.append("=" * 30)

    alert_text = "\n".join(block)

    # Write pretty alert to alerts.log
    with open(alert_file, "a") as f:
        clean_details = "\n".join(
            [line.replace(color, "").replace(RESET, "") for line in block]
        )
        f.write(clean_details + "\n\n")

    # ---- Write structured alert to CSV ----
    with open("alerts.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            alert_type,
            severity,
            details.get("User", ""),
            details.get("Resource", ""),
            details.get("Time", "")
        ])

    # Print colored output to terminal
    print(alert_text + "\n")

# Track user activity count
user_activity_count = {}

# Reset alert log each run
with open(alert_file, "w") as f:
    f.write("==== INSIDER THREAT ALERT LOG ====\n\n")

# Reset CSV alert output
with open("alerts.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["alert_type", "severity", "user", "resource", "time"])

# ---- Read and Process Logs ----
with open(log_file, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        user = row["user"]
        role = row["role"]
        resource = row["resource"]
        timestamp_str = row["timestamp"]

        # Count activity
        if user not in user_activity_count:
            user_activity_count[user] = 0
        user_activity_count[user] += 1

        # ---- Rule 1: Access Outside Working Hours ----
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M")
        hour = timestamp.hour

        if hour < WORK_START or hour >= WORK_END:
            details = {
                "User": user,
                "Time": timestamp_str
            }
            log_alert("Access Outside Working Hours", details, "MEDIUM")

        # ---- Rule 3: Role-Based Access Violation ----
        allowed_resources = ROLE_PERMISSIONS.get(role, [])

        if "*" not in allowed_resources and resource not in allowed_resources:
            details = {
                "User": user,
                "Role": role,
                "Resource": resource,
                "Time": timestamp_str
            }
            log_alert("Role-Based Access Violation", details, "HIGH")

# ---- Rule 2: Excessive Activity ----
for user, count in user_activity_count.items():
    if count > ACTION_THRESHOLD:
        details = {
            "User": user,
            "Actions": count
        }
        log_alert("Excessive User Activity", details, "LOW")


# ---- SUMMARY OUTPUT ----
summary_block = []
summary_block.append("\n======== SUMMARY ========")
summary_block.append(f"Total Alerts: {total_alerts}")
summary_block.append(f"HIGH: {severity_count['HIGH']}")
summary_block.append(f"MEDIUM: {severity_count['MEDIUM']}")
summary_block.append(f"LOW: {severity_count['LOW']}")
summary_block.append("Users Flagged: " + ", ".join(flagged_users))
summary_block.append("==========================\n")

summary_text = "\n".join(summary_block)

print(summary_text)

# Save summary to file
with open(alert_file, "a") as f:
    f.write(summary_text)

# ---- Save summary to JSON ----
summary_json = {
    "total_alerts": total_alerts,
    "high": severity_count["HIGH"],
    "medium": severity_count["MEDIUM"],
    "low": severity_count["LOW"],
    "flagged_users": list(flagged_users)
}

with open("summary.json", "w") as f:
    json.dump(summary_json, f, indent=4)