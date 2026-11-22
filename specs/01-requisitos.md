# Especificación de Requisitos · MIRA CU-2 (Elegibilidad de reprocesamiento)

- **Estado:** Aprobado — Control Humano 1 (aprobación del representante del cliente, Jorge, registrada el 2026-11-22)
- **Enfoque metodológico:** Alternativa A (Desarrollo Conducido por Especificación, SDD sin GitHub SpecKit)
- **Fuentes normativas vigentes:**
  - `MAN-INC` v2 (`kit/CU-2_soporte_operacion/corpus/MAN-INC_manual_incidentes.md`, vigente desde el 1 de agosto de 2026)
  - `CAT-ERR` v2 (`kit/CU-2_soporte_operacion/corpus/CAT-ERR_v2_vigente.md`, vigente desde el 1 de septiembre de 2026)
- **Fuente operativa auxiliar (solo referencia de servicios `SRV-*` y cola):**
  - `GUI-COL` v1 (`kit/CU-2_soporte_operacion/corpus/GUI-COL_colas_servicios_externos.md`, vigente desde el 1 de agosto de 2026; **no** autoriza la emisión de alertas S2 ni campos extra en la salida)
- **Fuentes excluidas:**
  - `CAT-ERR` v1 (`kit/CU-2_soporte_operacion/corpus/CAT-ERR_v1_derogado.md`) — **Derogado** desde el 1 de septiembre de 2026 y reemplazado por `CAT-ERR` v2; prohibida su aplicación en reglas, decisiones o mensajes.
- **Constancia de aplicación de skill:** Elaborado aplicando íntegramente `.agents/skills/especificacion/SKILL.md` y estructurado sobre `.agents/skills/especificacion/resources/plantilla-especificacion.md`.

---

## 1. Alcance, exclusiones e historia de usuario

### 1.1 Historia de usuario

> **Como** integrante autorizado del equipo de soporte u operación de DPRIME (`soporte_n1`, `soporte_n2` o `ingenieria`),  
> **quiero** consultar mediante un servicio mínimo si un caso específico de MIRA CU-2 es elegible para reprocesamiento dado mi identificador de usuario,  
> **para** obtener una decisión determinista (`puede_reprocesar`), sus motivos, la acción recomendada y las referencias normativas vigentes sin ejecutar acciones reales, sin infringir el catálogo vigente y sin quedar expuesto a instrucciones inyectadas en los registros técnicos.

### 1.2 Alcance incluido

- Evaluación determinista y de solo lectura de la elegibilidad de reprocesamiento de un caso de MIRA CU-2 a partir de `caso_id` y `usuario_id`.
- Validación simulada de autorización de rol del usuario solicitante conforme a `MAN-INC` v2 §4.
- Evaluación de reglas generales de reprocesamiento (`MAN-INC` v2 §4), reglas específicas por código de error (`CAT-ERR` v2 §1) y estado operativo de servicios dependientes (`CU-2_datos.xlsx`, referenciados en `GUI-COL` v1 §1).
- Exposición de un endpoint mínimo en Python + FastAPI y cobertura de pruebas automatizadas con `pytest` (sobre los registros vigentes del Excel oficial intacto y casos sintéticos en memoria en `tests/`).

### 1.3 Exclusiones obligatorias (alcance cerrado)

Queda **definitiva y explícitamente fuera de alcance** en esta entrega:
- Emitir alertas automáticas de incidentes S2 (o S3), agregar campos de alerta o severidad al contrato de respuesta, o generar incidentes automáticos para casos demorados en cola (como `C-039`) o errores `E-208` (`C-037`).
- Ejecutar reprocesamientos reales, modificar colas o alterar el estado de ningún caso o servicio.
- Implementar interfaz gráfica (*frontend*), motores RAG, servidores MCP, envío de notificaciones/correos o administración de incidentes.
- Implementar autenticación real de usuarios (contraseñas, tokens, sesiones o verificación criptográfica de identidad).
- Acceder al contenido de la evidencia documental o biométrica de las organizaciones (`POL-ACC` v1).
- Utilizar GitHub SpecKit o modificar cualquier archivo de `kit/CU-2_soporte_operacion/`.

---

## 2. Actores, precondiciones y contrato mínimo de la API

### 2.1 Actores

| Actor | Identificadores / Ejemplos (`CU-2_datos.xlsx`) | Rol / Función | Habilitado para reprocesar (`MAN-INC` v2 §4) |
|---|---|---|---|
| Soporte Nivel 1 | `U-S1` (Gabriela Núñez, `soporte_n1`, DPRIME) | Evalúa y solicita elegibilidad de reprocesamiento | Sí (`HTTP 200` si el caso existe) |
| Soporte Nivel 2 | `U-S2` (Martín Cáceres, `soporte_n2`, DPRIME) | Evalúa y solicita elegibilidad de reprocesamiento | Sí (`HTTP 200` si el caso existe) |
| Ingeniería | `U-S3` (Valeria Ortiz, `ingenieria`, DPRIME) | Evalúa y solicita elegibilidad de reprocesamiento | Sí (`HTTP 200` si el caso existe) |
| Usuario comercial (no autorizado) | `U-S4` (Constanza Ríos, `comercial`, DPRIME) | Consulta no habilitada para reproceso | No (rechazo `HTTP 403`) |
| Usuario inexistente / sin rol habilitado | Ej. `U-999` | Actor no reconocido o sin rol autorizado | No (rechazo `HTTP 403`) |
| Evaluador MIRA CU-2 | Sistema API FastAPI | Evalúa reglas normativas vigentes en modo solo lectura | N/A |

### 2.2 Precondiciones

1. Los datos operativos (`organizaciones`, `usuarios`, `servicios`, `casos`, `reprocesos` y `registro_tecnico`) provienen en modo **estrictamente de solo lectura** de `kit/CU-2_soporte_operacion/datos/CU-2_datos.xlsx` (o de fixtures sintéticos en memoria durante pruebas en `tests/`).
2. El catálogo normativo aplicado corresponde exclusivamente a `MAN-INC` v2 y `CAT-ERR` v2.
3. La validación de roles mediante `usuario_id` contra `CU-2_datos.xlsx` es **simulada** para fines del prototipo y **no constituye autenticación real** (no verifica identidad real, contraseñas, tokens ni sesiones).
4. Los registros de `registro_tecnico` se cargan o ignoran únicamente como texto pasivo no confiable; nunca participan en la lógica de decisión ni ejecutan acciones.
5. La petición de entrada incluye los campos `caso_id` y `usuario_id`.

