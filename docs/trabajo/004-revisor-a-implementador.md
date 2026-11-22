# Traspaso 004 · Revisor a Implementador / Control Humano (Iteración 0/2)

## 1. Metadatos de coordinación (registrados por el orquestador)

- **Fecha:** 2026-11-22
- **Fase:** `revision` (Fase 3 · Auditoría independiente)
- **Iteración auditada:** `0/2`
- **Commit de referencia auditado:** `e26eba3` (`feat: registrar implementacion inicial CU-2 iteracion 0`)
- **Subagente invocado:** `revisor` (`conversationId: e61985ce-c65b-43b1-9a5d-d348800704c4`)
- **Modo de ejecución verificado:** Solo lectura estricta (`read_file`, `send_message`, `list_resources`, `read_resource`, `manage_task`; sin `write_file`, `edit_file`, `run_command` ni MCP heredados)
- **Dictamen emitido:** `APROBADO CON OBSERVACIONES`
- **Estado de decisión humana:** **`SOLICITAR CORRECCIONES — RONDA 1/2 ABIERTA`** (`2026-11-22`, responsable técnico del equipo)
- **Separación de roles (AGENTS.md §5):** De acuerdo con la regla de independencia del revisor, el agente `revisor` no modificó archivos ni ejecutó comandos, entregando su dictamen íntegramente en la conversación. El orquestador crea este archivo exclusivamente para transcribir de forma literal dicho dictamen y habilitar el registro humano posterior, sin alterar el código, las pruebas ni los criterios emitidos.

---

## 2. Dictamen íntegro emitido por el agente `revisor`

> Nota de transcripción: El texto entre las líneas horizontales siguientes reproduce de forma literal y sin modificaciones la salida completa entregada por `revisor` (`e61985ce-c65b-43b1-9a5d-d348800704c4`).

---

# Dictamen de Auditoría Independiente · MIRA CU-2 (Iteración 0/2, ref. `e26eba3`)

## 1. Herramientas declaradas en sesión (confirmación de solo lectura)

- **Herramientas disponibles en sesión:** `read_file`, `send_message`, `list_resources`, `read_resource`, `manage_task`.
- **Herramientas de escritura/ejecución ausentes:** `write_file`, `edit_file`, `run_command` no existen en la sesión; tampoco hay servidores MCP heredados.
- **Modo de operación confirmado:** Solo lectura pura exclusivamente sobre archivos bajo `/home/lester/Documents/entrega4-mira-multiagente/`, contrastando especificación, código fuente, pruebas, actas de traspaso y el log de ejecución generado por el Implementador (`docs/evidencia/pytest-iter0.log`).

---

## 2. Dictamen explícito

- **Dictamen:** `APROBADO CON OBSERVACIONES`
- **Iteración auditada:** `0/2` (sobre commit de referencia `e26eba3`)
- **Hallazgos bloqueantes (`Crítica` / `Alta`):** `0`
- **Hallazgos no bloqueantes verificados:** `2` (`H-01` de severidad `Media`, `H-02` de severidad `Baja`)

---

## 3. Resumen ejecutivo de la auditoría (6 ejes)

### Eje 1 · Conformidad con requisitos (`REQ-01..REQ-18`), criterios (`CA-01..CA-10`) y exclusiones (`AGENTS.md`)
- **Estado:** Conforme (sin hallazgos).
- **Verificación:**
  - `pyproject.toml` (líneas 1-26) define únicamente `fastapi`, `uvicorn` y `openpyxl` (y `pytest`, `httpx` en `[project.optional-dependencies] dev`), con layout `src/` y `requires-python >= 3.11`.
  - `src/mira_reproceso/api.py` expone un único endpoint `POST /reprocesamiento/evaluar` (líneas 68-103) con entrada `EvaluarRequest(caso_id, usuario_id)` (`extra="forbid"`, líneas 19-33) y salida `EvaluarResponse(puede_reprocesar, motivos, accion_recomendada, referencias_normativas)` (`extra="forbid"`, líneas 36-44).
  - No existe reprocesamiento real, frontend, RAG, servidores MCP, envío de notificaciones, gestión de incidentes, acceso a evidencia documental/biométrica (`POL-ACC` v1), alertas automáticas S2 ni campos adicionales en respuestas `200 OK`.
  - Los 18 requisitos (`REQ-01..REQ-18`), los 10 criterios de aceptación (`CA-01..CA-10`) y las 8 tareas (`T-01..T-08`) están implementados dentro del alcance cerrado de `specs/01-requisitos.md` y `specs/02-plan.md`.

