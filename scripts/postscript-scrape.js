/**
 * Postscript SMS Scraper — Skullette (Shop 555740)
 *
 * Login → Switch to Skullette shop → Navigate campaigns →
 * Extract SMS body + metrics from each campaign page
 *
 * Usage:
 *   node postscript-scrape.js              # Full scrape (headed mode for first run)
 *   node postscript-scrape.js --headed     # Force headed mode (debug shop switch)
 *   node postscript-scrape.js --limit 5    # Limit to N campaigns
 *   node postscript-scrape.js --since 2026-01-01  # Only campaigns after date
 *
 * Requires:
 *   npm install playwright
 *   npx playwright install chromium
 */
import fs from 'fs';
import path from 'path';
import { chromium } from 'playwright';

// ─── Configuration ──────────────────────────────────────────────────────────
const EMAIL = 'duc@highcommerce.org';
const PASSWORD = 'Tun%fZy*$J08*G';
const SKULLETTE_SHOP_ID = 555740;
const API_BASE = 'https://internal-api.postscript.io';

const PROJECT_ROOT = path.resolve('d:/Skullette - Copywriting');
const OUTPUT = path.join(PROJECT_ROOT, 'postscript');
const SMS_DIR = path.join(OUTPUT, 'sms');
const SCREENSHOTS = path.join(OUTPUT, 'screenshots');
const RAW_FILE = path.join(OUTPUT, 'sms-raw.json');
const SUMMARY_FILE = path.join(OUTPUT, 'sms-summary.md');

function ensureDir(dir) { if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true }); }
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

