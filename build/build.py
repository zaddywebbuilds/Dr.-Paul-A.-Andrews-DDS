#!/usr/bin/env python3
"""Generate the interior pages for the Dr. Paul A. Andrews site.

The site ships as plain static HTML - this script exists only so the
shared chrome (head, hero frame, drawer, footer, floating actions) stays
byte-identical across every page. index.html is hand-maintained and is
NOT written by this script.

    python build/build.py

Re-run after editing NAV, FOOT or the shared template below.
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PHONE_E164 = "+14074612094"
PHONE_HUMAN = "(407) 461-2094"
ADDRESS = "1110 St. Albans Loop, Lake Mary, FL 32746"
MAPS_Q = "1110+St+Albans+Loop+Lake+Mary+FL+32746"
MAPS_LINK = f"https://www.google.com/maps/search/?api=1&amp;query={MAPS_Q}"

SVG = {
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.37 1.9.72 2.8a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.9.35 1.84.59 2.8.72A2 2 0 0 1 22 16.92z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    "cal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 11h18"/></svg>',
    "tooth": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 3c-2 0-2.6.9-4.2.9C6 3.9 4 5 4 8.2c0 3.4 1.2 5.3 1.9 7.6.6 2 .5 4.2 1.9 4.2 1.3 0 1.4-2.3 2-4.1.4-1.2 1-1.9 2.2-1.9s1.8.7 2.2 1.9c.6 1.8.7 4.1 2 4.1 1.4 0 1.3-2.2 1.9-4.2.7-2.3 1.9-4.2 1.9-7.6C20 5 18 3.9 16.2 3.9 14.6 3.9 14 3 12 3z"/></svg>',
    "heart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 21s-8-4.5-8-11.5A5.5 5.5 0 0 1 12 5a5.5 5.5 0 0 1 8 4.5C20 16.5 12 21 12 21z"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M9 12l2 2 4-4"/></svg>',
    "share": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M20 7h-9M14 17H5"/><circle cx="17" cy="17" r="3"/><circle cx="7" cy="7" r="3"/></svg>',
    "user": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
    "doc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></svg>',
}

# (href, label) - the single source of truth for site navigation.
NAV = [
    ("index.html", "Home"),
    ("services.html", "Dental Services"),
    ("tmj-care.html", "TMJ Care"),
    ("about.html", "About Dr. Andrews"),
    ("consulting.html", "Professional Consulting"),
    ("patient-resources.html", "Patient Resources &amp; FAQ"),
    ("contact.html", "Contact"),
]


def head(title, desc, canonical, og_image="images/dr-andrews.webp", extra=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="theme-color" content="#E5664A" />
  <meta name="format-detection" content="telephone=yes" />
  <meta name="geo.region" content="US-FL" />
  <meta name="geo.placename" content="Lake Mary, Florida" />
  <meta name="geo.position" content="28.7850199;-81.3589329" />

  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="https://zaddywebbuilds.github.io/Dr.-Paul-A.-Andrews-DDS/{canonical}" />

  <meta property="og:type" content="website" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="https://zaddywebbuilds.github.io/Dr.-Paul-A.-Andrews-DDS/{canonical}" />
  <meta property="og:image" content="https://zaddywebbuilds.github.io/Dr.-Paul-A.-Andrews-DDS/{og_image}" />
  <meta property="og:locale" content="en_US" />
  <meta name="twitter:card" content="summary_large_image" />

  <link rel="icon" href="favicon.svg" type="image/svg+xml" />
  <link rel="stylesheet" href="css/fonts.css" />
  <link rel="stylesheet" href="css/theme.css" />
  <link rel="stylesheet" href="css/dental.css" />
{extra}</head>
<body>

<a class="skip-link" href="#main">Skip to content</a>
"""


def hero(page, crumb, eyebrow, h1_html, sub, image, image_alt,
         primary=("contact.html", "Request an Appointment"),
         secondary=None):
    """The Oasis .osw window in its compact interior-page form."""
    sec = ""
    if secondary:
        sec = f'<a class="btn btn-glass" href="{secondary[0]}">{secondary[1]}</a>'
    return f"""
<section class="osw osw-small">
  <div class="osw-arch"><span></span><span></span><span></span><span></span><span></span></div>

  <header class="osw-bar">
    <div class="osw-bar-left">
      <a class="glass-chip" href="#" data-menu-open aria-expanded="false" aria-controls="menu-drawer">
        {SVG['menu']}
        Menu
      </a>
      <a class="glass-chip" href="tmj-care.html">TMJ Care</a>
      <a class="glass-chip" href="about.html">About</a>
    </div>

    <div class="osw-logo practice">
      <b>Paul A. Andrews</b>
      <span class="cred">DDS &middot; PhD</span>
      <small>Dental Care &middot; Lake Mary, FL</small>
    </div>

    <div class="osw-bar-right">
      <a class="glass-chip secondary" href="tel:{PHONE_E164}">{SVG['phone']} Call</a>
      <a class="glass-chip" href="contact.html" data-cta="appointment"><span class="t-full">Request Appointment</span><span class="t-short">Book</span></a>
      <a class="osw-avatar" href="about.html" aria-label="About Dr. Andrews"><img src="images/dr-andrews-avatar.webp" width="240" height="240" alt="Dr. Paul A. Andrews" /></a>
    </div>
  </header>

  <nav class="crumbs" aria-label="Breadcrumb">
    <a href="index.html">Home</a> <span>/</span> {crumb}
  </nav>


  <div class="osw-title">
    <span class="eyebrow" style="display:block; font-size:0.72rem; letter-spacing:0.28em; text-transform:uppercase; color:var(--c-coral-text); font-weight:700; margin-bottom:0.9rem;">{eyebrow}</span>
    <h1>{h1_html}</h1>
    <p class="sub">{sub}</p>
    <div class="btn-row" style="margin-top:1.4rem;">
      <a class="btn btn-primary" href="{primary[0]}" data-cta="appointment">{primary[1]}</a>
      {sec}
      <a class="btn btn-gold" href="tel:{PHONE_E164}">Call the Office</a>
    </div>
  </div>
</section>

<main id="main">
"""


