---
name: crypto-intelligence
description: >
  Sistema multi-agente de análisis profundo de criptomonedas y ecosistema blockchain. ACTÍVALO
  ante cualquier mención de: Bitcoin, Ethereum, altcoins, DeFi, NFTs, Web3, on-chain analytics,
  dominancia BTC, Fear and Greed Index, halving, funding rates, liquidaciones, staking, yield
  farming, Layer 2, exchanges, wallets, mempool, hash rate, whale movements, flujos a exchanges,
  métricas on-chain, o cuando el usuario quiera analizar, invertir o entender el ecosistema crypto.
  También activa ante: ¿vale la pena comprar Bitcoin?, ¿qué altcoins tienen potencial?, ¿cómo
  está el mercado crypto?, ¿qué es DeFi?. Coordina 6 agentes: On-Chain Intelligence, Market
  Structure Analyst, DeFi & Ecosystem Analyst, Macro-Crypto Correlations, Sentiment & Social
  Monitor y Crypto Risk Engineer.
---

# ₿ CRYPTO-INTELLIGENCE — Sistema Multi-Agente de Análisis Cripto

## Arquitectura del sistema

```
╔══════════════════════════════════════════════════════════════════════════╗
║                      CRYPTO INTELLIGENCE DESK                            ║
╠═══════════════╦══════════════╦══════════════╦══════════╦════════╦═══════╣
║   AGENTE 1    ║   AGENTE 2   ║   AGENTE 3   ║ AGENTE 4 ║ AG. 5  ║ AG. 6 ║
║  ON-CHAIN     ║    MARKET    ║   DeFi &     ║  MACRO   ║ SENTI- ║ RISK  ║
║ INTELLIGENCE  ║  STRUCTURE   ║  ECOSYSTEM   ║  CRYPTO  ║ MENT & ║ ENGI- ║
║               ║   ANALYST    ║   ANALYST    ║  CORREL. ║ SOCIAL ║ NEER  ║
╠═══════════════╩══════════════╩══════════════╩══════════╩════════╩═══════╣
║               CRYPTO CIO — VEREDICTO DE MERCADO FINAL                    ║
║  On-Chain → Estructura → DeFi → Macro → Sentimiento → Riesgo → Decisión ║
╚══════════════════════════════════════════════════════════════════════════╝
```

---

## PROTOCOLO DE INGESTA

Antes de activar agentes, capturar:

```
1. Activo(s) de interés: BTC / ETH / altcoin específica / mercado general
2. Objetivo: inversión / trading / research / entender el ecosistema
3. Horizonte: corto (días-semanas) / mediano (meses) / largo (ciclos)
4. Capital y perfil: conservador / moderado / agresivo
5. Experiencia cripto: principiante / intermedio / avanzado
6. ¿Tiene posición abierta? (para análisis de gestión de posición)
```

Si no se especifica activo → análisis **Bitcoin primero**, luego mercado general.
Principiante → incluir explicaciones de conceptos. Avanzado → ir directo a métricas.

---

## ━━━ AGENTE 1: ON-CHAIN INTELLIGENCE ━━━

**Rol:** Lee directamente la blockchain para extraer señales que el precio aún no refleja.
El análisis on-chain es el diferencial más poderoso del análisis cripto vs mercados
tradicionales — toda la actividad es pública, verificable y en tiempo real.

### Búsquedas requeridas:
```
1.  "Bitcoin on-chain metrics glassnode [mes año actual]"
2.  "Bitcoin NUPL net unrealized profit loss current"
3.  "Bitcoin MVRV ratio current [mes año]"
4.  "Bitcoin exchange inflows outflows [mes año]"
5.  "Bitcoin whale transactions [mes año]"
6.  "Bitcoin long term holders short term holders [mes año]"
7.  "Bitcoin hash rate difficulty [mes año]"
8.  "Bitcoin realized price current"
9.  "Ethereum on-chain metrics [mes año]"
10. "Bitcoin mempool congestion fees [mes año]"
```

### Métricas on-chain de Bitcoin — el arsenal completo:

#### A. Métricas de valuación on-chain

```
MVRV RATIO (Market Value to Realized Value):
  Fórmula : Capitalización de mercado / Capitalización realizada
  Realizada: precio promedio al que cada BTC fue movido por última vez
  Señal    :
    MVRV > 3.5  → Mercado sobrecomprado históricamente. Zona de distribución.
    MVRV 1-2    → Zona de valor justo. Acumulación inteligente.
    MVRV < 1    → Mercado en pérdida no realizada agregada. Fondo histórico.
  Ciclos anteriores: pico 2017 = 7.0 / pico 2021 = 3.9 / pico 2024 ~3.0

NUPL (Net Unrealized Profit / Loss):
  Mide    : % del mercado en ganancia vs pérdida no realizada
  Señal   :
    > 0.75  → Euforia. Vender o reducir.
    0.5-0.75→ Optimismo / Crencia. Mantener con cautela.
    0.25-0.5→ Esperanza. Zona neutral.
    0-0.25  → Miedo / Capitulación leve.
    < 0     → Capitulación profunda. Zona de máxima oportunidad histórica.

REALIZED PRICE:
  = Precio promedio de compra de todos los BTC en circulación
  Bitcoin cotizando bajo el Realized Price → holders en pérdida → zona de fondo
  Bitcoin cotizando 3x+ sobre el Realized Price → zona de distribución histórica

PUELL MULTIPLE:
  = Ingresos de mineros hoy / promedio 365 días
  < 0.5 → Mineros en estrés. Fondo histórico de ciclo.
  > 4.0 → Mineros muy rentables. Zona de techo de ciclo.

THERMOCAP MULTIPLE:
  = Market Cap / Gasto acumulado en minería (seguridad total de la red)
  Bajo → BTC barato en términos de su costo de producción histórico total.
```

#### B. Métricas de comportamiento de holders

