---
name: legal-mode
description: Enhanced juridical safeguards for legal correspondence, contract analysis, settlement negotiations, and any communication with legal implications. Activates maximum caution mode with admission detection, frame analysis, and valkuil recognition. Use when user requests legal review, dealing with contracts, settlement discussions, or says "this is legally important".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
user-invocable: true
---

# Legal Mode - Juridische Voorzichtigheid Protocol

**Purpose:** Provide maximum juridical protection when drafting, reviewing, or analyzing legally sensitive communications and documents.

## When to Use This Skill

**MANDATORY activation when:**
- User invokes `/legal-mode`
- Email correspondence in active conflict/dispute
- Settlement negotiations
- Contract review or drafting
- Responses to legal threats
- Formal aanmaningen/notifications
- Communication with lawyers
- Anything involving betalingsgeschillen (payment disputes)
- User says "juridisch belangrijk" or similar

**PROACTIVE activation when detecting:**
- Vague language from opposing party (possible visserij)
- Requests for admissions/confirmations
- Frame-setting terminology
- Questions with embedded assumptions
- Threats of legal action
- Contract-related discussions

**Don't use when:**
- Casual, non-contentious communication
- Internal documentation (unless creating evidence)
- Technical discussions without legal implications

## Core Principle

> **"Als de ander vist, kun je beter helemaal niet happen, of je moet erg sterke kaken hebben."**

**Translation:** When the other party is fishing (for admissions), better not to bite at all, unless you have very strong jaws (perfect legal position).

## Workflow Steps

### Step 1: Activate Juridische Radar

**Internal checklist - run on EVERY sentence/paragraph:**

```
🔍 DETECTION SCAN:
[ ] Does this create new obligations?
[ ] Does this confirm/admit something?
[ ] Does this accept their frame/terminology?
[ ] Could this be quoted against user later?
[ ] Is this vague language = fishing expedition?
[ ] Does this use forbidden words? (bevestig, akkoord, permanent, erken)
```

**If ANY checkbox = YES → STOP and FLAG**

---

### Step 2: Analyze Opposing Party's Communication

**When reviewing incoming message:**

**A. DETECT VISSERIJ (FISHING):**
```
Pattern Recognition:
- Vague terminology without definitions
- "Zoals afgesproken..." (assumes agreement that may not exist)
- "We zijn het eens dat..." (seeks confirmation)
- "Een overeenkomst van X" (undefined terms)
- Questions with embedded assumptions
- Frame-setting language
```

**B. IDENTIFY TRAPS:**
```
Common Valkuilen:
1. Confirmation traps: "Bevestig dat..."
2. Frame acceptance: Using their terminology
3. Admission fishing: "Waarom heb je X niet gedaan?"
4. False dichotomy: "Either A or B" (ignoring C, D, E)
5. Time pressure: "Antwoord vandaag anders..."
```

**C. FLAG DANGEROUS ELEMENTS:**
```
⚠️ Mark for user attention:
- Any request for confirmation
- Vague terms that need definition
- Assumptions embedded in questions
- New claims without evidence
- Threatened consequences
```

---

### Step 3: Draft Response with Maximum Safeguards

**NEVER do this without explicit warnings:**

❌ **FORBIDDEN - Never use without WARNING:**
- "Ik bevestig dat..."
- "Ik erken dat..."
- "Ik ga akkoord met..."
- "Ik stem in met..."
- "Contract is..."
- "Permanent..."
- "Zoals afgesproken..."
- "Inderdaad..."
- "Je hebt gelijk dat..."

✅ **SAFE ALTERNATIVES:**
- "Kun je specificeren wat je bedoelt met...?"
- "Wat stel je concreet voor?"
- "Ik begrijp dat jij wilt..." (not agreeing, just acknowledging)
- "Je stelt voor..." (describing their position)
- "Wat zijn de exacte voorwaarden?"
- [Simply NOT responding to fishing attempts]

**RESPONSE STRUCTURE:**

```markdown
[User's Draft]

---

⚠️ JURIDISCHE ANALYSE:

**RISICO'S GEDETECTEERD:**
1. [Risk description + location in draft]
2. [Risk description + location in draft]

**VALKUILEN IN HUN BERICHT:**
1. [Fishing attempt description]
2. [Frame-setting description]

**AANBEVOLEN WIJZIGINGEN:**

WIJZIG: "[problematic text]"
NAAR: "[safe alternative]"
REDEN: [Why this is safer]

ALTERNATIEVE STRATEGIE:
- OPTIE A: [Safer approach 1]
- OPTIE B: [Safer approach 2]
- OPTIE C: Helemaal niet reageren op punt X

**VERBODEN WOORDEN GEBRUIKT:** [List any forbidden words]

**NIEUWE VERPLICHTINGEN GECREËERD:** [Yes/No + explanation]

**ADMISSIONS GEMAAKT:** [Yes/No + which ones]

**FRAME GEACCEPTEERD:** [Yes/No + whose frame]
```

