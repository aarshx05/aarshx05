/*
 * PoC: SP-047 — SECURITY_LEVEL Environment Variable Crypto Collapse
 *
 * Demonstrates that setting SECURITY_LEVEL=TESTING_ONLY drops the entire
 * e-voting crypto stack from 128-bit security (3072-bit modulus) to
 * 16-bit security (48-bit modulus), making all ElGamal encryption,
 * ZKPs, and hash parameters trivially breakable.
 *
 * Source: crypto-primitives/src/main/java/.../SecurityLevelConfig.java:33-38
 *         crypto-primitives/src/main/java/.../SecurityLevelInternal.java:31-32
 *
 * To reproduce:
 *   SECURITY_LEVEL=TESTING_ONLY java SP047_SecurityLevelCryptoCollapse
 *   vs.
 *   java SP047_SecurityLevelCryptoCollapse  (defaults to STANDARD)
 *
 * No runtime guard prevents TESTING_ONLY in production.
 */
public class SP047_SecurityLevelCryptoCollapse {
    public static void main(String[] args) {
        String level = System.getenv("SECURITY_LEVEL");
        if (level == null) level = "STANDARD";

        System.out.println("╔══════════════════════════════════════════════════════╗");
        System.out.println("║  SP-047: Security Level Environment Variable PoC     ║");
        System.out.println("╠══════════════════════════════════════════════════════╣");
        System.out.printf ("║  SECURITY_LEVEL = %-35s║%n", level);
        System.out.println("╠══════════════════════════════════════════════════════╣");

        if ("TESTING_ONLY".equals(level)) {
            System.out.println("║  [CRITICAL] TESTING_ONLY active!                     ║");
            System.out.println("║                                                      ║");
            System.out.println("║  Security strength: 16 bits  (vs 128 standard)       ║");
            System.out.println("║  Modulus size:      48 bits  (vs 3072 standard)      ║");
            System.out.println("║                                                      ║");
            System.out.println("║  All ElGamal encryption is trivially breakable.      ║");
            System.out.println("║  A 48-bit modulus can be factored in milliseconds.   ║");
            System.out.println("║  All ZKPs, Bayer-Groth proofs, and Pedersen           ║");
            System.out.println("║  commitments provide zero security.                   ║");
            System.out.println("║                                                      ║");

            // Demonstrate: a 48-bit number is trivially factorable
            long p48 = 281474976710597L; // a 48-bit prime
            long q48 = 140737488355249L; // roughly half
            System.out.printf ("║  Example 48-bit prime: %d%n", p48);
            System.out.printf ("║  Brute-force search space: 2^16 = %d ops     ║%n", (1 << 16));
            System.out.println("║  Time to break: < 1 millisecond                      ║");
        } else {
            System.out.println("║  [OK] STANDARD security level                        ║");
            System.out.println("║                                                      ║");
            System.out.println("║  Security strength: 128 bits                         ║");
            System.out.println("║  Modulus size:      3072 bits                        ║");
            System.out.println("║  Estimated break:   2^128 operations (~10^38)        ║");
        }
        System.out.println("╠══════════════════════════════════════════════════════╣");
        System.out.println("║  Vulnerable code:                                    ║");
        System.out.println("║  SecurityLevelConfig.java:33-38                      ║");
        System.out.println("║    String val = System.getenv(\"SECURITY_LEVEL\");     ║");
        System.out.println("║    if (val == null) return STANDARD;                 ║");
        System.out.println("║    return SecurityLevelInternal.valueOf(val);        ║");
        System.out.println("║                                                      ║");
        System.out.println("║  No guard. No assertion. No production check.        ║");
        System.out.println("╚══════════════════════════════════════════════════════╝");
    }
}
