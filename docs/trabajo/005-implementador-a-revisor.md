# Traspaso 005: implementador -> revisor

- **Fecha:** 2026-11-22 20:43
- **Fase:** implementacion
- **Agente origen:** implementador
- **conversationId del Implementador:** `939546ea-7d84-4a46-878a-ae5960676b77`
- **Agente destino:** revisor
- **Iteración de corrección:** 1/2
- **Commit de referencia base:** `2c88947`
- **Dictamen de origen atendido:** `docs/trabajo/004-revisor-a-implementador.md` (`APROBADO CON OBSERVACIONES` · decisión humana `SOLICITAR CORRECCIONES — RONDA 1/2 ABIERTA`)
- **Control humano requerido:** registro humano de dictamen
- **Artefactos de entrada:**
  - `docs/trabajo/004-revisor-a-implementador.md`
  - `AGENTS.md`
  - `specs/01-requisitos.md` (`Aprobado — Control Humano 1`)
  - `specs/02-plan.md` (`Aprobado con observaciones — Control Humano 2`)
  - `specs/03-trazabilidad.md`
  - `.agents/skills/ejecucion-pruebas/SKILL.md`
  - `.agents/skills/trazabilidad/SKILL.md`
  - `docs/trabajo/README.md`
  - `src/mira_reproceso/rules.py`
  - `src/mira_reproceso/loader.py`
  - `tests/test_rules.py`
  - `tests/test_api.py`
- **Artefactos producidos/actualizados:**
  - `src/mira_reproceso/rules.py` (modificado — corrección `H-02`)
  - `tests/test_rules.py` (modificado — corrección `H-01` y prueba de regresión `H-02`)
  - `tests/test_api.py` (modificado — corrección `H-01`, verificación explícita `HTTP 422` de campo extra `"registro_tecnico"` y prueba HTTP de regresión `H-02`)
  - `specs/03-trazabilidad.md` (modificado — actualización de filas `RN-*` y separación explícita de evidencias iteración `0/2` vs `1/2`)
  - `docs/evidencia/pytest-iter1.log` (creado — log de ejecución de ronda `1/2`, conservando intacto `docs/evidencia/pytest-iter0.log`)
  - `docs/trabajo/005-implementador-a-revisor.md` (creado — presente acta)
- **Verificaciones ejecutadas:**
  1. `bash -o pipefail -c './.agents/skills/ejecucion-pruebas/scripts/run_tests.sh 2>&1 | tee docs/evidencia/pytest-iter1.log'` → código de salida `0`:
     - Integridad del kit CU-2 (`sha256sum -c docs/kit-sha256sums.txt`): **7 de 7 archivos `OK`**.
     - Resultado completo de `pytest -p no:cacheprovider -v`: **`48 passed, 0 failed, 0 skipped, 1 warning in 1.14s`** (`27` ítems en `tests/test_api.py` + `21` ítems en `tests/test_rules.py`), sin `__pycache__` ni `.pytest_cache`.
  2. `PYTHONDONTWRITEBYTECODE=1 python3 .agents/skills/trazabilidad/scripts/verificar_trazabilidad.py --check-kit --matrix specs/03-trazabilidad.md` → código de salida `0`:
     - `[OK] Integridad del kit CU-2 verificada contra docs/kit-sha256sums.txt.`
     - `[OK] Matriz de trazabilidad válida: /home/lester/Documents/entrega4-mira-multiagente/specs/03-trazabilidad.md`
- **Resumen y puntos abiertos:**
  - Se aplicaron exclusivamente las correcciones acotadas para **`H-01`** (`Media`) y **`H-02`** (`Baja`) conforme al dictamen y autorización humana de ronda `1/2` en `docs/trabajo/004-revisor-a-implementador.md`, sin agregar alcance fuera de especificación ni modificar archivos intocables (`specs/01-requisitos.md`, `specs/02-plan.md`, `kit/CU-2_soporte_operacion/`, `docs/evidencia/pytest-iter0.log`, `docs/trabajo/001..004`, `docs/bitacora.md`).
  - Pendiente la auditoría independiente de solo lectura del agente `revisor` sobre la ronda `1/2` y el registro humano del dictamen resultante.