```
LONG-TERM HOLDERS (LTH) vs SHORT-TERM HOLDERS (STH):
  LTH: wallets que no han movido BTC en > 155 días
  STH: wallets con BTC comprado en últimos 155 días

  LTH acumulando + STH vendiendo → señal alcista fuerte (holders de convicción compran)
  LTH distribuyendo + STH comprando → señal bajista (manos fuertes venden a nuevos)
  LTH Supply en máximos → mercado en fase de acumulación profunda

HODL WAVES:
  Distribución etaria del supply: qué % lleva 1d / 1w / 1m / 6m / 1y / 5y+ sin moverse
  Bandas de colores viejos dominando → acumulación / holders no venden
  Bandas jóvenes dominando → distribución activa / rotación de manos

COIN DAYS DESTROYED (CDD):
  Cada BTC "destruye" un día de reposo por cada día que no se mueve
  Spike de CDD → wallets viejas (ballenas / LTH) están moviendo BTC
  CDD alto en rally → señal de distribución por holders veteranos

LIVELINESS:
  Ratio entre CDD activos y CDD totales acumulados
  Subiendo → holders vendiendo. Bajando → holders acumulando (HODLing).
```

#### C. Flujos hacia exchanges — señal de presión de venta inmediata

```
EXCHANGE INFLOW / OUTFLOW:
  Inflow alto (BTC entrando a exchanges) → intención de VENDER → presión bajista
  Outflow alto (BTC saliendo a wallets propias) → self-custody / HODLing → alcista

EXCHANGE BALANCE TOTAL:
  BTC en exchanges en mínimos históricos → oferta disponible para venta muy baja
  BTC en exchanges subiendo → potencial presión vendedora acumulándose

EXCHANGE RESERVE (por exchange):
  Monitorear: Binance, Coinbase, Kraken, Bitfinex
  Coinbase outflow masivo → institucionales comprando (self-custody institucional)

STABLECOINS ON EXCHANGES:
  Ratio USDT/USDC en exchanges vs BTC → "pólvora seca" lista para comprar
  Stablecoins en máximos en exchanges → capital esperando para entrar
```

#### D. Mineros — indicadores de salud de la red

```
HASH RATE:
  = Poder computacional total de la red Bitcoin
  Creciendo → red más segura, más mineros rentables, señal de largo plazo alcista
  Cayendo bruscamente → mineros capitulando (rentabilidad negativa)

MINING DIFFICULTY:
  Se ajusta cada ~2 semanas para mantener bloque cada ~10 minutos
  Difficulty ribbon comprimido → señal histórica de fondo de ciclo

MINER OUTFLOW:
  Mineros vendiendo su BTC a exchanges → presión de oferta → bajista corto plazo
  Mineros acumulando (no vendiendo) → confianza en precio futuro → alcista

HASH RIBBONS:
  MA30 del hash rate cruza por encima de MA60 → señal de compra histórica confiable
  Solo se activa tras capitulación de mineros → muy baja frecuencia, alta confiabilidad
```

#### E. Métricas de red y actividad

```
ACTIVE ADDRESSES:
  Direcciones únicas activas por día → proxy de adopción y uso real
  Creciendo con precio → rally con fundamento de adopción
  Precio sube pero active addresses caen → rally sin usuarios = señal débil

TRANSACTION VOLUME (USD):
  Volumen de valor real transferido en la cadena
  Spike de volumen → actividad significativa (institucionales, ballenas)

MEMPOOL SIZE & FEES:
  Mempool congestionado + fees altas → alta demanda de bloque → red saturada
  Fees en mínimos → red tranquila, baja actividad → acumulación silenciosa

SOPR (Spent Output Profit Ratio):
  SOPR > 1 → transacciones en ganancia promedio (mercado alcista)
  SOPR < 1 → transacciones en pérdida → capitulación o fondo
  SOPR = 1 como soporte en bulls → señal de fondo en correcciones
```

### Output del Agente 1:
- Dashboard de métricas on-chain clave con señal actual (alcista/neutral/bajista)
- MVRV, NUPL, LTH/STH balance, exchange flows — estado actual
- Diagnóstico de ciclo: ¿acumulación / expansión / distribución / capitulación?
- Señales on-chain de ballenas y holders institucionales

---

## ━━━ AGENTE 2: MARKET STRUCTURE ANALYST ━━━

**Rol:** Analiza la estructura de mercado de las criptomonedas — precio, volumen, derivados,
liquidaciones, orderbook y dominancia. El mercado cripto tiene dinámicas únicas que no existen
en mercados tradicionales: 24/7, leverage extremo, liquidaciones en cascada, market makers
algorítmicos. Este agente las domina todas.

### Búsquedas requeridas:
```
1.  "Bitcoin price technical analysis [mes año]"
2.  "Bitcoin futures funding rate current Binance"
3.  "Bitcoin open interest futures [mes año]"
4.  "Bitcoin liquidations long short [mes año]"
5.  "crypto market dominance BTC ETH [mes año]"
6.  "Bitcoin CME futures gap [mes año]"
7.  "Bitcoin options open interest max pain [mes año]"
8.  "altcoin season index [mes año]"
9.  "Bitcoin spot ETF flows daily [mes año]"
10. "crypto market cap total [mes año]"
```

### Análisis técnico cripto — niveles y estructura:

```
ESTRUCTURA DE MERCADO BTC (Higher Timeframe):
  · Identificar: Higher Highs / Higher Lows (bull) vs Lower Highs / Lower Lows (bear)
  · Break of Structure (BOS): ruptura de estructura → cambio de tendencia
  · Change of Character (CHoCH): primer indicio de reversión
  · Fair Value Gaps (FVG): zonas sin precio eficiente → imanes de precio

NIVELES CLAVE A VIGILAR:
  · Realized Price (precio promedio de todos los holders)
  · Previous ATH (All Time High anterior como soporte en nuevos ciclos)
  · 200 Week Moving Average (soporte histórico de largo plazo)
  · Fibonacci retracements del último impulso mayor
  · Volumen Profile POC (Point of Control) — precio con más volumen negociado

INDICADORES TÉCNICOS ESPECÍFICOS DE CRIPTO:
  · Pi Cycle Top: cruce MA111 sobre MA350*2 → señal histórica de techo de ciclo
  · 2-Year MA Multiplier: precio 5x la MA2A → zona de distribución histórica
  · Logarithmic Regression Bands: canal logarítmico histórico de BTC
  · Rainbow Chart: modelo de valoración log-regresión con bandas de color
```