function sanitize(name) {
  return name.replace(/[<>:"/\\|?*]/g, '').replace(/\s+/g, '-').substring(0, 80);
}

function saveJSON(filepath, data) {
  fs.writeFileSync(filepath, JSON.stringify(data, null, 2), 'utf-8');
}

// ─── Parse CLI args ─────────────────────────────────────────────────────────
const args = process.argv.slice(2);
const HEADED = args.includes('--headed');
const LIMIT = args.includes('--limit') ? parseInt(args[args.indexOf('--limit') + 1]) : 0;
const SINCE = args.includes('--since') ? args[args.indexOf('--since') + 1] : null;

// ─── Extract content from campaign page ─────────────────────────────────────
async function extractCampaignContent(page) {
  return page.evaluate(() => {
    const text = document.body.innerText;
    const lines = text.split('\n').map(l => l.trim()).filter(l => l);
    const result = {};

    // Campaign name — before "Enter a description"
    for (let i = 0; i < lines.length; i++) {
      if (lines[i] === 'Enter a description' && i > 0) {
        result.name = lines[i - 1];
        break;
      }
    }

    // Extract metrics
    for (const line of lines) {
      if (line.startsWith('Revenue:')) result.revenue = line.replace('Revenue:', '').trim();
      if (line.startsWith('EPM:')) result.epm = line.replace('EPM:', '').trim();
      if (line.startsWith('Orders:') && !result.orders) result.orders = line.replace('Orders:', '').trim();
      if (line.startsWith('CVR:') && !result.cvr) result.cvr = line.replace('CVR:', '').trim();
      if (line.startsWith('Clicks:') && !result.clicks) result.clicks = line.replace('Clicks:', '').trim();
      if (line.startsWith('CTR:') && !result.ctr) result.ctr = line.replace('CTR:', '').trim();
      if (line.startsWith('UCTR:') && !result.uctr) result.uctr = line.replace('UCTR:', '').trim();
      if (line.startsWith('Messages sent:')) result.sent = line.replace('Messages sent:', '').trim();
      if (line.startsWith('Sent:') && !result.sent) result.sent = line.replace('Sent:', '').trim();
      if (line.startsWith('Unsubscribe rate:')) result.unsub_rate = line.replace('Unsubscribe rate:', '').trim();
      if (line.includes('Completed') && !result.status) result.status = 'Completed';
    }

    // Extract segment
    const segIdx = lines.findIndex(l => l === 'Send to subscribers in');
    if (segIdx >= 0 && lines[segIdx + 1]) {
      result.segment = lines[segIdx + 1];
    }

    // Extract SMS body — find "Message" label
    const msgIdx = lines.findIndex(l => l === 'Message');
    if (msgIdx >= 0) {
      const smsLines = [];
      for (let i = msgIdx + 1; i < lines.length; i++) {
        const l = lines[i];
        if (l.startsWith('Rev.:') || l.startsWith('EPM:') || l.startsWith('Orders:') ||
            l.startsWith('Revenue:') || l.startsWith('Clicks:')) break;
        smsLines.push(l);
      }
      result.sms_body = smsLines.join('\n').trim();
    }

    // Fallback: find text starting with "Skullette:" or shop name
    if (!result.sms_body) {
      for (let i = 0; i < lines.length; i++) {
        if (lines[i].startsWith('Skullette:') || lines[i].startsWith('{shop_name}')) {
          const smsLines = [lines[i]];
          for (let j = i + 1; j < Math.min(i + 20, lines.length); j++) {
            if (lines[j].startsWith('Rev.:') || lines[j].startsWith('EPM:')) break;
            smsLines.push(lines[j]);
          }
          result.sms_body = smsLines.join('\n').trim();
          break;
        }
      }
    }

    // Extract date
    const dateMatch = text.match(/([A-Z][a-z]{2}\s+\d{1,2},\s+\d{4})/);
    if (dateMatch) result.date = dateMatch[1];

    return result;
  });
}

// ─── Remove overlay popups ──────────────────────────────────────────────────
async function removeOverlays(page) {
  await page.evaluate(() => {
    document.querySelectorAll(
      '[class*="CL__sc-"], [class*="intercom"], iframe[name*="intercom"], #intercom-container'
    ).forEach(el => el.remove());
  }).catch(() => {});
}

// ─── Main ───────────────────────────────────────────────────────────────────
async function main() {
  ensureDir(OUTPUT);
  ensureDir(SMS_DIR);
  ensureDir(SCREENSHOTS);

  console.log('═══════════════════════════════════════');
  console.log(` POSTSCRIPT — SKULLETTE (${SKULLETTE_SHOP_ID})`);
  console.log('═══════════════════════════════════════\n');

  // Load existing data for resume
  let existing = [];
  let doneGuids = new Set();
  if (fs.existsSync(RAW_FILE)) {
    existing = JSON.parse(fs.readFileSync(RAW_FILE, 'utf-8'));
    doneGuids = new Set(existing.map(e => e.guid));
    console.log(`  Resuming: ${existing.length} campaigns already scraped`);
  }

  const browser = await chromium.launch({ headless: !HEADED, slowMo: HEADED ? 50 : 0 });
  const context = await browser.newContext({ viewport: { width: 1400, height: 900 } });
  const page = await context.newPage();

  let token = null;

  // Capture token from API responses
  page.on('request', (request) => {
    if (request.url().includes('internal-api.postscript.io')) {
      const auth = request.headers()['authorization'];
      if (auth?.startsWith('Bearer ')) token = auth.replace('Bearer ', '');
    }
  });
  page.on('response', async (response) => {
    if (!response.url().includes('internal-api.postscript.io')) return;
    try {
      if (response.status() === 200 && response.headers()['content-type']?.includes('json')) {
        const body = await response.json().catch(() => null);
        if (body?.access_token) { token = body.access_token; console.log('  🔑 Token captured'); }
      }
    } catch {}
  });

  // ── Step 1: Login ──
  console.log('🔑 Login...');
  await page.goto('https://app.postscript.io/login', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await sleep(3000);

  const emailLink = page.locator('text=Login With Email').first();
  if (await emailLink.isVisible().catch(() => false)) {
    await emailLink.click();
    await sleep(2000);
  }

  await page.locator('input[type="email"], input[placeholder*="email" i]').first().fill(EMAIL);
  await page.locator('input[type="password"]').first().fill(PASSWORD);
  await sleep(500);
  await page.locator('button[type="submit"], button:has-text("Log in"), button:has-text("Login")').first().click();
  await sleep(6000);
  console.log('  ✓ Logged in | URL:', page.url());
  await page.screenshot({ path: path.join(SCREENSHOTS, '01-logged-in.png'), fullPage: true });

  // ── Step 2: Switch to Skullette shop ──
  console.log('\n🔄 Switching to Skullette...');

  // Dismiss any overlays/modals that block interaction
  // Known: "Help Postscript understand your brand voice" modal + chat widget
  for (const dismissSel of [
    '[data-visible="true"][class*="sc-141v21k"]', // Postscript notification/chat overlay
    'button:has-text("Dismiss")',
    'button:has-text("Got it")',
    'button:has-text("Close")',
    '[aria-label="Close"]',
    'button:has-text("Skip")',
    'button:has-text("My Topics")', // Brand voice modal dismiss
    '[class*="modal"] button:has-text("Close")',
    '[class*="dialog"] button:has-text("Close")',
  ]) {
    const overlay = page.locator(dismissSel).first();
    if (await overlay.isVisible({ timeout: 1000 }).catch(() => false)) {
      console.log(`  Dismissing overlay: ${dismissSel}`);
      await overlay.click({ force: true }).catch(() => {});
      await sleep(1000);
    }
  }
  // Also press Escape to close any remaining modals
  await page.keyboard.press('Escape').catch(() => {});
  await sleep(1000);

  // Look for shop switcher at bottom of sidebar
  const shopArea = page.locator('text=total subscribers').first();
  if (await shopArea.isVisible({ timeout: 5000 }).catch(() => false)) {
    console.log('  Found shop switcher — clicking...');
    try {
      await shopArea.locator('..').click({ timeout: 5000 });
    } catch {
      console.log('  Overlay still blocking — forcing click...');
      await shopArea.locator('..').click({ force: true });
    }
    await sleep(2000);
    await page.screenshot({ path: path.join(SCREENSHOTS, '02-shop-dropdown.png'), fullPage: true });
  }

  // Find and click Skullette
  let foundShop = false;
  for (const selector of [
    'text=Skullette',
    '[class*="option"]:has-text("Skullette")',
    '[class*="shop"]:has-text("Skullette")',
    'li:has-text("Skullette")',
    'a:has-text("Skullette")',
    'div:has-text("Skullette")',
  ]) {
    const el = page.locator(selector).first();
    if (await el.isVisible({ timeout: 2000 }).catch(() => false)) {
      try {
        await el.click({ timeout: 3000 });
      } catch {
        await el.click({ force: true });
      }
      foundShop = true;
      console.log(`  ✓ Clicked Skullette (${selector})`);
      break;
    }
  }

  if (!foundShop) {
    // Fallback: direct URL navigation
    console.log('  ⚠️ Shop switcher not found — trying direct URL...');
    await page.goto(`https://app.postscript.io/shops/${SKULLETTE_SHOP_ID}`, { waitUntil: 'domcontentloaded' });
  }

  await sleep(5000);
  await page.screenshot({ path: path.join(SCREENSHOTS, '03-shop-switched.png'), fullPage: true });
  console.log('  Current URL:', page.url());

  // Wait for token
  if (!token) {
    console.log('  Waiting for API token...');
    await sleep(5000);
  }
  if (!token) {
    console.log('  ⚠️ No token captured. Trying to trigger API call...');
    await page.goto(`https://app.postscript.io/shops/${SKULLETTE_SHOP_ID}/campaigns`, { waitUntil: 'domcontentloaded' });
    await sleep(5000);
  }

  if (!token) {
    console.log('  ❌ No API token captured. Please run with --headed and manually switch shop.');
    await browser.close();
    return;
  }

  console.log('  ✓ Token available');

  // ── Step 3: Fetch campaigns via discovered API endpoints ──
  console.log('\n📋 Fetching campaign list...');

  // Navigate to campaigns page to get fresh token for this shop context
  await page.goto(`https://app.postscript.io/campaigns`, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await sleep(5000);
  await page.screenshot({ path: path.join(SCREENSHOTS, '04-campaigns-page.png'), fullPage: true });

  const headers = {
    'Authorization': `Bearer ${token}`,
    'X-Shop-Id': String(SKULLETTE_SHOP_ID),
    'Accept': 'application/json',
  };

  // Fetch sent campaigns using the confirmed working endpoint
  // Response format: { campaigns: [...] }
  let campaigns = [];
  const PAGE_SIZE = 50;

  console.log('  Fetching sent campaigns...');
  let start = 0;
  while (true) {
    const url = `${API_BASE}/campaigns/sent?limit=${PAGE_SIZE}&sort_column=sent_time&sort_reverse=true&start=${start}&title=`;
    try {
      const resp = await fetch(url, { headers });
      if (!resp.ok) {
        console.log(`  API error ${resp.status} at start=${start}`);
        break;
      }
      const data = await resp.json();
      console.log(`  Response keys: ${Object.keys(data).join(', ')}`);
      // Handle nested response: { campaigns: { campaigns: [...], totalResults: N } }
      let batch = data.campaigns;
      if (batch && typeof batch === 'object' && !Array.isArray(batch)) {
        console.log(`  Inner keys: ${Object.keys(batch).join(', ')}, totalResults: ${batch.totalResults}`);
        batch = batch.campaigns || batch.data || batch.sent || batch.results;
      }
      if (!Array.isArray(batch)) {
        console.log(`  Unexpected shape: ${JSON.stringify(data).substring(0, 500)}`);
        break;
      }
      if (batch.length === 0) break;
      campaigns.push(...batch);
      console.log(`  Fetched ${campaigns.length} sent campaigns (batch: ${batch.length})...`);
      if (batch.length < PAGE_SIZE) break; // last page
      start += PAGE_SIZE;
      await sleep(500); // rate limit
    } catch (e) {
      console.log(`  Fetch error at start=${start}: ${e.message}`);
      break;
    }
  }

  // Also fetch draft/preview campaigns
  console.log('  Fetching draft campaigns...');
  try {
    const resp = await fetch(`${API_BASE}/campaigns/preview?limit=50&sort_column=last_edited&sort_reverse=true&start=0&title=`, { headers });
    if (resp.ok) {
      const data = await resp.json();
      let drafts = data.campaigns;
      if (drafts && !Array.isArray(drafts)) drafts = drafts.data || Object.values(drafts);
      console.log(`  Found ${Array.isArray(drafts) ? drafts.length : 0} draft campaigns`);
    }
  } catch {}

  console.log(`  Total sent campaigns: ${campaigns.length}`);

  if (campaigns.length === 0) {
    console.log('  ❌ No campaigns found.');
    // Try the timeframe endpoint as last resort
    try {
      const resp = await fetch(`${API_BASE}/campaigns/timeframe/365`, { headers });
      if (resp.ok) {
        const data = await resp.json();
        let fb = data.campaigns;
        if (fb && !Array.isArray(fb)) fb = fb.data || Object.values(fb);
        if (Array.isArray(fb)) {
          campaigns = fb;
          console.log(`  Timeframe fallback: ${campaigns.length} campaigns`);
        } else {
          console.log(`  Timeframe shape: ${JSON.stringify(data).substring(0, 300)}`);
        }
      }
    } catch {}
  }

  if (campaigns.length === 0) {
    console.log('  ❌ No campaigns found after all attempts.');
    await page.screenshot({ path: path.join(SCREENSHOTS, '05-no-campaigns-debug.png'), fullPage: true });
    await browser.close();
    return;
  }

  // Log first campaign object keys for debugging
  if (campaigns.length > 0) {
    console.log(`  Campaign object keys: ${Object.keys(campaigns[0]).join(', ')}`);
    console.log(`  Sample: ${JSON.stringify(campaigns[0]).substring(0, 300)}`);
  }

  // Filter by date if --since provided
  if (SINCE) {
    const sinceDate = new Date(SINCE);
    const before = campaigns.length;
    campaigns = campaigns.filter(c => {
      const d = c.sent_time || c.sent_at || c.scheduled_at || c.created_at || '';
      return d ? new Date(d) >= sinceDate : true;
    });
    console.log(`  Filtered to ${campaigns.length} (from ${before}) since ${SINCE}`);
  }

  // Apply limit
  if (LIMIT && LIMIT > 0) {
    campaigns = campaigns.slice(0, LIMIT);
    console.log(`  Limited to ${campaigns.length}`);
  }

  // ── Step 4: Scrape each campaign ──
  console.log(`\n📱 Scraping ${campaigns.length} campaigns...`);
  const results = [...existing];
  let scraped = 0;

  for (const campaign of campaigns) {
    const cid = String(campaign.campaign_id || campaign.id || '');
    if (!cid || doneGuids.has(cid)) continue;

    const campaignName = campaign.name || campaign.title || 'Unknown';
    console.log(`\n  [${scraped + 1}/${campaigns.length}] ${campaignName}`);

    try {
      // Extract data from the list API response (already has SMS body as original_text)
      let smsBody = campaign.original_text || campaign.body || campaign.message || '';
      let sentDate = (campaign.sent_time || campaign.last_edited || campaign.sent_at || '').substring(0, 10);
      let segment = campaign.subscriber_group_name || campaign.segment_name || campaign.segment || '';

      // If no body in list data, fetch campaign detail API
      if (!smsBody) {
        try {
          const detailResp = await fetch(`${API_BASE}/campaigns/${cid}`, { headers });
          if (detailResp.ok) {
            const detail = await detailResp.json();
            const c = detail.campaign || detail.campaigns?.campaigns?.[0] || detail;
            smsBody = c.original_text || c.body || c.message || '';
            if (!segment) segment = c.subscriber_group_name || c.segment_name || '';
            if (!sentDate) sentDate = (c.sent_time || c.last_edited || '').substring(0, 10);
            if (smsBody) console.log(`    API detail ✓`);
          }
        } catch {}
      }

      // Last resort: page scraping
      if (!smsBody) {
        try {
          await page.goto(`https://app.postscript.io/campaigns/${cid}`, { waitUntil: 'domcontentloaded', timeout: 20000 });
          await sleep(3000);
          await removeOverlays(page);
          const content = await extractCampaignContent(page);
          smsBody = content.sms_body || '';
          if (!segment) segment = content.segment || '';
          if (smsBody) console.log(`    Page extract ✓`);
        } catch (e) {
          console.log(`    Page error: ${e.message.substring(0, 80)}`);
        }
      }

      // Extract segment name (segment may be an object or string)
      const segObj = campaign.segment;
      const segName = typeof segObj === 'string' ? segObj : (segObj?.name || segment || '');

      // Use correct metric field names from Postscript API
      const sentCount = campaign.sent_count || campaign.delivered_count || campaign.messages_sent || 0;
      const totalClicks = campaign.total_clicks || campaign.click_count || 0;
      const uniqueClicks = campaign.unique_clicks || 0;
      const uctrVal = sentCount > 0 ? ((uniqueClicks / sentCount) * 100) : 0;
      const ordersCount = campaign.attributed_orders_count || campaign.order_count || 0;
      const revenueVal = parseFloat(campaign.attributed_revenue || campaign.revenue || campaign.total_revenue || 0);
      const unsubCount = campaign.unsubscribe_count || 0;
      const unsubRate = sentCount > 0 ? ((unsubCount / sentCount) * 100).toFixed(2) + '%' : '';

      const record = {
        guid: cid,
        name: campaignName,
        date: sentDate,
        sms_body: smsBody,
        segment: segName,
        sent: sentCount,
        clicks: totalClicks,
        unique_clicks: uniqueClicks,
        uctr: Math.round(uctrVal * 100) / 100,
        orders: ordersCount,
        revenue: revenueVal,
        unsub_rate: unsubRate,
        status: campaign.status || '',
        channel: 'sms',
      };

      results.push(record);
      doneGuids.add(cid);
      scraped++;

      // Save individual .md file
      if (record.sms_body) {
        const datePart = record.date || 'no-date';
        const namePart = sanitize(record.name);
        const mdPath = path.join(SMS_DIR, `${datePart}_${namePart}.md`);
        const segStr = record.segment ? ` | **Segment:** ${record.segment}` : '';
        const md = `# SMS: ${record.name}
- **Date:** ${record.date || 'N/A'}${segStr}
- **Sent:** ${record.sent.toLocaleString()} | **Clicks:** ${record.clicks.toLocaleString()} | **UCTR:** ${record.uctr}%
- **Orders:** ${record.orders} | **Revenue:** $${record.revenue.toLocaleString()}

## Message
${record.sms_body}
`;
        fs.writeFileSync(mdPath, md, 'utf-8');
      }

      // Incremental save every 15
      if (scraped % 15 === 0) {
        saveJSON(RAW_FILE, results);
        console.log(`  💾 Saved progress (${results.length} total)`);
      }

    } catch (e) {
      console.log(`  ❌ Error: ${e.message}`);
    }
  }

  // ── Step 5: Final save ──
  saveJSON(RAW_FILE, results);

  // Generate summary
  const summaryLines = [
    '# Postscript SMS Summary — Skullette',
    '',
    `*Scraped: ${new Date().toISOString().substring(0, 16)}*`,
    '',
    `**Total SMS Campaigns:** ${results.length}`,
    '',
    '---',
    '',
    '| Date | Campaign | Segment | Sent | UCTR | Revenue |',
    '|------|----------|---------|------|------|---------|',
  ];
  for (const r of results.sort((a, b) => (b.date || '').localeCompare(a.date || ''))) {
    summaryLines.push(`| ${r.date || 'N/A'} | ${r.name?.substring(0, 40) || '?'} | ${r.segment || '?'} | ${r.sent.toLocaleString()} | ${r.uctr}% | $${r.revenue.toLocaleString()} |`);
  }
  fs.writeFileSync(SUMMARY_FILE, summaryLines.join('\n'), 'utf-8');

  console.log(`\n═══════════════════════════════════════`);
  console.log(`  ✓ Scraped ${scraped} new campaigns`);
  console.log(`  ✓ Total: ${results.length} campaigns`);
  console.log(`  ✓ Raw data: ${RAW_FILE}`);
  console.log(`  ✓ SMS files: ${SMS_DIR}`);
  console.log(`  ✓ Summary: ${SUMMARY_FILE}`);
  console.log(`═══════════════════════════════════════`);

  await browser.close();
}

main().catch(e => {
  console.error('Fatal error:', e);
  process.exit(1);
});
