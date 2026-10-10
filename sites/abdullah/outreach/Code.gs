/**
 * Abdullah Automations: free outreach system for Google Sheets + Gmail.
 *
 * Setup: create a Google Sheet, open Extensions > Apps Script, paste this file,
 * save, reload the sheet, then click Outreach > 1. Set up sheets.
 *
 * What it does
 *  - Leads tab: your prospects and their status (a simple CRM)
 *  - Sends a personalised 3-step email sequence from your Gmail (day 0, 3, 7)
 *  - Stops automatically when a lead replies, says "stop" or the email bounces
 *  - Builds one-click WhatsApp messages for every lead with a phone number
 *  - Optional autopilot: runs every morning by itself
 */

const CONFIG = {
  YOUR_NAME: 'Abdullah',
  COMPANY: 'Abdullah Automations',
  WEBSITE: 'https://abdullahautomations.com',
  REPLY_TO: 'info@abdullahautomations.com',
  // Required by anti-spam laws in many countries (e.g. US CAN-SPAM). Put your business address here.
  POSTAL_ADDRESS: '',
  // Keep this low so Gmail trusts you. Start at 20 a day, raise slowly to 40.
  DAILY_LIMIT: 20,
  // Days to wait before each follow-up (step 2 after step 1, step 3 after step 2).
  FOLLOW_UP_GAPS: [3, 4],
  AUTOPILOT_HOUR: 9,
};

const SHEETS = { LEADS: 'Leads', TEMPLATES: 'Templates', INDUSTRIES: 'Industries', LOG: 'Log', DASHBOARD: 'Dashboard' };
const COLS = ['First name', 'Business', 'Email', 'Phone (with country code)', 'Industry', 'City', 'Personal note', 'Status', 'Step', 'Last sent', 'Next send', 'WhatsApp', 'Notes'];
const C = Object.fromEntries(COLS.map((name, i) => [name, i]));
const STATUSES = ['New', 'Contacted', 'Replied', 'Call booked', 'Won', 'Lost', 'Unsubscribed', 'Bounced'];
const ACTIVE = ['New', 'Contacted'];

/* ---------- Menu ---------- */

function onOpen() {
  SpreadsheetApp.getUi().createMenu('Outreach')
    .addItem('1. Set up sheets', 'setup')
    .addItem('2. Send a test email to myself', 'sendTest')
    .addSeparator()
    .addItem('Check replies now', 'checkReplies')
    .addItem("Send today's emails now", 'sendDue')
    .addItem('Make WhatsApp links', 'makeWhatsAppLinks')
    .addSeparator()
    .addItem('Turn autopilot ON (every morning)', 'autopilotOn')
    .addItem('Turn autopilot OFF', 'autopilotOff')
    .addToUi();
}

/* ---------- Setup ---------- */

function setup() {
  const ss = SpreadsheetApp.getActive();
  const leads = getOrCreate_(ss, SHEETS.LEADS);
  if (leads.getLastRow() === 0) {
    leads.appendRow(COLS);
    leads.appendRow(['Sara', 'Brightline Dental', Session.getActiveUser().getEmail(), '', 'Dental clinic', 'Dubai',
      'Loved the photos of your new treatment rooms on Instagram.', 'New', 0, '', '', '', 'Example lead: replace with real ones']);
  }
  styleHeader_(leads, COLS.length);
  leads.getRange(2, C['Status'] + 1, 1000, 1).setDataValidation(
    SpreadsheetApp.newDataValidation().requireValueInList(STATUSES, true).build());
  leads.getRange(2, C['Industry'] + 1, 1000, 1).setDataValidation(
    SpreadsheetApp.newDataValidation().requireValueInRange(ss.getRange(SHEETS.INDUSTRIES + '!A2:A50'), true).setAllowInvalid(true).build());
  leads.setColumnWidths(1, COLS.length, 150);
  leads.setColumnWidth(C['Personal note'] + 1, 280);

  const ind = getOrCreate_(ss, SHEETS.INDUSTRIES);
  if (ind.getLastRow() === 0) {
    ind.appendRow(['Industry', 'Plural', 'Pain', 'Demo link']);
    INDUSTRY_ROWS.forEach(r => ind.appendRow(r));
  }
  styleHeader_(ind, 4);
  ind.setColumnWidth(3, 460); ind.setColumnWidth(4, 360);

  const tpl = getOrCreate_(ss, SHEETS.TEMPLATES);
  if (tpl.getLastRow() === 0) {
    tpl.appendRow(['Step', 'Subject', 'Body']);
    TEMPLATE_ROWS.forEach(r => tpl.appendRow(r));
  }
  styleHeader_(tpl, 3);
  tpl.setColumnWidth(2, 260); tpl.setColumnWidth(3, 640);
  tpl.getRange('C:C').setWrap(true);

  const log = getOrCreate_(ss, SHEETS.LOG);
  if (log.getLastRow() === 0) log.appendRow(['Time', 'Email', 'Business', 'Action', 'Detail']);
  styleHeader_(log, 5);

  const dash = getOrCreate_(ss, SHEETS.DASHBOARD);
  dash.clear();
  dash.getRange('A1').setValue('Outreach dashboard').setFontSize(16).setFontWeight('bold');
  const L = SHEETS.LEADS, col = letter_(C['Status'] + 1);
  const rows = [['Total leads', `=COUNTA(${L}!C2:C)`]].concat(
    STATUSES.map(s => [s, `=COUNTIF(${L}!${col}2:${col},"${s}")`]),
    [['Emails sent (all time)', `=COUNTIF(${SHEETS.LOG}!D2:D,"Sent*")`],
     ['Reply rate', `=IFERROR((B6+B7+B8+B9+B10)/(B5+B6+B7+B8+B9+B10),0)`]]);
  dash.getRange(3, 1, rows.length, 2).setValues(rows);
  dash.getRange('B' + (rows.length + 2)).setNumberFormat('0%');
  dash.setColumnWidth(1, 220);

  ss.setActiveSheet(leads);
  SpreadsheetApp.getUi().alert('Ready!\n\n1. Fill in your POSTAL_ADDRESS in the script (top of the file).\n2. Add your leads in the Leads tab.\n3. Use Outreach > Send a test email to myself.\n4. Then Outreach > Turn autopilot ON.');
}

