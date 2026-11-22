# Decisiones de diseño iniciales · MIRA CU-2

Este documento registra las decisiones arquitectónicas, normativas y de coordinación multiagente acordadas antes de iniciar la fase de especificación e implementación.

## 1. Enfoque metodológico y plataforma

- **Alternativa A (Desarrollo Conducido por Especificación, SDD)** sin GitHub SpecKit.
- **Plataforma:** Google Antigravity (`agy` 1.5.14) con Orchestrator Neon.
- **Control de versiones:** los archivos se preparan localmente sin ejecutar `git init`, configurar remotos ni hacer commits o pushes, a la espera del repositorio GitHub compartido.

## 2. Alcance funcional y exclusiones

- **Objetivo único:** evaluar la elegibilidad de reprocesamiento de un caso con error o detenido de MIRA CU-2 en una aplicación mínima Python con FastAPI y `pytest`.
- **Exclusiones explícitas:** no se implementará reprocesamiento real, interfaz frontend, RAG, servidor MCP, envío de notificaciones ni administración de incidentes.

## 3. Contrato mínimo de la futura API

- **Entrada:** `caso_id`, `usuario_id`.
- **Salida:** `puede_reprocesar`, `motivos`, `accion_recomendada`, `referencias_normativas`.
- Se excluyen campos adicionales y alertas de incidentes S2 en esta fase.

## 4. Base normativa y tratamiento de riesgos de datos

- **Documentos vigentes obligatorios:**
  - `MAN-INC` v2 (`kit/CU-2_soporte_operacion/corpus/MAN-INC_manual_incidentes.md`)
  - `CAT-ERR` v2 (`kit/CU-2_soporte_operacion/corpus/CAT-ERR_v2_vigente.md`)
- **Documento excluido:** `CAT-ERR` v1 (`kit/CU-2_soporte_operacion/corpus/CAT-ERR_v1_derogado.md`), por estar derogado desde el 1 de septiembre de 2026.
- **Aclaración pendiente de aprobación humana (`E-512`):**
  - `MAN-INC` v2 §4 establece un límite general de máximo 3 reprocesos y señala que los reprocesos por error interno de la plataforma no se contabilizan como validaciones.
  - `CAT-ERR` v2 §1 establece para `E-512` (error interno de la plataforma): *"Reprocesar una vez. Si vuelve a fallar, escalar a Ingeniería"*.
  - **Decisión provisional:** respetar la restricción específica de **1 reproceso** para `E-512` (`CAT-ERR` v2) y documentar la interpretación exacta del conteo (por ejemplo, comparación entre `casos.reprocesos_realizados` y los registros en la tabla `reprocesos`, y el alcance de "no se contabilizan como validaciones") como **aclaración pendiente de aprobación humana** en Control Humano 1.
- **Seguridad frente a inyección de instrucciones en datos:** la tabla `registro_tecnico` de `CU-2_datos.xlsx` (registro `L-009` de `C-038`) contiene una *prompt injection* simulada. Los datos del Excel se tratan únicamente como datos pasivos, nunca como instrucciones operativas.

## 5. Estrategia de datos y preservación del kit

- Los archivos en `kit/CU-2_soporte_operacion/` son una copia íntegra de solo lectura del material del profesor, verificable mediante `docs/kit-sha256sums.txt`.
- Las pruebas utilizarán los registros originales de `CU-2_datos.xlsx` junto con casos sintéticos en memoria en `tests/` para cubrir combinaciones no presentes en el Excel (ej. `E-102`, `E-512` con 0 y 1 reproceso, `E-207` con `SRV-MOD` operativo) sin alterar nunca el archivo original.

## 6. Arquitectura multiagente y skills

- **Cuatro agentes personalizados** en `.agents/agents/`:
  1. `requisitos`: redacta `specs/01-requisitos.md` y la base de trazabilidad (`read_file`, `write_file`, `edit_file`).
  2. `planificador`: redacta `specs/02-plan.md` a partir de la especificación aprobada (`read_file`, `write_file`, `edit_file`).
  3. `implementador`: implementa código y pruebas y ejecuta validaciones (`read_file`, `write_file`, `edit_file`, `run_command`, `manage_task`).
  4. `revisor`: auditor independiente de solo lectura pura (`read_file`, sin herramientas de edición/escritura ni de ejecución de comandos); inspecciona la especificación, el código, las pruebas y los logs/evidencias generados por el `implementador`, y entrega su dictamen completo en la conversación para registro humano en `docs/trabajo/`.