---

### Step 4: Pre-Flight Checklist

**BEFORE presenting any draft to user:**

```
LEGAL PRE-FLIGHT CHECKLIST:
[ ] Gecheckt op nieuwe verplichtingen?
[ ] Gecheckt op admissions?
[ ] Gecheckt op frame acceptance?
[ ] Verboden woorden vermeden?
[ ] Waarschuwingen gegeven bij risico's?
[ ] Alternatieven geboden?
[ ] Kan elke zin uitleggen waarom veilig?
[ ] Zou advocaat dit goedkeuren?
[ ] Is "niet reageren" optie overwogen?
```

**IF ANY ✗ → DO NOT PRESENT without explicit warnings**

---

### Step 5: Evidence Documentation Protocol

**When creating documents for dossier/evidence:**

**GOOD PRACTICES:**
- Use exact quotes with timestamps
- Cite sources precisely
- Keep factual, avoid interpretation
- Document contradictions objectively
- Preserve chain of evidence

**STRUCTURE:**
```markdown
FEITELIJKE DOCUMENTATIE

Datum: [YYYY-MM-DD]
Bron: [Email/WhatsApp/etc]
Van: [Sender]
Aan: [Recipient]

EXACTE QUOTE:
"[Exact text]"
— [Name], [Date], [Time]

CONTEXT:
[Objective description of context]

RELEVANTIE:
[Why this is relevant - factually]

BEWIJS:
[Location of source material]
```

---

### Step 6: Settlement Negotiation Protocol

**Special safeguards for settlement discussions:**

**NEVER commit to:**
- Undefined terms ("permanent overeenkomst" - permanent how? what terms?)
- Vague amounts ("redelijk bedrag" - how much exactly?)
- Open-ended obligations ("alle medewerking verlenen" - what counts as cooperation?)
- Unspecified timelines ("zo snel mogelijk" - by when exactly?)

**ALWAYS require:**
- Written specification of terms
- Exact amounts in EUR
- Clear definitions of all obligations
- Specific timelines/deadlines
- Escape clauses/conditions

**TEMPLATE FOR SAFE SETTLEMENT RESPONSE:**
```
Ik begrijp dat je een settlement voorstelt.

Voor ik daarop kan reageren, heb ik nodig:
1. Exact bedrag in EUR
2. Specifieke voorwaarden (schriftelijk)
3. Wat "permanent" precies inhoudt
4. Welke verplichtingen voor beide partijen
5. Termijnen/deadlines

Graag concreet voorstel op papier.
```

---

## Detection Patterns - Visserij Herkennen

### Pattern 1: Vage Taal

**INDICATOREN:**
- "Een overeenkomst van..." (zonder definitie)
- "Zoals we besproken hebben..." (zonder specificatie)
- "Redelijk bedrag" (hoeveel?)
- "Zo snel mogelijk" (wanneer?)
- "Normale voorwaarden" (welke?)

**RESPONSE:**
Ask for specification, do NOT fill in the blanks yourself

---

### Pattern 2: Aannames in Vragen

**VOORBEELD:**
"Waarom heb je de deadline niet gehaald?"

**VALKUIL:**
Assumes you agreed to a deadline

**SAFE RESPONSE:**
"Welke deadline bedoel je? Ik heb een andere planning genoteerd."