/* ---------- Sending ---------- */

function sendTest() {
  const me = Session.getActiveUser().getEmail();
  const lead = { 'First name': 'Sara', 'Business': 'Brightline Dental', 'Industry': 'Dental clinic', 'City': 'Dubai',
    'Personal note': 'Loved the photos of your new treatment rooms on Instagram.' };
  const tpl = getTemplates_();
  const ind = getIndustries_();
  [1, 2, 3].forEach(step => {
    const msg = render_(tpl[step], lead, ind);
    sendEmail_(me, '[TEST step ' + step + '] ' + msg.subject, msg.body);
  });
  SpreadsheetApp.getUi().alert('Sent 3 test emails (one per step) to ' + me + '. Check your inbox.');
}

function sendDue() {
  checkReplies();
  const sh = SpreadsheetApp.getActive().getSheetByName(SHEETS.LEADS);
  const data = sh.getDataRange().getValues();
  const tpl = getTemplates_();
  const ind = getIndustries_();
  const today = startOfDay_(new Date());
  let budget = Math.min(CONFIG.DAILY_LIMIT, MailApp.getRemainingDailyQuota());
  let sent = 0;

  for (let r = 1; r < data.length && budget > 0; r++) {
    const row = data[r];
    const lead = toObj_(row);
    const email = String(lead['Email'] || '').trim();
    const status = lead['Status'] || 'New';
    const step = Number(lead['Step'] || 0);
    if (!email || !ACTIVE.includes(status) || step >= 3) continue;
    const next = lead['Next send'] ? startOfDay_(new Date(lead['Next send'])) : today;
    if (next > today) continue;

    const msg = render_(tpl[step + 1], lead, ind);
    if (step > 0) msg.subject = 'Re: ' + render_(tpl[1], lead, ind).subject;
    try {
      sendEmail_(email, msg.subject, msg.body);
    } catch (e) {
      log_(email, lead['Business'], 'Error', String(e));
      continue;
    }
    const newStep = step + 1;
    const gap = CONFIG.FOLLOW_UP_GAPS[newStep - 1];
    row[C['Status']] = 'Contacted';
    row[C['Step']] = newStep;
    row[C['Last sent']] = new Date();
    row[C['Next send']] = gap ? addDays_(today, gap) : '';
    sh.getRange(r + 1, 1, 1, row.length).setValues([row]);
    log_(email, lead['Business'], 'Sent step ' + newStep, msg.subject);
    sent++; budget--;
    Utilities.sleep(1500 + Math.floor(Math.random() * 2500));
  }
  return sent;
}

/* ---------- Replies, unsubscribes and bounces ---------- */