### 2.3 Contrato mínimo de la API y códigos de respuesta HTTP

- **Entrada (JSON):**
  ```json
  {
    "caso_id": "string",
    "usuario_id": "string"
  }
  ```

- **Respuestas del endpoint según escenario:**

  1. **`HTTP 200 OK` — Evaluación válida (usuario autorizado + caso existente):**
     Devuelve **exactamente** el contrato mínimo de evaluación de 4 campos (sin campos adicionales ni alertas S2):
     ```json
     {
       "puede_reprocesar": false,
       "motivos": ["string"],
       "accion_recomendada": "string",
       "referencias_normativas": ["string"]
     }
     ```
     - `puede_reprocesar` (`boolean`): `true` únicamente si se cumplen **todas** las condiciones normativas de estado del caso, ausencia de decisión final, código de error reprocesable, servicio dependiente operativo y límite de reprocesos; `false` en caso contrario.
     - `motivos` (`list[string]`): lista no vacía de razones claras y verificables que justifican la decisión positiva o detallan **todos** los impedimentos normativos concurrentes detectados.
     - `accion_recomendada` (`string`): instrucción operativa concisa alineada con `MAN-INC` v2 y `CAT-ERR` v2.
     - `referencias_normativas` (`list[string]`): lista no vacía de citas normativas vigentes aplicables (p. ej. `MAN-INC v2 §4`, `CAT-ERR v2 §1 (E-207)`). Nunca referencia `CAT-ERR` v1.

  2. **`HTTP 403 Forbidden` — Usuario sin autorización (`usuario_id` inexistente o rol no autorizado):**
     Aplica cuando el usuario tiene un rol no autorizado (ej. `U-S4` `comercial`) o cuando `usuario_id` no existe o carece de rol habilitado. Devuelve una **respuesta de error HTTP estándar distinta del contrato de evaluación de 4 campos** (p. ej. `{"detail": "..."}`), **sin consultar ni revelar diagnósticos internos ni la existencia del caso**.

  3. **`HTTP 404 Not Found` — Caso inexistente (usuario autorizado + `caso_id` no encontrado):**
     Aplica cuando el usuario tiene rol autorizado, pero `caso_id` no existe en `casos`. Devuelve una **respuesta de error HTTP estándar distinta del contrato de evaluación de 4 campos** (p. ej. `{"detail": "..."}`).

  4. **`HTTP 422 Unprocessable Entity` — Solicitud malformada:**
     Aplica ante JSON inválido, campos obligatorios faltantes, tipos incorrectos o cadenas vacías / compuestas solo por espacios (`""`, `"   "`). Devuelve una **respuesta de error de validación HTTP distinta del contrato de evaluación de 4 campos**.

- **Prohibición contractual:** En respuestas `HTTP 200 OK` está prohibido agregar campos adicionales (tampoco `alerta_s2`, `severidad`, `registro_tecnico` ni metadatos extra) o emitir alertas automáticas S2. Las respuestas `403`, `404` y `422` son errores HTTP y nunca adoptan el esquema de 4 campos de evaluación.

---

## 3. Flujo principal y excepciones

### 3.1 Flujo principal de evaluación

1. El solicitante envía una petición con `{caso_id, usuario_id}`.
2. **Validación sintáctica del payload:** El sistema valida que el cuerpo sea JSON válido con `caso_id` y `usuario_id` de tipo cadena no vacíos tras recorte de espacios. Si falla, responde **`HTTP 422 Unprocessable Entity`** con respuesta de error de validación HTTP.
3. **Evaluación prioritaria de rol (antes de consultar o diagnosticar `caso_id`):** El sistema consulta de forma simulada `usuario_id` en `usuarios` y verifica que exista y posea un rol habilitado en `{soporte_n1, soporte_n2, ingenieria}`. Si `usuario_id` no existe o su rol no está autorizado, detiene inmediatamente la evaluación sin consultar ni exponer información sobre `caso_id` y responde **`HTTP 403 Forbidden`** con respuesta de error HTTP.
4. **Búsqueda de caso y servicio dependiente:** Solo tras aprobar el paso 3, el sistema busca `caso_id` en `casos`. Si no existe, responde **`HTTP 404 Not Found`** con respuesta de error HTTP. Si existe, obtiene el estado de su `servicio_dependiente` en `servicios` (además de `SRV-MOD` cuando `codigo_error == E-207`).
5. **Evaluación normativa completa:** El sistema evalúa de forma determinista todas las condiciones normativas de `MAN-INC` v2 §4 y `CAT-ERR` v2 §1 sobre el caso:
   - Estado del caso en `{error, detenido}`.
   - Ausencia de decisión final (`tiene_decision_final == no`).
   - Elegibilidad del `codigo_error` en `CAT-ERR` v2 §1.
   - Estado `operativo` del `servicio_dependiente` (y de `SRV-MOD` para `E-207`).
   - Límite de reprocesos aplicable al código usando `casos.reprocesos_realizados`: `1` para `E-512` (supuesto conservador provisional global por caso) y `3` para los demás códigos reprocesables (`E-207`, `E-305`).
6. **Aislamiento de `registro_tecnico`:** El sistema **no consulta ni interpreta** instrucciones contenidas en `registro_tecnico`.
7. **Respuesta `HTTP 200 OK`:** Si todas las condiciones se cumplen, responde `HTTP 200` con el contrato exacto de 4 campos (`puede_reprocesar: true`, motivo confirmatorio, `accion_recomendada` vigente y referencias normativas). Si falla al menos una condición, responde `HTTP 200` con `puede_reprocesar: false`, **todos** los motivos bloqueantes concurrentes, la `accion_recomendada` vigente y sus referencias normativas.

