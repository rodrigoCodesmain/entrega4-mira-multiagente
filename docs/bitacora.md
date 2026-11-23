# Bitácora · Entregable 4 de MIRA

Responsable del registro · Rodrigo Guerrero. Controles humanos y revisiones identificados por actas e historial Git: Jorge (Control Humano 1 y revisión independiente de cierre) y Lester González (`elesteber`; Control Humano 2, apertura de ronda `1/2`, cierre de Fase 3, ejecución y comparación de línea base).

## Preparación del repositorio

| Fecha (Chile) | Evento registrado | Evidencia o estado |
| --- | --- | --- |
| 2026-11-22 | Inventario inicial del repositorio. | El clon tenía solo `README.md` y el commit inicial `c6d40b0`. |
| 2026-11-22 | Consulta del plan simplificado de CU-2 y de la pauta académica. | Insumos utilizados para documentar el flujo en [decisión](decision.md) y el [registro de traspasos](trabajo/README.md). |
| 2026-11-22 | Preparación de la estructura de GitHub y de documentación. | [Índice del repositorio](../README.md). |
| 2026-11-22 | Intento de crear y publicar el commit de preparación. | El clon bloqueó la escritura del índice de Git. GitHub devolvió 404 desde una sesión sin autenticar. El trabajo quedó en la copia local. |

## Recepción de salidas

| Origen | Salida esperada | Estado |
| --- | --- | --- |
| Responsable de agentes y corridas | Definiciones de agentes y skills, prompts, traspasos y logs de ambas corridas. | Recibidas ambas corridas (2026-11-22): definición de 4 agentes y 3 skills en `.agents/`, corrida multiagente cerrada en `e998cca` ([pytest-iter0.log](evidencia/pytest-iter0.log), [pytest-iter1.log](evidencia/pytest-iter1.log), [trabajo/](trabajo/README.md), [CORRIDA-MA-01/](evidencia/CORRIDA-MA-01/)), línea base de agente único en [CORRIDA-LB-01/](linea-base/CORRIDA-LB-01/resultado.md) y comparación aprobada en [comparacion-resultados.md](linea-base/comparacion-resultados.md). |
| Requisitos y representante del cliente | Especificación, aclaraciones con fuente o supuesto y aprobación humana. | Recibido y aprobado en Control Humano 1 (2026-11-22, Jorge): [01-requisitos.md](../specs/01-requisitos.md) y [001-requisitos-a-planificador.md](trabajo/001-requisitos-a-planificador.md). |
| Planificador y persona revisora del plan | Plan, tareas y registro del segundo control humano. | Plan recibido y **aprobado con observaciones en Control Humano 2** (2026-11-22, **Lester González**, responsable técnico humano, commit `7c0e152`): [02-plan.md](../specs/02-plan.md), [03-trazabilidad.md](../specs/03-trazabilidad.md) y [002-planificador-a-implementador.md](trabajo/002-planificador-a-implementador.md). |
| Implementador y Revisor QA | Código, pruebas ejecutadas, dictamen y evidencia de correcciones cuando corresponda. | **Fase 3 completada y cerrada con aprobación humana final** (`2026-11-22`, **Lester González**, responsable técnico humano, commit `e998cca`): iteración `0/2` (`e26eba3`, `46 passed` en [pytest-iter0.log](evidencia/pytest-iter0.log), [003-implementador-a-revisor.md](trabajo/003-implementador-a-revisor.md), dictamen `APROBADO CON OBSERVACIONES` en [004-revisor-a-implementador.md](trabajo/004-revisor-a-implementador.md), commit `2c88947`); iteración `1/2` (`e9dd4f6`, `48 passed, 0 failed, 0 skipped` en [pytest-iter1.log](evidencia/pytest-iter1.log), [005-implementador-a-revisor.md](trabajo/005-implementador-a-revisor.md), [03-trazabilidad.md](../specs/03-trazabilidad.md)) reauditada por `revisor` con dictamen **`APROBADO`** (`H-01` y `H-02` **`RESUELTO`**, `0` hallazgos nuevos) y aceptada en [006-revisor-final.md](trabajo/006-revisor-final.md) sin requerir ronda `2/2`. |
| Jorge | Matriz de criterio a prueba y revisión independiente de resultados. | **Recibida el 2026-11-23.** Jorge cruzó los 10 criterios de aceptación (`CA-01` a `CA-10`), los 10 casos del Excel y los 14 escenarios sintéticos con `MAN-INC` v2 y `CAT-ERR` v2. Contrastó el código, los agentes y sus skills, las actas, la comparación con la línea base y los logs de `pytest` (48/48 pruebas aprobadas en la corrida multiagente y 58/58 en la línea base). La lógica, el contrato HTTP, la seguridad y las pruebas resultaron conformes dentro del alcance revisado. Dejó observaciones documentales menores sobre el estado de `specs/03-trazabilidad.md`, el contenido de `docs/decision.md`, la alineación de `ejecucion-pruebas/SKILL.md` con el rol de solo lectura del revisor y la identificación de quienes participaron en los controles humanos. El [informe de revisión independiente](evidencia/revision-independiente-jorge.md) quedó incorporado en `docs/evidencia/`. |

Las filas de esta tabla se actualizan cuando llega un archivo verificable. Registrar el detalle del intercambio en [traspasos](trabajo/README.md) y el commit o referencia de la versión recibida.

## Corridas y controles humanos

