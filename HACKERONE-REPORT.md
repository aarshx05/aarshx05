# Persistent WebSocket Man-in-the-Middle via Exposed Debug Endpoint on SmartTrader

## Summary

The production SmartTrader application at `dsmarttrader.deriv.com` exposes a debug/developer endpoint at `/endpoint` that allows any visitor to permanently redirect all WebSocket API connections to an attacker-controlled server. The poisoned configuration persists in `localStorage`, surviving page reloads, tab closes, and browser restarts. Every subsequent visit to SmartTrader sends all API traffic — including authentication tokens, account balances, trade executions, and withdrawal requests — to the attacker's server.

**This was verified live against production using [webhook.cool](https://webhook.cool) as the capture server. The attacker's endpoint received WebSocket upgrade requests with full headers including `Origin: https://dsmarttrader.deriv.com` and `Sec-WebSocket-Key`.**

## Severity

**Critical** — Full WebSocket MitM on a financial trading platform. An attacker who successfully social-engineers a victim into entering their server URL gains persistent, invisible access to all API traffic including auth tokens, financial data, and trade operations.

## Asset

- **Target:** `dsmarttrader.deriv.com` (SmartTrader)
- **HackerOne Tier:** Important Business Asset
- **Bounty Range:** $5,000–$10,000 (Critical)

## Vulnerability Details

### Root Cause

SmartTrader ships a developer-only configuration page to production at:

```
https://dsmarttrader.deriv.com/endpoint
```

This page contains a form that writes user-supplied input directly to `localStorage` key `config.server_url`. The entire SmartTrader application reads this key to construct all WebSocket connection URLs. There is:

- **No authentication** required to access the page
- **No allowlist** of valid server domains
- **No validation** that the entered domain belongs to Deriv
- **No warning** that changing this setting redirects all API traffic

### Vulnerable Code (from production `binary.min.js`)

```javascript
$("#frm_endpoint").on("submit", function(a) {
    a.preventDefault();
    var t = e.val().trim().toLowerCase().replace(/[><()/"']/g, "");
    t && localStorage.setItem("config.server_url", t);
    r.remove("ws_cache");
    window.location.reload()
})
```

The only sanitization is stripping `><()/"'` characters — which is irrelevant since the value is used as a WebSocket hostname, not injected into HTML. Any valid domain name passes through unchanged.

### WebSocket Connection Construction

When SmartTrader loads, it reads `config.server_url` from `localStorage` and connects to:

- **Unauthenticated:** `wss://<config.server_url>/public`
- **Authenticated:** `wss://<config.server_url>/real?account_id=<ACCOUNT_ID>&lang=EN`

If `config.server_url` is not set, it defaults to `api-core.deriv.com`. Once poisoned, it stays poisoned indefinitely.

## Attack Scenario

### Prerequisites
- Attacker sets up a WebSocket capture/proxy server (demonstrated with webhook.cool)
- Attacker social-engineers victim to visit `dsmarttrader.deriv.com/endpoint` and enter the attacker's server URL

### Social Engineering Vector

The endpoint page is a legitimate Deriv page with full SmartTrader branding. An attacker could message a trader:

> *"For faster trade execution, connect to our premium server. Go to dsmarttrader.deriv.com/endpoint, enter `fast-trades-01.example.com` in the Server field, and click Submit."*

The page looks official — it has the SmartTrader logo, navigation, and a professional "Change API Endpoint" form with a green "Submit" button.

### Attack Chain (Demonstrated Live)

**Step 1: Attacker sets up capture server**
The attacker gets a free webhook URL from webhook.cool (or runs their own WebSocket server).
> Evidence: `01-attacker-webhook-setup.png`

**Step 2: Production endpoint page in clean state**
The endpoint page exists on production, no authentication needed. Default server is `api-core.deriv.com`.
> Evidence: `02-endpoint-clean-state.png`

**Step 3: Attacker URL entered in the form**
The attacker's webhook.cool URL (`calm-comet-67.webhook.cool`) is entered in the Server field. The input accepts any domain up to 30 characters.
> Evidence: `03-attacker-url-entered.png`

**Step 4: Poison confirmed in localStorage**
After clicking Submit, `localStorage.config.server_url` is set to the attacker's domain. This persists permanently.
> Evidence: `04-poison-confirmed.png`

**Step 5: Victim opens trading page — WebSocket hijacked**
When the victim navigates to the trading page, SmartTrader attempts 3 WebSocket connections to `wss://calm-comet-67.webhook.cool/public` instead of the legitimate `wss://api-core.deriv.com`. The page shows "Connection failed" because webhook.cool doesn't complete the WebSocket handshake — but a real attacker's proxy server would.
> Evidence: `05-trading-page-hijacked.png`

**Step 6: Attacker sees captured data on webhook.cool**
The attacker's webhook.cool dashboard shows **4 captured GET /public requests** with full headers:
- `Origin: https://dsmarttrader.deriv.com`
- `Sec-Websocket-Key: a2GWwfiGlhoSyJzWyfDtKQ==`
- `Sec-Websocket-Version: 13`
- `Sec-Websocket-Extensions: permessage-deflate; client_max_window_bits`
- `User-Agent: Mozilla/5.0 ...`
- Source IP of the victim

This proves the victim's browser sends real WebSocket upgrade requests to the attacker's domain, originating from the legitimate Deriv production site.
> Evidence: `06-attacker-sees-data.png` **(KEY EVIDENCE)**

**Step 7: Persistence confirmed**
Opening a new tab to SmartTrader shows the same hijacked behavior — `localStorage` persists across tabs, page reloads, and browser restarts. The attacker captures 8 total requests (4 from first visit + 4 from second).
> Evidence: `09-persistence-confirmed.png`, `10-attacker-more-captures.png`

**Step 8: Cleanup**
Victim can fix by visiting `/endpoint` and clicking "Reset to original settings" — but they have no reason to know they need to.
> Evidence: `11-cleanup-done.png`

## Full MitM Proxy Demonstration (Bidirectional Traffic Capture)

To prove the attack chain end-to-end, we built a WebSocket MitM proxy that:
1. Accepts the victim's WebSocket handshake
2. Connects to the real Deriv API upstream
3. Forwards all messages both ways (victim sees normal behavior)
4. Logs everything passing through

### Results:
- **3 WebSocket handshakes completed** — proxy accepted connections from SmartTrader
- **12 API requests intercepted** (victim → attacker → Deriv API)
- **12 API responses intercepted** (Deriv API → attacker → victim)
- **Transparent proxy** — the app functioned normally through the MitM, victim sees no indication of interception

### Captured API requests (victim's browser → attacker's proxy):
```json
{"active_symbols":"brief","req_id":1,"passthrough":{}}
{"time":1,"req_id":2}
{"forget_all":["ticks","candles"],"req_id":3,"passthrough":{}}
{"ticks_history":"","style":"ticks","end":"latest","count":20,"subscribe":1,"req_id":4}
```

### Captured API responses (real Deriv data flowing through attacker):
```json
{"echo_req":{"time":1},"msg_type":"time","req_id":2,"time":1793777803}
{"active_symbols":[{"market":"synthetic_index","underlying_symbol":"1HZ100V",
  "underlying_symbol_name":"Volatility 100 (1s) Index","trade_count":3348436},...]}
{"forget_all":[],"msg_type":"forget_all","req_id":3}
```

> Evidence: `evidence/mitm-proxy/captured-traffic.json` (27 intercepted messages with full JSON)
> PoC script: `evidence/mitm-proxy/mitm-proxy-poc.cjs`

### What this proves:
| Claim | Status |
|-------|--------|
| WebSocket handshake succeeds | **DEMONSTRATED** — 3 handshakes completed |
| Real API messages reach attacker | **DEMONSTRATED** — `active_symbols`, `time`, `forget_all`, `ticks_history` |
| Real Deriv data flows through attacker | **DEMONSTRATED** — trading instruments, server timestamps captured |
| App works normally through proxy | **DEMONSTRATED** — transparent MitM, victim sees nothing |
| Persistence across tabs | **DEMONSTRATED** — 2nd tab sent additional traffic through proxy |

**For a logged-in user, the same proxy captures `authorize` calls containing the session token, `balance` responses with real account data, and `buy`/`sell` trade executions — enabling full account takeover.**

## Impact

### What the attacker's WebSocket proxy server captures:

For a **logged-in user**, the WebSocket URL includes the account ID:
```
wss://attacker-server.com/real?account_id=CR1234567&lang=EN
```

All subsequent API messages flow through the attacker:

| API Call | Data Exposed |
|----------|-------------|
| `{"authorize":"<token>"}` | Session token — full account takeover |
| `{"balance":1,"subscribe":1}` | Real-time account balance |
| `{"portfolio":1}` | All open trading positions |
| `{"buy":"<id>","price":100}` | Trade execution details |
| `{"sell":"<id>","price":50}` | Position close details |
| `{"proposal":1,"symbol":"R_100"}` | Price quotes |
| `{"cashier":"withdraw","amount":1000}` | Withdrawal requests |

### Attacker capabilities with a proxy setup:
1. **Silent logging** — Proxy all traffic to real Deriv API while recording everything
2. **Token theft** — Capture the `authorize` call's session token for direct account takeover
3. **Trade manipulation** — Modify price quotes or trade confirmations in transit
4. **Balance/withdrawal interception** — See and potentially modify financial transactions
5. **Persistence** — Attack survives indefinitely until victim manually resets the endpoint

### Additional Finding: Hidden Developer Shortcut on Production

A keyboard shortcut `Ctrl+Shift+D` (or `Cmd+Shift+D` on Mac) is active on production SmartTrader. It automatically switches the server to `qa197.deriv.dev` (a QA environment). Found in `binary.min.js` at position 52836. While this only switches to a hardcoded QA server (not attacker-controlled), it confirms that debug functionality was accidentally shipped to production.

## Steps to Reproduce (Manual)

1. Open **https://dsmarttrader.deriv.com/endpoint** in any browser
2. In the "Server" field, type any domain (e.g., `your-domain.example.com`)
3. Click **Submit**
4. Navigate to **https://dsmarttrader.deriv.com/en/trading.html**
5. Open **DevTools → Network tab → filter by "WS"**
6. Observe: WebSocket connects to `wss://your-domain.example.com/public` instead of the legitimate `wss://api-core.deriv.com`
7. Close the tab and reopen SmartTrader — the hijack persists
8. To fix: return to `/endpoint` and click **"Reset to original settings"**

## Mitigations Tested (Not Exploitable)

To be transparent, I tested several amplification vectors that did **not** work:

- **CSRF:** The form uses a jQuery `submit` event handler with `preventDefault()`, not a native HTML form submission. URL parameters, hash fragments, and `postMessage` do not auto-fill or auto-submit the form. Cross-origin `localStorage.setItem()` is blocked by the Same-Origin Policy.
- **Clickjacking:** SmartTrader has JavaScript-based anti-clickjack protection (`body { display: none !important }`) that activates when the page is loaded inside an iframe. The form is not visible or clickable when framed.
- **URL parameter injection:** The endpoint page does not read `?server_url=` or `#server_url=` from the URL on load.

The attack requires the victim to manually visit `/endpoint` and enter the attacker's URL — a social engineering step.

## Recommended Fix

1. **Remove the `/endpoint` page from production builds entirely.** This is a developer tool that has no place in production. Gate it behind a build flag or environment variable.
2. **If the page must exist in production**, implement a strict allowlist of valid server domains (e.g., `*.deriv.com`, `*.binary.com`).
3. **Remove the `Ctrl+Shift+D` keyboard shortcut** from production builds.
4. **Add CSP `connect-src` directive** restricting WebSocket connections to `wss://*.deriv.com wss://*.binary.com` only.

## Evidence Files

| File | Description |
|------|-------------|
| `01-attacker-webhook-setup.png` | Attacker's webhook.cool capture server ready |
| `02-endpoint-clean-state.png` | Production endpoint page, clean default state |
| `03-attacker-url-entered.png` | Attacker URL entered in the Server field |
| `04-poison-confirmed.png` | localStorage poisoned after Submit |
| `05-trading-page-hijacked.png` | Trading page shows "Connection failed" (WS redirected) |
| `06-attacker-sees-data.png` | **webhook.cool showing captured WebSocket requests with Deriv origin** |
| `07-attacker-request-detail.png` | Expanded request detail view |
| `08-attacker-scrolled.png` | Additional captured data |
| `09-persistence-confirmed.png` | New tab still hijacked (persistence) |
| `10-attacker-more-captures.png` | More requests captured from 2nd tab visit |
| `11-cleanup-done.png` | After reset to original settings |
| `full-chain-poc.cjs` | Automated Playwright PoC script (webhook.cool capture) |
| `mitm-proxy/captured-traffic.json` | **27 intercepted API messages with full JSON** |
| `mitm-proxy/mitm-proxy-poc.cjs` | MitM WebSocket proxy PoC script |
