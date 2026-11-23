# MIRA · Entregable 4 (`CU-2 · Soporte y operación`)

**Taller de Desarrollo de Software Conducido por Agentes de IA · Universidad de Valparaíso**

Este repositorio implementa la **Alternativa A: Desarrollo de Software Conducido por Especificación (SDD)** sin GitHub SpecKit sobre **MIRA CU-2 · Soporte y operación**, utilizando **Google Antigravity** con un flujo secuencial de cuatro perfiles de agente, controles humanos en compuerta, matriz de trazabilidad normativa y comparación objetiva contra una línea base de agente único ([`docs/linea-base/comparacion-resultados.md`](docs/linea-base/comparacion-resultados.md)).

---

## 1. Caso, contrato vigente y alcance

- **Funcionalidad única:** servicio de evaluación determinista y de solo lectura que determina si un caso en estado `error` o `detenido` es elegible para reprocesamiento (`POST /reprocesamiento/evaluar`), sin ejecutar reprocesos reales ni modificar el kit de entrada.
- **Fuentes normativas vigentes:** exclusivamente `MAN-INC` v2 y `CAT-ERR` v2 ([`kit/CU-2_soporte_operacion/corpus/`](kit/CU-2_soporte_operacion/corpus/)), con `GUI-COL` v1 (referencia auxiliar de servicios `SRV-*` sin alertas S2) y `POL-ACC` v1 (restricción de privacidad). El catálogo `CAT-ERR` v1 (`CAT-ERR_v1_derogado.md`) queda excluido en reglas y matriz.
- **Definiciones ratificadas en Control Humano 1 ([`specs/01-requisitos.md`](specs/01-requisitos.md)):**
  - **Contrato `HTTP 200 OK` estricto:** entrada `{caso_id, usuario_id}` y salida de 4 campos exactos `{puede_reprocesar, motivos, accion_recomendada, referencias_normativas}`, sin campos adicionales ni alertas S2.
  - **Validación simulada prioritaria de rol (`HTTP 403`):** evalúa `{soporte_n1, soporte_n2, ingenieria}` sobre la hoja `usuarios` antes de consultar `casos` (sin revelar si `caso_id` existe). Caso inexistente responde `HTTP 404`; carga malformada, tipos no cadena, campos extra o cadenas vacías responden `HTTP 422`.
  - **Supuesto conservador de `E-512`:** tope específico de **1 reproceso** usando `casos.reprocesos_realizados` como contador global por caso (manteniendo límite general de **3** para `E-207` y `E-305`).
  - **Inmunidad ante datos hostiles (`L-009` en `C-038`):** la hoja `registro_tecnico` de `CU-2_datos.xlsx` es excluida estructuralmente por [`src/mira_reproceso/loader.py`](src/mira_reproceso/loader.py).

---

## 2. Despliegue reproducible en menos de 15 minutos (desde `entrega-3`)

