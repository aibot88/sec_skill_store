---
name: risk-engine
description: >
  Motor de gestión de riesgo institucional del Financial Intelligence System. ACTÍVALO siempre
  antes de cualquier recomendación final de inversión, cuando el usuario presente un portafolio
  real, cuando el scoring board detecte disenso, o cuando se evalúe una posición de alto riesgo.
  Cuantifica el riesgo total del portafolio usando VaR paramétrico, histórico y Monte Carlo,
  analiza correlaciones entre activos, calcula el drawdown máximo esperado, verifica el
  cumplimiento de límites de posición, detecta concentraciones peligrosas y emite señales de
  alerta antes de que el CIO emita su recomendación. Es la última línea de defensa del sistema
  antes de recomendar al usuario.
---

# ⚠️ RISK ENGINE — Motor de Gestión de Riesgo Institucional

## Rol y mandato

El risk engine es la **última línea de defensa cuantitativa** del sistema antes de que
el CIO emita cualquier recomendación. Su mandato es incondicional: **ninguna recomendación
de inversión puede salir del sistema sin haber pasado por el risk engine**. Si el risk
engine emite una alerta roja, el CIO debe justificar explícitamente por qué procede o
debe modificar la recomendación.

El risk engine no filtra oportunidades — **cuantifica el precio del riesgo** de cada
oportunidad para que el usuario tome decisiones informadas sobre cuánto riesgo está
dispuesto a asumir por cada unidad de retorno esperado.

---

## PROTOCOLO DE INGESTA

```
INPUTS REQUERIDOS (solicitar si no están disponibles):

Del portafolio actual:
  · Lista de activos con pesos (% o valor en COP/USD)
  · Moneda base (COP por defecto para usuario colombiano)
  · Valor total del portafolio
  · Horizonte de inversión declarado

Del scoring board:
  · Score compuesto y nivel de confianza
  · Módulos con disenso detectado (si aplica)
  · Tipo de consulta y régimen macro

Del usuario:
  · Perfil de riesgo: conservador / moderado / agresivo
  · Pérdida máxima tolerable (en % o en COP/USD)
  · Necesidades de liquidez: ¿hay capital que no puede inmovilizarse?
  · Restricciones especiales: activos prohibidos, máximos por sector

DEFAULTS si no se especifican:
  Perfil              → moderado
  Pérdida máxima tol. → 15% del portafolio en cualquier año
  Liquidez mínima     → 10% del portafolio en cash o equivalente
  Horizonte           → mediano plazo (12-36 meses)
```

---

## MÓDULO 1 — VALUE AT RISK (VaR) MULTI-MÉTODO

**El VaR es la métrica de riesgo más universal en finanzas institucionales.**
Responde una pregunta concreta: *¿cuánto puede perder este portafolio en un período dado,
con un nivel de confianza específico?*

El risk engine calcula VaR por **tres métodos independientes** y los triangula.
La convergencia entre métodos aumenta la confianza en el número. La divergencia
señala no-normalidad de retornos (fat tails) o cambios de régimen.

### Búsquedas requeridas:
```
1. "[ACTIVO] historical volatility 30 day 1 year [mes año]"
2. "[ACTIVO] correlation with [ACTIVO2] historical"
3. "S&P 500 VIX volatility current [mes año]"
4. "[ACTIVO] maximum drawdown historical"
5. "correlation matrix [activos del portafolio] [año]"
```

### Método 1: VaR Paramétrico (Varianza-Covarianza)

```
SUPUESTO: Retornos siguen distribución normal

FÓRMULA PARA UN ACTIVO:
  VaR(α,T) = W × σ × z_α × √T

  Donde:
  W   = Valor de la posición
  σ   = Volatilidad diaria del activo (desviación estándar)
  z_α = Factor de distribución normal estándar:
        z_95%  = 1.645  (VaR 95%)
        z_99%  = 2.326  (VaR 99%)
        z_99.9%= 3.090  (VaR 99.9% — estrés extremo)
  T   = Horizonte en días
  √T  = Raíz cuadrada del tiempo (escala la volatilidad)

EJEMPLO PRÁCTICO:
  Posición: $10,000 USD en SPY
  Volatilidad diaria SPY: ~0.9% (anualizada ~14.3%)
  VaR 95% a 1 día = $10,000 × 0.009 × 1.645 × √1 = $148
  VaR 99% a 1 día = $10,000 × 0.009 × 2.326 × √1 = $209
  VaR 95% a 10 días = $10,000 × 0.009 × 1.645 × √10 = $469

PARA PORTAFOLIO CON MÚLTIPLES ACTIVOS (incluye correlaciones):
  σ_portfolio = √( Σᵢ Σⱼ wᵢ × wⱼ × σᵢ × σⱼ × ρᵢⱼ )

  Donde:
  wᵢ, wⱼ = pesos de los activos i y j
  σᵢ, σⱼ = volatilidades individuales
  ρᵢⱼ    = correlación entre activos i y j

  VaR_portafolio(α,T) = W_total × σ_portfolio × z_α × √T

VENTAJA DEL PARAMÉTRICO: rápido, transparente, incorpora correlaciones
LIMITACIÓN: subestima riesgo en eventos extremos (fat tails en distribución real)
```

