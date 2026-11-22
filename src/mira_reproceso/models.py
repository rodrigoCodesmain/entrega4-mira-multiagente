"""Modelos de dominio inmutables y excepciones para MIRA CU-2."""

from __future__ import annotations

from dataclasses import dataclass


class UsuarioNoAutorizadoError(Exception):
    """El usuario no existe o carece de un rol habilitado para evaluar reprocesamiento."""


class CasoNoEncontradoError(Exception):
    """El caso solicitado no existe en el registro operativo."""


@dataclass(frozen=True)
class Usuario:
    """Actor operativo habilitado o consultante en el prototipo."""

    usuario_id: str
    rol: str
    nombre: str | None = None
    organizacion_id: str | None = None


@dataclass(frozen=True)
class Servicio:
    """Servicio interno o externo del que dependen los módulos de MIRA."""

    servicio_id: str
    estado: str
    nombre: str | None = None
    tipo: str | None = None


@dataclass(frozen=True)
class Caso:
    """Metadatos estructurados de un caso operativo sin contenido de evidencia."""

    caso_id: str
    estado: str
    codigo_error: str
    servicio_dependiente: str
    reprocesos_realizados: int
    tiene_decision_final: bool
    organizacion_id: str | None = None


@dataclass(frozen=True)
class DatosOperativos:
    """Conjunto de datos operativos estructurados (sin registro_tecnico)."""

    usuarios: dict[str, Usuario]
    servicios: dict[str, Servicio]
    casos: dict[str, Caso]


@dataclass(frozen=True)
class ReglaCodigoError:
    """Regla normativa vigente por código de error en CAT-ERR v2."""

    codigo: str
    descripcion: str
    reprocesable: bool
    condicion: str
    motivo_bloqueo: str | None
    accion_recomendada: str
    referencia: str


@dataclass(frozen=True)
class ResultadoEvaluacion:
    """Resultado determinista de elegibilidad para reprocesamiento."""

    puede_reprocesar: bool
    motivos: list[str]
    accion_recomendada: str
    referencias_normativas: list[str]
