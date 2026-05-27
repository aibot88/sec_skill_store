---
name: due-diligence-spain
description: Sistema completo de due diligence para transacciones M&A en España. Abarca análisis jurídico (mercantil, regulatorio, compliance), fiscal (CIT, IVA, retenciones, facturación electrónica) y medioambiental (licencias, pasivos, responsabilidad). Incluye matrices de riesgo cuantitativas, workflows de ejecución, templates de informes y referencias normativas BOE/UE/ISO actualizadas. Úsalo cuando el usuario solicite due diligence en España, análisis de riesgos transaccionales, evaluación pre-adquisición o auditoría de cumplimiento normativo para share deals o asset deals.
---

# Due Diligence España - Sistema Integral M&A

## 📋 Índice de Contenidos

1. [Triggers y Casos de Uso](#triggers-y-casos-de-uso)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Workflows de Ejecución](#workflows-de-ejecución)
4. [Modelo A: Due Diligence Jurídica](#modelo-a-due-diligence-jurídica)
5. [Modelo B: Due Diligence Fiscal](#modelo-b-due-diligence-fiscal)
6. [Modelo C: Due Diligence Técnica Medioambiental](#modelo-c-due-diligence-técnica-medioambiental)
7. [Sistema de Cuantificación de Riesgos](#sistema-de-cuantificación-de-riesgos)
8. [Deliverables y Formatos](#deliverables-y-formatos)

---

## Triggers y Casos de Uso

### Triggers Automáticos

Activa esta skill cuando el usuario menciona:
- **Transacciones:** "due diligence", "DD", "M&A", "share deal", "asset deal", "adquisición", "compraventa de empresa"
- **Análisis:** "análisis de riesgos", "evaluación pre-adquisición", "auditoría jurídica", "revisión fiscal", "pasivos ambientales"
- **Contexto España:** Referencias a normativa española (BOE, LSC, LGT, RGPD, etc.) o jurisdicción española
- **Matrices:** "matriz de riesgos", "EV", "RPN", "scoring", "red flags", "contingencias"
- **Outputs:** "informe de DD", "resumen ejecutivo", "Data Request List", "DRL", "R&W", "CPs"

### Casos de Uso Principales

**Caso 1: Preparación Integral de Due Diligence**
- Input: "Necesito preparar una due diligence completa para adquirir una empresa industrial española"
- Output: Informe integrado con los 3 modelos (jurídico, fiscal, ambiental), matriz de riesgos consolidada, DRL, CPs recomendadas

**Caso 2: Análisis de Área Específica**
- Input: "Revisa el cumplimiento RGPD de este target" o "Analiza los riesgos fiscales de IVA"
- Output: Deep-dive en área específica con hallazgos, cuantificación EV y recomendaciones

**Caso 3: Validación de Hallazgos y Cuantificación**
- Input: "He identificado estos riesgos, ayúdame a cuantificarlos y priorizarlos"
- Output: Matriz de riesgos con scoring RPN, EV monetizado, propuestas de mitigación (CPs/R&W/escrow)

**Caso 4: Generación de Documentos Transaccionales**
- Input: "Genera el documento de Data Request List" o "Crea el mapa de R&W basado en hallazgos"
- Output: Documentos estructurados listos para negociación

---

## Arquitectura del Sistema

### Estructura de Tres Modelos Integrados

```
┌─────────────────────────────────────────────────────────────┐
│               DUE DILIGENCE INTEGRAL (ESPAÑA)               │
├───────────────────┬───────────────────┬─────────────────────┤
│   MODELO A        │   MODELO B        │   MODELO C          │
│   Jurídico        │   Fiscal          │   Medioambiental    │
├───────────────────┼───────────────────┼─────────────────────┤
│ • Societario      │ • IS (CIT)        │ • Licencias (AAI/   │
│ • Contratación    │ • IVA             │   APCA)             │
│ • Laboral/SS      │ • Retenciones     │ • Emisiones/        │
│ • RGPD/Privacidad │ • Locales         │   vertidos          │
│ • IP/IT           │ • Veri*factu      │ • Residuos          │
│ • Competencia     │ • Factura e-      │ • Suelos contami-   │
│ • PBC/FT          │ • Inspecciones    │   nados             │
│ • Compliance      │ • TP              │ • Responsabilidad   │
│   penal (31 bis)  │                   │   ambiental         │
└───────────────────┴───────────────────┴─────────────────────┘
                             ↓
         ┌──────────────────────────────────────┐
         │   MATRIZ DE RIESGOS CONSOLIDADA      │
         │   • Scoring: RAG + RPN (P×I)         │
         │   • EV monetizado: Prob(%) × €       │
         │   • Reservas: EV × factor prudencia  │
         │   • Priorización por materialidad    │
         └──────────────────────────────────────┘
                             ↓
         ┌──────────────────────────────────────┐
         │   MECANISMOS DE MITIGACIÓN           │
         │   • CPs (Conditions Precedent)       │
         │   • R&W (Reps & Warranties)          │
         │   • Indemnities específicas          │
         │   • Escrows / Ajustes precio         │
         └──────────────────────────────────────┘
```

### Escala de Materialidad Universal

**Sistema RAG (Rojo-Ámbar-Verde):**
- 🔴 **Rojo:** Crítico / deal-breaker → Requiere CP obligatoria o no-go
- 🟡 **Ámbar:** Mitigable → CP/R&W/indemnidad suficiente
- 🟢 **Verde:** Menor → R&W genérica, sin ajuste de precio

**Sistema de Scoring Cuantitativo:**
```
RPN (Risk Priority Number) = Probabilidad (P) × Impacto (I)

Probabilidad (P): 1=remoto … 5=alto
Impacto (I): 1=<0.5% EV … 5=>10% EV

EV (Expected Value) = Probabilidad (%) × Impacto (€)

Reserva recomendada = EV × factor_prudencia (1.1–1.5)

Umbral materialidad = ≥0.5–1.0% EV o ≥250.000€
```

---

## Workflows de Ejecución

### Workflow 1: Due Diligence Full Scope (Modelo Completo)

**Fase 1: Setup y Parametrización**
```python
# 1. Definir alcance
parametros = {
    "tipo_deal": "share_deal | asset_deal",
    "target": {
        "nombre": str,
        "sector": str,
        "CNAE": list,
        "volumen_negocio": float,  # € para materialidad
        "n_empleados": int,
        "geografía": list  # CCAA para normativa regional
    },
    "periodo_revisión": {
        "estatutos_actas": 10,  # años
        "contratos": 5,
        "licencias": "vigentes + 5 años histórico",
        "fiscal": 4,  # años (prescripción LGT)
        "ambiental": "histórico completo suelos"
    },
    "materialidad": {
        "umbral_porcentual": 0.01,  # 1% EV
        "umbral_absoluto": 250000,  # €
        "top_contratos": 20
    }
}
```

**Fase 2: Data Request y Recopilación**
```
1. Enviar Data Request List (DRL) completa → Ver references/drl_template.md
2. Setup data room estructurado
3. Calendario Q&A con target
4. Identificar limitaciones (info confidencial, litigios sub-judice)
```

**Fase 3: Ejecución Paralela de Modelos**

Ejecutar simultáneamente:
- **Modelo A (Jurídico)** → 4.1-4.8 según checklist
- **Modelo B (Fiscal)** → 4.1-4.6 según checklist  
- **Modelo C (Ambiental)** → 4.1-4.5 según checklist

**Fase 4: Consolidación de Hallazgos**
```
Para cada hallazgo identificado:

1. Clasificar por modelo (A/B/C)
2. Asignar ID único (J-01, F-01, E-01)
3. Evaluar:
   - RAG: Rojo/Ámbar/Verde
   - Probabilidad (P): 1-5 o porcentaje
   - Impacto (€): Cuantificación monetaria
4. Calcular:
   - RPN = P × I
   - EV = Probabilidad(%) × Impacto(€)
5. Proponer mitigación:
   - Tipo: CP | R&W | Indemnity | Escrow
   - Coste/ajuste precio
6. Añadir a matriz consolidada
```

**Fase 5: Generación de Deliverables**
```
Outputs finales:

1. Resumen Ejecutivo (2-4 páginas)
   - Top 5-10 hallazgos críticos
   - EV agregado por modelo
   - Reservas recomendadas
   - CPs esenciales

2. Informes Detallados (3 documentos)
   - Modelo A: Informe Jurídico (~30-50 págs)
   - Modelo B: Informe Fiscal (~20-30 págs)
   - Modelo C: Informe Ambiental (~15-25 págs)

3. Anexos Operativos
   - Matriz de Riesgos Consolidada (Excel/CSV)
   - Data Request List con tracking
   - Log Q&A y Red Flags
   - Mapa R&W y CPs
   - Clausulado tipo (indemnities, ajustes precio)

Formatos: DOCX (informes), XLSX (matrices), PDF (entrega final)
```

### Workflow 2: Quick Assessment (Revisión Específica)

Para análisis de área única (ej: solo fiscal, solo RGPD):

```
1. Identificar scope limitado (qué checklist del modelo)
2. Parametrizar materialidad reducida
3. Ejecutar solo esa sección del modelo
4. Generar mini-informe con:
   - Hallazgos específicos del área
   - Matriz de riesgos parcial
   - Recomendaciones targeted
5. Output: Informe breve (5-10 páginas) + matriz Excel
```

### Workflow 3: Post-Hallazgo (Cuantificación y Mitigación)

Cuando ya existen hallazgos identificados:

```python
def cuantificar_hallazgo(hallazgo):
    """
    Input: Descripción textual del hallazgo
    Output: Hallazgo estructurado con scoring
    """
    
    # 1. Extracción de información
    info = {
        "descripción": str,
        "norma_incumplida": str,  # ej: "RGPD art.30", "LGT art.191"
        "evidencia": list,
        "área_afectada": str  # Jurídico|Fiscal|Ambiental
    }
    
    # 2. Evaluación de probabilidad
    prob = evaluar_probabilidad(
        evidencia=info["evidencia"],
        jurisprudencia=buscar_precedentes(),
        criterio_administración=consultar_criterios()
    )
    
    # 3. Cuantificación de impacto
    impacto_euro = calcular_impacto(
        tipo="sanción | contingencia | CAPEX | pérdida_contrato",
        parámetros={
            "base_sanción": float,  # para multas
            "rango_multa": tuple,  # (min, max)
            "coste_remediación": float,  # para ambientales/técnicos
            "revenue_at_risk": float,  # para contratos
            "legal_costs": float
        }
    )
    
    # 4. Scoring
    P = prob  # 1-5 o %
    I = clasificar_impacto(impacto_euro, EV_total)  # 1-5
    RPN = P * I
    EV = (prob / 100) * impacto_euro if prob_porcentaje else P * impacto_euro / 5
    
    # 5. Clasificación RAG
    RAG = "Rojo" if RPN >= 15 or deal_breaker else \
          "Ámbar" if RPN >= 8 else \
          "Verde"
    
    # 6. Propuesta de mitigación
    mitigación = proponer_mitigación(
        RAG=RAG,
        tipo_hallazgo=info["área_afectada"],
        cuantificación={"RPN": RPN, "EV": EV}
    )
    
    return {
        "id": generar_id(área),  # J-01, F-01, E-01
        "hallazgo": info["descripción"],
        "norma": info["norma_incumplida"],
        "RAG": RAG,
        "P": P,
        "I": I,
        "Impacto_euro": impacto_euro,
        "RPN": RPN,
        "EV": EV,
        "mitigación": mitigación,
        "CP_RW": mitigación["mecanismo"],
        "ajuste_precio": EV if mitigación["ajuste"] else 0
    }
```

---

## Modelo A: Due Diligence Jurídica

### 4.1 Societario y Gobierno Corporativo

**Objetivos:**
- Verificar validez de la estructura societaria
- Confirmar facultades de órganos y representantes
- Detectar vicios en modificaciones estructurales
- Validar pactos parasociales y drag-along/tag-along

**Checklist Operativo:**

```markdown
☐ Estatutos sociales vigentes y actualizados (contraste con RMMM)
☐ Libro de socios/acciones completo
☐ Actas JG/CA últimos 10 años (verificar quórums y mayorías)
☐ Composición consejo: administradores, poderes, caducidad cargos
☐ Pactos parasociales vigentes (cláusulas de arrastre, acompañamiento, prelación)
☐ Modificaciones estructurales previas:
  ☐ Fusiones/escisiones: Proyectos, balances, informes experto, publicidad web/BORME
  ☐ Ampliaciones/reducciones capital: Acuerdos, desembolsos, prima de emisión
  ☐ Transformación de tipo social
☐ Garantías y gravámenes:
  ☐ Pignoraciones acciones/participaciones
  ☐ Garantías hipotecarias sobre activos
  ☐ Avales y garantías personales
  ☐ Contraste Registro Mercantil y Bienes Muebles
```

**Marco Normativo:**
- **RDL 5/2023** (Libro I: modificaciones estructurales; deroga Ley 3/2009)
- **LSC** (RDL 1/2010): Régimen societario general
- **RRM** (RD 1784/1996): Reglamento del Registro Mercantil

**Output:** Sección de informe con:
- Validación de estructura
- Red flags de gobierno (ej: acuerdos sin quórum, poderes caducados)
- Cargas y gravámenes identificados
- CP recomendada: Cancelación de cargas, regularización registral

### 4.2 Contratación Clave

**Objetivos:**
- Mapear dependencias contractuales críticas
- Identificar cláusulas de change of control
- Evaluar riesgo de terminación post-transacción

**Checklist Operativo:**

```markdown
☐ Top 20 clientes por volumen (facturación últimos 2 años)
☐ Top 20 proveedores por coste
☐ Análisis de cada contrato material (>1% EV):
  ☐ Duración y renovación (plazo, tácita reconducción, prórrogas)
  ☐ Cláusulas críticas:
    ✓ Change of control: ¿Derecho de terminación?
    ✓ Exclusividad (geográfica/sectorial)
    ✓ No competencia durante y post-contrato
    ✓ Penalidades por incumplimiento/rescisión
    ✓ Step-in rights (para financiadores)
    ✓ Subcontratación y cesión de créditos
    ✓ SLA/OLA con penalidades
    ✓ Propiedad del deliverable/IP generada
  ☐ Garantías prestadas (avales, bonos, retenciones)
  ☐ Condiciones de pago (plazos, confirming, factoring)
☐ Mapeo de dependencias:
  ☐ Clientes >15% ingresos (riesgo concentración)
  ☐ Proveedores >15% coste (riesgo supply chain)
  ☐ Proveedores monopolio (difícil sustitución)
☐ Contratos financieros:
  ☐ Financiación vigente (préstamos, líneas crédito)
  ☐ Covenants financieros (ratios, restricciones)
  ☐ Vencimientos y amortizaciones
  ☐ Garantías asociadas (hipotecas, pledges)
☐ Arrendamientos y leasing:
  ☐ Inmuebles (locales, oficinas, naves)
  ☐ Equipamiento (maquinaria, vehículos, IT)
  ☐ Plazos, opciones de compra, rentas
```

**Análisis de Dependencias:**

```python
def calcular_riesgo_contrato(contrato):
    """
    Evalúa el riesgo de un contrato específico
    """
    score_riesgo = 0
    
    # Factor 1: Change of control
    if contrato.tiene_change_of_control:
        if contrato.terminación_automática:
            score_riesgo += 5  # CRÍTICO
        elif contrato.consentimiento_requerido:
            score_riesgo += 3  # ALTO
    
    # Factor 2: Peso económico
    peso = contrato.volumen_anual / EV_empresa
    if peso > 0.15:
        score_riesgo += 4
    elif peso > 0.05:
        score_riesgo += 2
    
    # Factor 3: Sustituibilidad
    if contrato.proveedor_único or contrato.cliente_estratégico:
        score_riesgo += 3
    
    # Factor 4: Condiciones de salida
    if contrato.penalidad_terminación > 0.10 * contrato.volumen_anual:
        score_riesgo += 2
    
    # Clasificación
    if score_riesgo >= 10:
        return {"RAG": "Rojo", "acción": "CP: Consentimiento previo a closing"}
    elif score_riesgo >= 6:
        return {"RAG": "Ámbar", "acción": "R&W + Plan de mitigación"}
    else:
        return {"RAG": "Verde", "acción": "R&W estándar"}
```

**Output:**
- Tabla de contratos materiales con scoring
- Identificación de change of control críticos → CP
- Mapeo de dependencias cliente/proveedor
- R&W específicas sobre vigencia y no-breach

### 4.3 Laboral y Seguridad Social

**Objetivos:**
- Verificar regularidad de plantilla y contratación
- Detectar cesión ilegal de trabajadores
- Evaluar riesgos de inspecciones y litigios
- Cuantificar contingencias SS

**Checklist Operativo:**

```markdown
☐ Censo de trabajadores actualizado (RNT):
  ☐ Tipo de contrato (indefinido, temporal, prácticas, formación)
  ☐ Antigüedad por trabajador
  ☐ Convenio colectivo aplicable
  ☐ Categoría profesional y salario
☐ Contratación temporal:
  ☐ Causas de temporalidad (obra/servicio, eventual, interinidad)
  ☐ Riesgo de conversión en indefinidos
  ☐ Encadenamiento de contratos (fraude de ley)
☐ Subcontratación y cesión ilegal:
  ☐ Contratas externas (principalmente en actividad principal)
  ☐ ETTs: Convenio, duración, cotización
  ☐ Riesgo de reconocimiento laboral directo
☐ Representación legal de trabajadores:
  ☐ Comité de empresa / Delegados de personal
  ☐ Secciones sindicales
  ☐ Negociación colectiva (acuerdos empresa, convenios franja)
☐ Litigios laborales:
  ☐ Despidos impugnados (en curso y resueltos 5 años)
  ☐ Reclamaciones salariales
  ☐ Accidentes de trabajo (responsabilidad, sanciones)
  ☐ Acoso / discriminación
☐ Inspecciones de Trabajo:
  ☐ Actas de infracción últimos 5 años
  ☐ Sanciones (cuantía, pagadas/recurridas)
  ☐ Requerimientos pendientes
☐ Seguridad Social:
  ☐ Certificado de estar al corriente (VIASS)
  ☐ Cotizaciones: Bases, tipos, regularizaciones
  ☐ Bonificaciones aplicadas (verificar requisitos)
  ☐ Inspecciones TGSS
☐ Compliance laboral:
  ☐ Planes de igualdad (si >50 trabajadores desde 2022)
  ☐ Registro jornada (RD-ley 8/2019)
  ☐ Registro salarial (RD 902/2020)
  ☐ Protocolo acoso (si aplica)
  ☐ Planes LGTBI (Ley 4/2023, si >50 trabajadores)
```

**Marco Normativo:**
- **ET** (RDL 2/2015): Estatuto de los Trabajadores
- **LGSS** (RDL 8/2015): Ley General de Seguridad Social
- **Ley 4/2023**: Derechos de las personas trans y LGTBI

**Cuantificación Típica:**

```python
# Ejemplo: Contingencia por conversión contratos temporales
n_temporales_riesgo = 15
salario_medio_bruto = 30000  # €/año
años_antigüedad_media = 2.5
indemnización_por_trabajador = min(
    salario_medio_bruto / 365 * 33 * años_antigüedad_media * 365,
    24 * salario_medio_bruto / 12  # Tope 24 mensualidades
)
contingencia_total = n_temporales_riesgo * indemnización_por_trabajador
probabilidad = 0.40  # 40% si hay indicios claros de temporalidad fraudulenta
EV_laboral = probabilidad * contingencia_total
```

**Output:**
- Censo analizado con red flags
- Cuantificación de contingencias (conversión temporal, subcontratación ilegal)
- R&W: regularidad plantilla, inexistencia litigios materiales, cotizaciones al día

### 4.4 Privacidad y Ciberseguridad (RGPD)

**Objetivos:**
- Validar cumplimiento RGPD/LOPDGDD
- Identificar brechas de seguridad y exposición sancionatoria
- Evaluar contratos de encargados de tratamiento

**Checklist Operativo:**

```markdown
☐ Registro de Actividades de Tratamiento (art. 30 RGPD):
  ☐ Existe y está actualizado
  ☐ Incluye todas las actividades (RRHH, clientes, proveedores, marketing, etc.)
  ☐ Detalles: finalidades, bases legitimación, categorías datos, destinatarios, plazos
☐ DPO (Data Protection Officer):
  ☐ ¿Es obligatorio? (>250 empleados o tratamiento masivo de datos especiales)
  ☐ Si aplica: Designado, contacto publicado, recursos suficientes
☐ Bases de legitimación:
  ☐ Consentimiento (cuando aplica): Libre, específico, informado, inequívoco
  ☐ Ejecución contrato
  ☐ Interés legítimo (con balance de intereses)
  ☐ Obligación legal
  ☐ Datos especiales (art. 9): Salud, origen racial, etc. → Legitimación reforzada
☐ Transferencias internacionales:
  ☐ ¿Existen transferencias fuera EEE?
  ☐ Mecanismo: Decisión adecuación, cláusulas contractuales tipo (SCC), BCR
  ☐ Análisis de transferencias (EDPB Guidelines 07/2020)
☐ Evaluaciones de Impacto (DPIA - art. 35):
  ☐ Identificar tratamientos alto riesgo (scoring, vigilancia, datos especiales masivos)
  ☐ DPIA realizadas y actualizadas
  ☐ Medidas de mitigación implementadas
☐ Brechas de seguridad:
  ☐ Registro de brechas (últimos 3 años)
  ☐ Notificaciones a AEPD (72h) y afectados
  ☐ Medidas correctivas adoptadas
☐ Contratos art. 28 (Encargados de tratamiento):
  ☐ Identificar todos los encargados (cloud providers, software SaaS, consultores, etc.)
  ☐ Contratos firmados con cláusulas RGPD obligatorias
  ☐ Subencargados autorizados
☐ Cookies y tracking:
  ☐ Política de cookies conforme (LSSI y RGPD)
  ☐ Consentimiento previo (salvo técnicas imprescindibles)
  ☐ Configuración: Rechazo fácil = Aceptación fácil
☐ Derechos de interesados:
  ☐ Procedimientos para ejercicio (acceso, rectificación, supresión, portabilidad, oposición, limitación)
  ☐ Plazos de respuesta (1 mes) cumplidos
  ☐ Log de solicitudes y respuestas
```

**Marco Normativo:**
- **RGPD** (UE) 2016/679: Reglamento General de Protección de Datos
- **LO 3/2018** (LOPDGDD): Ley Orgánica de Protección de Datos española

**Cuantificación de Riesgos RGPD:**

```python
# Sanciones RGPD: Hasta 20M€ o 4% facturación anual global (el mayor)
# Tier 1 (infracciones graves): hasta 10M€ o 2%
# Tier 2 (infracciones muy graves): hasta 20M€ o 4%

def calcular_sanción_rgpd(incumplimiento, facturación_anual):
    """
    Estima sanción potencial RGPD
    """
    # Criterios AEPD: gravedad, intencionalidad, categorías datos, nº afectados, reincidencia
    
    if incumplimiento["tipo"] == "ausencia_registro_actividades":
        sanción_base = min(50000, 0.01 * facturación_anual)  # Tier 1
        prob = 0.25  # Si AEPD inspecciona
    
    elif incumplimiento["tipo"] == "falta_contratos_art28":
        sanción_base = min(100000, 0.02 * facturación_anual)  # Tier 1
        prob = 0.30
    
    elif incumplimiento["tipo"] == "transferencias_sin_garantías":
        sanción_base = min(500000, 0.02 * facturación_anual)  # Tier 2 potencial
        prob = 0.35
    
    elif incumplimiento["tipo"] == "brecha_no_notificada":
        sanción_base = min(1000000, 0.04 * facturación_anual)  # Tier 2
        prob = 0.50  # Mayor prob si brecha significativa
    
    else:
        sanción_base = 50000
        prob = 0.20
    
    EV = prob * sanción_base
    return {
        "sanción_estimada": sanción_base,
        "probabilidad": prob,
        "EV": EV,
        "RAG": "Rojo" if EV > 100000 else "Ámbar" if EV > 25000 else "Verde"
    }
```

**Output:**
- Informe de cumplimiento RGPD con gaps identificados
- Cuantificación EV de sanciones potenciales
- Indemnidad específica para sanciones AEPD
- CP (si crítico): Subsanación de incumplimientos tier-2 antes de closing

### 4.5 Propiedad Industrial e Intelectual (IP/IT)

**Objetivos:**
- Verificar titularidad de marcas, patentes, diseños, software
- Evaluar riesgos de infracción o disputas
- Validar licencias de software (propietario y open-source)

**Checklist Operativo:**

```markdown
☐ Cartera de Propiedad Industrial:
  ☐ Marcas registradas (OEPM / EUIPO):
    ✓ Números de registro
    ✓ Clases de Niza cubiertas
    ✓ Vigencia (renovaciones cada 10 años)
    ✓ Titularidad (empresa vs. fundadores/terceros)
    ✓ Licencias otorgadas o recibidas
  ☐ Patentes (si aplica):
    ✓ Números de patente (nacional, EP, PCT)
    ✓ Estado (en tramitación, concedida, caducada)
    ✓ Tasas de mantenimiento al día
    ✓ Titularidad y coinventores
    ✓ Libertad de explotación (freedom to operate)
  ☐ Diseños industriales:
    ✓ Registros vigentes
    ✓ Productos cubiertos
☐ Propiedad Intelectual (derechos de autor):
  ☐ Software propietario desarrollado:
    ✓ Cesión de derechos por empleados/contratistas (art. 97 LPI: presunción en sw laboral)
    ✓ Código fuente en escrow (si licenciado a terceros)
    ✓ Documentación técnica
  ☐ Contenidos (web, marketing, manuales):
    ✓ Autoría y cesión de derechos
    ✓ Uso de contenidos de terceros (licencias, stock photos)
☐ Licencias de software:
  ☐ Software comercial (Microsoft, Oracle, SAP, Salesforce, etc.):
    ✓ Licencias vigentes y auditorías
    ✓ Cláusulas de change of control
    ✓ Número de usuarios/dispositivos cubiertos
  ☐ Open-source:
    ✓ Inventario de componentes open-source usados
    ✓ Licencias: MIT, Apache, GPL, LGPL, AGPL
    ✓ Compatibilidad de licencias (ej: GPL es copyleft → viral)
    ✓ Riesgo: Software propietario derivado de GPL → obligación de liberar
☐ SaaS y Cloud:
  ☐ Contratos con proveedores SaaS
  ☐ Términos de servicio (ToS): Propiedad de datos, portabilidad, SLA
  ☐ Código en escrow (si dependencia crítica)
☐ Nombres de dominio:
  ☐ Registro de dominios (.es, .com, .eu, etc.)
  ☐ Titularidad (empresa o terceros)
  ☐ Vencimientos y renovaciones
☐ Litigios y disputas IP:
  ☐ Procedimientos de infracción activos
  ☐ Reclamaciones de terceros
  ☐ Oposiciones a marcas/patentes
```

**Marco Normativo:**
- **Ley 17/2001** de Marcas
- **LPI** (RDL 1/1996): Ley de Propiedad Intelectual
- **Ley 24/2015** de Patentes

**Análisis de Open-Source:**

```python
# Compatibilidad de licencias open-source
licencias_permisivas = ["MIT", "Apache-2.0", "BSD-3-Clause"]
licencias_copyleft_débil = ["LGPL-2.1", "LGPL-3.0", "MPL-2.0"]
licencias_copyleft_fuerte = ["GPL-2.0", "GPL-3.0", "AGPL-3.0"]

def analizar_riesgo_opensource(componentes):
    """
    Evalúa riesgos de licencias open-source
    """
    riesgos = []
    
    for comp in componentes:
        if comp.licencia in licencias_copyleft_fuerte:
            if comp.uso == "linked_dynamically":
                riesgo = "ÁMBAR: GPL/AGPL con linking dinámico. Verificar si obliga a liberar código."
            elif comp.uso == "linked_statically" or comp.uso == "modified":
                riesgo = "ROJO: GPL/AGPL con linking estático o modificación. Probable obligación de liberar."
            else:
                riesgo = "VERDE: Uso aislado de GPL/AGPL."
            
            riesgos.append({
                "componente": comp.nombre,
                "licencia": comp.licencia,
                "riesgo": riesgo,
                "mitigación": "Auditoría de código + segregación o sustitución componente"
            })
    
    return riesgos
```

**Output:**
- Inventario completo de IP/IT con estado y titularidad
- Red flags de licencias open-source incompatibles
- R&W: Titularidad exclusiva, no infracción de terceros, licencias válidas
- CP (si crítico): Transferencia formal de IP de fundadores a sociedad

### 4.6 Derecho de Competencia y Concentraciones

**Objetivos:**
- Detectar riesgos de prácticas anticompetitivas
- Evaluar obligación de notificación de concentración (CNMC/CE)

**Checklist Operativo:**

```markdown
☐ Análisis antitrust:
  ☐ Acuerdos horizontales (con competidores):
    ✓ Fijación de precios, reparto de mercados, limitación producción (hard-core)
    ✓ Intercambio de información sensible (precios, clientes, estrategias)
  ☐ Acuerdos verticales (con clientes/proveedores):
    ✓ Fijación de precios de reventa
    ✓ Restricciones territoriales
    ✓ Exclusividad (de compra/venta)
  ☐ Abuso de posición dominante (si cuota mercado >40%):
    ✓ Precios predatorios
    ✓ Negativa de suministro
    ✓ Descuentos exclusividad/fidelidad
    ✓ Ventas atadas (tying)
☐ Notificación de concentración:
  ☐ Umbrales CNMC (Ley 15/2007):
    ✓ Cuota mercado >25% (adquirente + target)
    ✓ O: Facturación conjunta en España >240M€ y cada parte >60M€
  ☐ Umbrales UE (Reglamento 139/2004):
    ✓ Facturación mundial >5.000M€ y UE >250M€ cada parte
    ✓ O: Facturación mundial >2.500M€ y UE >100M€ cada parte (con presencia significativa en ≥3 Estados)
  ☐ Si notificación obligatoria:
    ✓ Timing: Pre-closing notification y standstill obligation
    ✓ Plazo resolución: CNMC 1 mes (Fase I) o +3 meses (Fase II); CE 25 días laborables (Fase I)
☐ Investigaciones y sanciones:
  ☐ Procedimientos CNMC o CE abiertos
  ☐ Sanciones previas (última década)
  ☐ Programas de clemencia activos
```

**Marco Normativo:**
- **LDC 15/2007**: Ley de Defensa de la Competencia (España)
- **Reglamento (CE) 139/2004**: Control de concentraciones UE
- **Reglamento (CE) 1/2003**: Aplicación normas competencia UE

**Cálculo de Umbrales:**

```python
def evaluar_notificación_concentración(adquirente, target):
    """
    Determina si se requiere notificación a CNMC o CE
    """
    # Umbrales CNMC
    facturacion_conjunta_spain = adquirente.facturacion_ES + target.facturacion_ES
    facturacion_min = min(adquirente.facturacion_ES, target.facturacion_ES)
    
    cuota_mercado = calcular_cuota_mercado(adquirente, target)
    
    notificar_CNMC = (
        (cuota_mercado > 0.25) or
        (facturacion_conjunta_spain > 240e6 and 
         adquirente.facturacion_ES > 60e6 and 
         target.facturacion_ES > 60e6)
    )
    
    # Umbrales CE
    facturacion_mundial_conjunta = adquirente.facturacion_mundial + target.facturacion_mundial
    facturacion_UE_adquirente = adquirente.facturacion_UE
    facturacion_UE_target = target.facturacion_UE
    
    notificar_CE = (
        (facturacion_mundial_conjunta > 5000e6 and 
         facturacion_UE_adquirente > 250e6 and 
         facturacion_UE_target > 250e6) or
        (facturacion_mundial_conjunta > 2500e6 and
         # ... umbral alternativo
         )
    )
    
    return {
        "CNMC": notificar_CNMC,
        "CE": notificar_CE,
        "timing": "Pre-closing + standstill" if (notificar_CNMC or notificar_CE) else "N/A"
    }
```

**Output:**
- Análisis de umbrales con datos cuantitativos
- Riesgos antitrust identificados
- CP crítica: Obtención autorización CNMC/CE antes de closing (si aplica)
- Timeline de transacción ajustado (+1-4 meses si Fase I, +4-7 meses si Fase II)

### 4.7 PBC/FT (Prevención Blanqueo de Capitales)

**Aplicable si:** Target es sujeto obligado (Ley 10/2010)

**Checklist Operativo:**

```markdown
☐ Políticas y procedimientos:
  ☐ Manual PBC/FT aprobado y actualizado
  ☐ Enfoque basado en riesgo (EBR)
  ☐ Políticas KYC (Know Your Customer) y KYB (Know Your Business)
☐ Diligencia debida de clientes:
  ☐ Identificación y verificación de identidad
  ☐ Titularidad real (beneficiarios finales ≥25% participación)
  ☐ Clasificación de riesgo (bajo, medio, alto, PEP)
  ☐ Monitorización continua de operaciones
☐ PEP (Personas Políticamente Expuestas):
  ☐ Procedimientos reforzados para PEP y familiares/colaboradores
  ☐ Listas actualizadas (nacionales e internacionales)
☐ Listas de sanciones:
  ☐ Screening contra listas ONU, UE, OFAC (EE.UU.)
  ☐ Periodicidad de verificación (continua o periódica)
☐ Formación:
  ☐ Programa de formación continua para empleados relevantes
  ☐ Registros de asistencia y contenidos
☐ Órgano de control:
  ☐ Designación del Representante ante SEPBLAC (RO)
  ☐ Órgano de Control Interno (OCI) si aplica
  ☐ Recursos y competencias adecuadas
☐ Reporte a SEPBLAC:
  ☐ Operaciones comunicadas (sospechosas, sistemáticas)
  ☐ Declaraciones S-1 (operaciones >100.000€) y mensuales
  ☐ Expediente de cada comunicación
☐ Auditoría externa:
  ☐ Auditorías trienales realizadas (obligación desde 2021)
  ☐ Informe de auditor experto
  ☐ Implementación de recomendaciones
☐ Sanciones:
  ☐ Expedientes sancionadores (SEPBLAC, Banco de España, CNMV, DGS)
  ☐ Requerimientos de información
```

**Marco Normativo:**
- **Ley 10/2010** de prevención del blanqueo de capitales
- **RD 304/2014**: Reglamento de la Ley 10/2010

**Cuantificación:**

```python
# Sanciones PBC: Muy graves hasta 150% del importe blanqueado (o beneficio) con mínimo 150.000€
# Graves: hasta 300.000€; Leves: hasta 60.000€

def calcular_sanción_pbc(incumplimiento):
    if incumplimiento == "ausencia_políticas":
        return {"sanción": 150000, "prob": 0.25, "RAG": "Rojo"}
    elif incumplimiento == "falta_diligencia_PEP":
        return {"sanción": 300000, "prob": 0.35, "RAG": "Rojo"}
    elif incumplimiento == "no_auditoría_trienal":
        return {"sanción": 100000, "prob": 0.30, "RAG": "Ámbar"}
    else:
        return {"sanción": 60000, "prob": 0.20, "RAG": "Ámbar"}
```

**Output:**
- Informe de cumplimiento PBC/FT
- Gaps vs. Ley 10/2010 y RD 304/2014
- Indemnidad específica por sanciones SEPBLAC
- CP (si sujeto obligado crítico): Subsanación de incumplimientos graves

### 4.8 Compliance Penal (art. 31 bis CP)

**Objetivos:**
- Verificar existencia y eficacia del Modelo de Prevención de Delitos
- Evaluar riesgo de responsabilidad penal de la persona jurídica

**Checklist Operativo:**

```markdown
☐ Modelo de prevención de delitos (art. 31 bis CP):
  ☐ ¿Existe modelo aprobado por órgano de administración?
  ☐ Componentes del modelo:
    1. Gobierno: Órgano autónomo de control (si >50 empleados) o funciones de supervisión
    2. Risk Assessment: Mapa de riesgos penales (cohecho, blanqueo, estafa, insolvencia punible, delitos SS, medioambientales, etc.)
    3. Controles: Protocolos y procedimientos de mitigación
    4. Canal de denuncias: Whistleblowing interno (obligatorio desde Ley 2/2023)
    5. Formación: Programa de capacitación continua
    6. Investigación: Procedimiento interno de investigación de alertas
    7. Mejora continua: Revisiones periódicas del modelo
☐ Certificación UNE 19601:2025:
  ☐ ¿Está certificado el sistema de gestión de compliance penal?
  ☐ Si sí: Auditorías de seguimiento al día
  ☐ Si no: Plan de certificación o auditoría interna
☐ Órgano de control:
  ☐ Composición (independencia, recursos, expertise)
  ☐ Actas de reuniones y actividades
  ☐ Informes anuales al órgano de administración
☐ Canal de denuncias (Ley 2/2023):
  ☐ Sistema interno de información (canal confidencial)
  ☐ Gestor del canal (interno o externo)
  ☐ Protección del informante (no represalias)
  ☐ Procedimiento de gestión de alertas
  ☐ Registro de comunicaciones
☐ Procedimientos penales:
  ☐ Investigaciones o procesos penales abiertos contra la sociedad
  ☐ Delitos imputados a administradores/directivos/empleados en beneficio de la empresa
  ☐ Sentencias condenatorias previas
```

**Marco Normativo:**
- **CP art. 31 bis**: Responsabilidad penal de la persona jurídica
- **UNE 19601:2025**: Sistemas de gestión de compliance penal
- **Ley 2/2023**: Protección de informantes (whistleblowing)

**Análisis:**

```python
def evaluar_riesgo_penal(empresa):
    """
    Evalúa el riesgo de responsabilidad penal corporativa
    """
    score = 0
    
    # Factor 1: Existencia de modelo
    if not empresa.tiene_modelo_prevención:
        score += 5  # CRÍTICO
    elif not empresa.modelo_es_eficaz:  # Modelo "de papel"
        score += 3
    
    # Factor 2: Sector de alto riesgo penal
    if empresa.sector in ["construcción", "sanidad", "residuos", "contratación pública"]:
        score += 2
    
    # Factor 3: Investigaciones activas
    if empresa.procedimientos_penales_abiertos > 0:
        score += 4  # CRÍTICO
    
    # Factor 4: Canal denuncias conforme Ley 2/2023
    if not empresa.tiene_canal_denuncias:
        score += 2
    
    # Clasificación
    if score >= 7:
        return {
            "RAG": "Rojo",
            "acción": "CP: Implementación modelo prevención + auditoría externa",
            "exposición": "Sanciones: Multa (x3 beneficio ilícito) + prohibición contratar con AAPP + disolución judicial"
        }
    elif score >= 4:
        return {
            "RAG": "Ámbar",
            "acción": "R&W + Plan de refuerzo del modelo",
            "exposición": "Sanciones potenciales moderadas"
        }
    else:
        return {
            "RAG": "Verde",
            "acción": "R&W estándar",
            "exposición": "Baja"
        }
```

**Output:**
- Evaluación de la eficacia del modelo de compliance penal
- Gaps vs. UNE 19601:2025
- Riesgo de responsabilidad penal corporativa
- CP (si ausencia modelo en sectores críticos): Implementación previa a closing
- Indemnidad: Sanciones penales derivadas de hechos previos conocidos

---

## Modelo B: Due Diligence Fiscal

### Overview

El modelo fiscal evalúa el cumplimiento tributario del target en:
- **Impuestos directos:** IS (CIT), IRPF (retenciones)
- **Impuestos indirectos:** IVA, IGIC (Canarias), IPSI (Ceuta/Melilla)
- **Locales:** IAE, IBI, IVTM, ICIO
- **Especiales:** IIEE (si fabricación/distribución alcohol, tabaco, hidrocarburos)
- **Aduanas:** Aranceles, IVA importación (si comercio internacional)

### 4.1 Impuesto sobre Sociedades (IS)

**Objetivos:**
- Verificar conciliación contable-fiscal
- Validar BINs (Bases Imponibles Negativas) disponibles
- Evaluar deducciones aplicadas (I+D+i, reinversión, etc.)
- Detectar ajustes extracontables no documentados

**Checklist Operativo:**

```markdown
☐ Declaraciones IS últimos 4 años:
  ☐ Modelos 200 (anual) y 220 (consolidación fiscal, si aplica)
  ☐ Pagos fraccionados (Modelo 202) vs. resultado final
☐ Conciliación resultado contable ↔ base imponible:
  ☐ Ajustes extracontables (aumentos y disminuciones)
  ☐ Gastos no deducibles (multas, liberalidades, exceso retribuciones, etc.)
  ☐ Ingresos no contabilizados o exentos
  ☐ Amortizaciones: Tablas vs. contables; aceleradas
  ☐ Provisiones: Deducibilidad limitada (insolvencias con 6 meses, específicas)
☐ Bases Imponibles Negativas (BINs):
  ☐ Importe acumulado disponible
  ☐ Origen (años) y límites de compensación:
    ✓ Regla general: Sin límite temporal desde 2016
    ✓ Límite cuantitativo: 70% BI (si BI >1M€); 50% BI si cifra negocios >20M€ (2016-2023)
  ☐ Pérdida de BINs por cambio >50% capital en 3 años (art. 26.3 LIS) → CRÍTICO EN M&A
☐ Exención art. 21 LIS (participaciones):
  ☐ Dividendos y rentas de fuente extranjera: Requisitos (>5%, 1 año tenencia, tributación ≥10%)
  ☐ Plusvalías venta participaciones: Mismos requisitos
  ☐ Evidencia de cumplimiento de requisitos
☐ Deducciones aplicadas:
  ☐ I+D+i (art. 35 LIS): Informes motivados, certificaciones MINECO
  ☐ Reinversión de beneficios extraordinarios (derogada 2015, solo antiguos)
  ☐ Creación de empleo, producción cinematográfica, etc. (si aplica)
  ☐ Documentación de soporte suficiente (proyectos, presupuestos, gastos elegibles)
☐ Régimen de reestructuraciones (Capítulo VII LIS):
  ☐ Fusiones, escisiones, aportaciones no dinerarias: Neutralidad fiscal aplicada
  ☐ Informes de experto, proyectos, acuerdos
  ☐ Verificar traslado de BINs en reestructuraciones previas
☐ Precios de Transferencia (TP):
  ☐ Operaciones vinculadas (art. 18 LIS):
    ✓ Grupos de sociedades (>25% participación directa/indirecta)
    ✓ Administradores, socios significativos, familiares
  ☐ Documentación obligatoria (Reglamento IS, RD 634/2015):
    ✓ Country-by-Country Report (si >750M€ consolidado)
    ✓ Master File (si >45M€ facturación)
    ✓ Local File (si operaciones vinculadas >250k€)
  ☐ Metodologías aplicadas: CUP, Coste plus, Precio reventa, TNMM, Profit split
  ☐ Valoraciones de mercado (arm's length) justificadas
☐ Fondos de comercio financiero:
  ☐ Si adquisición previa de participaciones: Amortización 5% anual (deducible si requisitos)
  ☐ Documentación: Informe experto independiente sobre valor razonable activos/pasivos
☐ Operaciones con paraísos fiscales:
  ☐ Jurisdicciones lista negra (RD 1080/1991 y actualizaciones)
  ☐ Presunciones de transparencia fiscal internacional (TFI)
```

**Marco Normativo:**
- **LIS 27/2014**: Ley del Impuesto sobre Sociedades
- **RD 634/2015**: Reglamento del IS (incluye TP)

**Cuantificación:**

```python
def calcular_contingencia_IS(hallazgo):
    """
    Estima contingencia fiscal en IS
    """
    if hallazgo["tipo"] == "deducción_I+D_sin_informe":
        deducción_aplicada = hallazgo["importe_deducción"]
        cuota_recuperar = deducción_aplicada  # 100% si rechazada
        intereses_demora = cuota_recuperar * 0.0375 * hallazgo["años_transcurridos"]  # ~3.75% anual
        sanción = cuota_recuperar * 0.50  # 50% si no ocultación
        total = cuota_recuperar + intereses_demora + sanción
        prob = 0.40  # Depende de documentación
        return {"total": total, "EV": prob * total}
    
    elif hallazgo["tipo"] == "BINs_en_riesgo_por_cambio_50%":
        BINs_acumuladas = hallazgo["BINs"]
        ahorro_fiscal_potencial = BINs_acumuladas * 0.25  # Tipo IS estándar
        prob = 1.0 if hallazgo["cambio_accionarial"] else 0.0  # Binario
        return {"total": ahorro_fiscal_potencial, "EV": prob * ahorro_fiscal_potencial, "RAG": "Rojo"}
    
    # ... otros casos
```

### 4.2 IVA

**Objetivos:**
- Validar deducibilidad de IVA soportado
- Verificar correcta aplicación de tipos y exenciones
- Detectar errores en prorrata, inversión del sujeto pasivo, entregas intracomunitarias

**Checklist Operativo:**

```markdown
☐ Declaraciones IVA últimos 4 años:
  ☐ Modelos 303 (trimestral/mensual) y 390 (resumen anual)
  ☐ Modelo 349 (operaciones intracomunitarias)
☐ IVA soportado deducible:
  ☐ Facturas recibidas: Requisitos formales (RD 1619/2012)
  ☐ Bienes y servicios afectos a actividad empresarial
  ☐ Exclusiones: Vehículos turismo (salvo afectación exclusiva), gastos de representación, joyas
☐ Prorrata de deducción:
  ☐ Si actividad mixta (operaciones con y sin derecho a deducción):
    ✓ Prorrata general: % operaciones con derecho deducción
    ✓ Prorrata especial: Afectación directa (si autorizada AEAT)
  ☐ Cálculo correcto en ejercicios revisados
  ☐ Regularizaciones de bienes de inversión (si prorrata varía >10 pp en 5/10 años)
☐ Tipos impositivos aplicados:
  ☐ General 21%, Reducido 10%, Superreducido 4%
  ☐ Productos específicos: Libros (4%), alimentación (4%/10%), vivienda (10%), etc.
  ☐ Errores de tipificación → Ajuste de cuotas
☐ Exenciones:
  ☐ Exenciones limitadas (sin derecho deducción): Sanidad, educación, financieros/seguros, alquileres vivienda
  ☐ Exenciones plenas (con derecho deducción): Exportaciones, entregas intracomunitarias
  ☐ Documentación: Justificantes de exportación (DUA, CMR), NIF-IVA intracomunitario
☐ Inversión del sujeto pasivo (ISP):
  ☐ Operaciones construcción/inmobiliarias (art. 84 LIVA)
  ☐ Servicios de agencias de viaje
  ☐ Oro de inversión, residuos, etc.
  ☐ Correcta aplicación (receptor ingresa IVA)
☐ Operaciones intracomunitarias:
  ☐ Adquisiciones intracomunitarias (AIC): IVA devengado + soportado deducible
  ☐ Entregas intracomunitarias (EIC): Exentas si NIF-IVA válido y transporte intra-UE
  ☐ Modelo 349: Declaraciones recapitulativas correctas
  ☐ Quick fixes (desde 2020): Prueba de transporte, call-off stock
☐ Régimen OSS/IOSS (si e-commerce):
  ☐ One Stop Shop (OSS): Ventas B2C intra-UE
  ☐ Import One Stop Shop (IOSS): Importaciones <150€
  ☐ Declaraciones y pagos centralizados
☐ Facturación:
  ☐ Requisitos formales (RD 1619/2012 y RIVA):
    ✓ NIF emisor y receptor
    ✓ Numeración correlativa
    ✓ Descripción operación
    ✓ Base imponible, tipo, cuota
    ✓ Fecha expedición y devengo (si distinto)
  ☐ Factura electrónica: Formato estructurado (Facturae, UBL, etc.)
  ☐ Veri*factu (AEAT): Requisitos técnicos sistemas facturación
  ☐ Conservación: 4 años desde devengo
☐ Inspecciones y ajustes:
  ☐ Actas de inspección previas
  ☐ Autoliquidaciones complementarias
  ☐ Recursos en curso
```

**Marco Normativo:**
- **LIVA 37/1992**: Ley del IVA
- **RD 1624/1992** (RIVA): Reglamento del IVA
- **RD 1619/2012**: Reglamento de facturación

**Cuantificación:**

```python
def calcular_contingencia_IVA(hallazgo):
    """
    Estima contingencia en IVA
    """
    if hallazgo["tipo"] == "prorrata_mal_calculada":
        IVA_soportado_total = hallazgo["IVA_soportado"]
        prorrata_aplicada = hallazgo["prorrata_declarada"]
        prorrata_correcta = hallazgo["prorrata_real"]
        diferencia_prorrata = prorrata_aplicada - prorrata_correcta
        
        if diferencia_prorrata > 0:  # Dedujeron de más
            cuota_a_devolver = IVA_soportado_total * (diferencia_prorrata / 100)
            intereses = cuota_a_devolver * 0.0375 * hallazgo["años"]
            sanción = cuota_a_devolver * 0.50
            total = cuota_a_devolver + intereses + sanción
            prob = 0.45
            return {"total": total, "EV": prob * total, "RAG": "Ámbar"}
    
    elif hallazgo["tipo"] == "EIC_sin_justificante_transporte":
        cuota_IVA_exenta = hallazgo["base_imponible"] * 0.21
        # Si AEAT considera que no es EIC → IVA devengado no ingresado
        intereses = cuota_IVA_exenta * 0.0375 * hallazgo["años"]
        sanción = cuota_IVA_exenta * 1.0  # 100% si ocultación
        total = cuota_IVA_exenta + intereses + sanción
        prob = 0.30  # Depende de existencia parcial de docs
        return {"total": total, "EV": prob * total, "RAG": "Rojo"}
```

### 4.3 Retenciones e Ingresos a Cuenta

**Objetivos:**
- Verificar correcta aplicación de retenciones IRPF/IS
- Validar retenciones sobre rendimientos de no residentes

**Checklist Operativo:**

```markdown
☐ Declaraciones retenciones últimos 4 años:
  ☐ Modelos 111 (rendimientos trabajo) + 190 (resumen anual)
  ☐ Modelos 115 (arrendamientos) + 180
  ☐ Modelos 123 (capital mobiliario) + 193
  ☐ Modelos 216 (no residentes) + 296
☐ Retenciones sobre rendimientos del trabajo:
  ☐ Tipos aplicados: Tablas IRPF (progresivo según tramos)
  ☐ Retenciones sobre contratos de alta dirección, administradores
  ☐ Retenciones sobre opciones de compra (stock options)
☐ Retenciones sobre arrendamientos:
  ☐ 19% sobre rentas de inmuebles (locales, oficinas)
  ☐ Excepciones: Arrendamientos vivienda habitual (exentos si propietario persona física no profesional)
☐ Retenciones sobre servicios profesionales:
  ☐ 15% general (7% primeros 3 años actividad)
  ☐ Obligación: Pagador persona jurídica o empresario/profesional
☐ No residentes:
  ☐ Retención 19% general (o 24% si paraíso fiscal)
  ☐ Convenios de Doble Imposición (CDI):
    ✓ Certificado de residencia fiscal del no residente
    ✓ Tipo reducido según CDI (ej: dividendos 10-15%, intereses 0-10%, royalties 0-10%)
  ☐ Modelo 296: Declaración resumen anual
☐ Inspecciones:
  ☐ Actas de inspección sobre retenciones
  ☐ Sanciones por no retener o no ingresar
```

**Marco Normativo:**
- **IRPF 35/2006**: Ley del IRPF
- **RD 439/2007**: Reglamento del IRPF (retenciones)

### 4.4 Tributos Locales

**Checklist Operativo:**

```markdown
☐ IAE (Impuesto sobre Actividades Económicas):
  ☐ Exención: Personas físicas, sociedades <1M€ cifra negocios (primeros 2 años todas)
  ☐ Si sujeto: Epígrafes correctos, cuotas municipales
☐ IBI (Impuesto sobre Bienes Inmuebles):
  ☐ Inmuebles en propiedad: Recibos pagados al día
  ☐ Contrastar con inventario de activos inmobiliarios
☐ IVTM (Impuesto sobre Vehículos de Tracción Mecánica):
  ☐ Vehículos de empresa: Recibos pagados
☐ ICIO (Impuesto sobre Construcciones, Instalaciones y Obras):
  ☐ Si obras realizadas últimos 4 años: Liquidaciones
  ☐ Coste real de obra vs. declarado
☐ Tasas municipales y autonómicas:
  ☐ Licencias urbanísticas, ambientales
  ☐ Tasas por prestación de servicios públicos (residuos, etc.)
```

### 4.5 Sistemas y Facturación

**Objetivos:**
- Evaluar cumplimiento técnico de sistemas de facturación
- Validar preparación para factura electrónica B2B obligatoria
- Verificar Veri*factu (AEAT)

**Checklist Operativo:**

```markdown
☐ Sistemas de facturación actuales:
  ☐ Software utilizado (ERP, TPV, SaaS)
  ☐ Trazabilidad: Desde pedido → albaran → factura → cobro → contabilización
  ☐ Controles internos: Segregación de funciones, aprobaciones
☐ Veri*factu (AEAT):
  ☐ Requisitos técnicos del sistema:
    ✓ Registro de eventos (alta, modificación, anulación)
    ✓ Firma electrónica o código QR
    ✓ Remisión de registros a AEAT (o conservación local >4 años)
  ☐ Certificación del software (si aplicable)
  ☐ Logs de facturación conservados
☐ Factura electrónica B2B (Ley 18/2022 "Crea y Crece"):
  ☐ Obligatoriedad: Empresas y autónomos en relaciones B2B (desarrollo reglamentario pendiente a 2025)
  ☐ Formato estructurado: Facturae 3.2+ o UBL/CII
  ☐ Plataformas: AEAT (o plataformas certificadas privadas)
  ☐ Estado de preparación del target:
    ✓ Software compatible (actualización prevista)
    ✓ Procesos de emisión/recepción electrónica
    ✓ Integración con contabilidad
  ☐ Timing: Entrada en vigor gradual (grandes empresas primero, luego PYMES)
☐ Archivo y conservación:
  ☐ Facturas en formato electrónico o papel
  ☐ Legibilidad y accesibilidad (4 años desde devengo)
  ☐ Backup y recuperación
```

**Marco Normativo:**
- **Ley 18/2022** ("Crea y Crece"): Factura electrónica obligatoria B2B
- **AEAT** - Veri*factu: Especificaciones técnicas
- **MINECO**: Desarrollo reglamentario factura electrónica (pendiente)

**Análisis de Gap y CAPEX:**

```python
def evaluar_preparación_factura_electronica(target):
    """
    Evalúa el estado de preparación para factura electrónica B2B
    """
    gaps = []
    CAPEX_estimado = 0
    
    if not target.software_compatible:
        gaps.append("Software actual no soporta Facturae/UBL")
        CAPEX_estimado += 20000  # Actualización ERP o nuevo módulo
    
    if not target.procesos_emisión_electrónica:
        gaps.append("Procesos manuales de facturación")
        CAPEX_estimado += 10000  # Rediseño procesos + formación
    
    if not target.integración_contabilidad_automática:
        gaps.append("Contabilización manual de facturas recibidas")
        CAPEX_estimado += 15000  # Integración contable
    
    if len(gaps) == 0:
        RAG = "Verde"
        acción = "Listo para factura electrónica"
    elif CAPEX_estimado < 30000:
        RAG = "Ámbar"
        acción = "CP: Plan de adaptación pre-entrada en vigor"
    else:
        RAG = "Rojo"
        acción = "CP: Implementación completa + buffer CAPEX"
    
    return {
        "gaps": gaps,
        "CAPEX": CAPEX_estimado,
        "RAG": RAG,
        "acción": acción
    }
```

**Output:**
- Análisis de cumplimiento Veri*factu
- Evaluación de preparación factura electrónica B2B con CAPEX estimado
- CP (si crítico): Certificación de software y procesos antes de entrada en vigor normativa
- Ajuste precio: CAPEX necesario si significativo

### 4.6 Inspecciones y Procedimientos

**Checklist Operativo:**

```markdown
☐ Historial de inspecciones (últimos 10 años):
  ☐ AEAT: Impuestos revisados, periodos, resultado
  ☐ TGSS: Cotizaciones, bonificaciones
  ☐ Autonómicas: Impuestos cedidos (ej: ITP, Sucesiones)
☐ Actas de inspección:
  ☐ Tipo: Conformidad, disconformidad, previas
  ☐ Conceptos: Ajustes en bases imponibles, deducciones rechazadas, etc.
  ☐ Cuotas liquidadas, intereses, sanciones
  ☐ Estado: Firmes, recurridas (TEAR, AN, TS)
☐ Recursos en curso:
  ☐ Reclamaciones económico-administrativas (TEAR, TEAC)
  ☐ Contencioso-administrativo (Audiencia Nacional, TSJ, TS)
  ☐ Provisiones contables vs. contingencias reales
☐ Planes de inspección AEAT:
  ☐ Riesgo de inspección futura: Sectores prioritarios, alerts de control (anomalías en declaraciones)
  ☐ Comprobaciones limitadas (parciales) vs. inspecciones generales
☐ Sanciones:
  ☐ Graduación (RD 2063/2004): Criterios de reducción (conformidad, pronto pago)
  ☐ Infracciones leves (50%), graves (50-100%), muy graves (100-150%)
  ☐ Ocultación: Agravante (sanciones hasta 150%)
```

**Marco Normativo:**
- **LGT 58/2003**: Ley General Tributaria (procedimientos inspección, recursos, sanciones)
- **RD 1065/2007** (RGGI): Reglamento de gestión e inspección tributaria
- **RD 2063/2004**: Reglamento de régimen sancionador

**Cuantificación de Contingencias Fiscales:**

```python
def consolidar_contingencias_fiscales(hallazgos_fiscales):
    """
    Consolida todas las contingencias fiscales identificadas
    """
    contingencias = {
        "IS": [],
        "IVA": [],
        "Retenciones": [],
        "Locales": [],
        "Veri*factu": []
    }
    
    EV_total = 0
    
    for hallazgo in hallazgos_fiscales:
        cuota = hallazgo["cuota_principal"]
        intereses = cuota * 0.0375 * hallazgo["años_transcurridos"]
        sanción = cuota * hallazgo["coeficiente_sanción"]  # 0.50–1.50
        
        total_hallazgo = cuota + intereses + sanción
        EV_hallazgo = hallazgo["probabilidad"] * total_hallazgo
        
        contingencias[hallazgo["impuesto"]].append({
            "ID": hallazgo["ID"],
            "descripción": hallazgo["descripción"],
            "cuota": cuota,
            "intereses": intereses,
            "sanción": sanción,
            "total": total_hallazgo,
            "probabilidad": hallazgo["probabilidad"],
            "EV": EV_hallazgo,
            "RAG": hallazgo["RAG"]
        })
        
        EV_total += EV_hallazgo
    
    # Reserva fiscal recomendada
    factor_prudencia = 1.3  # 30% buffer
    reserva_fiscal = EV_total * factor_prudencia
    
    return {
        "contingencias_por_impuesto": contingencias,
        "EV_total": EV_total,
        "reserva_recomendada": reserva_fiscal
    }
```

---

## Modelo C: Due Diligence Técnica Medioambiental

### Overview

Evalúa el cumplimiento de normativa ambiental y cuantifica pasivos/contingencias relacionados con:
- **Emisiones industriales** (IED/IPPC)
- **Residuos**
- **Vertidos** (aguas)
- **Suelos contaminados**
- **Responsabilidad medioambiental** (Ley 26/2007)

### 4.1 Licencias y Autorizaciones Ambientales

**Objetivos:**
- Verificar vigencia y cumplimiento de autorizaciones
- Detectar actividades sin cobertura legal
- Evaluar riesgo de no renovación

**Checklist Operativo:**

```markdown
☐ Autorización Ambiental Integrada (AAI) - Ley 16/2002 + RD 815/2013:
  ☐ Aplicable si: Actividad del Anexo I (industrias energéticas, producción/transformación metales, minería, química, gestión residuos, ganadería intensiva, etc.)
  ☐ Resolución de AAI vigente
  ☐ Condicionantes de la AAI:
    ✓ Emisiones atmósfera: Valores Límite de Emisión (VLE) por foco
    ✓ Vertidos: Límites y periodicidad analíticas
    ✓ Residuos: Gestión, almacenamiento
    ✓ Ruido: Límites diurnos/nocturnos
    ✓ Mejores Técnicas Disponibles (MTD/BAT): Cumplimiento de conclusiones MTD (BREF)
  ☐ Renovación: Periódica (cada 8 años) o por modificación sustancial
☐ Autorización Ambiental Única (AAU) o APCA (autonómicas):
  ☐ Si no aplica AAI pero sí impacto ambiental significativo
  ☐ Condiciones específicas de cada CCAA
☐ Autorizaciones de vertido:
  ☐ Dominio público hidráulico (ríos, lagos): Confederación Hidrográfica
  ☐ Dominio público marítimo-terrestre (costa): Demarcación de Costas
  ☐ Red de saneamiento municipal: Ayuntamiento
  ☐ Parámetros límite: DQO, DBO5, SST, metales pesados, etc.
☐ Focos de emisión atmosférica:
  ☐ Inventario de focos (calderas, hornos, procesos)
  ☐ Autorizaciones específicas si superan umbrales
  ☐ Control continuo (SCIC) si AAI lo exige
☐ Productor/Gestor de residuos:
  ☐ Inscripción en registro de producción/gestión (autonómico)
  ☐ Tipos de residuos: Peligrosos (LER con *), No peligrosos
  ☐ Almacenamiento: Requisitos de cubetos, etiquetado, señalización, tiempos máximos
  ☐ Contratos con gestores autorizados (códigos LER, destino R/D)
☐ Almacenamiento de productos químicos:
  ☐ ITC MIE-APQ (RD 656/2017): Si >1.000 kg/L de productos químicos
  ☐ Cubetos de retención: 100% capacidad del mayor recipiente + 10% de la suma del resto (mínimo 100% mayor)
  ☐ Señalización CLP (Reglamento 1272/2008)
☐ Seveso (RD 840/2015):
  ☐ Si cantidades umbral de sustancias peligrosas (anexos I y II)
  ☐ Nivel inferior o superior
  ☐ Política de Prevención de Accidentes Graves (PPAG), Plan de Emergencia Exterior (PEE)
☐ Ruido:
  ☐ Límites municipales (ordenanzas)
  ☐ Mediciones acústicas periódicas
☐ Licencias municipales:
  ☐ Licencia de actividad
  ☐ Licencia de obras (si modificaciones)
```

**Marco Normativo:**
- **Ley 16/2002** + **RD 815/2013** (RIE): Emisiones industriales (transposición Directiva IED 2010/75/UE)
- **Directiva 2010/75/UE** (IED): Industrial Emissions Directive
- **Ley 7/2022**: Residuos y suelos contaminados
- **RD 656/2017**: Almacenamiento de productos químicos (ITC MIE-APQ)

**Output:**
- Inventario de licencias con vigencia y condicionantes
- Gap analysis: Autorizaciones faltantes o caducadas
- CP crítica: Regularización de licencias antes de closing
- RAG: Rojo si opera sin AAI/AAU obligatoria

### 4.2 Cumplimiento Operativo

**Objetivos:**
- Verificar cumplimiento de condiciones de las autorizaciones
- Detectar excesos de VLE (valores límite emisión)
- Validar gestión de residuos conforme

**Checklist Operativo:**

```markdown
☐ Emisiones atmosféricas:
  ☐ Autocontroles periódicos (analíticas de chimeneas)
  ☐ Comparativa con VLE de la AAI
  ☐ Excesos registrados y notificados a autoridad competente
  ☐ Medidas correctivas adoptadas
☐ Vertidos:
  ☐ Analíticas de vertidos (frecuencia según autorización)
  ☐ Parámetros: DQO, DBO5, SST, pH, temperatura, metales, etc.
  ☐ Excesos de límites → Notificación, causas, corrección
  ☐ Sistema de depuración propio (EDAR): Estado, mantenimiento
☐ Residuos:
  ☐ Registro de producción (cronológico, por tipo LER)
  ☐ Contratos con gestores autorizados:
    ✓ Código LER
    ✓ Gestor: NIMA (Número de Identificación Medioambiental), autorización vigente
    ✓ Operaciones: R (valorización) o D (eliminación)
  ☐ Documento de Identificación (DI) o e-DI:
    ✓ Trazabilidad: Productor → Transportista → Gestor
    ✓ Archivo conservado (5 años)
  ☐ Declaración anual de residuos (autonómica)
  ☐ Memoria anual de gestión (si gran productor)
☐ Almacenamiento de residuos y productos químicos:
  ☐ Zonas de almacenamiento:
    ✓ Cubetos de retención (verificar capacidad)
    ✓ Pavimento impermeable
    ✓ Señalización y etiquetado (CLP, pictogramas)
    ✓ Separación de incompatibles (ácidos vs. bases, oxidantes vs. reductores)
  ☐ Plazos de almacenamiento:
    ✓ Peligrosos: Máximo 6 meses (salvo autorización)
    ✓ No peligrosos: Máximo 2 años
☐ Subcontratas y transporte:
  ☐ Transportistas de residuos peligrosos: Autorización (ADR si aplica)
  ☐ Gestores: Verificar en registros oficiales (autonómicos, RGR)
☐ PRTR (Registro de Emisiones y Transferencias de Contaminantes):
  ☐ Si actividad del Anexo I (Ley 16/2002) y superación de umbrales
  ☐ Declaración anual a PRTR-España (MITECO)
  ☐ Datos: Emisiones aire, agua, suelo; transferencias de residuos
```

**Marco Normativo:**
- **Ley 7/2022**: Residuos y suelos
- **RD 553/2020**: Traslado de residuos
- **Reglamento 1272/2008** (CLP): Clasificación, etiquetado y envasado de productos químicos

**Cuantificación de Incumplimientos:**

```python
def calcular_sanción_ambiental(incumplimiento):
    """
    Estima sanciones ambientales por incumplimientos
    """
    # Sanciones ambientales (Ley 16/2002, Ley 7/2022):
    # Leves: hasta 20.000€ (autonómicas pueden variar)
    # Graves: 20.001€ – 200.000€
    # Muy graves: 200.001€ – 2.000.000€ (o más según normativa específica)
    
    if incumplimiento["tipo"] == "exceso_VLE_puntual":
        sanción = 50000  # Grave
        prob = 0.35 if incumplimiento["notificado"] else 0.50
        return {"sanción": sanción, "EV": prob * sanción, "RAG": "Ámbar"}
    
    elif incumplimiento["tipo"] == "exceso_VLE_reiterado":
        sanción = 300000  # Muy grave
        prob = 0.60
        return {"sanción": sanción, "EV": prob * sanción, "RAG": "Rojo"}
    
    elif incumplimiento["tipo"] == "gestión_residuos_peligrosos_sin_contrato":
        sanción = 150000  # Muy grave
        prob = 0.45
        return {"sanción": sanción, "EV": prob * sanción, "RAG": "Rojo"}
    
    elif incumplimiento["tipo"] == "almacenamiento_sin_cubeto":
        sanción = 30000  # Grave
        prob = 0.40
        return {"sanción": sanción, "EV": prob * sanción, "RAG": "Ámbar"}
    
    else:
        sanción = 10000
        prob = 0.25
        return {"sanción": sanción, "EV": prob * sanción, "RAG": "Verde"}
```

### 4.3 Suelos y Aguas Subterráneas

**Objetivos:**
- Identificar suelos potencialmente contaminados
- Cuantificar pasivos de remediación
- Evaluar responsabilidad histórica

**Checklist Operativo:**

```markdown
☐ Inventario de suelos:
  ☐ Histórico de usos del emplazamiento (industrial, agrícola, etc.)
  ☐ Actividades potencialmente contaminantes (Anexo I RD 9/2005):
    ✓ Fabricación productos químicos
    ✓ Tratamiento de metales
    ✓ Almacenamiento hidrocarburos
    ✓ Refinerías, coquerías
    ✓ Gestión de residuos
    ✓ ...
☐ Declaración de suelos:
  ☐ Si actividad potencialmente contaminante del suelo (APCS) → Declaración a CCAA
  ☐ Informe preliminar de situación de suelos (si cambio de titularidad o cese)
☐ Investigaciones de suelos realizadas:
  ☐ Campañas de muestreo:
    ✓ Puntos de investigación (sondeos, calicatas, piezómetros)
    ✓ Parámetros analizados (metales pesados, hidrocarburos, BTEX, PAH, PCB, pesticidas, etc.)
    ✓ Laboratorios acreditados (ISO/EN)
  ☐ Resultados:
    ✓ Comparativa con Niveles de Referencia (NR) o Niveles Genéricos de Referencia (NGR)
    ✓ Niveles de Concentración Admisibles (NCA) autonómicos
  ☐ Si superación de NCA:
    ✓ Evaluación de riesgos (específica del emplazamiento)
    ✓ Modelo conceptual: Focos, vías, receptores
    ✓ Riesgo inaceptable → Obligación de remediación
☐ Plan de remediación (si aplica):
  ☐ Tecnología seleccionada:
    ✓ Excavación y disposición externa (más costoso, más rápido)
    ✓ Tratamiento in-situ (bioventing, SVE, inyección reactivos)
    ✓ Tratamiento ex-situ (landfarming, biopile)
    ✓ Contención (barreras físicas, monitoreo)
  ☐ Presupuesto de remediación (CAPEX)
  ☐ Plazos de ejecución
  ☐ Validación post-remediación (analíticas finales)
☐ Aguas subterráneas:
  ☐ Piezómetros instalados
  ☐ Analíticas periódicas
  ☐ Contaminación detectada (pluma de contaminación)
  ☐ Bombeo y tratamiento (pump & treat) si necesario
```

**Marco Normativo:**
- **Ley 7/2022**: Residuos y suelos contaminados
- **RD 9/2005**: Relación de actividades potencialmente contaminantes del suelo

**Cuantificación de Remediación:**

```python
def estimar_coste_remediación_suelos(investigación):
    """
    Estima el coste de remediación de suelos contaminados
    """
    volumen_contaminado = investigación["volumen_m3"]  # m³
    contaminante_principal = investigación["contaminante"]  # ej: "hidrocarburos", "metales_pesados"
    tecnología_recomendada = seleccionar_tecnología(contaminante_principal)
    
    # Costes unitarios orientativos (€/m³ o €/tonelada)
    costes_unitarios = {
        "excavación_disposición": 150,  # €/m³ (incluye excavación + transporte + vertedero)
        "bioventing": 50,  # €/m³
        "SVE": 60,  # €/m³
        "landfarming": 80,  # €/tonelada
        "pump_treat_aguas": 200000  # €/año (OPEX)
    }
    
    if tecnología_recomendada in ["excavación_disposición", "bioventing", "SVE"]:
        CAPEX_remediación = volumen_contaminado * costes_unitarios[tecnología_recomendada]
        OPEX_anual = CAPEX_remediación * 0.05  # 5% mantenimiento/monitoreo
        plazo_años = 1 if tecnología_recomendada == "excavación_disposición" else 3
    
    elif tecnología_recomendada == "pump_treat_aguas":
        CAPEX_remediación = 300000  # Instalación sistema
        OPEX_anual = costes_unitarios["pump_treat_aguas"]
        plazo_años = 5  # Duración típica
    
    else:
        CAPEX_remediación = volumen_contaminado * 100
        OPEX_anual = 0
        plazo_años = 2
    
    coste_total = CAPEX_remediación + (OPEX_anual * plazo_años)
    
    # Probabilidad de remediación obligatoria
    if investigación["superación_NCA"]:
        prob = 0.80 if investigación["riesgo_inaceptable_confirmado"] else 0.50
    else:
        prob = 0.10  # Remediación voluntaria
    
    EV_remediación = prob * coste_total
    
    return {
        "CAPEX": CAPEX_remediación,
        "OPEX_anual": OPEX_anual,
        "plazo_años": plazo_años,
        "coste_total": coste_total,
        "probabilidad": prob,
        "EV": EV_remediación,
        "RAG": "Rojo" if EV_remediación > 500000 else "Ámbar" if EV_remediación > 100000 else "Verde"
    }
```

### 4.4 Responsabilidad Medioambiental (Ley 26/2007)

**Objetivos:**
- Evaluar riesgos de daños ambientales significativos
- Verificar garantías financieras obligatorias
- Cuantificar contingencias de responsabilidad

**Checklist Operativo:**

```markdown
☐ Análisis de Riesgo Ambiental (ARA) - RD 2090/2008:
  ☐ Obligatorio si: Actividad del Anexo III de Ley 26/2007 (similar Anexo I IED + otras)
  ☐ Metodología oficial (Orden ARM/1783/2011):
    ✓ Identificación de escenarios accidentales (fugas, derrames, incendios, explosiones)
    ✓ Estimación de probabilidad de ocurrencia
    ✓ Cuantificación del daño ambiental (especies protegidas, hábitats, aguas, suelos)
    ✓ Índice de Daño Medioambiental (IDM)
  ☐ Resultados ARA:
    ✓ Nivel de prioridad: 1 (más alto) a 3 (más bajo)
    ✓ Obligación de garantía financiera según nivel
☐ Garantía financiera obligatoria:
  ☐ Si ARA resultado nivel 1 → Garantía obligatoria inmediata
  ☐ Si nivel 2 → Obligatoria cuando MITECO lo establezca (priorización sectorial)
  ☐ Si nivel 3 → No obligatoria (análisis voluntario)
  ☐ Instrumentos de garantía:
    ✓ Póliza de seguro
    ✓ Aval bancario
    ✓ Reserva técnica (fondo ad hoc en balance)
  ☐ Cuantía de la garantía:
    ✓ Calculada según ARA (cobertura del escenario más desfavorable)
    ✓ Revisión periódica (cada 5 años o si cambios significativos)
☐ Seguros ambientales:
  ☐ Póliza de Responsabilidad Civil Medioambiental:
    ✓ Cobertura: Daños a terceros, costes de remediación
    ✓ Límites y franquicias
    ✓ Exclusiones (ej: contaminación gradual preexistente)
  ☐ Vigencia y pagos al día
☐ Daños ambientales previos:
  ☐ Histórico de incidentes ambientales (últimos 10-20 años)
  ☐ Notificaciones a autoridades
  ☐ Medidas correctivas adoptadas
  ☐ Pasivos ambientales latentes (ej: contaminación histórica no remediada)
```

**Marco Normativo:**
- **Ley 26/2007**: Responsabilidad Medioambiental
- **RD 2090/2008**: Reglamento de desarrollo de Ley 26/2007 (incluye ARA)
- **Orden ARM/1783/2011**: Metodología oficial de Análisis de Riesgo Ambiental

**Cuantificación:**

```python
def calcular_garantía_financiera_ambiental(ARA):
    """
    Calcula la garantía financiera obligatoria según ARA
    """
    escenarios = ARA["escenarios_accidentales"]
    
    costes_remediación = []
    for escenario in escenarios:
        # Coste de reparación primaria + complementaria + compensatoria
        coste_reparación = escenario["coste_reparación_primaria"]
        coste_complementaria = escenario["coste_reparación_complementaria"]
        coste_compensatoria = escenario["coste_reparación_compensatoria"]
        
        coste_total_escenario = coste_reparación + coste_complementaria + coste_compensatoria
        costes_remediación.append(coste_total_escenario)
    
    # Garantía = Coste del escenario más desfavorable
    garantía_mínima = max(costes_remediación)
    
    # Nivel de prioridad determina obligatoriedad
    nivel_prioridad = ARA["nivel_prioridad"]  # 1, 2, 3
    
    if nivel_prioridad == 1:
        obligatoria = True
        timing = "Inmediato"
    elif nivel_prioridad == 2:
        obligatoria = "Pendiente de orden sectorial MITECO"
        timing = "Cuando se publique orden"
    else:
        obligatoria = False
        timing = "N/A"
    
    return {
        "garantía_mínima": garantía_mínima,
        "nivel_prioridad": nivel_prioridad,
        "obligatoria": obligatoria,
        "timing": timing,
        "instrumentos_válidos": ["Póliza seguro", "Aval bancario", "Reserva técnica"]
    }
```

**Output:**
- Informe ARA con nivel de prioridad
- Cuantía de garantía financiera (si obligatoria)
- CP: Constitución de garantía antes de closing (si nivel 1 y no existe)
- Provisión balance: Reserva técnica o coste de póliza anual

### 4.5 Sistema de Gestión Ambiental (ISO 14001)

**Objetivos:**
- Evaluar madurez del sistema de gestión ambiental
- Verificar certificación ISO 14001 (si aplica)

**Checklist Operativo:**

```markdown
☐ ISO 14001:2015 + Enmienda 2024 (acción climática):
  ☐ ¿Está certificado?
  ☐ Si sí:
    ✓ Certificado vigente
    ✓ Auditorías de seguimiento (anuales) y renovación (cada 3 años)
    ✓ No conformidades abiertas
  ☐ Componentes del sistema:
    1. Contexto y partes interesadas
    2. Liderazgo y política ambiental
    3. Planificación:
       - Aspectos e impactos ambientales (identificación, evaluación significancia)
       - Obligaciones de cumplimiento (requisitos legales)
       - Objetivos y programas ambientales
    4. Soporte:
       - Recursos (personal, infraestructura, financieros)
       - Competencia y formación
       - Comunicación interna y externa
       - Información documentada (procedimientos, registros)
    5. Operación:
       - Controles operacionales
       - Preparación y respuesta ante emergencias (planes de emergencia, simulacros)
    6. Evaluación del desempeño:
       - Seguimiento, medición, análisis (indicadores KPI)
       - Auditorías internas (planificadas, ejecutadas, registradas)
       - Revisión por la dirección (anual)
    7. Mejora continua:
       - No conformidades y acciones correctivas
       - Mejora continua del SGA
☐ Indicadores ambientales (KPI):
  ☐ Consumos: Energía (kWh), agua (m³), materias primas
  ☐ Emisiones: CO₂e (huella de carbono), NOx, SOx, partículas
  ☐ Residuos: Toneladas generadas (peligrosos vs. no peligrosos), % valorización
  ☐ Vertidos: Volumen (m³), carga contaminante
  ☐ Cumplimiento legal: % requisitos legales cumplidos, n incidentes/sanciones
```

**Marco Normativo:**
- **ISO 14001:2015** + **Enmienda 2024**: Sistema de gestión ambiental
- **ISO 19011:2018**: Directrices para auditoría de sistemas de gestión

**Output:**
- Evaluación de madurez del SGA (certificado, implementado parcial, inexistente)
- Gap analysis vs. ISO 14001 (si no certificado)
- R&W: Certificaciones vigentes, cumplimiento normativo ambiental
- No suele ser CP (salvo exigencia contractual cliente/inversor)

---

## Sistema de Cuantificación de Riesgos

### Metodología de Scoring

Todos los hallazgos identificados en los 3 modelos se valoran con:

```
1. Clasificación RAG (cualitativa)
   - 🔴 Rojo: Deal-breaker potencial, requiere CP obligatoria
   - 🟡 Ámbar: Mitigable con CP/R&W/indemnidad
   - 🟢 Verde: Riesgo menor, R&W estándar suficiente

2. Probabilidad (P)
   - Escala 1-5: 1=remoto, 2=bajo, 3=medio, 4=probable, 5=alto
   - O porcentaje (%): 10%, 25%, 40%, 60%, 80%

3. Impacto (I)
   - Escala 1-5 según % de EV empresa:
     * 1: <0.5% EV
     * 2: 0.5-2% EV
     * 3: 2-5% EV
     * 4: 5-10% EV
     * 5: >10% EV
   - O valor absoluto (€)

4. RPN (Risk Priority Number) = P × I
   - Rango: 1 (mínimo) - 25 (máximo)
   - Umbrales:
     * RPN ≥ 15: Rojo (prioridad alta)
     * 8 ≤ RPN < 15: Ámbar (prioridad media)
     * RPN < 8: Verde (prioridad baja)

5. EV (Expected Value) = Probabilidad(%) × Impacto(€)
   - Valor monetario esperado de la contingencia
   - Base para cálculo de reservas y ajustes de precio

6. Reserva recomendada = EV × factor_prudencia
   - Factor prudencia: 1.1-1.5 según volatilidad/incertidumbre
   - Reserva = Provisión contable + Escrow + Ajuste precio
```

### Algoritmo de Priorización

```python
def priorizar_hallazgos(lista_hallazgos):
    """
    Prioriza hallazgos según metodología RAG + RPN + EV
    """
    # Paso 1: Filtrar hallazgos Rojos (críticos)
    rojos = [h for h in lista_hallazgos if h["RAG"] == "Rojo"]
    rojos_sorted = sorted(rojos, key=lambda x: x["RPN"], reverse=True)
    
    # Paso 2: Filtrar Ámbar (mitigables)
    ámbar = [h for h in lista_hallazgos if h["RAG"] == "Ámbar"]
    ámbar_sorted = sorted(ámbar, key=lambda x: x["EV"], reverse=True)
    
    # Paso 3: Verdes (menores)
    verdes = [h for h in lista_hallazgos if h["RAG"] == "Verde"]
    
    # Paso 4: Consolidar Top hallazgos para resumen ejecutivo
    top_critical = rojos_sorted[:5]  # Top 5 rojos
    top_mitigable = ámbar_sorted[:5]  # Top 5 ámbar por EV
    
    return {
        "críticos_Rojo": rojos_sorted,
        "mitigables_Ámbar": ámbar_sorted,
        "menores_Verde": verdes,
        "Top_10_resumen_ejecutivo": top_critical + top_mitigable[:5]
    }
```

### Matriz de Riesgos Consolidada (Template)

```markdown
| ID   | Hallazgo | Modelo | Norma | RAG | P | I | Impacto(€) | RPN | EV(€) | Mitigación | CP/R&W | Ajuste Precio |
|------|----------|--------|-------|-----|---|---|------------|-----|-------|------------|--------|---------------|
| J-01 | Falta publicidad fusión | A | RDL 5/2023 | 🔴 | 40% | 5 | 2.500.000 | 20 | 1.000.000 | Subsanación + reaprobación | CP | 1.000.000 |
| F-01 | Veri*factu no implementado | B | AEAT | 🔴 | 50% | 4 | 400.000 | 20 | 200.000 | Certificación SW + logs | CP | 200.000 |
| E-01 | Exceso VLE foco 3 | C | RD 815/2013 | 🔴 | 40% | 4 | 900.000 | 16 | 360.000 | Retrofit & BAT | CP | 360.000 (CAPEX) |
| J-02 | Canal denuncias incompleto | A | Ley 2/2023 | 🟡 | 35% | 2 | 150.000 | 7 | 52.500 | Implementar + auditar | R&W | 0 |
| F-02 | Prorrata IVA incorrecta | B | LIVA | 🟡 | 35% | 3 | 300.000 | 10.5 | 105.000 | Regularización + autoliquidación | R&W | 105.000 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| **TOTAL EV** | | | | | | | | | **1.717.500** | | | **1.665.000** |
| **Reserva (factor 1.3)** | | | | | | | | | **2.232.750** | | | |
```

**Interpretación:**
- **EV Total:** 1.717.500€ = Valor esperado de todas las contingencias identificadas
- **Reserva recomendada:** 2.232.750€ = EV × 1.3 (30% buffer por incertidumbre)
- **Ajuste precio sugerido:** 1.665.000€ = Suma de contingencias Rojas + Ámbar materiales
- **CPs críticas:** 3 (J-01, F-01, E-01) → Condiciones sine qua non para closing

---

## Deliverables y Formatos

### Estructura de Entregables

**1. Resumen Ejecutivo (DOCX, 2-4 páginas)**

Contenido:
```markdown
# Resumen Ejecutivo - Due Diligence [Target]

## 1. Scope de la Revisión
- Tipo de deal: [Share deal / Asset deal]
- Perímetro: [Sociedades/activos incluidos]
- Periodo revisado: [Fechas]
- Limitaciones: [Data room incompleto, etc.]

## 2. Hallazgos Críticos (Top 5-10)
[Tabla con ID, Hallazgo, RAG, EV, Acción]

## 3. Cuantificación Agregada
- **EV Jurídico:** [€]
- **EV Fiscal:** [€]
- **EV Ambiental:** [€]
- **EV TOTAL:** [€]
- **Reserva recomendada:** [€] (factor [1.1-1.5])

## 4. Conditions Precedent Esenciales
1. [CP-01]: [Descripción]
2. [CP-02]: [Descripción]
...

## 5. R&W Reforzadas Recomendadas
- Titularidad y ausencia de cargas
- Cumplimiento RGPD/PBC/Ambiental
- Inexistencia de litigios materiales
- Licencias y autorizaciones vigentes
- ...

## 6. Ajustes de Precio / Escrows
- Ajuste precio directo: [€]
- Escrow: [€] liberado en [hito/fecha]
- Indemnidades específicas: [Listar áreas]

## 7. Conclusión y Recomendación
[Viabilidad del deal: Go / Go con condiciones / No-go]
[Justificación]
```

**2. Informes Detallados por Modelo (DOCX, 20-50 págs c/u)**

- **Informe Jurídico (Modelo A):** Detalle de cada sección 4.1-4.8 con hallazgos, evidencias, análisis legal
- **Informe Fiscal (Modelo B):** Detalle de cada impuesto, conciliaciones, cuantificaciones
- **Informe Ambiental (Modelo C):** Detalle de licencias, cumplimiento, suelos, ARAs

Estructura tipo:
```markdown
# Informe de Due Diligence [Jurídica/Fiscal/Ambiental] - [Target]

## 1. Introducción y Metodología
## 2. Alcance y Limitaciones
## 3. Marco Normativo Aplicable
## 4. Desarrollo Técnico (Checklists)
   4.1. [Área 1]
       - Descripción
       - Documentación revisada
       - Hallazgos identificados
       - Análisis de riesgos
   4.2. [Área 2]
   ...
## 5. Matriz de Riesgos [Jurídicos/Fiscales/Ambientales]
## 6. Análisis Crítico (Pros/Contras/Riesgos/Sesgos)
## 7. Conclusiones y Recomendaciones
## Anexos:
   - Anexo I: Data Request List
   - Anexo II: Log Q&A y Red Flags
   - Anexo III: Mapa R&W y CPs propuestas
   - Anexo IV: Referencias normativas detalladas
```

**3. Matriz de Riesgos Consolidada (XLSX)**

Formato Excel con pestañas:
- **Dashboard:** Resumen visual (gráficos RAG, EV por modelo, Top 10 hallazgos)
- **Matriz_Completa:** Tabla detallada de todos los hallazgos
- **Jurídico:** Hallazgos Modelo A
- **Fiscal:** Hallazgos Modelo B
- **Ambiental:** Hallazgos Modelo C
- **CPs_RW:** Mapeo de CPs y R&W recomendadas
- **Cálculos:** Fórmulas de RPN, EV, Reservas

**4. Anexos Operativos**

- **Data Request List (DRL):** Excel con categorías (Legal, Fiscal, Ambiental), documentos solicitados, status (Recibido/Pendiente/N/A), observaciones
- **Log Q&A:** Registro cronológico de preguntas planteadas, responsables, fechas, respuestas, efecto en riesgos
- **Mapa R&W y CPs:** Tabla que vincula cada riesgo → R&W específica → CP recomendada
- **Clausulado Tipo:** Extractos de cláusulas modelo para SPA:
  - Indemnidades específicas (RGPD, PBC, Ambiental, Fiscal)
  - Fórmula de ajuste de precio: `Precio_final = Precio_base - (EV_jurídica + EV_fiscal + EV_ambiental) ± NWC_adj ± Deuda_Neta`
  - Escrows: Cuantía, condiciones de liberación, plazos

### Scripts de Automatización

**Script 1: Generación de Matriz de Riesgos (Python)**

```python
# scripts/generate_risk_matrix.py
"""
Genera matriz de riesgos Excel a partir de hallazgos estructurados
"""
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font
from openpyxl.utils.dataframe import dataframe_to_rows

def generar_matriz_riesgos(hallazgos_json, output_path):
    """
    Input: JSON con hallazgos estructurados
    Output: Excel con matriz consolidada + dashboard
    """
    
    # Cargar hallazgos
    df = pd.DataFrame(hallazgos_json)
    
    # Calcular métricas
    df['RPN'] = df['Probabilidad'] * df['Impacto_escala']
    df['EV'] = (df['Probabilidad'] / 100) * df['Impacto_euros']
    
    # Clasificar RAG según RPN
    def clasificar_RAG(row):
        if row['RPN'] >= 15:
            return 'Rojo'
        elif row['RPN'] >= 8:
            return 'Ámbar'
        else:
            return 'Verde'
    
    df['RAG'] = df.apply(clasificar_RAG, axis=1)
    
    # Ordenar por RPN descendente
    df_sorted = df.sort_values('RPN', ascending=False)
    
    # Crear Excel con múltiples pestañas
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Pestaña 1: Dashboard (summary)
        summary = {
            'Modelo': ['Jurídico', 'Fiscal', 'Ambiental', 'TOTAL'],
            'N_hallazgos': [
                len(df[df['Modelo'] == 'A']),
                len(df[df['Modelo'] == 'B']),
                len(df[df['Modelo'] == 'C']),
                len(df)
            ],
            'EV_total': [
                df[df['Modelo'] == 'A']['EV'].sum(),
                df[df['Modelo'] == 'B']['EV'].sum(),
                df[df['Modelo'] == 'C']['EV'].sum(),
                df['EV'].sum()
            ]
        }
        df_summary = pd.DataFrame(summary)
        df_summary.to_excel(writer, sheet_name='Dashboard', index=False)
        
        # Pestaña 2: Matriz completa
        df_sorted.to_excel(writer, sheet_name='Matriz_Completa', index=False)
        
        # Pestaña 3-5: Por modelo
        df[df['Modelo'] == 'A'].to_excel(writer, sheet_name='Jurídico', index=False)
        df[df['Modelo'] == 'B'].to_excel(writer, sheet_name='Fiscal', index=False)
        df[df['Modelo'] == 'C'].to_excel(writer, sheet_name='Ambiental', index=False)
    
    # Aplicar formato condicional (colores RAG)
    wb = load_workbook(output_path)
    ws_matriz = wb['Matriz_Completa']
    
    # Identificar columna RAG
    rag_col = None
    for cell in ws_matriz[1]:
        if cell.value == 'RAG':
            rag_col = cell.column
            break
    
    # Aplicar colores
    red_fill = PatternFill(start_color='FFCCCB', end_color='FFCCCB', fill_type='solid')
    amber_fill = PatternFill(start_color='FFE4B5', end_color='FFE4B5', fill_type='solid')
    green_fill = PatternFill(start_color='C8E6C9', end_color='C8E6C9', fill_type='solid')
    
    for row in ws_matriz.iter_rows(min_row=2, max_row=ws_matriz.max_row):
        rag_cell = row[rag_col - 1]
        if rag_cell.value == 'Rojo':
            for cell in row:
                cell.fill = red_fill
        elif rag_cell.value == 'Ámbar':
            for cell in row:
                cell.fill = amber_fill
        elif rag_cell.value == 'Verde':
            for cell in row:
                cell.fill = green_fill
    
    wb.save(output_path)
    print(f"✅ Matriz de riesgos generada: {output_path}")

# Uso:
# hallazgos = cargar_hallazgos_desde_json('hallazgos.json')
# generar_matriz_riesgos(hallazgos, '/mnt/user-data/outputs/matriz_riesgos.xlsx')
```

**Script 2: Generación de Informes DOCX (Python-docx)**

```python
# scripts/generate_dd_report.py
"""
Genera informes de DD en formato DOCX a partir de templates
"""
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def generar_resumen_ejecutivo(hallazgos_top, parametros_deal, output_path):
    """
    Genera resumen ejecutivo de 2-4 páginas
    """
    doc = Document()
    
    # Título
    title = doc.add_heading('Resumen Ejecutivo - Due Diligence', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    # 1. Scope
    doc.add_heading('1. Scope de la Revisión', 1)
    doc.add_paragraph(f"Target: {parametros_deal['target']}")
    doc.add_paragraph(f"Tipo de deal: {parametros_deal['tipo_deal']}")
    doc.add_paragraph(f"Periodo revisado: {parametros_deal['periodo']}")
    
    # 2. Hallazgos críticos
    doc.add_heading('2. Hallazgos Críticos (Top 10)', 1)
    table = doc.add_table(rows=1, cols=5)
    table.style = 'Light Grid Accent 1'
    
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'ID'
    hdr_cells[1].text = 'Hallazgo'
    hdr_cells[2].text = 'RAG'
    hdr_cells[3].text = 'EV (€)'
    hdr_cells[4].text = 'Acción'
    
    for hallazgo in hallazgos_top:
        row_cells = table.add_row().cells
        row_cells[0].text = hallazgo['ID']
        row_cells[1].text = hallazgo['Descripción']
        row_cells[2].text = hallazgo['RAG']
        row_cells[3].text = f"{hallazgo['EV']:,.0f}"
        row_cells[4].text = hallazgo['CP_RW']
        
        # Colorear celda RAG
        if hallazgo['RAG'] == 'Rojo':
            shading_elm = row_cells[2]._element.get_or_add_tcPr().get_or_add_shd()
            shading_elm.set(qn('w:fill'), 'FFCCCB')
    
    # 3. Cuantificación
    doc.add_heading('3. Cuantificación Agregada', 1)
    # ... (añadir tabla de resumen EV)
    
    # 4. CPs
    doc.add_heading('4. Conditions Precedent Esenciales', 1)
    # ... (listar CPs)
    
    # Guardar
    doc.save(output_path)
    print(f"✅ Resumen ejecutivo generado: {output_path}")

# Uso:
# generar_resumen_ejecutivo(top_10_hallazgos, params, '/mnt/user-data/outputs/resumen_ejecutivo.docx')
```

---

## Referencias y Normativa Consolidada

### Jurídico (Modelo A)

<file_location>references/marco_normativo_juridico.md</file_location>

Contiene listado detallado de:
- RDL 5/2023, LSC, RRM, LDC, RGPD, LO 3/2018, Ley 2/2023, Ley 10/2010, CP art.31bis, UNE 19601:2025, ET, LGSS, Leyes IP
- Enlaces BOE actualizados
- Extractos de artículos relevantes

### Fiscal (Modelo B)

<file_location>references/marco_normativo_fiscal.md</file_location>

Contiene:
- LGT, LIS, LIVA, IRPF, Reglamentos (RIVA, RD 1619/2012, RGGI, RD 2063/2004, RD 634/2015)
- Especificaciones técnicas AEAT (Veri*factu, factura electrónica)
- Enlaces BOE + AEAT

### Ambiental (Modelo C)

<file_location>references/marco_normativo_ambiental.md</file_location>

Contiene:
- Ley 26/2007, RD 2090/2008, Ley 21/2013, Ley 7/2022, RD 9/2005, Ley 16/2002, RD 815/2013, Directiva IED 2010/75/UE, ISO 14001, ISO 14015, ISO 19011
- Enlaces BOE + EUR-Lex + ISO

---

## Notas Finales de Uso

### Cuándo Usar Esta Skill

✅ **Usar cuando:**
- Usuario solicita "due diligence en España"
- Contexto M&A o adquisición de empresa española
- Necesidad de análisis de riesgos transaccionales
- Preparación de informes pre-inversión
- Referencias a normativa española (BOE, LSC, LGT, RGPD, etc.)

❌ **NO usar cuando:**
- Due diligence fuera de España (normativa diferente)
- Consultas de derecho general sin contexto transaccional
- Asesoramiento jurídico/fiscal específico de un caso concreto (disclaimers)

### Disclaimers Importantes

⚠️ **AVISO LEGAL:**
- Esta skill proporciona **plantillas operativas** y **metodología** para due diligence
- **NO sustituye** asesoramiento jurídico, fiscal o técnico profesional en casos concretos
- Las referencias normativas deben **verificarse** frente a:
  * Normativa autonómica específica de cada CCAA
  * Regulaciones sectoriales del target
  * Jurisprudencia y criterios administrativos actualizados
- Las cuantificaciones de riesgos son **estimativas** y requieren validación por expertos
- Siempre involucrar asesores legales, fiscales y técnicos externos en operaciones reales

### Personalización por Sector

La metodología es genérica y debe **adaptarse** según el sector del target:
- **Financiero:** Due diligence regulatoria específica (Banco de España, CNMV, DGS)
- **Sanitario:** Licencias sanitarias, autorización de centros, protección de datos de salud
- **Energía:** Autorizaciones CNE/CNMC, conexión a red, certificados energéticos
- **Telecom:** Licencias spectrum, CNMC, protección de datos de tráfico
- **Transporte:** Licencias de operador, concesiones administrativas
- **Construcción:** Licencias urbanísticas, POI si gran proyecto, calificación contratista

### Output Esperado

Al finalizar el uso de esta skill, se deben haber generado:
1. ✅ Informes DOCX (resumen ejecutivo + 3 informes detallados)
2. ✅ Matriz de riesgos Excel (con dashboard visual)
3. ✅ Anexos operativos (DRL, Q&A log, R&W/CPs)
4. ✅ Cuantificación monetaria (EV, reservas, ajustes precio)
5. ✅ Recomendaciones accionables (CPs, R&W, indemnities, escrows)

---

**Versión:** 1.0  
**Última actualización:** Octubre 2025  
**Autor:** NextHorizont AI  
**Basado en:** Documento maestro "MODELOS DE DUE DILIGENCE (ESPAÑA)"
