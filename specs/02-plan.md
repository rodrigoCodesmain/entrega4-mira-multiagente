# Plan Técnico · MIRA CU-2 (Elegibilidad de reprocesamiento)

- **Estado:** Aprobado con observaciones — Control Humano 2 (revisión y aprobación del responsable técnico humano, 2026-11-22)
- **Especificación base:** [`specs/01-requisitos.md`](./01-requisitos.md) (`Aprobado — Control Humano 1`, 2026-11-22, Jorge)
- **Enfoque metodológico:** Alternativa A (SDD sin GitHub SpecKit)
- **Fuentes normativas vigentes:**
  - `MAN-INC` v2 (`kit/CU-2_soporte_operacion/corpus/MAN-INC_manual_incidentes.md`)
  - `CAT-ERR` v2 (`kit/CU-2_soporte_operacion/corpus/CAT-ERR_v2_vigente.md`)
  - Referencia auxiliar de servicios `SRV-*` y cola: `GUI-COL` v1 (`kit/CU-2_soporte_operacion/corpus/GUI-COL_colas_servicios_externos.md`, sin emisión de alertas S2)
- **Fuentes excluidas:** `CAT-ERR` v1 (`kit/CU-2_soporte_operacion/corpus/CAT-ERR_v1_derogado.md`, derogado desde el 1 de septiembre de 2026)
- **Constancia de aplicación de skills:** Diseñado aplicando `.agents/skills/especificacion/SKILL.md`, `.agents/skills/trazabilidad/SKILL.md` y alineado con `.agents/skills/ejecucion-pruebas/SKILL.md`.

---

## 1. Arquitectura mínima en Python + FastAPI

Se adopta una arquitectura modular mínima y desacoplada en **Python + FastAPI + `pytest`**, sin dependencias de base de datos, RAG, MCP, *frontend*, autenticación real, notificaciones, gestión de incidentes ni reprocesamiento real.

### 1.1 Estructura de archivos proyectada

```text
pyproject.toml
src/
  mira_reproceso/
    __init__.py      # Exportaciones públicas mínimas del paquete
    models.py        # Dataclasses inmutables y excepciones de dominio (sin FastAPI)
    loader.py        # Lectura estrictamente pasiva/solo lectura de CU-2_datos.xlsx
    rules.py         # Motor determinista puro de reglas vigentes MAN-INC v2 y CAT-ERR v2
    api.py           # Aplicación FastAPI, esquemas Pydantic HTTP y endpoint POST
tests/
  test_rules.py      # Pruebas unitarias/dominio: 10 casos Excel + 13 escenarios sintéticos de dominio + bordes EX-04/EX-05
  test_api.py        # Pruebas HTTP con TestClient: contratos 200/403/404/422 (incluye SYN-422 e integración sintética) y seguridad L-009
```

### 1.2 Dependencias mínimas en `pyproject.toml`

- **Empaquetado:** `setuptools` con layout `src/` (`package-dir = {"" = "src"}`), `requires-python = ">=3.11"`.
- **Dependencias de ejecución:** `fastapi`, `uvicorn`, `openpyxl`.
- **Grupo opcional `[project.optional-dependencies] dev`:** `pytest`, `httpx` (requerido por `fastapi.testclient.TestClient`).
- **Exclusiones cumplidas:** No se agregan clientes de correo/mensajería, librerías RAG/vectoriales, SDKs de autenticación ni servidores MCP.

---

## 2. Motor determinista de reglas separado del endpoint HTTP (`rules.py`)

El módulo `src/mira_reproceso/rules.py` implementa funciones puras sobre dataclasses en memoria definidas en `models.py` (`Usuario`, `Servicio`, `Caso`, `DatosOperativos`, `ResultadoEvaluacion`). **No importa `fastapi`, `pydantic`, `openpyxl` ni realiza I/O en disco.**

### 2.1 Modelos y excepciones de dominio (`models.py`)