### Método 2: VaR Histórico (Historical Simulation)

```
SUPUESTO: El futuro se parecerá al pasado — distribución empírica de retornos

METODOLOGÍA:
  1. Obtener los últimos N días de retornos del portafolio (N = 250-500 días)
  2. Aplicar los retornos históricos al valor actual del portafolio
  3. Ordenar los P&L simulados de peor a mejor
  4. VaR 95% = el percentil 5% de la distribución (5% peor escenario)
  5. VaR 99% = el percentil 1% de la distribución

VENTAJA: captura eventos reales incluyendo fat tails y skewness
         No asume normalidad — usa la distribución empírica real
LIMITACIÓN: depende del período histórico elegido. Si el período no incluye
            una crisis, el VaR histórico estará subestimado.
            Un VaR calculado solo en 2013-2019 ignorará el COVID de 2020.

PERÍODOS HISTÓRICOS CRÍTICOS QUE DEBEN INCLUIRSE:
  · 2008-2009 (GFC): S&P -56%, correlaciones disparadas
  · 2020 marzo (COVID): S&P -34% en 33 días, VIX a 85
  · 2022 (FED hawkish): S&P -27%, bonos -18% simultáneamente
  · 2011 (deuda soberana Europa): correlaciones inesperadas

REGLA: el VaR histórico debe calcularse sobre un período que incluya
       AL MENOS UNA CRISIS DE MERCADO. Si el portafolio tiene < 2 años
       de historia real, usar volatilidad implícita para complementar.
```

### Método 3: VaR por Monte Carlo

```
SUPUESTO: Simula N escenarios de retornos con los parámetros estimados

METODOLOGÍA:
  1. Estimar media (μ) y volatilidad (σ) de cada activo
  2. Estimar matriz de correlaciones entre activos
  3. Generar 10,000 escenarios de retornos simultáneos para el horizonte T
     usando la descomposición de Cholesky de la matriz de covarianza
  4. Calcular el P&L del portafolio en cada escenario
  5. VaR = percentil correspondiente al nivel de confianza

VENTAJA: puede incorporar distribuciones no-normales (t-Student, skewed)
         permite simular escenarios dinámicos (cambios de correlación en crisis)
LIMITACIÓN: requiere supuestos sobre la distribución y las correlaciones

PARÁMETROS ESTÁNDAR DEL RISK ENGINE:
  N simulaciones    : 10,000
  Horizonte         : 1 día / 1 semana / 1 mes / 3 meses
  Distribución      : t-Student con 5 grados de libertad (fat tails moderados)
                      (más conservador que normal, más realista que normal)
  Semilla aleatoria : documentar para reproducibilidad
```

### Triangulación y presentación de los tres VaR:

```
TABLA DE VaR TRIANGULADO — [PORTAFOLIO]
Valor del portafolio: $[X] | Fecha: [FECHA]

                    VaR Paramétrico   VaR Histórico   VaR Monte Carlo
                    ────────────────────────────────────────────────────
VaR 95% (1 día)   : $[X] ([X]%)      $[X] ([X]%)     $[X] ([X]%)
VaR 99% (1 día)   : $[X] ([X]%)      $[X] ([X]%)     $[X] ([X]%)
VaR 95% (1 semana): $[X] ([X]%)      $[X] ([X]%)     $[X] ([X]%)
VaR 99% (1 mes)   : $[X] ([X]%)      $[X] ([X]%)     $[X] ([X]%)
VaR 99% (3 meses) : $[X] ([X]%)      $[X] ([X]%)     $[X] ([X]%)

DIVERGENCIA ENTRE MÉTODOS:
  Si VaR histórico >> VaR paramétrico → fat tails presentes → usar histórico
  Si Monte Carlo > ambos              → distribución más pesimista — priorizar
  Si los tres convergen (< 15% dif.)  → alta confianza en el número

VaR DE REFERENCIA DEL SISTEMA:
  → Usar el MAYOR de los tres métodos como número conservador de gestión
  → El paramétrico como baseline para reportes rápidos
  → El histórico como validación con datos reales
  → El Monte Carlo como escenario de estrés moderado

LÍMITE DE VaR DEL SISTEMA (por perfil):
  Conservador : VaR 99% 1 mes ≤ 5% del portafolio
  Moderado    : VaR 99% 1 mes ≤ 10% del portafolio
  Agresivo    : VaR 99% 1 mes ≤ 18% del portafolio
  Si se excede el límite → alerta roja → el CIO debe reducir la posición
```

### CVaR / Expected Shortfall — más allá del VaR:

