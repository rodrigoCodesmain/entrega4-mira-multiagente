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
| Implementador y Revisor QA | Código, pruebas ejecutadas, dictamen y evidencia de correcciones cuando corresponda. | Pendiente de recepción. |
| Jorge | Matriz de criterio a prueba y revisión independiente de resultados. | Pendiente de recepción. |

Las filas de esta tabla se actualizan cuando llega un archivo verificable. Registrar el detalle del intercambio en [traspasos](trabajo/README.md) y el commit o referencia de la versión recibida.

## Corridas y controles humanos

| Registro | Estado | Destino de la evidencia |
| --- | --- | --- |
| Corrida multiagente | Sin ejecución registrada. | [Evidencia multiagente](evidencia/README.md) |
| Comparación con un agente | Sin ejecución registrada. | [Línea base](linea-base/README.md) |
| Aprobación humana de la especificación | Aprobado — Control Humano 1 (2026-11-22, Jorge). Fase de planificación desbloqueada; listo para commit humano independiente. | [001-requisitos-a-planificador.md](trabajo/001-requisitos-a-planificador.md) · [01-requisitos.md](../specs/01-requisitos.md) |
| Control humano del plan | Aprobado con observaciones — Control Humano 2 (2026-11-22, responsable técnico humano). Correcciones documentales aplicadas; listo para commit humano previo a implementación. | [002-planificador-a-implementador.md](trabajo/002-planificador-a-implementador.md) · [02-plan.md](../specs/02-plan.md) · [03-trazabilidad.md](../specs/03-trazabilidad.md) |
| Fallas, cambios y reejecuciones | Sin observaciones de corrida registradas. | Cuando ocurra una falla, registrar el síntoma, la fuente, su posible causa, el cambio y la verificación posterior. |
| Etiqueta de entrega | Pendiente de confirmación y de un commit final validado. | [Control de commits y etiqueta](decision.md#control-de-commits-y-etiqueta) |

Al incorporar una ejecución, anotar el ID y modalidad de la corrida, fecha y hora, commit inicial, herramienta y modelo, prompt, agente, skill efectivamente usada, entrada y salida, veredicto o resultado y enlaces a la evidencia. Para pruebas, incluir comando, código de salida y conteos reales. Para una decisión humana, incluir quién decidió, qué revisó, el veredicto y su referencia.

## Registro de Control Humano 1

- **Fecha de registro:** 2026-11-22
- **Quién decidió:** Jorge (representante del cliente)
- **Qué revisó:** [specs/01-requisitos.md](../specs/01-requisitos.md), `MAN-INC` v2, `CAT-ERR` v2, `GUI-COL` v1, `POL-ACC` v1, los 10 casos del Excel (`C-031` a `C-040`) y los 14 escenarios sintéticos, incluida la protección frente a instrucciones maliciosas en `L-009`.
- **Veredicto:** **Aprobado — Control Humano 1** (autoriza `specs/01-requisitos.md` tal como está y el paso al agente `planificador`; ratifica `E-512` con máximo 1 reproceso y `casos.reprocesos_realizados` global por caso incluyendo supuesto conservador para mixtos, máximo 3 para `E-207`/`E-305`, e interpretación sobre validaciones/facturación como supuesto del prototipo respaldado por esta aprobación; confirma códigos HTTP `200`/`403`/`404`/`422` y errores estándar `{"detail": "..."}` separados del contrato de cuatro campos).
- **Evidencia:** Aprobación escrita por WhatsApp proporcionada por el equipo.
- **Referencias:** [01-requisitos.md](../specs/01-requisitos.md#L295-L305) · [001-requisitos-a-planificador.md](trabajo/001-requisitos-a-planificador.md#L50-L70)
- **Efecto:** Desbloquea la fase de planificación (`planificador`), pendiente del commit humano independiente de aprobación de especificación.

## Ejecución Fase 2 · Planificador

- **Fecha y hora (Chile):** 2026-11-22 (inicio 17:04, término 17:08)
- **Commit inicial:** `0e47c1c`
- **Herramienta y modalidad:** Antigravity (`agy 1.5.14`, Orchestrator Neon) vía `invoke_subagent` (`planificador`, `conversationId: a80ad08c-9d33-4a06-b0e2-418174f2e7fb`)
- **Skills utilizadas:** `trazabilidad` (`.agents/skills/trazabilidad/SKILL.md`), `especificacion` y referencia de comandos de `ejecucion-pruebas`
- **Entradas:** [01-requisitos.md](../specs/01-requisitos.md), [001-requisitos-a-planificador.md](trabajo/001-requisitos-a-planificador.md), [AGENTS.md](../AGENTS.md), [decision.md](decision.md) y [verificar_trazabilidad.py](../.agents/skills/trazabilidad/scripts/verificar_trazabilidad.py)
- **Salidas generadas:** [02-plan.md](../specs/02-plan.md), [03-trazabilidad.md](../specs/03-trazabilidad.md) y [002-planificador-a-implementador.md](trabajo/002-planificador-a-implementador.md)
- **Verificación ejecutada:** `python3 .agents/skills/trazabilidad/scripts/verificar_trazabilidad.py --check-kit --matrix specs/03-trazabilidad.md` → código de salida `0` (`[OK]` integridad del kit y matriz válida; pruebas funcionales aún no ejecutadas)
- **Tokens / costo:** No informado por la herramienta (sin métricas inventadas)
- **Estado:** Cerrado con **Control Humano 2 aprobado con observaciones** el 2026-11-22 (pruebas pendientes de ejecución en Fase 3)

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
- **Efecto:** Planificación aprobada; habilita el paso al agente `implementador` tras el commit humano de Control Humano 2.