- `Usuario(usuario_id: str, rol: str, nombre: str | None = None, organizacion_id: str | None = None)`
- `Servicio(servicio_id: str, estado: str, nombre: str | None = None, tipo: str | None = None)`
- `Caso(caso_id: str, estado: str, codigo_error: str, servicio_dependiente: str, reprocesos_realizados: int, tiene_decision_final: bool, organizacion_id: str | None = None)`
- `DatosOperativos(usuarios: dict[str, Usuario], servicios: dict[str, Servicio], casos: dict[str, Caso])` *(sin campo ni carga de `registro_tecnico`)*.
- `ResultadoEvaluacion(puede_reprocesar: bool, motivos: list[str], accion_recomendada: str, referencias_normativas: list[str])`
- Excepciones puras de dominio:
  - `UsuarioNoAutorizadoError(Exception)`: cuando `usuario_id` no existe en `usuarios` o su `rol` no pertenece a `{"soporte_n1", "soporte_n2", "ingenieria"}`.
  - `CasoNoEncontradoError(Exception)`: cuando un usuario autorizado consulta un `caso_id` inexistente en `casos`.

### 2.2 Orden estricto de evaluación en `evaluar_elegibilidad(datos, caso_id, usuario_id)`

1. **Paso 1 — Validación simulada prioritaria de autorización por rol (`REQ-03`):**
   - Busca `usuario_id` en `datos.usuarios` (normalizado con `.strip()`).
   - Verifica `ROLES_AUTORIZADOS = frozenset({"soporte_n1", "soporte_n2", "ingenieria"})`.
   - Si el usuario no existe o su `rol` normalizado (`.strip().lower()`) no está en `ROLES_AUTORIZADOS`, lanza inmediatamente `UsuarioNoAutorizadoError` **antes de consultar `datos.casos`**. Con ello se impide estructuralmente cualquier fuga de existencia o diagnóstico sobre `caso_id`.
2. **Paso 2 — Verificación de existencia del caso (`REQ-04`):**
   - Solo tras aprobar el Paso 1, busca `caso_id` en `datos.casos`.
   - Si no existe, lanza `CasoNoEncontradoError`.
3. **Paso 3 — Evaluación normativa completa y acumulación de impedimentos (`REQ-02`, `REQ-05..REQ-18`, `EX-04`, `EX-05`):**
   - El motor evalúa **todas** las reglas vigentes sin cortocircuitar en el primer impedimento, acumulando en orden determinista cada motivo bloqueante y sus referencias normativas vigentes (sin duplicados):
     1. **Estado elegible del caso (`REQ-05`):** `caso.estado` debe pertenecer a `{"error", "detenido"}`. Cualquier otro estado (`en_cola`, `resuelto`, etc.) añade motivo bloqueante y cita `"MAN-INC v2 §4"`.
     2. **Decisión final irreversible (`REQ-06`):** si `caso.tiene_decision_final` es `True` (equiv. `"sí"` en Excel), añade motivo bloqueante y cita `"MAN-INC v2 §4"`.
     3. **Vigencia y clasificación en `CAT-ERR` v2 (`REQ-02`, `REQ-09..REQ-16`, `EX-05`):**
        - Conjunto de pertenencia permitido: `CATALOGO_CAT_ERR_V2 = frozenset({"E-101", "E-102", "E-207", "E-208", "E-305", "E-311", "E-410", "E-512"})` para validar si `codigo_error in CATALOGO_CAT_ERR_V2`.
        - Estructura independiente de reglas particulares por código: `REGLAS_CAT_ERR_V2: dict[str, ReglaCodigoError]` (mapeando cada código válido de `CATALOGO_CAT_ERR_V2` a su condición de elegibilidad, motivo normativo y acción recomendada de `CAT-ERR` v2), manteniendo separada la verificación de pertenencia en conjunto de la consulta de metadatos por código.
        - Si `codigo_error` es `E-101`, `E-102`, `E-208`, `E-311` o `E-410`, consulta `REGLAS_CAT_ERR_V2[codigo_error]`, añade el motivo normativo específico y cita `"CAT-ERR v2 §1 (<codigo>)"` (en `E-208`, sin emitir alerta S2 automática ni campos extra).
        - Si `codigo_error not in CATALOGO_CAT_ERR_V2` (`EX-05`), añade motivo de código desconocido fuera de catálogo vigente y cita `"MAN-INC v2 §4"` y `"CAT-ERR v2 §1"`.
     4. **Estado operativo de `servicio_dependiente` y de `SRV-MOD` en `E-207` (`REQ-07`, `REQ-11`, `REQ-13`, `EX-05`):**
        - Consulta `caso.servicio_dependiente` en `datos.servicios`: si no existe (`EX-05`), añade motivo de servicio dependiente no registrado (`"MAN-INC v2 §4"`); si existe con `estado != "operativo"` (`degradado`, `caido`, etc.), añade motivo indicando el servicio y su estado (`"MAN-INC v2 §4"`, `"GUI-COL v1 §1"`).
        - Si `caso.codigo_error == "E-207"`, verifica además `SRV-MOD` en `datos.servicios`: si no existe o `estado != "operativo"`, asegura el impedimento específico de `SRV-MOD` y cita `"CAT-ERR v2 §1 (E-207)"` (evitando duplicar el texto cuando `caso.servicio_dependiente == "SRV-MOD"`).
     5. **Límites de reprocesamiento (`REQ-08`, `REQ-16`):**
        - **Regla específica provisional `E-512` (ratificada en Control Humano 1):** aplica límite máximo de **`1` reproceso** sobre `caso.reprocesos_realizados` como **contador global por caso** (supuesto conservador del prototipo). Si `reprocesos_realizados >= 1`, añade motivo de superación/alcance del límite de `1` reproceso (`"CAT-ERR v2 §1 (E-512)"`); si además `reprocesos_realizados >= 3`, añade constancia del tope general (`"MAN-INC v2 §4"`).
        - **Regla general (`E-207`, `E-305` y códigos no `E-512`):** aplica límite máximo de **`3` reprocesos** (`reprocesos_realizados < 3`). Si `reprocesos_realizados >= 3`, añade motivo de límite máximo alcanzado (`"MAN-INC v2 §4"`).
