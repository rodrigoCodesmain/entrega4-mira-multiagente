---
name: ejecucion-pruebas
description: >-
  Ejecuta las pruebas automatizadas con pytest y verifica la integridad de solo lectura del kit CU-2 mediante un script reproducible sin generar cachés en el repositorio. Activar antes de cerrar implementación o durante la auditoría del revisor.
---

# Skill: Ejecución de Pruebas (`ejecucion-pruebas`)

Estandariza la ejecución segura y reproducible de pruebas para MIRA CU-2 sin modificar el Excel del kit ni ensuciar el repositorio con archivos temporales o cachés.

## 1. Uso del script ejecutable

- **Modo verificación de entorno e integridad (fase de preparación o diagnóstico):**

```bash
./.agents/skills/ejecucion-pruebas/scripts/run_tests.sh --check-only
```

- **Modo ejecución de suite `pytest` (fases de implementación y revisión):**

```bash
./.agents/skills/ejecucion-pruebas/scripts/run_tests.sh
```

## 2. Garantías del script

1. Valida `docs/kit-sha256sums.txt` antes de correr pruebas para asegurar que `kit/CU-2_soporte_operacion/` no fue alterado.
2. Ejecuta `pytest` con `PYTHONDONTWRITEBYTECODE=1` y `-p no:cacheprovider`, por lo que es seguro incluso para el agente `revisor` de solo lectura.
3. No instala dependencias ni ejecuta comandos Git.

## 3. Evidencia mínima requerida

En el acta de traspaso o dictamen del `revisor`, incluir siempre:
- Comando exacto ejecutado.
- Resultado de verificación de checksums del kit.
- Conteo exacto de pruebas pasadas, fallidas o saltadas reportado por `pytest`.