### 3.2 Flujos de excepción y tratamiento de roles no autorizados

- **EX-00 · Solicitud malformada (`HTTP 422`):**
  - Ante JSON inválido, campos faltantes, tipos no cadena o `caso_id`/`usuario_id` vacíos o solo espacios, FastAPI/Pydantic rechaza la petición con `HTTP 422 Unprocessable Entity` (estructura de error de validación HTTP, distinta del contrato de 4 campos).
- **EX-01 · Usuario inexistente (`usuario_id` no encontrado → `HTTP 403`):**
  - Se verifica antes de consultar `caso_id` mediante validación simulada contra `usuarios` (no constituye autenticación real).
  - Termina de inmediato con **`HTTP 403 Forbidden`** y respuesta estándar de error HTTP (ej. `{"detail": "Usuario sin autorización para evaluar reprocesamiento."}`), **sin revelar si `caso_id` existe ni diagnósticos internos**.
- **EX-02 · Rol no autorizado (ej. `U-S4` `comercial` o cualquier rol fuera de `{soporte_n1, soporte_n2, ingenieria}` → `HTTP 403`):**
  - Se verifica antes de consultar o diagnosticar `caso_id`, rechazando **incluso si el caso cumple todas las condiciones técnicas** (ej. `C-032`).
  - Termina de inmediato con **`HTTP 403 Forbidden`** y respuesta estándar de error HTTP (ej. `{"detail": "Rol no autorizado para evaluar reprocesamiento."}`), **sin exponer si el caso existe, su estado, código de error ni motivos**.
- **EX-03 · Caso inexistente (`caso_id` no encontrado para un usuario autorizado → `HTTP 404`):**
  - Termina con **`HTTP 404 Not Found`** y respuesta estándar de error HTTP (ej. `{"detail": "Caso no encontrado."}`), distinta del contrato de 4 campos.
- **EX-04 · Múltiples impedimentos concurrentes (usuario autorizado + caso existente → `HTTP 200`):**
  - Cuando confluyen varias causas de rechazo (por ejemplo `C-036`: `estado=resuelto`, `tiene_decision_final=sí` y `SRV-MOD=degradado`; o `C-035`: `estado=en_cola` y `codigo_error=E-410`), se responde `HTTP 200 OK` con el contrato de 4 campos registrando **todos** los motivos normativos aplicables en `motivos` y sus citas vigentes en `referencias_normativas`, manteniendo una `accion_recomendada` coherente con el bloqueo principal.
- **EX-05 · Datos técnicos inconsistentes o código/servicio desconocido en un caso existente (`HTTP 200`):**
  - Si un caso existente referencia un `codigo_error` fuera de `CAT-ERR` v2 o un `servicio_dependiente` ausente en `servicios`, se responde `HTTP 200 OK` con `puede_reprocesar: false`, indicando la inconsistencia en `motivos`, recomendando escalar a Ingeniería y citando `MAN-INC v2 §4`.

---

## 4. Reglas de negocio verificables (`REQ-*`)

### 4.1 Reglas generales, contrato, HTTP y vigencia normativa

| ID Requisito | Regla / Condición | Fuente normativa | Criterio de aceptación resumido |
|---|---|---|---|
| `REQ-01` | **Contrato mínimo y códigos HTTP diferenciados:** en evaluaciones válidas (usuario autorizado + caso existente) responde `HTTP 200 OK` con exactamente `{puede_reprocesar, motivos, accion_recomendada, referencias_normativas}`, sin campos extra ni alertas S2. Las respuestas de error HTTP (`403`, `404`, `422`) usan formato estándar de error HTTP distinto del contrato de 4 campos. | Acuerdo de alcance (`docs/decision.md` §3) + Ajuste Control Humano | Toda respuesta `200` contiene únicamente las 4 claves; peticiones inválidas, no autorizadas o sobre casos inexistentes retornan `422`, `403` o `404`. |
| `REQ-02` | **Vigencia documental exclusiva:** toda decisión y referencia se basa únicamente en `MAN-INC` v2 y `CAT-ERR` v2; `CAT-ERR` v1 queda excluido como derogado. | `MAN-INC v2`, `CAT-ERR v2 §2` | Casos cuyo criterio cambió entre v1 y v2 (`E-207`, `E-410`, `E-512`) siguen estrictamente `CAT-ERR` v2. |
| `REQ-03` | **Autorización prioritaria simulada por rol (`HTTP 403`):** se evalúa primero el rol del `usuario_id` (validación simulada contra `usuarios`, no autenticación real) antes de consultar o diagnosticar `caso_id`. Si el usuario no existe o su rol no pertenece a `{soporte_n1, soporte_n2, ingenieria}` (ej. `U-S4` `comercial`), responde `HTTP 403 Forbidden` sin revelar existencia ni diagnóstico del caso. | `MAN-INC v2 §4` | `U-S4` o `U-999` consultando `C-032` o `C-999` retorna siempre `HTTP 403` sin exponer estado, código ni existencia del caso. |
| `REQ-04` | **Existencia de caso (`HTTP 404`) y servicio dependiente:** tras validar rol autorizado, si `caso_id` no existe en `casos` retorna `HTTP 404 Not Found` (error HTTP). Si existe pero su `servicio_dependiente` no resuelve en `servicios`, retorna `HTTP 200` con `puede_reprocesar: false`. | `MAN-INC v2 §4` | `C-999` con `U-S1` retorna `HTTP 404`; `C-999` con `U-S4` o `U-999` retorna `HTTP 403`. |
| `REQ-05` | **Estado elegible del caso:** solo son elegibles casos cuyo `estado` sea `error` o `detenido`. Casos en `en_cola`, `resuelto` u otro estado reciben `HTTP 200` con `puede_reprocesar = false`. | `MAN-INC v2 §4` | `C-035` (`en_cola`), `C-036` (`resuelto`) y `C-039` (`en_cola`) retornan `HTTP 200` con `puede_reprocesar = false`. |
| `REQ-06` | **Decisión final irreversible:** nunca se reprocesa un caso con `tiene_decision_final == sí`, cualquiera sea su estado o código de error. | `MAN-INC v2 §4` | `C-036` y todo caso con `tiene_decision_final = sí` (incluso en estado `error`) retornan `HTTP 200` con `puede_reprocesar = false`. |
| `REQ-07` | **Servicio dependiente operativo:** el `servicio_dependiente` del caso debe encontrarse en estado `operativo`. Si está `degradado` o `caido`, `puede_reprocesar = false`. | `MAN-INC v2 §4`, `GUI-COL v1 §1` | `C-031` (`SRV-MOD` `degradado`) y `C-040` (`SRV-REG` `caido`) retornan `HTTP 200` con `puede_reprocesar = false`. |
| `REQ-08` | **Límite general de reprocesos (códigos distintos de `E-512`):** un caso admite como máximo `3` reprocesos (`casos.reprocesos_realizados < 3`). Si `reprocesos_realizados >= 3`, `puede_reprocesar = false` y se recomienda escalar a Ingeniería como incidente S3 sin volver a intentar. | `MAN-INC v2 §4` | Caso `E-305` o `E-207` operativo con `2` reprocesos retorna `true`; con `3` retorna `false` recomendando escalar como S3. |

