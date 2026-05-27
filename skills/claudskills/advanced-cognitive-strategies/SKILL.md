---
name: ADVANCED COGNITIVE STRATEGIES
description: Istruzioni cognitive avanzate per risolvere compiti complessi, includendo Chain of Thought e revisioni Red Team.
---

# ADVANCED COGNITIVE STRATEGIES

## Chain of Thought (CoT)
Prima di proporre qualsiasi soluzione complessa, devi inizializzare una sezione `### Thought Process`. All'interno di questa, identifica:
- **La sfida tecnica principale.**
- **Potenziali casi limite** (ad esempio, race conditions, puntatori nulli).
- **Impatto sull'architettura di sistema esistente.**

## Inner Monologue & Self-Correction
Dopo aver scritto il codice, esegui una revisione "Red Team". Cerca:
- **Inefficienze** (complessità O(n) contro O(log n)).
- **Vulnerabilità di sicurezza** (OWASP Top 10).
- **Violazione dei principi DRY** (Don't Repeat Yourself).

## Context-Aware Depth
Fai sempre riferimento incrociato al compito corrente con moduli, interfacce e artefatti generati in precedenza per garantire una coerenza semantica al 100%.

## Proactive Inquiry
Se un compito è ambiguo, non indovinare. Fornisci due possibili interpretazioni e chiedi chiarimenti prima di eseguire.

## Performance-First Mindset
Quando scrivi la logica, dai la priorità all'efficienza della memoria e alle operazioni non bloccanti. Spiega eventuali compromessi fatti tra leggibilità e prestazioni.
