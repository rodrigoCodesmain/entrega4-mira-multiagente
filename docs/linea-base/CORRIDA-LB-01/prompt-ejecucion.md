# Experimento CORRIDA-LB-01 — Línea base de agente único

Trabaja exclusivamente en el workspace:

`/home/lester/Documents/mira-cu2-linea-base-aislada`

Estás realizando un experimento académico para evaluar si **un único agente de IA** puede desarrollar un prototipo a partir de una especificación de requisitos previamente aprobada.

## Objetivo

Diseñar, implementar y verificar por ti mismo una API de elegibilidad de reprocesamiento de casos para MIRA CU-2.

**Debes realizar todas las actividades directamente, sin delegar en subagentes.**

### Fuentes autorizadas

- `specs/01-requisitos.md`: especificación aprobada por un representante humano del cliente.
- `kit/CU-2_soporte_operacion/`: documentación normativa y datos oficiales.
- `docs/kit-sha256sums.txt`: comprobación de integridad.
- `.agents/skills/`: skills reutilizables disponibles para apoyar especificación, trazabilidad y ejecución de pruebas.

La especificación aprobada tiene prioridad para definir el alcance y los criterios de aceptación. Utiliza exclusivamente las versiones normativas vigentes señaladas allí.

## Actividades

1. Analiza los requisitos y los documentos normativos relevantes.
2. Define internamente un plan técnico sencillo para cumplir la especificación.
3. Implementa una solución mínima en Python con FastAPI y pytest, sin frontend ni infraestructura innecesaria.
4. Implementa las reglas de elegibilidad de forma determinista, utilizando los datos del Excel oficial en modo de solo lectura.
5. Implementa los contratos HTTP, controles de roles simulados, límites de reprocesamiento y demás comportamientos establecidos por los requisitos aprobados.
6. Crea pruebas automatizadas que cubran los diez casos reales del Excel, los catorce escenarios sintéticos y las condiciones de seguridad relevantes.
7. Ejecuta las pruebas y verifica la integridad del kit.
8. Corrige, si corresponde, los defectos que detectes durante tu propia ejecución, registrando las correcciones reales.
9. Prepara instrucciones breves para instalar dependencias, ejecutar las pruebas y levantar la API.

## Restricción experimental fundamental

Este experimento corresponde a **un solo agente**.

- No utilices `invoke_subagent`.
- No crees ni invoques agentes especializados.
- No utilices flujos de Implementador/Revisor, delegaciones ni revisiones realizadas por otro agente.
- No consultes ningún directorio fuera de este workspace.
- No busques otras soluciones del proyecto en GitHub, carpetas hermanas, conversaciones anteriores ni archivos externos.
- No leas implementaciones, pruebas, logs, dictámenes ni resultados de una corrida multiagente.
- Puedes utilizar directamente las skills y scripts presentes en este workspace.
- No modifiques el kit original.
- No inventes resultados ni afirmes haber ejecutado pruebas que no ejecutaste.

## Evidencias y métricas

Crea `docs/linea-base/CORRIDA-LB-01/` y registra allí:

1. `prompt-ejecucion.md`: copia fiel de este prompt, sin modificar su contenido.
2. `resultado.md`: identificación de la modalidad de agente único, modelo y configuración disponibles, tareas realizadas, archivos creados, decisiones técnicas, correcciones internas, intervenciones humanas y limitaciones.
3. `pytest.log`: salida real de las pruebas, con comando, conteo exacto y código de salida.
4. `metricas.md`: resultados verificables para `REQ-01..REQ-18`, `CA-01..CA-10`, casos del Excel, escenarios sintéticos, pruebas pasadas/fallidas/omitidas y número de correcciones realizadas.

Registra la hora de inicio y término si está disponible mediante herramientas confiables. No inventes duración, consumo de tokens ni costos.

Si alguna métrica no está disponible, escribe `No disponible`.

## Criterios de cierre

Al terminar:

- Verifica los resultados de pytest.
- Verifica los checksums del kit.
- Explica cualquier requisito o criterio no cumplido.
- Presenta un resumen de la solución, pruebas, correcciones y métricas.

No realices commits ni pushes.

Detente tras completar el experimento. No efectúes comparaciones con otras modalidades de agentes, porque sus resultados no forman parte de tus fuentes autorizadas.
