---
name: trazabilidad
description: >-
  Gestiona la matriz de trazabilidad normativa (regla CU-2 a requisito, componente y prueba), el registro de traspasos en docs/trabajo/ y la validación de integridad mediante script ejecutable. Activar al crear o auditar specs/03-trazabilidad.md o actas en docs/trabajo/.
---

# Skill: Trazabilidad y Registro de Traspasos

Mantiene trazabilidad bidireccional desde las reglas vigentes de `MAN-INC` v2 y `CAT-ERR` v2 hasta los requisitos, módulos, pruebas y traspasos entre agentes.

## 1. Matriz de trazabilidad (`specs/03-trazabilidad.md`)

Toda fila de la matriz debe usar estas columnas exactas:

| ID Regla | Documento Vigente y Sección | ID Requisito | Componente / Función | Caso de Prueba | Estado |
|---|---|---|---|---|---|

Reglas obligatorias:
- Nunca citar `CAT-ERR v1` o `CAT-ERR_v1_derogado.md` como fuente normativa activa.
- Toda regla de `REQ-*` debe mapear al menos a un componente en `src/` y al menos a un caso en `tests/`.

## 2. Registro de traspasos en `docs/trabajo/`

- Todo traspaso entre agentes debe crear o actualizar un archivo `docs/trabajo/NNN-<origen>-a-<destino>.md` según `docs/trabajo/README.md`.
- Indicar siempre la iteración de corrección (`0/2`, `1/2`, `2/2`) y el estado de la compuerta humana aplicable.
- Los dictámenes del `revisor` se emiten en conversación y son registrados por una persona en `docs/trabajo/`.

## 3. Verificación automática (solo lectura)

Ejecutar el script verificador incluido en esta skill:

```bash
python3 .agents/skills/trazabilidad/scripts/verificar_trazabilidad.py --check-kit
```

Cuando exista `specs/03-trazabilidad.md`, validar además la matriz:

```bash
python3 .agents/skills/trazabilidad/scripts/verificar_trazabilidad.py --check-kit --matrix specs/03-trazabilidad.md
```
