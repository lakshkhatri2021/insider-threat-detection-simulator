# 🔐 Insider Threat Detection Simulator

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![MIT License](https://img.shields.io/badge/License-MIT-green)
![Log Analysis](https://img.shields.io/badge/SOC-Log_Analysis-orange)

A lightweight, rule-based cybersecurity monitoring system that detects suspicious **internal (insider) behavior** using simulated user activity logs.

This project demonstrates **real-world SOC and SIEM concepts** such as log ingestion, event correlation, rule-based detection, severity classification, and multi-format alert outputs.

---

## 🚨 Why Insider Threats?

Most security breaches don’t come from external hackers — they originate from:

- Employees
- Interns
- Contractors
- Compromised internal accounts

Insider threats are harder to detect because they often look like _normal_ behavior.

This project simulates how organizations **identify abnormal internal activity** using logs and detection rules.

---

## 🧠 How It Works

log_generator.py → activity_logs.csv → detector.py → alerts.log / alerts.csv / summary.json

---

## 🔁 Project Components

### 1️⃣ Log Generator (`log_generator.py`)

- Automatically generates realistic user activity logs
- Random users, actions, timestamps, and resources
- Injects suspicious behavior intentionally
- Outputs logs to:  
  `logs/activity_logs.csv`

This simulates how logs are generated in real systems without using sensitive data.

---

### 2️⃣ Detector Engine (`detector.py`)

Reads logs and applies **three insider threat detection rules**:

#### ✔ Rule 1 — Access Outside Working Hours

Flags users accessing systems outside **09:00–18:00**.

#### ✔ Rule 2 — Excessive Activity

Detects users performing too many actions in a short period (potential data exfiltration).

#### ✔ Rule 3 — Role-Based Access Violation

Detects unauthorized access based on role permissions:

- Intern → payroll ❌
- Employee → confidential data ❌
- Admin → allowed ✔

---

### 3️⃣ Severity Classification

Each alert is classified as:

- 🔴 **HIGH**
- 🟡 **MEDIUM**
- 🟢 **LOW**

Alerts are **color-coded in the terminal** for real-time monitoring.

---

## 📤 Output Files

The system produces **multiple outputs**, similar to real SOC/SIEM tools:

### 📄 `alerts.log` — Human-readable alerts

- Detailed alert blocks
- Used for investigation and auditing

### 📊 `alerts.csv` — Dashboard-ready alerts

- One alert per row
- Can be imported into:
  - Excel
  - Power BI
  - Grafana
  - Tableau

### 📦 `summary.json` — Machine-readable report

- Total alerts
- Severity counts
- Flagged users
- Suitable for automation and dashboards

---

## ⚙️ Configuration (`config.json`)

All thresholds and permissions are configurable **without touching code**:

```json
{
  "work_start": 9,
  "work_end": 18,
  "action_threshold": 3,
  "role_permissions": {
    "intern": ["public_docs"],
    "employee": ["project_docs"],
    "admin": ["*"]
  }
}
```

This mirrors how real security tools store rules and thresholds.

## 🧰 Tech Stack

- **Python** — core detection logic, rule engine, and automation
- **Streamlit** — interactive SOC-style dashboard for alert visualization
- **Pandas** — CSV handling and tabular data processing
- **JSON** — configuration management & machine-readable summaries
- **CSV** — dashboard-friendly output format for alerts
- **Terminal / Shell** — running the detector & dashboard

## Sample Output (Terminal)

==============================
🚨 INSIDER THREAT ALERT 🚨
Type: Role-Based Access Violation
User: emp02
Role: intern
Resource: payroll.zip
Time: 2026-01-10 02:47
Severity: HIGH
==============================

======== SUMMARY ========
Total Alerts: 5
HIGH: 2
MEDIUM: 2
LOW: 1
Users Flagged: emp01, emp02
==========================

## 🛡Why This Project Is Valuable

This project demonstrates:
• Insider threat detection logic
• Log analysis and correlation
• Rule-based security monitoring
• Configurable detection systems
• SOC-style alert pipelines
• Multi-format security outputs

Concepts align with:
• SIEM platforms
• UEBA systems
• SOC workflows
• Enterprise security monitoring

## 🚀 Future Improvements

Planned enhancements include:
• ⏱ Time-windowed activity analysis
• 📊 Web-based dashboard visualization
• 🧠 Machine learning anomaly detection
• 🔗 Ingesting real system logs (Linux auth logs)
• 🌐 Streaming logs instead of batch processing
• 🗂 Timestamped summary files for historical analysis
• 📁 External rule definitions via YAML/JSON

## ▶️ How To Run

1️⃣ Install Python 3 (if not installed)
2️⃣ Run the detector : - python3 detector.py
This will automatically:-
• Generate fresh activity logs
• Detect insider threats
• Print colored alerts
• Save outputs to alerts.log, alerts.csv, and summary.json
• Print a summary report

## 🧼 Cleaning & Regeneration

Before committing updates, old alert files can be removed to regenerate clean logs:

rm alerts.log alerts.csv summary.json logs/activity_logs.csv
python3 detector.py

## 📊 Interactive Dashboard (Optional)

The project also includes a lightweight Streamlit-based dashboard for visualizing detected alerts.

The dashboard reads from `alerts.csv` and provides:

- Severity-based alert visualization
- Summary metrics (total alerts, high/medium severity)
- A SOC-style tabular view of incidents

### Run the dashboard: python3 -m streamlit run dashboard.py

This dashboard is an optional visualization layer and does not affect the core detection logic.

## 📄 License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute this project with attribution.