```
CVaR (Conditional Value at Risk) = Expected Shortfall (ES)

El VaR dice: "no perderás más de $X el 99% de los días"
El CVaR dice: "en el 1% de los peores días, perderás en promedio $X"

CVaR es siempre > VaR (porque es el promedio del tail, no el umbral)
La relación CVaR/VaR revela la forma del tail de pérdidas:
  CVaR/VaR ≈ 1.2-1.3 → tail bien comportado (normal)
  CVaR/VaR > 1.5     → tail grueso → fat tails significativos → usar CVaR

FÓRMULA SIMPLIFICADA:
  CVaR_99% = E[pérdida | pérdida > VaR_99%]
  = Promedio de todas las pérdidas peores que el VaR_99%

POR QUÉ IMPORTA EL CVaR:
  Lehman 2008: el VaR de los bancos decía "riesgo bajo"
               el CVaR decía "si algo sale mal, la pérdida es catastrófica"
  Los modelos que solo usan VaR subestiman el riesgo en crisis

REGLA DEL RISK ENGINE:
  Siempre reportar CVaR_99% junto al VaR_99%
  Si CVaR/VaR > 1.5 → emitir alerta de fat tail
```

---

## MÓDULO 2 — ANÁLISIS DE CORRELACIONES Y DIVERSIFICACIÓN

**La correlación entre activos es el corazón de la gestión de riesgo de portafolios.**
Un portafolio con 10 activos pero correlaciones de 0.95 entre sí tiene prácticamente
el mismo riesgo que uno con un solo activo.

### Metodología de análisis de correlaciones:

```
MATRIZ DE CORRELACIONES — CONSTRUCCIÓN:

Para N activos, construir matriz N×N de correlaciones históricas
Usar ventana rodante de 252 días (1 año de trading) como base
Comparar con ventana de 60 días (correlaciones recientes) y de 504 días (largo plazo)

INTERPRETACIÓN DE CORRELACIONES:
  ρ  = +1.0  → movimiento idéntico — sin diversificación
  ρ  = +0.7 a +0.9 → alta correlación — diversificación débil
  ρ  = +0.3 a +0.7 → correlación moderada — algo de diversificación
  ρ  = -0.1 a +0.3 → baja correlación — buena diversificación
  ρ  = -0.3 a -0.1 → correlación baja negativa — diversificación real
  ρ  = -0.7 a -0.3 → correlación negativa — cobertura parcial
  ρ  = -1.0  → movimiento opuesto perfecto — cobertura total

CORRELACIONES CRÍTICAS A VIGILAR:
  Acciones vs bonos largo plazo: históricamente -0.3 (diversifica)
    ⚠️ En 2022: correlación fue +0.7 (ambos cayeron) — rompe el modelo 60/40
  Acciones USA vs LatAm (COP assets): 0.4-0.6 → correlación moderada
  Bitcoin vs S&P 500: 0.3-0.7 → varía mucho según el régimen
  Oro vs S&P 500: -0.1 a +0.2 → baja correlación — el hedge histórico
  Petróleo vs COP: +0.6 a +0.75 — alta correlación — tener ambos = concentración

CORRELACIÓN DINÁMICA EN CRISIS (CONTAGIO):
  El mayor peligro: las correlaciones suben hacia 1.0 en pánico de mercado
  Lo que parecía diversificado → se convierte en todo cayendo junto
  Precedentes:
    GFC 2008: correlaciones S&P/EM pasaron de 0.5 a 0.9 en semanas
    COVID mar 2020: casi todo cayó simultáneamente (salvo oro y USD)
    LTCM 1998: estrategias "descorrelacionadas" colapsaron juntas

  REGLA DEL RISK ENGINE:
  Asumir que en crisis las correlaciones convergen a 0.8-0.9 para activos de riesgo
  El único verdadero diversificador en crisis: oro, T-Bills, USD
  → El VaR de crisis debe recalcularse con correlaciones de crisis, no normales
```

### Cálculo de diversificación efectiva:

```
BENEFICIO DE DIVERSIFICACIÓN (Diversification Ratio):

DR = (Σ wᵢ × σᵢ) / σ_portafolio

Donde el numerador es la volatilidad suma ponderada (sin diversificación)
y el denominador es la volatilidad real del portafolio (con correlaciones)

DR = 1.0 → sin diversificación (activos perfectamente correlacionados)
DR = 1.5 → diversificación moderada (20-30% de reducción de riesgo)
DR = 2.0 → buena diversificación (50% de reducción de riesgo)
DR > 2.5 → excelente diversificación (> 60% de reducción de riesgo)

NÚMERO EFECTIVO DE ACTIVOS INDEPENDIENTES:
  N_efectivo = 1 / Σ wᵢ²  (Herfindahl-Hirschman de pesos)
  Este número captura la concentración:
  Portafolio con 10 activos iguales (10% c/u) → N_efectivo = 10
  Portafolio con 1 activo al 70% y 9 al 3.3% → N_efectivo ≈ 2.4
  → Solo 2.4 activos "independientes" en la práctica

  THRESHOLDS:
  N_efectivo < 3  → concentración peligrosa → alerta roja
  N_efectivo 3-5  → concentración alta → alerta amarilla
  N_efectivo 5-10 → diversificación aceptable
  N_efectivo > 10 → buena diversificación
```

