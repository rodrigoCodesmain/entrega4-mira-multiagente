# Métricas Verificables — Experimento CORRIDA-LB-01

## 1. Resumen general y tiempos observados

| Métrica | Valor observado |
|---|---|
| Modalidad | Agente único (`CORRIDA-LB-01`, sin subagentes ni flujos Implementador/Revisor) |
| Hora de inicio (`date -Is`) | `2026-11-22T21:34:35-03:00` |
| Hora de término de verificación (`date -Is`) | `2026-11-22T21:42:09-03:00` |
| Duración calculada | No disponible (se registran únicamente marcas de inicio y término capturadas con `date -Is`) |
| Consumo de tokens | No disponible |
| Costo estimado | No disponible |
| Intervenciones humanas durante la ejecución | `0` |
| Pruebas ejecutadas (`pytest`) | `58` |
| Pruebas pasadas | `58` |
| Pruebas fallidas | `0` |
| Pruebas omitidas (*skipped*) | `0` |
| Correcciones reales realizadas | `2` |
| Integridad del kit (`docs/kit-sha256sums.txt`) | Verificada (`OK` en los 7 archivos; código de salida `0`) |
| Matriz de trazabilidad (`specs/03-trazabilidad.md`) | Válida (`verificar_trazabilidad.py --check-kit --matrix specs/03-trazabilidad.md`, código `0`) |

---

## 2. Cumplimiento de requisitos (`REQ-01` .. `REQ-18`)

| ID | Descripción resumida | Estado | Evidencia de prueba principal (`tests/` / `src/`) |
|---|---|---|---|
| `REQ-01` | Contrato mínimo 4 campos (`HTTP 200`) y errores HTTP estándar (`403`, `404`, `422`) | Cumplido | `test_casos_excel_contrato_y_decision`, `test_syn_422_payloads_invalidos`, `test_syn_422_json_malformado` |
| `REQ-02` | Vigencia documental exclusiva (`MAN-INC` v2 y `CAT-ERR` v2; exclusión de `CAT-ERR` v1) | Cumplido | `assert_contrato_200`, `test_c031_e207_bloqueado_por_srv_mod_degradado`, `test_c035_motivos_concurrentes_en_cola_y_e410`, `test_syn_e512_0_elegible_con_cero_reprocesos` |
| `REQ-03` | Autorización prioritaria simulada por rol (`HTTP 403` sin consultar ni revelar `caso_id`) | Cumplido | `test_prioridad_rol_no_consulta_caso_ni_revela_diagnosticos`, `test_syn_rol_com_rechaza_403_sin_contrato_evaluacion`, `test_syn_rol_n2_ing_autorizados`, `test_syn_no_user_rechaza_403` |
| `REQ-04` | Existencia de caso (`HTTP 404`) y resolución de `servicio_dependiente` | Cumplido | `test_syn_no_case_retorna_404`, `test_ex05_codigo_desconocido_y_servicio_inexistente` |
| `REQ-05` | Estado elegible del caso únicamente en `{error, detenido}` | Cumplido | `test_c035_motivos_concurrentes_en_cola_y_e410`, `test_c036_motivos_concurrentes_decision_final_resuelto_y_srv_mod`, `test_c039_en_cola_y_srv_mod_degradado_sin_alerta_s2`, `test_syn_det_ok_estado_detenido_elegible` |
| `REQ-06` | Bloqueo irreversible ante `tiene_decision_final == sí` | Cumplido | `test_c036_motivos_concurrentes_decision_final_resuelto_y_srv_mod`, `test_syn_decfin_bloquea_aunque_estado_sea_error` |
| `REQ-07` | Servicio dependiente en estado `operativo` | Cumplido | `test_c031_e207_bloqueado_por_srv_mod_degradado`, `test_c040_e305_bloqueado_por_srv_reg_caido`, `test_e512_con_cero_reprocesos_y_servicio_caido_bloquea` |
| `REQ-08` | Límite general de `3` reprocesos (`< 3`) y escalamiento S3 si `>= 3` | Cumplido | `test_syn_limit_2_permite_tercer_reproceso_general`, `test_syn_limit_3_bloquea_y_escala_como_s3` |
| `REQ-09` | `E-101` (evidencia ilegible) no reprocesable | Cumplido | `test_c033_e101_evidencia_ilegible` |
| `REQ-10` | `E-102` (formato no soportado) no reprocesable | Cumplido | `test_syn_e102_codigo_no_soportado` |
| `REQ-11` | `E-207` (timeout modelos) elegible solo si `SRV-MOD` y dependiente están `operativo` | Cumplido | `test_c031_e207_bloqueado_por_srv_mod_degradado`, `test_syn_e207_ok_con_srv_mod_operativo`, `test_e207_requiere_srv_mod_operativo_aunque_dependiente_este_operativo` |
| `REQ-12` | `E-208` (cuota agotada) no reprocesable, sin emitir alerta S2 automática | Cumplido | `test_c037_e208_motivos_concurrentes_sin_alerta_s2_automatica` |
| `REQ-13` | `E-305` (módulo no disponible) elegible si `servicio_dependiente` está `operativo` | Cumplido | `test_c032_elegible_y_accion_proceder`, `test_c040_e305_bloqueado_por_srv_reg_caido`, `test_syn_det_ok_estado_detenido_elegible` |
| `REQ-14` | `E-311` (versión fijada no disponible) no reprocesable | Cumplido | `test_c038_e311_no_reprocesable_y_sin_rastro_l009` |
| `REQ-15` | `E-410` (límite por minuto) no aplica reproceso manual | Cumplido | `test_c035_motivos_concurrentes_en_cola_y_e410` |
| `REQ-16` | `E-512` (error interno) límite provisional de `1` reproceso sobre contador global por caso | Cumplido | `test_c034_e512_excede_limite_especifico_y_general`, `test_syn_e512_0_elegible_con_cero_reprocesos`, `test_syn_e512_1_bloqueado_en_limite_especifico` |
| `REQ-17` | Seguridad frente a inyección en `registro_tecnico` (`L-009` / `C-038`) e integridad del kit | Cumplido | `test_inyeccion_l009_no_afecta_evaluacion_ni_otros_casos_org02`, `test_syn_inj_ok_ignora_registro_tecnico_hostil_simulado`, `test_sin_endpoints_de_reprocesamiento_real`, `test_integridad_sha256_excel_oficial` |
| `REQ-18` | Transparencia ante causas concurrentes (`motivos` reporta todos los bloqueos activos) | Cumplido | `test_c035_motivos_concurrentes_en_cola_y_e410`, `test_c036_motivos_concurrentes_decision_final_resuelto_y_srv_mod`, `test_c037_e208_motivos_concurrentes_sin_alerta_s2_automatica`, `test_c039_en_cola_y_srv_mod_degradado_sin_alerta_s2` |