def footer(page):
    links = "\n".join(
        f'    <a class="m-link" href="{href}"'
        + (' aria-current="page"' if href == page else "")
        + f">{label}</a>"
        for href, label in NAV
    )
    return f"""
</main>

<footer class="foot">
  <div class="foot-grid">
    <div class="foot-brand">
      <div class="osw-logo practice" style="text-align:left;">
        <b>Paul A. Andrews</b>
        <span class="cred" style="color:rgba(255,235,215,.6);">DDS &middot; PhD</span>
        <small>Dental Care &middot; Lake Mary, FL</small>
      </div>
      <p style="margin-top:1rem;">Thoughtful dental care and focused attention to jaw comfort and oral health in Lake Mary, Florida.</p>
      <div class="foot-contact" style="margin-top:1rem;">
        <div>{SVG['pin']}<span>{ADDRESS} <span class="verify">Confirm</span></span></div>
        <div>{SVG['phone']}<span><a href="tel:{PHONE_E164}">{PHONE_HUMAN}</a> <span class="verify">Confirm</span></span></div>
        <div>{SVG['clock']}<span>Opening hours to be confirmed <span class="verify">Confirm</span></span></div>
      </div>
    </div>

    <div>
      <h4>Care</h4>
      <ul>
        <li><a href="services.html">Dental Services</a></li>
        <li><a href="tmj-care.html">TMJ Care</a></li>
        <li><a href="services.html#restorative">Restorative</a></li>
        <li><a href="services.html#oral-health">Consultations</a></li>
      </ul>
    </div>

    <div>
      <h4>Practice</h4>
      <ul>
        <li><a href="index.html">Home</a></li>
        <li><a href="about.html">About Dr. Andrews</a></li>
        <li><a href="consulting.html">Professional Consulting</a></li>
        <li><a href="patient-resources.html">Patient Resources</a></li>
      </ul>
    </div>

    <div>
      <h4>Visit</h4>
      <ul>
        <li><a href="contact.html">Contact</a></li>
        <li><a href="{MAPS_LINK}" target="_blank" rel="noopener">Directions</a></li>
        <li><a href="patient-resources.html#faq">FAQ</a></li>
        <li><a href="privacy.html">Privacy</a></li>
        <li><a href="accessibility.html">Accessibility</a></li>
      </ul>
    </div>
  </div>

  <div class="foot-bottom">
    © <span class="js-year">2026</span> Dr. Paul A. Andrews, DDS, PhD &middot; Lake Mary, Florida &middot;
    <a href="privacy.html">Privacy</a> &middot; <a href="accessibility.html">Accessibility</a>
    <br /><br />
    <span style="opacity:.75; font-size:.76rem;">Website design proposal. Business details marked &ldquo;confirm&rdquo; are unverified and must be approved by the practice before publication.</span>
  </div>
</footer>

<div class="menu-drawer" id="menu-drawer" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Menu">
  <div class="menu-drawer-panel">
    <div class="menu-drawer-head">
      <div class="osw-logo practice" style="text-align:left;">
        <b>Paul A. Andrews</b>
        <span class="cred">DDS &middot; PhD</span>
        <small>Lake Mary, FL</small>
      </div>
      <button class="menu-drawer-close" type="button" aria-label="Close menu">&times;</button>
    </div>
{links}
    <div class="m-actions">
      <a class="btn btn-primary" href="contact.html" data-cta="appointment">Request an Appointment</a>
      <a class="btn btn-glass" href="tel:{PHONE_E164}">Call the Office</a>
    </div>
  </div>
</div>

<a class="float-call" href="tel:{PHONE_E164}" aria-label="Call the office">{SVG['phone']}</a>

<div class="mobile-cta">
  <a class="btn btn-primary" href="contact.html" data-cta="appointment">Appointment</a>
  <a class="btn btn-gold" href="tel:{PHONE_E164}">Call</a>
  <a class="btn btn-glass" href="tmj-care.html">TMJ</a>
</div>

<script src="js/main.js"></script>
</body>
</html>
"""


def cta(title, text):
    return f"""
  <section class="section">
    <div class="container">
      <div class="cta-strip reveal">
        <h2>{title}</h2>
        <p>{text}</p>
        <div class="action-trio">
          <a class="action-card" href="contact.html" data-cta="appointment">
            <span class="ico" aria-hidden="true">{SVG['cal']}</span>
            <strong>Request Appointment</strong><span>Send an enquiry</span>
          </a>
          <a class="action-card" href="tel:{PHONE_E164}">
            <span class="ico" aria-hidden="true">{SVG['phone']}</span>
            <strong>Call the Office</strong><span>{PHONE_HUMAN}</span>
          </a>
          <a class="action-card" href="{MAPS_LINK}" target="_blank" rel="noopener">
            <span class="ico" aria-hidden="true">{SVG['pin']}</span>
            <strong>Get Directions</strong><span>Lake Mary, FL</span>
          </a>
        </div>
        <p style="margin-bottom:1.5rem;"><span class="verify">Phone &amp; address to confirm</span></p>
        <div class="btn-row">
          <a class="btn btn-primary" href="contact.html" data-cta="appointment">Request an Appointment</a>
          <a class="btn btn-gold" href="tel:{PHONE_E164}">Call Now</a>
        </div>
      </div>
    </div>
  </section>
"""


CONCEPT_NOTE = (
    '<p class="verify-note reveal"><strong>Concept imagery.</strong> '
    'The interior and patient scenes on this page are AI-generated concept '
    'visuals supplied with the design kit. They do not show Dr. Andrews\' '
    'office, team, patients or equipment, and are replaced with commissioned '
    'photography before launch. The portrait of Dr. Andrews and the exterior '
    'photograph on the <a href="contact.html">contact page</a> are real.</p>'
)


def write(name, html):
    path = os.path.join(ROOT, name)
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    print(f"  wrote {name:<26} {len(html.encode('utf-8'))//1024:>3} KB")