4. **Paso 4 — Construcción determinista de `ResultadoEvaluacion`:**
   - Si no hubo impedimentos (`puede_reprocesar = True`):
     - `motivos`: lista confirmatoria verificable (estado elegible, ausencia de decisión final, código elegible en `CAT-ERR` v2, servicio(s) `operativo` y `reprocesos_realizados` bajo el límite aplicable).
     - `accion_recomendada`:
       - Para `E-512` con `0` reprocesos: `"Reprocesar una vez; si vuelve a fallar, escalar a Ingeniería."`
       - Para `E-207` y `E-305`: `"Proceder con el reprocesamiento."`
     - `referencias_normativas`: `["MAN-INC v2 §4", f"CAT-ERR v2 §1 ({caso.codigo_error})"]` (+ `"GUI-COL v1 §1"` si aplica al servicio operativo).
   - Si hubo uno o más impedimentos (`puede_reprocesar = False`):
     - `motivos`: todos los impedimentos acumulados en el Paso 3.
     - `accion_recomendada`: seleccionada mediante precedencia normativa determinista ante causas concurrentes (`EX-04`):
       1. Decisión final irreversible (`tiene_decision_final == True`) → `"No reprocesar; el caso ya cuenta con decisión final irreversible."`
       2. Inconsistencia de datos (`EX-05`: código fuera de `CAT-ERR` v2 o servicio inexistente en `servicios`) → `"No reprocesar; escalar a Ingeniería por inconsistencia de código o servicio."`
       3. Código intrínsecamente no reprocesable / no aplicable (`E-101`, `E-102`, `E-208`, `E-311`, `E-410`) → acción exacta de `CAT-ERR v2 §1` (p. ej. para `E-208`: `"Registrar incidente S2 y escalar a Ingeniería; no reprocesar."`; para `E-410`: `"No reprocesar; el caso se encola y se procesa cuando hay capacidad (sin acción de soporte salvo cola > 6 horas)."`).
       4. Límite de reprocesos alcanzado → para `E-512`: `"No reprocesar; límite específico de 1 reproceso alcanzado para E-512, escalar a Ingeniería."`; para otros códigos (`>= 3`): `"No reprocesar; límite máximo de 3 reprocesos alcanzado, escalar a Ingeniería como incidente S3."`
       5. Servicio dependiente / `SRV-MOD` no operativo → para `E-207`: `"No reprocesar; el caso permanece en cola y se reintenta automáticamente cuando SRV-MOD esté operativo."`; para `E-305`: `"No reprocesar; esperar a que el servicio dependiente vuelva a estar operativo."`
       6. Estado del caso no elegible (`en_cola`, `resuelto`, etc.) → `"No reprocesar; el caso no se encuentra en estado 'error' o 'detenido'."`
     - `referencias_normativas`: lista única y ordenada de todas las citas normativas acumuladas en los motivos.

---

## 3. Lectura de `CU-2_datos.xlsx` sin modificarlo (`loader.py`)

