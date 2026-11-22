# Traspaso 001: requisitos -> planificador

- **Fecha:** 2026-11-22 01:32
- **Fase:** requisitos
- **Agente origen:** requisitos
- **Agente destino:** planificador
- **Iteración de corrección:** 0/2
- **Control humano requerido:** Control Humano 1 (especificacion)
- **Estado de aprobación humana:** PENDIENTE DE APROBACIÓN (sin aprobar)
- **Artefactos de entrada:**
  - `.agents/skills/especificacion/SKILL.md`
  - `.agents/skills/especificacion/resources/plantilla-especificacion.md`
  - `kit/CU-2_soporte_operacion/corpus/MAN-INC_manual_incidentes.md`
  - `kit/CU-2_soporte_operacion/corpus/CAT-ERR_v2_vigente.md`
  - `kit/CU-2_soporte_operacion/corpus/CAT-ERR_v1_derogado.md`
  - `kit/CU-2_soporte_operacion/corpus/GUI-COL_colas_servicios_externos.md`
  - `kit/CU-2_soporte_operacion/corpus/POL-ACC_acceso_evidencia.md`
  - `kit/CU-2_soporte_operacion/corpus/PRO-MAN_mantencion.md`
  - `kit/CU-2_soporte_operacion/datos/CU-2_datos.xlsx` (lectura vía transcripción oficial aprobada, sin modificación)
  - `docs/trabajo/README.md`
- **Artefactos producidos/actualizados:**
  - `specs/01-requisitos.md`
  - `docs/trabajo/001-requisitos-a-planificador.md`
- **Verificaciones ejecutadas:** Ninguna ejecución de shell (el agente `requisitos` opera sin comandos de shell y sin escritura en `src/`, `tests/`, `specs/02-plan.md`, `specs/03-trazabilidad.md` ni `kit/`). Revisión documental cruzada de consistencia tras incorporar los 5 ajustes de revisión inicial en `specs/01-requisitos.md` (`REQ-01..REQ-18`, `CA-01..CA-10`, `§2.3`, `§3.1`, `§3.2`, `§6.1`, `§6.2`, `§7` y `§8`).

## Evidencia de uso de skill

1. **Archivos de `.agents/skills/especificacion/` leídos antes de redactar:**
   - `.agents/skills/especificacion/SKILL.md`
   - `.agents/skills/especificacion/resources/plantilla-especificacion.md`
2. **Aplicación punto por punto del checklist de `SKILL.md`:**
   - **§1 Verificación de fuentes vigentes:** Se tomaron exclusivamente `MAN-INC` v2 y `CAT-ERR` v2 como fuentes normativas de reprocesamiento (`GUI-COL` v1 se limitó a referencia de servicios `SRV-*` y comportamiento de cola sin incorporar alertas S2). Se verificó y documentó explícitamente la exclusión de `CAT-ERR` v1 por estar derogado desde el 1 de septiembre de 2026, y no se modificó ningún archivo de `kit/CU-2_soporte_operacion/`.
   - **§2 Reglas de alcance y contrato mínimo:** Se acotó la especificación a la evaluación de elegibilidad de reprocesamiento en Python + FastAPI + `pytest`, cerrando explícitamente las exclusiones de alertas automáticas S2, reprocesamiento real, frontend, RAG, MCP, notificaciones, administración de incidentes y SpecKit. Se fijó `HTTP 200 OK` con contrato exacto `{caso_id, usuario_id}` → `{puede_reprocesar, motivos, accion_recomendada, referencias_normativas}` (sin campos extra) separado de respuestas estándar de error HTTP (`403`, `404`, `422`).
   - **§3 Registro obligatorio de ambigüedades y seguridad:** Se actualizó la Sección 7 (*Definiciones adoptadas y puntos pendientes para Control Humano 1*) diferenciando las 5 definiciones adoptadas tras la revisión inicial (incluido el supuesto conservador global por caso para `E-512` con tope de `1` reproceso y `casos.reprocesos_realizados`) de los puntos pendientes de ratificación formal por el representante del cliente. Se mantuvo la Sección 8 declarando `registro_tecnico` (`L-009` en `C-038`) como dato pasivo no confiable y la validación de rol por `usuario_id` como simulación (no autenticación real). Se mantuvo en la Sección 6.2 la cobertura mediante casos sintéticos en memoria preservando intacto `CU-2_datos.xlsx`.
   - **§4 Plantilla y compuertas humanas:** Se estructuró `specs/01-requisitos.md` siguiendo `resources/plantilla-especificacion.md` más las secciones solicitadas, dejando explícitamente su estado en `Pendiente de Control Humano 1 (revisión y aprobación del representante del cliente)` y deteniendo el flujo a la espera de confirmación formal.