# =====================================================================
# PAGES
# =====================================================================

def page_services():
    p = "services.html"
    icons = [SVG['tooth'], SVG['heart'], SVG['check'], SVG['user'], SVG['doc'], SVG['share']]
    services = [
        ("general", "General Dental Care", "treatment-room.jpg",
         "A dental treatment room prepared for a routine examination",
         "Routine examinations, cleanings and the everyday care that keeps small problems small.",
         ["Examinations and assessment", "Cleaning and preventive care",
          "Monitoring existing work", "Advice you can actually act on"]),
        ("tmj", "TMJ &amp; Jaw Discomfort", "tmj-exam.jpg",
         "A clinician gently examining a patient's jaw",
         "Assessment of jaw pain, clicking, limited opening and related facial discomfort.",
         ["Where the discomfort is coming from", "How the joint is moving",
          "What makes it better or worse", "What the options are"]),
        ("restorative", "Restorative Dentistry", "care-planning.jpg",
         "A dentist reviewing a treatment plan with a patient",
         "Repairing and rebuilding teeth so they work comfortably and look like your own.",
         ["Restoring damaged teeth", "Replacing failing older work",
          "Function first, appearance with it", "A plan you understand before it starts"]),
        ("oral-health", "Oral Health Consultations", "care-discussion.jpg",
         "A dentist in conversation with a patient",
         "A considered second opinion, or a conversation about something you have been putting off.",
         ["A second opinion on a proposed plan", "A concern you want explained",
          "Understanding a diagnosis", "No pressure to proceed"]),
        ("trauma", "Dental Trauma Evaluation", "consult-hero.jpg",
         "A calm dental consultation room",
         "Assessment of injury to teeth and the surrounding structures, and what the options are.",
         ["Assessment after an injury", "Documentation of what is found",
          "Explanation of the findings", "Referral where that is the right step"]),
        ("consulting", "Professional Dental Consulting", "care-plan-digital.jpg",
         "Two professionals in discussion",
         "Dental consulting and expert opinion for legal and professional matters.",
         ["Not a patient treatment", "Handled on a separate path",
          "Enquiries from attorneys and professionals", "See the consulting page"]),
    ]

    cards = []
    for (sid, title, img, alt, lede, points), icon in zip(services, icons):
        pts = "".join(f"<li>{x}</li>" for x in points)
        link = "consulting.html" if sid == "consulting" else "contact.html"
        label = "Enquire" if sid == "consulting" else "Request Consultation"
        cards.append(f"""
        <article class="service-tile reveal" id="{sid}">
          <div class="service-tile-icon" aria-hidden="true">{icon}</div>
          <div class="service-tile-body">
            <h3>{title} <span class="verify">Confirm scope</span></h3>
            <p>{lede}</p>
            <ul style="margin:.5rem 0 0 1.1rem; color:var(--c-ink-soft); font-size:.9rem;">{pts}</ul>
            <div class="row">
              <a href="{'tmj-care.html' if sid == 'tmj' else link}">Learn more →</a>
              <a class="btn btn-gold" style="padding:.5rem .9rem; font-size:.8rem;" href="{link}" data-cta="appointment">{label}</a>
            </div>
          </div>
        </article>""")

    body = f"""
  <section class="section">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Our approach to care</span>
        <h2>Care for your smile. Attention to your comfort.</h2>
        <p>Each area below is proposed content drawn from publicly available professional descriptions. Nothing here is a confirmed appointment menu until the practice approves it.</p>
      </div>

      <div class="verify-note reveal" style="max-width:820px; margin:0 auto 2rem;">
        <p><strong>For the practice owner.</strong> Please confirm, edit or remove each category below. Anything you do not offer should be deleted rather than softened. Professional consulting is deliberately kept on its own path so it never appears as a bookable patient treatment.</p>
      </div>

      <div class="grid grid-3">{''.join(cards)}
      </div>

      {CONCEPT_NOTE}
    </div>
  </section>
{cta("Not sure which applies to you?",
     "That is a good reason to get in touch. Describe it in general terms and we can work out the right starting point together.")}
"""
    return p, head(
        "Dental Services | Dr. Paul A. Andrews, DDS, PhD, Lake Mary FL",
        "General dentistry, TMJ and jaw care, restorative dentistry and oral health consultations with Dr. Paul A. Andrews in Lake Mary, Florida.",
        p, og_image="images/treatment-room.webp"
    ) + hero(
        p, "Dental Services", "Dental services",
        "Care for your smile. Attention to your <span class=\"glow\">comfort</span>.",
        "Six areas of care, each one confirmed with the practice before this site goes live.",
        "images/consult-hero.webp",
        "A dentist in conversation with a seated patient in a warm treatment room",
        secondary=("tmj-care.html", "TMJ Care"),
    ) + body + footer(p)


