---
name: generational-audit
description: Audite un projet tech (code source + expérience rendue) et évalue son adéquation à 5 cohortes générationnelles (Boomers, Gen X, Millennials, Gen Z, Gen Alpha). Produit un rapport markdown et un JSON exploitable. Utiliser quand l'utilisateur demande un audit générationnel, une analyse d'audience, une évaluation cross-génération, ou veut savoir quelle génération un produit cible réellement.
---

# Generational Audit Skill

## Objet

Évaluer l'adéquation d'un projet tech (web app, mobile, script, SaaS, site) à 5 cohortes générationnelles, sur la base de critères UX/UI/produit sourcés.

## Limites épistémiques (à rappeler dans chaque rapport)

Les générations sont des **moyennes statistiques**, pas des déterminismes individuels. Le contexte (CSP, géographie, expertise numérique) pèse souvent autant que l'année de naissance. Cette skill produit des **hypothèses d'adéquation**, pas des prédictions de comportement.

## Périmètre d'audit (les deux modes obligatoires)

L'audit combine systématiquement :

1. **Audit du code source** (statique)
   - Lecture des fichiers : framework, deps, composants UI, accessibilité, patterns
   - Détection : stack, taille de police, contrastes déclarés, dark mode, i18n, breakpoints, gestion clavier, ARIA
   - Outils : `grep`, lecture de `package.json`, `tailwind.config`, fichiers CSS, composants

2. **Audit de l'expérience rendue** (dynamique)
   - Si URL fournie : `web_fetch` de la page principale + 2-3 pages clés
   - Si screenshots fournis : analyse visuelle directe
   - Détection : densité texte, hiérarchie visuelle, friction onboarding, trust signals, modes de paiement visibles

Si l'un des deux n'est pas accessible, le déclarer explicitement dans le rapport et baisser le niveau de confiance.

## Procédure (5 phases obligatoires)

### Phase 1 — Inventaire

Collecter et déclarer :
- Type de projet (web app, mobile, script CLI, SaaS, vitrine, jeu, etc.)
- Stack technique
- Public cible déclaré (si mentionné dans README, landing, brief)
- Marché géographique (France, EU, US, autre — par défaut France si non précisé)
- Secteur (e-commerce, culturel, B2B, etc.)

Charger les références applicables : `references/gen-*.md`.

### Phase 2 — Analyse par dimension

Pour chaque dimension de `criteria/`, scorer 0-5 par génération.

Dimensions obligatoires :
- `ui-patterns.md` — patterns visuels et navigation
- `interaction-models.md` — gestes, clavier, voix, recherche
- `accessibility.md` — contraste, taille, ARIA, clavier
- `content-density.md` — texte/visuel, longueur, scannabilité
- `trust-signals.md` — preuves sociales, certifications, sécurité

Échelle :
- 0 : bloquant pour cette génération
- 1-2 : friction forte
- 3 : neutre / acceptable
- 4 : bien adapté
- 5 : optimisé pour cette génération

### Phase 3 — Score global pondéré

Pondération par défaut (modifiable selon secteur) :
- UI patterns : 20%
- Interaction : 20%
- Accessibilité : 25% (poids fort, légalement requis en EU)
- Densité contenu : 20%
- Trust signals : 15%

Score /100 par génération + niveau de confiance (haute / moyenne / basse) basé sur la quantité de données collectées.

### Phase 4 — Identification des frictions

Pour chaque génération, lister **top 3 frictions concrètes** :
- Composant ou fichier en cause (chemin exact si code source)
- Description de la friction
- Source/critère qui la justifie

### Phase 5 — Recommandations actionnables

Format strict :
`[Génération cible] → [Zone du produit] → [Action concrète] → [Effort: S/M/L]`

- S : < 1 jour
- M : 1-5 jours
- L : > 5 jours ou refonte

Maximum 15 recommandations, triées par ratio impact/effort.

## Sorties (les deux formats obligatoires)

1. **Rapport markdown** : `templates/audit-report.md` rempli
2. **JSON exploitable** : structure définie dans `templates/audit-schema.json`

Les deux sont produits systématiquement, même si l'utilisateur n'en demande qu'un.

## Garde-fous

- **Sourcing obligatoire** : chaque affirmation générationnelle dans le rapport doit pointer vers une source dans `references/` ou `criteria/`. Pas d'affirmation hors-source.
- **Pas d'essentialisation** : éviter les formulations type « les Gen Z sont… ». Préférer « les études X montrent que la majorité des Gen Z dans le contexte Y… ».
- **Géo-sensibilité** : si le marché cible n'est pas FR, alerter sur la limite des sources francophones.
- **Datation** : privilégier sources < 3 ans. Mentionner la date de chaque source.

## Workflow d'exécution

```
1. Lire SKILL.md (ce fichier)
2. Lire references/*.md (5 fichiers cohortes)
3. Lire criteria/*.md (5 fichiers dimensions)
4. Lire templates/audit-report.md et audit-schema.json
5. Exécuter les 5 phases
6. Produire les 2 sorties
```

## Quand NE PAS utiliser cette skill

- Audit purement technique (perf, sécurité) sans dimension UX
- Étude de marché quantitative (cette skill est qualitative)
- Recommandations marketing (channel mix, pub) — hors périmètre
