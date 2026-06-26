🚀 5G Slice Validator

Automated 5G Standalone (SA) Slice Validation & Root Cause Analysis Tool

A Python-based framework that validates 5G network slicing configurations, analyzes Open5GS / UERANSIM logs, detects misconfigurations (DNN, TAC, S-NSSAI), and provides explainable root cause diagnosis with structured reports and a Streamlit dashboard.

📌 Project Highlights
✔ 5G SA configuration validation (UE, gNB, AMF, Subscriber)
✔ Log parsing for Open5GS / UERANSIM scenarios
✔ Detection of:
Wrong DNN
TAC mismatch
Slice (S-NSSAI) mismatch
SMF failure scenarios
✔ Rule-based Root Cause Analysis engine
✔ JSON + Markdown report generation
✔ Interactive Streamlit dashboard
✔ Fully reproducible test scenarios
🧠 Problem Statement

In 5G Standalone environments, failures in registration or PDU session establishment are often caused by subtle configuration mismatches across network functions.

Manually debugging these issues requires:

Comparing multiple YAML configuration files
Analyzing large log files
Interpreting NAS / SM cause codes

This process is slow and error-prone.

🎯 Solution

This tool automates the entire troubleshooting pipeline:

Configs + Logs → Parser → Validators → Diagnosis Engine → Reports + Dashboard

It converts raw logs and configurations into:

✔ Structured validation results
✔ Human-readable root cause explanation
✔ Actionable troubleshooting recommendations
🏗️ System Architecture
Layer	Component	Responsibility
Configuration Layer	YAML files	Define UE / gNB / AMF / Subscriber setup
Parsing Layer	parser/	Extract events & cause codes from logs
Validation Layer	validator/	Check registration, PDU session, consistency
Diagnosis Layer	diagnosis engine	Identify root cause
Reporting Layer	reports/	Generate JSON & Markdown outputs
UI Layer	dashboard/	Visualize results in Streamlit
⚙️ How It Works
Select scenario (success, wrong_dnn, wrong_tac, wrong_slice, smf_down)
Load corresponding configs + logs
Parse log events and NAS/SM messages
Run validation rules
Correlate evidence
Generate root cause + recommendations
Export reports + dashboard view
📂 Project Structure
5g-slice-validator/
│
├── main.py                  # CLI entry point
├── scenarios.py            # Scenario mappings
├── configs/                # Network configuration (YAML)
├── logs/                   # Sample 5G logs
├── parser/                 # Log parsing engine
├── validator/              # Validation + diagnosis logic
├── reports/                # Output reports (JSON/MD)
├── dashboard/              # Streamlit UI
├── tests/                  # Unit & integration tests
├── tools/                  # Scenario automation scripts
└── documentation/          # Full project documentation (PDF)
▶️ Installation
# Clone repository
git clone https://github.com/mahmoudbahnsey/5G-Slice-Validator.git

cd 5G-Slice-Validator

# Install dependencies
pip install -r requirements.txt
🚀 Usage
Run default scenario
python main.py
Run specific scenarios
python main.py --scenario success
python main.py --scenario wrong_dnn
python main.py --scenario wrong_tac
python main.py --scenario wrong_slice
python main.py --scenario smf_down
📊 Dashboard

Launch interactive UI:

streamlit run dashboard/app.py

Then open:

http://localhost:8501
🧪 Testing

Run automated tests:

python -m pytest tests -q

Expected output:

9 passed
📦 Outputs

The tool generates:

reports/last_run.json → Machine-readable results
reports/last_run.md → Human-readable report
Streamlit dashboard visualization
🧪 Supported Scenarios
Scenario	Description	Result
success	Valid 5G configuration	PASS
wrong_dnn	Invalid DNN configuration	FAIL
wrong_tac	TAC mismatch	FAIL
wrong_slice	Slice mismatch (S-NSSAI)	FAIL
smf_down	SMF service unavailable	FAIL
⚠️ Limitations
Works on simulated / offline logs
Rule-based (not AI/ML trained model)
Requires predefined scenario structure
Dashboard is basic (future improvement needed)
🚀 Future Improvements
Live Open5GS integration (real-time logs)
AI-based root cause prediction
Advanced dashboard analytics
Multi-operator support
Export PDF automated reports
Kubernetes-based deployment support
👨‍💻 Author

Mahmoud Bahnsey
Cybersecurity & Networking Student

📜 License

This project is for academic and educational use.

⭐ If you like it

Give the repo a ⭐ on GitHub to support development.