- Todos los agentes declaran `inheritMcp: false` para suprimir la herencia de servidores y herramientas MCP globales.
- **Tres skills propias** en `.agents/skills/`:
  1. `especificacion`: guía de redacción de especificación y plan conforme a fuentes vigentes y controles humanos.
  2. `trazabilidad`: matriz regla → requisito → componente → prueba y gestión de actas en `docs/trabajo/`, con script ejecutable `verificar_trazabilidad.py`.
  3. `ejecucion-pruebas`: ejecución reproducible de `pytest` y chequeo de integridad del kit en modo solo lectura mediante script ejecutable `run_tests.sh`.
- **Coordinación:** flujo secuencial `requisitos` → Control Humano 1 → `planificador` → Control Humano 2 → `implementador` ↔ `revisor` con máximo 2 rondas de corrección, registrando cada traspaso en `docs/trabajo/`.

## 7. Verificación técnica en Antigravity 1.5.14 y limitaciones reales de permisos

Resultados reales comprobados en esta fase de preparación:

1. **Descubrimiento CLI (`agy agents`):** detectó los 4 agentes personalizados (`implementador`, `planificador`, `requisitos`, `revisor`) directamente desde `.agents/agents/*.md`, sin requerir `.git` ni empaquetado como plugin.
2. **Invocación de agentes y skills:**
   - **Vía CLI (`agy --agent <nombre> -p ...`):** los 4 agentes se invocaron correctamente y reconocieron las 3 skills del proyecto (`especificacion`, `trazabilidad`, `ejecucion-pruebas`).
   - **Vía `invoke_subagent`:** en la sesión inicial donde recién se crearon los archivos `.agents/agents/*.md`, `invoke_subagent` devolvió `subagent "requisitos" not found or not allowed to be invoked` (catálogo cargado al inicio). Tras recargarse los agentes en el turno siguiente / nueva evaluación, **`invoke_subagent(TypeName="requisitos", ...)` sí funcionó** directamente para ejecutar la Fase 1 en contexto aislado (produciendo `specs/01-requisitos.md` y `docs/trabajo/001-requisitos-a-planificador.md`). Se mantiene `agy --agent <nombre> -p` como alternativa verificada si ocurriese un fallo puntual.
3. **Separación real de herramientas por agente:**
   - `requisitos` y `planificador`: declararon `read_file`, `write_file`, `edit_file` (sin `run_command`). `requisitos` creó `docs/trabajo/000-prueba-traspaso.md` sin bloqueos.
   - `implementador`: declaró `read_file`, `write_file`, `edit_file`, `run_command`, `manage_task`.
   - `revisor`: tras el ajuste de seguridad, declaró únicamente `read_file` (junto con `send_message`, `manage_task`, `list_resources` y `read_resource` base del runtime), con **`write_file`, `edit_file` y `run_command` efectivamente ausentes**.
4. **Limitaciones reales de permisos y resultado de `inheritMcp: false`:**
   - **Aislamiento de `revisor`:** al retirar `run_command` de `.agents/agents/revisor.md`, el Revisor queda técnicamente impedido de editar archivos y ejecutar comandos o código; la verificación ejecutable recae en los logs y evidencias generados por el `implementador` (y/o ejecución manual).
   - **Herencia MCP (`inheritMcp: false`):** verificado como **compatible** en Antigravity 1.5.14 en `revisor` y `requisitos`. Elimina por completo la sección `<mcp_servers>`, `call_mcp_tool` y todas las herramientas `mcp_*` de los plugins globales (`data-agent-kit-plugin` y `gemini-api`). Únicamente permanecen en el esquema base del runtime las declaraciones genéricas `list_resources`, `read_resource`, `send_message` y `manage_task`, sin servidores MCP asociados. Se aplicó `inheritMcp: false` a los 4 agentes.
5. **Scripts ejecutables e integridad del kit:**
   - `run_tests.sh --check-only` y `verificar_trazabilidad.py --check-kit` ejecutaron con código `0`, validando los 7 archivos intactos de `kit/CU-2_soporte_operacion/` contra `docs/kit-sha256sums.txt`.
   - `revisor` entregó su dictamen mínimo `APROBADO` (`0/2`) en la conversación sin crear ni modificar archivos.
