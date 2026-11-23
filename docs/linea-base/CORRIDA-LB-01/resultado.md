# Resultado del Experimento CORRIDA-LB-01 (Línea Base de Agente Único)

## 1. Identificación de modalidad, modelo y configuración

- **Modalidad de ejecución:** Agente único en un solo hilo de trabajo dentro de `/home/lester/Documents/mira-cu2-linea-base-aislada`, ejecutando análisis, diseño técnico, implementación, pruebas, corrección de defectos y documentación directamente sin uso de `invoke_subagent`, sin roles Implementador/Revisor y sin actas de traspaso en `docs/trabajo/`.
- **Modelo y entorno disponibles:** Modelo seleccionado Orchestrator (Neon) en Antigravity (con fase de planificación y fase de ejecución dentro de la misma conversación), ejecutado sobre Linux con `uv 0.13.8`, `CPython 3.12.14` (`.venv`), `fastapi 0.165.0`, `pydantic 2.14.4`, `openpyxl 3.1.5`, `httpx 0.28.1` y `pytest 9.2.0`.
- **Ventana temporal capturada (`date -Is`):**
  - Inicio: `2026-11-22T21:34:35-03:00`
  - Término de verificación final: `2026-11-22T21:42:09-03:00`

## 2. Tareas realizadas

1. Inventario del workspace, verificación inicial en modo solo lectura de `docs/kit-sha256sums.txt` mediante `.agents/skills/ejecucion-pruebas/scripts/run_tests.sh --check-only` y `.agents/skills/trazabilidad/scripts/verificar_trazabilidad.py --check-kit`, e inspección de solo lectura de `kit/CU-2_soporte_operacion/datos/CU-2_datos.xlsx`.
2. Lectura y análisis de `specs/01-requisitos.md` (aprobada en Control Humano 1) junto con las fuentes normativas vigentes `MAN-INC` v2, `CAT-ERR` v2, `GUI-COL` v1 y `POL-ACC` v1 (excluyendo `CAT-ERR` v1 como derogado).
3. Definición del plan técnico y configuración de `pyproject.toml` con entorno virtual en `.venv` usando `uv sync --python 3.12`.
4. Implementación del paquete `src/mira_cu2/`:
   - Modelos de dominio, excepciones y esquemas Pydantic v2 estrictos (`models.py`).
   - Repositorios de solo lectura en memoria y sobre `CU-2_datos.xlsx` aislando completamente la hoja `registro_tecnico` (`repository.py`).
   - Motor determinista de reglas normativas con evaluación prioritaria de rol y recolección completa de motivos bloqueantes concurrentes (`rules.py`).
   - Aplicación FastAPI mínima con `POST /elegibilidad` (`api.py`, `__init__.py`).
5. Creación de la suite de pruebas en `tests/` cubriendo los 10 casos del Excel (`C-031`..`C-040`), los 14 escenarios sintéticos (`SYN-*`), casos borde (`EX-05`), prioridad de rol sin consulta a `casos` (`HTTP 403`), aislamiento ante `L-009` e integridad SHA-256.
6. Creación de la matriz normativa `specs/03-trazabilidad.md` y guía de uso en `README.md`.
7. Ejecución completa de `./.agents/skills/ejecucion-pruebas/scripts/run_tests.sh`, verificación de trazabilidad con `verificar_trazabilidad.py`, corrección de los 2 defectos detectados durante la primera ejecución y captura de evidencias en `docs/linea-base/CORRIDA-LB-01/`.

## 3. Archivos creados

- `pyproject.toml`, `uv.lock`, `README.md`
- `src/mira_cu2/__init__.py`, `src/mira_cu2/models.py`, `src/mira_cu2/repository.py`, `src/mira_cu2/rules.py`, `src/mira_cu2/api.py`
- `tests/__init__.py`, `tests/conftest.py`, `tests/test_casos_excel.py`, `tests/test_escenarios_sinteticos.py`, `tests/test_seguridad.py`
- `specs/03-trazabilidad.md`
- `docs/linea-base/CORRIDA-LB-01/prompt-ejecucion.md`
- `docs/linea-base/CORRIDA-LB-01/pytest.log`
- `docs/linea-base/CORRIDA-LB-01/metricas.md`
- `docs/linea-base/CORRIDA-LB-01/resultado.md`

