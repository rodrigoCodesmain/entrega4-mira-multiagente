# Traspaso 002: planificador -> implementador

- **Fecha:** 2026-11-22 17:08
- **Fase:** planificacion
- **Agente origen:** planificador
- **Agente destino:** implementador
- **Iteración de corrección:** 0/2
- **Control humano requerido:** Control Humano 2 (plan)
- **Estado de aprobación humana:** Aprobado con observaciones — Control Humano 2 (2026-11-22, responsable técnico humano)
- **Artefactos de entrada:**
  - `specs/01-requisitos.md` (`Aprobado — Control Humano 1`)
  - `docs/trabajo/001-requisitos-a-planificador.md`
  - `AGENTS.md`
  - `docs/decision.md`
  - `.agents/skills/especificacion/SKILL.md`
  - `.agents/skills/trazabilidad/SKILL.md`
  - `.agents/skills/trazabilidad/scripts/verificar_trazabilidad.py`
  - `.agents/skills/ejecucion-pruebas/SKILL.md`
  - `docs/trabajo/README.md`
  - `kit/CU-2_soporte_operacion/corpus/MAN-INC_manual_incidentes.md`
  - `kit/CU-2_soporte_operacion/corpus/CAT-ERR_v2_vigente.md`
  - `kit/CU-2_soporte_operacion/corpus/GUI-COL_colas_servicios_externos.md`
  - `kit/CU-2_soporte_operacion/corpus/POL-ACC_acceso_evidencia.md`
  - `docs/kit-sha256sums.txt`
- **Artefactos producidos/actualizados:**
  - `specs/02-plan.md`
  - `specs/03-trazabilidad.md`
  - `docs/trabajo/002-planificador-a-implementador.md`
- **Verificaciones ejecutadas:** El agente `planificador` no posee `run_command` por diseño y no creó ni modificó `src/`, `tests/`, `pyproject.toml` ni `kit/`. Tras la entrega y tras incorporar las observaciones de Control Humano 2, se ejecutó desde la raíz del repositorio `python3 .agents/skills/trazabilidad/scripts/verificar_trazabilidad.py --check-kit --matrix specs/03-trazabilidad.md` (código de salida `0`: `[OK] Integridad del kit CU-2 verificada contra docs/kit-sha256sums.txt.` y `[OK] Matriz de trazabilidad válida: .../specs/03-trazabilidad.md`). Planificación **aprobada con observaciones en Control Humano 2** (pruebas aún pendientes de ejecución en Fase 3).
- **Resumen y puntos abiertos:**
  - Se diseñó la arquitectura mínima Python + FastAPI + `pytest` en `src/mira_reproceso/{__init__,models,loader,rules,api}.py` y `pyproject.toml` mínimo (`fastapi`, `uvicorn`, `openpyxl`; grupo `dev`: `pytest`, `httpx`), respetando estrictamente todas las exclusiones de alcance y el contrato aprobado en Control Humano 1.
  - Se separó el motor determinista puro (`rules.py` sobre dataclasses en `models.py`) del endpoint `POST /reprocesamiento/evaluar` (`api.py`), garantizando evaluación prioritaria simulada de rol (`403` sin consultar ni exponer `caso_id`), `404` ante caso inexistente, `422` ante payloads inválidos o vacíos, y `200` con exactamente 4 campos acumulando todos los impedimentos concurrentes.
  - Se fijó lectura exclusiva en solo lectura de `CU-2_datos.xlsx` (`usuarios`, `servicios`, `casos`) excluyendo estructuralmente `registro_tecnico` (`L-009`), manteniendo vigente el límite provisional de `1` reproceso global para `E-512` (`REQ-16`) y `3` para `E-207`/`E-305` (`REQ-08`).
  - Se detallaron las tareas `T-01..T-08`, la estrategia de pruebas distribuida entre `tests/test_rules.py` (10 casos del Excel `C-031..C-040` + 13 escenarios sintéticos de dominio `SYN-*` + `EX-04`/`EX-05`) y `tests/test_api.py` (`SYN-422` en validación HTTP + integración HTTP de `200`/`403`/`404`/`422` y seguridad `L-009`), y la generación de evidencia reproducible en `docs/evidencia/` mediante `run_tests.sh`.

## Decisiones clave del diseño y puntos de revisión para Control Humano 2

1. **Separación pura de dominio (`models.py` + `rules.py`) respecto de FastAPI (`api.py`) y Excel (`loader.py`):** permite probar determinísticamente `C-031..C-040` y los 13 `SYN-*` de dominio en `tests/test_rules.py` sin I/O ni servidor HTTP, dejando `SYN-422` y la verificación HTTP completa en `tests/test_api.py`.
2. **Inyección de datos en `create_app(datos: DatosOperativos | None = None)`:** cuando `datos` es `None`, carga `CU-2_datos.xlsx` bajo demanda en modo solo lectura; en pruebas sintéticas acepta `DatosOperativos` en memoria sin tocar `kit/`.
3. **Precedencia determinista de `accion_recomendada` ante bloqueos concurrentes (`EX-04`):** decisión final > inconsistencia `EX-05` > código no reprocesable en `CAT-ERR` v2 > límite de reprocesos > servicio no operativo > estado no elegible, mientras `motivos` reporta la totalidad de impedimentos detectados.
4. **Aclaración explícita sobre roles simulados:** la validación de `usuario_id` en `usuarios` es simulada y no constituye autenticación real.
5. **Estrategia de evidencia para el `revisor`:** al carecer de `run_command`, el `revisor` auditará el log generado por `run_tests.sh` en `docs/evidencia/pytest-iter0.log`.

## Evidencia de uso de skill