def page_tmj():
    p = "tmj-care.html"
    signs = [
        ("Jaw pain or tenderness", "Aching around the joint, or soreness that is worse at certain times of day."),
        ("Clicking or popping", "Noise from the joint when you open, close or chew."),
        ("Limited opening", "A jaw that will not open as far as it used to, or that catches."),
        ("Facial discomfort", "Pain spreading through the face, temples or around the ear."),
        ("Morning tightness", "Waking with a tight or tired jaw."),
        ("Discomfort when chewing", "Finding certain foods harder than they used to be."),
    ]
    cards = "".join(f"""
        <div class="glass-card reveal">
          <div class="icon sage" aria-hidden="true">{SVG['heart']}</div>
          <h3>{t}</h3>
          <p>{d}</p>
        </div>""" for t, d in signs)

    body = f"""
  <section class="section">
    <div class="container">
      <div class="media-split">
        <div class="media-split-text reveal">
          <span class="eyebrow" style="display:block; font-size:.72rem; letter-spacing:.28em; text-transform:uppercase; color:var(--c-coral-text); font-weight:700; margin-bottom:.9rem;">Why this page exists</span>
          <h2 style="font-size:clamp(1.8rem,3.6vw,2.5rem); margin-bottom:1rem;">Jaw discomfort deserves its own conversation.</h2>
          <p>Jaw pain is easy to live around. People adjust how they chew, avoid certain foods, and assume it is simply how things are now.</p>
          <p>It is worth describing properly to someone who will listen. Understanding where discomfort is coming from is the part that tends to get skipped, and it is the part this practice gives time to.</p>
          <p>Public patient feedback about Dr. Andrews mentions his attention to TMJ-related care specifically, which is why it has a page of its own here rather than a line in a list.</p>
        </div>
        <figure class="media-split-figure reveal">
          <img src="images/consult-hero.webp" width="941" height="1672" loading="lazy" decoding="async" alt="A dentist in conversation with a seated patient before an examination" />
        </figure>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">What people describe</span>
        <h2>Signs people often bring in.</h2>
        <p>If any of these sound familiar, they are worth raising. None of them on its own means anything in particular, and none is a diagnosis.</p>
      </div>
      <div class="grid grid-3">{cards}</div>

      <div class="verify-note reveal" style="max-width:820px; margin:1.75rem auto 0;">
        <p><strong>General information only.</strong> This page describes the kinds of concerns people raise. It is not medical or dental advice, makes no diagnosis, and promises no particular outcome. Specific treatments, appliances, timescales and costs are deliberately not listed, because none of that has been confirmed with the practice.</p>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">What to expect</span>
        <h2>A conversation before anything else.</h2>
      </div>
      <div class="steps-grid">
        <article class="step-card plain reveal">
          <span class="step-num" aria-hidden="true"></span>
          <div class="step-body"><h3>Describe it</h3><p>What you notice, when it started, and what makes it better or worse.</p></div>
        </article>
        <article class="step-card plain reveal">
          <span class="step-num" aria-hidden="true"></span>
          <div class="step-body"><h3>Be examined</h3><p>An assessment of how the jaw moves and where the discomfort sits.</p></div>
        </article>
        <article class="step-card plain reveal">
          <span class="step-num" aria-hidden="true"></span>
          <div class="step-body"><h3>Understand the options</h3><p>An explanation of the findings and what can reasonably be done about them.</p></div>
        </article>
      </div>
      {CONCEPT_NOTE}
    </div>
  </section>
{cta("Tell us about the jaw discomfort.",
     "Describe it in general terms when you get in touch. The detail is best discussed in person.")}
"""
    return p, head(
        "TMJ &amp; Jaw Care | Dr. Paul A. Andrews, DDS, PhD, Lake Mary FL",
        "Attention to jaw discomfort, clicking, limited opening and facial pain with Dr. Paul A. Andrews, DDS, PhD, in Lake Mary, Florida.",
        p, og_image="images/tmj-exam.webp"
    ) + hero(
        p, "TMJ Care", "TMJ &amp; jaw care",
        "Jaw comfort, taken <span class=\"glow\">seriously</span>.",
        "Attention to jaw discomfort, clicking, limited opening and facial pain, starting with understanding where it comes from.",
        "images/consult-hero.webp",
        "A clinician examining a patient's jaw in a calm treatment room",
        secondary=("services.html", "All Services"),
    ) + body + footer(p)


def page_about():
    p = "about.html"
    body = f"""
  <section class="section">
    <div class="container">
      <div class="bio-layout">
        <figure class="bio-portrait reveal">
          <img src="images/dr-andrews.webp" width="1122" height="1402" loading="lazy" decoding="async" alt="Studio portrait of Dr. Paul A. Andrews, DDS, PhD" />
          <figcaption class="bio-badge">Dr. Paul A. Andrews</figcaption>
        </figure>
        <div class="bio-body reveal">
          <span class="eyebrow" style="display:block; font-size:.72rem; letter-spacing:.28em; text-transform:uppercase; color:var(--c-coral-text); font-weight:700; margin-bottom:.9rem;">Meet your dentist</span>
          <h2>Dr. Paul A. Andrews, DDS, PhD</h2>
          <p>Dr. Andrews practises general dentistry in Lake Mary, Florida, with particular attention to the jaw: how it moves, where discomfort comes from, and what can reasonably be done about it.</p>
          <p>Patients who come in about jaw pain or facial discomfort often describe being listened to carefully before anything is recommended. That emphasis on understanding first is what this site is built around.</p>
          <p>Alongside patient care, Dr. Andrews is listed publicly as working in dental consulting and expert opinion for professional and legal matters. That work is kept on <a href="consulting.html">its own page</a> so it is never mistaken for a bookable treatment.</p>
          <ul class="cred-list">
            <li>DDS</li>
            <li>PhD</li>
            <li>General Dentistry</li>
            <li>TMJ &amp; Facial Pain</li>
            <li>Lake Mary, Florida</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="prose-card reveal" style="max-width:860px; margin:0 auto;">
        <h2 style="font-size:clamp(1.5rem,3vw,2rem);">What this page does not say</h2>
        <p>Writing a convincing dentist biography is easy. Writing a true one needs the dentist.</p>
        <p>So this page states only what public listings support: the name, the stated qualifications, the Lake Mary location, and the areas of work those listings describe. Everything a practice biography usually contains has been deliberately left out rather than invented:</p>
        <ul style="margin:0 0 1.25rem 1.5rem; color:var(--c-ink-soft);">
          <li>Years in practice</li>
          <li>Dental school, training and postgraduate work</li>
          <li>Awards, honours and recognitions</li>
          <li>Professional memberships and affiliations</li>
          <li>Clinical accomplishments, case numbers and outcomes</li>
          <li>Personal background, family and interests</li>
        </ul>
        <div class="verify-note">
          <p><strong>Dr. Andrews:</strong> this section is yours to fill. Send whatever you would like patients to know and it goes in as written. Nothing will be added on your behalf.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Areas of work</span>
        <h2>Where the attention goes.</h2>
      </div>
      <div class="grid grid-3">
        <div class="glass-card reveal">
          <div class="icon" aria-hidden="true">{SVG['tooth']}</div>
          <h3>General Dentistry</h3>
          <p>Everyday dental care, examinations and the work that keeps small problems small. <span class="verify">Confirm scope</span></p>
        </div>
        <div class="glass-card reveal">
          <div class="icon sage" aria-hidden="true">{SVG['heart']}</div>
          <h3>TMJ &amp; Facial Pain</h3>
          <p>Jaw discomfort, movement and related facial pain, with time given to understanding the cause. <span class="verify">Confirm scope</span></p>
        </div>
        <div class="glass-card reveal">
          <div class="icon violet" aria-hidden="true">{SVG['share']}</div>
          <h3>Professional Consulting</h3>
          <p>Dental consulting and expert opinion for legal and professional matters, handled separately from patient care. <span class="verify">Confirm scope</span></p>
        </div>
      </div>
    </div>
  </section>
{cta("Have a question for Dr. Andrews?",
     "Get in touch and describe what you would like to discuss.")}
"""
    return p, head(
        "About Dr. Paul A. Andrews, DDS, PhD | Lake Mary, Florida",
        "Dr. Paul A. Andrews, DDS, PhD, practises general dentistry in Lake Mary, Florida, with particular attention to jaw comfort and facial pain.",
        p
    ) + hero(
        p, "About Dr. Andrews", "Meet your dentist",
        "Experience. Understanding. <span class=\"glow\">Individual</span> Attention.",
        "General dentistry in Lake Mary, Florida, with particular attention to jaw comfort and facial pain.",
        "images/dr-andrews.webp",
        "Dr. Paul A. Andrews, DDS, PhD, in his dental coat",
        secondary=("consulting.html", "Professional Consulting"),
    ) + body + footer(p)


