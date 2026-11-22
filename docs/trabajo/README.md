# Registro de traspasos y dictámenes (`docs/trabajo/`)

Esta carpeta almacena la bitácora de coordinación secuencial entre los cuatro agentes (`requisitos`, `planificador`, `implementador`, `revisor`) y los dictámenes registrados por una persona.

## Convención de nombres

- Traspaso entre agentes: `NNN-<origen>-a-<destino>.md` (ej. `001-requisitos-a-planificador.md`).
- Prueba inicial de traspaso: `000-prueba-traspaso.md`.
- Dictamen del revisor registrado por una persona: `NNN-dictamen-revisor-iterN.md` (donde `N` es `0`, `1` o `2`).

## Campos mínimos de cada acta de traspaso

```markdown
# Traspaso NNN: <origen> -> <destino>

- **Fecha:** YYYY-MM-DD HH:MM
- **Fase:** <preparacion | requisitos | planificacion | implementacion | revision>
- **Agente origen:** <nombre>
- **Agente destino:** <nombre>
- **Iteración de corrección:** <0/2 | 1/2 | 2/2>
- **Control humano requerido:** <ninguno | Control Humano 1 (especificacion) | Control Humano 2 (plan) | registro humano de dictamen>
- **Artefactos de entrada:**
  - `<ruta>`
- **Artefactos producidos/actualizados:**
  - `<ruta>`
- **Verificaciones ejecutadas:** <comando y resultado resumido>
- **Resumen y puntos abiertos:** <detalle breve>
```

## Regla para dictámenes del `revisor`

El agente `revisor` **no escribe archivos** en el repositorio. Entrega su dictamen completo directamente en la conversación; una persona lo copia íntegramente en `docs/trabajo/NNN-dictamen-revisor-iterN.md` antes de iniciar una ronda de corrección con `implementador` (máximo 2 correcciones) o cerrar la entrega.
