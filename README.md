# 🚀 5G Slice Validator

**Automated 5G Standalone (SA) Slice Validation & Root Cause Analysis Platform**

A Python-based framework for validating 5G network slicing configurations, analyzing Open5GS / UERANSIM logs, detecting misconfigurations (DNN, TAC, S-NSSAI), and generating explainable root cause reports with a Streamlit dashboard.

---

## 📌 Project Highlights

- ✔ 5G SA configuration validation (UE, gNB, AMF, Subscriber)
- ✔ Real log parsing for Open5GS / UERANSIM
- ✔ Detection of:
  - Wrong DNN
  - TAC mismatch
  - Slice (S-NSSAI) mismatch
  - SMF failure scenarios
- ✔ Rule-based Root Cause Analysis engine
- ✔ JSON + Markdown report generation
- ✔ Interactive Streamlit dashboard
- ✔ Fully reproducible test scenarios

---

## 🧠 Problem Statement

In 5G Standalone networks, failures in registration or PDU sessions are often caused by subtle configuration mismatches across network functions.

Manual debugging requires:
- Comparing multiple YAML configs
- Reading large log files
- Interpreting NAS/SM cause codes

This process is slow, error-prone, and not scalable.

---

## 🎯 Solution

This tool automates the entire troubleshooting pipeline:

It transforms raw data into:

- ✔ Structured validation results  
- ✔ Human-readable root cause explanation  
- ✔ Actionable troubleshooting recommendations  

---

## 🏗️ System Architecture

| Layer | Component | Responsibility |
|------|----------|----------------|
| Configuration | YAML files | Define UE / gNB / AMF / Subscriber setup |
| Parsing | parser/ | Extract log events & cause codes |
| Validation | validator/ | Check registration, PDU session, consistency |
| Diagnosis | engine | Identify root cause |
| Reporting | reports/ | Generate JSON / Markdown outputs |
| UI | dashboard/ | Streamlit visualization |

---

## ⚙️ How It Works

1. Select scenario (`success`, `wrong_dnn`, `wrong_tac`, `wrong_slice`, `smf_down`)
2. Load configs + logs
3. Parse log events
4. Run validation rules
5. Detect failure reason
6. Generate report + dashboard output

---

## 📂 Project Structure
5g-slice-validator/
├── main.py
├── scenarios.py
├── configs/
├── logs/
├── parser/
├── validator/
├── reports/
├── dashboard/
├── tools/
└── tests/


---

## ▶️ Installation

bash
git clone https://github.com/mahmoudbahnsey/5G-Slice-Validator.git
cd 5G-Slice-Validator
pip install -r requirements.txt


🚀 Usage
python main.py
python main.py --scenario wrong_dnn
python main.py --scenario wrong_tac
python main.py --scenario wrong_slice
python main.py --scenario smf_down


📊 Dashboard
streamlit run dashboard/app.py

Then open:

http://localhost:8501


🧪 Testing
python -m pytest tests -q

Expected:

9 passed

 🧪 Supported Scenarios
Scenario	Description       	Result
success	Valid configuration	PASS
wrong_dnn	Invalid DNN       	FAIL
wrong_tac	TAC mismatch	      FAIL
wrong_slice	Slice mismatch	      FAIL
smf_down	SMF down	            FAIL

⚠️ Limitations
Offline / simulated logs
Rule-based (no AI model)
Requires predefined scenarios
Basic dashboard UI

🚀 Future Improvements
Real-time Open5GS integration
AI-based root cause prediction
Advanced dashboard analytics
PDF report export
Kubernetes deployment support

👨‍💻 Author
Mahmoud Bahnsey
Cybersecurity & Networking Student

ن