### Eje 2 · Conformidad normativa y precedencia determinista de `accion_recomendada`
- **Estado:** Conforme en reglas vigentes y precedencia; **1 observación menor (`H-02`, severidad `Baja`)** en una combinación teórica de `E-207`.
- **Verificación:**
  - Se aplican exclusivamente `MAN-INC` v2 §4 (`ESTADOS_ELEGIBLES = {"error", "detenido"}`, bloqueo por `tiene_decision_final`, roles autorizados `{soporte_n1, soporte_n2, ingenieria}`, límite general `LIMITE_GENERAL_REPROCESOS = 3` con escalamiento S3, servicio dependiente `operativo`), `CAT-ERR` v2 §1 (`E-101`, `E-102`, `E-207`, `E-208`, `E-305`, `E-311`, `E-410`, `E-512`) y `GUI-COL` v1 §1 como referencia de servicios `SRV-*`.
  - Exclusión total de `CAT-ERR` v1 comprobada en `REGLAS_CAT_ERR_V2` (`src/mira_reproceso/rules.py:36-128`): `E-207` exige `SRV-MOD` operativo y mantiene reintento automático en cola si está degradado/caído (`C-031`), `E-410` retorna `puede_reprocesar=False` con acción de encolado sin rechazo (`C-035`), y `E-512` permite 1 reproceso antes de escalar (`SYN-E512-0` vs `SYN-E512-1` / `C-034`).
  - Acumulación de impedimentos concurrentes (`EX-04`) e inconsistencias (`EX-05`) verificada en `evaluar_elegibilidad` (`src/mira_reproceso/rules.py:223-347`) y precedencia determinista en `_seleccionar_accion_bloqueo` (`rules.py:158-191`): decisión final > inconsistencia `EX-05` > código no reprocesable `CAT-ERR` v2 > límite `E-512` > límite general `3` > servicio no operativo > estado no elegible.
  - Véase `H-02` respecto al caso borde en que `codigo_error == "E-207"` coexista con un `servicio_dependiente != "SRV-MOD"` no operativo mientras `SRV-MOD` sí esté `operativo`.

### Eje 3 · Seguridad y control de rol simulado (`usuario_id`)
- **Estado:** Conforme (sin hallazgos).
- **Verificación:**
  - `evaluar_elegibilidad` (`src/mira_reproceso/rules.py:200-204`) ejecuta `validar_usuario_autorizado(datos, usuario_id)` (líneas 136-146) estrictamente antes de `obtener_caso(datos, caso_id)` (líneas 149-155), consultando únicamente `datos.usuarios` sin tocar `datos.casos`.
  - `api.py` (líneas 87-96) mapea `UsuarioNoAutorizadoError` a `HTTP 403` con mensaje uniforme `{"detail": "Usuario no autorizado para evaluar reprocesamiento."}`, tanto para roles no habilitados (`U-S4` `comercial`) como para usuarios inexistentes (`U-999`), sin revelar existencia ni diagnósticos de `caso_id`.
  - `CasoNoEncontradoError` mapea a `HTTP 404` (`{"detail": "Caso no encontrado."}`) solo cuando el usuario está autorizado.
  - `EvaluarRequest` (`api.py:19-33`) aplica `ConfigDict(extra="forbid")`, `StrictStr` (rechaza `int`, `bool`, `None`, `list`) y `field_validator` con `.strip()` rechazando cadenas vacías o solo espacios con `HTTP 422`. Las respuestas `403`, `404` y `422` son errores HTTP estándar separados del contrato de 4 campos de `HTTP 200`.

