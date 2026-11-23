"""Motor determinista puro de reglas vigentes (MAN-INC v2 y CAT-ERR v2) para MIRA CU-2."""

from __future__ import annotations

from mira_reproceso.models import (
    Caso,
    CasoNoEncontradoError,
    DatosOperativos,
    ReglaCodigoError,
    ResultadoEvaluacion,
    Usuario,
    UsuarioNoAutorizadoError,
)

ROLES_AUTORIZADOS: frozenset[str] = frozenset({"soporte_n1", "soporte_n2", "ingenieria"})
ESTADOS_ELEGIBLES: frozenset[str] = frozenset({"error", "detenido"})
LIMITE_GENERAL_REPROCESOS: int = 3
LIMITE_E512: int = 1
SERVICIO_MODELOS_ID: str = "SRV-MOD"

# Conjunto exclusivo para validar pertenencia de un código en CAT-ERR v2 vigente.
CATALOGO_CAT_ERR_V2: frozenset[str] = frozenset(
    {
        "E-101",
        "E-102",
        "E-207",
        "E-208",
        "E-305",
        "E-311",
        "E-410",
        "E-512",
    }
)

# Estructura independiente por código con la semántica y acción vigente de CAT-ERR v2.
REGLAS_CAT_ERR_V2: dict[str, ReglaCodigoError] = {
    "E-101": ReglaCodigoError(
        codigo="E-101",
        descripcion="Evidencia ilegible",
        reprocesable=False,
        condicion="No reprocesable",
        motivo_bloqueo=(
            "El código E-101 (evidencia ilegible) no es reprocesable según CAT-ERR v2; "
            "el reproceso produciría el mismo resultado."
        ),
        accion_recomendada="Solicitar el reenvío de la evidencia; no reprocesar.",
        referencia="CAT-ERR v2 §1 (E-101)",
    ),
    "E-102": ReglaCodigoError(
        codigo="E-102",
        descripcion="Formato de archivo no soportado",
        reprocesable=False,
        condicion="No reprocesable",
        motivo_bloqueo=(
            "El código E-102 (formato de archivo no soportado) no es reprocesable según CAT-ERR v2."
        ),
        accion_recomendada="Informar a la organización los formatos aceptados; no reprocesar.",
        referencia="CAT-ERR v2 §1 (E-102)",
    ),
    "E-207": ReglaCodigoError(
        codigo="E-207",
        descripcion="Tiempo de espera agotado con el proveedor de modelos",
        reprocesable=True,
        condicion="SRV-MOD operativo y servicio dependiente operativo",
        motivo_bloqueo=None,
        accion_recomendada="Proceder con el reprocesamiento.",
        referencia="CAT-ERR v2 §1 (E-207)",
    ),
    "E-208": ReglaCodigoError(
        codigo="E-208",
        descripcion="Cuota del proveedor de modelos agotada",
        reprocesable=False,
        condicion="No reprocesable",
        motivo_bloqueo=(
            "El código E-208 (cuota del proveedor de modelos agotada) no es reprocesable "
            "según CAT-ERR v2."
        ),
        accion_recomendada="Registrar incidente S2 y escalar a Ingeniería; no reprocesar.",
        referencia="CAT-ERR v2 §1 (E-208)",
    ),
    "E-305": ReglaCodigoError(
        codigo="E-305",
        descripcion="Módulo de análisis no disponible",
        reprocesable=True,
        condicion="Servicio dependiente del módulo operativo",
        motivo_bloqueo=None,
        accion_recomendada="Proceder con el reprocesamiento.",
        referencia="CAT-ERR v2 §1 (E-305)",
    ),
    "E-311": ReglaCodigoError(
        codigo="E-311",
        descripcion="Versión de módulo fijada no disponible",
        reprocesable=False,
        condicion="No reprocesable",
        motivo_bloqueo=(
            "El código E-311 (versión de módulo fijada no disponible) no es reprocesable "
            "según CAT-ERR v2; prohibido reprocesar con otra versión sin autorización de la organización."
        ),
        accion_recomendada=(
            "Escalar a Ingeniería; no reprocesar con otra versión sin autorización de la organización."
        ),
        referencia="CAT-ERR v2 §1 (E-311)",
    ),
    "E-410": ReglaCodigoError(
        codigo="E-410",
        descripcion="Límite de llamadas por minuto superado",
        reprocesable=False,
        condicion="No aplica para reproceso manual",
        motivo_bloqueo=(
            "El código E-410 (límite de llamadas por minuto superado) no aplica para reprocesamiento "
            "manual según CAT-ERR v2: la llamada se encola y procesa cuando hay capacidad."
        ),
        accion_recomendada=(
            "No reprocesar; el caso se encola y se procesa cuando hay capacidad "
            "(sin acción de soporte salvo cola > 6 horas)."
        ),
        referencia="CAT-ERR v2 §1 (E-410)",
    ),
    "E-512": ReglaCodigoError(
        codigo="E-512",
        descripcion="Error interno de la plataforma",
        reprocesable=True,
        condicion="Máximo específico de 1 reproceso bajo contador global por caso",
        motivo_bloqueo=None,
        accion_recomendada="Reprocesar una vez; si vuelve a fallar, escalar a Ingeniería.",
        referencia="CAT-ERR v2 §1 (E-512)",
    ),
}