1. **Aplicación de `.agents/skills/trazabilidad/SKILL.md` y `.agents/skills/trazabilidad/scripts/verificar_trazabilidad.py`:**
   - Se leyó íntegramente `SKILL.md` y la lógica de validación de `verificar_trazabilidad.py` antes de redactar `specs/03-trazabilidad.md`.
   - La primera tabla Markdown de `specs/03-trazabilidad.md` incluye exactamente los 6 encabezados requeridos por `REQUIRED_HEADERS` (`ID Regla`, `Documento Vigente y Sección`, `ID Requisito`, `Componente / Función`, `Caso de Prueba`, `Estado`), complementados con `Tarea` y `Criterio de Aceptación`.
   - Se evitó estrictamente incluir cadenas coincidentes con `FORBIDDEN_ACTIVE_PATTERNS` dentro de todas las filas de tabla (`| ... |`); en particular, para `REQ-02` se registró `"Solo MAN-INC v2 y CAT-ERR v2 vigentes (catálogo anterior derogado excluido)"`.
   - Se cubrieron los 18 requisitos (`REQ-01..REQ-18`), las 8 tareas (`T-01..T-08`), los 10 criterios (`CA-01..CA-10`), los 10 casos del Excel (`C-031..C-040`) y los 14 escenarios sintéticos (`SYN-*`: 13 de dominio en `tests/test_rules.py` y `SYN-422` de validación HTTP en `tests/test_api.py`), manteniendo todas las filas en estado **`Planificado (no ejecutado)`**.
   - Por diseño del rol, `planificador` no dispone de `run_command`; la verificación ejecutada posteriormente por el orquestador con `python3 .agents/skills/trazabilidad/scripts/verificar_trazabilidad.py --check-kit --matrix specs/03-trazabilidad.md` finalizó con código `0` (kit intacto y matriz válida).
2. **Aplicación de `.agents/skills/especificacion/SKILL.md` y alineación con `.agents/skills/ejecucion-pruebas/SKILL.md`:**
   - Se mantuvo exclusión estricta de la versión 1 derogada del catálogo, respeto de la aclaración ratificada de `E-512` (`1` reproceso global en `casos.reprocesos_realizados`), tratamiento pasivo/excluido de `registro_tecnico` (`L-009` en `C-038`) y ejecución reproducible mediante `./.agents/skills/ejecucion-pruebas/scripts/run_tests.sh` (sin bytecode ni cachés).

## Registro de Control Humano 2 (Aprobado con observaciones)

- **Estado:** `Aprobado con observaciones — Control Humano 2`
- **Responsable de revisión:** Responsable técnico humano *(revisión y aprobación realizadas por una persona, no por el agente)*
- **Fecha de revisión:** `2026-11-22`
- **Decisión:** `[ ] Aprobado` / `[x] Aprobado con observaciones` / `[ ] Requiere ajustes`
- **Evidencia:** Revisión y aprobación humana directa del responsable técnico sobre `specs/02-plan.md`, `specs/03-trazabilidad.md` y `docs/trabajo/002-planificador-a-implementador.md` (decisión emitida por una persona, no por el agente).
- **Observaciones documentales obligatorias incorporadas:**
  1. **Coherencia entre conjunto y mapa de reglas `CAT-ERR` v2:** se mantuvo `CATALOGO_CAT_ERR_V2` (`frozenset`) exclusivamente para validar pertenencia y se definió `REGLAS_CAT_ERR_V2` (`dict`) como estructura independiente por código en `specs/02-plan.md` y en las filas `RN-09..RN-16` de `specs/03-trazabilidad.md`.
  2. **Distribución explícita de los 14 escenarios sintéticos:** se precisó que 13 escenarios sintéticos de dominio residen en `tests/test_rules.py` y que `SYN-422` pertenece a las pruebas de validación HTTP en `tests/test_api.py` (junto con integración HTTP sobre `SYN-ROL-COM`, `SYN-NO-USER`, `SYN-NO-CASE`, `SYN-INJ-OK` y casos del Excel).
- **Lista de verificación aprobada en Control Humano 2:**
  - `[x]` Arquitectura mínima `src/mira_reproceso/{__init__,models,loader,rules,api}.py` y `pyproject.toml` sin alcance extra ni alertas automáticas S2.
  - `[x]` Motor determinista en `rules.py` separado de FastAPI, con validación prioritaria simulada de rol (`403` sin fuga de caso) y acumulación de todos los impedimentos concurrentes (`200`), manteniendo separados `CATALOGO_CAT_ERR_V2` y `REGLAS_CAT_ERR_V2`.
  - `[x]` Precedencia determinista de `accion_recomendada` en `EX-04` y tratamiento seguro de inconsistencias `EX-05`.
  - `[x]` Carga de solo lectura en `loader.py` (`openpyxl(..., read_only=True, data_only=True)`) excluyendo estructuralmente `registro_tecnico` (`L-009`).
  - `[x]` Plan ordenado de tareas `T-01..T-08`, cobertura distribuida entre `tests/test_rules.py` (`C-031..C-040` + 13 `SYN-*` de dominio) y `tests/test_api.py` (`SYN-422` + integración HTTP) y estrategia de evidencia en `docs/evidencia/` para el agente `revisor`.
  - `[x]` Validación externa ejecutada con éxito sobre la matriz corregida: `python3 .agents/skills/trazabilidad/scripts/verificar_trazabilidad.py --check-kit --matrix specs/03-trazabilidad.md` (código de salida `0`).

> **Compuerta de Control Humano 2:** Planificación **aprobada con observaciones** el `2026-11-22` por una persona (responsable técnico humano). Todas las pruebas siguen pendientes de ejecución hasta la Fase 3 (`implementador`), la cual queda habilitada tras registrar el commit humano de Control Humano 2.
