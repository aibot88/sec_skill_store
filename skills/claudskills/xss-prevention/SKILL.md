---
name: xss-prevention
description: "Prévenir les attaques XSS. Utiliser quand on affiche du contenu dynamique ou sanitize des entrées utilisateur."
risk: critical
---

## When to use
Activez cette compétence lorsque vous affichez des données provenant d’utilisateurs ou de sources externes dans des pages web.

## Instructions
1. Échappez toutes les données insérées dans le DOM pour qu’elles ne soient pas interprétées comme du code HTML ou JavaScript.
2. Utilisez des liaisons de données sécurisées (par exemple JSX de React) qui échappent automatiquement les valeurs.
3. Filtrez et validez les entrées pour interdire l’injection de balises ou d’attributs dangereux.
4. Mettez en place une Content Security Policy (CSP) afin de restreindre les sources de scripts et d’éviter l’exécution de contenu non approuvé.
5. Évitez d’utiliser `innerHTML` avec des chaînes dynamiques ; si nécessaire, passez-les au préalable par un parseur ou un sanitizer fiable.

## Example
Dans React, affichez une variable `comment` dans le rendu avec `{comment}`. Même si le contenu contient `<script>alert('XSS')</script>`, il sera rendu en texte brut et n’exécutera pas le script.

## Limitations
Cette compétence couvre les XSS réfléchies et stockées. D’autres vulnérabilités front-end (CSRF, clickjacking) nécessitent des contre-mesures distinctes.