# 5G Slice Validator

**Aggregate status:** `FAIL`

## Executive summary

- **Summary:** PDU session rejection consistent with DNN mismatch
- **Root cause:** Requested DNN is not configured or not allowed for this subscriber
- **Confidence:** high

### Recommendations

- Update subscriber APN/DNN in UDM/PCF or change UE requested DNN to match subscription.

## Module 1 — Core health

- Mode: `mock`
- **AMF:** UP
- **SMF:** UP
- **UPF:** UP
- **NRF:** UP
- **UDM:** UP
- **AUSF:** UP

## Module 2 — Registration

- Status: **PASS**
  - initial_registration_request: yes
  - authentication_request: no
  - security_mode_complete: no
  - registration_accept: yes

## Module 3 — PDU session

- Status: **FAIL**
- IP assigned: False
- Session active: False
- Reason: Missing or unknown DNN

## Module 4 — Configuration consistency

- Overall: **FAIL**
- `dnn_consistency` → FAILED (expected `internet`, actual `wrong-apn`)
- `ue_gnb_tac` → PASSED (expected `1`, actual `1`)
- `gnb_amf_tac` → PASSED (expected `one of [1]`, actual `1`)
- `slice_ue_subscriber` → PASSED (expected `sst=1, sd=010203`, actual `sst=1, sd=010203`)
- `slice_ue_amf` → PASSED (expected `AMF offers [(1, '010203')]`, actual `sst=1, sd=010203`)
- `plmn_consistency` → PASSED (expected `00101`, actual `00101`)

## Module 5 — Parsed causes

- MM causes: []
- SM causes: [27]
- IP addresses: []

## Inputs

- Config dir: `F:\courses1\RoutingAndSwitching\project\5g-slice-validator\configs\scenarios\wrong_dnn`
- Logs: ['F:\\courses1\\RoutingAndSwitching\\project\\5g-slice-validator\\logs\\scenario_wrong_dnn.log']