def _agregar_referencia(referencias: list[str], referencia: str) -> None:
    if referencia not in referencias:
        referencias.append(referencia)


def validar_usuario_autorizado(datos: DatosOperativos, usuario_id: str) -> Usuario:
    """Valida de forma simulada si el usuario existe y posee un rol autorizado.

    Se ejecuta estrictamente antes de consultar `datos.casos` para impedir
    cualquier revelación de existencia o diagnóstico de un caso ante rol no autorizado.
    """
    uid = usuario_id.strip()
    usuario = datos.usuarios.get(uid)
    if usuario is None or usuario.rol.strip().lower() not in ROLES_AUTORIZADOS:
        raise UsuarioNoAutorizadoError("Usuario no autorizado para evaluar reprocesamiento.")
    return usuario


def obtener_caso(datos: DatosOperativos, caso_id: str) -> Caso:
    """Obtiene un caso existente en `datos.casos` o lanza `CasoNoEncontradoError`."""
    cid = caso_id.strip()
    caso = datos.casos.get(cid)
    if caso is None:
        raise CasoNoEncontradoError("Caso no encontrado.")
    return caso


def _seleccionar_accion_bloqueo(
    *,
    tiene_bloqueo_decision_final: bool,
    tiene_inconsistencia_ex05: bool,
    codigo_no_reprocesable: str | None,
    limite_alcanzado_e512: bool,
    limite_alcanzado_general: bool,
    servicio_no_operativo_e207: bool,
    servicio_no_operativo_otro: bool,
    servicio_no_operativo_e207_otro_id: str | None = None,
) -> str:
    if tiene_bloqueo_decision_final:
        return "No reprocesar; el caso ya cuenta con decisión final irreversible."
    if tiene_inconsistencia_ex05:
        return "No reprocesar; escalar a Ingeniería por inconsistencia de código o servicio."
    if codigo_no_reprocesable is not None:
        return REGLAS_CAT_ERR_V2[codigo_no_reprocesable].accion_recomendada
    if limite_alcanzado_e512:
        return (
            "No reprocesar; límite específico de 1 reproceso alcanzado para E-512, "
            "escalar a Ingeniería."
        )
    if limite_alcanzado_general:
        return (
            "No reprocesar; límite máximo de 3 reprocesos alcanzado, "
            "escalar a Ingeniería como incidente S3."
        )
    if servicio_no_operativo_e207:
        return (
            "No reprocesar; el caso permanece en cola y se reintenta automáticamente "
            "cuando SRV-MOD esté operativo."
        )
    if servicio_no_operativo_otro:
        if servicio_no_operativo_e207_otro_id is not None:
            return (
                f"No reprocesar; esperar a que el servicio dependiente "
                f"'{servicio_no_operativo_e207_otro_id}' vuelva a estar operativo."
            )
        return "No reprocesar; esperar a que el servicio dependiente vuelva a estar operativo."
    return "No reprocesar; el caso no se encuentra en estado 'error' o 'detenido'."