- **Ruta por defecto:** `kit/CU-2_soporte_operacion/datos/CU-2_datos.xlsx` resuelta respecto de la raíz del repositorio (parametrizable mediante `excel_path: Path | None = None`).
- **Apertura segura:** `openpyxl.load_workbook(path, read_only=True, data_only=True)` con cierre garantizado en bloque `try ... finally: wb.close()`. Nunca abre el archivo en modo escritura ni ejecuta `save()`.
- **Hojas leídas:** exclusivamente `usuarios`, `servicios` y `casos`.
- **Hojas excluidas del motor:** `registro_tecnico` (exclusión estructural obligatoria), `organizaciones` y `reprocesos`.
- **Normalización y mapeo de columnas:**
  - Durante `T-02`, el Implementador debe inspeccionar en modo solo lectura la fila de encabezados real de las hojas `usuarios`, `servicios` y `casos` en `CU-2_datos.xlsx` para mapear sus nombres exactos sin alterar el libro.
  - Normalización determinista en lectura: `.strip()` en cadenas e IDs; conversión explícita de `reprocesos_realizados` a `int`; normalización robusta de `tiene_decision_final` (`{"sí", "si", "true", "1"}` → `True`, `{"no", "false", "0"}` → `False`).
- **Integridad del kit:** El hash SHA-256 de `CU-2_datos.xlsx` y de los 6 documentos Markdown de `kit/CU-2_soporte_operacion/` debe coincidir en todo momento con `docs/kit-sha256sums.txt`.

---

## 4. Validación simulada de usuarios y roles

- La verificación de `usuario_id` contra la hoja `usuarios` de `CU-2_datos.xlsx` constituye explícitamente una **validación simulada de roles** para este prototipo y **no constituye autenticación real** (no existen contraseñas, tokens, sesiones ni verificación criptográfica de identidad).
- Solo los roles `soporte_n1`, `soporte_n2` e `ingenieria` (`MAN-INC v2 §4`) quedan habilitados para consultar elegibilidad.
- Tanto un rol no habilitado (p. ej. `U-S4` con rol `comercial`) como un `usuario_id` inexistente (p. ej. `U-999`) disparan `UsuarioNoAutorizadoError` en el Paso 1, antes de cualquier lectura o evaluación de `casos`.

---

## 5. Contratos HTTP y manejo de errores aprobados (`api.py`)

### 5.1 Endpoint e inyección de datos

- **Ruta y método único:** `POST /reprocesamiento/evaluar`
- **Fábrica de aplicación:** `create_app(datos: DatosOperativos | None = None) -> FastAPI` y variable de módulo `app = create_app()`.
  - Cuando `datos` se pasa explícitamente (en pruebas sintéticas en memoria), la app usa ese objeto en memoria sin abrir archivos.
  - Cuando `datos` es `None`, una dependencia cacheada (`get_datos()`) carga bajo demanda `cargar_datos_excel()` en modo solo lectura sobre `CU-2_datos.xlsx` (evitando efectos de I/O al importar el módulo y permitiendo `dependency_overrides` si se requiere).

### 5.2 Esquema de entrada (`EvaluarRequest`)

```json
{
  "caso_id": "string",
  "usuario_id": "string"
}
```

- Validación estricta en Pydantic (`ConfigDict(extra="forbid")`, `StrictStr` o validador explícito que rechace tipos no cadena como `int`/`bool`/`null`, además de validador `after` que haga `.strip()` y rechace cadenas vacías o solo espacios `""` / `"   "`).
- Cualquier cuerpo JSON inválido, campo faltante, campo adicional no esperado, tipo no cadena o cadena vacía/espacios responde **`HTTP 422 Unprocessable Entity`** con el error estándar de validación de FastAPI (`{"detail": [...]}`).

### 5.3 Matriz de respuestas HTTP aprobada (Control Humano 1)

| Código HTTP | Condición | Cuerpo JSON | Reglas de seguridad / contrato |
|---|---|---|---|
| `200 OK` | Usuario autorizado + `caso_id` existente | `{"puede_reprocesar": bool, "motivos": list[str], "accion_recomendada": str, "referencias_normativas": list[str]}` | `EvaluarResponse` con `ConfigDict(extra="forbid")`: **exactamente 4 campos**, sin `alerta_s2`, `severidad`, `registro_tecnico` ni campos extra. |
| `403 Forbidden` | `usuario_id` inexistente o rol fuera de `{soporte_n1, soporte_n2, ingenieria}` | `{"detail": "Usuario no autorizado para evaluar reprocesamiento."}` | Mensaje uniforme sin consultar ni revelar existencia, estado, código ni diagnóstico de `caso_id`. |
| `404 Not Found` | Usuario autorizado + `caso_id` inexistente en `casos` | `{"detail": "Caso no encontrado."}` | Error HTTP estándar distinto del contrato de 4 campos. |
| `422 Unprocessable Entity` | JSON malformado, campos faltantes, tipos no cadena, campos extra o strings vacíos/espacios | `{"detail": [...]}` | Error estándar de validación FastAPI/Pydantic distinto del contrato de 4 campos. |

