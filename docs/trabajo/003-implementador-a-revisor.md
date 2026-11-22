# Traspaso 003: implementador -> revisor

- **Fecha:** 2026-11-22 19:29
- **Fase:** implementacion
- **Agente origen:** implementador (`invoke_subagent`, `conversationId: 30625f4b-c3db-4582-8621-966a1524504a`)
- **Agente destino:** revisor
- **Iteración de corrección:** 0/2
- **Control humano requerido:** registro humano de dictamen
- **Artefactos de entrada:**
  - `specs/01-requisitos.md` (`Aprobado — Control Humano 1`)
  - `specs/02-plan.md` (`Aprobado con observaciones — Control Humano 2`)
  - `specs/03-trazabilidad.md`
  - `docs/trabajo/002-planificador-a-implementador.md`
  - `AGENTS.md`
  - `.agents/skills/ejecucion-pruebas/SKILL.md`
  - `.agents/skills/trazabilidad/SKILL.md`
  - `docs/trabajo/README.md`
  - `kit/CU-2_soporte_operacion/corpus/MAN-INC_manual_incidentes.md`
  - `kit/CU-2_soporte_operacion/corpus/CAT-ERR_v2_vigente.md`
  - `kit/CU-2_soporte_operacion/corpus/GUI-COL_colas_servicios_externos.md`
  - `kit/CU-2_soporte_operacion/datos/CU-2_datos.xlsx` (solo lectura)
- **Artefactos producidos/actualizados:**
  - `pyproject.toml`
  - `src/mira_reproceso/__init__.py`
  - `src/mira_reproceso/models.py`
  - `src/mira_reproceso/loader.py`
  - `src/mira_reproceso/rules.py`
  - `src/mira_reproceso/api.py`
  - `tests/test_rules.py`
  - `tests/test_api.py`
  - `docs/evidencia/pytest-iter0.log`
  - `specs/03-trazabilidad.md`
  - `docs/trabajo/003-implementador-a-revisor.md`
- **Verificaciones ejecutadas:**
  1. `uv venv .venv && uv pip install --python .venv/bin/python -e ".[dev]"` → código de salida `0` (`CPython 3.12.14`, 25 paquetes instalados incluyendo `fastapi==0.165.0`, `uvicorn==0.54.0`, `openpyxl==3.1.5`, `pytest==9.2.0`, `httpx==0.28.1` y `mira-reproceso==0.1.0` editable).
  2. `bash -o pipefail -c './.agents/skills/ejecucion-pruebas/scripts/run_tests.sh 2>&1 | tee docs/evidencia/pytest-iter0.log'` → código de salida `0`:
     - Integridad del kit CU-2 (`sha256sum -c docs/kit-sha256sums.txt`): **7 de 7 archivos `OK`** (`CAT-ERR_v1_derogado.md`, `CAT-ERR_v2_vigente.md`, `GUI-COL_colas_servicios_externos.md`, `MAN-INC_manual_incidentes.md`, `POL-ACC_acceso_evidencia.md`, `PRO-MAN_mantencion.md`, `CU-2_datos.xlsx`).
     - Resultado completo de `pytest -p no:cacheprovider -v`: **`46 passed, 0 failed, 0 skipped, 1 warning in 1.09s`** (sin escribir bytecode `__pycache__` ni `.pytest_cache`).
  3. `PYTHONDONTWRITEBYTECODE=1 python3 .agents/skills/trazabilidad/scripts/verificar_trazabilidad.py --check-kit --matrix specs/03-trazabilidad.md` → código de salida `0`:
     - `[OK] Integridad del kit CU-2 verificada contra docs/kit-sha256sums.txt.`
     - `[OK] Matriz de trazabilidad válida: /home/lester/Documents/entrega4-mira-multiagente/specs/03-trazabilidad.md`
- **Resumen y puntos abiertos:**
  - Se completaron todas las tareas `T-01..T-08` conforme a `specs/01-requisitos.md` y `specs/02-plan.md`, sin ampliar alcance ni agregar alertas S2, frontend, RAG, MCP, notificaciones ni ejecución real de reprocesos.
  - Se mantuvo estrictamente la vigencia de `MAN-INC` v2, `CAT-ERR` v2 y `GUI-COL` v1 (auxiliar de servicios), excluyendo por completo el catálogo derogado.
  - Pendiente únicamente la auditoría independiente de solo lectura por el agente `revisor` sobre este código, pruebas, trazabilidad y el log `docs/evidencia/pytest-iter0.log`, y el registro humano del dictamen en `docs/trabajo/`.

