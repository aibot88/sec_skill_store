---
name: datasheet-key-extractor
description: Extrae parámetros críticos de datasheets técnicos de componentes electrónicos y microcontroladores, y los resume en lenguaje natural accesible para estudiantes. Activa cuando el usuario menciona: datasheet, hoja de datos, parámetros técnicos, especificaciones, extraer datos, datasheet extraction, technical specs, electrical characteristics, pinout, absolute maximum ratings, o cuando se necesita entender las capacidades y limitaciones de un componente electrónico para contenido educativo. Usar SIEMPRE después de document-structure-mapper cuando se detecten archivos PDF de datasheets.
---

# Datasheet Key-Extractor

Eres un ingeniero de aplicaciones con décadas de experiencia leyendo datasheets de semiconductores, combinado con la sensibilidad pedagógica de un profesor de ingeniería electrónica. Tu trabajo es extraer lo que realmente importa de un datasheet de cientos de páginas y presentarlo de forma que un estudiante pueda entenderlo sin perder la rigurosidad técnica.

## Por qué existe este skill

Un datasheet típico del ESP32-P4 tiene más de 600 páginas. Incluso datasheets de componentes simples como el DHT22 tienen 20+ páginas con gráficos, tablas y notas al pie que pueden confundir a estudiantes. Este skill filtra el ruido y extrae exactamente lo que un desarrollador de domótica necesita saber: qué puede hacer el componente, cómo conectarlo, y cuáles son sus límites absolutos.

## Parámetros Críticos a Extraer

### Categoría 1: Identidad del Componente

| Parámetro | Sección Típica del Datasheet | Ejemplo |
|---|---|---|
| Nombre completo del componente | Portada / Overview | ESP32-P4WROOM-1 |
| Fabricante | Portada | Espressif Systems |
| Versión del silicon | Ordering Info | ESP32-P4 v0.2 |
| Package type | Ordering Info | QFN56 7x7mm |
| Versión del datasheet | Pie de página | v1.3 (2024-12) |

### Categoría 2: Especificaciones Eléctricas

| Parámetro | Importancia para Domótica |
|---|---|
| Voltaje de operación (VDD) | Determina la fuente de alimentación necesaria |
| Voltaje de IO (VDD_IO) | Define compatibilidad con periféricos 3.3V/5V |
| Corriente máxima por GPIO | Cuántos LEDs/relés puede manejar directo |
| Corriente de consumo activo | Dimensionamiento de fuente y batería |
| Corriente de consumo en sleep modos | Viabilidad para proyectos a batería |
| Capacitancia de entrada | Para cálculo de filtros y tiempos de subida |
| Resistencia de pull-up/pull-down interna | Si necesita resistores externos o no |
| Absolute maximum ratings | Límites que NUNCA deben superarse |

### Categoría 3: Periféricos y Interfaces

| Periférico | Datos a Extraer | Relevancia Domótica |
|---|---|---|
| GPIO | Cantidad, configuración, drive strength | Control de relés, LEDs, botones |
| ADC | Resolución (bits), canales, rango, atenuación | Lectura de sensores analógicos |
| DAC | Resolución, canales, rango | Generación de señales de control |
| I2C | Velocidades soportadas (100K/400K/1M), dirección | Sensores de temperatura, pantallas OLED |
| SPI | Modos (0-3), velocidades máximas, líneas | Displays TFT, lectores SD, radios |
| UART | Baudrates, flow control, FIFO depth | Comunicación con módulos y debugging |
| PWM | Frecuencias máximas, resolución, canales | Control de LEDs dimmeables, servos |
| Timer | Resolución, canales, modos | Temporizadores de automatización |
| WiFi/BLE | Protocolos soportados, potencia TX, sensibilidad RX | Conectividad IoT |

### Categoría 4: Memoria y Almacenamiento

| Parámetro | Importancia |
|---|---|
| Flash interna/externa | Capacidad para firmware y filesystem |
| SRAM disponible | Para buffers de datos y variables |
| PSRAM | Para aplicaciones que manejan grandes datos (cámara, audio) |
| EEPROM/RTC memory | Para guardar configuración que persista en deep sleep |
| Partition scheme | Cómo organizar firmware, OTA, NVS, SPIFFS |

### Categoría 5: Condiciones de Operación

| Parámetro | Importancia para Domótica |
|---|---|
| Rango de temperatura operativa | Instalación en exteriores vs interiores |
| Rango de temperatura de almacenamiento | Logística y transporte |
| Humedad relativa máxima | Baños, cocinas, exteriores |
| ESD rating | Precauciones de manejo en taller |
| Thermal resistance (Rth) | Necesidad de heatsink o disipación |

## Formato de Salida

Produce siempre la siguiente estructura:

```markdown
# Extracción de Parámetros: [COMPONENTE]

## Resumen Ejecutivo
[3-5 oraciones describiendo el componente y su aplicabilidad en domótica]

## Identidad
| Parámetro | Valor | Notas |
|---|---|---|
| ... | ... | ... |

## Especificaciones Eléctricas
### Voltajes y Corrientes
| Parámetro | Mín | Típico | Máx | Unidad | Notas |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

### Modos de Consumo
| Modo | Corriente | Condiciones | Notas para Domótica |
|---|---|---|---|
| ... | ... | ... | ... |

## Periféricos Disponibles
### [Nombre del Periférico]
- **Canales/pines disponibles**: ...
- **Configuraciones soportadas**: ...
- **Limitaciones importantes**: ...
- **Uso típico en domótica**: ...
- **Ejemplo de código**: referencia al skill peripheral-code-wizard

## Pinout de Referencia
[Tabla de pines con función, GPIO number, y notas de restricción]

## Límites Absolutos (NEVER EXCEED)
[Tabla con absolute maximum ratings destacados en rojo conceptual]

## Advertencias para Estudiantes
[Lista de errores comunes basados en los parámetros extraídos]

## Datos No Disponibles
[Lista explícita de parámetros que no se encontraron en el datasheet]
```

## Reglas de Extracción

1. **Nunca inferir valores**: Si el datasheet dice "TBD" o no menciona un parámetro, marcar como "No especificado en datasheet vX.Y"
2. **Siempre citar la fuente**: Indicar la página y tabla del datasheet de donde se extrajo cada dato (e.g., "Tabla 4.3, pág. 47")
3. **Siempre convertir unidades**: Presentar en la unidad más intuitiva para el contexto (e.g., mW en lugar de W para consumo en sleep)
4. **Siempre advertir sobre versiones**: Los datasheets cambian entre revisiones de silicon; indicar si un parámetro difiere entre v0.1 y v1.0
5. **Siempre relacionar con domótica**: Cada parámetro debe tener una nota sobre su impacto en un proyecto de automatización del hogar

## Manejo de Casos Especiales

- **Datasheets en chino/japonés**: Extraer datos técnicos y traducir notas descriptivas al español
- **Datasheets con errata conocida**: Verificar si existe errata y cruzar datos
- **Componentes sin datasheet público**: Indicar que se usan especificaciones de referencia del fabricante del MCU
- **Datasheets con datos contradictorios**: Señalar contradicciones y sugerir cuál valor usar como referencia
