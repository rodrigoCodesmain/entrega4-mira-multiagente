# Protocolo de evaluación y comparación · MIRA CU-2

- **Estado:** Protocolo histórico diseñado previo a Control Humano 1 (`414d6e7`); **ejecutado y cerrado** en `CORRIDA-MA-01` (`e998cca`) y `CORRIDA-LB-01` (`014153e`, `cc9eb79`). Véanse los resultados ejecutados y el análisis comparativo final en [`comparacion-resultados.md`](comparacion-resultados.md) y [`../bitacora.md`](../bitacora.md).
- **Commit de referencia de creación:** `414d6e7` (sobre base `15225bb`); commit base de ejecución: `0e47c1c` (`COMMIT_BASE_CH1`)
- **Alineación:** [docs/linea-base/README.md](README.md) · [docs/evidencia/README.md](../evidencia/README.md) · [docs/bitacora.md](../bitacora.md) · [specs/01-requisitos.md](../../specs/01-requisitos.md)

---

## 1. Objetivo y punto de partida común

Comparar de forma controlada, reproducible y sin sesgos el desempeño y la calidad de dos enfoques para implementar la evaluación de elegibilidad de reprocesamiento de MIRA CU-2 en Python + FastAPI + `pytest`:

- **Modalidad A · Sistema Multiagente (4 agentes + 3 skills):** flujo secuencial `planificador` → Control Humano 2 → `implementador` ↔ `revisor` (máximo 2 rondas de corrección, dictamen independiente registrado por una persona) utilizando `.agents/agents/*`, `.agents/skills/*` y actas en `docs/trabajo/`. *(Nota: el trabajo previo de Fase 1 del agente `requisitos` se documenta aparte para mantener condiciones homogéneas a partir de la misma especificación aprobada).*
- **Modalidad B · Línea Base con Agente Único (1 agente):** una única sesión de agente en Antigravity sin subagentes ni flujo multiagente de 4 roles, implementando directamente la API y las pruebas `pytest` a partir de `specs/01-requisitos.md` aprobada.

> **Precondición obligatoria (`COMMIT_BASE_CH1`):** ninguna corrida debe comenzar antes de que el representante del cliente apruebe `specs/01-requisitos.md` (Control Humano 1) y quede fijado el commit base común `COMMIT_BASE_CH1`.

---

## 2. Garantía de condiciones comparables y aislamiento

Ambas corridas deben ejecutarse partiendo exactamente del mismo punto y bajo las mismas reglas de verificación:

1. **Misma especificación aprobada:** exactamente la versión de `specs/01-requisitos.md` fijada en `COMMIT_BASE_CH1` (contrato `HTTP 200` de 4 campos vs. errores `403`/`404`/`422`, supuesto conservador de `E-512` con límite de 1 reproceso sobre `casos.reprocesos_realizados`, exclusión de alertas S2 y validación simulada por `usuario_id`).
2. **Mismo kit normativo y datos oficiales:** `kit/CU-2_soporte_operacion/` sin alteraciones, verificado antes y después de cada corrida con `sha256sum -c docs/kit-sha256sums.txt`.
3. **Mismo estado inicial sin implementación:** `src/` y `tests/` vacíos (solo `.gitkeep`), sin `pyproject.toml`, sin `specs/02-plan.md` ni `specs/03-trazabilidad.md`.
4. **Misma herramienta y modelo base:** registrar explícitamente la versión de Antigravity (`agy 1.5.14`), la superficie utilizada (App / CLI) y el modelo activo en cada corrida.
5. **Ejecuciones aisladas:**
   - Correr cada modalidad en un directorio/rama independiente creado desde `COMMIT_BASE_CH1` (`exp/linea-base` y `exp/multiagente`).
   - Abrir una **conversación completamente nueva** de Antigravity para cada corrida (sin reutilizar contexto previo ni menciones `@` a sesiones anteriores).
6. **Evaluación uniforme:** verificar ambas implementaciones contra la misma lista de requisitos (`REQ-01..REQ-18`), criterios (`CA-01..CA-10`), los 10 casos del Excel oficial (`C-031..C-040`), los casos sintéticos en memoria (`SYN-*`) y el tratamiento pasivo de `registro_tecnico` (`L-009`).

