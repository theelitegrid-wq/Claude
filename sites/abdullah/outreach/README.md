# Free outreach system: setup guide

A Google Sheet that finds no one for you, but does everything after that: it sends personal emails from your Gmail, follows up on day 3 and day 7, stops when someone replies, and gives you one-click WhatsApp messages. It costs nothing and takes about 10 minutes to set up.

**You need:** a Google account (Gmail). Nothing to install.

---

## Setup (10 minutes)

1. Go to **sheets.new** to create a new Google Sheet. Name it "Outreach".
2. Click **Extensions → Apps Script**.
3. Delete everything in the code box, then paste the full contents of **`Code.gs`**.
4. At the top of the code, fill in **`POSTAL_ADDRESS`** with your business address. Anti-spam laws in many countries require it in sales emails.
5. Click **Save** (the disk icon) and close the Apps Script tab.
6. Reload the Google Sheet. A new **Outreach** menu appears at the top.
7. Click **Outreach → 1. Set up sheets**.
   - Google asks for permission the first time. Click **Continue**, choose your account, then **Advanced → Go to Outreach (unsafe) → Allow**.
   - The "unsafe" warning appears because you wrote the script yourself and Google hasn't reviewed it. The script only works inside your own Gmail and this sheet.
8. Click **Outreach → 2. Send a test email to myself**. Check your inbox: you should have 3 emails, one for each step.
9. When you're happy, click **Outreach → Turn autopilot ON**. It now runs every morning by itself.

### Optional: send from info@abdullahautomations.com

Replies already go to `info@abdullahautomations.com`. To also send *from* that address:
1. In Gmail, open **Settings → Accounts → Send mail as → Add another email address**.
2. Enter your Hostinger email details (from hPanel → Emails).
3. Make it the default address.

---

## How to use it

### The tabs

| Tab | What it's for |
|---|---|
| **Leads** | One row per business. Fill in first name, business, email and/or phone, industry, city, and a short personal note. |
| **Industries** | The problem and demo link used for each industry. Edit freely. |
| **Templates** | The 3 emails and the WhatsApp message. Edit the wording any time. |
| **Log** | Every email sent, every reply, bounce and unsubscribe. |
| **Dashboard** | Totals and your reply rate. |

### Statuses

- **New:** not contacted yet.
- **Contacted:** in the sequence.
- **Replied:** they wrote back, and the sequence stopped automatically. Reply to them yourself!
- **Call booked, Won, Lost:** set these yourself as the conversation moves on.
- **Unsubscribed / Bounced:** set automatically; never contacted again.

### The personal note is what gets replies

One honest line about *their* business makes the email feel personal and doubles reply rates. For example:
- "Saw your new Saturday opening hours on Google."
- "Your 4.8 rating with 200 reviews is impressive."
- "Loved the before-and-after photos on your Instagram."

If you leave it blank, the email still reads naturally.

### WhatsApp (often works better than email for local businesses)

1. Add phone numbers with the country code (for example `971501234567`).
2. Click **Outreach → Make WhatsApp links**.
3. Click **Open WhatsApp** in a row. The message is already written; check it and press send.

Send WhatsApp messages by hand, a few at a time. Mass messaging gets numbers banned.

---

## Where to find leads (free)

1. **Google Maps.** Search "[dentist / salon / plumber / real estate agency] in [your city]". The best prospects have:
   - few or old reviews
   - a dated website, or none
   - no online booking
   - reviews mentioning "hard to reach" or "no one answered"
2. **Their website and socials.** The contact page, Facebook "About" and Instagram bio usually show an email and a WhatsApp number.
3. **Speed it up (optional, free):** the Chrome extension **Instant Data Scraper** copies a page of Google Maps results into a spreadsheet in one click. Paste the useful columns into the Leads tab.
4. **Your own network.** Anyone you know who owns a business. Warm leads convert best.

---

## Your 20-minute daily routine

| Minutes | Task |
|---|---|
| 10 | Add 20 new leads to the Leads tab, each with a one-line personal note |
| 5 | Open WhatsApp links for 5 to 10 leads with phone numbers and send them |
| 5 | Check the Leads tab for anyone marked **Replied** and answer them personally |

Autopilot sends the emails and follow-ups each morning.

**What to expect:** with 20 new leads a day and good personal notes, a reply rate of 5 to 10% is realistic. That's 1 or 2 conversations a day, and usually a first client within the first couple of weeks.

---

## Rules that keep your Gmail safe

- **Start slowly.** Keep `DAILY_LIMIT` at 20 for the first two weeks, then raise it to 30 or 40. Free Gmail allows about 100 emails a day in total.
- **Be personal and relevant.** Contact businesses that could genuinely use the service, and never buy email lists.
- **Always let people opt out.** Every email ends with "Reply stop", and the system respects it automatically.
- **Check the law where you send.** Business-to-business cold email is allowed in most places when it's relevant and has an opt-out. In the EU and UK, contact businesses on their business addresses only and keep the message relevant to their work.