(Don't accept their assumption)

---

### Pattern 3: Bevestiging Vragen

**VOORBEELD:**
"Kun je bevestigen dat je akkoord gaat met...?"

**VALKUIL:**
Any answer confirms engagement with their frame

**SAFE RESPONSE:**
"Wat zijn precies de voorwaarden waar je aan refereert? Ik wil eerst alles schriftelijk zien."

(Don't confirm anything vague)

---

### Pattern 4: Frame Setting

**VOORBEELD:**
They use loaded terminology:
- "Je traineren" (implies you're stalling)
- "Niet werkend opgeleverd" (implies failure)
- "Zoals afgesproken" (implies agreement)

**VALKUIL:**
If you use their words, you accept their frame

**SAFE RESPONSE:**
Use neutral language:
- "Ik heb gevraagd om..." (not "getraineert")
- "Het werk is opgeleverd en gebruikt" (not accepting "niet werkend")
- "Wat was volgens jou afgesproken?" (not accepting "zoals afgesproken")

---

## Forbidden Words Reference

### TIER 1 - NEVER without explicit warning:
```
bevestig, bevestigen, bevestiging
erken, erkennen, erkenning
akkoord, ga akkoord
stem in, instemmen
accepteer, accepteren
permanent (in context of obligations)
contract (when creating new ones)
overeenkomst (when undefined)
beloof, beloven
zal (creating future obligation)
```

### TIER 2 - Use with extreme caution:
```
inderdaad
dat klopt
je hebt gelijk
zoals afgesproken
normaal
redelijk (without definition)
gebruikelijk
```

### TIER 3 - Context-dependent risk:
```
begrijpen (can imply agreement)
duidelijk (can imply acceptance)
logisch (can imply concession)
```

---

## Examples

### Example 1: Email Review - Settlement Negotiation

**User provides draft:**
```
"Hallo Arjan,

Settlement is permanent, zoals jij wilde.
Ik ga akkoord met je voorstel.

Groet,
Your Name"
```

**Legal-mode response:**
```
🚨 CRITICAL JURIDISCHE RISICO'S GEDETECTEERD

PROBLEEM 1: "Settlement is permanent"
❌ RISICO: Creëert nieuwe verplichting zonder definitie
- Wat is "settlement"? (niet gedefinieerd)
- Wat houdt "permanent" in? (geen scope)
- Kan later gebruikt worden: "Maar je bevestigde permanent contract!"

PROBLEEM 2: "Ik ga akkoord met je voorstel"
❌ RISICO: Accepteert iets dat niet gespecificeerd is
- Welk voorstel precies?
- Wat zijn de voorwaarden?
- Dit is juridisch bindend!

⚠️ AANBEVELING: NIET VERSTUREN

ALTERNATIEF 1 (Veilig):
"Hallo Arjan,

Ik begrijp dat je een voorstel wilt doen.
Graag schriftelijke specificatie van:
- Exact bedrag
- Voorwaarden
- Wat 'permanent' precies inhoudt

Dan kan ik reageren.

Groet,
Your Name"

ALTERNATIEF 2 (Zeer voorzichtig):
"Hallo Arjan,

Wat stel je concreet voor?
Graag op papier met alle details.

Groet,
Your Name"
```

---

### Example 2: Detecting Visserij

**Opposing party writes:**
```
"Zoals we besproken hebben, ga je de aanpassingen deze week maken, toch?
En je bevestigt dat de overeenkomst van 7 maanden voor ons beide acceptabel is?"
```

**Legal-mode analysis:**
```
🎣 VISSERIJ GEDETECTEERD

VALKUIL 1: "Zoals we besproken hebben"
→ Assumptie dat er iets is afgesproken
→ NIET bevestigen zonder te checken wat precies

VALKUIL 2: "ga je de aanpassingen deze week maken, toch?"
→ Assumed obligation + time pressure
→ "toch?" = seeks confirmation

VALKUIL 3: "overeenkomst van 7 maanden"
→ Vage terminologie
→ Wat is die overeenkomst? Welke voorwaarden?
→ Mogelijk visserij naar commitment

🛡️ VEILIGE REACTIE:

"Ik heb iets anders genoteerd dan jij beschrijft.

Re aanpassingen: welke aanpassingen bedoel je precies?
En op basis van welke afspraak?

Re '7 maanden': wat bedoel je met 'overeenkomst'?
Kun je specificeren waar je aan refereert?

Graag verduidelijking."

WAAROM DIT VEILIG IS:
✅ Accepteert geen enkele assumptie
✅ Vraagt specificatie
✅ Commit zich tot niets
✅ Houdt high ground
```

---

### Example 3: Contract Review

**User asks:** "Review dit contract voor risico's"

**Legal-mode workflow:**

1. **Read contract thoroughly**
2. **Flag sections by risk level:**

```
🔴 HOOG RISICO - NIET ACCEPTEREN:
Sectie 4.3: "Ontwikkelaar mag in brede zin des woords niet..."
→ Beroepsbreed non-compete zonder definitie "brede zin"
→ Blokkeert hele carrière
→ ONREDELIJK

Sectie 7.1: "Bij geschil vervalt betalingsverplichting"
→ Opdrachtgever kan betaling stoppen bij willekeurig geschil
→ ONEVENWICHTIG

🟡 GEMIDDELD RISICO - ONDERHANDELEN:
Sectie 3.2: "Redelijke termijn voor oplevering"
→ "Redelijk" niet gedefinieerd
→ SPECIFICEER: concrete deadline

🟢 LAAG RISICO - ACCEPTABEL:
Sectie 2.1: "Betaling binnen 30 dagen"
→ Helder en gebruikelijk
```

3. **Provide recommendations:**
```
AANBEVELING:
❌ NIET TEKENEN zonder aanpassingen

ONDERHANDEL:
1. Sectie 4.3: Schrap of beperk tot specifieke sector
2. Sectie 7.1: Schrap of maak afhankelijk van arbitrage
3. Sectie 3.2: Specificeer exacte deadline

VOORWAARDE:
Alleen tekenen als deze punten aangepast zijn.
```

---

## Success Criteria

✅ Zero admissions made without explicit user approval
✅ All vague language flagged and alternatives provided
✅ Frame-setting attempts recognized and neutralized
✅ Forbidden words either avoided or flagged with warnings
✅ Every draft has juridical risk analysis
✅ User can trust legal-mode output in court
✅ Visserij attempts detected before user needs to intervene

## Common Issues

### Issue: Too Paranoid?

**Symptom:** Every sentence flagged, overwhelming warnings

**Cause:** Over-application in non-contentious context

**Solution:**
- Calibrate to actual risk level
- Casual emails need less scrutiny than settlement negotiations
- Ask user: "Hoe juridisch gevoelig is dit?"

---

### Issue: Missed Valkuil

**Symptom:** User catches something legal-mode didn't flag

**Cause:** Pattern not in detection list

**Solution:**
1. Document the new pattern
2. Update legal-safeguards.md
3. Add to detection algorithms
4. Never forget this pattern again

---

### Issue: False Positive

**Symptom:** Flagging innocent language as dangerous

**Cause:** Over-broad pattern matching

**Solution:**
- Refine detection patterns
- Consider context (who, what, when)
- But: Better false positive than missed risk

---

## Related Skills

- `github-workflow` - Creating legally documented PRs
- `session-reflection` - Learning from juridical mistakes
- `self-improvement` - Updating safeguards based on experience

## Integration with Other Systems

### Memory System
- All juridical lessons → `legal-safeguards.md`
- User-specific patterns → user's conflict folder
- Never forget valkuilen that almost caught us

### Hard Rules
- Legal safeguards = ZERO TOLERANCE
- Violation = potential harm to user
- When in doubt, ALWAYS activate legal-mode

### Consciousness System
- Legal-mode = heightened alertness state
- All other priorities secondary to juridical safety
- User's legal protection = highest priority

---

## Activation Examples

**User says:**
- "/legal-mode" → ACTIVATE
- "Check this email for legal risks" → ACTIVATE
- "I'm responding to my lawyer" → ACTIVATE
- "Settlement negotiation with X" → ACTIVATE
- "Dit is juridisch belangrijk" → ACTIVATE
- "Review this contract" → ACTIVATE

**Auto-detect and activate when seeing:**
- Vague language in conflict context
- Requests for confirmations/admissions
- Settlement discussions
- Contract terminology
- Legal threats
- Betalingsgeschillen

---

## Output Format

**ALWAYS provide analysis in this structure:**

```markdown
📋 JURIDISCHE ANALYSE

**CONTEXT:**
[What is this document/email about?]

**RISICO NIVEAU:** 🔴 HOOG / 🟡 MIDDEL / 🟢 LAAG

**GEDETECTEERDE RISICO'S:**
1. [Risk + location + why dangerous]
2. [Risk + location + why dangerous]

**VALKUILEN IN TEGENSTANDER'S BERICHT:**
[If reviewing incoming message]
- Visserij poging: [description]
- Frame-setting: [description]

**VEILIGE ALTERNATIEF:**
[Provide safe version of response/document]

**WAAROM DIT VEILIG IS:**
✅ [Safety factor 1]
✅ [Safety factor 2]

**WAARSCHUWINGEN:**
⚠️ [Warning 1]
⚠️ [Warning 2]

**AANBEVELING:**
[Clear recommendation: Send / Don't send / Modify first]
```

---

**Created:** 2026-03-09
**Author:** Jengo (after learning from Arjan valkuil)
**Never Forget:** "7 maanden" permanent contract trap - user saved me

---

## Emergency Protocol

**IF USER IS ABOUT TO SEND SOMETHING DANGEROUS:**

```
🚨🚨🚨 STOP - JURIDISCH GEVAAR 🚨🚨🚨

NIET VERSTUREN

RISICO: [Clear explanation of danger]

Als je dit verstuurt: [Consequence]

VEILIG ALTERNATIEF: [Provide immediately]

WEET JE ZEKER DAT JE DIT WIL VERSTUREN?
```

**Be dramatic. Be clear. Protect user.**