function checkReplies() {
  const sh = SpreadsheetApp.getActive().getSheetByName(SHEETS.LEADS);
  const data = sh.getDataRange().getValues();
  const me = Session.getActiveUser().getEmail().toLowerCase();
  for (let r = 1; r < data.length; r++) {
    const lead = toObj_(data[r]);
    const email = String(lead['Email'] || '').trim();
    if (!email || lead['Status'] !== 'Contacted' || email.toLowerCase() === me) continue;

    const bounce = GmailApp.search(`from:(mailer-daemon OR postmaster) "${email}" newer_than:30d`, 0, 1);
    if (bounce.length) { setStatus_(sh, r, 'Bounced', email, lead['Business']); continue; }

    const replies = GmailApp.search(`from:${email} newer_than:60d`, 0, 5);
    if (!replies.length) continue;
    const text = replies.map(t => t.getMessages().filter(m => m.getFrom().toLowerCase().includes(email.toLowerCase()))
      .map(m => m.getPlainBody().slice(0, 400)).join(' ')).join(' ').toLowerCase();
    const optOut = /\b(stop|unsubscribe|remove me|not interested|no thanks)\b/.test(text);
    setStatus_(sh, r, optOut ? 'Unsubscribed' : 'Replied', email, lead['Business']);
  }
}

/* ---------- WhatsApp ---------- */

function makeWhatsAppLinks() {
  const sh = SpreadsheetApp.getActive().getSheetByName(SHEETS.LEADS);
  const data = sh.getDataRange().getValues();
  const tpl = getTemplates_();
  const ind = getIndustries_();
  let made = 0;
  for (let r = 1; r < data.length; r++) {
    const lead = toObj_(data[r]);
    const phone = String(lead['Phone (with country code)'] || '').replace(/[^\d]/g, '');
    if (!phone || ['Unsubscribed', 'Won', 'Lost'].includes(lead['Status'])) continue;
    const text = render_(tpl['WhatsApp'], lead, ind).body;
    const url = 'https://wa.me/' + phone + '?text=' + encodeURIComponent(text);
    sh.getRange(r + 1, C['WhatsApp'] + 1).setFormula('=HYPERLINK("' + url + '","Open WhatsApp")');
    made++;
  }
  SpreadsheetApp.getUi().alert(made + ' WhatsApp links ready. Click "Open WhatsApp" in a row, check the message and press send.');
}

/* ---------- Autopilot ---------- */

function autopilotOn() {
  autopilotOff();
  ScriptApp.newTrigger('dailyRun').timeBased().everyDays(1).atHour(CONFIG.AUTOPILOT_HOUR).create();
  SpreadsheetApp.getUi().alert('Autopilot is ON. Every morning around ' + CONFIG.AUTOPILOT_HOUR + ':00 it checks replies and sends due emails.');
}

function autopilotOff() {
  ScriptApp.getProjectTriggers().filter(t => t.getHandlerFunction() === 'dailyRun').forEach(t => ScriptApp.deleteTrigger(t));
}

function dailyRun() {
  const sent = sendDue();
  log_('', '', 'Autopilot', sent + ' emails sent');
}

/* ---------- Templates ---------- */

function render_(tpl, lead, industries) {
  if (!tpl) throw new Error('Missing template. Run Outreach > 1. Set up sheets.');
  const info = industries[String(lead['Industry'] || '').toLowerCase()] || industries['other'] || {};
  const vars = {
    first_name: String(lead['First name'] || '').trim() || 'there',
    business: String(lead['Business'] || '').trim() || 'your business',
    city: String(lead['City'] || '').trim(),
    industry: String(lead['Industry'] || 'business').toLowerCase(),
    industry_plural: info.plural || 'businesses like yours',
    pain: info.pain || 'missed calls and slow replies quietly send customers to competitors',
    demo_link: info.demo || CONFIG.WEBSITE + '/work/',
    personal_note: String(lead['Personal note'] || '').trim(),
    your_name: CONFIG.YOUR_NAME,
    company: CONFIG.COMPANY,
    website: CONFIG.WEBSITE,
  };
  const fill = s => String(s || '').replace(/\{\{\s*(\w+)\s*\}\}/g, (_, k) => (k in vars ? vars[k] : ''));
  let body = fill(tpl.body).replace(/\n{3,}/g, '\n\n').replace(/^\s*\n/, '');
  const footer = [CONFIG.POSTAL_ADDRESS, 'Not relevant? Reply "stop" and I won\'t email again.'].filter(Boolean).join('\n');
  if (tpl.step !== 'WhatsApp') body += '\n\n--\n' + footer;
  return { subject: fill(tpl.subject), body: body };
}

function getTemplates_() {
  const rows = SpreadsheetApp.getActive().getSheetByName(SHEETS.TEMPLATES).getDataRange().getValues().slice(1);
  const out = {};
  rows.forEach(([step, subject, body]) => { if (step !== '') out[step] = { step: step, subject: subject, body: body }; });
  return out;
}

function getIndustries_() {
  const rows = SpreadsheetApp.getActive().getSheetByName(SHEETS.INDUSTRIES).getDataRange().getValues().slice(1);
  const out = {};
  rows.forEach(([name, plural, pain, demo]) => { if (name) out[String(name).toLowerCase()] = { plural: plural, pain: pain, demo: demo }; });
  return out;
}

/* ---------- Helpers ---------- */