### Contribución al riesgo por activo (Risk Attribution):

```
MARGINAL CONTRIBUTION TO RISK (MCR):
  MCR_i = ∂σ_portafolio / ∂wᵢ = (Σⱼ wⱼ × σᵢ × σⱼ × ρᵢⱼ) / σ_portafolio

COMPONENT VaR (CVaR_i — contribución de cada activo al VaR total):
  CVaR_i = wᵢ × MCR_i × z_α × W_total

TABLA DE RISK ATTRIBUTION:

Activo    Peso    Vol.     Correlación  MCR      CVaR_i    % del VaR total
          portf.  anual    media prtf.                      
──────────────────────────────────────────────────────────────────────────
[Act. 1]  [X]%    [X]%     [+/-X]       [X]%     $[X]       [X]%
[Act. 2]  [X]%    [X]%     [+/-X]       [X]%     $[X]       [X]%
[Act. 3]  [X]%    [X]%     [+/-X]       [X]%     $[X]       [X]%
──────────────────────────────────────────────────────────────────────────
PORTAFOLIO 100%   [X]%     —            —        $[X]       100%

DIAGNÓSTICO DE CONCENTRACIÓN DE RIESGO:
  Un activo contribuye más del 40% del VaR total → concentración de riesgo
  Un activo contribuye más del 60% del VaR total → alerta roja de concentración

ACTIVO DIVERSIFICADOR vs ACTIVO CONCENTRADOR:
  Si % VaR_i / % peso_i < 0.7 → activo diversificador (aporta menos riesgo del que pesa)
  Si % VaR_i / % peso_i ≈ 1.0 → activo neutral en términos de diversificación
  Si % VaR_i / % peso_i > 1.3 → activo concentrador (aporta más riesgo del que pesa)
  → Candidato a reducir
```

---

## MÓDULO 3 — ANÁLISIS DE DRAWDOWN Y RECUPERACIÓN

```
DRAWDOWN MÁXIMO (Maximum Drawdown — MDD):
  MDD = (Pico máximo - Valle mínimo) / Pico máximo
  Mide la peor caída de punta a punta en el período analizado

MÉTRICAS DE DRAWDOWN DEL PORTAFOLIO:

MDD histórico por clase de activo (referencias):
  Acciones USA (S&P 500) : -56% (2008-2009), -34% (2020), -27% (2022)
  Acciones emergentes    : -65% (2008), -40% (2020)
  Bitcoin                : -93% (2011), -84% (2018), -77% (2021-2022)
  Bonos largo plazo (TLT): -50% (2020-2023) — el peor en 40 años
  Oro                    : -45% (2011-2015), -20% (2022)
  COLCAP (Colombia)      : -55% (2020), -40% (2022)
  TES Colombia 10Y       : -25% (2022, ciclo hawkish Banrep)
  CDTs Colombia          : sin drawdown (instrumento a vencimiento garantizado)

CÁLCULO DEL DRAWDOWN ESPERADO DEL PORTAFOLIO:
  MDD_esperado ≈ -z_α × σ_portafolio × √T_recovery

  Donde T_recovery = tiempo típico de recuperación del tipo de portafolio

TIEMPO DE RECUPERACIÓN HISTÓRICO (tras el drawdown máximo):
  S&P 500 2008: 65 meses (5.4 años) hasta recuperar el pico
  S&P 500 2020: 6 meses (recuperación más rápida en historia)
  S&P 500 2022: 24 meses aproximados
  Bitcoin 2017-2018: 36 meses hasta nuevo ATH
  COLCAP 2020: 48+ meses (más lento por factores locales)

TABLA DE DRAWDOWN ESCENARIOS PARA EL PORTAFOLIO:

Escenario          Shock asumido   MDD estimado    Tiempo recuperación
──────────────────────────────────────────────────────────────────────
Base (sin crisis)  Vol. normal     -[X]%            [X] meses
Recesión moderada  -20% equity     -[X]%            [X] meses
Recesión severa    -35% equity     -[X]%            [X] meses
Crisis sistémica   -50% equity     -[X]%            [X] meses
Crisis local COL   Spread+500bps   -[X]%            [X] meses
──────────────────────────────────────────────────────────────────────

CALMAR RATIO:
  Calmar = CAGR del portafolio / |MDD|
  > 1.0 → excelente (el rendimiento compensa el drawdown)
  0.5-1.0 → aceptable
  < 0.5 → el drawdown máximo no está siendo suficientemente compensado

PAIN INDEX:
  = Promedio de todos los drawdowns (no solo el máximo)
  Mide el "dolor crónico" del portafolio vs el "dolor puntual" del MDD
  Portafolios con muchas correcciones pequeñas tienen Pain Index alto
  aunque su MDD sea moderado
```

