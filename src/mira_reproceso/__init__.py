"""Paquete mínimo de evaluación de elegibilidad de reprocesamiento MIRA CU-2."""

from mira_reproceso.api import EvaluarRequest, EvaluarResponse, app, create_app, get_datos
from mira_reproceso.loader import cargar_datos_excel
from mira_reproceso.models import (
    Caso,
    CasoNoEncontradoError,
    DatosOperativos,
    ReglaCodigoError,
    ResultadoEvaluacion,
    Servicio,
    Usuario,
    UsuarioNoAutorizadoError,
)
from mira_reproceso.rules import (
    CATALOGO_CAT_ERR_V2,
    ESTADOS_ELEGIBLES,
    LIMITE_E512,
    LIMITE_GENERAL_REPROCESOS,
    REGLAS_CAT_ERR_V2,
    ROLES_AUTORIZADOS,
    evaluar_elegibilidad,
    obtener_caso,
    validar_usuario_autorizado,
)

__version__ = "0.1.0"

__all__ = [
    "CATALOGO_CAT_ERR_V2",
    "Caso",
    "CasoNoEncontradoError",
    "DatosOperativos",
    "ESTADOS_ELEGIBLES",
    "EvaluarRequest",
    "EvaluarResponse",
    "LIMITE_E512",
    "LIMITE_GENERAL_REPROCESOS",
    "REGLAS_CAT_ERR_V2",
    "ROLES_AUTORIZADOS",
    "ReglaCodigoError",
    "ResultadoEvaluacion",
    "Servicio",
    "Usuario",
    "UsuarioNoAutorizadoError",
    "__version__",
    "app",
    "cargar_datos_excel",
    "create_app",
    "evaluar_elegibilidad",
    "get_datos",
    "obtener_caso",
    "validar_usuario_autorizado",
]