*(No se modificó ningún archivo de `kit/CU-2_soporte_operacion/`, `specs/01-requisitos.md` ni `docs/kit-sha256sums.txt`.)*

## 4. Decisiones técnicas clave

- **Separación repositorio/reglas (`RepositorioDatos`):** `RepositorioExcel` carga únicamente las hojas `usuarios`, `servicios` y `casos` mediante `openpyxl(..., read_only=True, data_only=True)` y nunca abre `registro_tecnico`, garantizando aislamiento estructural ante `L-009` (`REQ-17`).
- **Validación de entrada estricta (`EvaluacionRequest`):** uso de `StrictStr`, `ConfigDict(extra="forbid")` y recorte de espacios para responder `HTTP 422` ante tipos incorrectos, campos extra o cadenas vacías/blancas.
- **Contrato de salida estricto (`EvaluacionResponse`):** `ConfigDict(extra="forbid")` con exactamente `{puede_reprocesar, motivos, accion_recomendada, referencias_normativas}`, sin campos extra ni alertas S2 automáticas (`REQ-01`, `REQ-12`).
- **Autorización prioritaria simulada (`REQ-03`):** `evaluar_solicitud` consulta `obtener_usuario(usuario_id)` y valida el rol en `{soporte_n1, soporte_n2, ingenieria}` antes de invocar `obtener_caso(caso_id)`, emitiendo `HTTP 403` sin revelar existencia ni diagnóstico del caso.
- **Evaluación no cortocircuitada (`REQ-18`, `EX-04`):** el motor inspecciona todas las condiciones normativas vigentes (`MAN-INC` v2 §4 y `CAT-ERR` v2 §1, incluyendo límite específico `1` de `E-512` sobre `casos.reprocesos_realizados` y validación de `SRV-MOD` en `E-207`) y reporta todos los motivos bloqueantes concurrentes con una prioridad determinista para `accion_recomendada`.

## 5. Correcciones internas realizadas durante la ejecución

Se detectaron y corrigieron **2 defectos reales** tras la primera ejecución de pruebas y *smoke test*:

1. **Error de importación de paquete `tests` en recolección de `pytest` (3 errores de colección, código de salida `2`):** `run_tests.sh` falló inicialmente con `ModuleNotFoundError: No module named 'tests'` porque `pyproject.toml` solo declaraba `pythonpath = ["src"]` y faltaba `tests/__init__.py`. **Corrección:** se actualizó `pyproject.toml` a `pythonpath = [".", "src"]` y se creó `tests/__init__.py`.
2. **Paquete `mira_cu2` ausente en el entorno `.venv` tras la instalación inicial (`ModuleNotFoundError: No module named 'mira_cu2'` en *smoke test*):** al haber ejecutado `uv sync --python 3.12` antes de crear el directorio `src/mira_cu2/`, el paquete editable inicial no contenía los módulos de aplicación. **Corrección:** se ejecutó `uv sync --python 3.12 --reinstall-package mira-cu2` luego de completar `src/mira_cu2/`.

## 6. Intervenciones humanas y limitaciones

- **Intervenciones humanas:** `0` durante la ejecución de `CORRIDA-LB-01` (se trabajó exclusivamente a partir de la especificación ya aprobada en `specs/01-requisitos.md`).
- **Limitaciones registradas:**
  - La verificación de roles contra `CU-2_datos.xlsx` es una validación simulada de rol para prototipo y no constituye autenticación real (`specs/01-requisitos.md` §2.2, §8).
  - Para `E-512`, el límite específico de `1` reproceso sobre `casos.reprocesos_realizados` se implementa bajo el supuesto conservador global aprobado en Control Humano 1 (`specs/01-requisitos.md` §7.2).
  - La advertencia emitida por Starlette/FastAPI en `TestClient` (`StarletteDeprecationWarning: Using httpx with starlette.testclient is deprecated`) proviene de dependencias externas instaladas y no afectó la ejecución ni el resultado (`58 passed`).
  - No existen herramientas en el entorno para medir consumo de tokens o costo de inferencia, por lo que esas métricas se registran como `No disponible`.
