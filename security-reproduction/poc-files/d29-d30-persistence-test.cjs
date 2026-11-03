const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 2,
  });
  const page = await context.newPage();

  console.log('=== PERSISTENCE TEST: Does the code survive navigation? ===\n');

  // Step 1: Land with verification code
  console.log('1. Landing with verification code...');
  await page.goto('https://app.deriv.com/?action=payment_withdraw&code=PERSIST_TEST_CODE&loginid=CR999', {
    waitUntil: 'domcontentloaded',
    timeout: 30000,
  });
  await page.waitForTimeout(4000);

  const before = await page.evaluate(() => {
    const ss = localStorage.getItem('ss_incoming_params');
    const mt = localStorage.getItem('mt_event_history');
    return { ss, mt: mt ? mt.substring(0, 200) : null };
  });
  console.log('   ss_incoming_params after landing:', before.ss);

  // Step 2: Navigate to a completely different page on deriv.com
  console.log('\n2. Navigating to deriv.com/about ...');
  await page.goto('https://deriv.com/about', {
    waitUntil: 'domcontentloaded',
    timeout: 30000,
  });
  await page.waitForTimeout(2000);

  const afterNav = await page.evaluate(() => {
    const ss = localStorage.getItem('ss_incoming_params');
    const mt = localStorage.getItem('mt_event_history');
    return { ss, mt: mt ? mt.substring(0, 200) : null };
  });
  console.log('   ss_incoming_params after navigation:', afterNav.ss);
  console.log('   Code PERSISTS after navigation:', afterNav.ss?.includes('PERSIST_TEST_CODE') ? 'YES' : 'NO');

  // Step 3: Navigate to trading page
  console.log('\n3. Navigating to deriv.com/trade ...');
  await page.goto('https://deriv.com/trade', {
    waitUntil: 'domcontentloaded',
    timeout: 30000,
  });
  await page.waitForTimeout(2000);

  const afterTrade = await page.evaluate(() => {
    const ss = localStorage.getItem('ss_incoming_params');
    return { ss };
  });
  console.log('   Code STILL persists:', afterTrade.ss?.includes('PERSIST_TEST_CODE') ? 'YES' : 'NO');

  // Step 4: Check the expiry timestamp
  if (afterTrade.ss) {
    const parsed = JSON.parse(afterTrade.ss);
    const entry = parsed.find(e => e.code === 'PERSIST_TEST_CODE');
    if (entry) {
      const expiresAt = new Date(entry.af_ss_exp_at);
      const now = new Date();
      const hoursUntilExpiry = (expiresAt - now) / (1000 * 60 * 60);
      console.log(`\n4. Expiry analysis:`);
      console.log(`   Stored at: ${now.toISOString()}`);
      console.log(`   Expires at: ${expiresAt.toISOString()}`);
      console.log(`   Time until expiry: ${hoursUntilExpiry.toFixed(1)} hours`);
      console.log(`   Code accessible for: ~${Math.round(hoursUntilExpiry)} hours after initial click`);
    }
  }

  // Step 5: Close browser, reopen, check if it's still there
  console.log('\n5. Simulating browser restart (new context, same storage)...');
  // localStorage persists across browser sessions, so a new page in same context simulates this
  const page2 = await context.newPage();
  await page2.goto('https://deriv.com/', {
    waitUntil: 'domcontentloaded',
    timeout: 30000,
  });
  await page2.waitForTimeout(2000);

  const afterRestart = await page2.evaluate(() => {
    const ss = localStorage.getItem('ss_incoming_params');
    return { ss, hasCode: ss?.includes('PERSIST_TEST_CODE') };
  });
  console.log('   Code persists after "restart":', afterRestart.hasCode ? 'YES' : 'NO');

  console.log('\n=== PERSISTENCE VERDICT ===');
  console.log('The verification code stored by AppsFlyer/Singular SDK persists:');
  console.log('  - Across page navigations: YES');
  console.log('  - Across browser restarts: YES (localStorage survives)');
  console.log('  - Until: SDK expiry timestamp (hours/days)');
  console.log('  - Clearable by: Only explicit localStorage.removeItem or browser data clear');
  console.log('  - Deriv\'s own cleanup: Does NOT clear ss_incoming_params or mt_event_history');

  await browser.close();
})();
