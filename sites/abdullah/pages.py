"""Render the SEO landing pages (services, industries, guides) into a site folder."""
import html
import json
import pathlib

from content import BRAND, GUIDES, INDUSTRIES, SERVICES, SITE

LASTMOD = "2026-10-09"
FONTS = "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,700&display=swap"


def esc(s):
    return html.escape(s, quote=True)


def page_title(t):
    full = f"{t} | {BRAND}"
    return full if len(full) <= 60 else t


def nav():
    items = [("/services/", "Services"), ("/industries/", "Industries"), ("/work/", "Work"), ("/pricing/", "Pricing"), ("/guides/", "Guides"), ("/about/", "About")]
    links = "".join(f'<a href="{u}">{t}</a>' for u, t in items)
    return f'''<header class="nav">
  <div class="wrap">
    <a class="brand" href="/">Abdullah <small>AUTOMATIONS</small></a>
    <nav class="links" aria-label="Main">{links}</nav>
    <a class="btn btn-gold" href="/contact/">Contact</a>
  </div>
</header>'''


def footer():
    col = lambda items: "".join(f'<li><a href="{u}">{esc(t)}</a></li>' for u, t in items)
    services = [(f'/{s["slug"]}/', s["keyword"].capitalize()) for s in SERVICES]
    industries = [(f'/ai-automation-for/{i["slug"]}/', f'AI automation for {i["name"]}') for i in INDUSTRIES]
    guides = [(f'/guides/{g["slug"]}/', g["h1"].split("?")[0].split(":")[0] + ("?" if "?" in g["h1"] else "")) for g in GUIDES]
    company = [("/about/", "About"), ("/work/", "Work"), ("/pricing/", "Pricing"), ("/contact/", "Contact"), ("/privacy-policy/", "Privacy policy"), ("/terms/", "Terms of service")]
    return f'''<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div><a class="brand" href="/">Abdullah <small>AUTOMATIONS</small></a><p>AI agents, AI automation and premium websites for businesses that don't want to miss a customer.</p><a class="btn btn-gold" href="/contact/">Book a free strategy call</a><p class="mail">Email: <a href="mailto:info@abdullahautomations.com">info@abdullahautomations.com</a></p></div>
      <div><h2>Services</h2><ul>{col(services)}</ul></div>
      <div><h2>Industries</h2><ul>{col(industries)}</ul></div>
      <div><h2>Guides</h2><ul>{col(guides)}</ul></div>
      <div><h2>Company</h2><ul>{col(company)}</ul></div>
    </div>
    <p class="copy">&copy; 2026 {BRAND}. All rights reserved.</p>
  </div>
</footer>'''


def faq_html(faqs):
    items = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs)
    return f'<section class="sec"><div class="wrap faq"><div><span class="kick">FAQ</span><h2>Common questions</h2></div><div>{items}</div></div></section>'


def cta(text="See where an AI agent would win you more customers. Book a free 30-minute strategy call and leave with a plan, whether you hire me or not."):
    return f'''<section class="sec cta-sec"><div class="wrap cta"><div><h2>Ready to stop missing customers?</h2><p>{text}</p></div><a class="btn btn-gold" href="/contact/">Book a free strategy call</a></div></section>'''


def crumbs(trail):
    links = " <span>/</span> ".join(f'<a href="{u}">{esc(t)}</a>' if u else f"<span aria-current=\"page\">{esc(t)}</span>" for t, u in trail)
    return f'<nav class="crumbs" aria-label="Breadcrumb">{links}</nav>'


def schema_crumbs(trail, url):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": t, "item": (SITE + u) if u else url}
        for i, (t, u) in enumerate(trail)]}