### Eje 4 · Reglas críticas específicas (`E-512`, `E-207` y separación `CATALOGO_CAT_ERR_V2` / `REGLAS_CAT_ERR_V2`)
- **Estado:** Conforme (sin hallazgos propios fuera de la observación menor `H-02`).
- **Verificación:**
  - **`E-512`:** `LIMITE_E512 = 1` (`rules.py:18`) aplicado en `rules.py:325-338` usando `caso.reprocesos_realizados` como contador global conservador por caso (ratificado en Control Humano 1, `specs/01-requisitos.md §7.2`). Con `0` reprocesos habilita 1 reproceso (`SYN-E512-0`); con `>= 1` bloquea citando `CAT-ERR v2 §1 (E-512)` (y si `>= 3`, añade cita a `MAN-INC v2 §4` como en `C-034`), manteniendo `LIMITE_GENERAL_REPROCESOS = 3` intacto para `E-207` y `E-305`.
  - **`E-207`:** `rules.py:259-317` y `357-358` verifican tanto `caso.servicio_dependiente` como `SERVICIO_MODELOS_ID = "SRV-MOD"` (sin duplicar mensajes cuando `servicio_dependiente == "SRV-MOD"` y cubriendo el caso en que `servicio_dependiente != "SRV-MOD"`).
  - **Observación de Control Humano 2:** `CATALOGO_CAT_ERR_V2` (`frozenset[str]`, `rules.py:22-33`) se usa exclusivamente para pertenencia (`codigo_error in CATALOGO_CAT_ERR_V2`, línea 241), separado de `REGLAS_CAT_ERR_V2` (`dict[str, ReglaCodigoError]`, líneas 36-128), y verificado en `tests/test_rules.py:168-171`.

### Eje 5 · Validez y suficiencia de las pruebas automatizadas (`tests/test_rules.py` y `tests/test_api.py`)
- **Estado:** Cobertura nominal completa (`10/10` Excel + `14/14` `SYN-*` + `EX-04`/`EX-05`), con **1 hallazgo verificado (`H-01`, severidad `Media`)** sobre el diseño tautológico de `SYN-INJ-OK`.
- **Verificación:**
  - `tests/test_rules.py` (20 ítems ejecutados) y `tests/test_api.py` (26 ítems ejecutados) cubren los 10 casos de `CU-2_datos.xlsx` (`C-031..C-040`), los 14 escenarios sintéticos (`SYN-E102`, `SYN-E512-0`, `SYN-E512-1`, `SYN-E207-OK`, `SYN-DET-OK`, `SYN-LIMIT-2`, `SYN-LIMIT-3`, `SYN-DECFIN`, `SYN-ROL-COM`, `SYN-ROL-N2-ING`, `SYN-NO-USER`, `SYN-NO-CASE`, `SYN-422`, `SYN-INJ-OK`), pureza AST de `rules.py`, lectura intacta de `CU-2_datos.xlsx` (`sha256` antes/después) y exclusión de `registro_tecnico`.
  - **Análisis crítico de resistencia a *prompt injection* (`C-038`/`L-009` vs `SYN-INJ-OK`):**
    - Para **`C-038` / `L-009`**: las pruebas `test_loader_solo_lectura_y_exclusion_registro_tecnico` (`tests/test_rules.py:174-194`), `test_casos_reales_excel_c031_a_c040` (`test_rules.py:292-304`) y `test_http_resistencia_prompt_injection_c038_y_syn_inj_ok` (`tests/test_api.py:271-282`) **sí demuestran comportamiento real**, porque cargan el archivo oficial `CU-2_datos.xlsx` que contiene la hoja `registro_tecnico` (`L-009`), comprueban que `DatosOperativos` y `Caso` carecen de `registro_tecnico`, verifican que el SHA-256 del Excel no cambia y confirman que `C-038` responde únicamente por `E-311` sin referencias ni acciones sobre `ORG-02`.
    - Para **`SYN-INJ-OK`** (`tests/test_rules.py:432-444` y `tests/test_api.py:284-292`): véase **`H-01`** (`Media`). Aunque sigue el patrón de fixture externo mencionado en `specs/02-plan.md:166,188`, las aserciones sobre `registro_tecnico_hostil` y `_registro_hostil_ignorado` son tautológicas sobre variables locales desconectadas del sistema bajo prueba y no ejercitan la frontera real de ingestión (`cargar_datos_excel` o payload HTTP rechazado) con un `registro_tecnico` hostil adjunto a un caso elegible.

### Eje 6 · Trazabilidad e integridad de la evidencia
- **Estado:** Conforme (sin hallazgos).
- **Verificación:**
  - `docs/evidencia/pytest-iter0.log` (líneas 1-8) muestra `sha256sum -c docs/kit-sha256sums.txt` con **7 de 7 archivos `OK`**, y ejecución sin caché de `pytest -p no:cacheprovider -v` con **`46 passed, 1 warning in 1.09s`** (`0 failed`, `0 skipped`).
  - Los 46 casos listados en `docs/evidencia/pytest-iter0.log` (líneas 17-62) coinciden 1 a 1 en nombre y parametrización con los 26 ítems de `tests/test_api.py` y 20 ítems de `tests/test_rules.py`.
  - Todos los símbolos, funciones y casos citados en `specs/03-trazabilidad.md` (`RN-01..RN-18`) existen exactamente con ese nombre en `src/mira_reproceso/` y `tests/`, sin referencias activas a `CAT-ERR` v1.
  - `docs/trabajo/003-implementador-a-revisor.md` es consistente con la evidencia del log, con el estado de `specs/03-trazabilidad.md` y con los comandos ejecutados (`verificar_trazabilidad.py --check-kit --matrix specs/03-trazabilidad.md` con salida `0`).