def page_consulting():
    p = "consulting.html"
    body = f"""
  <section class="section">
    <div class="container">
      <div class="verify-note reveal" style="max-width:860px; margin:0 auto 2rem;">
        <p><strong>This page is not for patients.</strong> It describes professional dental consulting and expert opinion work. It is not a dental treatment, it does not create a dentist&ndash;patient relationship, and nothing here is an appointment request. If you are looking for dental care, please use the <a href="services.html">dental services</a> page instead.</p>
      </div>

      <div class="prose-card reveal" style="max-width:860px;margin:0 auto;">
        <div class="media-split-text">
          <span class="eyebrow" style="display:block; font-size:.72rem; letter-spacing:.28em; text-transform:uppercase; color:var(--c-coral-text); font-weight:700; margin-bottom:.9rem;">For professionals</span>
          <h2 style="font-size:clamp(1.8rem,3.6vw,2.5rem); margin-bottom:1rem;">Dental consulting and expert opinion.</h2>
          <p>Public professional directories list Dr. Paul A. Andrews, DDS, PhD, among practitioners offering dental consulting and expert witness work, including matters involving dental forensics, injury and standards of care.</p>
          <p>This page exists so that enquiries of that kind have a proper route, kept entirely separate from patient appointment requests.</p>
          <div class="verify-note">
            <p><strong>Scope to be confirmed.</strong> The specific matters Dr. Andrews currently accepts, his availability, jurisdictions, fee structure and engagement terms have not been verified. Nothing is stated here beyond what public directory listings support.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Areas listed publicly</span>
        <h2>What directories describe.</h2>
        <p>These are drawn from public professional listings, not from the practice. Each one needs confirmation.</p>
      </div>
      <div class="grid grid-3">
        <div class="glass-card reveal">
          <div class="icon violet" aria-hidden="true">{SVG['doc']}</div>
          <h3>Dental Forensics</h3>
          <p>Forensic dental consulting as described in public expert directories. <span class="verify">Confirm</span></p>
        </div>
        <div class="glass-card reveal">
          <div class="icon gold" aria-hidden="true">{SVG['check']}</div>
          <h3>Injury &amp; Trauma Matters</h3>
          <p>Opinion relating to dental injury and trauma. <span class="verify">Confirm</span></p>
        </div>
        <div class="glass-card reveal">
          <div class="icon sage" aria-hidden="true">{SVG['heart']}</div>
          <h3>TMJ &amp; Facial Pain</h3>
          <p>Matters involving the temporomandibular joint and facial pain. <span class="verify">Confirm</span></p>
        </div>
      </div>
    </div>
  </section>

  <section class="section" id="enquire">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Professional enquiries</span>
        <h2>Start a consulting enquiry.</h2>
        <p>For attorneys, insurers and professional colleagues. Please do not include case detail, client information or anything confidential in a first message.</p>
      </div>

      <form class="enquiry reveal" id="enquiry-form" novalidate>
        <h3>Professional enquiry</h3>
        <p>A short note is enough to start. Detail is better discussed directly.</p>

        <div class="field-row">
          <div class="field">
            <label for="c-name">Your name <span class="req" aria-hidden="true">*</span></label>
            <input id="c-name" name="name" type="text" autocomplete="name" required />
          </div>
          <div class="field">
            <label for="c-contact">How to reach you <span class="req" aria-hidden="true">*</span></label>
            <input id="c-contact" name="contact" type="text" autocomplete="email" required />
          </div>
        </div>

        <div class="field-row">
          <div class="field">
            <label for="c-method">Preferred contact method</label>
            <select id="c-method" name="method">
              <option>Email</option>
              <option>Phone</option>
            </select>
          </div>
          <div class="field">
            <label for="c-reason">Nature of enquiry</label>
            <select id="c-reason" name="reason">
              <option>Consulting availability</option>
              <option>Expert opinion</option>
              <option>Fees and engagement terms</option>
              <option>Something else</option>
            </select>
          </div>
        </div>

        <div class="field">
          <label for="c-notes">Brief note</label>
          <textarea id="c-notes" name="notes" rows="4" placeholder="A general description only."></textarea>
          <p class="hint">Please keep this general. Do not include case detail, client names or confidential material.</p>
        </div>

        <label class="consent">
          <input type="checkbox" name="consent" required />
          <span>I agree to be contacted about this enquiry, and I understand that sending it does not create a professional engagement.</span>
        </label>

        <button class="btn btn-primary" type="submit">Send Enquiry</button>
        <div class="form-status" role="status" aria-live="polite"></div>

        <p class="hint" style="margin-top:1rem;">
          This form is not connected to a server. It opens your own email application so nothing is transmitted through this website. A secure destination is configured before launch.
        </p>
      </form>
    </div>
  </section>
"""
    return p, head(
        "Professional Dental Consulting | Dr. Paul A. Andrews, DDS, PhD",
        "Dental consulting and expert opinion enquiries for attorneys and professionals. Separate from patient dental care.",
        p, og_image="images/care-plan-digital.webp"
    ) + hero(
        p, "Professional Consulting", "For professionals",
        "Dental consulting and <span class=\"glow\">expert</span> opinion.",
        "A separate path for attorneys, insurers and professional colleagues. Not a patient treatment.",
        "images/consult-hero.webp",
        "Two professionals in discussion in a clinical office",
        primary=("#enquire", "Start an Enquiry"),
        secondary=("about.html", "About Dr. Andrews"),
    ) + body + footer(p)


