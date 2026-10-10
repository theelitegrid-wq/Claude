"""Render the company pages: about, contact, pricing, work, hub pages, legal pages and 404."""
import pathlib

from company import ABOUT, CONTACT, EMAIL, NOT_FOUND, PRICING, PRIVACY, TERMS, UPDATED, WORK
from content import BRAND, GUIDES, INDUSTRIES, SERVICES, SITE
from pages import LASTMOD, crumbs, cta, document, esc, faq_html, hero, schema_crumbs, schema_faq


def webpage(url, kind, name, desc):
    return {"@type": kind, "@id": url, "url": url, "name": name, "description": desc, "isPartOf": {"@id": SITE + "/#website"}, "inLanguage": "en"}


def about():
    url = f"{SITE}/about/"
    trail = [("Home", "/"), ("About", None)]
    story = "".join(f"<p>{esc(p)}</p>" for p in ABOUT["story"])
    prin = "".join(f'<article class="card"><h3>{esc(t)}</h3><p>{esc(d)}</p></article>' for t, d in ABOUT["principles"])
    svc = "".join(f'<li><a href="/{s["slug"]}/">{esc(s["keyword"].capitalize())}</a></li>' for s in SERVICES)
    body = (hero(trail, "About", ABOUT["h1"], ABOUT["lede"], '<a class="btn btn-glass" href="/work/">See the work</a>') +
            f'<section class="sec"><div class="wrap split"><div class="prose"><span class="kick">The story</span><h2>Why I started Abdullah Automations</h2>{story}</div>'
            f'<div class="card founder"><span class="kick">Founder</span><h3>Abdullah</h3><p>Founder of {BRAND}. Designs and builds every AI agent, automation and website personally.</p>'
            f'<ul class="links-list">{svc}</ul><p class="mail-line">Email: <a href="mailto:{EMAIL}">{EMAIL}</a></p></div></div></section>'
            f'<section class="sec alt"><div class="wrap"><span class="kick">How I work</span><h2>Four promises to every client</h2><div class="cards two">{prin}</div></div></section>'
            + cta())
    graph = [webpage(url, "AboutPage", ABOUT["title"], ABOUT["desc"]) | {"about": {"@id": SITE + "/#business"}}, schema_crumbs(trail, url)]
    return "about/index.html", document(url=url, title=ABOUT["title"], desc=ABOUT["desc"], body=body, graph=graph)