## Tareas completadas (`T-01..T-08`)

1. **`T-01` (Configuración mínima del paquete):** Se crearon `pyproject.toml` (`setuptools`, layout `src/`, `requires-python = ">=3.11"`, dependencias `fastapi`, `uvicorn`, `openpyxl` y grupo `dev` con `pytest`, `httpx`) y `src/mira_reproceso/__init__.py`, instalando `.venv` en modo editable.
2. **`T-02` (Modelos y cargador solo lectura):** Se inspeccionaron en solo lectura los encabezados y filas reales de `usuarios`, `servicios` y `casos` en `kit/CU-2_soporte_operacion/datos/CU-2_datos.xlsx`. Se implementaron dataclasses inmutables y excepciones puras en `src/mira_reproceso/models.py` (sin `registro_tecnico`) y `cargar_datos_excel()` / `normalizar_decision_final()` en `src/mira_reproceso/loader.py` usando `openpyxl.load_workbook(..., read_only=True, data_only=True)` con cierre garantizado `finally: wb.close()`, omitiendo por completo `registro_tecnico`.
3. **`T-03` y `T-04` (Motor determinista puro `src/mira_reproceso/rules.py`):** Sin importar `fastapi`, `pydantic` ni `openpyxl`. Define `ROLES_AUTORIZADOS`, `ESTADOS_ELEGIBLES`, `CATALOGO_CAT_ERR_V2` (`frozenset` exclusivo para pertenencia), `REGLAS_CAT_ERR_V2` (`dict` independiente por código), `LIMITE_GENERAL_REPROCESOS = 3` y `LIMITE_E512 = 1`. En `evaluar_elegibilidad()`: Paso 1 (`validar_usuario_autorizado` antes de consultar `casos`), Paso 2 (`obtener_caso`), Paso 3 (acumulación completa de impedimentos concurrentes `EX-04` e inconsistencias `EX-05`) y Paso 4 (precedencia determinista de `accion_recomendada` y citas exclusivas a normas vigentes).
4. **`T-05` (Endpoint FastAPI y contratos HTTP `src/mira_reproceso/api.py`):** Implementa `create_app(datos: DatosOperativos | None = None)`, `app = create_app()`, `get_datos()` con carga perezosa cacheada bajo demanda, `EvaluarRequest` (`ConfigDict(extra="forbid")`, `StrictStr`, `.strip()` y rechazo de vacíos/espacios), `EvaluarResponse` (`ConfigDict(extra="forbid")`, exactamente `{puede_reprocesar, motivos, accion_recomendada, referencias_normativas}`) y `POST /reprocesamiento/evaluar` mapeando `200`, `403` uniforme sin fuga de caso, `404` y `422`.
5. **`T-06` (`tests/test_rules.py`):** Cubre pureza de imports de `rules.py`, lectura intacta de `CU-2_datos.xlsx` sin `registro_tecnico`, normalización de `tiene_decision_final`, los 10 casos reales `C-031..C-040`, los 13 escenarios sintéticos de dominio (`SYN-E102`, `SYN-E512-0`, `SYN-E512-1`, `SYN-E207-OK`, `SYN-DET-OK`, `SYN-LIMIT-2`, `SYN-LIMIT-3`, `SYN-DECFIN`, `SYN-ROL-COM`, `SYN-ROL-N2-ING`, `SYN-NO-USER`, `SYN-NO-CASE`, `SYN-INJ-OK`), `E-207` con servicio dependiente distinto de `SRV-MOD`, `EX-04` y `EX-05`.
6. **`T-07` (`tests/test_api.py`):** Cubre vía `TestClient` respuestas `HTTP 200` (4 claves exactas, tipos, sin alertas S2 ni citas derogadas en `C-031..C-040` y sintéticos), `HTTP 403` idéntico sin fuga en `SYN-ROL-COM` y `SYN-NO-USER` sobre `C-032` y `C-999`, `HTTP 404` (`SYN-NO-CASE`), `HTTP 422` (`SYN-422`: JSON malformado, faltantes, extras, tipos inválidos, vacíos/espacios y recorte de espacios válidos) y resistencia a *prompt injection* (`C-038` con `L-009` en Excel intacto y `SYN-INJ-OK`).
7. **`T-08` (Evidencia, trazabilidad y entrega):** Se ejecutó `run_tests.sh` guardando la salida real en `docs/evidencia/pytest-iter0.log`, se actualizó `specs/03-trazabilidad.md` con componentes, funciones y pruebas ejecutadas, se validó la matriz y checksums con `verificar_trazabilidad.py` y se emitió la presente acta.

