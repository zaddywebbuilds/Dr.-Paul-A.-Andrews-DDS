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

| File | Size | Used on | Replace with |
|---|---|---|---|
| `consult-hero` | 941×1672 (9:16) | Interior page heroes, a service card | A real consultation photograph, portrait format |
| `treatment-room` | 1122×1402 (4:5) | "A look inside", General Dental Care card, FAQ | The actual treatment room |
| `tmj-exam` | 1122×1402 (4:5) | TMJ card, TMJ page, "TMJ & Jaw Comfort" | A real jaw examination, with patient consent |
| `care-planning` | 1122×1402 (4:5) | Restorative card, "Personalized Dental Care", a step card | A real treatment-planning conversation |
| `care-discussion` | 1122×1402 (4:5) | Oral Health card, "Clear, Thoughtful Guidance", a step card | A real consultation |
| `care-plan-digital` | 1122×1402 (4:5) | Consulting card, "Professional Consulting", a step card | A real chairside discussion |

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