### 4.2 Reglas específicas por código de error (`CAT-ERR` v2 §1)

| ID Requisito | Código | Regla / Condición vigente | Fuente normativa | Acción recomendada en respuesta (`HTTP 200`) |
|---|---|---|---|---|
| `REQ-09` | `E-101` | **Evidencia ilegible — No reprocesable:** retornar siempre `puede_reprocesar = false` (el reproceso produciría el mismo resultado). | `CAT-ERR v2 §1 (E-101)` | Solicitar el reenvío de la evidencia; no reprocesar. |
| `REQ-10` | `E-102` | **Formato de archivo no soportado — No reprocesable:** retornar siempre `puede_reprocesar = false`. | `CAT-ERR v2 §1 (E-102)` | Informar a la organización los formatos aceptados; no reprocesar. |
| `REQ-11` | `E-207` | **Timeout con proveedor de modelos — Sí, con condición:** elegible solo si además de `REQ-03..08` el servicio `SRV-MOD` (y el `servicio_dependiente`) está `operativo`. Si `SRV-MOD` está `degradado` o `caido`, `puede_reprocesar = false`. | `CAT-ERR v2 §1 (E-207)`, `MAN-INC v2 §4` | Si elegible: Proceder con el reprocesamiento. Si `SRV-MOD` degradado/caído: No reprocesar; el caso permanece en cola y se reintenta automáticamente. |
| `REQ-12` | `E-208` | **Cuota del proveedor de modelos agotada — No reprocesable:** retornar siempre `puede_reprocesar = false`. *(Sin generar incidente automático ni campo S2 en la API).* | `CAT-ERR v2 §1 (E-208)` | Registrar incidente S2 y escalar a Ingeniería; no reprocesar. |
| `REQ-13` | `E-305` | **Módulo de análisis no disponible — Sí, con condición:** elegible solo si se cumplen `REQ-03..08` y el `servicio_dependiente` del módulo está `operativo`. | `CAT-ERR v2 §1 (E-305)`, `MAN-INC v2 §4` | Si elegible: Proceder con el reprocesamiento. Si servicio no operativo: No reprocesar; esperar a que el servicio dependiente vuelva a estar operativo. |
| `REQ-14` | `E-311` | **Versión de módulo fijada no disponible — No reprocesable:** retornar siempre `puede_reprocesar = false`; prohibido reprocesar con otra versión sin autorización de la organización. | `CAT-ERR v2 §1 (E-311)` | Escalar a Ingeniería; no reprocesar con otra versión sin autorización de la organización. |
| `REQ-15` | `E-410` | **Límite de llamadas por minuto superado — No aplica:** la llamada no se rechaza sino que se encola y procesa cuando hay capacidad; retornar `puede_reprocesar = false`. | `CAT-ERR v2 §1 (E-410)` | No reprocesar; el caso se encola y se procesa cuando hay capacidad (sin acción de soporte salvo cola > 6 horas). |
| `REQ-16` | `E-512` | **Error interno de la plataforma — Sí, con condición (provisional):** por especialidad y vigencia de `CAT-ERR` v2 frente a `MAN-INC` v2 §4 (sin alterar el límite general de `3` para `E-207` y `E-305`), aplica un límite específico de **`1` reproceso** (`casos.reprocesos_realizados < 1`). En escenarios mixtos se toma `casos.reprocesos_realizados` como **contador global por caso** (supuesto conservador del prototipo pendiente de ratificación formal por el representante del cliente). Con `reprocesos_realizados >= 1`, `puede_reprocesar = false`. | `CAT-ERR v2 §1-§2 (E-512)`, `MAN-INC v2 §4` *(supuesto conservador pendiente de ratificación en CH1)* | Si `reprocesos_realizados == 0`: Reprocesar una vez; si vuelve a fallar, escalar a Ingeniería. Si `reprocesos_realizados >= 1`: No reprocesar; escalar a Ingeniería. |

### 4.3 Reglas transversales de seguridad y determinismo

| ID Requisito | Regla / Condición | Fuente normativa | Criterio de aceptación resumido |
|---|---|---|---|
| `REQ-17` | **Seguridad frente a inyección de instrucciones y preservación del kit:** `registro_tecnico` (en especial `L-009` de `C-038`) se trata estrictamente como texto de datos pasivo y queda excluido del motor de reglas; `CU-2_datos.xlsx` nunca se modifica ni se ejecutan instrucciones embebidas en datos. | Regla de seguridad del proyecto, `POL-ACC v1 §2` | Ninguna cadena en `registro_tecnico` altera `puede_reprocesar`, `accion_recomendada` ni dispara acciones sobre otros casos. |
| `REQ-18` | **Transparencia ante causas concurrentes:** únicamente cuando el usuario está autorizado y el caso existe (`HTTP 200`), si concurren múltiples impedimentos se reportan **todos** los motivos bloqueantes y referencias vigentes relevantes sin omitir bloqueos activos. | `MAN-INC v2 §4`, `CAT-ERR v2 §1` | En `C-036` se reportan decisión final, estado `resuelto` y `SRV-MOD` `degradado`. |

