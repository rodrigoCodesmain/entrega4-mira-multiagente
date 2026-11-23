# Comparación Objetiva de Modalidades · MIRA CU-2 (`CORRIDA-MA-01` vs. `CORRIDA-LB-01`)

- **Fecha de elaboración:** 2026-11-22
- **Estado:** **Aprobado con ajustes metodológicos menores** (`2026-11-22`, responsable técnico humano)
- **Commit base en el repositorio multiagente (`HEAD`):** `e998cca` (*docs: cerrar corrida multiagente con aprobacion humana final*)
- **Documentos de referencia:** [`protocolo-comparacion.md`](protocolo-comparacion.md) · [`specs/01-requisitos.md`](../../specs/01-requisitos.md) · [`docs/bitacora.md`](../bitacora.md)
- **Alcance temporal comparado:** Ambas corridas se comparan **a partir de `specs/01-requisitos.md` aprobada en Control Humano 1 (`0e47c1c`)**. Se excluyen explícitamente la Fase 1 previa (levantamiento normativo y redacción de requisitos por `requisitos`) y la espera de aprobación del Control Humano 1.

---

## 1. Síntesis metodológica y fuentes verificadas

| Eje | Modalidad A · Multiagente (`CORRIDA-MA-01`) | Modalidad B · Agente Único (`CORRIDA-LB-01`) |
|---|---|---|
| **Workspace / aislamiento** | `/home/lester/Documents/entrega4-mira-multiagente` (clon compartido, commits `0e47c1c` → `e998cca`) | `/home/lester/Documents/mira-cu2-linea-base-aislada` (preparado externamente mediante `git archive 0e47c1c` según comandos documentados por el responsable humano; ese hash no quedó anotado originalmente en los reportes internos de la corrida; código archivado en [`codigo-agente-unico.tar.gz`](CORRIDA-LB-01/codigo-agente-unico.tar.gz)) |
| **Flujo ejecutado** | Secuencial con 4 agentes configurados en `.agents/agents/`: `planificador` → **Control Humano 2** → `implementador` (`0/2`) ↔ `revisor` (`0/2`) → decisión humana → `implementador` (`1/2`) ↔ `revisor` (`1/2`) → cierre humano | Sesión única de 1 agente en Antigravity (planificación y ejecución en el mismo hilo), sin `invoke_subagent`, sin flujo Implementador/Revisor y sin actas de traspaso |
| **Paquete y artefactos** | `src/mira_reproceso/` (`__init__`, `models`, `loader`, `rules`, `api`), `tests/{test_rules,test_api}.py`, `specs/02-plan.md`, `specs/03-trazabilidad.md`, actas `docs/trabajo/002..006` | `src/mira_cu2/` (`__init__`, `models`, `repository`, `rules`, `api`), `tests/{conftest,test_casos_excel,test_escenarios_sinteticos,test_seguridad}.py`, `specs/03-trazabilidad.md`, `README.md` |
| **Evidencias revisadas** | [`docs/bitacora.md`](../bitacora.md), [`docs/evidencia/pytest-iter0.log`](../evidencia/pytest-iter0.log), [`docs/evidencia/pytest-iter1.log`](../evidencia/pytest-iter1.log), [`docs/trabajo/002..006`](../trabajo/README.md) y [`docs/evidencia/CORRIDA-MA-01/`](../evidencia/CORRIDA-MA-01/) | [`prompt-ejecucion.md`](CORRIDA-LB-01/prompt-ejecucion.md), [`resultado.md`](CORRIDA-LB-01/resultado.md), [`metricas.md`](CORRIDA-LB-01/metricas.md), [`pytest.log`](CORRIDA-LB-01/pytest.log), [`codigo-agente-unico.tar.gz`](CORRIDA-LB-01/codigo-agente-unico.tar.gz) y [`workspace-aislado.png`](CORRIDA-LB-01/workspace-aislado.png) |

---

## 2. Tabla comparativa de métricas verificables

