"""Content for the company pages: about, contact, pricing, work, hubs, legal and 404."""

EMAIL = "info@abdullahautomations.com"
UPDATED = "9 October 2026"

ABOUT = {
    "title": "About Abdullah Automations: AI Agents & Websites",
    "desc": "Abdullah Automations is a small studio that builds AI agents, AI automation and premium websites for service businesses. Meet Abdullah and see how we work.",
    "h1": "A small studio that builds AI your customers will actually like",
    "lede": "Abdullah Automations is run by Abdullah. I build AI agents, automations and websites for service businesses that are losing customers to slow replies, missed calls and dated websites.",
    "story": [
        "I started Abdullah Automations because I kept seeing the same problem. Good businesses with happy customers were losing new ones before the first conversation even started. The phone rang while the owner was busy, a message sat unread over the weekend, or a visitor left a slow website and booked with a competitor.",
        "AI can fix most of that today, but only if it is set up carefully. An assistant that gives wrong answers or sounds like a robot does more harm than good. So I build systems the way I would want them for my own business: trained on your real information, connected to the tools you already use, tested before launch, and easy to hand over to a person.",
        "I work with a small number of clients at a time, so every project gets my full attention from the first call to launch and after.",
    ],
    "principles": [
        ("Plain language", "You get clear explanations, written plans and fixed prices. No jargon and no surprise invoices."),
        ("Your business, your data", "Your website, accounts and customer data stay in accounts you own. You can leave at any time and take everything with you."),
        ("Careful AI", "Agents answer only from information you approve and hand over to a person when they are unsure. You can read every conversation."),
        ("Results you can count", "We agree what success looks like before we start, such as replies, bookings or hours saved, and track it after launch."),
    ],
}

CONTACT = {
    "title": "Contact Abdullah Automations: Book a Free Strategy Call",
    "desc": "Contact Abdullah Automations to book a free 30-minute strategy call about AI agents, AI automation or a new website. Email info@abdullahautomations.com.",
    "h1": "Let's talk about your business",
    "lede": "Tell me a little about your business and what you would like help with. I reply to every enquiry within one working day, usually much sooner.",
    "expect": [
        ("You send a message", "Use the form or email me directly. A few sentences about your business is enough."),
        ("We book a call", "I reply with a few times for a free 30-minute video call."),
        ("You get a plan", "On the call we look at where you lose leads and time. You leave with clear next steps, whether you hire me or not."),
    ],
}

PRICING = {
    "title": "Pricing: AI Agents, Automation & Websites",
    "desc": "Clear, fixed pricing for AI agents, AI automation and premium websites. Websites from $1,500, automation from $1,200, AI agents from $2,500. No hidden fees.",
    "h1": "Clear pricing. Fixed quotes.",
    "lede": "Every project starts with a written blueprint and a fixed price, so you know the full cost before any work begins. These are starting prices; your quote depends on the channels, tools and pages you need.",
    "plans": [
        {"name": "Website", "price": "1500", "label": "$1,500", "per": "from, one time", "for": "A bespoke website that makes your business look like the premium choice and turns visitors into enquiries.",
         "items": ["Up to 6 custom-designed pages", "Background video and animation", "Booking or enquiry flow", "SEO, speed and analytics setup", "30 days of support after launch"], "cta": "Start a website"},
        {"name": "Growth system", "price": "6000", "label": "$6,000", "per": "from, plus $600/month", "for": "Website, AI agent and automations, built together and managed for you every month.", "feat": True,
         "items": ["Everything in Website and AI agent", "Agent on web, WhatsApp and Instagram", "CRM, follow-ups, reminders and reviews", "Monthly tuning and a results report", "Priority support"], "cta": "Book a strategy call"},
        {"name": "AI agent", "price": "2500", "label": "$2,500", "per": "from, plus $300/month", "for": "An assistant that answers and books for you, added to the website you already have.",
         "items": ["Trained on your business information", "Books into your calendar", "Hand-off to you or your team", "Website chat or WhatsApp", "Monthly conversation review"], "cta": "Add an AI agent"},
    ],
    "addons": [
        ("AI automation project", "From $1,200", "Lead capture, follow-ups, reminders, review requests or reporting, built as a one-off project."),
        ("Voice receptionist", "Quoted per project", "An AI agent that answers phone calls, takes bookings and texts back missed callers."),
        ("Extra website pages", "From $150 per page", "Service, location or landing pages designed to match your site."),
        ("Care plan", "From $300/month", "Hosting, AI usage within normal volume, monitoring, fixes and monthly improvements."),
    ],
    "faqs": [
        ("Why do prices say \"from\"?", "Projects vary in the number of channels, tools and pages involved. After a free call you get a fixed quote for your exact project."),
        ("What does the monthly fee cover?", "Hosting, AI usage within normal volume, monitoring, fixes and monthly improvements. Very high message volume is quoted separately and agreed in advance."),
        ("Do you offer payment plans?", "Yes. Larger projects are usually split into a deposit and a final payment at launch. Ask on your call."),
        ("Can I cancel the care plan?", "Yes, with 30 days' notice. Your website, accounts and data stay yours."),
    ],
}