> **Nota sobre la etiqueta `entrega-3`:** si estás revisando el repositorio antes del etiquetado humano final (`git tag -l` aún vacío según [`docs/decision.md#control-de-commits-y-etiqueta`](docs/decision.md#control-de-commits-y-etiqueta)), permanece en la rama `main` tras clonar. Una vez publicada la etiqueta `entrega-3`, posiciona el árbol en ella con el paso 1.

### Paso 1 · Ubicar la etiqueta e instalar dependencias con `uv`

Requisitos del entorno: Linux/macOS/WSL2 con Python `>= 3.11` (validado en `CPython 3.12.14`), [`uv`](https://docs.astral.sh/uv/) (`0.13.8`) y `sha256sum`.

```bash
# Posicionarse en la etiqueta de entrega cuando esté creada en el repositorio:
git checkout entrega-3

# Crear entorno virtual local e instalar el paquete editable junto a dependencias de prueba:
uv venv .venv
uv pip install --python .venv/bin/python -e ".[dev]"
```

### Paso 2 · Verificar integridad del kit CU-2 y esquema de trazabilidad

```bash
sha256sum -c docs/kit-sha256sums.txt
PYTHONDONTWRITEBYTECODE=1 python3 .agents/skills/trazabilidad/scripts/verificar_trazabilidad.py --check-kit --matrix specs/03-trazabilidad.md
```

Resultado esperado: **7 de 7 archivos del kit en `OK`** y salida `[OK] Matriz de trazabilidad válida`.

### Paso 3 · Ejecutar la suite automatizada `pytest` en modo solo lectura

```bash
./.agents/skills/ejecucion-pruebas/scripts/run_tests.sh
```

Este script verifica previamente los 7 checksums SHA-256 del kit y ejecuta `pytest -p no:cacheprovider -v` sin escribir `__pycache__` ni `.pytest_cache` (`PYTHONDONTWRITEBYTECODE=1`). Resultado esperado: **`48 passed, 0 failed, 0 skipped`** (`0` errores).

### Paso 4 · Levantar la API FastAPI y probar `C-032` y `C-031` desde `/docs`

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/uvicorn mira_reproceso.api:app --host 127.0.0.1 --port 8000
```

1. Abrir **`http://127.0.0.1:8000/docs`** en el navegador.
2. Desplegar **`POST /reprocesamiento/evaluar`** → **Try it out**.
3. Ejecutar el caso **`C-032`** (elegible: `error`, `E-305`, `SRV-ROS` `operativo`, `0` reprocesos) con usuario autorizado `U-S1`:

```json
{
  "caso_id": "C-032",
  "usuario_id": "U-S1"
}
```

Respuesta verificada (`HTTP 200 OK`):

```json
{
  "puede_reprocesar": true,
  "motivos": [
    "El caso 'C-032' se encuentra en estado elegible ('error').",
    "El caso no tiene decisión final irreversible registrada.",
    "El código de error 'E-305' es reprocesable según CAT-ERR v2.",
    "El servicio dependiente 'SRV-ROS' se encuentra 'operativo'.",
    "El caso registra 0 de 3 reprocesos permitidos por MAN-INC v2."
  ],
  "accion_recomendada": "Proceder con el reprocesamiento.",
  "referencias_normativas": [
    "MAN-INC v2 §4",
    "CAT-ERR v2 §1 (E-305)",
    "GUI-COL v1 §1"
  ]
}
```

4. Ejecutar el caso **`C-031`** (no elegible: `E-207` con `SRV-MOD` en estado `degradado` según `CAT-ERR` v2, descartando `CAT-ERR` v1):

```json
{
  "caso_id": "C-031",
  "usuario_id": "U-S1"
}
```

Respuesta verificada (`HTTP 200 OK`):

```json
{
  "puede_reprocesar": false,
  "motivos": [
    "El servicio dependiente 'SRV-MOD' (requerido por E-207) se encuentra en estado 'degradado' (se requiere estado 'operativo')."
  ],
  "accion_recomendada": "No reprocesar; el caso permanece en cola y se reintenta automáticamente cuando SRV-MOD esté operativo.",
  "referencias_normativas": [
    "MAN-INC v2 §4",
    "GUI-COL v1 §1",
    "CAT-ERR v2 §1 (E-207)"
  ]
}
```

*(Alternativa desde terminal en una segunda consola mientras corre `uvicorn`):*

```bash
curl -s -X POST http://127.0.0.1:8000/reprocesamiento/evaluar -H 'Content-Type: application/json' -d '{"caso_id":"C-032","usuario_id":"U-S1"}'
curl -s -X POST http://127.0.0.1:8000/reprocesamiento/evaluar -H 'Content-Type: application/json' -d '{"caso_id":"C-031","usuario_id":"U-S1"}'
```

---

## 3. Arquitectura multiagente, `Orchestrator Neon` y ambigüedades frente a la rúbrica

### Entorno coordinador vs. los cuatro perfiles personalizados

En Google Antigravity (`agy 1.5.14`), **`Orchestrator (Neon)`** es el **entorno/selector de coordinación de la sesión principal**, desde donde el operador humano aplica las compuertas entre fases y despacha cada rol mediante `invoke_subagent`. **No es un quinto perfil del dominio**, sino el coordinador de la sesión frente a los **cuatro perfiles personalizados** definidos en [`.agents/agents/`](.agents/agents/):

| Perfil (`.agents/agents/`) | Herramientas activas (`inheritMcp: false`) | Artefactos propios y límite de rol | Traspaso en `docs/trabajo/` |
|---|---|---|---|
| [`requisitos`](.agents/agents/requisitos.md) | `read_file`, `write_file`, `edit_file` (sin shell) | Redacta [`specs/01-requisitos.md`](specs/01-requisitos.md) con `MAN-INC` v2 y `CAT-ERR` v2; se detiene en **CH1**. | [`001-requisitos-a-planificador.md`](docs/trabajo/001-requisitos-a-planificador.md) |
| [`planificador`](.agents/agents/planificador.md) | `read_file`, `write_file`, `edit_file` (sin shell) | Diseña [`specs/02-plan.md`](specs/02-plan.md) e inicia [`specs/03-trazabilidad.md`](specs/03-trazabilidad.md); se detiene en **CH2**. | [`002-planificador-a-implementador.md`](docs/trabajo/002-planificador-a-implementador.md) |
| [`implementador`](.agents/agents/implementador.md) | `read_file`, `write_file`, `edit_file`, `run_command`, `manage_task` | Implementa `src/mira_reproceso/`, `tests/`, actualiza `specs/03-trazabilidad.md` y ejecuta `run_tests.sh` (iteraciones `0/2` y `1/2`). | [`003`](docs/trabajo/003-implementador-a-revisor.md), [`005`](docs/trabajo/005-implementador-a-revisor.md) |
| [`revisor`](.agents/agents/revisor.md) | Exclusivamente `read_file` (+ mensajería base del runtime; sin escritura ni shell) | Auditor independiente de **solo lectura pura**; entrega dictámenes literales en conversación para registro humano. | [`004` (`0/2`)](docs/trabajo/004-revisor-a-implementador.md), [`006` (`1/2`)](docs/trabajo/006-revisor-final.md) |

Las **tres skills propias** en [`.agents/skills/`](.agents/skills/) son: [`especificacion`](.agents/skills/especificacion/SKILL.md), [`trazabilidad`](.agents/skills/trazabilidad/SKILL.md) y [`ejecucion-pruebas`](.agents/skills/ejecucion-pruebas/SKILL.md). La justificación completa de permisos por principio de privilegio mínimo y los patrones descartados consta en [`docs/decision.md §6`](docs/decision.md#L55-L89).

### Ambigüedades explícitas frente a la rúbrica (declaración transparente)

1. **`Orchestrator (Neon)` y modelos internos de subagentes:** la UI de Antigravity muestra `Orchestrator (Neon)` en la sesión coordinadora, pero no informa el desglose de modelos internos empleados por cada subagente ni el consumo de tokens/costo; ambos campos se registran como `No disponible` en [`docs/bitacora.md`](docs/bitacora.md) y [`docs/linea-base/comparacion-resultados.md`](docs/linea-base/comparacion-resultados.md).
2. **Alcance del análisis MAST (Criterio 16 de la rúbrica):** los hallazgos `H-01` (`Media`) y `H-02` (`Baja`) cuentan con causa verificada y *diff* auditable en código, pruebas y trazabilidad (`git diff e26eba3 e9dd4f6` sobre `src/mira_reproceso/rules.py`, `tests/test_rules.py`, `tests/test_api.py`, `specs/03-trazabilidad.md`), con reejecución aprobada en [`docs/evidencia/pytest-iter1.log`](docs/evidencia/pytest-iter1.log). Sin embargo, `.agents/` quedó congelado desde `145efff`, por lo que las eventuales influencias de la redacción de `specs/02-plan.md` o `.agents/agents/implementador.md` se consignan estrictamente como **hipótesis no demostradas causalmente** en [`docs/bitacora.md`](docs/bitacora.md#L189-L210).
3. **Coherencia histórica `.agents/skills/` vs. `revisor.md`:** [`ejecucion-pruebas/SKILL.md`](.agents/skills/ejecucion-pruebas/SKILL.md) menciona su uso durante la auditoría del `revisor`, pero `.agents/agents/revisor.md` deshabilitó `run_command`; en ambas corridas reales prevaleció el bloqueo efectivo `tools: [read_file]`. Además, en `0/2` el `revisor` emitió `APROBADO CON OBSERVACIONES` pese al par binario de `revisor.md:28` (absorbido conservadoramente por compuerta humana en `2c88947`).
4. **Duración de demostración vs. corrida multiagente completa:** los comandos de la Sección 2 permiten validar integridad, `pytest`, la API en `/docs` y las evidencias en **menos de 15 minutos**. **No se promete** ejecutar una corrida multiagente completa nueva con sus compuertas humanas en 6 minutos: en la corrida real `CORRIDA-MA-01`, las cinco ventanas sumadas de subagentes tomaron `~21 min` y el reloj total entre hitos con revisiones humanas abarcó `~4 h 09 min` (mientras la línea base de agente único sin compuertas tomó `7 min 34 s`).
5. **Etiqueta `entrega-3` y plazo:** la etiqueta Git `entrega-3` se encuentra pendiente de creación tras el commit final ([`docs/decision.md#control-de-commits-y-etiqueta`](docs/decision.md#control-de-commits-y-etiqueta)). En versiones previas de la guía se indicó plazo `2026-11-23 14:00` en sección 10 frente a `2026-11-30` en portada.

---

## 4. Guía breve de demostración en vivo (evidencias, skills y controles humanos)

Secuencia recomendada (< 5–10 minutos) dentro de la presentación de 15 minutos, sin relanzar corridas:

1. **Mostrar los 4 perfiles personalizados y el aislamiento del `revisor`:**
   - Abrir `.agents/agents/` (`requisitos.md`, `planificador.md`, `implementador.md`, `revisor.md`) señalando `inheritMcp: false` y `tools: [read_file]` en `revisor.md`.
   - Mostrar las capturas reales de invocación en [`docs/evidencia/CORRIDA-MA-01/panel-subagentes.png`](docs/evidencia/CORRIDA-MA-01/panel-subagentes.png) e [`invocacion-revisor-iter1.png`](docs/evidencia/CORRIDA-MA-01/invocacion-revisor-iter1.png).
2. **Recorrer la cadena secuencial de traspasos (`docs/trabajo/`):**
   - [`001-requisitos-a-planificador.md`](docs/trabajo/001-requisitos-a-planificador.md) (`requisitos`) → [`002-planificador-a-implementador.md`](docs/trabajo/002-planificador-a-implementador.md) (`planificador`) → [`003-implementador-a-revisor.md`](docs/trabajo/003-implementador-a-revisor.md) (`0/2`, `46 passed`) → [`004-revisor-a-implementador.md`](docs/trabajo/004-revisor-a-implementador.md) (`H-01`, `H-02`) → [`005-implementador-a-revisor.md`](docs/trabajo/005-implementador-a-revisor.md) (`1/2`, `48 passed`) → [`006-revisor-final.md`](docs/trabajo/006-revisor-final.md) (`APROBADO`).
3. **Demostrar una skill aplicada:**
   - Abrir [`.agents/skills/trazabilidad/SKILL.md`](.agents/skills/trazabilidad/SKILL.md) (o [`ejecucion-pruebas/SKILL.md`](.agents/skills/ejecucion-pruebas/SKILL.md)), mostrar la matriz en [`specs/03-trazabilidad.md`](specs/03-trazabilidad.md), ejecutar el verificador (`verificar_trazabilidad.py --check-kit --matrix specs/03-trazabilidad.md`) o `run_tests.sh`, y exhibir la constancia de uso registrada en [`005-implementador-a-revisor.md`](docs/trabajo/005-implementador-a-revisor.md#L74-L86) y [`docs/bitacora.md`](docs/bitacora.md).
4. **Mostrar los controles humanos, la revisión independiente y la comparación objetiva:**
   - Cadena Git verificable (`git log --oneline`): `0e47c1c` (**CH1**, Jorge), `7c0e152` (**CH2**, Lester González), `2c88947` (apertura ronda `1/2`, Lester González), `e998cca` (cierre de Fase 3, Lester González) y `220c553` (revisión independiente posterior, Jorge en [`docs/evidencia/revision-independiente-jorge.md`](docs/evidencia/revision-independiente-jorge.md)).
   - Contrastar el análisis de errores `H-01`/`H-02` frente a la corrida de agente único en [`docs/linea-base/comparacion-resultados.md`](docs/linea-base/comparacion-resultados.md) (`CORRIDA-LB-01`: `58 passed`, sin auditor independiente, dejó tautología en `SYN-INJ-OK` y acción genérica en `E-207`).

---

## 5. Organización del repositorio

| Ruta | Contenido verificado |
|---|---|
| [`AGENTS.md`](AGENTS.md) | Reglas globales del proyecto, inmutabilidad del kit, vigencia normativa y controles humanos. |
| [`.agents/agents/`](.agents/agents/) | Perfiles personalizados en Antigravity (`requisitos.md`, `planificador.md`, `implementador.md`, `revisor.md`). |
| [`.agents/skills/`](.agents/skills/) | Skills del proyecto (`especificacion`, `trazabilidad`, `ejecucion-pruebas`) con sus scripts reproducibles. |
| [`kit/CU-2_soporte_operacion/`](kit/CU-2_soporte_operacion/) | Corpus normativo y datos oficiales `CU-2_datos.xlsx` intactos (verificados contra `docs/kit-sha256sums.txt`). |
| [`specs/`](specs/) | `01-requisitos.md` (CH1), `02-plan.md` (CH2) y `03-trazabilidad.md` (RN-01..RN-18 y cierre). |
| [`src/mira_reproceso/`](src/mira_reproceso/) | Implementación mínima Python + FastAPI (`models.py`, `loader.py`, `rules.py`, `api.py`). |
| [`tests/`](tests/) | Suite automatizada `pytest` (`test_rules.py` y `test_api.py`, `48` casos aprobados en `1/2`). |
| [`docs/trabajo/`](docs/trabajo/README.md) | Actas de traspaso y dictámenes literales (`000` a `006`). |
| [`docs/evidencia/`](docs/evidencia/README.md) | Logs `pytest-iter0.log`, `pytest-iter1.log`, capturas `CORRIDA-MA-01/` y `revision-independiente-jorge.md`. |
| [`docs/linea-base/`](docs/linea-base/README.md) | Protocolo, corrida aislada `CORRIDA-LB-01/` y comparación objetiva `comparacion-resultados.md`. |
| [`docs/decision.md`](docs/decision.md) | Decisiones arquitectónicas, privilegio mínimo, patrones descartados y control de commits/etiqueta. |
| [`docs/bitacora.md`](docs/bitacora.md) | Registro completo de corridas, responsables humanos, análisis MAST y cierre de observaciones. |

## 6. Condiciones académicas de entrega

- **Repositorio y etiqueta:** incluye agentes, skills, código, pruebas y evidencias verificadas; commit final de cierre y etiqueta `entrega-3` pendientes de confirmación humana ([`docs/decision.md#control-de-commits-y-etiqueta`](docs/decision.md#control-de-commits-y-etiqueta)).
- **Informe PDF y presentación PPT:** deben reflejar la Alternativa A (SDD), Antigravity `1.5.14` con `Orchestrator (Neon)` (y desglose interno de modelos `No disponible`), integrantes (**Rodrigo Guerrero**, **Lester González**, **Jorge**), representante del cliente (**Jorge** en CH1 y revisión independiente, distinto de la Entrega 2) y el análisis MAST de [`docs/bitacora.md`](docs/bitacora.md).