| Registro | Estado | Destino de la evidencia |
| --- | --- | --- |
| Corrida multiagente | **Cerrada con aprobación humana final — Fase 3 completada** (`2026-11-22`, **Lester González**, responsable técnico humano): iteración `0/2` (`e26eba3`, `46 passed`, `APROBADO CON OBSERVACIONES` en `2c88947`) e iteración `1/2` (`e9dd4f6`, `48 passed, 0 failed, 0 skipped`, reauditoría `revisor` **`APROBADO`**, `H-01` y `H-02` **`RESUELTO`**, `0` hallazgos nuevos, sin ronda `2/2`); **publicada en el commit humano independiente de cierre `e998cca`**. | [evidencia/pytest-iter0.log](evidencia/pytest-iter0.log) · [evidencia/pytest-iter1.log](evidencia/pytest-iter1.log) · [003-implementador-a-revisor.md](trabajo/003-implementador-a-revisor.md) · [004-revisor-a-implementador.md](trabajo/004-revisor-a-implementador.md) · [005-implementador-a-revisor.md](trabajo/005-implementador-a-revisor.md) · [006-revisor-final.md](trabajo/006-revisor-final.md) · [invocacion-revisor-iter1.png](evidencia/CORRIDA-MA-01/invocacion-revisor-iter1.png) · [panel-subagentes.png](evidencia/CORRIDA-MA-01/panel-subagentes.png) |
| Comparación con un agente | **Ejecutada y comparada** (`2026-11-22`, `CORRIDA-LB-01` sobre directorio preparado externamente mediante `git archive 0e47c1c`, `58 passed, 0 failed, 0 skipped` en `0.27s`, `7/7` kit `OK`, `0` intervenciones humanas durante la corrida, `2` autocorrecciones internas de entorno/empaquetado, tokens/costo `No disponible`; comparación aprobada humanamente por **Lester González**, commits `014153e` y `cc9eb79`, con ajustes metodológicos menores en [comparacion-resultados.md](linea-base/comparacion-resultados.md)). | [comparacion-resultados.md](linea-base/comparacion-resultados.md) · [resultado.md](linea-base/CORRIDA-LB-01/resultado.md) · [metricas.md](linea-base/CORRIDA-LB-01/metricas.md) · [pytest.log](linea-base/CORRIDA-LB-01/pytest.log) · [workspace-aislado.png](linea-base/CORRIDA-LB-01/workspace-aislado.png) |
| Aprobación humana de la especificación | Aprobado — Control Humano 1 (2026-11-22, Jorge). Publicado en commit humano independiente `0e47c1c`; fase de planificación ejecutada. | [001-requisitos-a-planificador.md](trabajo/001-requisitos-a-planificador.md) · [01-requisitos.md](../specs/01-requisitos.md) |
| Control humano del plan | Aprobado con observaciones — Control Humano 2 (2026-11-22, **Lester González**, responsable técnico humano). Correcciones documentales aplicadas y publicadas en commit humano `7c0e152`; implementación iteración `0/2` ejecutada y publicada en `e26eba3`. | [002-planificador-a-implementador.md](trabajo/002-planificador-a-implementador.md) · [02-plan.md](../specs/02-plan.md) · [03-trazabilidad.md](../specs/03-trazabilidad.md) |
| Fallas, cambios y reejecuciones | Auditoría `revisor` (iteración `0/2`, `e26eba3`) detectó `H-01` (`Media`: pruebas tautológicas en `SYN-INJ-OK`) y `H-02` (`Baja`: `accion_recomendada` de `E-207` si falla un `servicio_dependiente != "SRV-MOD"` con `SRV-MOD` operativo). Decisión humana (**Lester González**, `2c88947`, 2026-11-22): abrir **ronda `1/2`**. Correcciones ejecutadas por `implementador` (`e9dd4f6`, `48 passed` en [pytest-iter1.log](evidencia/pytest-iter1.log), iteración `0/2` intacta en [pytest-iter0.log](evidencia/pytest-iter0.log)). Segunda auditoría `revisor` sobre `e9dd4f6` (`APROBADO`): `H-01` **`RESUELTO`**, `H-02` **`RESUELTO`**, `0` hallazgos nuevos ([006-revisor-final.md](trabajo/006-revisor-final.md)). **Cerrado con aprobación humana final el 2026-11-22** (Lester González, `e998cca`; sin ronda `2/2`). | [004-revisor-a-implementador.md](trabajo/004-revisor-a-implementador.md) · [005-implementador-a-revisor.md](trabajo/005-implementador-a-revisor.md) · [pytest-iter1.log](evidencia/pytest-iter1.log) · [006-revisor-final.md](trabajo/006-revisor-final.md) |
| Etiqueta de entrega | Pendiente de confirmación y de un commit final validado. | [Control de commits y etiqueta](decision.md#control-de-commits-y-etiqueta) |

Al incorporar una ejecución, anotar el ID y modalidad de la corrida, fecha y hora, commit inicial, herramienta y modelo, prompt, agente, skill efectivamente usada, entrada y salida, veredicto o resultado y enlaces a la evidencia. Para pruebas, incluir comando, código de salida y conteos reales. Para una decisión humana, incluir quién decidió, qué revisó, el veredicto y su referencia.

## Registro de Control Humano 1

- **Fecha de registro:** 2026-11-22
- **Quién decidió:** Jorge (representante del cliente)
- **Qué revisó:** [specs/01-requisitos.md](../specs/01-requisitos.md), `MAN-INC` v2, `CAT-ERR` v2, `GUI-COL` v1, `POL-ACC` v1, los 10 casos del Excel (`C-031` a `C-040`) y los 14 escenarios sintéticos, incluida la protección frente a instrucciones maliciosas en `L-009`.
- **Veredicto:** **Aprobado — Control Humano 1** (autoriza `specs/01-requisitos.md` tal como está y el paso al agente `planificador`; ratifica `E-512` con máximo 1 reproceso y `casos.reprocesos_realizados` global por caso incluyendo supuesto conservador para mixtos, máximo 3 para `E-207`/`E-305`, e interpretación sobre validaciones/facturación como supuesto del prototipo respaldado por esta aprobación; confirma códigos HTTP `200`/`403`/`404`/`422` y errores estándar `{"detail": "..."}` separados del contrato de cuatro campos).
- **Evidencia:** Aprobación escrita por WhatsApp proporcionada por el equipo.
- **Referencias:** [01-requisitos.md](../specs/01-requisitos.md#L295-L305) · [001-requisitos-a-planificador.md](trabajo/001-requisitos-a-planificador.md#L50-L70)
- **Efecto:** Desbloqueó la fase de planificación (`planificador`); aprobación publicada en el commit humano independiente `0e47c1c`.

## Ejecución Fase 2 · Planificador

- **Fecha y hora (Chile):** 2026-11-22 (inicio 17:04, término 17:08)
- **Commit inicial:** `0e47c1c`
- **Herramienta y modalidad:** Antigravity (`agy 1.5.14`, Orchestrator Neon) vía `invoke_subagent` (`planificador`, `conversationId: a80ad08c-9d33-4a06-b0e2-418174f2e7fb`)
- **Skills utilizadas:** `trazabilidad` (`.agents/skills/trazabilidad/SKILL.md`), `especificacion` y referencia de comandos de `ejecucion-pruebas`
- **Entradas:** [01-requisitos.md](../specs/01-requisitos.md), [001-requisitos-a-planificador.md](trabajo/001-requisitos-a-planificador.md), [AGENTS.md](../AGENTS.md), [decision.md](decision.md) y [verificar_trazabilidad.py](../.agents/skills/trazabilidad/scripts/verificar_trazabilidad.py)
- **Salidas generadas:** [02-plan.md](../specs/02-plan.md), [03-trazabilidad.md](../specs/03-trazabilidad.md) y [002-planificador-a-implementador.md](trabajo/002-planificador-a-implementador.md)
- **Verificación ejecutada:** `python3 .agents/skills/trazabilidad/scripts/verificar_trazabilidad.py --check-kit --matrix specs/03-trazabilidad.md` → código de salida `0` (`[OK]` integridad del kit y matriz válida; pruebas funcionales aún no ejecutadas)
- **Tokens / costo:** No informado por la herramienta (sin métricas inventadas)
- **Estado:** Cerrado con **Control Humano 2 aprobado con observaciones** el 2026-11-22 (publicado en commit `7c0e152`; implementación y pruebas iniciales ejecutadas en Fase 3, iteración `0/2`, commit `e26eba3`)

## Registro de Control Humano 2

- **Fecha:** 2026-11-22
- **Quién decidió:** Lester González (responsable técnico humano, commit `7c0e152`) *(revisión y aprobación realizadas directamente por una persona, no por el agente; las actas históricas `002`, `004` y `006` se conservan sin edición retroactiva)*
- **Qué revisó:** [02-plan.md](../specs/02-plan.md), [03-trazabilidad.md](../specs/03-trazabilidad.md) y [002-planificador-a-implementador.md](trabajo/002-planificador-a-implementador.md)
- **Veredicto:** **Aprobado con observaciones — Control Humano 2**
- **Correcciones documentales obligatorias aplicadas:**
  1. Separación coherente entre `CATALOGO_CAT_ERR_V2` (`frozenset` de pertenencia) y `REGLAS_CAT_ERR_V2` (estructura independiente por código), eliminando las expresiones `CATALOGO_CAT_ERR_V2["E-..."]` en `specs/03-trazabilidad.md`.
  2. Precisión de la distribución de los 14 escenarios sintéticos entre `tests/test_rules.py` (13 escenarios de dominio en memoria) y `tests/test_api.py` (donde `SYN-422` corresponde a validación HTTP junto con integración HTTP sobre `SYN-ROL-COM`, `SYN-NO-USER`, `SYN-NO-CASE`, `SYN-INJ-OK` y casos del Excel).
- **Evidencia de verificación documental:** `python3 .agents/skills/trazabilidad/scripts/verificar_trazabilidad.py --check-kit --matrix specs/03-trazabilidad.md` (código de salida `0`; todas las pruebas permanecen como `Planificado (no ejecutado)`).
- **Referencias:** [02-plan.md](../specs/02-plan.md#L246-L256) · [002-planificador-a-implementador.md](trabajo/002-planificador-a-implementador.md#L55-L73)
- **Efecto:** Planificación aprobada y publicada en el commit humano `7c0e152`; habilitó el paso al agente `implementador` en Fase 3 (iteración `0/2` publicada en `e26eba3`).

## Ejecución Fase 3 · Implementador (Iteración 0/2)

- **Fecha y hora (Chile):** 2026-11-22 (inicio 19:23, término 19:30)
- **Commit inicial:** `7c0e152`
- **Herramienta y modalidad:** Antigravity (`agy 1.5.14`, Orchestrator Neon) vía `invoke_subagent` (`implementador`, `conversationId: 30625f4b-c3db-4582-8621-966a1524504a`)
- **Skills utilizadas:** `ejecucion-pruebas` ([SKILL.md](../.agents/skills/ejecucion-pruebas/SKILL.md) y [run_tests.sh](../.agents/skills/ejecucion-pruebas/scripts/run_tests.sh)) y `trazabilidad` ([SKILL.md](../.agents/skills/trazabilidad/SKILL.md) y [verificar_trazabilidad.py](../.agents/skills/trazabilidad/scripts/verificar_trazabilidad.py))
- **Entradas:** [01-requisitos.md](../specs/01-requisitos.md), [02-plan.md](../specs/02-plan.md), [03-trazabilidad.md](../specs/03-trazabilidad.md), [002-planificador-a-implementador.md](trabajo/002-planificador-a-implementador.md), [AGENTS.md](../AGENTS.md) y normas/datos vigentes del kit CU-2
- **Salidas generadas:** `pyproject.toml`, `src/mira_reproceso/{__init__,models,loader,rules,api}.py`, `tests/{test_rules,test_api}.py`, [pytest-iter0.log](evidencia/pytest-iter0.log), [03-trazabilidad.md](../specs/03-trazabilidad.md) y [003-implementador-a-revisor.md](trabajo/003-implementador-a-revisor.md)
- **Comandos de verificación ejecutados:**
  - `uv venv .venv && uv pip install --python .venv/bin/python -e ".[dev]"` → código de salida `0` (`CPython 3.12.14`)
  - `bash -o pipefail -c './.agents/skills/ejecucion-pruebas/scripts/run_tests.sh 2>&1 | tee docs/evidencia/pytest-iter0.log'` → código de salida `0`; `sha256sum -c docs/kit-sha256sums.txt`: **7/7 `OK`**; `pytest -p no:cacheprovider -v`: **`46 passed, 0 failed, 0 skipped, 1 warning in 1.09s`** (`StarletteDeprecationWarning` en `fastapi/testclient.py` sobre `httpx`/`httpx2`)
  - `PYTHONDONTWRITEBYTECODE=1 python3 .agents/skills/trazabilidad/scripts/verificar_trazabilidad.py --check-kit --matrix specs/03-trazabilidad.md` → código de salida `0`
- **Tokens / costo:** No informado por la herramienta (sin métricas inventadas)
- **Estado:** Conservado en el commit humano `e26eba3` (`feat: registrar implementacion inicial CU-2 iteracion 0`) y auditado por el agente `revisor` en iteración `0/2`.

## Ejecución Fase 3 · Revisor (Iteración 0/2)

- **Fecha y hora:** 2026-11-22 (`19:45:50-03:00` invocación · `22:48:55Z` / `19:48:55-03:00` recepción del dictamen)
- **Commit de referencia auditado:** `e26eba3`
- **Herramienta y entorno:** Antigravity (orquestador + invocación real del subagente `revisor` mediante `invoke_subagent`)
- **Agente invocado:** `revisor` (`conversationId`: `e61985ce-c65b-43b1-9a5d-d348800704c4`)
- **Herramientas confirmadas en sesión del Revisor:** `read_file`, `send_message`, `list_resources`, `read_resource`, `manage_task` (ausencia confirmada de `write_file`, `edit_file`, `run_command` y servidores MCP heredados; solo lectura estricta verificada)
- **Entradas auditadas (rutas bajo `/home/lester/Documents/entrega4-mira-multiagente/`):** `AGENTS.md`, `docs/decision.md`, `docs/bitacora.md`, `specs/01-requisitos.md`, `specs/02-plan.md`, `specs/03-trazabilidad.md`, corpus CU-2 (`MAN-INC` v2, `CAT-ERR` v2, `CAT-ERR` v1 solo para verificar exclusión, `GUI-COL` v1, `POL-ACC` v1, `PRO-MAN` v1), `docs/kit-sha256sums.txt`, `pyproject.toml`, `src/mira_reproceso/{__init__.py,models.py,loader.py,rules.py,api.py}`, `tests/{test_rules.py,test_api.py}`, `docs/trabajo/{README.md,001-requisitos-a-planificador.md,002-planificador-a-implementador.md,003-implementador-a-revisor.md}`, `docs/evidencia/pytest-iter0.log` y scripts de `.agents/skills/`
- **Salida registrada:** `docs/trabajo/004-revisor-a-implementador.md` (dictamen transcrito íntegramente por el orquestador sin alteraciones al texto del Revisor, con sección de decisión humana pendiente)
- **Dictamen emitido:** `APROBADO CON OBSERVACIONES`
- **Resumen de hallazgos por severidad:**
  - `Crítica`: 0
  - `Alta`: 0
  - `Media`: 1 (`H-01`: `SYN-INJ-OK` en `tests/test_rules.py:432-444` y `tests/test_api.py:284-292` usa variables locales desconectadas y aserciones tautológicas; el caso real `C-038`/`L-009` + `test_loader_solo_lectura_y_exclusion_registro_tecnico` sí prueban la exclusión estructural real sobre `CU-2_datos.xlsx`)
  - `Baja`: 1 (`H-02`: `src/mira_reproceso/rules.py:270-285` y `184-188`, borde teórico en `E-207` si falla un `servicio_dependiente != "SRV-MOD"` mientras `"SRV-MOD"` está `"operativo"`)
- **Tokens / costo:** No informado por la herramienta (sin métricas inventadas)
- **Estado:** Revisado por **Lester González** (responsable técnico del equipo, commit `2c88947`) el 2026-11-22 con decisión de **Solicitar correcciones (apertura de ronda `1/2`)**; detenido para commit humano independiente previo a invocar al `implementador`.

## Decisión Humana · Revisión Iteración 0/2 (Apertura Ronda 1/2)

- **Fecha:** 2026-11-22
- **Quién decidió:** **Lester González** (responsable técnico del equipo, commit `2c88947`) *(decisión humana directa; no emitida por el agente)*
- **Qué revisó:** Dictamen independiente del agente `revisor` (`conversationId: e61985ce-c65b-43b1-9a5d-d348800704c4`) sobre la iteración `0/2` (commit `e26eba3`), registrado en [004-revisor-a-implementador.md](trabajo/004-revisor-a-implementador.md)
- **Decisión:** **Solicitar correcciones — Apertura de ronda `1/2`** *(no se rechaza la implementación completa; el dictamen `APROBADO CON OBSERVACIONES` se considera válido, pero se resuelve subsanar los dos hallazgos verificados antes de cerrar la entrega)*
- **Correcciones autorizadas para la ronda `1/2`:**
  1. **`H-01` (`Media`):** reemplazar las pruebas tautológicas de `SYN-INJ-OK` por una prueba real sobre la frontera de entrada usando un Excel sintético temporal con `registro_tecnico` hostil cargado mediante `cargar_datos_excel`, sin modificar el kit original (`kit/CU-2_soporte_operacion/`), comprobando que el resultado normativo de un caso elegible no cambia (y opcionalmente verificando rechazo HTTP `422` ante campos extra).
  2. **`H-02` (`Baja`):** corregir la selección de `accion_recomendada` para `E-207` cuando `SRV-MOD` está `operativo` pero otro servicio dependiente no lo está, añadiendo una prueba de regresión específica.
- **Referencias:** [004-revisor-a-implementador.md](trabajo/004-revisor-a-implementador.md#L182-L194) · commit auditado `e26eba3`
- **Estado:** Conservado y publicado en el commit humano independiente `2c88947` (`docs: registrar auditoria independiente y solicitar correcciones`), habilitando la ejecución acotada de la ronda `1/2`.

## Ejecución Fase 3 · Implementador (Iteración 1/2)

- **Fecha y hora (Chile):** 2026-11-22 (`20:39:47-03:00` invocación · `23:44:43Z` / `20:44:43-03:00` término)
- **Commit base:** `2c88947`
- **Herramienta y modalidad:** Antigravity (`agy 1.5.14`, Orchestrator Neon) vía `invoke_subagent` (`implementador`, `conversationId: 939546ea-7d84-4a46-878a-ae5960676b77`)
- **Skills utilizadas:** `ejecucion-pruebas` ([SKILL.md](../.agents/skills/ejecucion-pruebas/SKILL.md) y [run_tests.sh](../.agents/skills/ejecucion-pruebas/scripts/run_tests.sh)) y `trazabilidad` ([SKILL.md](../.agents/skills/trazabilidad/SKILL.md) y [verificar_trazabilidad.py](../.agents/skills/trazabilidad/scripts/verificar_trazabilidad.py))
- **Alcance acotado atendido:**
  - **`H-01` (`Media`):** eliminadas las variables/aserciones tautológicas de `SYN-INJ-OK` en `tests/test_rules.py` y `tests/test_api.py`; reemplazadas por generación en `tmp_path` de un `.xlsx` temporal con hoja `registro_tecnico` hostil cargado mediante `cargar_datos_excel()` y evaluado vía `evaluar_elegibilidad()` y `TestClient(create_app(datos=...))`, verificando exclusión de `registro_tecnico` y marcadores hostiles (`ORG-02`, `puede_reprocesar=false`, `INYECCION_HOSTIL_SYN_TEST`), más rechazo explícito `HTTP 422` si se envía `"registro_tecnico"` como campo extra en el JSON.
  - **`H-02` (`Baja`):** corregida en `src/mira_reproceso/rules.py` (`evaluar_elegibilidad` y `_seleccionar_accion_bloqueo`) la selección de `accion_recomendada` para `E-207` cuando `SRV-MOD` está `operativo` pero falla otro `servicio_dependiente` (emitiendo `"No reprocesar; esperar a que el servicio dependiente '<servicio_id>' vuelva a estar operativo."` sin citar `SRV-MOD`, manteniendo prioridad de `SRV-MOD` si también falla), con pruebas de regresión en `tests/test_rules.py` y `tests/test_api.py`.
- **Entradas:** [004-revisor-a-implementador.md](trabajo/004-revisor-a-implementador.md), [AGENTS.md](../AGENTS.md), [01-requisitos.md](../specs/01-requisitos.md), [02-plan.md](../specs/02-plan.md), [03-trazabilidad.md](../specs/03-trazabilidad.md), `src/mira_reproceso/{rules,loader}.py`, `tests/{test_rules,test_api}.py`
- **Salidas generadas / actualizadas:** `src/mira_reproceso/rules.py`, `tests/test_rules.py`, `tests/test_api.py`, [03-trazabilidad.md](../specs/03-trazabilidad.md), [pytest-iter1.log](evidencia/pytest-iter1.log) (conservando intacto [pytest-iter0.log](evidencia/pytest-iter0.log)) y [005-implementador-a-revisor.md](trabajo/005-implementador-a-revisor.md)
- **Comandos de verificación ejecutados:**
  - `bash -o pipefail -c './.agents/skills/ejecucion-pruebas/scripts/run_tests.sh 2>&1 | tee docs/evidencia/pytest-iter1.log'` → código de salida `0`; `sha256sum -c docs/kit-sha256sums.txt`: **7/7 `OK`**; `pytest -p no:cacheprovider -v`: **`48 passed, 0 failed, 0 skipped, 1 warning in 1.14s`** (`27` ítems en `tests/test_api.py` + `21` ítems en `tests/test_rules.py`; `StarletteDeprecationWarning` en `fastapi/testclient.py` sobre `httpx`/`httpx2`)
  - `PYTHONDONTWRITEBYTECODE=1 python3 .agents/skills/trazabilidad/scripts/verificar_trazabilidad.py --check-kit --matrix specs/03-trazabilidad.md` → código de salida `0` (`[OK]` integridad del kit y matriz válida)
- **Tokens / costo:** No informado por la herramienta (sin métricas inventadas)
- **Estado:** Publicado en el commit humano `e9dd4f6` (`fix: corregir hallazgos H-01 y H-02 en iteracion 1`) y reauditado por el agente `revisor` en iteración `1/2` (evidencia `0/2` en `pytest-iter0.log` conservada íntegra).

## Ejecución Fase 3 · Revisor (Iteración 1/2 · Reauditoría)

- **Fecha y hora:** `2026-11-22` Chile (`21:03:45-03:00` invocación · `21:05:41-03:00` recepción del dictamen / `2026-11-23T00:05:41Z` UTC)
- **Commit de referencia auditado:** `e9dd4f6` (`fix: corregir hallazgos H-01 y H-02 en iteracion 1`)
- **Herramienta y modalidad:** Antigravity (orquestador + invocación real del subagente `revisor` vía `invoke_subagent`)
- **Agente invocado:** `revisor` (`conversationId: b7480979-17ff-4ea7-b780-30a0936b61b4`)
- **Herramientas confirmadas en sesión del Revisor:** `read_file`, `send_message`, `list_resources`, `read_resource`, `manage_task` (ausencia confirmada de `write_file`, `edit_file`, `run_command` y herramientas/servidores `mcp__*` heredados; solo lectura estricta verificada)
- **Entradas auditadas (rutas bajo `/home/lester/Documents/entrega4-mira-multiagente/`):** `AGENTS.md`, `docs/decision.md`, `docs/bitacora.md`, `specs/01-requisitos.md`, `specs/02-plan.md`, `specs/03-trazabilidad.md`, `docs/trabajo/{README.md,003-implementador-a-revisor.md,004-revisor-a-implementador.md,005-implementador-a-revisor.md}`, `docs/evidencia/pytest-iter0.log`, `docs/evidencia/pytest-iter1.log`, `pyproject.toml`, `src/mira_reproceso/{__init__.py,models.py,loader.py,rules.py,api.py}`, `tests/{test_rules.py,test_api.py}`, corpus CU-2 (`MAN-INC` v2, `CAT-ERR` v2, `CAT-ERR` v1 solo para verificar exclusión, `GUI-COL` v1, `POL-ACC` v1, `PRO-MAN` v1), `docs/kit-sha256sums.txt` y scripts de `.agents/skills/`
- **Salida registrada:** [006-revisor-final.md](trabajo/006-revisor-final.md) (dictamen transcrito íntegramente por el orquestador sin alteraciones al texto del Revisor, con sección de decisión humana final pendiente)
- **Dictamen emitido:** **`APROBADO`**
- **Estado de hallazgos previos verificado por el Revisor:**
  - `H-01` (`Media`): **`RESUELTO`** (Excel sintético temporal en `tmp_path` con hoja `registro_tecnico` hostil cargado mediante `cargar_datos_excel()` → dominio `evaluar_elegibilidad()` y HTTP `create_app()`, sin tautologías y con rechazo explícito `HTTP 422` ante campo extra `"registro_tecnico"`)
  - `H-02` (`Baja`): **`RESUELTO`** (`E-207` distingue fallo de `SRV-MOD` frente a fallo de otro `servicio_dependiente` con `SRV-MOD` operativo identificando el servicio bloqueante real, manteniendo prioridad de `SRV-MOD` si ambos fallan y pruebas de regresión en reglas y HTTP)
- **Nuevos hallazgos verificados:** `0` (`0` Crítica, `0` Alta, `0` Media, `0` Baja)
- **Métricas y contraste disponibles (sin datos inventados):**
  - `pytest-iter0.log` (`0/2`): `46 passed, 0 failed, 0 skipped, 1 warning in 1.09s` (`26` `test_api.py` + `20` `test_rules.py`), `7/7` checksums del kit `OK`
  - `pytest-iter1.log` (`1/2`): `48 passed, 0 failed, 0 skipped, 1 warning in 1.14s` (`27` `test_api.py` + `21` `test_rules.py`, `+2` casos de regresión `H-02` más reescritura de `SYN-INJ-OK` y caso `422` de `"registro_tecnico"`), `7/7` checksums del kit `OK`
  - Conformidad global verificada: `REQ-01..REQ-18` (`18/18`), `CA-01..CA-10` (`10/10`), inmutabilidad de especificaciones/plan/kit/contrato HTTP
  - **Tokens / costo:** No informado por la herramienta (sin métricas inventadas)
- **Estado:** Revisado por **Lester González** (responsable técnico humano, commit `e998cca`) el 2026-11-22 con decisión de **Aceptar la implementación y cerrar la Fase 3** (corrida multiagente cerrada; sin ronda `2/2`).

## Decisión Humana Final · Cierre de Fase 3 (Corrida Multiagente)

- **Fecha:** `2026-11-22`
- **Quién decidió:** **Lester González** (responsable técnico humano, commit `e998cca`) *(decisión humana directa; no emitida por el agente)*
- **Qué revisó:** Dictamen final independiente del agente `revisor` (`conversationId: b7480979-17ff-4ea7-b780-30a0936b61b4`) sobre la iteración `1/2` y el commit `e9dd4f6`, registrado íntegramente en [006-revisor-final.md](trabajo/006-revisor-final.md)
- **Veredicto:** **Aceptar la implementación y cerrar la Fase 3** *(corrida multiagente cerrada; no es necesario ejecutar la ronda `2/2`)*
- **Fundamento verificado:**
  - Dictamen final del Revisor: **`APROBADO`**.
  - `H-01` (`Media`): **`RESUELTO`**; `H-02` (`Baja`): **`RESUELTO`**; `0` hallazgos nuevos.
  - Suite automatizada: **`48 passed, 0 failed, 0 skipped`** ([pytest-iter1.log](evidencia/pytest-iter1.log)), con iteración `0/2` intacta ([pytest-iter0.log](evidencia/pytest-iter0.log), `46 passed`).
  - Integridad de los siete archivos del kit CU-2 confirmada (`7/7 OK` contra [kit-sha256sums.txt](kit-sha256sums.txt)).
- **Evidencia gráfica verificada en `docs/evidencia/CORRIDA-MA-01/`:** [invocacion-implementador.png](evidencia/CORRIDA-MA-01/invocacion-implementador.png), [invocacion-revisor.png](evidencia/CORRIDA-MA-01/invocacion-revisor.png), [invocacion-revisor-iter1.png](evidencia/CORRIDA-MA-01/invocacion-revisor-iter1.png) y [panel-subagentes.png](evidencia/CORRIDA-MA-01/panel-subagentes.png)
- **Referencias:** [006-revisor-final.md](trabajo/006-revisor-final.md#L142-L155) · commit `e9dd4f6`
- **Estado:** **Fase 3 completada y corrida multiagente cerrada**; publicada en el commit humano independiente `e998cca` (*docs: cerrar corrida multiagente con aprobacion humana final*). La línea base de agente único y la comparación documental quedan registradas en la sección siguiente.

## Ejecución Línea Base · Agente Único (`CORRIDA-LB-01`) y Cierre de Comparación

- **Fecha y marcas `date -Is` (Chile):** `2026-11-22` (`21:34:35-03:00` inicio · `21:42:09-03:00` término de verificación · `21:42:55-03:00` chequeo posterior registrado en [workspace-aislado.png](linea-base/CORRIDA-LB-01/workspace-aislado.png)). Intervalo aproximado derivado entre marcas inicio/término: `7 min 34 s` (`8 min 20 s` hasta el chequeo final), registrado en [metricas.md](linea-base/CORRIDA-LB-01/metricas.md) explícitamente como `No disponible` en su campo de duración calculada. *Nota:* los tiempos de ambas modalidades provienen de métodos distintos de registro y no deben interpretarse como una comparación experimental controlada de rendimiento.
- **Preparación de aislamiento (evidencia externa vs. reporte interno):** directorio aislado `/home/lester/Documents/mira-cu2-linea-base-aislada` preparado externamente mediante `git archive 0e47c1c` según los comandos documentados por **Lester González** (commit `014153e`, mitigando acceso al historial posterior en `R2`). Se distingue explícitamente esta evidencia externa de preparación del hecho de que el hash `0e47c1c` no fue anotado originalmente dentro de los reportes internos del agente único ([resultado.md](linea-base/CORRIDA-LB-01/resultado.md), [metricas.md](linea-base/CORRIDA-LB-01/metricas.md)).
- **Herramienta y modalidad:** Google Antigravity (`Orchestrator (Neon)` y modo `Turbo` visibles en [workspace-aislado.png](linea-base/CORRIDA-LB-01/workspace-aislado.png); submodelos internos y versión exacta de `agy` en esa sesión: `No disponible`), ejecutado como agente único en un solo hilo sin `invoke_subagent`, sin flujo de 4 roles y con `0` intervenciones humanas durante la corrida.
- **Entorno técnico:** Linux, `uv 0.13.8`, `CPython 3.12.14`, `fastapi 0.165.0`, `pydantic 2.14.4`, `openpyxl 3.1.5`, `httpx 0.28.1`, `pytest 9.2.0`.
- **Entradas:** [prompt-ejecucion.md](linea-base/CORRIDA-LB-01/prompt-ejecucion.md), [01-requisitos.md](../specs/01-requisitos.md), corpus/datos oficiales en `kit/CU-2_soporte_operacion/` y `.agents/skills/` del repositorio base.
- **Salidas registradas en `docs/linea-base/`:** [CORRIDA-LB-01/prompt-ejecucion.md](linea-base/CORRIDA-LB-01/prompt-ejecucion.md), [CORRIDA-LB-01/resultado.md](linea-base/CORRIDA-LB-01/resultado.md), [CORRIDA-LB-01/metricas.md](linea-base/CORRIDA-LB-01/metricas.md), [CORRIDA-LB-01/pytest.log](linea-base/CORRIDA-LB-01/pytest.log), [CORRIDA-LB-01/codigo-agente-unico.tar.gz](linea-base/CORRIDA-LB-01/codigo-agente-unico.tar.gz), [CORRIDA-LB-01/workspace-aislado.png](linea-base/CORRIDA-LB-01/workspace-aislado.png) y el informe comparativo [comparacion-resultados.md](linea-base/comparacion-resultados.md).
- **Verificaciones y métricas observables (sin datos inventados):**
  - `./.agents/skills/ejecucion-pruebas/scripts/run_tests.sh` → `EXIT_CODE=0`; integridad del kit (`docs/kit-sha256sums.txt`): **`7/7 OK`**; `pytest`: **`58 passed, 0 failed, 0 skipped, 1 warning in 0.27s`** (`StarletteDeprecationWarning` sobre `httpx`/`httpx2`).
  - `verificar_trazabilidad.py --check-kit --matrix specs/03-trazabilidad.md` → código `0`.
  - Cumplimiento reportado: `18/18 REQ` y `10/10 CA` respaldados por su suite propia (`20` `test_casos_excel.py` + `31` `test_escenarios_sinteticos.py` + `7` `test_seguridad.py`) y análisis de código frente a `specs/01-requisitos.md` (sin batería común de pruebas cruzadas entre ambas modalidades). Endpoint `POST /elegibilidad` conforme con `specs/01-requisitos.md`.
  - Correcciones internas durante la corrida: `2` ajustes propios de entorno/empaquetado (`pythonpath`/`tests/__init__.py` y `uv sync --reinstall-package mira-cu2`); `0` revisiones independientes externas.
  - **Tokens / costo:** `No disponible` (no informado por Antigravity).
- **Cierre humano de comparación (2026-11-22):** **Lester González** (responsable técnico humano, commits `014153e` y `cc9eb79`) aprobó [comparacion-resultados.md](linea-base/comparacion-resultados.md) con ajustes metodológicos menores *(el encabezado literal de dicho informe conserva `responsable técnico humano` sin edición retroactiva)*. Ambas modalidades lograron resultados funcionales satisfactorios; el agente único requirió menos tiempo activo registrado y menos coordinación, mientras la modalidad multiagente aportó una revisión independiente que permitió descubrir y corregir dos observaciones verificadas (`H-01` y `H-02`).
- **Estado:** **Comparación cerrada documentalmente y documentación de cierre actualizada** (pendiente únicamente commit final y etiqueta de entrega tras revisión humana).

## Análisis de fallos y taxonomía MAST (Criterio 16 de la rúbrica)

A efectos del análisis MAST (*Multi-Agent System Failure Taxonomy*, Cemri et al., 2025, arXiv:2503.13657) exigido en la pauta (`protocolo-comparacion.md §5.2` y Criterio 16 de la rúbrica), se distinguen explícitamente: (a) las **causas verificadas en código y pruebas** con *diff* observable (`e26eba3..e9dd4f6`), (b) las **hipótesis no demostradas causalmente** sobre la redacción de planes o definiciones `.agents/`, y (c) dos desajustes documentales en `.agents/` observados durante la auditoría sin edición retroactiva.

### 1. Fallos reales de ejecución en `CORRIDA-MA-01` (`e26eba3` → `e9dd4f6`)

| ID / Corrida | Categoría y modo MAST | Causa verificada en código / pruebas (hecho en `e26eba3`) | Hipótesis sobre planificación / `.agents/` *(no demostrada causalmente)* | Cambio verificable con *diff* (`e26eba3..e9dd4f6`) y reejecución |
|---|---|---|---|---|
| **`H-01` (`Media`)** · `CORRIDA-MA-01` iter. `0/2` | **Categoría 3 · *Task Verification & Termination* (*Incorrect / Incomplete Verification*)** en la verificación de pruebas | Verificado directamente en `e26eba3`: `tests/test_rules.py:432-444` y `tests/test_api.py:284-292` definieron variables locales (`registro_tecnico_hostil`, `_registro_hostil_ignorado`) y aserciones tautológicas desconectadas de `cargar_datos_excel()`, `evaluar_elegibilidad()` y `create_app()`. | *Hipótesis (Categoría 1 · subespecificación de tarea):* `specs/02-plan.md:166,188` describió `SYN-INJ-OK` como *"texto hostil simulado en fixture externo al motor"* y `.agents/agents/implementador.md:28` pidió *"casos sintéticos requeridos en memoria dentro de `tests/`"* sin exigir un `.xlsx` temporal en frontera real. **No demostrado causalmente:** ninguno de ambos archivos fue editado en `e9dd4f6` (bastó el dictamen `004` para corregir las pruebas) y `CORRIDA-LB-01` —sin `specs/02-plan.md`— incurrió en la misma tautología. | **`git diff e26eba3 e9dd4f6 -- tests/test_rules.py tests/test_api.py`**: reemplazo por `_crear_excel_sintetico_con_inyeccion()` en `tmp_path` con hoja `registro_tecnico` hostil ingestado vía `cargar_datos_excel()` → `evaluar_elegibilidad()` / `create_app()`, más `HTTP 422` ante campo extra `"registro_tecnico"`. Reejecución en [pytest-iter1.log](evidencia/pytest-iter1.log): **`48 passed, 0 failed, 0 skipped`** (`7/7` kit `OK`). Dictamen **`APROBADO`** (`H-01: RESUELTO`) en [006-revisor-final.md](trabajo/006-revisor-final.md). |
| **`H-02` (`Baja`)** · `CORRIDA-MA-01` iter. `0/2` | **Categoría 2 · *Inter-Agent Misalignment* (*Reasoning-Action Mismatch* / caso borde omitido)** | Verificado directamente en `e26eba3`: `src/mira_reproceso/rules.py:184-190, 270-285` activó `servicio_no_operativo_e207 = True` ante cualquier falla de `servicio_dependiente` con `codigo_error == "E-207"`, haciendo que `_seleccionar_accion_bloqueo` citara esperar a `SRV-MOD` aunque `SRV-MOD` estuviera `"operativo"` y fallara otro `servicio_dependiente != "SRV-MOD"`. | *Hipótesis (Categoría 1 · simplificación en traspaso):* la regla 5 resumida en `specs/02-plan.md:97` (*"Servicio dependiente / `SRV-MOD` no operativo → para `E-207`: '...cuando SRV-MOD esté operativo'"*) pudo inducir la agrupación en `rules.py`. **No demostrado causalmente:** `specs/02-plan.md` y `.agents/` no fueron modificados en `e9dd4f6`, por lo que no existe evidencia experimental de intervención sobre el plan o prompts. | **`git diff e26eba3 e9dd4f6 -- src/mira_reproceso/rules.py tests/test_rules.py tests/test_api.py`**: separación entre `servicio_no_operativo_e207` (`SRV-MOD`) y `servicio_no_operativo_otro` + `servicio_no_operativo_e207_otro_id`, conservando prioridad de `SRV-MOD` si ambos fallan, más 2 pruebas de regresión en dominio y HTTP. Reejecución en [pytest-iter1.log](evidencia/pytest-iter1.log): **`48 passed`** (`+2` casos `H-02`, `0` fallos). Dictamen **`APROBADO`** (`H-02: RESUELTO`) en [006-revisor-final.md](trabajo/006-revisor-final.md). |

### 2. Desajustes históricos en definiciones `.agents/` observados en revisión (sin edición retroactiva)

- **Conflicto skill vs. rol de solo lectura (`Obs. 3` · Categoría 1 MAST *System Design & Specification Issues*):** `.agents/skills/ejecucion-pruebas/SKILL.md:4,19,28,33` indica activar/ejecutar `run_tests.sh` también durante la auditoría del `revisor`, mientras `.agents/agents/revisor.md:8-10,17-19` retiró `run_command` para garantizar solo lectura estricta (`tools: [read_file]`). En las dos corridas reales del `revisor` (`004` y `006`) prevaleció el bloqueo técnico de herramientas de `revisor.md`, auditando `pytest-iter0.log` y `pytest-iter1.log`.
- **Desviación de formato en vocabulario de veredictos (`Obs. 6a` · Categoría 1 MAST *Disobey Task Specification* en formato de salida):** `.agents/agents/revisor.md:28` define únicamente `APROBADO` o `REQUIERE CORRECCIONES`, mientras en iteración `0/2` ([004-revisor-a-implementador.md](trabajo/004-revisor-a-implementador.md#L11-L35)) el `revisor` emitió `APROBADO CON OBSERVACIONES`. La compuerta humana de Lester González (`2c88947`) absorbió la desviación tratándola conservadoramente como solicitud de correcciones (`1/2`), y en `1/2` el `revisor` emitió literalmente `APROBADO`.

### 3. Nota metodológica de transparencia respecto al Criterio 16 de la rúbrica y al entorno `Orchestrator Neon`

En el historial Git del repositorio (`.agents/` congelado en `145efff`), **ningún commit posterior modificó los archivos `.agents/agents/*.md` ni `.agents/skills/*/SKILL.md`**, porque durante el cierre académico se prohibió alterar retroactivamente los prompts de las corridas ya cerradas o fabricar *diffs* ficticios. En consecuencia:
- **Relación causal verificada vs. hipótesis:** únicamente está verificada en artefactos la causa técnica en código/pruebas (`tests/test_rules.py`, `tests/test_api.py`, `src/mira_reproceso/rules.py` en `e26eba3`) junto con su *diff* de corrección (`e26eba3..e9dd4f6`) y reejecución (`48/48` en `pytest-iter1.log`). La eventual contribución de `specs/02-plan.md:97,166,188` o `.agents/agents/implementador.md:28` se consigna estrictamente como **hipótesis plausibles no demostradas**, porque no hubo modificación de esas líneas ni corrida experimental controlada de verificación sobre `.agents/`.
- **Brecha explícita frente a la rúbrica (Criterio 16):** si la rúbrica se interpreta literalmente exigiendo *"cambio en una línea de un agente o skill en `.agents/` con diff y nueva ejecución"*, esa modificación en `.agents/` **no ocurrió** y queda como **decisión humana pendiente** (abrir eventualmente una edición controlada de `.agents/` con reejecución formal, fuera de este cierre documental).
- **Entorno coordinador vs. perfiles personalizados (`Orchestrator Neon`):** en Antigravity (`agy 1.5.14`), **`Orchestrator (Neon)`** operó como el entorno/selector de coordinación de la sesión principal (donde el humano aplica las compuertas e invoca subagentes), mientras que los **cuatro perfiles personalizados** configurados son exclusivamente `requisitos`, `planificador`, `implementador` y `revisor` (`.agents/agents/*.md`). Antigravity no expone el desglose de modelos internos ejecutados dentro de cada subagente, por lo que ese campo permanece declarado como `No disponible` en actas y comparaciones.

## Resolución documental de la revisión independiente ([`revision-independiente-jorge.md`](evidencia/revision-independiente-jorge.md))

| Obs. (`revision-independiente-jorge.md §3`) | Estado | Resolución o aclaración documental verificada |
|---|---|---|
| **1. Estado obsoleto en `specs/03-trazabilidad.md`** | **Resuelta** | Actualizado encabezado y subsección de cierre en [specs/03-trazabilidad.md](../specs/03-trazabilidad.md) reflejando `48/48` en iteración `1/2`, dictamen `APROBADO` en `006-revisor-final.md` (`e998cca`) y revisión de Jorge (`220c553`), manteniendo validación `verificar_trazabilidad.py` con código `0`. |
| **2a. Estado Git §1 y enlace roto `#control-de-commits-y-etiqueta` en `docs/decision.md`** | **Resuelta** | Actualizada §1 de [docs/decision.md](decision.md) distinguiendo preparación inicial (`145efff`) vs. repositorio compartido vigente (`c6d40b0..220c553`), y creada la sección `## Control de commits y etiqueta` (`#control-de-commits-y-etiqueta`). |
| **2b. Justificación de herramientas y patrón de coordinación descartado en `docs/decision.md`** | **Resuelta** | Incorporadas las subsecciones `### 6.1 Justificación de herramientas por agente (principio de privilegio mínimo)` y `### 6.2 Patrones de coordinación descartados (costo, riesgo y control)` en [docs/decision.md](decision.md). |
| **3. Discordancia `ejecucion-pruebas/SKILL.md` vs. solo lectura `revisor.md`** | **Resuelta documentalmente** *(sin editar `.agents/`)* | Documentada en [docs/decision.md §6.3](decision.md#L81-L87) y en la sección MAST anterior, distinguiendo el texto de la skill frente a los permisos efectivos `tools: [read_file]` verificados en `004` y `006`. |
| **4. Identificación nominal de responsables humanos** | **Resuelta documentalmente** *(actas `002/004/006` e informe `comparacion-resultados.md` intactos)* | Identificados **Jorge** (`0e47c1c`, `220c553`), **Lester González** (`7c0e152`, `2c88947`, `e998cca`, `014153e`, `cc9eb79` respaldados por `git log`) y **Rodrigo Guerrero** (`c6d40b0`, `eb69c32`, `220c553`) en [docs/bitacora.md](bitacora.md) y [docs/decision.md](decision.md). |
| **5. Encuadre MAST para el informe (rúbrica Criterio 16)** | **Resuelta en análisis; decisión humana abierta sobre `.agents/`** | Documentado el mapeo MAST completo de `H-01`, `H-02` y las fricciones `.agents/` con total transparencia sobre la ausencia de commits posteriores a `145efff` en `.agents/` (véase sección MAST §3 arriba). |
| **6a. Vocabulario `revisor.md` vs. `APROBADO CON OBSERVACIONES`** | **Resuelta documentalmente** *(sin editar `.agents/` ni `004`)* | Documentada en [docs/decision.md §6.3](decision.md#L81-L87) y análisis MAST de esta bitácora. |
| **6b. Propiedad de semilla `specs/03-trazabilidad.md` (`requisitos.md` vs. `planificador`)** | **Resuelta documentalmente** *(sin editar `.agents/`)* | Aclarada en [docs/decision.md §6.3](decision.md#L81-L87): `requisitos.md:19` asignó la semilla, pero se materializó en Fase 2 (`planificador`, `7c0e152`). |
| **6c. `pytest-iter0.log` y `pytest-iter1.log` sin cabecera/exit code dentro del `.log`** | **Resuelta documentalmente** *(logs crudos preservados intactos)* | Los archivos conservan la salida estándar cruda de `run_tests.sh`; el comando exacto (`bash -o pipefail -c './.agents/skills/ejecucion-pruebas/scripts/run_tests.sh 2>&1 | tee ...'`) y `EXIT_CODE=0` están documentados en `003`, `005` y en las secciones de ejecución `0/2` y `1/2` de esta bitácora. |
| **6d. Estado pre-CH1 en `docs/linea-base/protocolo-comparacion.md`** | **Resuelta** | Actualizado el encabezado y añadida nota post-ejecución en [protocolo-comparacion.md](linea-base/protocolo-comparacion.md) enlazando a [comparacion-resultados.md](linea-base/comparacion-resultados.md) y preservando el diseño original. |
| **6e. Guarda defensiva `reprocesos < 0` (`rules.py:322-327`, `EX-05`) sin prueba dedicada** | **Pendiente (observación menor no bloqueante)** | Registrada como guarda defensiva adicional en `src/mira_reproceso/rules.py:322-327`; no bloquea el alcance vigente y no se añaden pruebas al permanecer cerrada la Fase 3. |