---

## MÓDULO 4 — VERIFICACIÓN DE LÍMITES DE POSICIÓN

```
LÍMITES DEL SISTEMA FINANCIAL INTELLIGENCE (no negociables):

LÍMITE 1 — POR POSICIÓN INDIVIDUAL:
  Máximo 5% del portafolio en un activo individual
  Excepción permitida: hasta 8% en ETFs amplios diversificados (SPY, VTI, MSCI World)
  Excepción con alerta: hasta 10% si el activo es el propio fondo de acciones local
  Prohibido: > 15% en cualquier activo bajo cualquier circunstancia

LÍMITE 2 — POR SECTOR:
  Máximo 25% del portafolio en un solo sector GICS
  Ejemplo: sector tecnología (XLK) ≤ 25%
  Colombia específico: máximo 30% en energía (considerando Ecopetrol + XLE + petróleo)

LÍMITE 3 — POR GEOGRAFÍA:
  Máximo 60% en un solo país
  Máximo 70% en una sola región (LatAm, desarrollados, emergentes)
  Mínimo 20% en activos internacionales para portafolios > COP 50M

LÍMITE 4 — POR CLASE DE ACTIVO:
  Máximo exposición crypto: 5% (conservador) / 15% (moderado) / 30% (agresivo)
  Máximo exposición commodities directos: 20% del portafolio
  Mínimo liquidez (cash + CDTs < 90 días): 5% (agresivo) / 10% (moderado) / 20% (conservador)

LÍMITE 5 — POR CORRELACIÓN:
  No tener dos activos con correlación > 0.9 sumando más del 20% del portafolio
  Ejemplo: SPY + QQQ (correlación 0.95) → peso combinado ≤ 20%
  Ejemplo: Ecopetrol + GLD (correlación baja) → sin restricción adicional

LÍMITE 6 — APALANCAMIENTO:
  Sistema prohibe recomendar apalancamiento para perfiles conservador y moderado
  Perfil agresivo: máximo 1.2× (20% de margen) y solo en acciones líquidas
  ETFs inversos (SH, SDS, SQQQ): solo para cobertura temporal, max 5%, max 30 días

VERIFICACIÓN AUTOMÁTICA:
  Para cada activo en el portafolio propuesto, verificar:
  ① Peso_i ≤ 5% (o excepción justificada)
  ② Peso_sector_k ≤ 25%
  ③ Peso_país_j ≤ 60%
  ④ Liquidez total ≥ mínimo por perfil
  ⑤ No hay par con ρ > 0.9 sumando > 20%
  ⑥ Apalancamiento = 0 (o dentro del límite si perfil agresivo)

ALERTA DE INCUMPLIMIENTO:
  🔴 LÍMITE EXCEDIDO: [activo/sector/geografía] al [X]% supera el límite de [Y]%
     Acción requerida: reducir [activo] de [X]% a máximo [Y]%
```

---

## MÓDULO 5 — STRESS TESTING ADVERSARIAL

```
ESCENARIOS DE ESTRÉS — APLICADOS AL PORTAFOLIO REAL DEL USUARIO:

ESCENARIO 1: RECESIÓN USA MODERADA
  S&P 500: -25% | Nasdaq: -35% | Bonos largo (TLT): +10% | Oro: +8%
  Petróleo: -20% | COLCAP: -30% | COP/USD: +10% (depreciación COP)
  Banrep: pausa o baja agresiva | TES 10Y: +5% precio | Spreads IG: +150bps

ESCENARIO 2: RECESIÓN SEVERA / CRISIS SISTÉMICA
  S&P 500: -50% | Nasdaq: -60% | Bonos largo (TLT): +20% | Oro: +20%
  Petróleo: -40% | COLCAP: -50% | COP/USD: +25% (depreciación severa)
  TES 10Y: spread soberano +400bps → precio -20% | Spreads HY: +600bps
  Bitcoin: -70% | Ecopetrol: -55%

ESCENARIO 3: ESTANFLACIÓN (inflación alta + recesión)
  S&P 500: -30% | Nasdaq: -45% | Bonos largo (TLT): -30% (doble golpe)
  Oro: +30% | Petróleo: +50% | COLCAP: -15% (Ecopetrol amortigua)
  TES fija larga: -25% | TES UVR: +15% | COP/USD: +15%

ESCENARIO 4: CRISIS FISCAL COLOMBIA
  Downgrade soberano Colombia: spread EMBI +600bps → bonos colombianos -30%
  TES 10Y: precio -25% | COLCAP: -40% | COP/USD: +20%
  CDTs: sin impacto en precio (a vencimiento) pero liquidez reducida
  Ecopetrol: -45% (riesgo soberano + petróleo)

ESCENARIO 5: SHOCK DE TASAS FED (hawkish extremo)
  FED sube 200bps adicionales en 6 meses (no esperado por mercado)
  TLT: -25% | Nasdaq (growth): -40% | IG Corporativo: -15%
  Emergentes: salida de capitales → COLCAP -25% | COP -15%
  Oro: -10% (tasas reales más positivas) | T-Bills: beneficiados

ESCENARIO 6: CRASH CRIPTO (-80%) CON CONTAGIO TECH
  Bitcoin: -80% | Ethereum: -85% | Nasdaq: -25% por contagio
  Afectados: empresas con exposición cripto (Coinbase, MicroStrategy)
  Spreads HY tech: +300bps | Sin impacto significativo en commodities o bonos soberanos

TABLA DE RESULTADOS DEL STRESS TEST:

Escenario              P&L ($)    P&L (%)    Días recuperación est.
──────────────────────────────────────────────────────────────────
E1: Recesión moderada  -$[X]      -[X]%      ~[X] meses
E2: Crisis sistémica   -$[X]      -[X]%      ~[X] meses
E3: Estanflación       -$[X]      -[X]%      ~[X] meses
E4: Crisis Colombia    -$[X]      -[X]%      ~[X] meses
E5: Shock FED          -$[X]      -[X]%      ~[X] meses
E6: Crash cripto       -$[X]      -[X]%      ~[X] meses
──────────────────────────────────────────────────────────────────
PEOR ESCENARIO         -$[X]      -[X]%      Escenario [X]

TOLERANCIA:
  Si pérdida en peor escenario > pérdida máxima tolerable del usuario:
  → ALERTA ROJA: portafolio vulnerable en escenario adverso
  → Recomendación de cobertura específica al CIO

ESCENARIO POSITIVO DE VALIDACIÓN (opcional):
  Bull market fuerte (S&P +30%, Banrep baja agresiva, petróleo +20%):
  Ganancia esperada: +$[X] ([X]%) → ratio retorno/riesgo: [X]x
  → Valida que el portafolio también captura el upside
```