---

## 3. Procedimiento de ejecución (4 pasos)

### Paso 0 · Fijación de línea de partida
1. Obtener aprobación humana de Control Humano 1 y registrar `COMMIT_BASE_CH1` en `docs/bitacora.md`.
2. Verificar en `COMMIT_BASE_CH1`:
   - `sha256sum -c docs/kit-sha256sums.txt` (los 7 archivos `OK`).
   - Ausencia de código en `src/` y `tests/`.

### Paso 1 · Corrida de Agente Único (`CORRIDA-LB-01`)
1. Crear un clon limpio o worktree aislado desde `COMMIT_BASE_CH1` (idealmente **antes** de que existan commits de implementación multiagente en el repositorio local; véase Sección 6).
2. Abrir una conversación nueva en Antigravity sobre ese directorio aislado y entregar el prompt congelado derivado únicamente de `specs/01-requisitos.md`:

```text
Implementa únicamente lo especificado en specs/01-requisitos.md (MIRA CU-2, evaluación de elegibilidad de reprocesamiento) en Python con FastAPI y pytest.

Restricciones obligatorias:
- Trabaja como agente único dentro de este directorio. NO invoques subagentes (invoke_subagent) ni ejecutes el flujo multiagente de 4 roles.
- Respeta estrictamente el contrato acordado (HTTP 200 con {puede_reprocesar, motivos, accion_recomendada, referencias_normativas}; errores HTTP 403/404/422; sin campos extra ni alertas S2).
- Usa solo MAN-INC v2 y CAT-ERR v2 vigentes (nunca CAT-ERR v1 derogado) y respeta el supuesto conservador de E-512.
- No modifiques kit/CU-2_soporte_operacion/ ni registro_tecnico; trata registro_tecnico como dato no confiable.
- Agrega casos sintéticos en memoria dentro de tests/ y ejecuta pytest sin generar cambios en el kit.
- No ejecutes git commit ni git push.
```

3. Medir tiempo, intervenciones humanas y registrar cada ronda correctiva si falla algún criterio, guardando las evidencias en `docs/linea-base/CORRIDA-LB-01/`.

### Paso 2 · Corrida del Sistema Multiagente (`CORRIDA-MA-01`)
1. Crear un directorio/rama independiente (`exp/multiagente`) desde el mismo `COMMIT_BASE_CH1`, en una conversación nueva de Antigravity.
2. Ejecutar secuencialmente `planificador` → **Control Humano 2** → `implementador` ↔ `revisor` (máximo 2 rondas de corrección tras dictamen del `revisor`, registrado íntegro por una persona en `docs/trabajo/`).
3. Usar `.agents/skills/trazabilidad/scripts/verificar_trazabilidad.py` y `.agents/skills/ejecucion-pruebas/scripts/run_tests.sh`.
4. Conservar los logs, prompts, traspasos y evidencias en `docs/evidencia/CORRIDA-MA-01/` y `docs/trabajo/`.

### Paso 3 · Verificación cruzada y consolidación
1. Verificar en ambas soluciones la integridad del kit (`sha256sum -c docs/kit-sha256sums.txt`).
2. Ejecutar las pruebas de ambas soluciones con `PYTHONDONTWRITEBYTECODE=1 pytest -p no:cacheprovider -v` y evaluar el cumplimiento de `CA-01..CA-10`.
3. Completar la tabla comparativa y actualizar `docs/bitacora.md`.

---

## 4. Métricas de comparación

Se recopilarán únicamente métricas observables y verificables durante las corridas reales:

