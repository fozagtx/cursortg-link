---
name: landing-page-rewrite
description: >
  Rewrite or build a high-converting SaaS landing page using a proven
  conversion framework. Use when the user says "rewrite my landing
  page", "improve landing page", "create a landing page", "make a
  better hero", "my landing page isn't converting", "fix the homepage",
  "marketing page", or asks to apply conversion principles to a
  marketing/product page. Triggers proactively when a generic or
  vague landing page is detected during frontend work.
---

# Landing Page Rewrite

A drop-in framework for turning any generic product page into a high-converting SaaS landing page. Apply when rewriting a homepage, building a new one, or auditing an existing one against conversion principles.

## When to apply

- User asks to "rewrite the landing page", "improve the homepage", "make a better hero", or similar
- Existing landing has vague/poetic copy ("X for the modern team", "intelligence that floats") with no concrete value
- Existing landing has fewer than 4 sections, no FAQ, no second CTA, no problem statement
- Sponsor/partner badges shown without context ("Powered by")
- A new homepage is being scaffolded from scratch for a product

## Non-negotiable principles

1. **The 5-year-old test** — A 5-year-old should grasp the core value of the product from the hero alone. If your headline could apply to 100 other products, rewrite it.
2. **Problem before solution** — Don't lead with features. Lead with the specific pain. The reader should think "yes, that's me" before they see what you sell.
3. **Concrete over poetic** — "Win more deals. Stop guessing why you lost." beats "Sales intelligence floating in the cloud." Numbers, named pains, real outcomes — not adjectives.
4. **Two CTAs above the fold** — A primary action ("Start free", "Try a deck") and an escape valve ("See how it works" anchor). The escape valve actually increases primary conversion.
5. **One job per section** — Hero declares value · trust bar builds credibility · problem creates urgency · solution shows the fix · differentiators handle objections · FAQ removes friction · final CTA closes. Mixing jobs dilutes each.
6. **Restate the value at the end** — The final CTA section repeats the hero's promise in different words. The reader who scrolled has earned a refresher.

## The framework — sections in order

### 1. Hero (above the fold)

**Structure:**

```
[Status badge — "Live · 3 agents" or "Beta — invite only"]
[Headline — concrete value or sharp problem framing]
[Subheadline — what it does + who it's for, ~2 sentences]
[Primary CTA] [Secondary CTA / anchor]
[3 trust microbadges — speed/cost/openness or similar]
```

**Headline formulas (pick the one that fits):**
- Problem-led: "Stop losing deals to bad pitch decks." → most aggressive, best for crowded categories
- Outcome-led: "Win more deals. Stop guessing why you lost." → confident, clear stakes
- Transformation: "From rambling discovery calls to a live switch chart in 60 seconds."
- Numeric: "Audit 90% of your lost deals in 90 seconds each."

**Anti-patterns:**
- Metaphor headlines ("floating in the cloud", "rocket fuel for X", "the AI brain") — vague
- Two-line poetic headlines that could describe any competitor
- Generic CTA: "Get started" — replace with action that previews the value: "Try a deck", "Score my pitch", "Run an audit"

### 2. Trust bar (right under hero)

**Purpose:** Reduce perceived risk before the reader scrolls further.

**Options, ranked by power:**
- Real customer logos with permission
- Real testimonials ("X helped us land Y" — named, attributable)
- Numeric proof: "12,000 founders" / "$4M analyzed"
- Sponsor/infra stack only if positioned as credibility: "Built on the same stack as the agents winning AI Olympics" — never just "Powered by" with no claim
- Press logos / GitHub stars / open-source badges

**Rule:** Never put a trust bar that says "Trusted by hundreds" with no logos. Empty trust bars are worse than no trust bar.

### 3. Problem section

**Structure:** 3 concrete pain cards. Each card = one pain + one consequence + a tiny hint of the fix.

**Headline formulas:**
- "You're leaking deals at three obvious points."
- "Three reasons your team keeps losing winnable deals."
- "What's broken today."

**Card pattern:**
```
[Red ✗ icon — visual marker for "today, bad"]
[3-word problem title — "Your deck buries the offer"]
[2-3 sentence consequence + how RevAgent fixes it]
[Small "With RevAgent →" footer with a green ✓]
```

**Anti-patterns:**
- 6 pain points (3 is the magic number — 4 max if absolutely necessary)
- Generic pains like "communication is hard" — make them visceral and specific to the buyer's job
- Pain that doesn't have a clean fix in your product

### 4. Solution / How it works

**Structure:** 3 product/feature cards mapping to the 3 pains, in the same order. This creates a satisfying "problem → fix" parallel that the reader subconsciously tracks.

**Card pattern:**
```
[Icon] [sponsor/tech name — small eyebrow]
[Product name — bold, 2-3 words]
[Headline metric — "$0.04 / deck", "<2s latency", "~90s / deal"]
[2-sentence description ending with the concrete output]
[Link "Open →"]
```

**Rule:** The headline metric is the killer. It promises measurable speed, cost, or output. Never just "fast" — give the number.

### 5. Differentiators ("Why not just X?")