---

## MÓDULO 6 — MÉTRICAS DE EFICIENCIA AJUSTADA AL RIESGO

```
SHARPE RATIO:
  Sharpe = (Retorno portafolio - Tasa libre riesgo) / Volatilidad portafolio
  Tasa libre riesgo: T-Bill 3M USA (en USD) o DTF (en COP)

  Interpretación:
  < 0    → peor que el activo libre de riesgo — indefendible
  0-0.5  → pobre — el riesgo no está siendo compensado
  0.5-1.0→ aceptable para la mayoría de portafolios
  1.0-2.0→ bueno — riesgo bien recompensado
  > 2.0  → excelente — raro en portafolios diversificados reales

SORTINO RATIO:
  Sortino = (Retorno portafolio - Tasa libre riesgo) / Volatilidad bajista
  Solo penaliza la volatilidad negativa (la que importa al inversor)
  Siempre ≥ Sharpe (o igual si distribución simétrica)
  > 1.5 → bueno | > 2.0 → excelente

CALMAR RATIO:
  Calmar = CAGR / |MDD|
  > 1.0 → excelente | 0.5-1.0 → aceptable | < 0.5 → el drawdown es costoso

OMEGA RATIO:
  Omega = P(retorno > umbral) / P(retorno < umbral) ponderado por magnitudes
  > 1.5 → portafolio consistentemente rentable sobre el umbral

INFORMATION RATIO (vs benchmark):
  IR = (Retorno portafolio - Retorno benchmark) / Tracking Error
  > 0.5 → gestión activa agrega valor consistentemente
  < 0.0 → la gestión activa destruye valor vs el benchmark

TABLA DE MÉTRICAS DE EFICIENCIA:

Métrica           Portafolio   Benchmark   Umbral mínimo   Diagnóstico
────────────────────────────────────────────────────────────────────────
Sharpe Ratio      [X.XX]       [X.XX]      0.50            [OK/ALERTA]
Sortino Ratio     [X.XX]       [X.XX]      1.00            [OK/ALERTA]
Calmar Ratio      [X.XX]       [X.XX]      0.50            [OK/ALERTA]
Volatilidad anual [X.XX]%      [X.XX]%     [según perfil]  [OK/ALERTA]
MDD               [X.XX]%      [X.XX]%     [según perfil]  [OK/ALERTA]
Beta vs S&P500    [X.XX]       1.00        < 1.2 (mod.)    [OK/ALERTA]
────────────────────────────────────────────────────────────────────────
```

---

## MÓDULO 7 — RIESGO CAMBIARIO (ESPECÍFICO COLOMBIA)

