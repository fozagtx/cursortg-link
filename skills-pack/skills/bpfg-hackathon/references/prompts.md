# Prompt Library — Copy / Paste

All prompts assume the Village system prompt is loaded when possible.

---

## 1. Brief Builder

```text
Brief Builder. Do NOT research yet.
Raw intent (voice transcript or dump):
"""
{PASTE}
"""
1) Mirror multi-part ask
2) Propose ONE living question (open ≥2 directions)
3) Force audience split if needed
4) Ask only critical friction questions
5) Output FULL commission template (territories, void language, shadow, filters, evidence rules, deploy options)
```

---

## 2. Mapper

```text
Scout Orchestrator · MAPPER
Commission:
{FULL_BRIEF}

Rank territories by lived pain + honesty of signal.
Hackathon limit: 2–4 territories.
Flag paywalled/dark social.
Output dispatch order.
```

---

## 3. Landscape scout

```text
You are a Scout (ethnographer), not a summarizer.
Mode: LANDSCAPE
Territory: {TERRITORY}
Full brief:
{FULL_BRIEF}

Return: map → intensity-ranked signals → exact phrases → workarounds → absences → CANDIDATES
Do not invent users. Cite or mark CANDIDATE.
```

---

## 4. Deep dive scout

```text
Scout DEEP DIVE on {community}.
Treat as a village: roles, rituals, beliefs, status, recurring fights.
Brief: {FULL_BRIEF}
Time window: {if any}
Output ethnographic notes + implications for a 24h product demo.
```

---

## 5. Multi-model through-line

```text
Two scout reports below.
Extract:
- Agreements (through-line)
- Productive disagreements
- Unique edges only one saw
- Claims needing human validation
Do NOT average into bland consensus.

REPORT A:
{...}

REPORT B:
{...}
```

---

## 6. Elder lead pair

```text
Elder Council · LEAD PAIR
Deadline: {hours} hours left.
Living question: {...}
Insight bank summary:
{...}

@Detective and @Decider: CONVERSE (not monologues).
Output:
1) Demo spine (one sentence)
2) Cut list
3) Hero line in field language
4) Riskiest claim + 30-min validation path
5) Next 60 minutes
```

---

## 7. Full council

```text
Full council: @Detective @Decider @Antenna
We must ship a demo that closes one void.
Argue, then recommend.
Separate: known vs CANDIDATE.
```

---

## 8. Insight → product

```text
From this insight bank:
1) Void-language hero line (user words only)
2) MVP that automates the top workaround
3) Non-goals for the demo
4) Archetype the product fulfills (one sentence)
5) Riskiest assumption + cheapest test before more code
```

---

## 9. Storyteller / pitch

```text
Insight Storyteller.
Outputs: Top 3 struggles (plain English) + 90s pitch spine + demo script.
Rules: exact field phrases; no generic AI-startup filler; one void closed.
Insight bank:
{...}
```

---

## 10. Bank / Archiva

```text
Archiva: bank the most important insights as INSIGHT STORIES.
For each: context → tension → evidence quotes → so-what → confidence → validation next.
Then: void lexicon table, decisions, cuts, still unknown.
```

---

## 11. Mid-hackathon standup

```text
Village check-in:
1) Living question still correct? (yes/no + rewrite)
2) Strongest field quote since last check
3) Riskiest product claim still unvalidated
4) Cut one thing from scope
5) Next 3-hour demo spine
@Detective @Decider — argue if needed, then decide.
```

---

## 12. Emergency lost

```text
We're lost mid-hackathon.
Raw dump:
{what we built / think / heard}

1) Reconstruct the living question we should have
2) Name the void we ignored
3) Smallest demo that closes that void
4) Delete list for next 30 minutes
@Decider leads. @Detective may only block if the question is wrong.
```

---

## 13. Pre-pitch drill

```text
Using ONLY field language from the insight bank:
- 15s hook
- 45s problem (void)
- 60s product moment
- 30s proof (quotes/models)
- 15s ask
Flag any sentence that sounds like generic AI startup.
```

---

## 14. Hallucination principles inject

```text
Crystallize the following into 8–12 POSITIVE principles our scouts/elders must abide by.
Do not store as a long "don't do" list.

Source material:
{papers / HMG notes / failure modes}

Also produce a short "all scouts follow these principles" block to paste into instructions.
```

---

## 15. Counter-study

```text
Design a COUNTER-STUDY to our thesis.
Thesis: {...}
What would we see in the field if we were wrong?
Which territory would show falsification fastest?
Run a landscape there. Do not defend the thesis.
```

---

## 16. Guide mode switch

```text
Mode: GUIDE for the next 10 minutes.
Do not give the answer. Socratic only.
Goal: unlock whether our living question is wrong.
```

---

## 17. Oracle mode switch

```text
Mode: ORACLE.
We trust the bank. Give the sharpest demo path and cut list now.
```

---

## 18. ChatGPT / non-skills portability glue

```text
You have skill documents in this project.
Whenever I say a skill name (e.g. "Brief Builder", "Reddit Scout"),
read that skill and follow it exactly until I say stop.
Skills:
{paste or list files}
```

---

## 19. Voice dump helper (if no Whisper)

```text
I will paste an unedited brain dump. Do not judge prose.
Run Brief Builder on it. Preserve almost-said content; ask about anything I half-named.
```

---

## 20. Claims whitelist for stage

```text
From the insight bank, produce:
ON-STAGE WHITELIST (only HIGH confidence with quotes)
BACKSTAGE CANDIDATES (interesting but not claimed)
FORBIDDEN (tempting but unsupported)
```

---

## 21. Layer-1 framing (pre-verbal)

```text
Reframe this product idea using the 5 insight layers.
Force a Layer-1 living question (unnamed felt need).
Do not start at rationalization (Layer 4) or behavior (Layer 5).
Idea:
{...}
```

---

## 22. Village loop status check

```text
Score our project against the village loop:
L1 Sensing / L2 Synthesizing / L3 Shaping / T1 Strategizing / T2 Structuring / T3 Syncing
For each: done | weak | missing. What one upgrade next?
```

---

## 23. Trust gate (decision-grade)

```text
Run trust checks on these claims:
Transparent? Rigorous? Unbiased? Segmented? Triangulated?
Flag language distortion, missing sources, harm, or leap.
Claims:
{...}
```

---

## 24. Interrogate the brief (briefing village)

```text
Interrogate this client/hackathon brief before we research or build.
Use five-whys, audience split, pain-holder, living question, void language.
Do not research yet. Output: sharpened commission or reject-as-unclear.
Brief:
{...}
```

---

## 25. Per-territory brief split

```text
Split this commission into separate territory briefs
(Reddit / Reviews / X / …). Each keeps the same living question
but tailored hunt/avoid/filter for that platform's ontology.
Master commission:
{...}
```

---

## 26. Scout skill builder recipe

```text
Build a scout skill for {platform or niche}.
Include: platform ontology, modes, tools/hands, analytical frameworks to embed,
hunt list, avoid/filter list, evidence rules (URLs), output format.
Then: please make the skill as downloadable markdown.
```

---

## 27. Village audit

```text
Audit this village after our last edits:
redundant scouts/elders, broken @dependencies, missing HMG,
invasive elders, global vs project skill leakage, orphan manuals.
Recommend exact fixes.
```
