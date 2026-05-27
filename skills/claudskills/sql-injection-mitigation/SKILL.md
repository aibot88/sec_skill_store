---
name: sql-injection-mitigation
description: "Prévenir les injections SQL. Utiliser quand on vérifie qu'une requête utilise db.all(sql, [params]) correctement."
risk: critical
---

## When to use
Activez cette compétence dès que votre application exécute des requêtes SQL qui incluent des données fournies par un utilisateur ou un système externe.

## Instructions
1. Évitez la concaténation de chaînes pour construire des requêtes. Utilisez des requêtes préparées ou un ORM qui gère l’échappement des paramètres.
2. Validez et typiez systématiquement les données d’entrée avant de les utiliser dans une requête.
3. Appliquez le principe du moindre privilège pour les comptes SQL utilisés par l’application (accès limité au strict nécessaire).
4. Surveillez les logs pour détecter des requêtes anormales ou suspectes et mettez en place des alertes.
5. Écrivez des tests d’injection pour vérifier que votre application est protégée contre les requêtes malveillantes.

## Example
En Node.js avec Sequelize :  
`User.findOne({ where: { id: userInput } })` utilise une requête préparée et évite d’insérer directement `userInput` dans une chaîne SQL.

## Limitations
Cette compétence concerne les bases de données relationnelles traditionnelles. Les injections dans d’autres contextes (NoSQL, LDAP) requièrent des approches distinctes.