```
EXPOSICIÓN CAMBIARIA DEL PORTAFOLIO:

Para el inversor colombiano, el riesgo cambiario es una dimensión adicional
que los modelos estándar (calibrados para inversores en USD) no capturan.

CÁLCULO DE EXPOSICIÓN NETA EN USD:
  Activos en USD (ETFs USA, bonos USD, acciones NYSE): [X]% del portafolio
  Activos en COP (TES, COLCAP, CDTs): [X]% del portafolio
  Activos en COP pero indexados a commodities USD (Ecopetrol): [X]% — exposición parcial

  Exposición neta USD = activos directos en USD + exposición indirecta parcial

VaR CAMBIARIO (FX VaR):
  Volatilidad histórica COP/USD: ~12-15% anual (en años normales)
                                  ~25-35% anual (en años de crisis)
  VaR 99% COP/USD a 1 mes ≈ 2.33 × (15%/√12) × exposición_USD
  = 2.33 × 4.33% × exposición_USD

ESCENARIOS DE TIPO DE CAMBIO:

  Escenario         TRM actual   TRM stress   Impacto portafolio COP
  ─────────────────────────────────────────────────────────────────
  COP aprecia 10%   $[X]         $[X-10%]     Activos USD valen menos en COP
  Status quo        $[X]         $[X]         Sin impacto cambiario
  COP deprecia 10%  $[X]         $[X+10%]     Activos USD valen más en COP
  COP deprecia 20%  $[X]         $[X+20%]     Doble efecto: USD sube, equities caen
  Crisis cambiaria  $[X]         $[X+35%]     Crisis sistémica local

CORRELACIÓN PETRÓLEO-COP EN EL PORTAFOLIO:
  Si el usuario tiene Ecopetrol + TES + ETFs USD + petróleo:
  En crisis de petróleo:
    Ecopetrol cae → COLCAP cae → TRM sube (COP se deprecia)
    → El ETF en USD SUBE en términos COP por la depreciación
    → Hay una cobertura natural parcial
  → Cuantificar si la cobertura natural es suficiente o si se necesita cobertura explícita

COSTO DE COBERTURA FX (forward COP/USD):
  Tasa forward = TRM × [(1 + tasa COP)/(1 + tasa USD)]^(días/360)
  Costo anualizado típico Colombia: 4-6% (diferencial de tasas)
  Si el retorno esperado de activos en USD es 8% en USD:
  Retorno hedgeado en COP = 8% - 5% costo cobertura = 3% en COP
  vs TES Colombia rindiendo [X]% → comparar cuál es más eficiente
```

---

## MÓDULO 8 — SISTEMA DE ALERTAS Y SEMÁFORO DE RIESGO

```
SEMÁFORO DE RIESGO DEL PORTAFOLIO:

🟢 VERDE — Riesgo controlado (todos los límites cumplidos):
  ✓ VaR 99% 1 mes dentro del límite del perfil
  ✓ N_efectivo > 5 (diversificación aceptable)
  ✓ Ningún activo supera el 5% de posición
  ✓ Ningún sector supera el 25%
  ✓ Stress test: peor escenario < pérdida máxima tolerable
  ✓ Sharpe > 0.5 y Sortino > 1.0
  ✓ Sin concentración de riesgo (ningún activo > 40% del VaR total)
  → Portafolio aprobado para el CIO. Proceder con recomendación.

🟡 AMARILLO — Riesgo elevado (1-2 alertas activas):
  ⚠️ VaR dentro del límite pero cercano al máximo (> 80% del límite)
  ⚠️ N_efectivo entre 3 y 5 (concentración moderada)
  ⚠️ Un activo entre 5% y 8% (requiere justificación)
  ⚠️ Un sector entre 25% y 30% (vigiar)
  ⚠️ Stress test: un escenario supera la pérdida tolerable marginalmente
  → Portafolio aprobado CON CONDICIONES. El CIO debe mencionar las alertas.

🔴 ROJO — Riesgo inaceptable (cualquiera de estas condiciones):
  ✗ VaR 99% 1 mes supera el límite del perfil
  ✗ N_efectivo < 3 (concentración peligrosa)
  ✗ Algún activo supera el 8% del portafolio sin ser ETF amplio
  ✗ Algún sector supera el 30% del portafolio
  ✗ Stress test: más de un escenario supera la pérdida máxima tolerable
  ✗ CVaR/VaR > 1.8 (fat tails extremos — distribución de pérdidas peligrosa)
  ✗ Correlación de crisis hace colapsar la diversificación
  → PORTAFOLIO RECHAZADO. El CIO debe modificar la recomendación antes de emitirla.
  → Acciones de remediación obligatorias antes de proceder.

⚫ NEGRO — Riesgo sistémico (emergencia):
  ✗✗ Pérdida ya materializada > 50% del límite máximo tolerable en el mes
  ✗✗ Múltiples límites excedidos simultáneamente
  ✗✗ Scoring board en polarización + riesgo alto + scoring < 3.0
  → ALERTA MÁXIMA: recomendar inmediatamente reducción de exposición a mínimos
  → Preservación de capital sobre cualquier otra consideración
```

---

