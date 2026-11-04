/*
 * PoC: SP-032 — Keystore Password Improperly Zeroed
 *
 * The SignatureKeystoreService.java (line 88) attempts to clear the
 * keystore password from memory after use, but uses Arrays.fill(password, '0')
 * instead of Arrays.fill(password, '\0').
 *
 * '0' is char 0x30 (the digit zero), not '\0' (null char 0x00).
 * The password array is replaced with "000000..." rather than being blanked.
 *
 * Source: crypto-primitives/src/main/java/.../internal/signing/SignatureKeystoreService.java:88
 *
 * Impact: A memory dump or heap analysis will find the string "000000..."
 * at exactly the same length as the original password, leaking the password
 * length and making it clear this location held a password. A true zeroing
 * ('\0') would appear as empty memory.
 */
public class SP032_PasswordZeroing {
    public static void main(String[] args) {
        char[] password = "Election2025!Secret".toCharArray();
        System.out.println("╔══════════════════════════════════════════════════════╗");
        System.out.println("║  SP-032: Password Zeroing Bug PoC                    ║");
        System.out.println("╠══════════════════════════════════════════════════════╣");

        System.out.println("║  Original password: " + new String(password));
        System.out.println("║  Length: " + password.length + " characters");
        System.out.println("║                                                      ║");

        // What the code DOES (buggy):
        java.util.Arrays.fill(password, '0');
        System.out.println("║  After Arrays.fill(password, '0'):                   ║");
        System.out.println("║  Memory contains: \"" + new String(password) + "\"");
        System.out.println("║  Hex dump: " + toHex(password));
        System.out.println("║  → Password LENGTH leaked, location obvious          ║");
        System.out.println("║                                                      ║");

        // What the code SHOULD do:
        char[] password2 = "Election2025!Secret".toCharArray();
        java.util.Arrays.fill(password2, '\0');
        System.out.println("║  After Arrays.fill(password, '\\0') [correct]:        ║");
        System.out.println("║  Memory contains: \"" + new String(password2).replace("\0","\\0") + "\"");
        System.out.println("║  Hex dump: " + toHex(password2));
        System.out.println("║  → Appears as empty memory                           ║");

        System.out.println("╠══════════════════════════════════════════════════════╣");
        System.out.println("║  Vulnerable line:                                    ║");
        System.out.println("║  SignatureKeystoreService.java:88                    ║");
        System.out.println("║    Arrays.fill(password, '0');  // char '0' = 0x30   ║");
        System.out.println("║  Should be:                                          ║");
        System.out.println("║    Arrays.fill(password, '\\0'); // null char = 0x00  ║");
        System.out.println("╚══════════════════════════════════════════════════════╝");
    }

    static String toHex(char[] chars) {
        StringBuilder sb = new StringBuilder();
        for (char c : chars) sb.append(String.format("0x%02X ", (int) c));
        return sb.toString().trim();
    }
}
