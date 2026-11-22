# Instrucciones del repositorio MIRA · Entregable 4

- La alternativa A usa un flujo conducido por especificación. El plan de coordinación propone evaluar la autorización de reprocesamiento para CU-2 Soporte y operación. Las reglas funcionales se contrastan con MAN-INC, CAT-ERR y CU-2_datos.xlsx, y cualquier supuesto se somete al representante del cliente.
- Los cuatro roles del flujo son Requisitos, Planificador, Implementador y Revisor QA. El siguiente rol lee el archivo del traspaso en `docs/trabajo/`. La persona operadora guarda el dictamen del Revisor QA, que trabaja con permisos de lectura.
- Antes de escribir código, deja constancia de la aprobación humana de la versión exacta de la especificación en un commit propio. Registra también el control humano del plan antes de pasarlo al Implementador. Se permiten hasta dos correcciones entre Implementador y Revisor QA.
- Registra únicamente eventos observados y archivos recibidos en `docs/bitacora.md`. Usa `docs/evidencia/` para la corrida multiagente y `docs/linea-base/` para la comparación con un único agente. Conserva el hash del commit y el identificador de la corrida en cada registro.
- Usa datos de prueba adecuados para compartir con el equipo. Revisa capturas y logs antes de versionarlos para retirar secretos y datos personales.