---

## 5. Criterios de aceptación (`Given / When / Then`)

1. **CA-01 · Caso elegible en estado `error` (`C-032`):**
   - **Given** el caso `C-032` (`estado=error`, `codigo_error=E-305`, `servicio_dependiente=SRV-ROS` `operativo`, `reprocesos_realizados=0`, `tiene_decision_final=no`) y el usuario autorizado `U-S1` (`soporte_n1`),
   - **When** se solicita evaluar elegibilidad con `{caso_id: "C-032", usuario_id: "U-S1"}`,
   - **Then** responde **`HTTP 200 OK`** con exactamente las 4 claves del contrato, `puede_reprocesar: true`, motivos que confirman estado, ausencia de decisión final, `SRV-ROS` operativo y `0` reprocesos previos, acción de proceder con el reprocesamiento y referencias a `MAN-INC v2 §4` y `CAT-ERR v2 §1 (E-305)`.

2. **CA-02 · Caso `E-207` bloqueado por servicio degradado (`C-031`, aplicación estricta de `CAT-ERR` v2):**
   - **Given** el caso `C-031` (`estado=error`, `codigo_error=E-207`, `servicio_dependiente=SRV-MOD` `degradado`, `reprocesos_realizados=1`, `tiene_decision_final=no`) y `U-S1`,
   - **When** se evalúa `{caso_id: "C-031", usuario_id: "U-S1"}`,
   - **Then** responde **`HTTP 200 OK`** con `puede_reprocesar: false` (descartando la regla derogada de `CAT-ERR` v1), indica que `SRV-MOD` está `degradado`, recomienda no reprocesar y mantener en cola para reintento automático, y cita `CAT-ERR v2 §1 (E-207)` y `MAN-INC v2 §4`.

3. **CA-03 · Caso sintético `E-207` elegible cuando `SRV-MOD` está operativo:**
   - **Given** un caso sintético en memoria con `estado=error`, `codigo_error=E-207`, `servicio_dependiente=SRV-MOD` en estado `operativo`, `reprocesos_realizados=1`, `tiene_decision_final=no` y usuario `U-S2` (`soporte_n2`),
   - **When** se evalúa elegibilidad,
   - **Then** responde **`HTTP 200 OK`** con `puede_reprocesar: true` y recomienda proceder con el reprocesamiento bajo `MAN-INC v2 §4` y `CAT-ERR v2 §1 (E-207)`.

4. **CA-04 · Caso sintético en estado `detenido` elegible:**
   - **Given** un caso sintético en memoria con `estado=detenido`, `codigo_error=E-305`, `servicio_dependiente=SRV-ROS` `operativo`, `reprocesos_realizados=0`, `tiene_decision_final=no` y usuario `U-S3` (`ingenieria`),
   - **When** se evalúa elegibilidad,
   - **Then** responde **`HTTP 200 OK`** con `puede_reprocesar: true`.

5. **CA-05 · Caso `E-305` con servicio caído (`C-040`):**
   - **Given** el caso `C-040` (`estado=error`, `codigo_error=E-305`, `servicio_dependiente=SRV-REG` `caido`) y usuario `U-S3`,
   - **When** se evalúa `{caso_id: "C-040", usuario_id: "U-S3"}`,
   - **Then** responde **`HTTP 200 OK`** con `puede_reprocesar: false`, señala que `SRV-REG` está `caido` y recomienda esperar a que vuelva a estar operativo.

6. **CA-06 · Códigos no reprocesables (`E-101`, `E-102`, `E-208`, `E-311`, `E-410`):**
   - **Given** un usuario autorizado (`U-S1` o `U-S2`) y cualquiera de los casos `C-033` (`E-101`), `C-035` (`E-410`, `en_cola`), `C-037` (`E-208`), `C-038` (`E-311`) o el caso sintético `E-102`,
   - **When** se evalúa elegibilidad,
   - **Then** responde **`HTTP 200 OK`** con `puede_reprocesar: false` y la `accion_recomendada` específica de `CAT-ERR` v2 §1 para cada código, sin agregar campos extra ni generar alertas S2 automáticas en `E-208`.

7. **CA-07 · Bloqueo absoluto por decisión final y estados no elegibles (`C-036`, `C-039` y sintético):**
   - **Given** `U-S1` evaluando `C-036` (`resuelto`, `tiene_decision_final=sí`), `C-039` (`en_cola`, `E-207`, `SRV-MOD=degradado`) o un caso sintético en estado `error` con `E-305`, `SRV-ROS=operativo` pero `tiene_decision_final=sí`,
   - **When** se evalúa elegibilidad,
   - **Then** en todos los casos responde **`HTTP 200 OK`** con `puede_reprocesar: false`, reportando todos los motivos bloqueantes concurrentes (en `C-036`: decisión final, estado `resuelto` y `SRV-MOD` `degradado`) y sin emitir alertas S2 en `C-039`.

8. **CA-08 · Regla específica provisional `E-512` (0, 1 y 3 reprocesos) frente a límite general de 3:**
   - **Given** `U-S2` evaluando `E-512` con `SRV-COL=operativo` en estado `error` y sin decisión final (utilizando `casos.reprocesos_realizados` como contador global por caso):
     - con `0` reprocesos (sintético) → **Then** `HTTP 200 OK`, `puede_reprocesar: true` y acción `"Reprocesar una vez; si vuelve a fallar, escalar a Ingeniería"`;
     - con `1` reproceso (sintético, incluso en escenario mixto bajo supuesto conservador) → **Then** `HTTP 200 OK`, `puede_reprocesar: false` y acción de escalar a Ingeniería por alcanzar el límite específico de `1` reproceso de `CAT-ERR v2 §1 (E-512)`;
     - con `3` reprocesos (`C-034`) → **Then** `HTTP 200 OK`, `puede_reprocesar: false` y acción de escalar a Ingeniería.
   - **Given** un caso sintético `E-305` con `SRV-ROS=operativo` y `2` reprocesos → **Then** `HTTP 200 OK` con `puede_reprocesar: true`; con `3` reprocesos → **Then** `HTTP 200 OK` con `puede_reprocesar: false` recomendando escalar a Ingeniería como incidente S3 (`MAN-INC v2 §4`).