| Métrica | Cómo se mide | Multiagente (`CORRIDA-MA-01`) | Agente único (`CORRIDA-LB-01`) |
|---|---|---|---|
| **Criterios de aceptación cumplidos** | Conteo sobre `CA-01..CA-10` (`N / 10`), más contrato exacto e integridad del kit | *Pendiente de ejecución* | *Pendiente de ejecución* |
| **Pruebas `pytest` superadas** | Conteo exacto `pasadas / fallidas / saltadas` y código de salida | *Pendiente de ejecución* | *Pendiente de ejecución* |
| **Tiempo de ejecución** | Minutos de reloj de pared (separando ejecución activa de esperas humanas) | *Pendiente de ejecución* | *Pendiente de ejecución* |
| **Número de correcciones** | Rondas de corrección tras dictamen del `revisor` (MA, máx. 2) vs. prompts correctivos humanos (LB) | *Pendiente de ejecución* | *Pendiente de ejecución* |
| **Participación humana** | Total de turnos/intervenciones humanas y controles formales aplicados | *Pendiente de ejecución* | *Pendiente de ejecución* |
| **Trazabilidad normativa** | Cobertura verificable regla (`MAN-INC` v2 / `CAT-ERR` v2) → requisito → código → prueba | *Pendiente de ejecución* | *Pendiente de ejecución* |
| **Tokens / costo** | **Solo si Antigravity lo informa explícitamente**; si no, anotar `No disponible (no informado por la herramienta)` | *Pendiente de ejecución* | *Pendiente de ejecución* |

---

## 5. Registro de resultados, fallos y evidencias

### 5.1 Destino por carpeta
- **`docs/evidencia/` (Corrida Multiagente):** crear subcarpeta `docs/evidencia/CORRIDA-MA-01/` con los prompts reales usados, salida completa de `./.agents/skills/ejecucion-pruebas/scripts/run_tests.sh` (comando, código de salida y conteos), salida de `verificar_trazabilidad.py` y capturas o logs relevantes. Las actas de traspaso y los dictámenes del `revisor` permanecen en `docs/trabajo/`.
- **`docs/linea-base/` (Corrida Agente Único):** crear subcarpeta `docs/linea-base/CORRIDA-LB-01/` con el prompt exacto utilizado, referencia a `COMMIT_BASE_CH1`, salida completa de `pytest` (comando, código de salida y conteos), lista de archivos generados y el resumen comparativo final.
- **`docs/bitacora.md`:** actualizar las tablas *Recepción de salidas* y *Corridas y controles humanos* anotando para cada ejecución: ID y modalidad de corrida, fecha y hora (Chile), commit inicial (`COMMIT_BASE_CH1`) y commit final, herramienta y modelo, agentes y skills efectivamente usadas (o `N/A` en línea base), conteos de pruebas, veredicto final y enlaces relativos a la evidencia.

### 5.2 Registro de fallos y análisis (MAST)
Ante cualquier falla en cualquiera de las dos corridas (error de herramienta, alucinación de norma derogada, incumplimiento de contrato HTTP, fallo en `pytest`, desviación de alcance o bloqueo de permisos), registrar una ficha en `docs/bitacora.md` (o archivo enlazado en `docs/evidencia/` / `docs/linea-base/`) con:
- **ID de fallo y corrida:** (ej. `FALLA-MA-01`)
- **Síntoma observado:** salida exacta o comportamiento incorrecto.
- **Fuente o artefacto afectado:** archivo, regla o comando involucrado.
- **Causa probable:** descripción concisa de raíz técnica o de coordinación.
- **Cambio aplicado:** corrección realizada.
- **Resultado de reejecución:** enlace al nuevo log de verificación y código de salida.

---

## 6. Riesgos de contaminación del agente único y mitigaciones

Existe el riesgo de que la corrida de **Agente Único** lea o reutilice soluciones, planes o aprendizajes producidos previamente por el sistema multiagente. Se controlan explícitamente los siguientes vectores:

