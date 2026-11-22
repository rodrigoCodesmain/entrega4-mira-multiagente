# Bitácora · Entregable 4 de MIRA

Responsable del registro · Rodrigo Guerrero.

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
| Responsable de agentes y corridas | Definiciones de agentes y skills, prompts, traspasos y logs de ambas corridas. | Pendiente de recepción. |
| Requisitos y representante del cliente | Especificación, aclaraciones con fuente o supuesto y aprobación humana. | Recibido y aprobado en Control Humano 1 (2026-11-22, Jorge): [01-requisitos.md](../specs/01-requisitos.md) y [001-requisitos-a-planificador.md](trabajo/001-requisitos-a-planificador.md). |
| Planificador y persona revisora del plan | Plan, tareas y registro del segundo control humano. | Plan recibido y **aprobado con observaciones en Control Humano 2** (2026-11-22, responsable técnico humano): [02-plan.md](../specs/02-plan.md), [03-trazabilidad.md](../specs/03-trazabilidad.md) y [002-planificador-a-implementador.md](trabajo/002-planificador-a-implementador.md). |
| Implementador y Revisor QA | Código, pruebas ejecutadas, dictamen y evidencia de correcciones cuando corresponda. | Entrega del `implementador` (iteración `0/2`, commit `e26eba3`) recibida el 2026-11-22 (`46 passed, 0 failed, 0 skipped`): [003-implementador-a-revisor.md](trabajo/003-implementador-a-revisor.md), [pytest-iter0.log](evidencia/pytest-iter0.log), [03-trazabilidad.md](../specs/03-trazabilidad.md). Auditoría del `revisor` (iteración `0/2` sobre `e26eba3`): **`APROBADO CON OBSERVACIONES`** (0 críticos/altos; `H-01` Media y `H-02` Baja) en [004-revisor-a-implementador.md](trabajo/004-revisor-a-implementador.md). Decisión humana (2026-11-22, responsable técnico del equipo): **Solicitar correcciones — ronda `1/2` abierta**; detenido para commit humano previo a invocar al `implementador`. |
| Jorge | Matriz de criterio a prueba y revisión independiente de resultados. | Pendiente de recepción. |

Las filas de esta tabla se actualizan cuando llega un archivo verificable. Registrar el detalle del intercambio en [traspasos](trabajo/README.md) y el commit o referencia de la versión recibida.

## Corridas y controles humanos

| Registro | Estado | Destino de la evidencia |
| --- | --- | --- |
| Corrida multiagente | Fase 3 ejecutada el 2026-11-22: `implementador` (iteración `0/2` sobre `7c0e152`, publicada en `e26eba3`, `46 passed`) y `revisor` (iteración `0/2` sobre `e26eba3`, dictamen **`APROBADO CON OBSERVACIONES`**, `H-01` Media y `H-02` Baja). Decisión humana (2026-11-22): **Solicitar correcciones — ronda `1/2` abierta**; detenido para commit humano previo a ronda `1/2`. | [evidencia/pytest-iter0.log](evidencia/pytest-iter0.log) · [003-implementador-a-revisor.md](trabajo/003-implementador-a-revisor.md) · [004-revisor-a-implementador.md](trabajo/004-revisor-a-implementador.md) |
| Comparación con un agente | Sin ejecución registrada. | [Línea base](linea-base/README.md) |
| Aprobación humana de la especificación | Aprobado — Control Humano 1 (2026-11-22, Jorge). Publicado en commit humano independiente `0e47c1c`; fase de planificación ejecutada. | [001-requisitos-a-planificador.md](trabajo/001-requisitos-a-planificador.md) · [01-requisitos.md](../specs/01-requisitos.md) |
| Control humano del plan | Aprobado con observaciones — Control Humano 2 (2026-11-22, responsable técnico humano). Correcciones documentales aplicadas y publicadas en commit humano `7c0e152`; implementación iteración `0/2` ejecutada y publicada en `e26eba3`. | [002-planificador-a-implementador.md](trabajo/002-planificador-a-implementador.md) · [02-plan.md](../specs/02-plan.md) · [03-trazabilidad.md](../specs/03-trazabilidad.md) |
| Fallas, cambios y reejecuciones | Auditoría `revisor` (iteración `0/2`, `e26eba3`) detectó `H-01` (`Media`: pruebas tautológicas en `SYN-INJ-OK`) y `H-02` (`Baja`: `accion_recomendada` de `E-207` si falla un `servicio_dependiente != "SRV-MOD"` con `SRV-MOD` operativo). Decisión humana (2026-11-22): abrir **ronda `1/2`** de correcciones (pendiente de ejecución tras commit humano). | [004-revisor-a-implementador.md](trabajo/004-revisor-a-implementador.md) |
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
- **Quién decidió:** Responsable técnico humano *(revisión y aprobación realizadas directamente por una persona, no por el agente)*
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
- **Estado:** Revisado por el responsable técnico del equipo el 2026-11-22 con decisión de **Solicitar correcciones (apertura de ronda `1/2`)**; detenido para commit humano independiente previo a invocar al `implementador`.

## Decisión Humana · Revisión Iteración 0/2 (Apertura Ronda 1/2)

- **Fecha:** 2026-11-22
- **Quién decidió:** Responsable técnico del equipo *(decisión humana directa; no emitida por el agente)*
- **Qué revisó:** Dictamen independiente del agente `revisor` (`conversationId: e61985ce-c65b-43b1-9a5d-d348800704c4`) sobre la iteración `0/2` (commit `e26eba3`), registrado en [004-revisor-a-implementador.md](trabajo/004-revisor-a-implementador.md)
- **Decisión:** **Solicitar correcciones — Apertura de ronda `1/2`** *(no se rechaza la implementación completa; el dictamen `APROBADO CON OBSERVACIONES` se considera válido, pero se resuelve subsanar los dos hallazgos verificados antes de cerrar la entrega)*
- **Correcciones autorizadas para la ronda `1/2`:**
  1. **`H-01` (`Media`):** reemplazar las pruebas tautológicas de `SYN-INJ-OK` por una prueba real sobre la frontera de entrada usando un Excel sintético temporal con `registro_tecnico` hostil cargado mediante `cargar_datos_excel`, sin modificar el kit original (`kit/CU-2_soporte_operacion/`), comprobando que el resultado normativo de un caso elegible no cambia (y opcionalmente verificando rechazo HTTP `422` ante campos extra).
  2. **`H-02` (`Baja`):** corregir la selección de `accion_recomendada` para `E-207` cuando `SRV-MOD` está `operativo` pero otro servicio dependiente no lo está, añadiendo una prueba de regresión específica.
- **Referencias:** [004-revisor-a-implementador.md](trabajo/004-revisor-a-implementador.md#L182-L194) · commit auditado `e26eba3`
- **Estado:** **Detenido para commit humano independiente** que conserve el dictamen del `revisor` y la decisión de apertura de ronda `1/2`, antes de invocar al agente `implementador` (sin cambios en código, pruebas, especificaciones ni kit; sin commits ni pushes).