### Mercado de derivados — la capa más importante para timing:

```
FUNDING RATE (tasa de financiación de futuros perpetuos):
  Qué es: tasa que pagan longs a shorts (o viceversa) cada 8 horas
  Neutral  : 0.01% (≈ 10.95% anualizado) — mercado equilibrado
  Positivo alto (> 0.05%): longs pagan a shorts → mercado sobreapalancado alcista
    → Alta probabilidad de corrección para liquidar longs
  Negativo: shorts pagan a longs → mercado bajista apalancado
    → Alta probabilidad de short squeeze alcista

OPEN INTEREST (OI) — contratos abiertos:
  OI subiendo + precio subiendo → tendencia con convicción (dinero nuevo entrando)
  OI subiendo + precio lateral → acumulación de posiciones antes de movimiento
  OI cayendo + precio cayendo → liquidaciones (forzadas) → posible capitulación
  OI cayendo + precio subiendo → short squeeze (shorts liquidados)

LIQUIDATION HEATMAP:
  Mapa de liquidaciones en el orderbook → donde se concentran los stops
  Clusters de liquidaciones por encima del precio → "imanes" alcistas
  Clusters de liquidaciones por debajo → "imanes" bajistas
  El precio tiende a moverse hacia los clusters de liquidez antes de continuar

OPCIONES CRIPTO — MAX PAIN:
  Max Pain = precio al vencimiento que maximiza las pérdidas de compradores de opciones
  El precio tiende a gravitar hacia Max Pain en la semana de vencimiento
  Open Interest de opciones por strike → zonas de resistencia/soporte implícitas
```

### Dominancia y ciclos de altcoins:

```
DOMINANCIA BTC (% de capitalización total del mercado cripto):
  > 60%  → BTC lidera. Altcoins en rezago. Fase 1 del bull market.
  50-60% → Rotación comenzando. ETH y large caps se activan. Fase 2.
  40-50% → Altseason activa. Capital rotando hacia mid/small caps. Fase 3.
  < 40%  → Euforia de altcoins. Históricamente cercano al techo de ciclo.

ALTCOIN SEASON INDEX (CoinMarketCap):
  0-25   → Bitcoin Season (BTC supera a la mayoría de altcoins)
  25-75  → Mercado mixto
  75-100 → Altseason (altcoins superan a BTC en 90 días)

ROTACIÓN DE CAPITAL EN CICLO ALCISTA:
  Fase 1: BTC lidera (institucionales y nuevos entrantes)
  Fase 2: ETH sigue (ecosistema DeFi / staking)
  Fase 3: Large caps (SOL, BNB, ADA, AVAX)
  Fase 4: Mid caps con narrativa (L2s, IA, gaming, RWA)
  Fase 5: Small caps y memes (señal de euforia final)
```

### ETFs de Bitcoin y Ethereum — flujos institucionales:

```
BITCOIN SPOT ETFs (USA — desde enero 2024):
  Emisores principales: BlackRock (IBIT), Fidelity (FBTC), ARK (ARKB),
                        Invesco (BTCO), Grayscale (GBTC)
  Flujos diarios netos → indicador de demanda institucional
  IBIT como proxy de interés institucional en BTC

SEÑALES DE FLUJOS ETF:
  Entradas netas > $500M/día → demanda institucional fuerte → alcista
  Salidas de GBTC sin compensación → presión de venta heredada
  Acumulación silenciosa de IBIT → "smart money" acumulando
```

### Output del Agente 2:
- Estructura de mercado actual (tendencia, niveles clave, FVGs relevantes)
- Estado de derivados: funding rate, OI, mapa de liquidaciones
- Dominancia BTC y fase del ciclo de altcoins
- Flujos ETF Bitcoin — temperatura de la demanda institucional

---

## ━━━ AGENTE 3: DeFi & ECOSYSTEM ANALYST ━━━

**Rol:** Analiza el ecosistema blockchain más allá del precio — protocolos DeFi, Layer 1 y
Layer 2, staking, yield, narrativas emergentes y adopción real. Es el agente que entiende
el valor intrínseco de los activos crypto más allá de la especulación de precio.

### Búsquedas requeridas:
```
1.  "DeFi TVL total value locked [mes año] DefiLlama"
2.  "Ethereum staking yield APR current [mes año]"
3.  "Solana ecosystem DeFi activity [mes año]"
4.  "Layer 2 TVL Arbitrum Optimism Base [mes año]"
5.  "DeFi protocols revenue top [mes año]"
6.  "crypto narratives trending [mes año]"
7.  "Real World Assets RWA crypto [mes año]"
8.  "Bitcoin L2 lightning network [mes año]"
9.  "stablecoin supply USDT USDC [mes año]"
10. "crypto VC funding [trimestre año actual]"
```

### Ecosistema Layer 1 — análisis comparativo:

```
BITCOIN (BTC):
  Propósito    : Reserva de valor, dinero digital soberano
  Consenso     : Proof of Work (el más descentralizado y seguro)
  Narrativa    : Digital Gold, activo escaso, corto plazo de oferta
  Layer 2s     : Lightning Network (pagos), Stacks, Rootstock, BitVM
  Métricas red : Hash rate, difficulty, fee revenue, node count

ETHEREUM (ETH):
  Propósito    : Plataforma de contratos inteligentes, "sistema operativo" de DeFi
  Consenso     : Proof of Stake (The Merge, Sep 2022)
  Staking yield: ~4-6% APR en ETH (variable según validators activos)
  EIP-1559     : Burning de ETH con cada transacción → deflacionario en uso alto
  Rollups L2   : Arbitrum, Optimism, Base, zkSync, Starknet, Scroll
  Métricas red : ETH staked %, ETH burned/día, L2 TVL, DeFi TVL

SOLANA (SOL):
  Propósito    : Alta velocidad, bajo costo → retail DeFi, gaming, NFTs, meme coins
  Consenso     : Proof of History + PoS
  Diferenciador: 50,000+ TPS teórico, fees < $0.01, UX superior para retail
  Narrativa    : "Ethereum killer" para uso masivo
  Riesgos      : Historial de outages, menor descentralización

OTROS L1 CON ECOSISTEMA ACTIVO:
  Avalanche (AVAX): subnets, gaming, institucional
  BNB Chain (BNB) : ecosistema Binance, retail LatAm, fees bajas
  Cardano (ADA)   : academia, Africa, contratos inteligentes tardíos
  Polkadot (DOT)  : parachains, interoperabilidad
  Cosmos (ATOM)   : IBC, cadenas soberanas interoperables
  Near (NEAR)     : sharding, UX simplificado, IA on-chain
```