def evaluar_elegibilidad(
    datos: DatosOperativos,
    caso_id: str,
    usuario_id: str,
) -> ResultadoEvaluacion:
    """Evalúa de forma determinista y sin efectos laterales la elegibilidad de reprocesamiento."""
    # Paso 1: validación simulada prioritaria de autorización por rol (sin leer `datos.casos`).
    validar_usuario_autorizado(datos, usuario_id)

    # Paso 2: verificación de existencia del caso tras autorizar el rol.
    caso = obtener_caso(datos, caso_id)

    # Paso 3: evaluación normativa completa acumulando todos los impedimentos concurrentes.
    estado = caso.estado.strip().lower()
    codigo_error = caso.codigo_error.strip()
    servicio_dep_id = caso.servicio_dependiente.strip()
    reprocesos = caso.reprocesos_realizados

    motivos: list[str] = []
    referencias: list[str] = []

    tiene_bloqueo_decision_final = False
    tiene_inconsistencia_ex05 = False
    codigo_no_reprocesable: str | None = None
    limite_alcanzado_e512 = False
    limite_alcanzado_general = False
    servicio_no_operativo_e207 = False
    servicio_no_operativo_otro = False
    servicio_no_operativo_e207_otro_id: str | None = None

    # 3.1 Estado elegible del caso (MAN-INC v2 §4).
    if estado not in ESTADOS_ELEGIBLES:
        motivos.append(
            f"El caso '{caso.caso_id}' está en estado '{estado}'; "
            "solo se reprocesan casos en estado 'error' o 'detenido'."
        )
        _agregar_referencia(referencias, "MAN-INC v2 §4")

    # 3.2 Decisión final irreversible (MAN-INC v2 §4).
    if caso.tiene_decision_final:
        tiene_bloqueo_decision_final = True
        motivos.append(
            f"El caso '{caso.caso_id}' ya cuenta con decisión final irreversible "
            "(tiene_decision_final=sí); nunca se reprocesa."
        )
        _agregar_referencia(referencias, "MAN-INC v2 §4")

    # 3.3 Pertenencia y clasificación en CAT-ERR v2 vigente.
    codigo_en_catalogo = codigo_error in CATALOGO_CAT_ERR_V2
    if not codigo_en_catalogo:
        tiene_inconsistencia_ex05 = True
        motivos.append(
            f"El código de error '{codigo_error}' no pertenece al catálogo vigente CAT-ERR v2 "
            "(inconsistencia de datos)."
        )
        _agregar_referencia(referencias, "MAN-INC v2 §4")
        _agregar_referencia(referencias, "CAT-ERR v2 §1")
    else:
        regla_codigo = REGLAS_CAT_ERR_V2[codigo_error]
        if not regla_codigo.reprocesable:
            codigo_no_reprocesable = codigo_error
            assert regla_codigo.motivo_bloqueo is not None
            motivos.append(regla_codigo.motivo_bloqueo)
            _agregar_referencia(referencias, regla_codigo.referencia)

    # 3.4 Estado operativo de servicio_dependiente y de SRV-MOD para E-207.
    servicio_dep = datos.servicios.get(servicio_dep_id)
    if servicio_dep is None:
        tiene_inconsistencia_ex05 = True
        motivos.append(
            f"El servicio dependiente '{servicio_dep_id}' no existe en el registro de servicios "
            "(inconsistencia de datos)."
        )
        _agregar_referencia(referencias, "MAN-INC v2 §4")
    else:
        estado_srv_dep = servicio_dep.estado.strip().lower()
        if estado_srv_dep != "operativo":
            if codigo_error == "E-207" and servicio_dep.servicio_id == SERVICIO_MODELOS_ID:
                servicio_no_operativo_e207 = True
                motivos.append(
                    f"El servicio dependiente '{SERVICIO_MODELOS_ID}' (requerido por E-207) "
                    f"se encuentra en estado '{estado_srv_dep}' (se requiere estado 'operativo')."
                )
                _agregar_referencia(referencias, "MAN-INC v2 §4")
                _agregar_referencia(referencias, "GUI-COL v1 §1")
                _agregar_referencia(referencias, "CAT-ERR v2 §1 (E-207)")
            else:
                servicio_no_operativo_otro = True
                if codigo_error == "E-207":
                    servicio_no_operativo_e207_otro_id = servicio_dep.servicio_id
                motivos.append(
                    f"El servicio dependiente '{servicio_dep.servicio_id}' se encuentra en "
                    f"estado '{estado_srv_dep}' (se requiere estado 'operativo')."
                )
                _agregar_referencia(referencias, "MAN-INC v2 §4")
                _agregar_referencia(referencias, "GUI-COL v1 §1")
                if codigo_en_catalogo and REGLAS_CAT_ERR_V2[codigo_error].reprocesable:
                    _agregar_referencia(referencias, REGLAS_CAT_ERR_V2[codigo_error].referencia)

    if codigo_error == "E-207" and servicio_dep_id != SERVICIO_MODELOS_ID:
        srv_mod = datos.servicios.get(SERVICIO_MODELOS_ID)
        if srv_mod is None:
            tiene_inconsistencia_ex05 = True
            motivos.append(
                f"El código E-207 requiere verificar '{SERVICIO_MODELOS_ID}', pero dicho servicio "
                "no existe en el registro de servicios (inconsistencia de datos)."
            )
            _agregar_referencia(referencias, "CAT-ERR v2 §1 (E-207)")
            _agregar_referencia(referencias, "MAN-INC v2 §4")
        else:
            estado_srv_mod = srv_mod.estado.strip().lower()
            if estado_srv_mod != "operativo":
                servicio_no_operativo_e207 = True
                motivos.append(
                    f"El código E-207 exige que '{SERVICIO_MODELOS_ID}' esté 'operativo', "
                    f"pero su estado actual es '{estado_srv_mod}'."
                )
                _agregar_referencia(referencias, "CAT-ERR v2 §1 (E-207)")
                _agregar_referencia(referencias, "MAN-INC v2 §4")
                _agregar_referencia(referencias, "GUI-COL v1 §1")

    # 3.5 Límites de reprocesamiento (E-512: máximo 1 global; general: máximo 3).
    if reprocesos < 0:
        tiene_inconsistencia_ex05 = True
        motivos.append(
            f"El contador reprocesos_realizados={reprocesos} es negativo (inconsistencia de datos)."
        )
        _agregar_referencia(referencias, "MAN-INC v2 §4")
    elif codigo_error == "E-512":
        if reprocesos >= LIMITE_E512:
            limite_alcanzado_e512 = True
            motivos.append(
                f"El código E-512 admite un máximo específico de {LIMITE_E512} reproceso "
                f"(contador global por caso: reprocesos_realizados={reprocesos})."
            )
            _agregar_referencia(referencias, "CAT-ERR v2 §1 (E-512)")
            if reprocesos >= LIMITE_GENERAL_REPROCESOS:
                motivos.append(
                    f"Además, el caso alcanzó el máximo general de {LIMITE_GENERAL_REPROCESOS} "
                    f"reprocesos (reprocesos_realizados={reprocesos})."
                )
                _agregar_referencia(referencias, "MAN-INC v2 §4")
    else:
        if reprocesos >= LIMITE_GENERAL_REPROCESOS:
            limite_alcanzado_general = True
            motivos.append(
                f"El caso alcanzó el límite máximo general de {LIMITE_GENERAL_REPROCESOS} "
                f"reprocesos (reprocesos_realizados={reprocesos})."
            )
            _agregar_referencia(referencias, "MAN-INC v2 §4")

    # Paso 4: construcción determinista de ResultadoEvaluacion.
    if not motivos:
        regla = REGLAS_CAT_ERR_V2[codigo_error]
        motivos_ok = [
            f"El caso '{caso.caso_id}' se encuentra en estado elegible ('{estado}').",
            "El caso no tiene decisión final irreversible registrada.",
            f"El código de error '{codigo_error}' es reprocesable según CAT-ERR v2.",
            f"El servicio dependiente '{servicio_dep_id}' se encuentra 'operativo'.",
        ]
        if codigo_error == "E-207" and servicio_dep_id != SERVICIO_MODELOS_ID:
            motivos_ok.append(f"El servicio '{SERVICIO_MODELOS_ID}' se encuentra 'operativo'.")
        if codigo_error == "E-512":
            motivos_ok.append(
                f"El caso registra {reprocesos} de {LIMITE_E512} reproceso permitido para E-512 "
                "(contador global por caso)."
            )
        else:
            motivos_ok.append(
                f"El caso registra {reprocesos} de {LIMITE_GENERAL_REPROCESOS} reprocesos "
                "permitidos por MAN-INC v2."
            )
        refs_ok = ["MAN-INC v2 §4", regla.referencia, "GUI-COL v1 §1"]
        return ResultadoEvaluacion(
            puede_reprocesar=True,
            motivos=motivos_ok,
            accion_recomendada=regla.accion_recomendada,
            referencias_normativas=refs_ok,
        )

    accion = _seleccionar_accion_bloqueo(
        tiene_bloqueo_decision_final=tiene_bloqueo_decision_final,
        tiene_inconsistencia_ex05=tiene_inconsistencia_ex05,
        codigo_no_reprocesable=codigo_no_reprocesable,
        limite_alcanzado_e512=limite_alcanzado_e512,
        limite_alcanzado_general=limite_alcanzado_general,
        servicio_no_operativo_e207=servicio_no_operativo_e207,
        servicio_no_operativo_otro=servicio_no_operativo_otro,
        servicio_no_operativo_e207_otro_id=servicio_no_operativo_e207_otro_id,
    )
    return ResultadoEvaluacion(
        puede_reprocesar=False,
        motivos=motivos,
        accion_recomendada=accion,
        referencias_normativas=referencias,
    )