**Purpose:** Pre-empt the #1 objection every modern SaaS faces: "can't I just use ChatGPT/Codex/Linear/Notion?"

**Headline formulas:**
- "ChatGPT won't do this."
- "Why not just a Notion template?"
- "More than a wrapper."

**Card pattern (3 cards):**
- Built around your workflow (vs generic prompt)
- Structured outputs (vs prose blob)
- Your data, your bucket (vs trained on your inputs)

Adjust based on the actual category. Common differentiator buckets:
- Specialization (purpose-built vs general)
- Output format (structured vs prose)
- Data ownership / privacy
- Speed / latency
- Open-source / self-hostable
- Integrations
- Price

### 6. FAQ

**Structure:** 6 collapsible Q&As. Every question should be one a reader is actively thinking before they trust you with their work.

**The 6 questions to always answer:**
1. "What does it cost?" — Be specific. Free during beta beats "starting at $0".
2. "Do I need to integrate my CRM/stack/whatever?" — Lower the activation barrier.
3. "Where does my data go?" — Privacy. Mention concrete storage if you can.
4. "How fast is it?" — Concrete time bounds.
5. "What if [X] breaks?" — Show you have a real error-handling story.
6. One category-specific question that addresses the #1 buyer hesitation in your niche.

**Anti-patterns:**
- "How does AI work?" — too high-level, treats reader like a child
- Marketing-as-FAQ ("How is X different from competitors?") — handle this in the Differentiators section, not here
- FAQs that don't anticipate real objections — they should make the reader nod, not roll their eyes

### 7. Final CTA

**Structure:**
```
[Eyebrow — "Stop guessing" or "Get started"]
[Big restated value headline — different words, same promise as hero]
[1-sentence reminder of the input → output]
[Primary CTA] [Secondary — usually "Star on GitHub" or "Read the docs"]
```

**Rule:** The final CTA must repeat the hero's value in fresh language. The reader who scrolled past 6 sections has earned a recap — don't just say "Sign up now."

## Audit checklist (when reviewing an existing page)

Before rewriting, score the current page against this list. Anything answered "no" = a rewrite target.

- [ ] Hero headline passes the 5-year-old test
- [ ] Hero subhead names WHO it's for + WHAT it does in <30 words
- [ ] Two CTAs above the fold (primary + escape valve anchor)
- [ ] Trust bar has actual claim, not just "Powered by"
- [ ] Problem section exists and has 3 concrete pains, not 6
- [ ] Solution maps 1:1 to the problems in the same order
- [ ] Each solution card has a headline metric
- [ ] Differentiator section pre-empts "why not just X?"
- [ ] FAQ has 6 real-objection questions
- [ ] Final CTA restates value in fresh language
- [ ] No metaphor headlines ("floating", "rocket fuel", "the X brain")
- [ ] Every CTA points to the same destination or a logical sub-funnel

## Component conventions to preserve

When rewriting an existing app's page:

- **Keep the existing design system** — don't introduce new colors, fonts, or component primitives. The new copy/structure goes into existing Card / Button / PageHeader / etc. components.
- **Reuse animation tokens** — if the codebase has `rise-in`, `stagger-1..5`, `fade-in`, etc., apply them consistently. New page should feel like the existing app, just sharper.
- **Match the existing typography hierarchy** — serif for headlines, sans for body, mono for eyebrows/badges. If the system already uses these, keep them.
- **Use the existing icon library** — don't introduce a new icon set. Most SaaS apps use lucide-react; check before importing.

## Example rewrite

Below is the before/after pattern from a hackathon SaaS app. Note how the hero went from vague-poetic to concrete-aggressive, and how a single-section page became a 7-section funnel.

**Before (3 sections):**
- Hero: "Sales intelligence, floating in the cloud" / "Three coordinated AI agents that fix the three most-broken parts..."
- Three agents grid
- "Powered by" sponsor strip

**After (7 sections):**
- Hero: "Win more deals. Stop guessing why you lost." + 2 CTAs + 3 trust microbadges
- Trust bar: positioned sponsor stack as credibility
- Problem: 3 red ✗ pain cards
- Solution: 3 agent cards with metrics ($0.04 / deck, <2s latency, ~90s / deal)
- Differentiators: "ChatGPT won't do this" — 3 cards
- FAQ: 6 questions covering cost / CRM / data / audio / speed / failure
- Final CTA: "See your deck through your buyer's eyes — in 60 seconds" + dual CTAs

## When NOT to use this framework

- **Brutally minimal indie tools** where the audience is technical and conversion is via word-of-mouth (e.g., a single-purpose CLI tool's homepage). One paragraph + GitHub link can outperform a 7-section funnel.
- **Enterprise sales pages** that exist to feed a sales team, not self-serve signups. Those need different sections: ROI calculator, security badges, customer logos, demo booking flow.
- **Brand-led pages** for established companies where the brand itself is the conversion driver. Less framework, more art direction.

If the audience self-serves and converts via signup → this framework applies. Adapt section count for shorter pages by collapsing Differentiators into the Solution section, but never skip Hero, Problem, Solution, FAQ, Final CTA.
