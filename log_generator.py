import csv
import random
from datetime import datetime, timedelta

# Output file
output_file = "logs/activity_logs.csv"

# Users and roles
USERS = {
    "emp01": "employee",
    "emp02": "intern",
    "emp03": "admin",
}

# Possible actions
ACTIONS = ["login", "read", "download"]

# Resources by role
RESOURCES = {
    "intern": ["public_docs"],
    "employee": ["project_docs"],
    "admin": ["public_docs", "project_docs", "confidential_reports", "payroll.zip"],
}

# Generate random timestamps
def random_timestamp():
    start = datetime(2026, 1, 10, 0, 0)
    end = datetime(2026, 1, 10, 23, 59)
    delta = end - start
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_seconds)

# Generate logs
def generate_logs(count=50):
    rows = []
    for _ in range(count):
        user = random.choice(list(USERS.keys()))
        role = USERS[user]
        action = random.choice(ACTIONS)
        resource = random.choice(RESOURCES[role])
        timestamp = random_timestamp().strftime("%Y-%m-%d %H:%M")

        rows.append([timestamp, user, role, action, resource])

    # Inject suspicious behavior
    rows.append(["2026-01-10 02:47", "emp02", "intern", "download", "payroll.zip"])
    rows.append(["2026-01-10 03:10", "emp01", "employee", "download", "confidential_reports"])
    rows.append(["2026-01-10 04:20", "emp02", "intern", "read", "confidential_reports"])

    return rows

# Write to CSV
def write_logs():
    rows = generate_logs()

    with open(output_file, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "user", "role", "action", "resource"])
        writer.writerows(rows)

    print("Generated activity logs!")

if __name__ == "__main__":
    write_logs()