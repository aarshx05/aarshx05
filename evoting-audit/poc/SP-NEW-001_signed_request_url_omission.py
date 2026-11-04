#!/usr/bin/env python3
"""
PoC: Inter-Service Signed Request URL Omission
Target: evotingBounty voting-server (older architecture)
File: voting-server/commons/commons-sign/src/main/java/.../sign/beans/SignedRequestContent.java
Lines: 59-68

VULNERABILITY:
SignedRequestContent.getBytes() constructs the signed payload as:
  - Empty body: method + originator
  - Non-empty body: method + body + originator

The URL is passed to the constructor but NEVER included in the signed bytes.
This means the digital signature does not bind to the endpoint being called.

IMPACT:
1. GET Request Replay: All signed GET requests from the same originator with
   no body produce IDENTICAL signatures (method="GET" + originator). A valid
   signed GET to any "secured" endpoint can be replayed to ANY other "secured"
   endpoint on any service.

2. POST Request Cross-Endpoint: A valid signed POST to one endpoint can be
   replayed to a DIFFERENT endpoint accepting the same body structure.

AFFECTED SERVICES (all use SignedRequestFilter with .*secured.*|.*platformdata.*):
- authentication
- certificate-registry
- election-information
- extended-authentication
- orchestrator
- vote-verification
- voter-material
- voting-workflow

CONCRETE ATTACK SCENARIO:
An attacker with network access to the internal service mesh who intercepts a
single signed GET request from any CC node can:
1. Replay it against election-information's getEncryptedBallotBoxes endpoint
   (BallotBoxResource.java:132) to download entire encrypted ballot boxes
2. Replay it against voter-material's secured endpoints to enumerate voter info
3. Replay it against voting-workflow's getIdAndStateOfInactiveVotingCards
   (VoteResource.java:238) to identify which voters haven't voted

BOUNTY RELEVANCE:
- Requires internal network position (CC node compromise or network MITM)
- Enables data exfiltration of election data across service boundaries
- Could enable privacy violation (learning which voters voted/didn't vote)
"""

import hashlib
import hmac
import base64

def demonstrate_url_omission():
    """Demonstrate that different URLs produce identical signatures."""

    # Simulating SignedRequestContent.getBytes() behavior
    def get_signed_bytes(url, method, body, originator):
        """Replicates Java SignedRequestContent.getBytes() - note URL is IGNORED"""
        if not body:
            return (method + originator).encode('utf-8')
        else:
            return (method + body + originator).encode('utf-8')

    originator = "CC_NODE_1"
    method = "GET"

    # Two completely different URLs
    url1 = "/vw-rs-rest/api/v1/secured/tenant/100/electionevent/abc123/votingcards/states/inactive"
    url2 = "/ei-rs-rest/api/v1/secured/tenant/100/electionevent/abc123/ballotbox/def456"

    bytes1 = get_signed_bytes(url1, method, "", originator)
    bytes2 = get_signed_bytes(url2, method, "", originator)

    print("=" * 70)
    print("PoC: SignedRequestContent URL Omission")
    print("=" * 70)
    print()
    print(f"URL 1 (voting-workflow):      {url1}")
    print(f"URL 2 (election-information): {url2}")
    print(f"Method: {method}")
    print(f"Body: (empty)")
    print(f"Originator: {originator}")
    print()
    print(f"Signed bytes for URL 1: {bytes1}")
    print(f"Signed bytes for URL 2: {bytes2}")
    print(f"Bytes are identical: {bytes1 == bytes2}")
    print()

    # Hash (simulating PrimitivesService.getHash)
    hash1 = hashlib.sha256(bytes1).hexdigest()
    hash2 = hashlib.sha256(bytes2).hexdigest()

    print(f"Hash of signed bytes 1: {hash1}")
    print(f"Hash of signed bytes 2: {hash2}")
    print(f"Hashes are identical:   {hash1 == hash2}")
    print()
    print("CONCLUSION: The signature is IDENTICAL for both URLs.")
    print("A valid signed GET intercepted from one endpoint can be")
    print("replayed against ANY other secured endpoint on ANY service.")
    print()

    # POST scenario
    print("-" * 70)
    print("POST Cross-Endpoint Scenario:")
    print("-" * 70)
    body = '{"tenantId":"100","electionEventId":"abc123"}'

    url_auth = "/au-rs-rest/api/v1/secured/tenant/100/authentication/challenge"
    url_ei = "/ei-rs-rest/api/v1/secured/tenant/100/electionevent/abc123/ballotbox/def456"

    bytes_auth = get_signed_bytes(url_auth, "POST", body, originator)
    bytes_ei = get_signed_bytes(url_ei, "POST", body, originator)

    print(f"Auth URL:            {url_auth}")
    print(f"Election Info URL:   {url_ei}")
    print(f"POST body:           {body}")
    print(f"Signed bytes match:  {bytes_auth == bytes_ei}")
    print()
    print("A signed POST to the auth endpoint can be replayed to any")
    print("other secured POST endpoint accepting the same body format.")

    # Source code evidence
    print()
    print("=" * 70)
    print("SOURCE CODE EVIDENCE")
    print("=" * 70)
    print()
    print("SignedRequestContent.java (lines 20-25):")
    print("  Constructor stores URL: this.url = url;")
    print()
    print("SignedRequestContent.java (lines 59-68):")
    print("  getBytes() NEVER uses this.url:")
    print("    if (StringUtils.isEmpty(body)) {")
    print("      return sb.append(method).append(originator)...;")
    print("    } else {")
    print("      return sb.append(method).append(body).append(originator)...;")
    print("    }")
    print()
    print("RestClientInterceptor.java (line 86):")
    print("  URL is passed to constructor but wasted:")
    print("  new SignedRequestContent(request.url().toString(), ...)")
    print()
    print("RequestSigner.java (line 26):")
    print("  sign() calls signedRequestContent.getBytes() -> URL omitted")
    print()
    print("SignedRequestFilter.java (line 152-153):")
    print("  Verification also uses getBytes() -> consistent but broken")

if __name__ == "__main__":
    demonstrate_url_omission()
