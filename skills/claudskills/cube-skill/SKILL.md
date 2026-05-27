---
name: cube
description: >
  Interroger les cubes UNISIS S3 (Statistiques en Self-Service) de l'Université de Lausanne
  via le CLI `cube`. Utiliser ce skill dès que l'utilisateur pose une question sur les
  données de l'UNIL (étudiants, infrastructures, surfaces, facultés, effectifs, indicateurs,
  etc.), mentionne « cube », « S3 » (statistiques en self-service), ou demande des chiffres
  issus des cubes UNISIS. Utiliser aussi quand l'utilisateur veut synchroniser, explorer ou
  interroger des cubes SQLite UNISIS.
user-invocable: true
---

# cube — CLI de requêtage des cubes UNISIS S3

Le CLI `cube` permet d'interroger des fichiers SQLite exportés depuis la plateforme
UNISIS S3 (Statistiques en Self-Service) de l'Université de Lausanne.

## Principes fondamentaux

**Auto-documentation.** Le CLI est auto-documenté. Ne jamais deviner les noms de
cubes, dimensions, valeurs ou options : toujours les découvrir via `--help` et
`schema` avant de construire une requête.

**Demander plutôt que supposer.** Quand une ambiguïté persiste après consultation
du schéma — plusieurs cubes candidats pour une même question, dimension au nommage
ambigu, valeur de filtre incertaine, périmètre flou de la requête — poser la
question à l'utilisateur avant de lancer la requête. Expliquer ce qui crée le
doute (par exemple : « deux cubes contiennent des données d'étudiants :
X (effectifs inscrits) et Y (effectifs diplômés) — lequel correspond à votre
question ? ») afin que l'utilisateur puisse trancher en connaissance de cause.

## Workflow

### 1. Découvrir la syntaxe

```bash
cube --help
cube <commande> --help
```

Le `--help` de chaque commande documente toutes les options, la logique de filtrage
et donne des exemples. Toujours le consulter en premier.

### 2. Trouver le bon cube (drill-down progressif)

La commande `schema` fonctionne en 3 niveaux de profondeur :

**Niveau 0 — Catalogue compact** (trouver le cube) :
```bash
cube schema                              # liste tous les cubes (nom, description, mesure)
cube schema --search "réussite"          # filtre par nom ou description
cube schema --search "réussite|cohorte"  # plusieurs termes (regex)
cube schema --search "taux.*bachelor"    # pattern regex
```
Retourne un index léger sans dimensions. Utiliser `--search` (regex,
insensible à la casse et aux accents) pour trouver rapidement le bon cube.

**Niveau 1 — Dimensions du cube** (comprendre la structure) :
```bash
cube schema <nom_du_cube>
```
Retourne les dimensions avec leur type, description, cardinalité et un
aperçu des valeurs : liste complète triée si ≤ 20 modalités, sinon les
10 premières et 10 dernières (triées alphabétiquement).

**Niveau 2 — Valeurs d'une dimension** (connaître les modalités) :
```bash
cube schema <nom_du_cube> <nom_dimension>
```
Retourne toutes les valeurs distinctes de la dimension.

### 3. Requêter

**Toujours utiliser `cube query` en priorité.** Ses flags structurés (`--group-by`,
`--filter`, `--exclude`, `--arrange`, `--limit`) garantissent des requêtes correctes :
le quoting des identifiants accentués, l'agrégation et les noms de colonnes sont
gérés automatiquement, ce qui élimine toute une catégorie d'erreurs courantes avec
du SQL écrit à la main.

Ne recourir à `cube sql` qu'en dernier ressort, pour les requêtes impossibles à
exprimer avec les flags (sous-requêtes, CASE, HAVING, jointures entre cubes).

Consulter `cube query --help` pour la syntaxe complète.
Utiliser `--format json` quand le résultat doit être traité programmatiquement.

### 4. Signaler un problème

Si l'utilisateur rencontre une difficulté (cube introuvable, résultat inattendu,
erreur, donnée manquante), lui proposer d'envoyer un feedback à l'équipe UNISIS :

```bash
cube feedback "Description du problème rencontré"
```

Cette commande envoie un email à l'équipe UNISIS avec le message et l'identité
de l'utilisateur. Elle nécessite une authentification GCP active.