---

## 4. Hallazgos verificados

### Tabla resumen

| ID | Severidad | Archivo y línea(s) | Requisito o criterio afectado | Resumen del hallazgo |
|---|---|---|---|---|
| `H-01` | `Media` | `tests/test_rules.py:432-444`, `tests/test_api.py:284-292` | `REQ-17`, `CA-10` | `SYN-INJ-OK` usa variables locales desconectadas del SUT y aserciones tautológicas; no ejercita ingestión real de `registro_tecnico` hostil en un caso elegible. |
| `H-02` | `Baja` | `src/mira_reproceso/rules.py:270-285`, `src/mira_reproceso/rules.py:184-188` | `REQ-07`, `REQ-11` | En `E-207`, si falla un `servicio_dependiente != "SRV-MOD"` mientras `"SRV-MOD"` está `"operativo"`, la acción recomendada menciona erróneamente esperar a `"SRV-MOD"`. |

*(Ejes 1, 3, 4 y 6: sin hallazgos verificados).*

---

### Fichas detalladas

#### Hallazgo `H-01`
- **Severidad:** `Media` (no bloqueante para el código productivo, observación relevante de calidad probatoria).
- **Archivo y línea(s):**
  - `/home/lester/Documents/entrega4-mira-multiagente/tests/test_rules.py#L432-L444`
  - `/home/lester/Documents/entrega4-mira-multiagente/tests/test_api.py#L284-L292`
- **Requisito o criterio afectado:** `REQ-17`, `CA-10` (`SYN-INJ-OK`).
- **Justificación verificable:**
  - En `tests/test_rules.py:434-441`, `test_sintetico_prompt_injection_ignorado_syn_inj_ok` define el diccionario local `registro_tecnico_hostil`, ejecuta la aserción tautológica `assert "SYN-INJ-OK" in registro_tecnico_hostil` (línea 440) y llama a `evaluar_elegibilidad(datos, "SYN-INJ-OK", "U-S1")` sin que `registro_tecnico_hostil` interactúe en ningún punto con `loader.py`, `models.py` o `rules.py`.
  - En `tests/test_api.py:285-292`, `test_http_resistencia_prompt_injection_c038_y_syn_inj_ok` define la cadena local `_registro_hostil_ignorado`, ejecuta la aserción tautológica `assert _registro_hostil_ignorado` (línea 286) y envía un `POST` sobre `SYN-INJ-OK` cuyo objeto `Caso` (`tests/test_api.py:108-115`) es equivalente a `C-032` sin dato hostil adjunto.
  - Si bien la seguridad estructural del código está probada de forma real por `cargar_datos_excel()` + `test_loader_solo_lectura_y_exclusion_registro_tecnico` + `C-038`/`L-009` (sobre `CU-2_datos.xlsx`), `SYN-INJ-OK` por sí solo no demuestra la inmunidad ante un `registro_tecnico` hostil en un caso elegible (`puede_reprocesar=True`). Para demostrarlo efectivamente sin alterar `kit/`, la prueba debería construir en `tmp_path` un `.xlsx` sintético en memoria/temporal con un caso elegible y una hoja `registro_tecnico` hostil y pasarlo por `cargar_datos_excel(ruta_tmp)` → `create_app(datos)` (además de verificar opcionalmente el rechazo `422` si se inyecta `registro_tecnico` en el JSON de `POST /reprocesamiento/evaluar`).

#### Hallazgo `H-02`
- **Severidad:** `Baja` (observación de borde teórico; alineada con el texto de `specs/02-plan.md:97`).
- **Archivo y línea(s):**
  - `/home/lester/Documents/entrega4-mira-multiagente/src/mira_reproceso/rules.py#L270-L285`
  - `/home/lester/Documents/entrega4-mira-multiagente/src/mira_reproceso/rules.py#L184-L188`