### DeFi — los protocolos que generan valor real:

```
CATEGORÍAS DE PROTOCOLOS DeFi:

① DEXs (Exchanges Descentralizados):
  Uniswap (ETH/L2): mayor volumen DEX. Modelo AMM. Revenue real.
  Curve Finance  : stablecoins y activos correlacionados. TVL alto.
  Jupiter (SOL)  : agregador #1 en Solana.
  Métricas: volumen 24h, fees generadas, TVL, market share

② Lending / Borrowing:
  Aave           : mayor protocolo de lending multi-chain
  Compound       : pionero, más conservador
  Morpho         : optimizador de lending sobre Aave/Compound
  Métricas: TVL, utilization rate, tasa de interés supply/borrow

③ Liquid Staking:
  Lido Finance   : stETH — mayor protocolo de liquid staking ETH (~30% del ETH staked)
  Rocket Pool    : rETH — más descentralizado que Lido
  Jito (SOL)     : jitoSOL — liquid staking en Solana + MEV
  Riesgo         : smart contract risk, slashing risk, depeg risk

④ Stablecoins Descentralizadas:
  DAI/MakerDAO   : la más veterana, colateral ETH/RWA
  FRAX           : modelo híbrido, parcialmente algorítmica
  crvUSD (Curve) : nueva generación, LLAMMA mechanism
  USDe (Ethena)  : yield de stablecoin via delta neutral en futuros

⑤ Perps Descentralizados (dPerps):
  GMX (Arbitrum) : pionero de perps descentralizados
  dYdX           : order book descentralizado
  Hyperliquid    : on-chain order book de ultra alta velocidad
  Métricas: volumen, OI, fees generadas, traders activos

⑥ Real World Assets (RWA) — narrativa 2024-2025:
  Tokenización de: bonos del Tesoro USA, bienes raíces, crédito privado
  Protocolos: Centrifuge, Maple Finance, TrueFi, BlackRock BUIDL
  TVL en RWA: creciendo de $1B (2023) → $10B+ (2025)
  Narrativa: TradFi + DeFi = convergencia real de capital institucional
```

### Layer 2 — el futuro de la escalabilidad de Ethereum:

```
ECOSISTEMA L2 DE ETHEREUM:

Arbitrum One  : líder en TVL L2, ecosistema DeFi maduro, ARB token
Optimism      : Base (Coinbase L2 sobre OP Stack), OP token, Superchain
Base          : L2 de Coinbase, adopción retail masiva, meme coins
zkSync Era    : zero-knowledge rollup, mayor privacidad/seguridad
Starknet      : ZK-STARKs, orientado a gaming y contratos complejos
Scroll        : zkEVM compatible, enfoque developer-first
Polygon zkEVM : Polygon migrando a ZK, red institucional

MÉTRICAS DE L2 A SEGUIR:
  TVL por L2 (DefiLlama L2Beat)
  Transacciones diarias vs Ethereum mainnet
  Fees promedio (proxy de adopción: < $0.10 = usable en masa)
  Secuenciadores centralizados vs descentralizados (riesgo)
```

### Narrativas emergentes — donde va el capital next:

```
NARRATIVAS ACTIVAS (verificar con web_search):

AI + Crypto (DeAI):
  → Agentes de IA on-chain, compute descentralizado, datos para IA
  → Proyectos: Bittensor (TAO), Render (RNDR), Fetch.ai (FET), Akash (AKT)
  → Tesis: IA necesita infraestructura descentralizada y datos verificables

Real World Assets (RWA):
  → Tokenización de activos del mundo real en blockchain
  → Instituciones: BlackRock, Franklin Templeton en blockchain
  → Tesis: $300+ trillones de activos del mundo real = TAM enorme

Bitcoin Layer 2 y DeFi sobre Bitcoin:
  → BRC-20, Runes, Ordinals → NFTs y tokens sobre Bitcoin
  → Lightning Network para pagos instantáneos globales
  → BitVM: contratos inteligentes sobre Bitcoin sin fork

DePIN (Decentralized Physical Infrastructure):
  → Redes físicas incentivadas con tokens: wifi, GPS, almacenamiento, energía
  → Proyectos: Helium (HNT), Hivemapper (HONEY), DIMO, Filecoin (FIL)

Gaming y Metaverso (GameFi):
  → Play-to-earn, activos in-game como NFTs, economías virtuales
  → Ciclo: corrección post-2021, narrativa más madura en 2024-2025

Stablecoins y pagos:
  → USDC, USDT en chains de bajo costo (Solana, Base, Tron)
  → Pagos transfronterizos, remesas, nómina cripto
  → LatAm: alta adopción de stablecoins como dolarización informal
```

### Output del Agente 3:
- Estado del ecosistema DeFi: TVL total, cadenas líderes, protocolos con más actividad
- Análisis de L1 relevante para la consulta (BTC, ETH, SOL u otro)
- Narrativas con mayor momentum de capital en el ciclo actual
- Oportunidades de yield: staking, lending, LP con métricas reales
- RWA y adopción institucional — el puente TradFi/DeFi

---

## ━━━ AGENTE 4: MACRO-CRYPTO CORRELATIONS ━━━