| Métrica | Modalidad A · Multiagente (`CORRIDA-MA-01`) | Modalidad B · Agente Único (`CORRIDA-LB-01`) | Notas metodológicas |
|---|---|---|---|
| **Requisitos (`REQ-01..REQ-18`)** | `18 / 18` respaldados por las pruebas propias y análisis de código (`0` faltantes declarados) | `18 / 18` respaldados por las pruebas propias y análisis de código (`0` faltantes declarados) | El cumplimiento está respaldado por las pruebas y análisis de cada modalidad frente a `specs/01-requisitos.md`, **no** por una batería idéntica de pruebas cruzadas ejecutada contra ambas soluciones. |
| **Criterios de aceptación comunes (`CA-01..CA-10`)** | `10 / 10` según su suite propia y revisión (`C-031..C-040` + `14/14` `SYN-*`) | `10 / 10` según su suite propia (`C-031..C-040` + `14/14` `SYN-*`) | Cobertura respaldada por pruebas propias de cada corrida (sin batería cruzada común). Diferencia cualitativa en `SYN-INJ-OK` (`CA-10`): en MA `1/2` usa `.xlsx` temporal cargado con `cargar_datos_excel()`, mientras LB mantiene una aserción tautológica sobre diccionario local (ver §3.3). |
| **Integridad del kit (`docs/kit-sha256sums.txt`)** | `7 / 7 OK` (verificado en iter. `0/2`, iter. `1/2` y cierre) | `7 / 7 OK` (verificado al término en `pytest.log` y test dedicado) | Ninguna modalidad modificó `kit/CU-2_soporte_operacion/`. |
| **Pruebas `pytest` ejecutadas** | Iter. `0/2`: **`46 passed, 0 failed, 0 skipped`** (`1.09s`, `1` warning)<br>Iter. `1/2`: **`48 passed, 0 failed, 0 skipped`** (`1.14s`, `1` warning; `27` en `test_api.py` + `21` en `test_rules.py`) | **`58 passed, 0 failed, 0 skipped`** (`0.27s`, `1` warning; `20` en `test_casos_excel.py` + `31` en `test_escenarios_sinteticos.py` + `7` en `test_seguridad.py`) | **El conteo bruto `58 > 48` no indica superioridad**: LB parametriza doble los 10 casos del Excel y separa 9 payloads `SYN-422` en casos independientes (`test_api.py` en MA agrupa 14 variantes `422` en 1 función). La diferencia de duración (`0.27s` frente a `1.14s`) se registra únicamente como **observación**, sin atribuirla definitivamente a fixtures u otras causas no aisladas experimentalmente. Mismo `StarletteDeprecationWarning` externo. |
| **Tiempo activo aproximado de agentes** | ~`21 min` aproximados sumando las 5 ventanas registradas de subagentes (`planificador` `4m`, `implementador 0/2` `7m`, `revisor 0/2` `3m05s`, `implementador 1/2` `4m56s`, `revisor 1/2` `1m56s`); sobrecarga de turnos del orquestador: `No disponible` | `7 min 34 s` aproximados entre marcas `date -Is` (`21:34:35-03:00` → `21:42:09-03:00`; `8 min 20 s` hasta el chequeo de `21:42:55-03:00`). En `metricas.md` figura como `No disponible` | **Aproximaciones con métodos distintos de medición** (suma parcial de ventanas de subagentes vs. marcas `date -Is` en una sesión única). No constituyen una comparación experimental controlada de rendimiento, aunque reflejan menor sobrecarga operativa en agente único. |
| **Tiempo total transcurrido y espera humana** | **`~4 h 09 min`** de tiempo total transcurrido entre eventos (`17:04` inicio Fase 2 → `21:13+` decisión final de cierre, publicado luego en `e998cca`). El intervalo restante tras restar las ventanas de subagentes incluye pausas, coordinación, orquestación y acciones humanas cuya duración individual no fue medida (`No disponible`) | **`0 min` de espera o intervención humana durante la ejecución** (`0` intervenciones entre `21:34:35` y `21:42:09`); tiempos externos previos y posteriores: `No disponible` | Las `~4 h 09 min` de MA representan tiempo de reloj entre eventos, **no** tiempo de trabajo humano efectivamente medido; reflejan la presencia de compuertas entre fases frente a una corrida ininterrumpida en LB. |
| **Correcciones realizadas (por naturaleza)** | **`1` ronda formal tras auditoría independiente (`1/2`)** sobre `H-01` (`Media`) y `H-02` (`Baja`), más `2` observaciones documentales en Control Humano 2 | **`2` autocorrecciones internas de entorno/empaquetado** durante su propia ejecución (`pythonpath`/`tests/__init__.py` y `uv sync --reinstall-package`); **`0` correcciones por revisión externa** | **No son equivalentes:** las correcciones de LB resolvieron fallos propios de empaquetado inicial en `.venv`; la ronda `1/2` de MA corrigió debilidades semánticas y probatorias (`H-01`, `H-02`) detectadas por un auditor independiente que habían pasado inadvertidas con las 46 pruebas iniciales en verde. |
| **Participación humana y controles formales** | Alta: Control Humano 2 (`7c0e152`), decisión tras `revisor 0/2` (`2c88947`), aceptación final (`e998cca`), 5 commits humanos post-CH1 e historial en bitácora | Nula durante la ejecución (`0` intervenciones entre prompt inicial y cierre; empaquetado y copia de evidencias realizados externamente) | La gobernanza humana en MA aportó validación de diseño y cierre, a costa de mayor latencia operativa. |
| **Trazabilidad normativa y auditoría independiente** | `specs/02-plan.md` + `specs/03-trazabilidad.md` (`RN-01..RN-18`, validado con `verificar_trazabilidad.py`, evidencia `0/2` y `1/2` separada) + 5 actas post-CH1 + 2 dictámenes de solo lectura | `specs/03-trazabilidad.md` (`REG-01..REG-18`, validado con `verificar_trazabilidad.py`) + `resultado.md`/`metricas.md` + `README.md`; sin plan aprobado por compuerta, sin actas ni auditoría independiente | Ambas superaron `verificar_trazabilidad.py`; solo MA cuenta con verificación independiente separada de escritura y ejecución. |
| **Tokens / costo** | `No disponible` (no informado por Antigravity) | `No disponible` (no informado por Antigravity) | Sin telemetría de consumo o costo en ninguna de las dos corridas. |