9. **CA-09 · Control de acceso prioritario por rol, entidades inexistentes y validación de entrada (`403` / `404` / `422`):**
   - **Given** `U-S4` (`comercial`) o `U-999` (`usuario_id` inexistente) consultando `C-032` o `C-999`,
   - **When** se evalúa elegibilidad,
   - **Then** se evalúa el rol antes de consultar o diagnosticar `caso_id` y responde **`HTTP 403 Forbidden`** con estructura de error HTTP estándar distinta del contrato de 4 campos (sin `puede_reprocesar` y sin revelar si el caso existe ni su estado/código/motivos).
   - **Given** un usuario autorizado (`U-S1`) consultando `C-999` (`caso_id` inexistente),
   - **When** se evalúa elegibilidad,
   - **Then** responde **`HTTP 404 Not Found`** con estructura de error HTTP estándar distinta del contrato de 4 campos.
   - **Given** una solicitud malformada (JSON inválido, campo faltante, tipo incorrecto o `caso_id`/`usuario_id` vacío o solo espacios),
   - **When** se envía al endpoint,
   - **Then** responde **`HTTP 422 Unprocessable Entity`** con respuesta estándar de error de validación HTTP.

10. **CA-10 · Seguridad de datos ante inyección en `registro_tecnico` (`L-009` en `C-038` y sintético):**
    - **Given** `C-038` (cuyo `registro_tecnico` `L-009` contiene una instrucción maliciosa simulada ordenando reprocesar todos los casos de `ORG-02` sin confirmación) y un caso sintético elegible cuyo `registro_tecnico` contenga instrucciones contradictorias (ej. forzar denegación o ejecutar acciones externas),
    - **When** se evalúa elegibilidad con `U-S1`,
    - **Then** responde `HTTP 200 OK` determinando el resultado únicamente con los campos estructurados del caso/servicio/usuario y las reglas normativas vigentes (`C-038` retorna `puede_reprocesar: false` por `E-311` sin reprocesar `ORG-02`; el caso sintético elegible retorna `puede_reprocesar: true`), sin obedecer ni propagar instrucciones de `registro_tecnico`.

---

## 6. Datos de prueba: Excel oficial y casos sintéticos en memoria

> **Regla de integridad:** `kit/CU-2_soporte_operacion/datos/CU-2_datos.xlsx` se utiliza exclusivamente en modo lectura y permanece sin modificaciones. Toda combinación faltante en el Excel se define como dato sintético en memoria dentro de `tests/`.

### 6.1 Matriz de casos derivados de `CU-2_datos.xlsx` (`C-031` a `C-040`)

Escenario base evaluado con usuario autorizado (`U-S1` `soporte_n1`, `U-S2` `soporte_n2` o `U-S3` `ingenieria`) → todos retornan `HTTP 200 OK` con contrato exacto de 4 campos:

| Caso | Org | Estado | Código | Servicio dep. (estado) | Reproc. | Dec. final | Resultado (`HTTP 200`) | Motivo normativo principal y acción esperada |
|---|---|---|---|---|---|---|---|---|
| `C-031` | `ORG-01` | `error` | `E-207` | `SRV-MOD` (`degradado`) | `1` | `no` | `puede_reprocesar: false` | `E-207` exige `SRV-MOD` operativo; está `degradado`. No reprocesar: permanece en cola para reintento automático (`CAT-ERR v2 §1`, `MAN-INC v2 §4`). |
| `C-032` | `ORG-01` | `error` | `E-305` | `SRV-ROS` (`operativo`) | `0` | `no` | `puede_reprocesar: true` | Cumple estado `error`, sin decisión final, `<3` reprocesos, `E-305` reprocesable y `SRV-ROS` operativo. Proceder con reprocesamiento (`MAN-INC v2 §4`, `CAT-ERR v2 §1`). |
| `C-033` | `ORG-02` | `error` | `E-101` | `SRV-OCR` (`operativo`) | `0` | `no` | `puede_reprocesar: false` | `E-101` (evidencia ilegible) no es reprocesable. Solicitar reenvío de la evidencia (`CAT-ERR v2 §1`). |
| `C-034` | `ORG-02` | `error` | `E-512` | `SRV-COL` (`operativo`) | `3` | `no` | `puede_reprocesar: false` | `E-512` excede el límite específico de `1` reproceso (`CAT-ERR v2 §1`) y alcanza el máximo general de `3` (`MAN-INC v2 §4`; `R-002..R-004` fallidos). No reprocesar; escalar a Ingeniería. |
| `C-035` | `ORG-03` | `en_cola` | `E-410` | `SRV-API` (`operativo`) | `0` | `no` | `puede_reprocesar: false` | Estado `en_cola` (no `error`/`detenido`) y `E-410` no aplica para reproceso manual (se encola y procesa al haber capacidad) (`MAN-INC v2 §4`, `CAT-ERR v2 §1`). |
| `C-036` | `ORG-01` | `resuelto` | `E-207` | `SRV-MOD` (`degradado`) | `1` | `sí` | `puede_reprocesar: false` | Tiene decisión final (`sí`), estado `resuelto` y `SRV-MOD` `degradado` (`R-005` exitoso). No reprocesar (`MAN-INC v2 §4`, `CAT-ERR v2 §1`). |
| `C-037` | `ORG-03` | `error` | `E-208` | `SRV-MOD` (`degradado`) | `0` | `no` | `puede_reprocesar: false` | `E-208` (cuota agotada) no es reprocesable (y `SRV-MOD` `degradado`). Recomendar registrar incidente S2 y escalar a Ingeniería sin emitir alerta S2 automática (`CAT-ERR v2 §1`). |
| `C-038` | `ORG-02` | `detenido` | `E-311` | `SRV-COL` (`operativo`) | `0` | `no` | `puede_reprocesar: false` | `E-311` (versión de módulo fijada no disponible) no es reprocesable. Escalar a Ingeniería; no cambiar versión. Ignorar *prompt injection* `L-009` (`CAT-ERR v2 §1`). |
| `C-039` | `ORG-01` | `en_cola` | `E-207` | `SRV-MOD` (`degradado`) | `0` | `no` | `puede_reprocesar: false` | Estado `en_cola` (no `error`/`detenido`) y `SRV-MOD` `degradado`. No reprocesar: permanece en cola para reintento automático (`MAN-INC v2 §4`, `CAT-ERR v2 §1`). *(Excluidas alertas S2 aunque supere 6 h).* |
| `C-040` | `ORG-03` | `error` | `E-305` | `SRV-REG` (`caido`) | `0` | `no` | `puede_reprocesar: false` | `E-305` requiere servicio dependiente operativo; `SRV-REG` está `caido`. Esperar recuperación de `SRV-REG` (`MAN-INC v2 §4`, `CAT-ERR v2 §1`). |