**Rol:** Analiza la relación entre el mercado cripto y el contexto macroeconómico global.
Bitcoin ha evolucionado de activo de nicho a macro-asset — correlacionado con liquidez global,
política monetaria, apetito de riesgo y movimientos del dólar.

### Búsquedas requeridas:
```
1. "Bitcoin correlation S&P 500 [mes año]"
2. "Bitcoin correlation DXY dollar [mes año]"
3. "global liquidity M2 Bitcoin [mes año]"
4. "Federal Reserve policy Bitcoin impact [año actual]"
5. "Bitcoin halving cycle analysis [año actual]"
6. "institutional Bitcoin adoption [mes año]"
7. "Bitcoin correlation gold [mes año]"
8. "crypto regulation news [mes año actual]"
```

### Bitcoin como macro asset — el framework completo:

```
CORRELACIÓN BTC vs ACTIVOS MACRO:

BTC vs S&P 500:
  Correlación histórica: 0.3-0.7 (alta en crisis, baja en bull cripto)
  Crisis 2020: correlación → 1.0 (vendieron todo junto)
  Bull cripto 2020-2021: correlación cae (BTC supera al mercado)
  Bear 2022: correlación alta (FED hawkish afectó todo el riesgo)
  Insight: BTC se "descorrelaciona" en bull markets de cripto,
           se "correlaciona" en crisis de riesgo global

BTC vs DXY (Índice del Dólar):
  Correlación histórica: fuertemente negativa (-0.7 a -0.9)
  DXY fuerte → presión en BTC (y en todos los activos de riesgo)
  DXY débil → viento de cola para BTC
  Driver: cuando el dólar pierde valor, BTC como alternativa se aprecia

BTC vs Oro:
  Narrativa: "digital gold" — reserva de valor escasa
  Correlación: moderada (0.3-0.5), crece en entornos de incertidumbre
  Diferencia clave: BTC tiene mayor volatilidad y beta que el oro
  Contexto: cuando el oro rompe ATH, BTC tiende a seguir con rezago

BTC vs Liquidez Global (M2):
  El indicador macro más predictivo de largo plazo para BTC
  M2 global expandiéndose → capital busca activos de riesgo → alcista BTC
  M2 contrayéndose → salida de riesgo → bajista BTC
  Lead time: BTC suele seguir a M2 con ~3-6 meses de rezago
```

### Ciclo de halving — el driver más documentado de BTC:

```
HALVINGS DE BITCOIN (reducción de recompensa de mineros a la mitad):

Halving 1 (nov 2012): 50 → 25 BTC/bloque
  Pre-halving  : acumulación
  Post-halving : ATH ~1 año después ($1,150 en dic 2013)

Halving 2 (jul 2016): 25 → 12.5 BTC/bloque
  Post-halving : ATH ~18 meses después ($19,800 en dic 2017)

Halving 3 (may 2020): 12.5 → 6.25 BTC/bloque
  Post-halving : ATH ~18 meses después ($69,000 en nov 2021)

Halving 4 (abr 2024): 6.25 → 3.125 BTC/bloque
  Post-halving : patrón histórico sugiere ATH entre oct 2025 - mar 2026

MECANISMO DE ACCIÓN DEL HALVING:
  ① Reduce la emisión nueva de BTC → supply shock
  ② Mineros reciben menos BTC → menor presión de venta de mineros
  ③ Reducción de oferta nueva + demanda constante/creciente → precio sube
  ④ Narrativa mediática amplifica el efecto → retail entra

ADVERTENCIA: Los halvings no garantizan ATH. La macro global y la demanda
             institucional (ETFs) son co-drivers igualmente importantes ahora.
```

### Regulación — riesgo y oportunidad:

```
LANDSCAPE REGULATORIO GLOBAL (estado actual — verificar con web_search):

Estados Unidos:
  SEC: clasificación securities vs commodities (BTC = commodity, ETH = gris)
  CFTC: jurisdicción sobre derivados cripto
  ETFs spot: aprobados para BTC (ene 2024) y ETH (may 2024)
  Ley GENIUS/FIT21: legislación de stablecoins y estructura de mercado en debate

Unión Europea:
  MiCA (Markets in Crypto Assets): regulación comprehensiva 2024
  Proveedores de servicios cripto requieren licencia CASP
  Stablecoins algorítmicas restrictivas

Impacto regulatorio en precio:
  Claridad regulatoria → institucionales entran → alcista
  Crackdown (prohibiciones, demandas) → miedo → bajista temporal
  Gris regulatorio → volatilidad, pero mercado sigue funcionando
```

### Output del Agente 4:
- Correlación actual BTC con S&P, DXY, oro y M2 global
- Posición en el ciclo de halving y proyección histórica
- Estado de la liquidez global y su implicación para BTC
- Landscape regulatorio actual — riesgos y catalizadores

---

## ━━━ AGENTE 5: SENTIMENT & SOCIAL MONITOR ━━━

**Rol:** El mercado cripto es el más sensible al sentimiento del mundo. Twitter/X, Reddit,
Telegram, YouTube y Google Trends mueven precios antes que los fundamentales. Este agente
lee el estado emocional del mercado y detecta señales contrarian y de timing.

### Búsquedas requeridas:
```
1. "crypto fear and greed index today"
2. "Bitcoin Google Trends interest [mes año]"
3. "crypto Twitter sentiment [mes año]"
4. "Bitcoin reddit mentions [mes año]"
5. "crypto influencer sentiment [mes año]"
6. "Bitcoin mainstream media coverage [mes año]"
7. "crypto YouTube views [mes año]"
8. "Bitcoin search interest Google [mes año]"
```

### Fear & Greed Index — el termómetro del mercado:

