# Action required — 2026-09-15

## One command, then one script

```powershell
Remove-Item 'C:\Users\justi\OneDrive\Diabetes_Research\.git\index.lock' -Force
cd 'C:\Users\justi\OneDrive\Diabetes_Research'
.\PUSH_AND_VERIFY.ps1
```

That is the whole ask. Everything below is why.

---

## What changed today

The sandbox **recovered**. Six consecutive runs (09-09 → 09-14) failed with the same
Plan9 mount error and ran no Python at all. Today Python ran: the extraction pipeline
executed, five builders rebuilt, and 25 stale dashboards under `docs/` were republished.

## What is still blocked, and it is narrower than before

`git` is not writable from the sandbox. A stale `.git/index.lock` exists, and the
sandbox cannot unlink anything under `.git` on the OneDrive mount —
`Operation not permitted`. So `git commit` refused.

**Nothing is lost.** Every edit is saved in the working tree on your disk. What is
outstanding is only the commit — seven days of citation repairs plus today's eight,
on top of the 100+ commit backlog that has kept the published site frozen since
2026-04-20.

---

## The finding worth your attention

The queue asked for an author-surname gate: for every `<Surname> et al.` within ~80
characters of a PMID, compare against the paper library's first author.

Built exactly as specified, it reported **103 mismatches**. Inspection of the source
showed **essentially all of them were correctly cited.**

The repo writes citations in semicolon-separated runs:

```
Hoppe et al. ... (PMID:28010783); Zhang et al. ... (PMID:36109742); Clemens et al. ... (PMID:32312859)
```

A *symmetric* window centred on "Zhang" reaches **backwards** and finds Hoppe's PMID
first. Every surname in a list gets tested against its predecessor — a perfect
shift-by-one chain of fake mismatches.

Shipped as written, this gate would have driven mass "correction" of correct
citations. The standing "measure before wiring in" rule is what caught it. That rule
has now stopped three bad gates.

Four false-positive classes were fixed: reverse window straddle, PubMed initials
captured as surnames (`Khan MAB et al.` → `MAB`), slash-joined author runs
(`Reichman/Markmann/Odorico et al.`), and HTML-entity/diacritic folding
(`Abramoff` vs `Abràmoff`).

**Final: 171 attributions checked · 151 confirmed correct · 13 flagged.**
It still reproduces both known-positive test cases, so the reach is real.

---

## Eight false citations fixed

Each verified against NCBI esummary. In four cases the cited PMID was a paper on an
entirely unrelated subject.

| Asserted | Actually was | Action |
|---|---|---|
| `10919952` "Shapiro, NEJM 2000", islet transplant | Zeisel, *dietary supplementation*, Am J Clin Nutr | → `10911004` (×2 instances) |
| `17596481` "Balk, chromium" | Metzger, **gestational diabetes** guideline | → `17519436` (×2 instances) |
| `12122111` "Hundal, salsalate" | Chaisson, **mouse hepatocyte** NF-κB study | → `12021247`; drug also corrected to *aspirin* |
| `24838679` "Antvorskov, dietary gluten" | Galderisi, a single-author *Comment* | → `24871322` |
| `18397984` "Yin et al" | Zhang et al. (PMID supports the claim) | surname corrected |
| `32943753` "Hu, Nature 2020, gasdermin D" | Agrawal, podocyte review, Nat Rev Nephrol | **withdrawn** |
| `18073361` "UKPDS", GADA prevalence | Willi, *smoking and T2D risk*, JAMA 2007 | **withdrawn** (×2) |

Replacements were asserted **only** where esummary confirmed title *and* journal.
A candidate for the berberine trial (`18191047`) was checked and **rejected** — it is
a vitamin D paper — so that surname was dropped rather than guessed.

### One instance no gate could have caught

The Shapiro defect appeared twice. The prose instance was caught by the new gate. The
second was:

```html
<a onclick="alert('PMID: 10919952')">Shapiro et al., NEJM</a>
```

An identifier inside a JavaScript string, with the surname in the anchor text. It was
found only by grepping the *generated HTML* after the fix. These are the clickable
citations a reader actually follows. Queued as P1.

---

## Not fixed — recorded deliberately

The chromium sentence in `build_nutrition_beta.py` claims chromium "enhances insulin
receptor signaling at the cellular level." Its identifier is now correct
(`17519436`, Balk). But Balk is a **clinical systematic review with an equivocal
result** — it tests no cellular mechanism. An inline caveat was added rather than
leave a citation that merely *looks* supported.

This is the more dangerous defect class: a **true** citation attached to a claim it
does not reach. No current gate detects it.
