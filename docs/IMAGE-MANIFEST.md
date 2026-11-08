# Image manifest

Where every image is used, what it actually is, and what must replace it.

Each file exists as both `.webp` (what the pages load) and `.jpg` (a
fallback kept for the owner). All images are stored **uncropped at their
source aspect ratio** and are never scaled up, so nothing is cut off and
nothing is softened. The CSS aspect-ratios are matched to the files.

---

## Real photographs — safe to publish

| File | Size | Used on | What it is |
|---|---|---|---|
| `dr-andrews` | 1122×1402 (4:5) | Homepage hero, About page, Open Graph | Studio portrait of Dr. Andrews, from his own Google Business Profile. The coat reads "Paul A. Andrews, DDS, Ph.D." |
| `dr-andrews-avatar` | 240×240 (1:1) | Nav avatar chip | Square crop of the portrait, head area. The one intentional crop on the site. |
| `office-exterior` | 1672×941 (16:9) | Contact page | The actual office building in Lake Mary, supplied by the client. |

## AI-generated concept renders — must be replaced before launch

From `Andrews_Dental_15_Image_Kit`. Its own README states these are concept
visuals, not photographs, and must not be presented as the real practice.
Every page that shows one carries a visible note saying exactly that.

**Each one is used exactly once across the whole site.**

| File | Size | Used on | Replace with |
|---|---|---|---|
| `consult-hero` | 941×1672 | TMJ page, side figure | A real consultation photograph |
| `care-planning` | 1122×1402 | Home, "Personalized Dental Care" | A real treatment-planning conversation |
| `tmj-exam` | 1122×1402 | Home, "TMJ & Jaw Comfort" | A real jaw examination, with consent |
| `care-discussion` | 1122×1402 | Home, "Clear, Thoughtful Guidance" | A real consultation |
| `care-plan-digital` | 1122×1402 | Home, "Professional Consulting" | A real chairside discussion |
| `treatment-room` | 1122×1402 | Home, "A look inside" | The actual treatment room |
| `operatory` | 300×333 | Home, General Dental Care card | The actual operatory |
| `jaw-discomfort` | 299×333 | Home, TMJ & Jaw Discomfort card | Licensed lifestyle photograph |
| `instruments` | 299×333 | Home, Restorative Dentistry card | The practice's own instruments |
| `checkup` | 299×333 | Home, Oral Health Consultations card | A real check-up, with consent |
| `xray-consult` | 299×334 | Home, Dental Trauma Evaluation card | A real imaging review |
| `clinical-team` | 299×333 | Home, Professional Consulting card | The actual team |
| `reception` | 299×334 | Home, step 1 "Reach Out" | The actual reception |
| `patient-smile` | 300×334 | Home, step 2 "Discuss Your Concerns" | A real patient, with consent |
| `waiting-lounge` | 300×333 | Home, step 3 "Plan Your Next Steps" | The actual waiting area |

The nine 299×333 frames are small by design. They are placed in compact
horizontal cards where they render at roughly 150–230px wide, i.e. below
their native size, so they stay sharp. Do not move them into a full-width
slot without replacing them first.

## No image appears twice

Every content photograph above is used in exactly one place. Two deliberate
exceptions:

- `dr-andrews-avatar` is the navigation chip and appears on all nine pages.
  It is interface furniture, like a logo, not content imagery.
- `dr-andrews` appears twice: the homepage hero and the About page portrait.
  It is the only real photograph of him that exists. The homepage
  "Meet your dentist" section was made text-only so it does not repeat the
  hero a third time.

Pages with no photographs at all, by design: services (icon-led cards),
consulting, patient resources, privacy and accessibility. Their heroes are
text-led, which also removed a large amount of empty space.

---

## Rules this set follows

- **Nothing is cropped.** Each media box uses the photograph's own aspect
  ratio, so `object-fit: cover` has nothing left to trim. The hero portrait
  additionally uses `object-fit: contain`.
- **Nothing is upscaled.** No output is larger than its source, which is
  what kept the earlier hero looking soft.
- **No photograph is a background.** Every image is a foreground `<img>`.
  No text, button or gradient is laid over a photograph anywhere on the site.
- **Grading lives in CSS**, not in the files. `.dental-photo` and the shared
  rule in `css/dental.css` apply `saturate(.88) contrast(.97) brightness(1.035)`
  so the whole site reads as one shoot while the originals stay untouched.

## When you replace an image

1. Export at the aspect ratio in the table above, or update the matching
   `aspect-ratio` in `css/dental.css` section 16.
2. Save as both `.webp` and `.jpg` into `images/`, same base name.
3. Update the `width` and `height` attributes in the HTML so the browser
   reserves the right space and the layout does not shift.
4. Remove that row's note from the concept-imagery disclosures.

## Sources kept for provenance

`assets-source/` holds the untouched originals, the image kit zip, and the
kit's own README and manifest. Nothing in that folder is served by the site.