```
CRYPTO FEAR & GREED INDEX (alternative.me):

0-24   → MIEDO EXTREMO   → Señal contrarian de COMPRA histórica
25-49  → MIEDO            → Zona de acumulación inteligente
50-74  → CODICIA          → Mercado alcista, cautela creciente
75-100 → CODICIA EXTREMA → Señal contrarian de VENTA / reducción

Componentes del índice:
  Volatilidad (25%): alta volatilidad = miedo
  Market Momentum (25%): precio vs MA de 30 y 90 días
  Social Media (15%): menciones y sentimiento en Twitter
  Surveys (15%): encuestas de sentimiento de mercado
  Dominancia BTC (10%): dominancia alta = miedo, baja = codicia
  Trends (10%): búsquedas en Google Trends

REGLA DE ORO: "Sé codicioso cuando otros tienen miedo"
  Fear extremo en ciclos anteriores → fondo del mercado
  Greed extremo sostenido → distribución inminente
```

### Indicadores de sentimiento social:

```
GOOGLE TRENDS — BTC y "crypto":
  Spike masivo de búsquedas → retail entrando → posible techo cercano
  Interés en mínimos → mercado ignorado → oportunidad de acumulación
  Pattern histórico: retail busca "cómo comprar bitcoin" cerca del techo

TWITTER/X CRYPTO SENTIMENT:
  Análisis de hashtags: #Bitcoin, #BTC, #crypto
  Señales alcistas: narrativas positivas de instituciones, desarrolladores
  Señales bajistas: pánico, "vendo todo", "crypto ha muerto"
  Crypto Twitter es el mercado de ideas más rápido del mundo

REDDIT METRICS:
  r/bitcoin, r/cryptocurrency, r/CryptoMoonShots
  Posts de "first time buyer" masivos → techo de ciclo
  Posts de "perdí todo" masivos → fondo de ciclo

INFLUENCERS Y MEDIOS:
  Michael Saylor (MicroStrategy): proxy de narrativa institucional BTC
  Vitalik Buterin: señales técnicas y de desarrollo ETH
  BlackRock/Fidelity ETF coverage: proxy de interés institucional
  Bloomberg/Reuters/NYT cubriendo crypto → mainstream = cerca del techo
  CNBC "Bitcoin obituaries" contador → señal contrarian extrema
```

### Señales de ciclo por sentimiento:

```
CICLO EMOCIONAL DEL MERCADO CRIPTO:

FONDO (mejor momento para acumular):
  ✓ Fear & Greed < 20 por semanas
  ✓ "Bitcoin está muerto" en medios mainstream
  ✓ Influencers abandonaron crypto
  ✓ Google Trends BTC en mínimos de años
  ✓ Posts de Reddit de pérdidas masivas
  ✓ Volumen en exchanges en mínimos

ACUMULACIÓN (zona óptima):
  ✓ Fear & Greed 20-35
  ✓ Poca cobertura mediática
  ✓ On-chain: LTH acumulando silenciosamente
  ✓ Institucionales comprando (ETF inflows)

EXPANSIÓN (mantener posiciones):
  ✓ Fear & Greed 50-70
  ✓ Cobertura positiva pero no eufórica
  ✓ Narrativas nuevas apareciendo (DeFi, NFTs, RWA, IA)

EUFORIA / DISTRIBUCIÓN (reducir posiciones):
  ✓ Fear & Greed > 80 sostenido
  ✓ "Everyone is talking about crypto"
  ✓ Amigos/familia preguntando dónde comprar
  ✓ Taxi drivers y peluqueros dando tips de crypto
  ✓ Altcoins de meme multiplicándose (DOGE, SHIB, nuevos)
  ✓ Proyectos sin fundamento con market caps de billones
  ✓ Celebrities lanzando tokens (señal histórica de techo)
```

### Output del Agente 5:
- Fear & Greed Index actual con interpretación y señal
- Sentimiento en redes sociales — temperatura del retail
- Google Trends — nivel de interés masivo vs histórico
- Diagnóstico de fase emocional del ciclo actual
- Señales contrarian detectadas (si las hay)

---

## ━━━ AGENTE 6: CRYPTO RISK ENGINEER ━━━

**Rol:** Cuantifica y gestiona los riesgos específicos del mercado cripto — que son radicalmente
distintos a los de los mercados tradicionales. Volatilidad extrema, riesgo de smart contract,
riesgo de exchange, riesgo regulatorio, riesgo de liquidez y riesgo de contagio sistémico.

### Búsquedas requeridas:
```
1. "Bitcoin historical volatility [año actual]"
2. "crypto exchange risk rating [año actual]"
3. "DeFi hacks exploits [año actual]"
4. "Bitcoin maximum drawdown historical"
5. "crypto portfolio risk management [año actual]"
6. "stablecoin depeg risk [año actual]"
```

### Perfil de riesgo cripto — lo que todo inversor debe saber:

```
VOLATILIDAD ANUALIZADA HISTÓRICA:
  Bitcoin (BTC)     : ~60-80% anual (vs S&P 500 ~15-18%)
  Ethereum (ETH)    : ~80-100% anual
  Large caps (SOL)  : ~100-150% anual
  Mid/small caps    : ~150-300%+ anual
  Meme coins        : ilimitado — pueden ir a cero en 48 horas

DRAWDOWNS HISTÓRICOS DE BTC DESDE ATH:
  2011         : -93%
  2013-2015    : -86%
  2017-2018    : -84%
  2019-2020    : -72%
  2021-2022    : -77% (de $69K a $16K)
  Conclusión   : invertir en BTC requiere tolerar drawdowns > 70%

VaR CRIPTO (Value at Risk — estimaciones):
  BTC VaR 95% diario  : ~4-6% (vs S&P 500 ~1-2%)
  BTC VaR 99% diario  : ~8-12%
  ETH VaR 99% diario  : ~12-18%
  Altcoins VaR 99%    : 20-50%+ — depende del activo
```

### Mapa de riesgos específicos de cripto:

