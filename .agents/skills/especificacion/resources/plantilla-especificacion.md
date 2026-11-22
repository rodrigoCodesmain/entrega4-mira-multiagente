# Especificación de Requisitos · MIRA CU-2 (Elegibilidad de reprocesamiento)

- **Estado:** Borrador pendiente de Control Humano 1
- **Fuentes normativas vigentes:** `MAN-INC` v2, `CAT-ERR` v2
- **Fuentes excluidas:** `CAT-ERR` v1 (derogado)

## 1. Alcance y exclusiones
- Qué hace el sistema (evaluación de elegibilidad).
- Qué queda fuera explícitamente.

## 2. Contrato mínimo de la API
- Entrada: `caso_id`, `usuario_id`.
- Salida: `puede_reprocesar`, `motivos`, `accion_recomendada`, `referencias_normativas`.

## 3. Reglas de negocio verificables (`REQ-*`)
| ID Requisito | Regla / Condición | Fuente normativa | Criterio de aceptación |
|---|---|---|---|
| `REQ-01` | ... | `MAN-INC v2 §4` | ... |

## 4. Casos borde y datos de prueba
- Registros cubiertos por `CU-2_datos.xlsx` (intacto).
- Casos sintéticos en memoria requeridos para completar cobertura.

## 5. Aclaraciones pendientes de aprobación humana
- Interpretación del conteo y límite de 1 reproceso para `E-512`.
- Otros supuestos explícitos (ej. manejo de IDs inexistentes).

## 6. Seguridad de datos
- Tratamiento pasivo de `registro_tecnico` (mitigación frente a `L-009` en `C-038`).