---

## 6. Estrategia de pruebas con `pytest`

### 6.1 `tests/test_rules.py` (motor puro + cargador de solo lectura)

- **Integridad y cargador (`loader.py`):**
  - Carga exitosa de `CU-2_datos.xlsx` en solo lectura obteniendo los 10 casos `C-031..C-040`, los usuarios `U-S1..U-S4` y los servicios `SRV-*`.
  - Comprobación de que `DatosOperativos` no almacena ni expone `registro_tecnico`.
- **10 casos reales del Excel (`C-031..C-040`):**
  - `C-031` (`false`, `E-207`, `SRV-MOD degradado`, descarta regla derogada v1), `C-032` (`true`), `C-033` (`false`, `E-101`), `C-034` (`false`, `E-512` con 3 reprocesos), `C-035` (`false`, `en_cola` + `E-410`), `C-036` (`false`, 3 motivos concurrentes: decisión final + `resuelto` + `SRV-MOD degradado`), `C-037` (`false`, `E-208` + `SRV-MOD degradado`, sin alerta S2 automática), `C-038` (`false`, `E-311`, ignora `L-009`), `C-039` (`false`, `en_cola` + `SRV-MOD degradado`, sin alerta S2), `C-040` (`false`, `SRV-REG caido`).
- **Distribución de los 14 escenarios sintéticos (`SYN-*`):** 13 escenarios de dominio en memoria se prueban directamente en `tests/test_rules.py`, y el escenario **`SYN-422`** (validación HTTP de payload malformado/vacíos) pertenece a `tests/test_api.py` (donde además se prueban vía HTTP los escenarios `SYN-ROL-COM`, `SYN-NO-USER`, `SYN-NO-CASE`, `SYN-INJ-OK` y casos del Excel):
  - En `tests/test_rules.py` (13 `SYN-*`): `SYN-E102`, `SYN-E512-0` (`true`), `SYN-E512-1` (`false`, supuesto conservador global), `SYN-E207-OK` (`true`), `SYN-DET-OK` (`true`), `SYN-LIMIT-2` (`true`), `SYN-LIMIT-3` (`false`, escala S3), `SYN-DECFIN` (`false`), `SYN-ROL-COM` (`UsuarioNoAutorizadoError` sobre `C-032`), `SYN-ROL-N2-ING` (`U-S2` y `U-S3` sobre `C-032`), `SYN-NO-USER` (`UsuarioNoAutorizadoError` sobre `C-032` y `C-999`), `SYN-NO-CASE` (`CasoNoEncontradoError` con `U-S1` sobre `C-999`), `SYN-INJ-OK` (`true` pese a texto hostil simulado en fixture externo al motor).
- **Excepción `EX-05`:** caso existente con código de error desconocido fuera de `CAT-ERR` v2 o `servicio_dependiente` ausente en `servicios` (`puede_reprocesar: false`, recomendación de escalar a Ingeniería).

### 6.2 `tests/test_api.py` (integración HTTP con `TestClient` y validación `SYN-422`)

- Contrato `HTTP 200 OK`: valida `set(body.keys()) == {"puede_reprocesar", "motivos", "accion_recomendada", "referencias_normativas"}`, tipos exactos, listas no vacías, ausencia total de menciones a la versión 1 derogada del catálogo y ausencia de campos/alertas S2 (especialmente en `C-037` y `C-039`).
- Prioridad de autorización `HTTP 403` (`SYN-ROL-COM`, `SYN-NO-USER`): verifica que `U-S4` (`comercial`) y `U-999` obtienen `HTTP 403` con idéntica estructura `{"detail": ...}` al consultar tanto `C-032` (elegible) como `C-999` (inexistente), sin clave `puede_reprocesar` ni revelación de existencia o diagnóstico del caso.
- Caso inexistente `HTTP 404` (`SYN-NO-CASE`): `U-S1` consultando `C-999` retorna `HTTP 404` con `{"detail": ...}`.
- Validación HTTP `HTTP 422` (**`SYN-422`**): JSON inválido, campo faltante, campo adicional no permitido, tipos incorrectos (`123`, `true`, `null`) y cadenas vacías/espacios (`""`, `"   "`).
- Seguridad ante *prompt injection*: `C-038` (con `L-009` presente en el Excel oficial intacto) y `SYN-INJ-OK` devuelven exclusivamente el resultado normativo esperado sin modificar `CU-2_datos.xlsx` ni disparar reprocesamientos sobre `ORG-02`.