def page_resources():
    p = "patient-resources.html"
    faqs = [
        ("How can I request an appointment?",
         '<p>Call the office, or send an enquiry through the <a href="contact.html">contact page</a> and let us know how you would prefer to be reached.</p>', False),
        ("Where is the practice located?",
         f'<p>Lake Mary, Florida. The address shown on this site is {ADDRESS}.</p>'
         '<p class="verify-note"><strong>To confirm:</strong> public directories disagree. Some list 1110 St. Albans Loop and others list 1540 International Parkway, Suite 2000. The correct current address must be confirmed before launch.</p>', False),
        ("Can I ask about TMJ or jaw discomfort?",
         '<p>Yes. Jaw comfort and facial pain are a particular area of attention here. Describe your concern in general terms when you get in touch, and the detail can be discussed in person. There is more on the <a href="tmj-care.html">TMJ care page</a>.</p>', False),
        ("What should I bring to my first consultation?",
         '<p class="verify-note"><strong>Answer pending.</strong> What to bring depends on the practice\'s own intake process. Rather than guess, this is left for the practice to complete.</p>', True),
        ("Does the practice accept dental insurance?",
         '<p class="verify-note"><strong>Answer pending.</strong> Accepted plans, fees and payment options have not been confirmed, so nothing is stated here.</p>', True),
        ("What are the opening hours?",
         '<p class="verify-note"><strong>Answer pending.</strong> Opening hours have not been confirmed and are deliberately not shown anywhere on this site.</p>', True),
        ("How do I get a copy of my records?",
         '<p class="verify-note"><strong>Answer pending.</strong> Records requests follow the practice\'s own process, which has not been supplied.</p>', True),
        ("How can professionals enquire about dental consulting?",
         '<p>Professional and legal consulting enquiries have their own route. See the <a href="consulting.html">professional consulting page</a>, which is kept separate from patient appointment requests.</p>', False),
    ]
    items = "".join(f"""
          <div class="faq-item">
            <button class="faq-q" type="button">{q}{' <span class="verify">Pending</span>' if pend else ''}<span class="arrow" aria-hidden="true">+</span></button>
            <div class="faq-a">{a}</div>
          </div>""" for q, a, pend in faqs)

    body = f"""
  <section class="section" id="faq">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">FAQ</span>
        <h2>Frequently asked questions</h2>
        <p>Only questions with a confirmed answer are answered. The rest are shown with the answer left open rather than filled in with a guess.</p>
      </div>

      <div class="faq-layout">
        <div class="faq-list">{items}</div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Before you visit</span>
        <h2>A few practical things.</h2>
      </div>
      <div class="fact-grid">
        <div class="glass-card reveal">
          <div class="icon" aria-hidden="true">{SVG['pin']}</div>
          <h3>Finding us</h3>
          <p>{ADDRESS} <span class="verify">Confirm</span></p>
          <p><a href="{MAPS_LINK}" target="_blank" rel="noopener">Open in Google Maps →</a></p>
        </div>
        <div class="glass-card reveal">
          <div class="icon gold" aria-hidden="true">{SVG['phone']}</div>
          <h3>Getting in touch</h3>
          <p><a href="tel:{PHONE_E164}">{PHONE_HUMAN}</a> <span class="verify">Confirm</span></p>
          <p>Or send an enquiry from the <a href="contact.html">contact page</a>.</p>
        </div>
        <div class="glass-card reveal">
          <div class="icon sage" aria-hidden="true">{SVG['clock']}</div>
          <h3>Opening hours</h3>
          <p>Not yet confirmed. <span class="verify">Confirm</span></p>
          <p>Please call to check before travelling.</p>
        </div>
        <div class="glass-card reveal">
          <div class="icon violet" aria-hidden="true">{SVG['doc']}</div>
          <h3>Insurance &amp; fees</h3>
          <p>Not yet confirmed. <span class="verify">Confirm</span></p>
          <p>Ask when you get in touch.</p>
        </div>
      </div>
    </div>
  </section>
{cta("Still have a question?",
     "Ask it directly. If we do not know the answer yet, we will say so.")}
"""
    return p, head(
        "Patient Resources &amp; FAQ | Dr. Paul A. Andrews, DDS, PhD",
        "Practical information and frequently asked questions for patients of Dr. Paul A. Andrews, DDS, PhD, in Lake Mary, Florida.",
        p, og_image="images/treatment-room.webp"
    ) + hero(
        p, "Patient Resources", "Patient resources",
        "The practical <span class=\"glow\">details</span>.",
        "Straight answers where we have them, and an honest blank where we do not.",
        "images/consult-hero.webp",
        "A calm, welcoming dental consultation room",
        secondary=("services.html", "Dental Services"),
    ) + body + footer(p)


