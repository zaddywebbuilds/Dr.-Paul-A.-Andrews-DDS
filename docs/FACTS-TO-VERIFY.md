# Business facts that need owner approval before launch

Every item below is either unconfirmed or contradicted by another public
source. Nothing on this list should go live until Dr. Andrews or his office
confirms it. Items marked **BLOCKER** will mislead patients if left wrong.

> **The on-page flags have been removed.** Earlier builds marked every
> unverified fact with an amber `Confirm` badge and carried a note on each
> page explaining that most photography is AI concept imagery. Those were
> scaffolding for the pitch and have been taken out so the demo reads as a
> finished site. **This document is now the only record.** Work through it
> before the site is pointed at a real domain or shown to patients.

---

## 1. Address — **BLOCKER**

Public directories disagree:

| Source | Address |
|---|---|
| Google Maps pin supplied for this build | 1110 St. Albans Loop, Lake Mary, FL 32746 |
| Yelp, and several directories | 1540 International Pkwy, Suite 2000, Lake Mary, FL 32746 |

Complication: **1110 St Albans Loop is also listed as Greenberg Dental &
Orthodontics.** Dr. Andrews may practise from that location, the listing may
be stale, or the two may be unrelated.

The site currently shows **1110 St. Albans Loop** because that is where the
supplied Google Maps pin points, and the exterior photograph on the contact
page is of that building.

**Action:** confirm the correct current practice address.

## 2. Telephone — **BLOCKER**

| Source | Number |
|---|---|
| Yelp, Expert Pages, LinkedIn | (407) 461-2094 |
| One directory, and Greenberg Dental's listing | (407) 862-0444 |

The site uses **(407) 461-2094** in every call link, the footer and the
structured data, because it appears on Dr. Andrews' own LinkedIn profile.

**Action:** confirm. If it is wrong, every `tel:` link needs updating.

## 3. Opening hours

Not confirmed. One secondary source suggests Monday to Friday, 8:00am to
4:30pm, closed weekends, but this was not verified against a primary source.

**No opening hours appear anywhere on the site.** The footer, the FAQ and
the contact page all say "to be confirmed" rather than guess.

**Action:** supply the real hours. They then go in the footer, the contact
page, the FAQ, and as `openingHoursSpecification` in the structured data.

## 4. Services offered

The six service categories are **proposed content**, drawn from public
professional descriptions. They are not a verified appointment menu.

1. General Dental Care
2. TMJ & Jaw Discomfort
3. Restorative Dentistry
4. Oral Health Consultations
5. Dental Trauma Evaluation
6. Professional Dental Consulting *(kept on a separate path, not bookable)*

**Action:** confirm, edit or delete each one. Anything not offered should be
removed outright rather than reworded.

## 5. Biography and credentials

The site states only: the name, **DDS**, **PhD**, the Lake Mary location, and
the areas of work that public listings describe.

Deliberately **not** stated, because inventing them would be dishonest:

- Years in practice *(one secondary source says "over 48 years" — unverified)*
- Dental school, training, postgraduate work
- Awards, honours, recognitions
- Professional memberships and affiliations
- Clinical accomplishments, case numbers, outcomes
- Personal background

**Action:** Dr. Andrews supplies whatever he wants patients to know. It goes
in as written.

## 6. Reviews

Four reviews are quoted **verbatim** from the public Google Business Profile,
each with the reviewer's name and the age of the review as Google shows it.
The real aggregate — **4.7 from 10 reviews** — is displayed, and the page
links to the complete set.

Important points:

- The four shown are a **positive selection**. The profile also contains a
  two-star review criticising office staff. The link goes to all of them.
- The reviews are **old**: roughly 7 to 11 years. The site says so on each
  card and never implies they are recent.
- Five further reviews could not be retrieved; Google requires a signed-in
  account to display them.
- `aggregateRating` and two `Review` entries appear in the structured data.

**Action:** confirm you are happy to republish these four, and that the
rating is current. If the profile changes, update both the cards and the
structured data. Remove the `aggregateRating` block if you would rather not
make a rating claim in search results.

## 7. Insurance, fees and payment

Entirely unconfirmed. The FAQ answer is left open rather than filled in.

**Action:** supply accepted plans and payment options, or confirm that the
answer should stay "please call to ask".

## 8. The enquiry forms

The appointment and consulting forms **do not transmit anything**. They open
the visitor's own email application with the message prepared.

This is deliberate: a static website is not an appropriate place to collect
patient health information, and no secure endpoint has been configured.

**Action before launch:**

1. Choose a provider appropriate for patient enquiries, taking advice on any
   obligations that apply to health information.
2. Set the form's `data-to` attribute, or replace the handler in
   `js/main.js` with a real submission.
3. Only then consider collecting any clinical detail. The forms currently
   ask visitors *not* to send symptoms or medical history.

## 9. Photography — **BLOCKER for the concept renders**

| Image | Status |
|---|---|
| `dr-andrews.webp` | **Real.** Studio portrait from the practice's own Google Business Profile. |
| `office-exterior.webp` | **Real.** The actual building, supplied by the client. |
| All other photographs | **AI-generated concept visuals** from `Andrews_Dental_15_Image_Kit`. |

The concept renders do **not** show Dr. Andrews' office, team, patients or
equipment. The site no longer says so on the page, so this is the only place
it is written down.

**Action:** commission real photography of the practice and replace every
concept render before launch. See `docs/IMAGE-MANIFEST.md`.

## 10. Domain and canonical URLs

Canonical URLs and the sitemap currently point at the GitHub Pages address:

`https://zaddywebbuilds.github.io/Dr.-Paul-A.-Andrews-DDS/`

**Action:** when a real domain is chosen, update `build/build.py`, re-run it,
and update `sitemap.xml` and `robots.txt`.

## 11. Privacy and accessibility statements

Both are **drafts written for this proposal**, not legal documents and not
the output of an audit.

**Action:** have both reviewed before publication.