---

## 3. Análisis de conformidad contractual (`specs/01-requisitos.md`) y hallazgos técnicos

### 3.1 Divergencia de ruta HTTP: `POST /reprocesamiento/evaluar` vs. `POST /elegibilidad`

- **Lo que exige `specs/01-requisitos.md`:** en la Sección 2.3 (*Contrato mínimo de la API y códigos de respuesta HTTP*, líneas 64–100) y en los criterios `CA-01..CA-10`, la especificación aprobada en Control Humano 1 establece con precisión la carga útil de entrada (`{caso_id, usuario_id}`), el contrato exacto de 4 campos de `HTTP 200` (`puede_reprocesar`, `motivos`, `accion_recomendada`, `referencias_normativas`) y la separación respecto de errores `HTTP 403`, `404` y `422`, **sin definir ni exigir ninguna ruta URI específica** (se refiere genéricamente a *"un endpoint mínimo"* o *"el endpoint"*, líneas 29, 74 y 229).
- **Origen de cada ruta:**
  - En **`CORRIDA-MA-01`**, la ruta **`POST /reprocesamiento/evaluar`** fue definida posteriormente en [`specs/02-plan.md`](../../specs/02-plan.md#L128) (`src/mira_reproceso/api.py:69`) y aprobada en Control Humano 2 (`7c0e152`), etapa que no formaba parte de `COMMIT_BASE_CH1` (`0e47c1c`).
  - En **`CORRIDA-LB-01`**, al partir exclusivamente de `specs/01-requisitos.md`, el agente único escogió libremente **`POST /elegibilidad`** (`src/mira_cu2/api.py:27`).
- **Conclusión contractual:** **ninguna de las dos soluciones incumple `specs/01-requisitos.md`** por el nombre de la ruta. No obstante, la ausencia de una ruta URI fija en `specs/01-requisitos.md` constituye una **ambigüedad o brecha menor de la especificación inicial**: impide ejecutar exactamente el mismo cliente o suite HTTP cruzada contra ambas APIs sin parametrizar el *path*.

### 3.2 Cumplimiento funcional de `REQ-01..REQ-18` y `CA-01..CA-10`

Al inspeccionar el código fuente de `CORRIDA-MA-01` (`src/mira_reproceso/`) y el código extraído de `CORRIDA-LB-01` (`src/mira_cu2/` dentro de `codigo-agente-unico.tar.gz`), el cumplimiento de los `18` requisitos y los `10` criterios de aceptación está respaldado por las pruebas propias de cada modalidad y dicho análisis contra `specs/01-requisitos.md`, **no** por una batería idéntica de pruebas cruzadas ejecutada contra ambas soluciones:

- Evaluación determinista de `C-031..C-040` con separación estricta respecto de `CAT-ERR` v1 (respetando la inversión normativa de `E-207`, `E-410` y el límite específico de `1` reproceso global para `E-512`).
- Autorización simulada prioritaria por rol (`soporte_n1`, `soporte_n2`, `ingenieria`) ejecutada antes de consultar `casos`, verificada mediante guardas/espías que prueban cero accesos a `casos` ante `HTTP 403`.
- Validación estricta de entrada (`StrictStr`, `extra="forbid"`, `.strip()` no vacío → `HTTP 422`) y salida estricta de 4 campos (`HTTP 200`, sin campos extra ni alertas automáticas S2).
- Acumulación de impedimentos concurrentes (`EX-04`, ej. `C-035`, `C-036`, `C-037`, `C-039`) y manejo seguro de inconsistencias (`EX-05`).
- Lectura en solo lectura (`openpyxl(..., read_only=True, data_only=True)`) que excluye estructuralmente la hoja `registro_tecnico` (protección real ante `L-009` en `C-038`).

### 3.3 Diferencias técnicas y hallazgos detectados por inspección comparativa del código

La inspección directa del código fuente y pruebas de `CORRIDA-LB-01` frente a las dos iteraciones de `CORRIDA-MA-01` revela diferencias concretas de calidad y robustez:

1. **Debilidad probatoria equivalente a `H-01` presente en `CORRIDA-LB-01`:**
   - En `CORRIDA-LB-01` (`tests/test_escenarios_sinteticos.py:262-283`), `test_syn_inj_ok_ignora_registro_tecnico_hostil_simulado` define un diccionario local `registro_tecnico_simulado = {"SYN-INJ-OK": ...}` dentro de la función de prueba, desconectado de `RepositorioExcel`, `RepositorioMemoria` y `TestClient`, verificando al final que esa cadena local no está en `motivos`.
   - Este patrón es prácticamente idéntico al defecto **`H-01` (`Media`)** que `CORRIDA-MA-01` cometió en su iteración `0/2`. En `CORRIDA-MA-01`, la revisión independiente del `revisor` identificó esa tautología y forzó en iteración `1/2` una prueba real sobre `.xlsx` temporal en `tmp_path` cargado mediante `cargar_datos_excel()` junto con la prueba explícita de rechazo `HTTP 422` ante campo extra `"registro_tecnico"`. En `CORRIDA-LB-01`, al no existir revisor independiente, esa debilidad permaneció en verde. *(Cabe precisar que en ambas soluciones la resistencia real de `C-038`/`L-009` sobre `CU-2_datos.xlsx` sí está probada efectivamente).*
2. **Debilidad comparable a `H-02` presente en `CORRIDA-LB-01`:**
   - En `CORRIDA-LB-01` (`src/mira_cu2/rules.py:133-136, 219-237`), un único booleano `servicio_no_operativo` agrupa fallos del `servicio_dependiente` y de `SRV-MOD`. Si un caso `E-207` tiene `SRV-MOD` en estado `operativo` pero su `servicio_dependiente` (distinto de `SRV-MOD`, p. ej. `SRV-REG`) está `caido`, `_seleccionar_accion_bloqueada` devuelve una acción recomendada genérica (`"No reprocesar; el caso permanece en cola y se reintenta automáticamente."`) que **no identifica el servicio dependiente bloqueante**.
   - Se trata de una **debilidad comparable —aunque no idéntica en la redacción—** al defecto `H-02` (`Baja`) que apareció en la iteración `0/2` de `CORRIDA-MA-01` (donde la acción nombraba erróneamente a `SRV-MOD` en lugar del servicio caído) y que quedó corregido y cubierto por pruebas de regresión en iteración `1/2` (`src/mira_reproceso/rules.py:185-196, 277-319`).
3. **Diferencia en mensajes `HTTP 403` (`EX-01` vs. `EX-02`):**
   - `CORRIDA-LB-01` (`src/mira_cu2/rules.py:173-176`) devuelve `"Usuario sin autorización para evaluar reprocesamiento."` si `usuario_id` no existe y `"Rol no autorizado para evaluar reprocesamiento."` si existe con rol inválido. Sigue literalmente los ejemplos de `specs/01-requisitos.md §3.2`, pero revela implícitamente si un `usuario_id` existe o no en `usuarios`.
   - `CORRIDA-MA-01` (`src/mira_reproceso/api.py:88-91`) devuelve un único `detail` uniforme (`"Usuario no autorizado para evaluar reprocesamiento."`), evitando tanto fuga de casos como enumeración de `usuario_id`.
4. **Cobertura defensiva en carga Excel, referencias normativas y estructura de pruebas:**
   - **Normalización de entrada Excel:** `CORRIDA-MA-01` (`loader.py:57-72, 152-183`) normaliza booleanos reales, `0/1`, `true/false` y `sí/si/no` y aplica `.lower()` a `rol`/`estado`; `CORRIDA-LB-01` (`repository.py:24-31, 115-142`) exige exclusivamente `"sí"/"si"/"no"` y no normaliza a minúsculas `rol` ni `estado` (suficiente para el Excel actual, más frágil ante variaciones).
   - **Referencias normativas:** `CORRIDA-MA-01` añade la cita auxiliar `"GUI-COL v1 §1"` cuando evalúa servicios; `CORRIDA-LB-01` cita únicamente `"MAN-INC v2 §4"` y `"CAT-ERR v2 §1 (...)"`.
   - **Estrategia de pruebas:** `CORRIDA-MA-01` separa pruebas puras de dominio (incluido análisis AST verificando que `rules.py` no importa `fastapi`, `pydantic` ni `openpyxl` en `tests/test_rules.py:198-216`) de pruebas HTTP (`tests/test_api.py`), mientras `CORRIDA-LB-01` ejecuta todas sus pruebas mediante `TestClient` HTTP.

---

## 4. Auditoría de `prompt-ejecucion.md` y condiciones experimentales

### 4.1 Fidelidad de `prompt-ejecucion.md` respecto de las instrucciones ejecutadas

- **Evidencia directa observada:** no se dispone en el repositorio del log completo de conversación de `CORRIDA-LB-01` ni de una captura del mensaje inicial del usuario (`workspace-aislado.png` muestra únicamente el cierre de la sesión, `"16 files changed +1615 -0"` y `"58m ago"`). Por ello, **no es posible verificar criptográficamente la literalidad byte a byte** del prompt entregado en el chat.
- **Consistencia inferida por correspondencia de artefactos:** todas las salidas generadas en `CORRIDA-LB-01` reflejan exactamente las instrucciones específicas de [`prompt-ejecucion.md`](CORRIDA-LB-01/prompt-ejecucion.md): creación exacta de `prompt-ejecucion.md`, `resultado.md`, `metricas.md` y `pytest.log`, inclusión de guía de uso en `README.md` (actividad 9), marcas `date -Is` de inicio/término, anotación explícita de `No disponible`, uso directo de `run_tests.sh` y `verificar_trazabilidad.py`, creación de `specs/03-trazabilidad.md` y ausencia total de delegación o comparaciones con la modalidad multiagente.

### 4.2 Desviación respecto del prompt congelado del protocolo (`protocolo-comparacion.md`)

- **Prompt congelado en [`protocolo-comparacion.md`](protocolo-comparacion.md#L47-L57):** constaba de 10 líneas mínimas centradas únicamente en implementar `specs/01-requisitos.md` con FastAPI/`pytest` sin `invoke_subagent` ni modificaciones al kit.
- **Prompt real en [`prompt-ejecucion.md`](CORRIDA-LB-01/prompt-ejecucion.md) (74 líneas):** amplió sustancialmente la guía operativa detallando 9 actividades secuenciales (incluida la cobertura de los 10 casos del Excel y 14 escenarios sintéticos, registro de correcciones e instrucciones de instalación/arranque en `README.md`), autorizó explícitamente el uso de `.agents/skills/` y estandarizó los 4 archivos de métricas y cierre.
- **Implicación metodológica (Riesgo `R6`):** aunque no filtró soluciones ni código multiagente, la mayor estructuración del prompt ejecutado facilitó que el agente único documentara trazabilidad (`specs/03-trazabilidad.md`) y formato de métricas homogéneo respecto de la guía minimalista inicialmente congelada en el protocolo.

### 4.3 Control de aislamiento y riesgos (`R1..R6`)

- **Controles efectivos verificados:** uso de workspace independiente (`/home/lester/Documents/mira-cu2-linea-base-aislada`), preparado externamente mediante `git archive 0e47c1c` según los comandos documentados por el responsable humano (sin carpeta `.git` ni historial posterior, mitigando el riesgo `R2`), visible en [`workspace-aislado.png`](CORRIDA-LB-01/workspace-aislado.png); conversación nueva dedicada (*Experimento Línea Base Agente Único*); y diseño completamente autónomo sin trazas de copia respecto de `CORRIDA-MA-01` (distinto nombre de paquete `mira_cu2` vs. `mira_reproceso`, distinta abstracción `RepositorioDatos` vs. dataclass `DatosOperativos`, distinta ruta `/elegibilidad` vs. `/reprocesamiento/evaluar`, distinto prefijo en trazabilidad `REG-*` vs. `RN-*`).
- **Limitaciones de aislamiento observadas:**
  - **Orden temporal (`R2`):** `CORRIDA-LB-01` se ejecutó entre `21:34` y `21:42`, **después** de cerrar `CORRIDA-MA-01` (`21:13`), en lugar de haberse ejecutado antes de iniciar la implementación multiagente (mitigado por el uso de una carpeta aislada exportada con `git archive 0e47c1c`).
  - **Registro del commit base (`COMMIT_BASE_CH1`):** por evidencia externa documentada por el responsable humano, el directorio se preparó mediante `git archive 0e47c1c`; sin embargo, **dicho hash no quedó anotado originalmente dentro de los reportes internos generados por el agente único** ([`resultado.md`](CORRIDA-LB-01/resultado.md), [`metricas.md`](CORRIDA-LB-01/metricas.md)).
  - **Presencia de `.agents/skills/` (`R3`):** el agente único conservó y utilizó los scripts `.agents/skills/ejecucion-pruebas/scripts/run_tests.sh` y `.agents/skills/trazabilidad/scripts/verificar_trazabilidad.py`, lo cual estaba expresamente permitido en `prompt-ejecucion.md` y documentado como opción en `protocolo-comparacion.md` (`R3`), pero implica que parte de la infraestructura de verificación provino del repositorio base exportado desde `0e47c1c`.
  - **Barra lateral visible en `workspace-aislado.png`:** muestra el workspace hermano `entrega4-mira-cu2` en la lista de proyectos de la IDE (no abierto en la sesión mostrada).

---

## 5. Diferencias verificables de configuración, modelo y entorno

| Parámetro | Modalidad A · Multiagente (`CORRIDA-MA-01`) | Modalidad B · Agente Único (`CORRIDA-LB-01`) | Verificabilidad |
|---|---|---|---|
| **Plataforma / IDE** | Google Antigravity (`agy 1.5.14`) + CLI de verificación en host | Google Antigravity (`agy` versión no registrada explícitamente en `resultado.md`; IDE visible en `workspace-aislado.png`) | Verificado en [`docs/bitacora.md`](../bitacora.md) y `agy --version` / captura |
| **Selector de modelo UI** | `Orchestrator (Neon)` (subagentes ejecutados vía `invoke_subagent` con modelos por defecto heredados; desglose de modelos internos por subagente: `No disponible`) | `Orchestrator (Neon)` en Antigravity (`resultado.md` línea 6; desglose interno de modelos: `No disponible`) | Verificado en bitácora, `resultado.md` y `workspace-aislado.png` |
| **Modo de ejecución en UI** | `No disponible` en las capturas de `CORRIDA-MA-01` (las capturas muestran tarjetas de subagentes y panel overview) | Modo **`Turbo`** visible en la barra inferior de [`workspace-aislado.png`](CORRIDA-LB-01/workspace-aislado.png) | Diferencia de configuración no controlada explícitamente |
| **Runtime Python y `uv`** | `CPython 3.12.14`, `uv 0.13.8`, Linux | `CPython 3.12.14`, `uv 0.13.8`, Linux | Idéntico y verificado |
| **Versiones de librerías** | `fastapi 0.165.0`, `pydantic 2.14.4`, `openpyxl 3.1.5`, `httpx 0.28.1`, `pytest 9.2.0`, `uvicorn 0.54.0` | `fastapi 0.165.0`, `pydantic 2.14.4`, `openpyxl 3.1.5`, `httpx 0.28.1`, `pytest 9.2.0` (`uvicorn`: `No disponible` en `resultado.md`, incluido en `pyproject.toml`) | Prácticamente idéntico y verificado |
| **Empaquetado Python** | `setuptools>=68` (`pyproject.toml` sin cotas de versión y sin `uv.lock`; `requires-python >= 3.11`) | `hatchling>=1.25.0` (cotas `>=` en dependencias, `uv.lock` generado; `requires-python >= 3.12`) | Verificado en `pyproject.toml` de ambos |
| **Política sobre `README.md`** | Conservó intacto el `README.md` académico del repositorio compartido | Sobrescribió `README.md` con guía de instalación/ejecución conforme a actividad 9 de `prompt-ejecucion.md` | Verificado en `codigo-agente-unico.tar.gz` |

---

## 6. Limitaciones metodológicas del estudio y conclusiones objetivas

### 6.1 Limitaciones de comparabilidad

1. **Tamaño muestral único (`n = 1`):** una sola corrida por modalidad no permite inferencia estadística ni descarta variabilidad estocástica del modelo.
2. **Ausencia de telemetría de tokens y costo:** al no estar informados por Antigravity (`No disponible`), no es posible evaluar la relación costo/calidad ni cuantificar el consumo real del flujo multiagente de 4 roles frente al hilo único.
3. **Exclusión del levantamiento de requisitos y CH1:** la comparación mide la capacidad de implementar a partir de una especificación ya depurada (`specs/01-requisitos.md`); en proyectos reales, la Fase 1 y el control humano de requisitos absorben parte relevante del valor de la especialización.
4. **Asimetría de auditoría post-implementación:** `CORRIDA-MA-01` contó con un agente `revisor` de solo lectura que detectó `H-01` y `H-02`, mientras `CORRIDA-LB-01` no fue sometida al mismo protocolo de revisión independiente hasta este análisis comparativo.
5. **Divergencia respecto del prompt congelado (`R6`) y trazabilidad del origen en LB:** `prompt-ejecucion.md` introdujo más estructura de reporte que el protocolo inicial de 10 líneas; adicionalmente, aunque por evidencia externa del responsable humano consta que el workspace aislado fue preparado mediante `git archive 0e47c1c`, ese hash no quedó registrado dentro de los reportes internos del agente único.
6. **Ausencia de batería cruzada común y heterogeneidad de medición temporal:** el cumplimiento de `18/18 REQ` y `10/10 CA` se apoya en las pruebas propias y el análisis de cada modalidad (no en una batería idéntica ejecutada sobre ambas APIs, dada también la divergencia `/reprocesamiento/evaluar` vs. `/elegibilidad`), y los tiempos activos (`~21 min` parciales de subagentes vs. `~7.5 min` por `date -Is`) proceden de métodos distintos que no constituyen una medición experimental controlada de rendimiento (tampoco las `~4 h 09 min` totales de reloj en MA miden trabajo humano efectivo ni la diferencia `0.27s` vs. `1.14s` en `pytest` permite inferir causalidad sin aislar variables).

### 6.2 Balance objetivo sin afirmación de superioridad absoluta

Con la evidencia disponible en [`CORRIDA-MA-01`](../evidencia/CORRIDA-MA-01/) y [`CORRIDA-LB-01`](CORRIDA-LB-01/), **ambas modalidades lograron resultados funcionales satisfactorios** según sus pruebas propias y análisis frente a `specs/01-requisitos.md`, manteniendo `7/7` checksums del kit `OK`, sin corresponder afirmar superioridad absoluta de una sobre otra:

- **La modalidad de Agente Único (`CORRIDA-LB-01`)** requirió **menos tiempo activo registrado y menos coordinación**, resolviendo por sí misma dos incidentes internos de entorno/empaquetado (`0` intervenciones humanas durante la corrida). Sin embargo, sin auditoría independiente dejaron de detectarse una aserción tautológica en `SYN-INJ-OK` (equivalente a `H-01`) y una acción recomendada genérica ante `E-207` con `SRV-MOD` operativo y otro servicio dependiente caído que no identifica al servicio bloqueante (debilidad comparable, aunque no idéntica en redacción, a `H-02` de la modalidad multiagente), además de exponer mensajes `403` diferenciados entre usuario inexistente y rol no autorizado.
- **La modalidad Multiagente (`CORRIDA-MA-01`)** implicó mayor coordinación formal y mayor tiempo total transcurrido entre hitos hasta su cierre en `e998cca`. A cambio, aportó trazabilidad por etapas, separación arquitectónica verificada por AST entre dominio puro y FastAPI, respuesta `403` uniforme y normalización Excel defensiva; de forma destacada, **su revisión independiente (`revisor`) permitió descubrir y corregir dos observaciones verificadas (`H-01` y `H-02`)** que habían quedado ocultas tras una primera suite en verde (`46/46`).