def page_contact():
    p = "contact.html"
    extra = """  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Dentist",
    "name": "Dr. Paul A. Andrews, DDS, PhD",
    "url": "https://zaddywebbuilds.github.io/Dr.-Paul-A.-Andrews-DDS/",
    "image": "https://zaddywebbuilds.github.io/Dr.-Paul-A.-Andrews-DDS/images/office-exterior.webp",
    "telephone": "+1-407-461-2094",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "1110 St. Albans Loop",
      "addressLocality": "Lake Mary",
      "addressRegion": "FL",
      "postalCode": "32746",
      "addressCountry": "US"
    },
    "geo": { "@type": "GeoCoordinates", "latitude": 28.7850199, "longitude": -81.3589329 }
  }
  </script>
"""
    body = f"""
  <section class="section">
    <div class="container">
      <div class="media-split">
        <div class="media-split-text reveal">
          <span class="eyebrow" style="display:block; font-size:.72rem; letter-spacing:.28em; text-transform:uppercase; color:var(--c-coral-text); font-weight:700; margin-bottom:.9rem;">Find the office</span>
          <h2 style="font-size:clamp(1.8rem,3.6vw,2.5rem); margin-bottom:1rem;">Lake Mary, Florida</h2>
          <div class="info-row">{SVG['pin']}<span><strong>Address</strong>{ADDRESS} <span class="verify">Confirm</span></span></div>
          <div class="info-row">{SVG['phone']}<span><strong>Phone</strong><a href="tel:{PHONE_E164}">{PHONE_HUMAN}</a> <span class="verify">Confirm</span></span></div>
          <div class="info-row">{SVG['clock']}<span><strong>Opening hours</strong>Not yet confirmed <span class="verify">Confirm</span></span></div>
          <div class="btn-row" style="justify-content:flex-start; margin-top:1.25rem;">
            <a class="btn btn-primary" href="tel:{PHONE_E164}">Call the Office</a>
            <a class="btn btn-glass" href="{MAPS_LINK}" target="_blank" rel="noopener">Get Directions</a>
          </div>
          <div class="verify-note">
            <p><strong>Address conflict to resolve.</strong> Public directories list two different addresses for Dr. Andrews: 1110 St. Albans Loop and 1540 International Parkway, Suite 2000. The Google Maps pin used for this proposal points to St. Albans Loop. The correct current address and phone number must be confirmed before this site goes live.</p>
          </div>
        </div>
        <figure class="media-split-figure wide reveal">
          <img src="images/office-exterior.webp" width="1672" height="941" loading="lazy" decoding="async" alt="The exterior of the office building in Lake Mary, Florida" />
        </figure>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="container">
      <div class="map-frame reveal">
        <iframe
          title="Map showing the practice location in Lake Mary, Florida"
          src="https://www.openstreetmap.org/export/embed.html?bbox=-81.3689%2C28.7800%2C-81.3489%2C28.7900&amp;layer=mapnik&amp;marker=28.7850199%2C-81.3589329"
          loading="lazy"
          referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
      <p style="text-align:center; margin-top:.85rem; font-size:.85rem;">
        <a href="{MAPS_LINK}" target="_blank" rel="noopener">Open directions in Google Maps →</a>
      </p>
    </div>
  </section>

  <section class="section" id="enquire">
    <div class="container">
      <div class="section-head reveal">
        <span class="eyebrow">Request an appointment</span>
        <h2>Let's take the next step.</h2>
        <p>Tell us how to reach you and the general reason for getting in touch. Nothing detailed or medical, please.</p>
      </div>

      <form class="enquiry reveal" id="enquiry-form" novalidate>
        <h3>Appointment enquiry</h3>
        <p>We will get back to you to arrange a time.</p>

        <div class="field-row">
          <div class="field">
            <label for="f-name">Your name <span class="req" aria-hidden="true">*</span></label>
            <input id="f-name" name="name" type="text" autocomplete="name" required />
          </div>
          <div class="field">
            <label for="f-contact">How to reach you <span class="req" aria-hidden="true">*</span></label>
            <input id="f-contact" name="contact" type="text" autocomplete="email" required />
            <p class="hint">An email address or phone number.</p>
          </div>
        </div>

        <div class="field-row">
          <div class="field">
            <label for="f-method">Preferred contact method</label>
            <select id="f-method" name="method">
              <option>Phone call</option>
              <option>Email</option>
              <option>Text message</option>
            </select>
          </div>
          <div class="field">
            <label for="f-reason">General reason for enquiry</label>
            <select id="f-reason" name="reason">
              <option>New patient enquiry</option>
              <option>Routine dental care</option>
              <option>Jaw discomfort or TMJ</option>
              <option>Second opinion</option>
              <option>Something else</option>
            </select>
          </div>
        </div>

        <div class="field">
          <label for="f-notes">Anything else we should know?</label>
          <textarea id="f-notes" name="notes" rows="4" placeholder="Optional. Please keep it general."></textarea>
          <p class="hint">Please do not send symptoms, medical history or other health information through this form.</p>
        </div>

        <label class="consent">
          <input type="checkbox" name="consent" required />
          <span>I agree to be contacted about this enquiry using the details I have provided.</span>
        </label>

        <button class="btn btn-primary" type="submit">Send Enquiry</button>
        <div class="form-status" role="status" aria-live="polite"></div>

        <div class="verify-note" style="margin-top:1.25rem;">
          <p><strong>Nothing is transmitted by this website.</strong> This form does not send data anywhere. It opens your own email application with the message prepared, so no information passes through this site or any third party.</p>
          <p>Before launch, the practice should put a secure, appropriately compliant provider behind this form. Only then should any clinical detail be collected, and this page should be reviewed against the practice's own privacy obligations first.</p>
        </div>
      </form>
    </div>
  </section>
"""
    return p, head(
        "Contact | Dr. Paul A. Andrews, DDS, PhD, Lake Mary FL",
        "Contact Dr. Paul A. Andrews, DDS, PhD, in Lake Mary, Florida. Request an appointment, call the office or get directions.",
        p, og_image="images/office-exterior.webp", extra=extra
    ) + hero(
        p, "Contact", "Get in touch",
        "Let's take the next step toward your <span class=\"glow\">dental health</span>.",
        "Have a question or need a consultation? Reach out to discuss your dental care needs.",
        "images/consult-hero.webp",
        "A welcoming dental consultation room",
        primary=("#enquire", "Request an Appointment"),
        secondary=("patient-resources.html", "Patient Resources"),
    ) + body + footer(p)