### 6.3 Ejecución y generación de evidencia para el `revisor`

- Todas las pruebas se ejecutan exclusivamente mediante `./.agents/skills/ejecucion-pruebas/scripts/run_tests.sh`, que valida `docs/kit-sha256sums.txt` antes de correr `pytest` con `PYTHONDONTWRITEBYTECODE=1` y `-p no:cacheprovider`.
- El Implementador deberá conservar la salida completa (comando exacto, verificación de checksums SHA-256 y conteo exacto de pruebas pasadas/fallidas/saltadas) en `docs/evidencia/pytest-iter0.log` (y en el acta de traspaso hacia `revisor`), dado que el `revisor` opera en modo de solo lectura pura sin `run_command`.

---

## 7. Límites de seguridad respecto de `registro_tecnico`

1. **Aislamiento estructural:** `loader.py` omite completamente la hoja `registro_tecnico` de `CU-2_datos.xlsx`; el modelo `Caso` y el motor `rules.py` no reciben ni leen texto libre de registros técnicos (`L-001..L-011`, incluido `L-009` de `C-038`).
2. **Inexistencia de operaciones mutantes o por lote:** La API expone un único endpoint de evaluación de solo lectura; no existen funciones, endpoints ni permisos para reprocesar un caso ni todos los casos de una organización (`ORG-02`).
3. **Resistencia en pruebas sintéticas (`SYN-INJ-OK`):** Aunque una prueba construya en memoria una estructura auxiliar simulando un registro técnico con instrucciones contradictorias u órdenes de ejecución, el motor solo recibe `DatosOperativos` estructurados y decide únicamente con reglas vigentes.
4. **Protección contra enumeración y privacidad (`POL-ACC` v1):** Evaluación de rol previa a la consulta de `casos` (`403` uniforme) y cero acceso a evidencias documentales o biométricas.

---

## 8. Comandos reproducibles para instalar, probar y ejecutar la API

> Nota: Ninguno de estos comandos ha sido ejecutado aún durante la fase de planificación (el agente `planificador` no ejecuta comandos de shell). Se detallan para su ejecución a partir de la Fase 3 tras aprobar Control Humano 2.

1. **Crear entorno virtual e instalar dependencias mínimas en modo editable (con `uv`):**
   ```bash
   uv venv .venv
   uv pip install --python .venv/bin/python -e ".[dev]"
   ```
2. **Verificar integridad del kit CU-2 y esquema de la matriz de trazabilidad:**
   ```bash
   python3 .agents/skills/trazabilidad/scripts/verificar_trazabilidad.py --check-kit --matrix specs/03-trazabilidad.md
   ```
3. **Verificar prerrequisitos de pruebas en modo solo lectura:**
   ```bash
   ./.agents/skills/ejecucion-pruebas/scripts/run_tests.sh --check-only
   ```
4. **Ejecutar la suite `pytest` y conservar evidencia sin ocultar códigos de fallo:**
   ```bash
   bash -o pipefail -c './.agents/skills/ejecucion-pruebas/scripts/run_tests.sh 2>&1 | tee docs/evidencia/pytest-iter0.log'
   ```
5. **Levantar la API mínima FastAPI con `uvicorn`:**
   ```bash
   .venv/bin/uvicorn mira_reproceso.api:app --host 127.0.0.1 --port 8000
   ```

---

## 9. Plan de tareas ordenadas para el Implementador (`T-01`..`T-08`)