---

## Detalle de correcciones aplicadas (ronda `1/2`)

### 1. Hallazgo `H-01` (`Media`) — Pruebas reales de ingestión hostil para `SYN-INJ-OK` y rechazo `422`

- **`tests/test_rules.py`:**
  - Se eliminaron por completo la variable local desconectada `registro_tecnico_hostil` y la aserción tautológica `assert "SYN-INJ-OK" in registro_tecnico_hostil`.
  - Se incorporó el helper local `_crear_excel_sintetico_con_inyeccion(ruta_excel: Path)` usando `openpyxl.Workbook()` con los encabezados exactos esperados por `cargar_datos_excel()` (`usuarios`, `servicios`, `casos` con el caso elegible `SYN-INJ-OK`, más hoja `registro_tecnico` con contenido hostil que incluye `"ORG-02"`, `"puede_reprocesar=false"` e `"INYECCION_HOSTIL_SYN_TEST"`).
  - `test_sintetico_prompt_injection_ignorado_syn_inj_ok(tmp_path: Path)` genera el `.xlsx` temporal en `tmp_path`, verifica que el SHA-256 del Excel oficial del kit no varía, lo carga con `cargar_datos_excel(ruta_temporal)`, verifica que ni `DatosOperativos` ni `Caso` exponen atributo `registro_tecnico`, confirma que ninguno de los marcadores hostiles aparece en `repr(datos)` ni en `repr(datos.casos["SYN-INJ-OK"])`, evalúa mediante `evaluar_elegibilidad(datos, "SYN-INJ-OK", "U-S1")` y valida `puede_reprocesar is True`, `accion_recomendada == "Proceder con el reprocesamiento."`, citas normativas vigentes (`"MAN-INC v2 §4"`, `"CAT-ERR v2 §1 (E-305)"`, `"GUI-COL v1 §1"`) y ausencia total de marcadores hostiles en la salida.
- **`tests/test_api.py`:**
  - Se eliminaron por completo la variable local `_registro_hostil_ignorado` y la aserción tautológica `assert _registro_hostil_ignorado`.
  - `test_http_resistencia_prompt_injection_c038_y_syn_inj_ok(tmp_path: Path)` conserva intacta la comprobación real de `C-038`/`L-009` sobre `DEFAULT_EXCEL_PATH` (con SHA-256 antes/después) y sustituye el bloque sintético por un libro `.xlsx` temporal en `tmp_path` con `registro_tecnico` hostil, cargado mediante `cargar_datos_excel(ruta_temporal)`, verificando ausencia de `registro_tecnico` y marcadores hostiles en `repr(datos_sint)`, levantando `TestClient(create_app(datos=datos_sint))`, enviando `POST /reprocesamiento/evaluar` con `{"caso_id": "SYN-INJ-OK", "usuario_id": "U-S1"}` y validando `HTTP 200`, `_validar_contrato_200`, `puede_reprocesar is True`, `accion_recomendada == "Proceder con el reprocesamiento."`, referencias normativas vigentes y ausencia de `"ORG-02"`, `"puede_reprocesar=false"` e `"INYECCION_HOSTIL_SYN_TEST"` en la respuesta JSON.
  - En `test_http_422_validacion_estricta_syn_422()` se añadió la verificación explícita `HTTP 422` enviando el campo adicional `"registro_tecnico"` en el JSON de `POST /reprocesamiento/evaluar` (`status_code == 422` y `"puede_reprocesar" not in resp.json()`).

### 2. Hallazgo `H-02` (`Baja`) — Recomendación precisa para `E-207` cuando `SRV-MOD` está `operativo` y falla otro `servicio_dependiente`

