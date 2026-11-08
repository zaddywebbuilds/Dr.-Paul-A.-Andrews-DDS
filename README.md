# Dr. Paul A. Andrews, DDS, PhD — website design proposal

A premium website concept for a general dentistry and TMJ practice in
Lake Mary, Florida, built as a faithful dental adaptation of the
[Oasis Massage Studio](https://zaddyjohn-cyber.github.io/Oasismassagestudio/)
design system.

> **This is a proposal, not a live practice website.** It is presented
> clean, with no on-page caveats, so the owner sees the finished design.
> Several business details are still unverified and most photography is
> AI-generated concept imagery. Everything that needs confirming is
> recorded in [`docs/FACTS-TO-VERIFY.md`](docs/FACTS-TO-VERIFY.md) — read it
> before this is pointed at a real domain.

---

## Running it

It is a static site with no build step and no dependencies.

```bash
python -m http.server 4173
```

Then open <http://localhost:4173>.

## Structure

```
├── index.html              Homepage (hand-maintained)
├── services.html           Six areas of dental care
├── tmj-care.html           Dedicated TMJ page
├── about.html              About Dr. Andrews
├── consulting.html         Professional / expert-witness consulting
├── patient-resources.html  Practical info and FAQ
├── contact.html            Address, map, appointment enquiry
├── privacy.html            Draft privacy statement
├── accessibility.html      Accessibility statement
│
├── css/
│   ├── fonts.css           Self-hosted font faces
│   ├── theme.css           The Oasis design system, unmodified
│   └── dental.css          The dental layer on top
├── js/main.js              Drawer, FAQ, reveals, form, perf observers
├── fonts/                  Cormorant Garamond + Inter (woff2, variable)
├── images/                 webp + jpg pairs, uncropped
├── build/build.py          Generates the eight interior pages
├── docs/                   Manifest and the facts-to-verify list
└── assets-source/          Untouched originals (not served)
```

## How the Oasis design was reused

`css/theme.css` is the Oasis stylesheet **copied byte-for-byte**, not
reimplemented from a screenshot. The repository was cloned and its real
HTML, CSS and JS were read before any markup was written.

Preserved exactly: the `.osw` iPad-style hero frame with its 32px corners
and layered radial gradients, the vertical light streaks, the frosted glass
chips and widgets, the floating centrepiece with its coral aura and
`floatY` drift, the bottom-centred serif headline with the coral gradient
highlight, the service and review cards, the FAQ accordion, the dark CTA
strip, the footer, and the mobile sticky bar.

Changed for dentistry: the centrepiece is Dr. Andrews' real portrait rather
than a video; WhatsApp booking became phone and enquiry actions; the
rotating service ring became a floating care directory; the palette is used
more sparingly so coral reads as an accent rather than the whole interface.

`build/build.py` generates the eight interior pages so the shared chrome
stays identical across them. `index.html` is hand-maintained. Re-run it
after editing navigation, the footer or contact details:

```bash
python build/build.py
```

## Photography rules

- Nothing is cropped — each media box matches its photograph's own aspect ratio.
- Nothing is upscaled — no output is larger than its source.
- No photograph is used as a background, and no text sits over one.
- No photograph appears twice. Every content image is used exactly once;
  only the nav avatar and Dr. Andrews' portrait repeat, and the manifest
  explains why.
- Colour grading lives in CSS, so the source files stay untouched.

Only the portrait of Dr. Andrews and the office exterior are real.
Everything else is AI-generated concept imagery, held as placeholders until
the practice supplies its own photography. The manifest says exactly which
file goes where: [`docs/IMAGE-MANIFEST.md`](docs/IMAGE-MANIFEST.md).

## Accessibility

Skip link, semantic landmarks, one `h1` per page, visible focus rings,
full keyboard operation, a focus-trapped mobile drawer that closes on
`Esc`, labelled form controls, polite status messages, descriptive alt
text, `prefers-reduced-motion` support, and no horizontal scrolling down
to 320px.

Verified at 320, 375, 390, 430, 768, 1024 and 1440px across all nine pages:
no horizontal overflow and no clipped element at any of them.

Text contrast was measured programmatically on every text node of all nine
pages against WCAG AA. The Oasis coral (#E5664A) reaches only 2.7:1 on cream,
so a deeper burnt coral (#B23F1B, 5.3:1) is used wherever coral carries
words, while the original stays for gradients, icons and decorative marks.
All nine pages now pass.

Not yet done: testing with assistive technology, and a full manual WCAG 2.2
AA review covering non-text contrast and every interactive state.
See `accessibility.html`.

## SEO

Unique titles, descriptions, canonicals and Open Graph tags per page;
`Dentist` structured data using only verified facts; `sitemap.xml` and
`robots.txt`; semantic headings; descriptive alt text; `width`/`height` on
every image to prevent layout shift; lazy loading below the fold; WebP;
self-hosted fonts with no third-party requests.

Structured data includes `aggregateRating` (4.7 from 10 reviews) and two
`Review` entries, all read directly from the practice's public Google
Business Profile. Opening hours are deliberately absent until confirmed.

## What is deliberately missing

Nothing here is invented to look impressive:

- No fabricated testimonials — the four shown are real, quoted verbatim,
  dated honestly, and the site links to the full set including the
  critical one.
- No invented biography, years in practice, awards or memberships.
- No guessed opening hours, insurance list or fees.
- No fake booking calendar or invented appointment slots.
- No AI-generated face presented as Dr. Andrews.
- No form that silently collects health information.

Each gap is tracked in [`docs/FACTS-TO-VERIFY.md`](docs/FACTS-TO-VERIFY.md).
The site itself carries no caveats, so that file is the only record.
