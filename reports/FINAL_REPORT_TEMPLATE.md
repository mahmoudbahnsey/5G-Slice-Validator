# Final Report — 5G Slice Validator

*Fill in each section for your course submission. This template matches the requested structure.*

## Abstract

Summarize the problem (complex 5G SA troubleshooting), the solution (automated validation, log parsing, diagnosis, dashboard), and key results (which scenarios pass/fail and what was validated).

## Introduction

Describe the motivation: engineers face opaque NAS/SM causes, slice/DNN/TAC mismatches, and distributed logs across Core and RAN. State the project goal: a Python toolkit that validates configuration consistency, registration and PDU session workflows, maps causes to human explanations, and recommends fixes.

## Literature Review

### 5G SA basics

Briefly describe registration (5GMM), PDU session establishment (5GSM), AMF/SMF/UPF roles, NSSAI/S-NSSAI, DNN/APN, and GUTI/TAI concepts relevant to your tests.

### Network slicing

Explain S-NSSAI (SST/SD), slice consistency across UE, AMF, SMF, and subscriber profile, and typical failure modes.

## Methodology

Explain your approach:

1. **Simulation / lab:** UERANSIM UE/gNB with Open5GS (when deployed).
2. **Artifacts:** YAML configs, AMF/SMF logs, UE logs.
3. **Processing:** regex parsing, structured checks, rule-based root-cause analysis.
4. **Presentation:** Streamlit dashboard and generated Markdown/JSON reports.

## System Design

Describe the four layers:

- **Layer 1:** UERANSIM UE/gNB (simulation).
- **Layer 2:** Open5GS NFs (AMF, SMF, UPF, NRF, UDM, AUSF).
- **Layer 3:** Python validation engine (this repository).
- **Layer 4:** Streamlit visualization.

Include a simple diagram (block diagram) of data flow: logs/configs → parser → validators → diagnosis → dashboard/reports.

## Implementation

Document modules:

| Module | Responsibility |
|--------|----------------|
| Core Health | Service availability (systemd or mock probe) |
| Registration | NAS registration flow from logs |
| PDU Session | Session outcome, IP, SM causes |
| Config Consistency | DNN, TAC, S-NSSAI across UE/gNB/AMF/subscriber |
| Log Parser | Open5GS/UERANSIM patterns and cause extraction |
| Root Cause Analyzer | Correlate symptoms with configuration |
| Dashboard | Streamlit UI |
| Report Generator | Markdown + JSON |

Reference the actual paths: `validator/`, `parser/`, `dashboard/app.py`, `main.py`.

## Test Scenarios

| Scenario | Expected | What is validated |
|----------|----------|-------------------|
| Successful registration | PASS | Happy path logs + aligned YAML |
| Wrong DNN | FAIL | SM cause 27 / subscriber mismatch |
| Wrong TAC | FAIL | Registration / TAI mismatch |
| Wrong slice | FAIL | Slice inconsistency + PDU reject |
| SMF down | FAIL | Core health detects SMF DOWN |

## Results

Paste aggregate statuses, example diagnosis output, and screenshots of the Streamlit dashboard. Discuss false positives/negatives and parser limitations.

## Challenges

Examples: log format variance across Open5GS versions; distinguishing root cause vs. symptom; lack of live ICMP from the tool unless integrated; Windows vs. Linux service probing.

## Conclusion

Summarize how the toolkit reduces time-to-diagnosis for junior engineers and propose future work (live PCAP, NRF discovery checks, automated UERANSIM runs in CI).