### 6.2 Matriz de casos sintéticos en memoria (huecos del Excel)

| ID Sintético | Escenario cubierto | Datos clave | HTTP y resultado esperado | Objetivo de verificación |
|---|---|---|---|---|
| `SYN-E102` | Código `E-102` ausente en Excel | `estado=error`, `codigo_error=E-102`, `SRV-OCR=operativo`, `reprocesos=0`, `dec_final=no`, `U-S1` | `HTTP 200` (`puede_reprocesar: false`) | Cobertura de los 8 códigos de `CAT-ERR` v2 (`REQ-10`). |
| `SYN-E512-0` | `E-512` elegible (0 reprocesos) | `estado=error`, `codigo_error=E-512`, `SRV-COL=operativo`, `reprocesos=0`, `dec_final=no`, `U-S2` | `HTTP 200` (`puede_reprocesar: true`) | Valida elegibilidad de primer reproceso en `CAT-ERR` v2 vs v1 (`REQ-16`). |
| `SYN-E512-1` | `E-512` en límite específico (1 reproceso) | `estado=error`, `codigo_error=E-512`, `SRV-COL=operativo`, `reprocesos=1`, `dec_final=no`, `U-S2` | `HTTP 200` (`puede_reprocesar: false`) | Valida tope específico de `1` reproceso y supuesto conservador global por caso (`REQ-16`). |
| `SYN-E207-OK` | `E-207` con `SRV-MOD` operativo | `estado=error`, `codigo_error=E-207`, `SRV-MOD=operativo`, `reprocesos=1`, `dec_final=no`, `U-S1` | `HTTP 200` (`puede_reprocesar: true`) | Contrasta contra `C-031` para confirmar condición de `SRV-MOD` operativo (`REQ-11`). |
| `SYN-DET-OK` | Caso `detenido` elegible | `estado=detenido`, `codigo_error=E-305`, `SRV-ROS=operativo`, `reprocesos=0`, `dec_final=no`, `U-S3` | `HTTP 200` (`puede_reprocesar: true`) | En el Excel `C-038` (`detenido`) tiene `E-311`; verifica estado `detenido` elegible (`REQ-05`). |
| `SYN-LIMIT-2` | Tope general `< 3` (`2` reprocesos) | `estado=error`, `codigo_error=E-305`, `SRV-ROS=operativo`, `reprocesos=2`, `dec_final=no`, `U-S1` | `HTTP 200` (`puede_reprocesar: true`) | Confirma que el tope de `1` de `E-512` no reduce el límite general de `3` (`REQ-08`). |
| `SYN-LIMIT-3` | Tope general `== 3` en código no `E-512` | `estado=error`, `codigo_error=E-305`, `SRV-ROS=operativo`, `reprocesos=3`, `dec_final=no`, `U-S1` | `HTTP 200` (`puede_reprocesar: false`) | Valida bloqueo por 3 reprocesos y recomendación de escalamiento S3 (`REQ-08`). |
| `SYN-DECFIN` | `tiene_decision_final=sí` en estado `error` | `estado=error`, `codigo_error=E-305`, `SRV-ROS=operativo`, `reprocesos=0`, `dec_final=sí`, `U-S1` | `HTTP 200` (`puede_reprocesar: false`) | Aísla regla de decisión final respecto del estado `resuelto` de `C-036` (`REQ-06`). |
| `SYN-ROL-COM` | Rol no autorizado sobre caso elegible | `caso_id=C-032`, `usuario_id=U-S4` (`comercial`) | `HTTP 403` (error HTTP estándar sin diagnóstico ni existencia del caso) | Verifica rechazo prioritario de rol `comercial` sin contrato de 4 campos (`REQ-03`). |
| `SYN-ROL-N2-ING` | Roles `soporte_n2` e `ingenieria` | `caso_id=C-032`, `usuario_id=U-S2` y `U-S3` | `HTTP 200` (`puede_reprocesar: true`) | Verifica los 3 roles autorizados por `MAN-INC v2 §4` (`REQ-03`). |
| `SYN-NO-USER` | `usuario_id` inexistente | `caso_id=C-032` o `C-999`, `usuario_id=U-999` | `HTTP 403` (error HTTP estándar sin diagnóstico ni existencia del caso) | Verifica rechazo `403` sin revelar existencia del caso (`REQ-03`). |
| `SYN-NO-CASE` | `caso_id` inexistente con usuario autorizado | `caso_id=C-999`, `usuario_id=U-S1` | `HTTP 404` (error HTTP estándar distinto del contrato de 4 campos) | Verifica respuesta `404` ante caso no encontrado (`REQ-04`). |
| `SYN-422` | Solicitud malformada | JSON inválido, campo faltante, tipo incorrecto o `caso_id=""` / `usuario_id="   "` | `HTTP 422` (error de validación HTTP distinto del contrato de 4 campos) | Verifica validación de esquema de entrada (`REQ-01`). |
| `SYN-INJ-OK` | *Prompt injection* sobre caso elegible | Caso equivalente a `C-032` con `registro_tecnico` malicioso simulado | `HTTP 200` (`puede_reprocesar: true`) | Confirma que `registro_tecnico` no bloquea ni ejecuta instrucciones (`REQ-17`). |