- **`src/mira_reproceso/rules.py`:**
  - En `evaluar_elegibilidad()`, `servicio_no_operativo_e207` se activa **únicamente** cuando `SRV-MOD` (`SERVICIO_MODELOS_ID`) no está `"operativo"` (tanto si `servicio_dep.servicio_id == SERVICIO_MODELOS_ID` como cuando `servicio_dep_id != SERVICIO_MODELOS_ID` y `SRV-MOD` falla).
  - Cuando `codigo_error == "E-207"`, `SRV-MOD` está `"operativo"`, y falla un `servicio_dependiente` distinto (`servicio_dep.servicio_id != SERVICIO_MODELOS_ID`), no se activa `servicio_no_operativo_e207`: se activa `servicio_no_operativo_otro = True` y se pasa `servicio_no_operativo_e207_otro_id = servicio_dep.servicio_id` a `_seleccionar_accion_bloqueo()`.
  - En `_seleccionar_accion_bloqueo()`, manteniendo intacta la precedencia normativa determinista (donde `servicio_no_operativo_e207` sigue teniendo prioridad si `SRV-MOD` también falla), cuando solo bloquea ese otro servicio dependiente retorna:
    `f"No reprocesar; esperar a que el servicio dependiente '{servicio_no_operativo_e207_otro_id}' vuelva a estar operativo."`
    sin mencionar `SRV-MOD`, y conservando para códigos distintos de `E-207` (`E-305`/`C-040`) el mensaje existente `"No reprocesar; esperar a que el servicio dependiente vuelva a estar operativo."`.
- **`tests/test_rules.py`:**
  - En `test_sinteticos_e207_dependiente_distinto_de_srv_mod()` se reforzó la verificación de que `SYN-E207-DEP-API` sigue recomendando esperar a `SRV-MOD`.
  - Se añadió `test_regresion_h02_e207_srv_mod_operativo_y_otro_dependiente_no_operativo()` verificando: (a) `E-207` con `SRV-MOD` `"operativo"` y `SRV-REG` `"caido"` → `puede_reprocesar is False`, `"SRV-REG"` y `"caido"` en `motivos`, `"SRV-REG"` en `accion_recomendada`, `"SRV-MOD"` ausente de `accion_recomendada` y `motivos`, y citas `"MAN-INC v2 §4"`, `"GUI-COL v1 §1"`, `"CAT-ERR v2 §1 (E-207)"`; y (b) si `SRV-MOD` también pasa a `"degradado"`, `SRV-MOD` conserva prioridad en `accion_recomendada`.
- **`tests/test_api.py`:**
  - Se añadió `test_http_regresion_h02_e207_srv_mod_operativo_y_otro_no_operativo()` verificando el mismo escenario de regresión `H-02` a través de `POST /reprocesamiento/evaluar` (`HTTP 200`, contrato estricto de 4 campos).

---

## Evidencia separada por iteración y uso de skills

- **Iteración `0/2` (línea base intacta en `docs/evidencia/pytest-iter0.log`):**
  - `46 passed, 0 failed, 0 skipped, 1 warning in 1.09s` (`26` ítems en `tests/test_api.py` + `20` ítems en `tests/test_rules.py`), con `7/7` checksums `OK`.
- **Iteración `1/2` (evidencia actual en `docs/evidencia/pytest-iter1.log`):**
  - Skill `ejecucion-pruebas`:
    - Comando: `bash -o pipefail -c './.agents/skills/ejecucion-pruebas/scripts/run_tests.sh 2>&1 | tee docs/evidencia/pytest-iter1.log'`
    - Checksums (`docs/kit-sha256sums.txt`): **`7/7` archivos `OK`**.
    - Conteo `pytest -p no:cacheprovider -v`: **`48 passed, 0 failed, 0 skipped, 1 warning in 1.14s`** (`27` ítems en `tests/test_api.py` + `21` ítems en `tests/test_rules.py`).
    - Advertencia mantenida: `StarletteDeprecationWarning` de `fastapi/testclient.py` sobre `httpx`/`httpx2`.
  - Skill `trazabilidad`:
    - Actualizada `specs/03-trazabilidad.md` sin referencias prohibidas a la versión derogada v1 y con evidencias `0/2` y `1/2` separadas.
    - Comando: `PYTHONDONTWRITEBYTECODE=1 python3 .agents/skills/trazabilidad/scripts/verificar_trazabilidad.py --check-kit --matrix specs/03-trazabilidad.md` → salida `0` (`[OK]` kit y matriz).