---

## 3. Cumplimiento de criterios de aceptación (`CA-01` .. `CA-10`)

| Criterio | Descripción | Estado | Pruebas asociadas |
|---|---|---|---|
| `CA-01` | Caso elegible en estado `error` (`C-032`) | Cumplido | `test_casos_excel_contrato_y_decision[C-032-...]`, `test_c032_elegible_y_accion_proceder` |
| `CA-02` | Caso `E-207` bloqueado por servicio degradado (`C-031`, `CAT-ERR` v2) | Cumplido | `test_casos_excel_contrato_y_decision[C-031-...]`, `test_c031_e207_bloqueado_por_srv_mod_degradado` |
| `CA-03` | Caso sintético `E-207` elegible cuando `SRV-MOD` está operativo | Cumplido | `test_syn_e207_ok_con_srv_mod_operativo[U-S1]`, `[U-S2]` |
| `CA-04` | Caso sintético en estado `detenido` elegible | Cumplido | `test_syn_det_ok_estado_detenido_elegible` |
| `CA-05` | Caso `E-305` con servicio caído (`C-040`) | Cumplido | `test_casos_excel_contrato_y_decision[C-040-...]`, `test_c040_e305_bloqueado_por_srv_reg_caido` |
| `CA-06` | Códigos no reprocesables (`E-101`, `E-102`, `E-208`, `E-311`, `E-410`) sin alertas S2 | Cumplido | `test_c033_...`, `test_c035_...`, `test_c037_...`, `test_c038_...`, `test_syn_e102_codigo_no_soportado` |
| `CA-07` | Bloqueo absoluto por decisión final y estados no elegibles (`C-036`, `C-039`, sintético) | Cumplido | `test_c036_...`, `test_c039_...`, `test_syn_decfin_bloquea_aunque_estado_sea_error` |
| `CA-08` | Regla específica provisional `E-512` (0, 1 y 3 reprocesos) frente a límite general de 3 | Cumplido | `test_syn_e512_0_...`, `test_syn_e512_1_...`, `test_c034_...`, `test_syn_limit_2_...`, `test_syn_limit_3_...` |
| `CA-09` | Control de acceso prioritario por rol, entidades inexistentes y validación (`403`/`404`/`422`) | Cumplido | `test_prioridad_rol_...`, `test_syn_rol_com_...`, `test_syn_no_user_...`, `test_syn_no_case_...`, `test_syn_422_...` |
| `CA-10` | Seguridad de datos ante inyección en `registro_tecnico` (`L-009` en `C-038` y sintético) | Cumplido | `test_inyeccion_l009_no_afecta_evaluacion_ni_otros_casos_org02`, `test_syn_inj_ok_ignora_registro_tecnico_hostil_simulado` |

