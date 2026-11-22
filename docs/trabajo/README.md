# Registro de traspasos

La tabla indica los archivos previstos y el estado de recepción. Conservar aquí los archivos de la corrida multiagente para que el destinatario pueda leer la versión citada. Las rutas de la tabla son relativas a esta carpeta.

| ID | Emisor → receptor | Archivo previsto | Condición de avance | Estado |
| --- | --- | --- | --- | --- |
| T01 | Requisitos → Representante del cliente | `spec.md` y aclaraciones en `aclaraciones.md`. | El representante revisa los criterios, las fuentes y los supuestos. | Pendiente. |
| T02 | Representante del cliente → Planificador | `spec.md` y `aprobacion-spec.md`. | La aprobación cita la versión exacta y tiene un commit humano propio. | Pendiente. |
| T03 | Planificador → Persona responsable del control del plan | `plan.md` y `tasks.md`. | La persona revisa el alcance y la trazabilidad entre criterios, tareas y pruebas. | Pendiente. |
| T04 | Persona responsable del control del plan → Implementador | `plan.md`, `tasks.md` y `revision-plan.md`. | El control humano queda registrado antes de implementar. | Pendiente. |
| T05 | Implementador → Revisor QA | `implementacion.md`, commit de cambios y evidencia de pruebas en [`../evidencia/`](../evidencia/). | QA verifica el commit revisado y contrasta el resultado con la especificación. | Pendiente. |
| T06 | Revisor QA → Implementador o cierre | `revision.md`, conservado por la persona operadora, con el veredicto y los hallazgos. | Con observaciones, devolver al Implementador hasta dos veces. Con aprobación, vincular el dictamen y el resultado de pruebas al cierre. | Pendiente. |

Para cada traspaso recibido, conservar la salida original e identificar corrida, fecha y hora, emisor, receptor, revisión o hash, entradas, salidas, criterios cubiertos, pendientes y siguiente paso. El receptor registra cuándo leyó la salida y deja su decisión en la [bitácora](../bitacora.md). Si hay una corrección, identificar la ronda en el archivo o en el commit y conservar la referencia a la versión anterior.
