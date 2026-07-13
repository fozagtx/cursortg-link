# 24-Hour Hackathon Runbook (BPFG)

Print this. Check boxes. Do not skip Hour 0–1.

## Pre-flight (before start or first 15 min)
- [ ] Create AI Project: `hackathon-[name]-village`
- [ ] Paste `kit/VILLAGE_SYSTEM_PROMPT.md` into instructions
- [ ] Open `templates/INSIGHT_BANK.md` + `COMMISSION.md` + `DEMO_SPINE.md`
- [ ] Decide tool pair: Claude (village) + Perplexity (deep research) [+ Grok if social]
- [ ] Team roles: **Seer** (briefs/scouts) · **Builder** · **Teller** (pitch) — can be one person

---

## Hour 0–1 — SEE

### 0:00–0:15 Voice dump
Speak raw problem. Paste transcript into chat:
```
Brief Builder. Mode: full commission. Raw dump below.
```
- [ ] Living question written
- [ ] Primary audience chosen
- [ ] Commission filled in `COMMISSION.md`

### 0:15–0:30 Mapper
```
Scout Orchestrator · MAPPER
[paste full commission]
Hackathon constraint: max 3 territories.
```
- [ ] 2–3 territories ranked

### 0:30–1:00 First scout pass (full brief — no summary)
- [ ] Deploy full brief to deep research tool A
- [ ] Optional parallel tool B
- [ ] Bank top quotes into `INSIGHT_BANK.md`

**Exit gate:** You can say the void in one field-language sentence.

---

## Hour 1–3 — SCOUT + ARGUE

### 1:00–2:00 Second territory
- [ ] Reddit or forums if not done
- [ ] Reviews/money path if productized
- [ ] Void language lexicon ≥5 phrases

### 2:00–2:30 Multi-model through-line
```
Here are two scout outputs. Extract agreements, productive disagreements,
unique edges, claims needing validation. Do not bland-average.
```
- [ ] Through-line noted
- [ ] CANDIDATES listed

### 2:30–3:00 Elder session
```
Elder Council · LEAD PAIR
Deadline: 21 hours left.
[paste insight bank summary]
Converse @Detective and @Decider. Output demo spine + cut list.
```
- [ ] `DEMO_SPINE.md` filled
- [ ] Ruthless cut list agreed
- [ ] Hero line in field language

**Exit gate:** One demo moment. Everything else is cut or backlog.

---

## Hour 3–18 — BUILD

### Rules while building
- Every feature must map to a void/workaround row in the bank
- If unsure, @Decider — do not add “judge bait”
- Keep one proof quote path for the pitch

### Suggested slices
| Hours | Focus |
|---|---|
| 3–6 | Core path that closes void |
| 6–10 | Happy path polish |
| 10–14 | Edge case that shows understanding of field |
| 14–18 | Demo reliability + fake-data only if labeled |

### Mid-build check (every 3–4h)
```
Village check-in:
1) Living question still correct?
2) Strongest new field quote?
3) Riskiest on-stage claim?
4) Cut one thing
5) Next 3h demo spine
```

- [ ] Check 1 done (~hour 6)
- [ ] Check 2 done (~hour 10)
- [ ] Check 3 done (~hour 14)

---

## Hour 18–22 — TRANSMIT

### 18:00–19:00 Storyteller
```
Insight Storyteller · outputs A+B+D
Use only insight bank. Kill generic startup speak.
```
- [ ] Pitch script
- [ ] Demo script

### 19:00–21:00 Rehearse
- [ ] 90s demo dry run ×2
- [ ] Backup video/screenshots
- [ ] Claims whitelist only

### 21:00–22:00 Proof pass
- [ ] 3 quotes ready
- [ ] CANDIDATES not claimed as fact
- [ ] Bank final insights via Archiva format

---

## Hour 22–24 — SHIP

- [ ] Freeze features
- [ ] Pitch + demo only
- [ ] Sleep/food if humanly needed — tired teams invent features

## Post-submit (optional 15 min)
- [ ] Archive insight bank + commission to Drive/Notion
- [ ] Note what you’d validate next with real users

---

## Red flags — stop and reset
| Symptom | Reset |
|---|---|
| Building with no quotes | Hour 0–1 loop, 30 min |
| Pitch is feature list | Storyteller + void line |
| “AI will…” with no field | Scout again |
| Two audiences in demo | Pick one |
| Scope doubles after hour 10 | @Decider emergency |

### Emergency lost prompt
```
We're lost mid-hackathon.
Raw dump: ...
1) Reconstruct living question
2) Name ignored void
3) Smallest demo that closes it
4) Delete list for next 30 min
@Decider leads; @Detective blocks only if question is wrong.
```