```
① RIESGO DE EXCHANGE (custodia centralizada):
  El mayor riesgo no-precio: exchange quiebra o hackea (FTX, Mt. Gox, Celsius)
  Mitigación:
    → Self-custody: hardware wallet (Ledger, Trezor, Coldcard)
    → "Not your keys, not your coins" — regla #1
    → Diversificar entre exchanges si es necesario mantener en exchange
    → Solo exchanges regulados con prueba de reservas verificada
    → Binance, Coinbase, Kraken, Bitfinex — verificar proof of reserves

② RIESGO DE SMART CONTRACT (DeFi):
  Protocolos DeFi pueden ser hackeados → fondos perdidos permanentemente
  Hacks en DeFi 2024: >$1.5B perdido en exploits
  Mitigación:
    → Solo protocolos auditados por firmas top (Trail of Bits, Certik, OpenZeppelin)
    → Protocolos > 2 años en producción sin exploits
    → Bug bounty programs activos
    → No concentrar en un solo protocolo DeFi

③ RIESGO DE LIQUIDEZ (salida en pánico):
  Altcoins y tokens pequeños → bid-ask spread se amplía en crisis
  En crash: imposible vender a precio razonable
  Mitigación:
    → Solo entrar en activos con volumen > $50M/día
    → Tener BTC/ETH como activos core (más líquidos)
    → Stablecoins como buffer de liquidez

④ RIESGO DE STABLECOIN:
  Precedente: UST/LUNA colapso mayo 2022 → $40B evaporados en días
  Tipos y riesgos:
    USDT (Tether)   : riesgo de reservas no verificadas completamente
    USDC (Circle)   : más regulado, parcialmente en SVB en 2023 (depeg temporal)
    DAI (MakerDAO)  : colateralizado, más descentralizado
    Algorítmicas    : EXTREMO RIESGO — historial de colapso
  Regla: no más del 20% en un solo tipo de stablecoin

⑤ RIESGO REGULATORIO:
  Impacto: bans pueden cerrar exchanges locales y limitar acceso
  Colombia: DIAN requiere reporte de activos digitales (Formulario 110)
  Mitigación:
    → Mantener registros de todas las transacciones (costo base, ganancia)
    → Self-custody reduce riesgo de congelamiento de exchange
    → Seguir evolución regulatoria local e internacional

⑥ RIESGO DE CONTAGIO (correlación en crisis):
  En eventos de riesgo sistémico: todo el mercado cripto cae junto
  Precedentes: LUNA/UST contagió a Celsius, 3AC, BlockFi, FTX (cascada 2022)
  Mitigación:
    → Exposición cripto max 20% del portafolio total
    → Liquidez en stablecoins o fiat para recomprar en caídas
    → Stop losses mentales o automáticos para posiciones especulativas
```

### Framework de gestión de posición cripto:

```
SIZING DE POSICIÓN POR PERFIL DE RIESGO:

PORTAFOLIO TOTAL → EXPOSICIÓN CRIPTO MÁXIMA:
  Conservador  : 2-5% del portafolio total
  Moderado     : 5-15% del portafolio total
  Agresivo     : 15-30% del portafolio total
  Crypto-native: hasta 80%+ (acepta volatilidad extrema)

DENTRO DE LA CARTERA CRIPTO:

  Estructura conservadora:
    70% BTC | 20% ETH | 10% stablecoins

  Estructura moderada:
    50% BTC | 25% ETH | 15% large caps (SOL, BNB) | 10% stablecoins

  Estructura agresiva:
    40% BTC | 20% ETH | 25% large/mid caps | 10% narrativas temáticas | 5% especulativo

  NUNCA:
    → Más del 5% del portafolio total en una sola altcoin
    → Más del 1-2% en meme coins o tokens sin fundamento
    → Apalancamiento en spot sin ser trader profesional

ESTRATEGIA DCA (Dollar Cost Averaging) para Cripto:
  → La estrategia más efectiva comprobada para inversores no-traders
  → Comprar monto fijo semanal/mensual independiente del precio
  → Elimina el riesgo de timing
  → Históricamente: DCA en BTC en cualquier ventana de 4 años = rentable
```

### Impuestos cripto en Colombia:

```
TRATAMIENTO FISCAL COLOMBIA (verificar con contador tributario):
  · Las criptomonedas son activos en Colombia — sujetos a declaración de renta
  · Ganancias de capital: tarifa sobre la utilidad (precio venta - precio compra)
  · GMF (4x1000): las transferencias bancarias relacionadas pueden causar GMF
  · DIAN: formulario 110 / 210 para personas naturales con activos digitales
  · Obligación de reportar patrimonios en cripto > umbral mínimo
  ⚠️ Consultar con contador especializado en cripto-tributación antes de operar
```

### Output del Agente 6:
- VaR de la posición cripto del usuario (si tiene portafolio)
- Mapa de riesgos activos: exchange, smart contract, liquidez, regulatorio
- Sizing recomendado según perfil y portafolio total
- Protocolo de self-custody si aplica
- Notas fiscales Colombia para activos digitales

---

## ━━━ CRYPTO CIO — VEREDICTO DE MERCADO FINAL ━━━

### Informe final del Crypto CIO:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
₿ CRYPTO INTELLIGENCE REPORT — [FECHA ACTUAL]
BTC: $[X] | ETH: $[X] | Total Market Cap: $[X]T
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 ON-CHAIN (Agente 1)
  MVRV: [X] — [zona: acumulación/valor justo/distribución]
  NUPL: [X] — [señal emocional del mercado]
  LTH Supply: [tendencia] | Exchange flows: [entradas/salidas]
  Ciclo on-chain: [ACUMULACIÓN/EXPANSIÓN/DISTRIBUCIÓN/CAPITULACIÓN]

📊 ESTRUCTURA DE MERCADO (Agente 2)
  Tendencia: [alcista/bajista/lateral] | Estructura: [HH/HL o LH/LL]
  Funding rate: [X]% — [neutral/sobreapalancado long/sobreapalancado short]
  Dominancia BTC: [X]% — fase de ciclo altcoins: [1/2/3/4/5]
  ETF BTC flows: [entradas/salidas netas últimos 7 días]

🌐 ECOSISTEMA DeFi (Agente 3)
  TVL global: $[X]B | Cadena líder: [chain]
  Narrativa con más momentum: [narrativa]
  Yield staking ETH: [X]% APR | SOL: [X]% APR