- **Requisito o criterio afectado:** `REQ-07`, `REQ-11`.
- **Justificación verificable:**
  - En `rules.py:270-271`, dentro de `if estado_srv_dep != "operativo":`, toda falla del `servicio_dependiente` cuando `codigo_error == "E-207"` activa `servicio_no_operativo_e207 = True`, incluso cuando `servicio_dep.servicio_id != SERVICIO_MODELOS_ID` y `SRV-MOD` está `operativo` en las líneas `296-316`.
  - Esto provoca que `_seleccionar_accion_bloqueo` (`rules.py:184-188`) retorne `"No reprocesar; el caso permanece en cola y se reintenta automáticamente cuando SRV-MOD esté operativo."` aunque el servicio bloqueante haya sido otro `servicio_dependiente` distinto de `SRV-MOD`.
  - No afecta a ningún caso del kit (`C-031`, `C-036`, `C-039` tienen `servicio_dependiente == "SRV-MOD"`) y sigue la redacción resumida de `specs/02-plan.md:97`, pero debería distinguirse (`servicio_no_operativo_e207` solo cuando `SRV-MOD` no está operativo; `servicio_no_operativo_otro` si falla únicamente otro `servicio_dependiente`) si en evolución futura un `E-207` depende de múltiples servicios.

---

## 5. Conclusión y recomendación operativa

- **Veredicto:** **`APROBADO CON OBSERVACIONES`** (Iteración `0/2`).
- **Fundamento:** El prototipo cumple íntegramente el contrato mínimo, las reglas vigentes de `MAN-INC` v2 y `CAT-ERR` v2, la exclusión de `CAT-ERR` v1 y alcance extra, el control prioritario simulado de rol (`403` uniforme sin fuga de casos), el supuesto conservador ratificado de `E-512`, la inmutabilidad del kit (`7/7` checksums `OK`) y la ejecución reproducible de `46/46` pruebas sin fallos ni omisiones. No existen defectos `Críticos` ni `Altos`.
- **Recomendación operativa para la decisión humana:**
  1. **Opción recomendada (cierre directo en Iteración `0/2` si se prioriza el alcance actual):** Aprobar formalmente la entrega registrando este dictamen en `docs/trabajo/`, dejando documentados `H-01` y `H-02` como observaciones no bloqueantes (dado que `C-038`/`L-009` + `test_loader_solo_lectura_y_exclusion_registro_tecnico` ya prueban la exclusión estructural real de `registro_tecnico` y ningún caso `E-207` actual depende de un servicio distinto de `SRV-MOD` degradado con `SRV-MOD` operativo).
  2. **Opción alternativa (Iteración `1/2` opcional de endurecimiento):** Si la persona responsable técnica exige que `SYN-INJ-OK` pruebe el flujo completo de ingestión hostil sin tautologías, abrir la ronda `1/2` acotada exclusivamente a:
     - Reemplazar las variables locales tautológicas de `SYN-INJ-OK` (`tests/test_rules.py:432-444` y `tests/test_api.py:284-292`) por un libro `.xlsx` sintético en `tmp_path` con un caso elegible (`puede_reprocesar=True`) y una hoja `registro_tecnico` hostil cargado con `cargar_datos_excel(...)` → `create_app(...)`.
     - Ajustar `rules.py:270-285` para asignar `servicio_no_operativo_e207` únicamente cuando falla `SRV-MOD` y `servicio_no_operativo_otro` cuando `SRV-MOD` está `operativo` pero falla otro `servicio_dependiente`, añadiendo el caso de prueba correspondiente.

---

## 6. Evidencia auditada (rutas absolutas bajo `/home/lester/Documents/entrega4-mira-multiagente/`)

- Reglas y decisiones:
  - `/home/lester/Documents/entrega4-mira-multiagente/AGENTS.md`
  - `/home/lester/Documents/entrega4-mira-multiagente/docs/decision.md`
  - `/home/lester/Documents/entrega4-mira-multiagente/docs/bitacora.md`
- Especificación, plan y trazabilidad:
  - `/home/lester/Documents/entrega4-mira-multiagente/specs/01-requisitos.md`
  - `/home/lester/Documents/entrega4-mira-multiagente/specs/02-plan.md`
  - `/home/lester/Documents/entrega4-mira-multiagente/specs/03-trazabilidad.md`