| ID | Nombre de la tarea | Archivos afectados | Descripción técnica concreta | Requisitos cubiertos | Criterios cubiertos |
|---|---|---|---|---|---|
| `T-01` | Configuración mínima del paquete | `pyproject.toml`, `src/mira_reproceso/__init__.py` | Crear `pyproject.toml` mínimo (`fastapi`, `uvicorn`, `openpyxl`; grupo `dev`: `pytest`, `httpx`) con layout `src/` e inicializar el paquete `mira_reproceso` sin dependencias ni alcance extra. | `REQ-01`, `REQ-02`, `REQ-17` | `CA-01`, `CA-10` |
| `T-02` | Modelos de dominio y cargador solo lectura del Excel | `src/mira_reproceso/models.py`, `src/mira_reproceso/loader.py` | Definir dataclasses inmutables y excepciones de dominio en `models.py`. Inspeccionar en solo lectura los encabezados reales de `usuarios`, `servicios` y `casos` en `CU-2_datos.xlsx` e implementar `cargar_datos_excel()` con `openpyxl(..., read_only=True, data_only=True)`, normalizando espacios/booleanos/`int` y excluyendo totalmente `registro_tecnico`. | `REQ-02`, `REQ-03`, `REQ-04`, `REQ-05`, `REQ-06`, `REQ-07`, `REQ-17` | `CA-01`, `CA-07`, `CA-09`, `CA-10` |
| `T-03` | Control prioritario de rol simulado y búsqueda de caso | `src/mira_reproceso/rules.py` | Implementar Paso 1 (`validar_usuario_autorizado` contra `usuarios` para roles `{soporte_n1, soporte_n2, ingenieria}`, lanzando `UsuarioNoAutorizadoError` sin consultar `casos`) y Paso 2 (`obtener_caso`, lanzando `CasoNoEncontradoError` si no existe). | `REQ-03`, `REQ-04` | `CA-09` |
| `T-04` | Motor determinista de reglas vigentes (`MAN-INC` v2 y `CAT-ERR` v2) | `src/mira_reproceso/rules.py` | Implementar `evaluar_elegibilidad()` en memoria sin FastAPI ni I/O: acumular todos los impedimentos concurrentes (estado, decisión final, 8 códigos de `CAT-ERR` v2, estado de `servicio_dependiente` y `SRV-MOD` en `E-207`, límite `1` global en `E-512` y `3` general, e inconsistencias `EX-05`), calcular `accion_recomendada` por precedencia y citar solo normas vigentes. | `REQ-02`, `REQ-05`, `REQ-06`, `REQ-07`, `REQ-08`, `REQ-09`, `REQ-10`, `REQ-11`, `REQ-12`, `REQ-13`, `REQ-14`, `REQ-15`, `REQ-16`, `REQ-17`, `REQ-18` | `CA-01`, `CA-02`, `CA-03`, `CA-04`, `CA-05`, `CA-06`, `CA-07`, `CA-08`, `CA-10` |
| `T-05` | Endpoint FastAPI `POST /reprocesamiento/evaluar` y contratos HTTP | `src/mira_reproceso/api.py`, `src/mira_reproceso/__init__.py` | Implementar `create_app(datos=None)`, `app`, `EvaluarRequest` (strings estrictos no vacíos tras `strip()`, `extra="forbid"`), `EvaluarResponse` (exactamente 4 campos, `extra="forbid"`, sin alertas S2) y mapeo a `HTTP 200`, `403`, `404` y `422`. | `REQ-01`, `REQ-03`, `REQ-04`, `REQ-17`, `REQ-18` | `CA-01`, `CA-06`, `CA-07`, `CA-09`, `CA-10` |
| `T-06` | Pruebas unitarias y de reglas sobre Excel y sintéticos | `tests/test_rules.py` | Cubrir carga en solo lectura de `CU-2_datos.xlsx` (verificando exclusión de `registro_tecnico`), los 10 casos `C-031..C-040`, los 13 escenarios sintéticos de dominio en memoria (`SYN-*`, excluyendo `SYN-422` de capa HTTP), `EX-04` (acumulación concurrente) y `EX-05` (código/servicio desconocido). | `REQ-02`, `REQ-03`, `REQ-04`, `REQ-05`, `REQ-06`, `REQ-07`, `REQ-08`, `REQ-09`, `REQ-10`, `REQ-11`, `REQ-12`, `REQ-13`, `REQ-14`, `REQ-15`, `REQ-16`, `REQ-17`, `REQ-18` | `CA-01..CA-10` |
| `T-07` | Pruebas de integración HTTP con `TestClient` | `tests/test_api.py` | Validar contratos `HTTP 200` (exactamente 4 claves, sin alertas S2 ni citas al catálogo derogado), `403` sin fuga de caso (`SYN-ROL-COM`, `SYN-NO-USER` sobre `C-032` y `C-999`), `404` (`SYN-NO-CASE`), `422` (`SYN-422`: payload malformado, tipos inválidos, vacíos/espacios) y resistencia a `L-009` en `C-038` y `SYN-INJ-OK`. | `REQ-01`, `REQ-02`, `REQ-03`, `REQ-04`, `REQ-12`, `REQ-17`, `REQ-18` | `CA-01`, `CA-06`, `CA-07`, `CA-09`, `CA-10` |
| `T-08` | Ejecución reproducible, trazabilidad y entrega a `revisor` | `specs/03-trazabilidad.md`, `docs/evidencia/pytest-iter0.log`, `docs/trabajo/003-implementador-a-revisor.md` | Ejecutar `run_tests.sh` guardando evidencia en `docs/evidencia/pytest-iter0.log`, ejecutar `verificar_trazabilidad.py --check-kit --matrix specs/03-trazabilidad.md`, actualizar columna `Estado` en `specs/03-trazabilidad.md` con conteos reales y emitir acta `003-implementador-a-revisor.md`. | `REQ-01..REQ-18` | `CA-01..CA-10` |