def schema_faq(faqs, url):
    return {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def document(*, url, title, desc, body, graph, og_type="website"):
    t = page_title(title)
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(t)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#061440">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{esc(t)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{SITE}/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(t)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE}/og-image.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
{nav()}
<main>
{body}
</main>
{footer()}
</body>
</html>
'''


def hero(trail, kick, h1, lede, extra=""):
    return f'''<section class="hero"><div class="wrap">{crumbs(trail)}<span class="kick">{esc(kick)}</span><h1>{esc(h1)}</h1><p class="lede">{esc(lede)}</p>
<div class="row"><a class="btn btn-gold" href="/contact/">Book a free strategy call</a>{extra}</div></div></section>'''


def service_page(s):
    url = f"{SITE}/{s['slug']}/"
    trail = [("Home", "/"), ("Services", "/services/"), (s["nav"], None)]
    intro = "".join(f'<div class="prose"><h2>{esc(h)}</h2>{"".join(f"<p>{esc(p)}</p>" for p in ps)}</div>' for h, ps in s["sections"])
    feats = "".join(f'<article class="card"><h3>{esc(t)}</h3><p>{esc(d)}</p></article>' for t, d in s["features"])
    steps = "".join(f'<li><h3>{esc(t)}</h3><p>{esc(d)}</p></li>' for t, d in s["steps"])
    inds = "".join(f'<a class="chip" href="/ai-automation-for/{i["slug"]}/">{esc(i["short"])}</a>' for i in INDUSTRIES)
    others = "".join(f'<a class="chip" href="/{o["slug"]}/">{esc(o["keyword"].capitalize())}</a>' for o in SERVICES if o is not s)
    tools = "".join(f"<span>{esc(t)}</span>" for t in s["tools"])
    body = (hero(trail, s["keyword"], s["h1"], s["lede"], '<a class="btn btn-glass" href="/work/">See demo sites</a>') +
            f'<section class="sec"><div class="wrap">{intro}</div></section>'
            f'<section class="sec alt"><div class="wrap"><span class="kick">What\'s included</span><h2>What you get</h2><div class="cards">{feats}</div></div></section>'
            f'<section class="sec dark"><div class="wrap"><span class="kick">How it works</span><h2>From first call to launch</h2><ol class="steps">{steps}</ol></div></section>'
            f'<section class="sec"><div class="wrap split"><div><span class="kick">Pricing</span><h2>Clear, fixed pricing</h2><p class="big">{esc(s["price_note"])}</p><p>Every project starts with a written blueprint and a fixed quote, so you know the full cost before work begins. See all packages on the <a href="/pricing/">pricing section</a>.</p></div>'
            f'<div><span class="kick">Works with</span><h2>Tools I connect</h2><div class="tools">{tools}</div></div></div></section>'
            f'<section class="sec alt"><div class="wrap"><span class="kick">Industries</span><h2>Built for your industry</h2><p>See how {esc(s["keyword"].lower())} works for your type of business:</p><div class="chips">{inds}</div><p class="also">Related services:</p><div class="chips">{others}</div></div></section>'
            + faq_html(s["faqs"]) + cta())
    graph = [
        {"@type": "Service", "@id": url + "#service", "name": s["keyword"].capitalize(), "serviceType": s["keyword"], "description": s["desc"], "url": url,
         "provider": {"@id": SITE + "/#business"}, "areaServed": "Worldwide",
         "offers": {"@type": "Offer", "price": s["price"], "priceCurrency": "USD", "url": url}},
        {"@type": "WebPage", "@id": url, "url": url, "name": page_title(s["title"]), "description": s["desc"], "isPartOf": {"@id": SITE + "/#website"}, "inLanguage": "en"},
        schema_crumbs(trail, url), schema_faq(s["faqs"], url)]
    return f"{s['slug']}/index.html", document(url=url, title=s["title"], desc=s["desc"], body=body, graph=graph)


def industry_page(i):
    url = f"{SITE}/ai-automation-for/{i['slug']}/"
    trail = [("Home", "/"), ("Industries", "/industries/"), (i["short"], None)]
    pains = "".join(f'<article class="card pain"><h3>{esc(t)}</h3><p>{esc(d)}</p></article>' for t, d in i["pains"])
    sols = "".join(f"<li>{esc(x)}</li>" for x in i["solutions"])
    convo = "".join(f'<div class="msg {w}"><span class="who">{"CUSTOMER" if w == "in" else "AI AGENT"}</span>{esc(t)}</div>' for w, t in i["convo"])
    tools = "".join(f"<span>{esc(t)}</span>" for t in i["tools"])
    demo = f'<a class="btn btn-glass" href="{i["demo"]}">Try the demo site</a>' if i["demo"] else ""
    demo_note = (f'<p>Want to see it working? <a href="{i["demo"]}">Open the {esc(i["short"].lower())} demo site</a> and ask the assistant in the corner to book something.</p>' if i["demo"] else "")
    others = "".join(f'<a class="chip" href="/ai-automation-for/{o["slug"]}/">{esc(o["short"])}</a>' for o in INDUSTRIES if o is not i)
    body = (hero(trail, f"AI automation for {i['name']}", i["h1"], i["lede"], demo) +
            f'<section class="sec"><div class="wrap"><span class="kick">The problem</span><h2>Where {esc(i["name"])} lose customers</h2><div class="cards two">{pains}</div></div></section>'
            f'<section class="sec dark"><div class="wrap split"><div><span class="kick">The solution</span><h2>What your AI agent does</h2><ul class="ticks">{sols}</ul>{demo_note}</div>'
            f'<div class="chat" aria-label="Example conversation">{convo}</div></div></section>'
            f'<section class="sec"><div class="wrap split"><div><span class="kick">Integrations</span><h2>Works with your tools</h2><p>The assistant connects to the software {esc(i["name"])} already use, so bookings, leads and messages land where your team expects them.</p><div class="tools">{tools}</div></div>'
            f'<div><span class="kick">Services</span><h2>What I build for you</h2><ul class="links-list"><li><a href="/ai-agents/">AI agents for chat, WhatsApp and phone</a></li><li><a href="/ai-automation-services/">AI automation for follow-ups, reminders and CRM</a></li><li><a href="/website-design-services/">Premium website design</a></li></ul></div></div></section>'
            + faq_html(i["faqs"]) +
            f'<section class="sec alt"><div class="wrap"><span class="kick">Other industries</span><h2>AI automation for other businesses</h2><div class="chips">{others}</div></div></section>'
            + cta())
    graph = [
        {"@type": "Service", "@id": url + "#service", "name": i["h1"], "serviceType": "AI automation", "description": i["desc"], "url": url,
         "provider": {"@id": SITE + "/#business"}, "audience": {"@type": "BusinessAudience", "name": i["name"].capitalize()}, "areaServed": "Worldwide"},
        {"@type": "WebPage", "@id": url, "url": url, "name": page_title(i["title"]), "description": i["desc"], "isPartOf": {"@id": SITE + "/#website"}, "inLanguage": "en"},
        schema_crumbs(trail, url), schema_faq(i["faqs"], url)]
    return f"ai-automation-for/{i['slug']}/index.html", document(url=url, title=i["title"], desc=i["desc"], body=body, graph=graph)


def guide_page(g):
    url = f"{SITE}/guides/{g['slug']}/"
    trail = [("Home", "/"), ("Guides", "/guides/"), (g["h1"].split(":")[0].split("?")[0], None)]
    parts = []
    toc = []
    for n, sec in enumerate(g["body"]):
        h, ps = sec[0], sec[1]
        lst = sec[2] if len(sec) > 2 else []
        sid = f"s{n + 1}"
        toc.append(f'<li><a href="#{sid}">{esc(h)}</a></li>')
        ul = "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in lst) + "</ul>" if lst else ""
        parts.append(f'<h2 id="{sid}">{esc(h)}</h2>' + "".join(f"<p>{p}</p>" for p in ps) + ul)
    more = "".join(f'<li><a href="/guides/{o["slug"]}/">{esc(o["h1"])}</a></li>' for o in GUIDES if o is not g)
    body = (f'<section class="hero guide-hero"><div class="wrap narrow">{crumbs(trail)}<span class="kick">Guide</span><h1>{esc(g["h1"])}</h1><p class="lede">{esc(g["lede"])}</p>'
            f'<p class="byline">By Abdullah, founder of {BRAND}. Updated <time datetime="{LASTMOD}">9 October 2026</time>.</p></div></section>'
            f'<section class="sec"><div class="wrap narrow"><nav class="toc" aria-label="Contents"><strong>In this guide</strong><ol>{"".join(toc)}</ol></nav>'
            f'<article class="prose article">{"".join(parts)}</article>'
            f'<aside class="next"><h2>Keep reading</h2><ul>{more}</ul><p>Or see the services: <a href="/ai-agents/">AI agents</a>, <a href="/ai-automation-services/">AI automation services</a> and <a href="/website-design-services/">website design services</a>.</p></aside></div></section>'
            + faq_html(g["faqs"]) + cta())
    graph = [
        {"@type": "Article", "@id": url + "#article", "headline": g["h1"], "description": g["desc"], "url": url, "mainEntityOfPage": url,
         "datePublished": LASTMOD, "dateModified": LASTMOD, "inLanguage": "en", "image": SITE + "/og-image.jpg",
         "author": {"@type": "Person", "@id": SITE + "/#abdullah", "name": "Abdullah", "url": SITE + "/"},
         "publisher": {"@type": "Organization", "@id": SITE + "/#business", "name": BRAND, "logo": {"@type": "ImageObject", "url": SITE + "/apple-touch-icon.png"}}},
        schema_crumbs(trail, url), schema_faq(g["faqs"], url)]
    return f"guides/{g['slug']}/index.html", document(url=url, title=g["title"], desc=g["desc"], body=body, graph=graph, og_type="article")


def render_all(out: pathlib.Path):
    """Write every landing page under out/ and return their public URLs."""
    urls = []
    for fn in [service_page(s) for s in SERVICES] + [industry_page(i) for i in INDUSTRIES] + [guide_page(g) for g in GUIDES]:
        rel, doc = fn
        path = out / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(doc, encoding="utf-8")
        urls.append(f"{SITE}/{rel[:-len('index.html')]}")
    return urls