- Kit normativo e integridad:
  - `/home/lester/Documents/entrega4-mira-multiagente/kit/CU-2_soporte_operacion/corpus/MAN-INC_manual_incidentes.md`
  - `/home/lester/Documents/entrega4-mira-multiagente/kit/CU-2_soporte_operacion/corpus/CAT-ERR_v2_vigente.md`
  - `/home/lester/Documents/entrega4-mira-multiagente/kit/CU-2_soporte_operacion/corpus/CAT-ERR_v1_derogado.md`
  - `/home/lester/Documents/entrega4-mira-multiagente/kit/CU-2_soporte_operacion/corpus/GUI-COL_colas_servicios_externos.md`
  - `/home/lester/Documents/entrega4-mira-multiagente/kit/CU-2_soporte_operacion/corpus/POL-ACC_acceso_evidencia.md`
  - `/home/lester/Documents/entrega4-mira-multiagente/kit/CU-2_soporte_operacion/corpus/PRO-MAN_mantencion.md`
  - `/home/lester/Documents/entrega4-mira-multiagente/docs/kit-sha256sums.txt`
- Código fuente y pruebas:
  - `/home/lester/Documents/entrega4-mira-multiagente/pyproject.toml`
  - `/home/lester/Documents/entrega4-mira-multiagente/src/mira_reproceso/__init__.py`
  - `/home/lester/Documents/entrega4-mira-multiagente/src/mira_reproceso/models.py`
  - `/home/lester/Documents/entrega4-mira-multiagente/src/mira_reproceso/loader.py`
  - `/home/lester/Documents/entrega4-mira-multiagente/src/mira_reproceso/rules.py`
  - `/home/lester/Documents/entrega4-mira-multiagente/src/mira_reproceso/api.py`
  - `/home/lester/Documents/entrega4-mira-multiagente/tests/test_rules.py`
  - `/home/lester/Documents/entrega4-mira-multiagente/tests/test_api.py`
- Traspasos, scripts de verificación y evidencia de ejecución:
  - `/home/lester/Documents/entrega4-mira-multiagente/docs/trabajo/README.md`
  - `/home/lester/Documents/entrega4-mira-multiagente/docs/trabajo/001-requisitos-a-planificador.md`
  - `/home/lester/Documents/entrega4-mira-multiagente/docs/trabajo/002-planificador-a-implementador.md`
  - `/home/lester/Documents/entrega4-mira-multiagente/docs/trabajo/003-implementador-a-revisor.md`
  - `/home/lester/Documents/entrega4-mira-multiagente/docs/evidencia/pytest-iter0.log`
  - `/home/lester/Documents/entrega4-mira-multiagente/.agents/skills/ejecucion-pruebas/scripts/run_tests.sh`
  - `/home/lester/Documents/entrega4-mira-multiagente/.agents/skills/trazabilidad/scripts/verificar_trazabilidad.py`

---

## 3. Decisión humana registrada (Control de calidad Iteración 0/2 · Apertura ronda 1/2)

- **Resolución:**
  - `[ ] Aceptar entrega` (cerrar implementación en iteración `0/2` dejando `H-01` y `H-02` documentados como observaciones no bloqueantes)
  - `[x] Solicitar correcciones al Implementador (ronda 1/2)` (atender `H-01` y `H-02` en una ronda acotada)
  - `[ ] Rechazar entrega`
- **Responsable:** Responsable técnico del equipo *(decisión humana directa; no emitida por el agente)*
- **Fecha:** `2026-11-22`
- **Observaciones y correcciones autorizadas (ronda 1/2):**
  - No se rechaza la implementación completa: se reconoce como válido el dictamen `APROBADO CON OBSERVACIONES` del agente `revisor` sobre la iteración `0/2` (commit `e26eba3`), pero se resuelve corregir los dos hallazgos verificados antes de cerrar la entrega, abriendo formalmente la **ronda `1/2`**.
  - **`H-01` (`Media`):** reemplazar las pruebas tautológicas de `SYN-INJ-OK` por una prueba que ejercite realmente la frontera de entrada, utilizando un Excel sintético temporal con `registro_tecnico` hostil cargado mediante `cargar_datos_excel`, sin modificar el kit original (`kit/CU-2_soporte_operacion/`). Comprobar que el resultado normativo de un caso elegible no cambia; opcionalmente, comprobar el rechazo HTTP `422` ante campos extra.
  - **`H-02` (`Baja`):** corregir la selección de `accion_recomendada` para `E-207` cuando `SRV-MOD` está `operativo` pero otro servicio dependiente no lo está, añadiendo una prueba de regresión específica.
  - **Compuerta previa a ronda 1/2:** se conserva íntegra la transcripción del dictamen del `revisor` (Sección 2) y el flujo se detiene para registrar un commit humano independiente antes de invocar al `implementador` en la ronda `1/2`.