def contact():
    url = f"{SITE}/contact/"
    trail = [("Home", "/"), ("Contact", None)]
    steps = "".join(f'<li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for t, d in CONTACT["expect"])
    opts = "".join(f"<option>{esc(x)}</option>" for x in ["AI agent", "AI automation", "New website", "Growth system (all three)", "Not sure yet"])
    inds = "".join(f"<option>{esc(i['short'])}</option>" for i in INDUSTRIES) + "<option>Something else</option>"
    body = (hero(trail, "Contact", CONTACT["h1"], CONTACT["lede"]).replace('<a class="btn btn-gold" href="/contact/">Book a free strategy call</a>', f'<a class="btn btn-gold" href="mailto:{EMAIL}">Email {EMAIL}</a>') +
            f'''<section class="sec"><div class="wrap split">
<form class="card form" id="contactForm" novalidate>
  <h2>Send a message</h2>
  <div class="f"><label for="c-name">Your name</label><input id="c-name" name="name" autocomplete="name" required></div>
  <div class="f"><label for="c-email">Email</label><input id="c-email" name="email" type="email" autocomplete="email" required></div>
  <div class="f"><label for="c-biz">Business name</label><input id="c-biz" name="business" autocomplete="organization"></div>
  <div class="f two"><div><label for="c-need">I'm interested in</label><select id="c-need">{opts}</select></div><div><label for="c-ind">Industry</label><select id="c-ind">{inds}</select></div></div>
  <div class="f"><label for="c-msg">How can I help?</label><textarea id="c-msg" rows="5" placeholder="For example: we miss calls after 6 p.m. and want online booking"></textarea></div>
  <button class="btn btn-gold" type="submit">Send message</button>
  <p class="note" id="c-note">This opens your email app with your message ready to send to {EMAIL}.</p>
</form>
<div><span class="kick">What happens next</span><h2>Three simple steps</h2><ol class="steps vertical">{steps}</ol>
<div class="card"><h3>Prefer email?</h3><p>Write to <a href="mailto:{EMAIL}">{EMAIL}</a>. I reply within one working day.</p></div></div>
</div></section>
<script>
document.getElementById('contactForm').addEventListener('submit', function (e) {{
  e.preventDefault();
  var v = function (id) {{ return document.getElementById(id).value.trim(); }};
  var name = document.getElementById('c-name'), mail = document.getElementById('c-email');
  var bad = [name, mail].filter(function (f) {{ return !f.value.trim() || !f.checkValidity(); }});
  [name, mail].forEach(function (f) {{ f.classList.toggle('bad', bad.indexOf(f) > -1); }});
  if (bad.length) {{ bad[0].focus(); return; }}
  var body = 'Name: ' + v('c-name') + '\\nEmail: ' + v('c-email') + '\\nBusiness: ' + (v('c-biz') || '-') + '\\nInterested in: ' + v('c-need') + '\\nIndustry: ' + v('c-ind') + '\\n\\n' + (v('c-msg') || 'I would like a free strategy call.');
  window.location.href = 'mailto:{EMAIL}?subject=' + encodeURIComponent('Enquiry from ' + v('c-name')) + '&body=' + encodeURIComponent(body);
  document.getElementById('c-note').textContent = 'Your email app should open now. If it does not, email {EMAIL} directly.';
}});
</script>''' + faq_html([
                ("How quickly will you reply?", "Within one working day, usually much sooner."),
                ("Is the strategy call really free?", "Yes. It's a 30-minute video call to understand your business and suggest next steps. There's no obligation to hire me."),
                ("Do you work with businesses outside my country?", "Yes. I work with clients remotely around the world, and calls are booked at a time that suits your time zone."),
            ]))
    graph = [webpage(url, "ContactPage", CONTACT["title"], CONTACT["desc"]) | {"about": {"@id": SITE + "/#business"}}, schema_crumbs(trail, url)]
    return "contact/index.html", document(url=url, title=CONTACT["title"], desc=CONTACT["desc"], body=body, graph=graph)


def pricing():
    url = f"{SITE}/pricing/"
    trail = [("Home", "/"), ("Pricing", None)]
    plans = ""
    for p in PRICING["plans"]:
        items = "".join(f"<li>{esc(x)}</li>" for x in p["items"])
        tag = '<span class="tag">Most chosen</span>' if p.get("feat") else ""
        plans += (f'<article class="plan{" feat" if p.get("feat") else ""}">{tag}<h3>{esc(p["name"])}</h3><div class="cost">{p["label"]} <small>{esc(p["per"])}</small></div>'
                  f'<p>{esc(p["for"])}</p><ul class="ticks">{items}</ul><a class="btn btn-gold" href="/contact/">{esc(p["cta"])}</a></article>')
    adds = "".join(f'<tr><th scope="row">{esc(n)}</th><td>{esc(pr)}</td><td>{esc(d)}</td></tr>' for n, pr, d in PRICING["addons"])
    body = (hero(trail, "Pricing", PRICING["h1"], PRICING["lede"]) +
            f'<section class="sec"><div class="wrap"><div class="plans">{plans}</div></div></section>'
            f'<section class="sec alt"><div class="wrap"><span class="kick">Add-ons</span><h2>Other services and care plans</h2><div class="table-wrap"><table><thead><tr><th scope="col">Service</th><th scope="col">Price</th><th scope="col">What it includes</th></tr></thead><tbody>{adds}</tbody></table></div>'
            f'<p class="also">Not sure what it would cost for your business? Read <a href="/guides/how-much-does-ai-automation-cost/">how much AI automation costs</a> or <a href="/contact/">ask for a fixed quote</a>.</p></div></section>'
            + faq_html(PRICING["faqs"]) + cta())
    offers = [{"@type": "Offer", "name": p["name"], "price": p["price"], "priceCurrency": "USD", "description": p["for"], "url": url} for p in PRICING["plans"]]
    graph = [webpage(url, "WebPage", PRICING["title"], PRICING["desc"]) | {"mainEntity": {"@type": "OfferCatalog", "name": "Abdullah Automations pricing", "itemListElement": offers}},
             schema_crumbs(trail, url), schema_faq(PRICING["faqs"], url)]
    return "pricing/index.html", document(url=url, title=PRICING["title"], desc=PRICING["desc"], body=body, graph=graph)


def work():
    url = f"{SITE}/work/"
    trail = [("Home", "/"), ("Work", None)]
    items = "".join(
        f'<article class="work-item"><a class="shot" href="/demos/{slug}.html"><img src="/assets/work/{slug}.jpg" width="1200" height="750" loading="lazy" decoding="async" alt="Homepage of the {esc(name)} concept website, a {esc(kind.lower())} site with an AI assistant"></a>'
        f'<div><span class="kick">{esc(kind)}</span><h2>{esc(name)}</h2><p>{esc(d)}</p><div class="row"><a class="btn btn-gold" href="/demos/{slug}.html">Open the live demo</a><a class="text-link" href="{page}">AI automation for {esc(kind.lower())}</a></div></div></article>'
        for slug, name, kind, d, page in WORK["items"])
    body = (hero(trail, "Work", WORK["h1"], WORK["lede"]) +
            f'<section class="sec"><div class="wrap work">{items}</div></section>' + cta("Want a site like these for your business, with an AI agent that books customers for you? Book a free strategy call."))
    graph = [webpage(url, "CollectionPage", WORK["title"], WORK["desc"]) | {"mainEntity": {"@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": n + 1, "name": name, "url": f"{SITE}/demos/{slug}.html"} for n, (slug, name, _, _, _) in enumerate(WORK["items"])]}},
        schema_crumbs(trail, url)]
    return "work/index.html", document(url=url, title=WORK["title"], desc=WORK["desc"], body=body, graph=graph)