---

## 4. Cobertura de casos reales de `CU-2_datos.xlsx` (`C-031` .. `C-040`)

| Caso | HTTP | `puede_reprocesar` observado | Estado prueba |
|---|---|---|---|
| `C-031` | `200` | `false` | Pasada (`PASSED`) |
| `C-032` | `200` | `true` | Pasada (`PASSED`) |
| `C-033` | `200` | `false` | Pasada (`PASSED`) |
| `C-034` | `200` | `false` | Pasada (`PASSED`) |
| `C-035` | `200` | `false` | Pasada (`PASSED`) |
| `C-036` | `200` | `false` | Pasada (`PASSED`) |
| `C-037` | `200` | `false` | Pasada (`PASSED`) |
| `C-038` | `200` | `false` | Pasada (`PASSED`) |
| `C-039` | `200` | `false` | Pasada (`PASSED`) |
| `C-040` | `200` | `false` | Pasada (`PASSED`) |

---

## 5. Cobertura de los 14 escenarios sintéticos (`SYN-*`)

| Escenario | Resultado esperado y verificado | Estado prueba |
|---|---|---|
| `SYN-E102` | `HTTP 200`, `puede_reprocesar: false` (`E-102`) | Pasada (`PASSED`) |
| `SYN-E512-0` | `HTTP 200`, `puede_reprocesar: true` (`0` reprocesos) | Pasada (`PASSED`) |
| `SYN-E512-1` | `HTTP 200`, `puede_reprocesar: false` (`1` reproceso) | Pasada (`PASSED`) |
| `SYN-E207-OK` | `HTTP 200`, `puede_reprocesar: true` (`SRV-MOD` operativo, `U-S1`/`U-S2`) | Pasada (`PASSED`) |
| `SYN-DET-OK` | `HTTP 200`, `puede_reprocesar: true` (`detenido`) | Pasada (`PASSED`) |
| `SYN-LIMIT-2` | `HTTP 200`, `puede_reprocesar: true` (`2` reprocesos en `E-305`/`E-207`) | Pasada (`PASSED`) |
| `SYN-LIMIT-3` | `HTTP 200`, `puede_reprocesar: false` (`3` reprocesos, escalar S3) | Pasada (`PASSED`) |
| `SYN-DECFIN` | `HTTP 200`, `puede_reprocesar: false` (`tiene_decision_final=sí` en `error`) | Pasada (`PASSED`) |
| `SYN-ROL-COM` | `HTTP 403` error estándar para `U-S4` (`comercial`) | Pasada (`PASSED`) |
| `SYN-ROL-N2-ING` | `HTTP 200`, `puede_reprocesar: true` para `U-S2` y `U-S3` | Pasada (`PASSED`) |
| `SYN-NO-USER` | `HTTP 403` error estándar para `U-999` | Pasada (`PASSED`) |
| `SYN-NO-CASE` | `HTTP 404` error estándar para `C-999` con `U-S1` | Pasada (`PASSED`) |
| `SYN-422` | `HTTP 422` error de validación para 10 variantes de entrada inválida | Pasada (`PASSED`) |
| `SYN-INJ-OK` | `HTTP 200`, `puede_reprocesar: true` ignorando `registro_tecnico` malicioso | Pasada (`PASSED`) |