function sendEmail_(to, subject, body) {
  GmailApp.sendEmail(to, subject, body, { name: CONFIG.YOUR_NAME + ' | ' + CONFIG.COMPANY, replyTo: CONFIG.REPLY_TO });
}

function setStatus_(sh, r, status, email, business) {
  sh.getRange(r + 1, C['Status'] + 1).setValue(status);
  sh.getRange(r + 1, C['Next send'] + 1).setValue('');
  log_(email, business, status, '');
}

function log_(email, business, action, detail) {
  const sh = SpreadsheetApp.getActive().getSheetByName(SHEETS.LOG);
  if (sh) sh.appendRow([new Date(), email, business || '', action, detail || '']);
}

function toObj_(row) { const o = {}; COLS.forEach((name, i) => { o[name] = row[i]; }); return o; }
function getOrCreate_(ss, name) { return ss.getSheetByName(name) || ss.insertSheet(name); }
function startOfDay_(d) { const x = new Date(d); x.setHours(0, 0, 0, 0); return x; }
function addDays_(d, n) { const x = new Date(d); x.setDate(x.getDate() + n); return x; }
function letter_(n) { let s = ''; while (n > 0) { const m = (n - 1) % 26; s = String.fromCharCode(65 + m) + s; n = Math.floor((n - 1) / 26); } return s; }
function styleHeader_(sh, n) {
  sh.getRange(1, 1, 1, n).setFontWeight('bold').setBackground('#0a1f5c').setFontColor('#ffffff');
  sh.setFrozenRows(1);
}

/* ---------- Starting content (editable in the sheet after setup) ---------- */

const DEMO = CONFIG.WEBSITE;
const INDUSTRY_ROWS = [
  ['Dental clinic', 'dental clinics', 'patients who reach voicemail usually book with the next clinic on Google', DEMO + '/demos/dental.html'],
  ['Real estate', 'real estate agents', 'the first agent to reply to a new lead usually wins the client', DEMO + '/demos/realestate.html'],
  ['Restaurant', 'restaurants', 'booking requests in DMs and calls during service often go unanswered', DEMO + '/demos/restaurant.html'],
  ['E-commerce', 'online stores', '"where is my order?" messages eat hours and shoppers leave with unanswered questions', DEMO + '/demos/store.html'],
  ['Salon or spa', 'salons', 'booking requests sit in Instagram DMs while the team is busy with clients', DEMO + '/ai-automation-for/salons-spas/'],
  ['Home services', 'trades businesses', 'a missed call while you are on a job is usually a lost job', DEMO + '/ai-automation-for/home-services/'],
  ['Law firm', 'law firms', 'potential clients call several firms and hire the first one that responds properly', DEMO + '/ai-automation-for/law-firms/'],
  ['Gym or fitness', 'gyms and studios', 'trial sign-ups who do not hear back quickly never come in', DEMO + '/ai-automation-for/fitness-studios/'],
  ['Clinic', 'clinics', 'patients who reach voicemail usually book somewhere else', DEMO + '/ai-automation-for/dental-clinics/'],
  ['Other', 'businesses like yours', 'missed calls and slow replies quietly send customers to competitors', DEMO + '/work/'],
];

const TEMPLATE_ROWS = [
  [1, 'Quick question about {{business}}',
   'Hi {{first_name}},\n\n{{personal_note}}\n\nQuick question: what happens when someone calls {{business}} while your team is busy? For most {{industry_plural}}, {{pain}}.\n\nI set up a simple AI assistant that texts back every missed call within seconds, answers common questions and books the customer straight into your calendar, day or night.\n\nHere is a 1-minute demo you can try yourself: {{demo_link}}\n\nIt goes live in 3 days for a one-time $497, with a money-back guarantee if it does not bring you at least one new enquiry in the first 30 days.\n\nWorth a quick 10-minute call this week?\n\n{{your_name}}\n{{company}} | {{website}}'],
  [2, '',
   'Hi {{first_name}},\n\nJust bringing this back to the top of your inbox. Happy to show you the demo live on a short call, or send a 2-minute video if that is easier.\n\nWould that be useful for {{business}}?\n\n{{your_name}}'],
  [3, '',
   'Hi {{first_name}},\n\nI will stop here so I do not crowd your inbox. If missed calls or slow replies ever start costing {{business}} customers, just reply to this email and I will set up the assistant for you.\n\nAll the best,\n{{your_name}}\n{{website}}'],
  ['WhatsApp', '',
   'Hi {{first_name}}, this is {{your_name}} from {{company}}. I help {{industry_plural}} make sure no customer is missed: an AI assistant texts back missed calls in seconds and books them in, 24/7. Here is a 1-minute demo: {{demo_link}} Would it be useful for {{business}}? If not, no worries at all.'],
];