def hub(slug, kick, title, desc, h1, lede, cards):
    url = f"{SITE}/{slug}/"
    trail = [("Home", "/"), (kick, None)]
    grid = "".join(f'<a class="card link-card" href="{u}"><h2>{esc(t)}</h2><p>{esc(d)}</p><span class="text-link">{esc(more)}</span></a>' for u, t, d, more in cards)
    body = hero(trail, kick, h1, lede) + f'<section class="sec"><div class="wrap"><div class="cards hub{" three" if len(cards) % 3 == 0 and len(cards) < 6 else ""}">{grid}</div></div></section>' + cta()
    graph = [webpage(url, "CollectionPage", title, desc) | {"mainEntity": {"@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": n + 1, "name": t, "url": SITE + u} for n, (u, t, _, _) in enumerate(cards)]}}, schema_crumbs(trail, url)]
    return f"{slug}/index.html", document(url=url, title=title, desc=desc, body=body, graph=graph)


def hubs():
    return [
        hub("services", "Services", "Services: AI Agents, AI Automation & Websites",
            "AI agents, AI automation and premium website design services from Abdullah Automations. Fixed-price projects for service businesses. See what each includes.",
            "Services", "Three services that work on their own or together as one system: a website that brings customers in, an AI agent that talks to them, and automations that make sure nothing gets dropped.",
            [(f'/{s["slug"]}/', s["keyword"].capitalize(), s["lede"], "See what's included") for s in SERVICES]),
        hub("industries", "Industries", "AI Automation by Industry | Abdullah Automations",
            "See how AI agents and automation work for dental clinics, real estate, restaurants, e-commerce, law firms, gyms, home services and salons.",
            "AI automation for your industry", "Every industry loses customers in different places. Pick yours to see the common problems, what an AI agent does about them and the tools it connects to.",
            [(f'/ai-automation-for/{i["slug"]}/', i["h1"].replace("AI automation for ", "").capitalize(), i["lede"], f"AI automation for {i['name']}") for i in INDUSTRIES]),
        hub("guides", "Guides", "AI Automation Guides for Small Businesses",
            "Plain-English guides to AI automation and AI agents for small businesses: what they are, how they compare to chatbots and what they cost.",
            "Guides", "Plain-English guides for business owners who want to understand AI automation before they spend money on it.",
            [(f'/guides/{g["slug"]}/', g["h1"], g["lede"], "Read the guide") for g in GUIDES]),
    ]


def legal(slug, data):
    url = f"{SITE}/{slug}/"
    trail = [("Home", "/"), (data["h1"].capitalize(), None)]
    secs = "".join(f'<h2>{esc(h)}</h2>' + "".join(f"<p>{p}</p>" for p in ps) for h, ps in data["sections"])
    body = (f'<section class="hero guide-hero"><div class="wrap narrow">{crumbs(trail)}<span class="kick">Legal</span><h1>{esc(data["h1"].capitalize())}</h1>'
            f'<p class="byline">Last updated <time datetime="{LASTMOD}">{UPDATED}</time></p></div></section>'
            f'<section class="sec"><div class="wrap narrow"><article class="prose article">{secs}</article></div></section>')
    graph = [webpage(url, "WebPage", data["title"], data["desc"]), schema_crumbs(trail, url)]
    return f"{slug}/index.html", document(url=url, title=data["title"], desc=data["desc"], body=body, graph=graph)


def not_found():
    links = [("/", "Homepage"), ("/services/", "Services"), ("/ai-agents/", "AI agents"), ("/ai-automation-services/", "AI automation services"),
             ("/website-design-services/", "Website design"), ("/pricing/", "Pricing"), ("/contact/", "Contact")]
    li = "".join(f'<a class="chip" href="{u}">{esc(t)}</a>' for u, t in links)
    body = (f'<section class="hero"><div class="wrap"><span class="kick">Error 404</span><h1>{esc(NOT_FOUND["h1"])}</h1><p class="lede">{esc(NOT_FOUND["lede"])}</p>'
            f'<div class="row"><a class="btn btn-gold" href="/">Go to the homepage</a></div></div></section><section class="sec"><div class="wrap"><div class="chips">{li}</div></div></section>')
    doc = document(url=f"{SITE}/404.html", title=NOT_FOUND["title"], desc=NOT_FOUND["desc"], body=body, graph=[])
    doc = doc.replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
    doc = doc.replace(f'<link rel="canonical" href="{SITE}/404.html">\n', "")
    return "404.html", doc


def render_company(out: pathlib.Path):
    """Write the company pages and return the URLs that belong in the sitemap."""
    urls = []
    pages = [about(), contact(), pricing(), work(), *hubs(), legal("privacy-policy", PRIVACY), legal("terms", TERMS)]
    for rel, doc in pages + [not_found()]:
        path = out / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(doc, encoding="utf-8")
    for rel, _ in pages:
        urls.append(f"{SITE}/{rel[:-len('index.html')]}")
    return urls