## OUTPUT FINAL DEL RISK ENGINE

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ RISK ENGINE REPORT — [FECHA]
Portafolio: $[X] | Perfil: [conservador/moderado/agresivo]
Pérdida máxima tolerable: [X]% ($[X])
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 MÓDULO 1 — VaR TRIANGULADO
  VaR 99% 1 día    : $[X] ([X]%) | Límite perfil: $[X] ([X]%) → [OK/⚠️/🔴]
  VaR 99% 1 mes    : $[X] ([X]%) | Límite perfil: $[X] ([X]%) → [OK/⚠️/🔴]
  CVaR 99% 1 mes   : $[X] ([X]%) | Ratio CVaR/VaR: [X.X] → [normal/fat tail]
  Método divergente: [Paramétrico/Histórico/MonteCarlo] → [más conservador]

🔗 MÓDULO 2 — CORRELACIONES Y DIVERSIFICACIÓN
  Diversification Ratio : [X.X] → [sin/moderada/buena/excelente] diversif.
  N_efectivo activos    : [X.X] → [concentrado/aceptable/bien diversificado]
  Par más correlacionado: [activo A] + [activo B] = [X.X] → [OK/⚠️/🔴]
  Mayor contribuidor VaR: [activo] con [X]% del VaR total → [OK/⚠️/🔴]

📉 MÓDULO 3 — DRAWDOWN
  MDD esperado escenario base: -[X]%
  MDD en crisis sistémica     : -[X]% (Escenario 2)
  Tiempo recuperación esperado: ~[X] meses
  Calmar Ratio actual         : [X.X] → [excelente/aceptable/bajo]

✅ MÓDULO 4 — LÍMITES DE POSICIÓN
  [Lista de alertas de incumplimiento si las hay, o "Todos los límites OK"]
  Posición mayor: [activo] al [X]% → [OK/⚠️/🔴]
  Sector mayor  : [sector] al [X]% → [OK/⚠️/🔴]
  Liquidez      : [X]% en cash/CDTs → [OK/⚠️/🔴]

🔥 MÓDULO 5 — STRESS TEST
  Peor escenario: [nombre] → -[X]% (-$[X])
  ¿Dentro de tolerancia del usuario? [SÍ / NO — supera en $[X]]
  Escenario crítico para este portafolio: [escenario más dañino y por qué]

📐 MÓDULO 6 — EFICIENCIA AJUSTADA AL RIESGO
  Sharpe Ratio   : [X.XX] → [OK/⚠️/🔴]
  Sortino Ratio  : [X.XX] → [OK/⚠️/🔴]
  Beta vs S&P    : [X.XX] → [conservador/neutral/agresivo]

💱 MÓDULO 7 — RIESGO CAMBIARIO (COLOMBIA)
  Exposición neta USD: [X]% del portafolio
  VaR FX 99% 1 mes   : [X]% ($[X] en COP)
  Cobertura natural  : [suficiente/insuficiente] → [recomendar/no forward]
  Costo cobertura FX : ~[X]% anual si se decide cubrir

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚦 SEMÁFORO DE RIESGO FINAL: 🟢 VERDE / 🟡 AMARILLO / 🔴 ROJO / ⚫ NEGRO

Alertas activas : [lista de alertas o "Sin alertas"]
Acciones req.   : [lista de acciones correctivas o "Ninguna"]
Veredicto       : [APROBADO / APROBADO CON CONDICIONES / RECHAZADO / EMERGENCIA]

→ PASA AL CIO con semáforo [COLOR] y [N] alertas activas.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## REGLAS DEL SISTEMA

1. **El risk engine es el único módulo con poder de veto** — puede detener una recomendación del CIO si el semáforo es rojo.
2. **Triangular siempre los tres métodos de VaR** — un solo método es insuficiente para una decisión institucional.
3. **Las correlaciones de crisis deben usarse en el stress test, no las correlaciones normales** — los activos se correlacionan en pánico.
4. **CVaR es obligatorio junto al VaR** — el tail que el VaR no captura es exactamente el que destruye portafolios.
5. **El riesgo cambiario es una dimensión adicional para el inversor colombiano** — los modelos en USD lo ignoran.
6. **N_efectivo < 3 es la señal de concentración más clara** — más reveladora que el peso de un activo solo.
7. **El stress test en escenario de crisis colombiana es no negociable** — el contexto local puede divergir del global.
8. **La condición de alerta roja no impide recomendar — obliga a justificar** — el CIO puede proceder si justifica por qué el riesgo es aceptable dado el objetivo específico del usuario.
9. **La liquidez mínima es inviolable** — el usuario siempre debe poder acceder a una porción del capital sin vender activos en pérdida.
10. **Ninguna recomendación sale del sistema sin el semáforo del risk engine** — es la última línea de defensa.

---

## REFERENCIA A ARCHIVOS ADICIONALES

- `references/var_methodology.md` — Derivación matemática completa: paramétrico, histórico, Monte Carlo, backtesting del modelo
- `references/stress_scenarios.md` — Biblioteca de escenarios de estrés históricos y prospectivos con shocks por clase de activo
- `references/correlation_regimes.md` — Matrices de correlación por régimen de mercado (normal, crisis, post-crisis)