WORK = {
    "title": "Work: Concept Websites with AI Agents | Abdullah Automations",
    "desc": "See concept websites with working AI assistants for a dental clinic, real estate agency, restaurant and skincare store. Click through and try each assistant.",
    "h1": "Concept sites you can click through",
    "lede": "These are concept websites I designed and built to show the standard of work you get. The businesses are fictional, but the designs and AI assistants are real: open any site and ask the assistant in the corner to book something.",
    "items": [
        ("dental", "Brightline Dental Atelier", "Dental clinic", "An ivory, emerald and brass design for a modern clinic. The assistant books check-ups, handles emergencies and answers insurance questions.", "/ai-automation-for/dental-clinics/"),
        ("realestate", "Harbor & Stone Realty", "Real estate", "A dark, quiet-luxury brokerage site with filterable listings. The assistant qualifies buyers, answers listing questions and books viewings.", "/ai-automation-for/real-estate/"),
        ("restaurant", "Ember & Oak", "Restaurant", "A firelit design with a printed-menu layout. The assistant takes reservations, records allergies and captures private event enquiries.", "/ai-automation-for/restaurants/"),
        ("store", "Northfold Skincare", "E-commerce", "A calm product-first store. The assistant builds a skincare routine, tracks orders and handles returns and exchanges.", "/ai-automation-for/ecommerce/"),
    ],
}

PRIVACY = {
    "title": "Privacy Policy | Abdullah Automations",
    "desc": "How Abdullah Automations collects, uses and protects personal information when you visit abdullahautomations.com or contact us about our services.",
    "h1": "Privacy policy",
    "sections": [
        ("Who we are", [f"This website is run by Abdullah Automations (\"we\", \"us\"). If you have any questions about this policy or your information, email <a href=\"mailto:{EMAIL}\">{EMAIL}</a>."]),
        ("Information we collect", ["We collect information you choose to give us, such as your name, business name, email address and the details of your enquiry when you contact us or book a call.",
                                    "When you visit the website, our hosting provider and analytics tools may collect standard technical information such as your IP address, browser type, pages visited and the time of your visit."]),
        ("How we use your information", ["We use your information to reply to your enquiry, provide our services, send you information you have asked for, improve our website and meet our legal obligations. We do not sell your personal information."]),
        ("Legal basis", ["Where data protection law requires a legal basis, we rely on your consent, on steps taken at your request before entering into a contract, on performing a contract with you, or on our legitimate interest in running and improving our business."]),
        ("Sharing your information", ["We share information only with service providers who help us run the business, such as website hosting, email, scheduling and analytics providers, and only as needed for them to provide their service. We may also share information if the law requires it."]),
        ("Client projects and AI systems", ["When we build AI agents or automations for a client, the client decides what customer data the system processes and remains responsible for it. We process that data only on the client's instructions and set systems up to use accounts the client owns."]),
        ("Cookies and analytics", ["The website may use cookies or similar technology for basic functions and to understand how visitors use the site. You can block or delete cookies in your browser settings."]),
        ("How long we keep information", ["We keep enquiry and client information only as long as needed for the purposes above, or as long as the law requires, and then delete it."]),
        ("Your rights", [f"Depending on where you live, you may have the right to access, correct, delete or limit the use of your personal information, to object to processing and to receive a copy of your data. To make a request, email <a href=\"mailto:{EMAIL}\">{EMAIL}</a>. You may also complain to your local data protection authority."]),
        ("Security", ["We use reasonable technical and organisational measures to protect personal information. No method of sending or storing data is completely secure, so we cannot guarantee absolute security."]),
        ("Changes to this policy", ["We may update this policy from time to time. The date at the top of the page shows when it was last changed."]),
    ],
}

TERMS = {
    "title": "Terms of Service | Abdullah Automations",
    "desc": "The terms that apply when you use abdullahautomations.com and when you work with Abdullah Automations on AI agents, automation or website projects.",
    "h1": "Terms of service",
    "sections": [
        ("About these terms", [f"These terms apply to your use of abdullahautomations.com and to services provided by Abdullah Automations. Each client project is also covered by a written proposal or agreement, which takes priority if it differs from these terms. Questions: <a href=\"mailto:{EMAIL}\">{EMAIL}</a>."]),
        ("Using this website", ["You may use this website for lawful purposes only. The content is provided for general information and may change without notice. Concept and demo sites shown on this website feature fictional businesses and are for illustration only."]),
        ("Proposals and payment", ["Projects start after you accept a written proposal and pay any agreed deposit. Prices, scope, timeline and payment terms are set out in the proposal. Work outside the agreed scope is quoted separately before it begins."]),
        ("Your responsibilities", ["You agree to provide accurate information, timely feedback and access to the accounts and tools needed for the project. You are responsible for the information an AI agent is trained on, for how you use the systems we build, and for complying with laws that apply to your business, including data protection and marketing rules."]),
        ("AI systems", ["AI agents and automations are set up to answer from the information you approve and to hand over to a person when unsure. AI output can still be incomplete or wrong, so you should review conversations and not rely on an AI agent for legal, medical, financial or other professional advice to your customers."]),
        ("Ownership", ["When a project is paid in full, you own the website content and design created for you, and the accounts set up in your name. We keep ownership of our general tools, templates and know-how, and may show the finished work in our portfolio unless you ask us not to."]),
        ("Care plans", ["Monthly care plans run month to month and can be cancelled with 30 days' written notice. Third-party costs such as hosting, software subscriptions and AI usage above the agreed volume may be charged separately, as set out in your plan."]),
        ("Third-party services", ["Projects often rely on third-party platforms such as hosting, messaging, AI and scheduling providers. We are not responsible for their availability, pricing or policy changes, but we will help you respond to them."]),
        ("Limitation of liability", ["To the extent the law allows, our total liability for any claim relating to a project is limited to the amount you paid for that project in the previous 12 months, and we are not liable for indirect or consequential losses such as lost profits."]),
        ("Changes to these terms", ["We may update these terms from time to time. The date at the top of the page shows when they were last changed."]),
    ],
}

NOT_FOUND = {
    "title": "Page not found | Abdullah Automations",
    "desc": "This page could not be found. Visit the homepage or explore AI agents, AI automation and website design services from Abdullah Automations.",
    "h1": "This page doesn't exist",
    "lede": "The link may be old or mistyped. Here are the most useful places to go instead.",
}
