---
name: gdpr-lgpd-aware
description: Implementa export e delete de dados pessoais por padrão
roles: [dev, cto]
---
Toda entidade ligada a user tem:
- **Export**: endpoint que devolve JSON com tudo daquele user.
- **Delete**: hard delete OU anonimização explícita (substituir PII por hash/null).

Consentimento:
- Granular (separe marketing, funcional, terceiros — nunca um checkbox só).
- Versionado: guarde qual versão do termo o user aceitou e quando.

Retenção:
- Definida por tabela (em política, não só no código).
- Job recorrente apaga/anonimiza dados expirados.

Em incidente, o tempo de resposta é a métrica que pega multa.