def page_privacy():
    p = "privacy.html"
    body = f"""
  <section class="section">
    <div class="container">
      <div class="prose-card reveal" style="max-width:820px; margin:0 auto;">
        <div class="verify-note">
          <p><strong>Draft for review.</strong> This is a starting point written for the design proposal, not legal advice and not a finished policy. The practice should have it reviewed against its own obligations, including any that apply to health information, before publication.</p>
        </div>

        <h2>What this website collects</h2>
        <p>As published in this proposal, the site collects nothing. There is no analytics provider, no advertising pixel, no cookie banner because no cookies are set, and no form data is transmitted to any server.</p>

        <h2>The enquiry forms</h2>
        <p>The appointment and consulting forms do not send data to this website or to any third party. Submitting one opens your own email application with the message prepared, which you then send yourself. Your information travels through your own email provider, not through this site.</p>
        <p>You are asked not to include symptoms, medical history or other health information in those forms.</p>

        <h2>Fonts and embedded content</h2>
        <p>Typefaces are served from this website itself rather than a third-party font service, so loading a page does not reveal your visit to another company.</p>
        <p>The contact page embeds a map from OpenStreetMap. Loading that map involves a request to openstreetmap.org, which is subject to its own privacy policy.</p>

        <h2>If analytics are added later</h2>
        <p>The site contains inactive hooks for conversion tracking. They do nothing unless an analytics provider is installed. If the practice adds one, this policy and the site's consent handling must be updated first.</p>

        <h2>Health information</h2>
        <div class="verify-note">
          <p><strong>To be completed by the practice.</strong> How patient information is handled in the office, retention periods, patient rights, and any notice obligations that apply are matters for the practice and its advisers. Nothing has been written here on the practice's behalf.</p>
        </div>

        <h2>Contact</h2>
        <p>Questions about this policy can be directed to the practice using the details on the <a href="contact.html">contact page</a>.</p>
        <p style="margin-top:1.5rem; font-size:.85rem;">Last reviewed: not yet reviewed. <span class="verify">Pending</span></p>
      </div>
    </div>
  </section>
"""
    return p, head(
        "Privacy | Dr. Paul A. Andrews, DDS, PhD",
        "How this website handles information. A draft policy prepared for review by the practice.",
        p
    ) + hero(
        p, "Privacy", "Privacy",
        "How this site handles <span class=\"glow\">information</span>.",
        "A short, honest account of what this website does and does not collect.",
        "images/consult-hero.webp", "A calm dental consultation room",
        secondary=("accessibility.html", "Accessibility"),
    ) + body + footer(p)


def page_accessibility():
    p = "accessibility.html"
    body = f"""
  <section class="section">
    <div class="container">
      <div class="prose-card reveal" style="max-width:820px; margin:0 auto;">
        <h2>What has been built in</h2>
        <ul style="margin:0 0 1.5rem 1.5rem; color:var(--c-ink-soft);">
          <li>Semantic landmarks, a single <code>h1</code> per page and an ordered heading structure.</li>
          <li>A &ldquo;skip to content&rdquo; link as the first focusable element on every page.</li>
          <li>Visible focus outlines on every link, button and form control.</li>
          <li>Full keyboard operation, including the FAQ accordion and the mobile menu, which traps focus while open and closes on <kbd>Esc</kbd>.</li>
          <li>Descriptive alternative text on meaningful images, and empty alt on decorative ones.</li>
          <li>Form labels tied to their controls, with status messages announced politely.</li>
          <li>Respect for the operating system's reduced-motion setting: floating, pulsing and reveal animations stop.</li>
          <li>Text that reflows without horizontal scrolling down to 320px.</li>
          <li>Tap targets sized for touch on small screens.</li>
        </ul>

        <h2>Known limitations</h2>
        <ul style="margin:0 0 1.5rem 1.5rem; color:var(--c-ink-soft);">
          <li>The design uses translucent glass surfaces over photography. Contrast has been kept conservative, but a full audit against WCAG 2.2 AA has not been carried out on every state.</li>
          <li>The embedded map is third-party content and its accessibility is outside this site's control. A text address and a directions link are always provided alongside it.</li>
          <li>Testing with assistive technology has not yet been performed by a user of that technology.</li>
        </ul>

        <div class="verify-note">
          <p><strong>Before launch.</strong> A full accessibility audit is recommended, and this statement should be updated with the standard the practice is committing to, the date of the audit, and a contact route for access problems.</p>
        </div>

        <h2>Telling us about a problem</h2>
        <p>If any part of this site is difficult to use, please get in touch through the <a href="contact.html">contact page</a> or call the office, and describe what you were trying to do.</p>
        <p style="margin-top:1.5rem; font-size:.85rem;">Last reviewed: not yet reviewed. <span class="verify">Pending</span></p>
      </div>
    </div>
  </section>
"""
    return p, head(
        "Accessibility | Dr. Paul A. Andrews, DDS, PhD",
        "How this website approaches accessibility, what has been built in, and what still needs auditing.",
        p
    ) + hero(
        p, "Accessibility", "Accessibility",
        "Built to be <span class=\"glow\">usable</span>.",
        "What has been done, and what is honestly still outstanding.",
        "images/consult-hero.webp", "A calm dental consultation room",
        secondary=("privacy.html", "Privacy"),
    ) + body + footer(p)


def main():
    print("Building interior pages...")
    for fn in (page_services, page_tmj, page_about, page_consulting,
               page_resources, page_contact, page_privacy, page_accessibility):
        name, html = fn()
        write(name, html)
    print("\nindex.html is hand-maintained and was not touched.")


if __name__ == "__main__":
    main()
