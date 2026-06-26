🚀 5G Slice Validator
Intelligent 5G Standalone Network Troubleshooting & Root Cause Intelligence Platform

A simulation-grade diagnostic engine that transforms raw 5G logs and configuration data into structured root cause intelligence, enabling rapid troubleshooting of network slicing failures in 5G SA environments.

Built for network engineers, SOC-style analysis workflows, and telecom troubleshooting pipelines.

🧠 Executive Summary

5G Slice Validator is a telecom intelligence system that emulates real-world 5G SA troubleshooting environments.

It automatically:

Ingests UE / gNB / AMF / Subscriber configurations
Parses Open5GS / UERANSIM logs
Detects slicing misconfigurations (DNN, TAC, S-NSSAI)
Classifies failure scenarios
Produces explainable root cause analysis with structured reports

The system is designed as a diagnostic command pipeline, not just a script.

⚡ Why This Project Is Different

Unlike traditional log parsers, this system provides:

🧩 Hybrid Intelligence Engine

Combines:

Deterministic rule-based validation
Log-driven behavioral analysis
Cause-code correlation engine
🧠 Root Cause Explanation Layer

Instead of just saying "FAIL", it explains:

Why it failed
Where mismatch occurred
Which 5G component caused it
📊 Scenario-Based Simulation System

Reproducible failure environments:

wrong_dnn
wrong_tac
wrong_slice
smf_down
success baseline
🔍 Telecom-Aware Diagnostics

Focuses on real 5G issues:

PDU session failures
Registration rejection flows
Slice allocation mismatches
🏗️ System Architecture
Configs + Logs
      ↓
Log Parser Engine (regex + pattern matching)
      ↓
Validation Layer (5G rules engine)
      ↓
Diagnosis Engine (root cause correlation)
      ↓
Report Generator (JSON + Markdown)
      ↓
Dashboard (Streamlit visualization)
🧪 Fault Intelligence Model
Code	Meaning	Impact
DNN mismatch	Wrong data network	PDU failure
TAC mismatch	Tracking area error	Registration failure
Slice mismatch	S-NSSAI unsupported	Session rejection
SMF down	Core service failure	Session blocked
🧠 Core Intelligence Modules
📡 Parser Engine
Extracts NAS / SM cause codes
Normalizes Open5GS / UERANSIM logs
🧾 Validation Core
UE / gNB / AMF consistency checks
Subscriber validation logic
🧠 Diagnosis Engine
Correlates multi-layer evidence
Produces root cause + recommendation
📊 Reporting System
JSON machine output
Markdown human report
Dashboard visualization
📂 System Layout
5g-slice-validator/
│
├── main.py              → Execution engine
├── scenarios.py         → Scenario orchestration
├── configs/             → Network definitions
├── logs/                → Simulation logs
├── parser/              → Log intelligence layer
├── validator/           → Rule engine + diagnosis
├── reports/             → Output intelligence reports
├── dashboard/           → Visualization layer
├── tests/               → Verification suite
└── tools/              → Scenario automation
🚀 Execution Flow
Select scenario
Load network configuration
Parse simulated 5G logs
Run validation engine
Detect failure pattern
Generate root cause explanation
Export structured report
📊 Dashboard Interface

Streamlit-based operational dashboard provides:

Real-time scenario execution
Validation status tracking
Root cause visualization
Historical reports view
🧪 Supported Scenarios
Scenario	Description	Outcome
success	Valid configuration	PASS
wrong_dnn	Invalid DNN	FAIL
wrong_tac	TAC mismatch	FAIL
wrong_slice	Slice mismatch	FAIL
smf_down	Core service failure	FAIL
⚙️ Tech Stack
Python 3.10+
Regex-based log parsing
YAML configuration system
Streamlit dashboard
Pytest validation framework
🧠 Design Philosophy

This project is built around three principles:

Explainability over complexity
Reproducibility over randomness
Engineering realism over abstraction

The goal is not just detection — but understanding failure in 5G systems.

🚀 Future Evolution
Live Open5GS integration
AI-assisted root cause prediction
Real-time log streaming
Kubernetes deployment mode
Advanced visualization dashboards
PDF report automation engine
👨‍💻 Author

Mahmoud Bahnsey
Cybersecurity & Networking Engineer (Student)