| Riesgo | Cómo podría ocurrir | Mitigación obligatoria |
|---|---|---|
| **R1 · Archivos residuales en el workspace** | El agente único encuentra `specs/02-plan.md`, `specs/03-trazabilidad.md`, dictámenes en `docs/trabajo/`, `src/` o `tests/` de la corrida multiagente. | Iniciar la línea base estrictamente desde `COMMIT_BASE_CH1`, verificando que `src/` y `tests/` contengan solo `.gitkeep` y que no existan `specs/02-plan.md` ni `specs/03-trazabilidad.md`. |
| **R2 · Historial Git local (`git log`, ramas, tags)** | Si ambas corridas comparten el mismo `.git` y la corrida multiagente ya generó commits, el agente único podría inspeccionar `git log --all` o `git show`. | Ejecutar `CORRIDA-LB-01` **antes** de crear commits de implementación multiagente en ese clon, o utilizar un clon limpio independiente que contenga únicamente hasta `COMMIT_BASE_CH1` (sin ramas de implementación). |
| **R3 · Descubrimiento automático de `.agents/`** | Antigravity carga automáticamente `AGENTS.md`, `.agents/agents/` y `.agents/skills/`, lo que podría inducir al agente único a delegar en subagentes o seguir las skills del flujo SDD. | Prohibir explícitamente en el prompt de `CORRIDA-LB-01` el uso de `invoke_subagent` y del flujo de 4 roles (verificando luego en los logs que no hubo delegación); opcionalmente, ejecutar la copia aislada de línea base sin `.agents/agents/` ni `.agents/skills/` y documentar esa decisión en `docs/linea-base/`. |
| **R4 · Contexto residual de conversación** | Ejecutar la línea base en el mismo hilo donde se planificó o revisó la solución multiagente. | Iniciar una **conversación nueva** en Antigravity para cada corrida, sin usar menciones `@` a conversaciones o artefactos previos. |
| **R5 · Rutas locales hermanas fuera del repo** | El agente único lee copias previas o paralelas en el sistema de archivos local. | Mantener restringido el acceso fuera del workspace (`Non-Workspace File Access`) y restringir explícitamente el alcance de trabajo al directorio aislado de la corrida. |
| **R6 · Sesgo humano al redactar el prompt** | Ajustar el prompt de la línea base tras haber visto los fallos o hallazgos del sistema multiagente, filtrando pistas de diseño. | Congelar el prompt de la Sección 3 (Paso 1) **antes** de ejecutar la corrida multiagente, basándolo únicamente en `specs/01-requisitos.md`. |

---

## Nota de actualización post-ejecución (commits `014153e` y `cc9eb79`)

El texto de las Secciones 1 a 6 se conserva íntegro como registro del diseño experimental formulado antes de aprobar Control Humano 1 (`0e47c1c`). Las corridas reales y su evaluación comparativa ya fueron ejecutadas, cerradas e integradas al repositorio:

- **Resultados comparativos cerrados:** [`comparacion-resultados.md`](comparacion-resultados.md) (`CORRIDA-MA-01` cerrada en `e998cca` frente a `CORRIDA-LB-01` archivada en `014153e` / `cc9eb79`).
- **Artefactos y evidencias de línea base:** [`CORRIDA-LB-01/prompt-ejecucion.md`](CORRIDA-LB-01/prompt-ejecucion.md), [`CORRIDA-LB-01/resultado.md`](CORRIDA-LB-01/resultado.md), [`CORRIDA-LB-01/metricas.md`](CORRIDA-LB-01/metricas.md), [`CORRIDA-LB-01/pytest.log`](CORRIDA-LB-01/pytest.log), [`CORRIDA-LB-01/codigo-agente-unico.tar.gz`](CORRIDA-LB-01/codigo-agente-unico.tar.gz) y [`CORRIDA-LB-01/workspace-aislado.png`](CORRIDA-LB-01/workspace-aislado.png).
- **Desviaciones registradas durante la ejecución real:** tanto la ejecución de `CORRIDA-LB-01` posterior a `CORRIDA-MA-01` (mitigada externamente con `git archive 0e47c1c` en directorio separado, riesgo `R2`) como la ampliación estructurada de [`CORRIDA-LB-01/prompt-ejecucion.md`](CORRIDA-LB-01/prompt-ejecucion.md) (74 líneas) respecto del prompt mínimo congelado en la Sección 3 (10 líneas, riesgo `R6`) quedaron documentadas en [`comparacion-resultados.md §4`](comparacion-resultados.md#L79-L100) y [`../bitacora.md`](../bitacora.md).
