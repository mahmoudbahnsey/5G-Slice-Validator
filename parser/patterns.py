"""Regex patterns and 5G NAS / session cause dictionaries."""

import re
from typing import Any

# Open5GS AMF / common NAS strings (log wording varies by version)
REGISTRATION_REQUEST = re.compile(
    r"(?:Initial\s+)?Registration\s+Request|registration\s+request",
    re.I,
)
REGISTRATION_ACCEPT = re.compile(r"Registration\s+accept|Registration\s+Accept", re.I)
REGISTRATION_REJECT = re.compile(r"Registration\s+reject|Registration\s+Reject", re.I)
AUTH_REQUEST = re.compile(r"Authentication\s+request|Authentication\s+Request", re.I)
SECURITY_MODE_COMPLETE = re.compile(
    r"Security\s+mode\s+complete|Security\s+Mode\s+Complete", re.I
)

PDU_SESSION_ESTABLISHMENT_ACCEPT = re.compile(
    r"PDU\s+session\s+establishment\s+accept|Session\s+Established", re.I
)
PDU_SESSION_ESTABLISHMENT_REJECT = re.compile(
    r"PDU\s+session\s+establishment\s+reject|pdu_session_establishment_reject", re.I
)

# Cause extraction (multiple formats)
NAS_CAUSE = re.compile(
    r"(?:cause|Cause)\s*[=:]\s*(\d+)|(?:reject).*?(?:cause|cm)\s*[=:]\s*(\d+)",
    re.I,
)
SM_CAUSE = re.compile(
    r"(?:Session\s+reject|PDU\s+session\s+establishment\s+reject)[^\n]{0,120}?cause\s*[=:]?\s*(\d+)",
    re.I,
)
SM_CAUSE_INLINE = re.compile(r"\bsm\s+cause\s+(\d+)", re.I)

IP_ASSIGNED = re.compile(
    r"(?:IPv4|IPv6|IP)[:\s]+(?:address\s*)?(\d+\.\d+\.\d+\.\d+)|addr[=:\s]+(\d+\.\d+\.\d+\.\d+)",
    re.I,
)

UERANSIM_REGISTERED = re.compile(r"(?:\[NAS\]|\[RRC\]).*?(?:Registration\s+accept|registered)", re.I)
UERANSIM_SESSION = re.compile(r"PDU session is activated|Session\s+established|UE IPv4", re.I)

# Compact log styles: cause=27, cm: 11
CAUSE_EQUALS = re.compile(r"cause\s*=\s*(\d+)", re.I)

# 5GMM cause values (TS 24.501) — subset used in demos
MM_CAUSE_MAP: dict[int, str] = {
    3: "Illegal UE",
    5: "PEI not accepted",
    6: "Illegal ME",
    7: "5GS services not allowed",
    9: "UE identity cannot be derived by the network",
    10: "Implicitly de-registered",
    11: "PLMN not allowed",
    12: "Tracking area not allowed",
    13: "Roaming not allowed in this tracking area",
    15: "No suitable cells in tracking area",
    20: "MAC failure",
    21: "Synch failure",
    22: "Congestion",
    23: "UE security capabilities not accepted",
    26: "Insufficient resources",
    27: "Missing or unknown DNN",
    28: "Unknown PDU session type",
    29: "User authentication failed",
    43: "LADN not available",
    62: "No network slices available",
    71: "N1 mode not allowed",
}

# 5GSM cause (PDU session) — TS 24.501
SM_CAUSE_MAP: dict[int, str] = {
    26: "Insufficient resources",
    27: "Missing or unknown DNN",
    28: "Unknown PDU session type",
    29: "User authentication or authorization failed",
    32: "Service option temporarily out of order",
    33: "Requested service option not subscribed",
    36: "Regular deactivation",
    43: "Invalid PDU session identity",
    44: "Semantic errors in request",
    45: "Invalid mandatory information",
    46: "Activated PDU session count exceeds limit",
    51: "PDU type IPv4 only allowed",
    54: "PDU session type mismatch",
    58: "Unsupported SSC mode",
    62: "Slice not supported",
}


def explain_mm_cause(code: int | None) -> str:
    if code is None:
        return "Unknown or unspecified MM cause"
    return MM_CAUSE_MAP.get(code, f"MM cause {code} (see 3GPP TS 24.501)")


def explain_sm_cause(code: int | None) -> str:
    if code is None:
        return "Unknown or unspecified SM cause"
    return SM_CAUSE_MAP.get(code, f"SM cause {code} (see 3GPP TS 24.501)")


def extract_first_int(match: re.Match[str], groups: int = 2) -> int | None:
    for i in range(1, groups + 1):
        g = match.group(i)
        if g:
            return int(g)
    return None