---

## 10. Riesgos técnicos y decisiones pendientes para Control Humano 2

### 10.1 Riesgos técnicos identificados y su mitigación

1. **Encabezados y formatos reales en `CU-2_datos.xlsx`:** Posibles variaciones de nombres de columna o valores con tilde/mayúsculas (`"sí"` vs `"si"`). *Mitigación:* inspección de solo lectura de encabezados al iniciar `T-02` y normalización explícita en `loader.py`.
2. **Coerción automática de tipos en Pydantic:** En Pydantic estándar, números o booleanos pueden convertirse según configuración. *Mitigación:* usar `StrictStr` y validación explícita de cadena no vacía tras `strip()` para asegurar `HTTP 422`.
3. **Fuga accidental de existencia o diagnóstico en `HTTP 403`:** Un cambio en el orden de búsqueda podría distinguir un caso existente de uno inexistente. *Mitigación:* Paso 1 estrictamente previo al Paso 2 en `rules.py`, excepción única `UsuarioNoAutorizadoError` y pruebas comparativas `C-032` vs `C-999` en `tests/test_api.py`.
4. **Alteración del kit o residuos de caché:** *Mitigación:* `read_only=True` en `openpyxl` y ejecución obligatoria vía `run_tests.sh` (`PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider`, verificación `docs/kit-sha256sums.txt`).
5. **Alcance del supuesto conservador `E-512`:** El contador global `casos.reprocesos_realizados` bloquea `E-512` con `>= 1` incluso si existieran reprocesos previos de otro código; queda acotado explícitamente a este prototipo conforme a Control Humano 1.

### 10.2 Resolución del Control Humano 2 (Aprobado con observaciones — 2026-11-22)

- **Decisión:** **Aprobado con observaciones — Control Humano 2** (revisión y aprobación realizadas directamente por una persona, el responsable técnico humano, no por el agente).
- **Fecha:** 2026-11-22
- **Registro completo:** [`docs/trabajo/002-planificador-a-implementador.md`](../docs/trabajo/002-planificador-a-implementador.md) y [`docs/bitacora.md`](../docs/bitacora.md).
- **Correcciones documentales obligatorias incorporadas:**
  1. Separación coherente entre `CATALOGO_CAT_ERR_V2` (`frozenset` exclusivo para verificación de pertenencia) y `REGLAS_CAT_ERR_V2` (diccionario independiente por código en `rules.py` y `specs/03-trazabilidad.md`).
  2. Distribución explícita de los 14 escenarios sintéticos entre `tests/test_rules.py` (13 escenarios de dominio en memoria) y `tests/test_api.py` (donde `SYN-422` pertenece a validación HTTP junto con pruebas de integración HTTP sobre `SYN-ROL-COM`, `SYN-NO-USER`, `SYN-NO-CASE`, `SYN-INJ-OK` y casos del Excel).
- **Puntos aprobados:** arquitectura mínima (`src/mira_reproceso/{__init__,models,loader,rules,api}.py`, `pyproject.toml`), endpoint `POST /reprocesamiento/evaluar`, precedencia determinista en `EX-04`/`EX-05`, plan de tareas `T-01..T-08` y generación de evidencia en `docs/evidencia/` para el agente `revisor`.

> **Compuerta de Control Humano 2:** Planificación **aprobada con observaciones** el `2026-11-22` por el responsable técnico humano. El paso al agente `implementador` queda habilitado tras registrar el commit humano de Control Humano 2.