## Cobertura verificada (10 casos reales + 14 sintéticos + excepciones)

- **Casos reales del Excel (`CU-2_datos.xlsx`, 10/10):** `C-031`, `C-032`, `C-033`, `C-034`, `C-035`, `C-036`, `C-037`, `C-038`, `C-039`, `C-040` (verificados en `tests/test_rules.py` y `tests/test_api.py`).
- **Escenarios sintéticos en memoria (`SYN-*`, 14/14):**
  - 13 de dominio en `tests/test_rules.py` (10 de ellos además ejercitados vía HTTP en `tests/test_api.py`): `SYN-E102`, `SYN-E512-0`, `SYN-E512-1`, `SYN-E207-OK`, `SYN-DET-OK`, `SYN-LIMIT-2`, `SYN-LIMIT-3`, `SYN-DECFIN`, `SYN-ROL-COM`, `SYN-ROL-N2-ING`, `SYN-NO-USER`, `SYN-NO-CASE`, `SYN-INJ-OK`.
  - 1 de validación HTTP en `tests/test_api.py`: `SYN-422`.
- **Excepciones concurrentes e inconsistencias:** `EX-04` (acumulación de hasta 5 impedimentos con precedencia determinista de acción) y `EX-05` (código fuera de `CAT-ERR` v2, `servicio_dependiente` ausente y `SRV-MOD` faltante en `E-207`).

## Evidencia de uso de skills

1. **Skill `ejecucion-pruebas` (`.agents/skills/ejecucion-pruebas/SKILL.md`):**
   - Comando exacto ejecutado:
     `bash -o pipefail -c './.agents/skills/ejecucion-pruebas/scripts/run_tests.sh 2>&1 | tee docs/evidencia/pytest-iter0.log'`
   - Verificación de checksums del kit (`docs/kit-sha256sums.txt`): **7/7 archivos `OK`** sin modificaciones.
   - Conteo exacto reportado por `pytest`: **`46 passed, 0 failed, 0 skipped, 1 warning in 1.09s`**, sin generación de `__pycache__` ni `.pytest_cache`.
2. **Skill `trazabilidad` (`.agents/skills/trazabilidad/SKILL.md`):**
   - Matriz `specs/03-trazabilidad.md` actualizada manteniendo los 6 encabezados obligatorios, sin referencias al catálogo derogado y reflejando únicamente pruebas ejecutadas y aprobadas en `docs/evidencia/pytest-iter0.log`.
   - Verificación automática ejecutada: `PYTHONDONTWRITEBYTECODE=1 python3 .agents/skills/trazabilidad/scripts/verificar_trazabilidad.py --check-kit --matrix specs/03-trazabilidad.md` (código de salida `0`).

## Observaciones y puntos abiertos

- **Supuesto conservador `E-512`:** Se mantiene documentado el límite específico de `1` reproceso sobre `casos.reprocesos_realizados` como contador global por caso, conforme a la ratificación registrada en Control Humano 1 (`specs/01-requisitos.md §7.2`).
- **Advertencia observada en `pytest`:** `StarletteDeprecationWarning` emitida por `fastapi/testclient.py` respecto a la versión de `httpx`/`httpx2`; no afecta la ejecución ni los resultados de las 46 pruebas (`0 failed`, `0 skipped`).
- **Siguiente paso:** Auditoría independiente de solo lectura por el agente `revisor` y registro humano de su dictamen en `docs/trabajo/`.