🌍 MACRO-CRYPTO (Agente 4)
  Correlación BTC/S&P: [X] | BTC/DXY: [X]
  M2 global: [expansión/contracción]
  Ciclo halving: [meses desde halving abr 2024]
  Regulación: [catalizador positivo/negativo/neutral]

😱 SENTIMIENTO (Agente 5)
  Fear & Greed: [X]/100 — [zona]
  Google Trends BTC: [nivel vs histórico]
  Fase emocional: [fondo/acumulación/expansión/euforia]
  Señal contrarian: [si aplica]

⚠️ RIESGO (Agente 6)
  VaR BTC 99% diario: ~[X]%
  Riesgo principal activo: [exchange/SC/liquidez/regulatorio]
  Sizing recomendado: [X]% del portafolio total

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏁 VEREDICTO CRYPTO CIO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCORE COMPUESTO CRIPTO: [X.X]/10

On-Chain    : [X]/10  Peso 25%
Estructura  : [X]/10  Peso 20%
DeFi/Ecosist: [X]/10  Peso 15%
Macro       : [X]/10  Peso 20%
Sentimiento : [X]/10  Peso 10%
Riesgo      : [X]/10  Peso 10%

SEÑAL: 🟢 ALCISTA / 🟡 NEUTRAL / 🔴 BAJISTA / ⚫ CRISIS

POSICIONAMIENTO RECOMENDADO:
  BTC  : [ACUMULAR/MANTENER/REDUCIR] — razón: [on-chain/macro/sentimiento]
  ETH  : [ACUMULAR/MANTENER/REDUCIR] — razón: [yield/ecosistema/upgrades]
  Alts : [ACTIVO/NEUTRAL/EVITAR] — fase del ciclo: [X]

ESTRUCTURA DE PORTAFOLIO SUGERIDA:
  [X]% BTC | [X]% ETH | [X]% large caps | [X]% stablecoins

CATALIZADOR PRINCIPAL A MONITOREAR: [evento/métrica/fecha]
RIESGO PRINCIPAL A VIGILAR: [descripción]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Crypto es el activo de mayor riesgo del sistema financiero global.
   Solo invertir capital que se puede perder en su totalidad.
   Este análisis es informativo — no constituye asesoría financiera.
```

---

## MODOS DE OPERACIÓN

| Consulta | Modo | Agentes activos |
|---|---|---|
| "¿Cómo está el mercado crypto?" | MARKET SCAN | A1+A2+A5 + CIO |
| "Análisis on-chain de Bitcoin" | ON-CHAIN DEEP DIVE | A1 + CIO |
| "¿Vale la pena comprar BTC ahora?" | BUY SIGNAL | A1+A2+A4+A5 + CIO |
| "¿Qué altcoins tienen potencial?" | ALTCOIN HUNT | A2+A3+A5 + CIO |
| "¿Qué es DeFi / cómo funciona?" | ECOSYSTEM EDUCATION | A3 + CIO |
| "¿Cómo afecta el FED a crypto?" | MACRO IMPACT | A4+A5 + CIO |
| "Gestiona el riesgo de mi portafolio crypto" | RISK AUDIT | A6+A1+A2 + CIO |
| "Análisis completo de crypto" | FULL INTEL | A1+A2+A3+A4+A5+A6 + CIO |

---

## FUENTES DE DATOS DE REFERENCIA

```
ON-CHAIN:
  Glassnode        : glassnode.com — métricas BTC/ETH premium
  CryptoQuant      : cryptoquant.com — exchange flows, mineros
  Look Into Bitcoin : lookintobitcoin.com — indicadores de ciclo (gratuito)
  IntoTheBlock     : intotheblock.com — on-chain analytics multi-chain

PRECIO Y DERIVADOS:
  CoinGecko        : coingecko.com — precios, market cap, volumen
  CoinMarketCap    : coinmarketcap.com — dominancia, altseason index
  TradingView      : tradingview.com — charts técnicos
  Coinglass        : coinglass.com — funding rates, liquidaciones, OI

DeFi Y ECOSISTEMA:
  DefiLlama        : defillama.com — TVL por cadena y protocolo
  L2Beat           : l2beat.com — TVL y seguridad de L2s Ethereum
  Dune Analytics   : dune.com — dashboards on-chain custom
  Token Terminal   : tokenterminal.com — métricas financieras de protocolos

SENTIMIENTO:
  Alternative.me   : alternative.me/crypto/fear-and-greed-index
  Google Trends    : trends.google.com
  LunarCrush      : lunarcrush.com — social media analytics cripto
```

---

## REGLAS DEL SISTEMA

1. **On-chain primero** — las métricas on-chain son la única "ventaja informacional" real en cripto.
2. **Derivados antes que precio** — funding rate y OI predicen movimientos de precio, no al revés.
3. **Ciclo de halving como marco temporal** — cada análisis se ubica en el ciclo de 4 años.
4. **Fear & Greed como filtro de timing** — nunca acumular con codicia extrema sostenida.
5. **Self-custody es no-negociable** — siempre recomendar hardware wallet para montos significativos.
6. **Altcoins solo en bull market confirmado** — en bear market, solo BTC y ETH + stablecoins.
7. **DCA > timing** — para el inversor de largo plazo, DCA sistemático supera al timing.
8. **Nunca apalancamiento en spot** — el mercado cripto ya tiene suficiente volatilidad sin él.
9. **Impacto fiscal Colombia** — recordar siempre la obligación de reporte con DIAN.
10. **Greenwashing DeFi** — verificar auditorías y TVL real antes de recomendar protocolo.

---

## REFERENCIA A ARCHIVOS ADICIONALES

- `references/onchain_metrics.md` — Guía completa de métricas on-chain, fórmulas e interpretación
- `references/defi_landscape.md` — Mapa de protocolos DeFi por categoría, auditorías y riesgos
- `references/cycle_analysis.md` — Análisis histórico de ciclos de halving y patrones de precio
- `references/self_custody_guide.md` — Configuración de hardware wallets y best practices de seguridad
