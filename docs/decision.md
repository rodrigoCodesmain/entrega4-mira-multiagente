# Decisiones de diseño iniciales · MIRA CU-2

Este documento registra las decisiones arquitectónicas, normativas y de coordinación multiagente acordadas antes de iniciar la fase de especificación e implementación.

## 1. Enfoque metodológico y plataforma

- **Alternativa A (Desarrollo Conducido por Especificación, SDD)** sin GitHub SpecKit.
- **Plataforma y entorno de coordinación:** Google Antigravity (`agy` 1.5.14) utilizando **`Orchestrator (Neon)`** como entorno/selector de coordinación de la sesión principal.
  - *Distinción frente a los perfiles personalizados:* `Orchestrator (Neon)` es el entorno de sesión desde el que la persona operadora coordina compuertas y despacha subagentes (`invoke_subagent`); los **cuatro perfiles personalizados** definidos para el flujo son `requisitos`, `planificador`, `implementador` y `revisor` en [`.agents/agents/`](../.agents/agents/).
  - *Ambigüedad de telemetría frente a la rúbrica:* Antigravity muestra `Orchestrator (Neon)` como perfil/selector de sesión principal, pero no informa el desglose de modelos internos ejecutados por cada subagente ni el consumo de tokens/costo; por fidelidad documental, ambos se registran como `No disponible` en actas y comparación.