## Resumen de ajustes aplicados y puntos abiertos

- **Resumen de los 5 ajustes aplicados en `specs/01-requisitos.md`:**
  1. **Ajuste 1 (`E-512`):** Límite provisional específico de `1` reproceso (`reprocesos_realizados < 1`) usando `casos.reprocesos_realizados` como **contador global por caso** en escenarios mixtos (documentado como **supuesto conservador del prototipo** pendiente de ratificación formal), manteniendo el límite general de `3` para `E-207` y `E-305`.
  2. **Ajuste 2 (Códigos HTTP diferenciados):** `HTTP 200 OK` devuelve el contrato exacto de 4 campos (evaluaciones válidas); `HTTP 403 Forbidden` (rol no autorizado o `usuario_id` inexistente), `HTTP 404 Not Found` (`caso_id` inexistente con usuario autorizado) y `HTTP 422 Unprocessable Entity` (solicitudes malformadas) devuelven respuestas estándar de error HTTP distintas del contrato de 4 campos (`§2.3`, `§3.1`, `§3.2`, `REQ-01`, `REQ-03`, `REQ-04`, `CA-09`, `§6.2`).
  3. **Ajuste 3 (Orden de evaluación y reserva de diagnóstico):** Se evalúa primero el rol del usuario antes de consultar o diagnosticar `caso_id`, sin exponer diagnósticos internos ni si el caso existe cuando hay rechazo `403`, manteniendo el reporte completo de todos los motivos bloqueantes concurrentes cuando usuario está autorizado y caso existe.
  4. **Ajuste 4 (Cierre de exclusiones):** Cerrada definitivamente la exclusión de alertas automáticas S2 (ni para `C-039` ni campos adicionales en `C-037`) y de cualquier funcionalidad fuera del alcance mínimo.
  5. **Ajuste 5 (Validación simulada de roles):** Aclarado en `§2`, `§3.2`, `REQ-03`, `§7.1` y `§8` que la validación por `usuario_id` contra `CU-2_datos.xlsx` es simulada para el prototipo y no constituye autenticación real.
- **Puntos pendientes de confirmación formal en Control Humano 1:**
  1. Aprobación formal de `specs/01-requisitos.md`.
  2. Ratificación formal del supuesto conservador del prototipo para `E-512` en escenarios mixtos (`casos.reprocesos_realizados` como contador global por caso con tope de `1` reproceso).
  3. Conformidad con `HTTP 403 Forbidden` para `usuario_id` inexistente y con el formato estándar de error HTTP (`{"detail": "..."}`) para `403`, `404` y `422`.

## Registro de Control Humano 1 (Pendiente de aprobación)

- **Estado:** `PENDIENTE DE APROBACIÓN`
- **Representante del cliente / Revisor humano:** `[Por completar]`
- **Fecha de decisión:** `[Por completar]`
- **Decisión:** `[ ] Aprobado` / `[ ] Aprobado con observaciones` / `[ ] Requiere ajustes`
- **Lista de verificación:**
  - `[ ]` Alcance mínimo y exclusiones cerradas sin alertas S2 ni funcionalidades adicionales.
  - `[ ]` Contrato `HTTP 200` exacto de 4 campos separado de errores HTTP estándar `403` / `404` / `422`.
  - `[ ]` Evaluación prioritaria de rol simulado (no autenticación real) sin exponer diagnósticos internos ni existencia de casos ante `403`.
  - `[ ]` Vigencia normativa exclusiva de `MAN-INC` v2 y `CAT-ERR` v2, excluyendo `CAT-ERR` v1 derogado.
  - `[ ]` Supuesto conservador provisional de `E-512` (límite de `1` reproceso y uso de `casos.reprocesos_realizados` como contador global por caso).
  - `[ ]` Seguridad de datos frente a inyección en `registro_tecnico` (`L-009` en `C-038`) e integridad de solo lectura de `kit/CU-2_soporte_operacion/`.
- **Observaciones y confirmación del representante del cliente:** `[Por completar]`

> **Nota obligatoria de compuerta:** **No se invocará al agente `planificador`** ni se crearán `specs/02-plan.md` ni `specs/03-trazabilidad.md` hasta recibir confirmación explícita del representante del cliente registrada en este control humano.
