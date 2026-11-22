# MIRA · Entregable 4

**Taller de Desarrollo de Software Conducido por Agentes de IA · Universidad de Valparaíso**

La entrega aplica la **alternativa A, desarrollo de software conducido por especificación (SDD)**, a **MIRA CU-2 · Soporte y operación**. El objetivo académico es demostrar con evidencia cómo cuatro agentes llevan una necesidad del cliente desde la especificación hasta una implementación verificada, con controles humanos y una comparación frente a un solo agente.

## Caso y alcance

La necesidad que inicia el flujo es determinar si corresponde **autorizar el reprocesamiento de un caso**. La funcionalidad evaluará los datos del caso y devolverá una decisión verificable (`permitido` o `no permitido`), el motivo y la acción sugerida. La operación termina con esa respuesta.

El enunciado definitivo, las reglas y sus excepciones se fijarán con **MAN-INC**, **CAT-ERR**, **`CU-2_datos.xlsx`** y las aclaraciones del representante del cliente. El plan propone **Python**, una **API local mínima** y **pytest**. Las pruebas previstas cubrirán errores reprocesables y no reprocesables, disponibilidad de servicios, límite de intentos, estados y datos incompatibles, formato de la respuesta e identificadores inexistentes. Los resultados esperados se fijarán en la especificación.

## Flujo multiagente

| Rol | Trabajo y salida principal |
| --- | --- |
| Requisitos | Redacta la historia de usuario, los criterios de aceptación en formato Dado/Cuando/Entonces y el caso de uso en `spec.md`. Lleva las aclaraciones al representante del cliente. |
| Planificador | Lee la especificación aprobada y produce `plan.md` y `tasks.md` con el diseño, las tareas y las pruebas previstas por criterio. |
| Implementador | Lee el plan revisado, implementa la API y las pruebas, y entrega `implementacion.md` con las referencias a sus cambios y la ejecución de la suite. |
| Revisor QA | Contrasta la especificación, los cambios y las pruebas con permisos de lectura. La persona operadora conserva su dictamen en `revision.md`. |

La coordinación es secuencial. **Antes de escribir código, una persona debe aprobar la versión exacta de `spec.md` en un commit propio.** Un segundo control humano revisa el plan antes de pasar al Implementador. Si QA solicita cambios, se permiten hasta **dos correcciones**. Cada destinatario lee el archivo que recibe en [`docs/trabajo/`](docs/trabajo/README.md).

El plan propone **Antigravity con Orchestrator Neon**, sujeto a verificar la configuración, las versiones, los modelos y los permisos. Las tres skills previstas son `crear-especificacion`, `validar-trazabilidad` y `ejecutar-pruebas`. Esta última contempla un script para ejecutar `pytest` y conservar su salida y código de retorno. El [documento de decisiones](docs/decision.md) explica el patrón y los permisos previstos.

## Organización del repositorio

| Ruta | Qué contiene hoy y qué se guarda allí |
| --- | --- |
| [`AGENTS.md`](AGENTS.md) | Instrucciones del proyecto para los agentes, incluidos los controles humanos y el manejo de evidencias. |
| [`.github/agents/`](.github/agents/) | Carpeta reservada para las cuatro definiciones `.agent.md`. Contiene `.gitkeep`. La ubicación efectiva se documentará si la herramienta usa otra ruta. |
| [`.github/skills/`](.github/skills/) | Carpeta reservada para las tres skills, cada una con su `SKILL.md` y sus recursos. Contiene `.gitkeep`. |
| [`docs/decision.md`](docs/decision.md) | Alcance, patrón, roles, herramientas previstas y control de commits y etiqueta. |
| [`docs/bitacora.md`](docs/bitacora.md) | Preparación del repositorio e inventario de entregas pendientes. Aquí se registrarán las salidas recibidas, decisiones y resultados comprobados. |
| [`docs/trabajo/`](docs/trabajo/README.md) | Índice de los seis traspasos previstos. Recibirá la especificación, las aclaraciones, las aprobaciones, el plan, las tareas y los dictámenes. |
| [`docs/evidencia/`](docs/evidencia/README.md) | Guía de archivo para los prompts, capturas, logs, pruebas y resultados de la corrida multiagente. |
| [`docs/linea-base/`](docs/linea-base/README.md) | Protocolo para la corrida de comparación con un solo agente y lugar de archivo de sus resultados. |
| [`src/`](src/) y [`tests/`](tests/) | Carpetas reservadas para la implementación y las pruebas automatizadas. Ambas contienen `.gitkeep`. |

## Evidencia y comparación

La corrida multiagente debe recorrer el caso desde la necesidad inicial hasta el dictamen de QA y las pruebas en verde. La línea base parte del **mismo commit inicial**, con la misma necesidad y datos y criterios comparables. Se compararán criterios cumplidos, pruebas aprobadas y fallidas, tiempo, interacciones, correcciones y trazabilidad. Los tokens o el costo se registrarán cuando la herramienta los informe.

Cada ejecución se enlaza desde la [bitácora](docs/bitacora.md) con su identificador y commit. La bitácora registra el uso de las tres skills y el resultado de ejecutar el script de pruebas. Para documentar una corrección o un rechazo humano, se conserva la salida revisada, la decisión y su evidencia. Para el análisis MAST se registran las fallas observadas, su causa, el cambio aplicado y el resultado de la reejecución.

## Demostración y entrega

El repositorio está en **preparación documental**. La demostración y los comandos de ejecución quedan pendientes de incorporar hasta contar con el caso de entrada confirmado, los agentes y las skills configurados, la API y sus pruebas. La [bitácora](docs/bitacora.md) contiene el estado de recepción.

Para la versión final, este README debe indicar los prerrequisitos, cómo cargar los agentes, cómo lanzar el flujo con la entrada original, dónde aplicar los controles humanos y qué comandos ejecutar para invocar la API y correr las pruebas. La pauta pide que el docente pueda **lanzar el flujo en menos de 15 minutos** desde la etiqueta de entrega. La demostración se realiza en vivo dentro de la presentación de 15 minutos.

- **Repositorio.** Debe incluir agentes, skills, artefactos y evidencia, con acceso para el docente. La pauta indica la etiqueta `entrega-3`. Su nombre y publicación se controlan en [decisiones](docs/decision.md#control-de-commits-y-etiqueta).
- **Informe PDF y presentación PPT.** El informe debe declarar la alternativa, la herramienta y su versión, los modelos usados, los integrantes y el representante del cliente. El representante debe ser distinto de quien ejerció ese rol en la Entrega 2.
- **Plazo.** La sección 10 de la pauta indica el **23 de noviembre de 2026 a las 14:00** por Aula Académica. La portada señala el **30 de noviembre de 2026**. Queda pendiente confirmar la fecha en Aula Académica.