- **Control de versiones (fase inicial vs. repositorio compartido):**
  - *Preparación previa (ref. `145efff`):* inicialmente los archivos base se prepararon en copia local sin ejecutar `git init`, configurar remotos ni hacer commits o pushes mientras se habilitaba el repositorio GitHub compartido.
  - *Estado vigente en repositorio compartido (`main`, refs. `c6d40b0..220c553`):* el proyecto ya está integrado en el repositorio Git compartido desde el merge `15225bb` (`2026-11-22`) y opera bajo control de commits humanos independientes por hito, compuerta y auditoría. Véase la cadena verificada y el estado de etiqueta en [Control de commits y etiqueta](#control-de-commits-y-etiqueta).

## 2. Alcance funcional y exclusiones

- **Objetivo único:** evaluar la elegibilidad de reprocesamiento de un caso con error o detenido de MIRA CU-2 en una aplicación mínima Python con FastAPI y `pytest`.
- **Exclusiones explícitas:** no se implementará reprocesamiento real, interfaz frontend, RAG, servidor MCP, envío de notificaciones ni administración de incidentes.

## 3. Contrato mínimo de la futura API

- **Entrada:** `caso_id`, `usuario_id`.
- **Salida:** `puede_reprocesar`, `motivos`, `accion_recomendada`, `referencias_normativas`.
- Se excluyen campos adicionales y alertas de incidentes S2 en esta fase.

## 4. Base normativa y tratamiento de riesgos de datos

- **Documentos vigentes obligatorios:**
  - `MAN-INC` v2 (`kit/CU-2_soporte_operacion/corpus/MAN-INC_manual_incidentes.md`)
  - `CAT-ERR` v2 (`kit/CU-2_soporte_operacion/corpus/CAT-ERR_v2_vigente.md`)
- **Documento excluido:** `CAT-ERR` v1 (`kit/CU-2_soporte_operacion/corpus/CAT-ERR_v1_derogado.md`), por estar derogado desde el 1 de septiembre de 2026.
- **Aclaración pendiente de aprobación humana (`E-512`):**
  - `MAN-INC` v2 §4 establece un límite general de máximo 3 reprocesos y señala que los reprocesos por error interno de la plataforma no se contabilizan como validaciones.
  - `CAT-ERR` v2 §1 establece para `E-512` (error interno de la plataforma): *"Reprocesar una vez. Si vuelve a fallar, escalar a Ingeniería"*.
  - **Decisión provisional:** respetar la restricción específica de **1 reproceso** para `E-512` (`CAT-ERR` v2) y documentar la interpretación exacta del conteo (por ejemplo, comparación entre `casos.reprocesos_realizados` y los registros en la tabla `reprocesos`, y el alcance de "no se contabilizan como validaciones") como **aclaración pendiente de aprobación humana** en Control Humano 1.
- **Seguridad frente a inyección de instrucciones en datos:** la tabla `registro_tecnico` de `CU-2_datos.xlsx` (registro `L-009` de `C-038`) contiene una *prompt injection* simulada. Los datos del Excel se tratan únicamente como datos pasivos, nunca como instrucciones operativas.

## 5. Estrategia de datos y preservación del kit

- Los archivos en `kit/CU-2_soporte_operacion/` son una copia íntegra de solo lectura del material del profesor, verificable mediante `docs/kit-sha256sums.txt`.
- Las pruebas utilizarán los registros originales de `CU-2_datos.xlsx` junto con casos sintéticos en memoria en `tests/` para cubrir combinaciones no presentes en el Excel (ej. `E-102`, `E-512` con 0 y 1 reproceso, `E-207` con `SRV-MOD` operativo) sin alterar nunca el archivo original.

## 6. Arquitectura multiagente y skills

- **Cuatro agentes personalizados** en `.agents/agents/`:
  1. `requisitos`: redacta `specs/01-requisitos.md` y la base de trazabilidad (`read_file`, `write_file`, `edit_file`).
  2. `planificador`: redacta `specs/02-plan.md` a partir de la especificación aprobada (`read_file`, `write_file`, `edit_file`).
  3. `implementador`: implementa código y pruebas y ejecuta validaciones (`read_file`, `write_file`, `edit_file`, `run_command`, `manage_task`).
  4. `revisor`: auditor independiente de solo lectura pura (`read_file`, sin herramientas de edición/escritura ni de ejecución de comandos); inspecciona la especificación, el código, las pruebas y los logs/evidencias generados por el `implementador`, y entrega su dictamen completo en la conversación para registro humano en `docs/trabajo/`.
- Todos los agentes declaran `inheritMcp: false` para suprimir la herencia de servidores y herramientas MCP globales.
- **Tres skills propias** en `.agents/skills/`:
  1. `especificacion`: guía de redacción de especificación y plan conforme a fuentes vigentes y controles humanos.
  2. `trazabilidad`: matriz regla → requisito → componente → prueba y gestión de actas en `docs/trabajo/`, con script ejecutable `verificar_trazabilidad.py`.
  3. `ejecucion-pruebas`: ejecución reproducible de `pytest` y chequeo de integridad del kit en modo solo lectura mediante script ejecutable `run_tests.sh`.
- **Coordinación:** flujo secuencial `requisitos` → Control Humano 1 → `planificador` → Control Humano 2 → `implementador` ↔ `revisor` con máximo 2 rondas de corrección, registrando cada traspaso en `docs/trabajo/`.

### 6.1 Justificación de herramientas por agente (principio de privilegio mínimo)

Cada subagente recibe únicamente las herramientas estrictamente necesarias para producir los artefactos de su fase, aislando lectura, escritura y ejecución para prevenir modificaciones fuera de alcance y proteger la independencia de la auditoría:

| Agente | Herramientas habilitadas | Herramientas restringidas / omitidas | Justificación de diseño (privilegio mínimo) |
|---|---|---|---|
| `requisitos` | `read_file`, `write_file`, `edit_file` (`inheritMcp: false`) | Sin `run_command`, `manage_task` ni MCP heredados | Solo requiere leer el corpus normativo/kit y redactar `specs/01-requisitos.md` y su acta en `docs/trabajo/`. Omitir `run_command` impide ejecutar código o scripts sobre datos no confiables (`L-009`) o adelantarse a la implementación antes de **Control Humano 1**. |
| `planificador` | `read_file`, `write_file`, `edit_file` (`inheritMcp: false`) | Sin `run_command`, `manage_task` ni MCP heredados | Solo necesita leer la especificación aprobada y diseñar `specs/02-plan.md`, `specs/03-trazabilidad.md` y el traspaso `002`. Sin `run_command`, no puede crear entornos, instalar dependencias ni escribir o probar código antes de **Control Humano 2**. |
| `implementador` | `read_file`, `write_file`, `edit_file`, `run_command`, `manage_task` (`inheritMcp: false`) | Sin escritura en `kit/CU-2_soporte_operacion/` ni comandos Git (`AGENTS.md`) y sin MCP heredados | Es el único agente de ejecución técnica: necesita escritura para `pyproject.toml`, `src/`, `tests/` y `specs/03-trazabilidad.md`, y `run_command` / `manage_task` exclusivamente para preparar `.venv`, ejecutar `run_tests.sh` (validando SHA-256 del kit + `pytest`) y correr `verificar_trazabilidad.py`. |
| `revisor` | Exclusivamente `read_file` (junto con mensajería base `send_message`, `list_resources`, `read_resource`, `manage_task` del runtime; `inheritMcp: false`) | Sin `write_file`, `edit_file`, `run_command` ni servidores MCP heredados | Auditor independiente de **solo lectura pura**. Deshabilitar escritura y ejecución garantiza técnicamente que no puede corregir código por su cuenta, falsear logs ni mutar el kit, la matriz o las pruebas. Entrega su dictamen en conversación para registro humano en `docs/trabajo/`. |

- **Justificación transversal de `inheritMcp: false`:** todos los agentes desactivan la herencia de servidores MCP externos globales para reducir superficie de herramientas, evitar filtraciones hacia servicios externos y acotar la ejecución únicamente al repositorio local.

### 6.2 Patrones de coordinación descartados (costo, riesgo y control)

Antes de fijar el flujo secuencial con compuertas humanas (SDD · Alternativa A), se descartaron dos patrones alternativos por criterios de **costo**, **riesgo** y **control**:

1. **Malla autónoma entre pares (*peer-to-peer* / *swarm* sin compuertas humanas) o enrutador dinámico libre:**
   - **Costo:** habilita conversaciones abiertas y reintentos no acotados entre agentes, multiplicando el consumo de tokens, latencia y contexto sin garantía de convergencia.
   - **Riesgo:** sin detenciones obligatorias ni validación humana de requisitos (`CH1`) y diseño (`CH2`), un supuesto ambiguo (como el límite de `E-512` o reglas de `CAT-ERR` v1) puede propagarse automáticamente hasta el código y las pruebas. Además, difumina el principio de privilegio mínimo si todos los pares invocan herramientas de escritura o ejecución sobre el mismo árbol.
   - **Control:** dificulta reconstruir quién aprobó cada cambio contractual y elimina puntos deterministas de rollback en Git entre especificación, plan e implementación. El flujo secuencial elegido impone 2 compuertas humanas explícitas, actas `docs/trabajo/001..006` y un tope estricto de `2` rondas `implementador` ↔ `revisor`.
2. **Hilo único con agente autónomo sin separación Implementador–Revisor (evaluado como línea base `CORRIDA-LB-01`):**
   - **Costo:** menor sobrecarga operativa y menor tiempo activo en tareas acotadas (`~7 min 34 s` frente a `~21 min` sumados de subagentes en `CORRIDA-MA-01`, sin requerir traspasos formales).
   - **Riesgo:** introduce sesgo de confirmación y acoplamiento entre quien escribe el código, quien diseña las pruebas y quien las aprueba en la misma ventana de contexto. En `CORRIDA-LB-01`, aunque `58/58` pruebas pasaron, permanecieron sin detectar una prueba tautológica en `SYN-INJ-OK` (equivalente a `H-01`) y una recomendación genérica en `E-207` cuando falla otro servicio dependiente distinto de `SRV-MOD` (comparable a `H-02`).
   - **Control:** carece de verificación independiente de solo lectura y de compuerta de diseño (`CH2`) previa a codificar. Por ello se conservó únicamente como línea base comparativa experimental y no como arquitectura principal del sistema multiagente.

### 6.3 Notas de coherencia histórica entre definiciones de `.agents/` y ejecución real

Las definiciones de `.agents/agents/` y `.agents/skills/` quedaron congeladas desde la Fase 0 (commit `145efff`) para preservar trazabilidad fiel de la corrida sin reescrituras retroactivas. Durante las auditorías y la revisión independiente (`docs/evidencia/revision-independiente-jorge.md`) se constataron tres desajustes históricos entre texto normativo interno y ejecución real:

1. **`.agents/skills/ejecucion-pruebas/SKILL.md` vs. solo lectura estricta en `.agents/agents/revisor.md`:** `SKILL.md` (líneas `4`, `28` y `33-36`) describe la ejecución de `run_tests.sh` también durante la auditoría del `revisor`, mientras `.agents/agents/revisor.md` (líneas `8-9` y `17`) suprimió `run_command` para imponer solo lectura pura. **Comportamiento efectivo verificado:** en ambas auditorías reales (`004-revisor-a-implementador.md` y `006-revisor-final.md`), las herramientas reales de sesión del `revisor` excluyeron `run_command`, por lo que `revisor` auditó los logs `pytest-iter0.log` y `pytest-iter1.log` generados por `implementador` (y complementados por verificación externa en host).
2. **Vocabulario de veredictos en `.agents/agents/revisor.md:28` vs. iteración `0/2`:** `revisor.md` especifica únicamente `APROBADO` o `REQUIERE CORRECCIONES`, pero en la iteración `0/2` el subagente emitió `APROBADO CON OBSERVACIONES` (`0` bloqueantes, `H-01` `Media`, `H-02` `Baja`). La compuerta humana de Lester González (`2c88947`) resolvió conservadoramente ese dictamen como **`SOLICITAR CORRECCIONES — RONDA 1/2 ABIERTA`**, y en la iteración `1/2` el `revisor` emitió literalmente **`APROBADO`**.
3. **Inicialización de `specs/03-trazabilidad.md` (`.agents/agents/requisitos.md:19` vs. ejecución):** aunque `requisitos.md` menciona iniciar la semilla de `specs/03-trazabilidad.md`, la tabla vacía sin diseño técnico aún no aportaba componentes ni pruebas; por coordinación real, `planificador` materializó `specs/03-trazabilidad.md` en Fase 2 (`7c0e152`) con las columnas y filas iniciales `RN-01..RN-18` en estado `Planificado (no ejecutado)`.

## 7. Verificación técnica en Antigravity 1.5.14 y limitaciones reales de permisos

Resultados reales comprobados en esta fase de preparación:

1. **Descubrimiento CLI (`agy agents`):** detectó los 4 agentes personalizados (`implementador`, `planificador`, `requisitos`, `revisor`) directamente desde `.agents/agents/*.md`, sin requerir `.git` ni empaquetado como plugin.
2. **Invocación de agentes y skills:**
   - **Vía CLI (`agy --agent <nombre> -p ...`):** los 4 agentes se invocaron correctamente y reconocieron las 3 skills del proyecto (`especificacion`, `trazabilidad`, `ejecucion-pruebas`).
   - **Vía `invoke_subagent`:** en la sesión inicial donde recién se crearon los archivos `.agents/agents/*.md`, `invoke_subagent` devolvió `subagent "requisitos" not found or not allowed to be invoked` (catálogo cargado al inicio). Tras recargarse los agentes en el turno siguiente / nueva evaluación, **`invoke_subagent(TypeName="requisitos", ...)` sí funcionó** directamente para ejecutar la Fase 1 en contexto aislado (produciendo `specs/01-requisitos.md` y `docs/trabajo/001-requisitos-a-planificador.md`). Se mantiene `agy --agent <nombre> -p` como alternativa verificada si ocurriese un fallo puntual.
3. **Separación real de herramientas por agente:**
   - `requisitos` y `planificador`: declararon `read_file`, `write_file`, `edit_file` (sin `run_command`). `requisitos` creó `docs/trabajo/000-prueba-traspaso.md` sin bloqueos.
   - `implementador`: declaró `read_file`, `write_file`, `edit_file`, `run_command`, `manage_task`.
   - `revisor`: tras el ajuste de seguridad, declaró únicamente `read_file` (junto con `send_message`, `manage_task`, `list_resources` y `read_resource` base del runtime), con **`write_file`, `edit_file` y `run_command` efectivamente ausentes**.
4. **Limitaciones reales de permisos y resultado de `inheritMcp: false`:**
   - **Aislamiento de `revisor`:** al retirar `run_command` de `.agents/agents/revisor.md`, el Revisor queda técnicamente impedido de editar archivos y ejecutar comandos o código; la verificación ejecutable recae en los logs y evidencias generados por el `implementador` (y/o ejecución manual).
   - **Herencia MCP (`inheritMcp: false`):** verificado como **compatible** en Antigravity 1.5.14 en `revisor` y `requisitos`. Elimina por completo la sección `<mcp_servers>`, `call_mcp_tool` y todas las herramientas `mcp_*` de los plugins globales (`data-agent-kit-plugin` y `gemini-api`). Únicamente permanecen en el esquema base del runtime las declaraciones genéricas `list_resources`, `read_resource`, `send_message` y `manage_task`, sin servidores MCP asociados. Se aplicó `inheritMcp: false` a los 4 agentes.
5. **Scripts ejecutables e integridad del kit:**
   - `run_tests.sh --check-only` y `verificar_trazabilidad.py --check-kit` ejecutaron con código `0`, validando los 7 archivos intactos de `kit/CU-2_soporte_operacion/` contra `docs/kit-sha256sums.txt`.
   - `revisor` entregó su dictamen mínimo `APROBADO` (`0/2`) en la conversación sin crear ni modificar archivos *(prueba técnica previa al flujo principal de CU-2; la auditoría real de `CORRIDA-MA-01` consta en `docs/trabajo/004-revisor-a-implementador.md` y `docs/trabajo/006-revisor-final.md`)*.

## Control de commits y etiqueta

Para preservar auditabilidad por etapa y compuerta humana, cada cambio autorizado se consolidó en commits independientes en la rama `main`, sin ejecución automática de comandos Git (`commit`, `push`, `tag`) por parte de los subagentes.

### Cadena verificable de commits en `main`

| Commit | Fecha (Chile) | Autor Git (`git log`) | Responsable / rol humano | Hito o compuerta registrada |
|---|---|---|---|---|
| `c6d40b0` | 2026-11-22 00:05 | `rodrigoCodesmain` | Rodrigo Guerrero | Commit inicial del repositorio (`README.md`). |
| `eb69c32` | 2026-11-22 01:56 | `Rodrigo` | Rodrigo Guerrero | Estructura inicial de documentación, traspasos, bitácora y evidencias. |
| `145efff` | 2026-11-22 02:04 | `elesteber` | Lester González | Configuración de los 4 agentes, 3 skills, kit oficial CU-2, `docs/kit-sha256sums.txt` y borrador `specs/01-requisitos.md` (`000`, `001`). |
| `15225bb` | 2026-11-22 02:09 | `elesteber` | Lester González | Merge de integración entre estructura documental e insumos técnicos CU-2. |
| `414d6e7` | 2026-11-22 02:29 | `elesteber` | Lester González | Definición del protocolo de comparación (`docs/linea-base/protocolo-comparacion.md`) y actualización de `README.md`. |
| `0e47c1c` | 2026-11-22 16:46 | `elesteber` | Lester González (publicación en Git) · **Jorge** (aprobación CH1) | **Control Humano 1:** aprobación formal de `specs/01-requisitos.md` por Jorge (`COMMIT_BASE_CH1`). |
| `7c0e152` | 2026-11-22 19:21 | `elesteber` | Lester González | **Control Humano 2:** aprobación con observaciones del plan técnico (`specs/02-plan.md`, `specs/03-trazabilidad.md`, `002`). |
| `e26eba3` | 2026-11-22 19:43 | `elesteber` | Lester González | Registro de implementación inicial (`implementador`, iteración `0/2`, `46 passed` en `pytest-iter0.log`, `003`). |
| `2c88947` | 2026-11-22 20:17 | `elesteber` | Lester González | **Compuerta post-revisor (`0/2`):** registro de auditoría independiente (`004`) y apertura de ronda `1/2` (`H-01`, `H-02`). |
| `e9dd4f6` | 2026-11-22 21:02 | `elesteber` | Lester González | Correcciones `H-01` y `H-02` en iteración `1/2` (`48 passed` en `pytest-iter1.log`, `005`). |
| `e998cca` | 2026-11-22 21:18 | `elesteber` | Lester González | **Cierre humano de Fase 3:** registro del dictamen `APROBADO` (`006-revisor-final.md`) y cierre de `CORRIDA-MA-01`. |
| `014153e` | 2026-11-22 23:22 | `elesteber` | Lester González | Registro de línea base `CORRIDA-LB-01` (`58 passed`) e informe `docs/linea-base/comparacion-resultados.md`. |
| `cc9eb79` | 2026-11-22 23:55 | `elesteber` | Lester González | Precisión de referencia de cierre multiagente en `comparacion-resultados.md`. |
| `220c553` | 2026-11-23 01:10 | `Rodrigo` | Rodrigo Guerrero (integración Git) · **Jorge** (revisión independiente) | Incorporación de [`docs/evidencia/revision-independiente-jorge.md`](evidencia/revision-independiente-jorge.md) y enlace en bitácora. |

### Estado de etiqueta de entrega (`git tag`)

- **Etiqueta de referencia prevista en `README.md`:** `entrega-3` (pauta académica: lanzar el flujo desde la etiqueta de entrega).
- **Estado actual en el repositorio:** **`Pendiente de confirmación y commit final`** (`git tag -l` vacío). La creación del commit final de cierre documental y el etiquetado correspondiente quedan sujetos a validación y autorización humana expresa antes de publicar en `origin/main`.