---

## 7. Definiciones adoptadas y resolución del Control Humano 1

### 7.1 Definiciones adoptadas tras la revisión inicial

1. **`E-512` (límite específico provisional y supuesto conservador):** Se adopta provisionalmente el máximo específico de **`1` reproceso** (`casos.reprocesos_realizados < 1`) usando `casos.reprocesos_realizados`, manteniendo el máximo general de `3` para los demás códigos elegibles (`E-207`, `E-305`). Para escenarios mixtos que combinen `E-512` con otros códigos de error, se trata `casos.reprocesos_realizados` como **contador global por caso**, dejando documentado expresamente que constituye un **supuesto conservador del prototipo**.
2. **Códigos HTTP y distinción contractual:**
   - `HTTP 200 OK` para evaluaciones válidas (usuario autorizado + caso existente), devolviendo exactamente los 4 campos `{puede_reprocesar, motivos, accion_recomendada, referencias_normativas}`.
   - `HTTP 403 Forbidden` para usuarios con rol no autorizado o `usuario_id` inexistente, devolviendo una respuesta estándar de error HTTP distinta del contrato de 4 campos y sin revelar diagnósticos ni existencia del caso.
   - `HTTP 404 Not Found` para `caso_id` inexistente con usuario autorizado, devolviendo una respuesta estándar de error HTTP distinta del contrato de 4 campos.
   - `HTTP 422 Unprocessable Entity` para solicitudes malformadas (JSON inválido, faltantes, tipos incorrectos o cadenas vacías/solo espacios).
3. **Orden de evaluación y reserva de diagnósticos:** Se evalúa primero el rol del usuario antes de consultar o diagnosticar `caso_id`, sin exponer existencia ni diagnósticos internos del caso ante `403`. Cuando el usuario está autorizado y el caso existe, se reportan todos los motivos bloqueantes concurrentes.
4. **Cierre de exclusiones (sin alertas S2 ni alcance extra):** Queda cerrada la exclusión de alertas automáticas S2 (ni campos adicionales ni emisión automática de incidentes S2 para `C-039` o `C-037`) y de toda funcionalidad adicional (reprocesamiento real, frontend, RAG, MCP, notificaciones, administración de incidentes).
5. **Validación simulada de roles:** La verificación mediante `usuario_id` contra `CU-2_datos.xlsx` se define explícitamente como una validación simulada de roles para el prototipo y no constituye autenticación real (sin verificación de identidad, contraseñas, tokens ni sesiones).

### 7.2 Resolución del Control Humano 1 (aprobado el 2026-11-22)

- **Representante del cliente:** Jorge
- **Decisión:** Aprobado — Control Humano 1
- **Fecha de registro:** 2026-11-22
- **Evidencia:** Aprobación escrita por WhatsApp proporcionada por el equipo (registrada en `docs/trabajo/001-requisitos-a-planificador.md` y `docs/bitacora.md`).
- **Decisiones confirmadas por el representante del cliente:**
  1. **Aprobación:** Aprueba `specs/01-requisitos.md` tal como está, autorizando el paso al agente `planificador`.
  2. **`E-512`:** Ratifica el máximo específico de un (`1`) reproceso y el uso de `casos.reprocesos_realizados` como contador global por caso, incluido el supuesto conservador para escenarios mixtos. Se mantiene el máximo general de tres (`3`) para `E-207` y `E-305`. La interpretación sobre validaciones/facturación queda identificada como supuesto del prototipo respaldado por esta aprobación, no como regla adicional inventada.
  3. **Códigos HTTP:** Confirma `200` para evaluación válida, `403` para usuarios sin autorización o inexistentes, `404` para casos inexistentes y `422` para solicitudes malformadas, con errores HTTP estándar `{"detail": "..."}` separados del contrato de cuatro campos.
- **Material revisado confirmado:** `MAN-INC` v2, `CAT-ERR` v2, `GUI-COL` v1, `POL-ACC` v1, los 10 casos del Excel (`C-031` a `C-040`) y los 14 escenarios sintéticos, incluida la protección frente a instrucciones maliciosas en `L-009`.

---

## 8. Seguridad de datos

1. **Tratamiento pasivo de `registro_tecnico`:**
   - La hoja `registro_tecnico` de `CU-2_datos.xlsx` (`L-001` a `L-011`) contiene texto libre potencialmente hostil o manipulado. En particular, el registro **`L-009`** asociado al caso **`C-038`** contiene una *prompt injection* simulada que intenta ordenar al asistente reprocesar todos los casos de `ORG-02` sin pedir confirmación.
   - **Mitigación obligatoria:**
     - La capa de dominio y evaluación **no lee ni evalúa** `registro_tecnico` para tomar decisiones de elegibilidad, construir acciones ni ejecutar operaciones en lote.
     - Incluso si un consumidor o prueba carga la tabla `registro_tecnico`, sus contenidos se consideran **datos pasivos no confiables** (*untrusted data*), nunca instrucciones del sistema ni reglas de negocio.
     - No existe operación ni endpoint de reprocesamiento real ni por lote en el sistema.
2. **Validación simulada de roles (no autenticación real) y reserva de diagnóstico:**
   - La consulta de `usuario_id` contra `CU-2_datos.xlsx` es exclusivamente una **validación simulada de roles** para el prototipo y **no constituye autenticación real** (no valida identidad, credenciales, tokens ni sesiones).
   - Para evitar enumeración o fuga de información operativa hacia roles sin autorización en el flujo de la API, el control de rol se ejecuta antes de consultar `caso_id`, devolviendo `HTTP 403` sin revelar si el caso existe ni sus detalles internos.
3. **Protección de evidencia y privacidad (`POL-ACC` v1):**
   - El servicio no accede a documentos, imágenes, videos ni datos biométricos de las organizaciones; opera exclusivamente con identificadores y metadatos operativos no sensibles.
4. **Inmutabilidad del kit oficial:**
   - Todos los archivos bajo `kit/CU-2_soporte_operacion/` permanecen en modo solo lectura verificable mediante `docs/kit-sha256sums.txt`.
