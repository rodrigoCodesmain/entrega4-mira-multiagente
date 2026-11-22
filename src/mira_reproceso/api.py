"""Aplicación FastAPI mínima y contrato HTTP para MIRA CU-2."""

from __future__ import annotations

from functools import lru_cache

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict, StrictStr, field_validator

from mira_reproceso.loader import cargar_datos_excel
from mira_reproceso.models import (
    CasoNoEncontradoError,
    DatosOperativos,
    UsuarioNoAutorizadoError,
)
from mira_reproceso.rules import evaluar_elegibilidad


class EvaluarRequest(BaseModel):
    """Carga útil mínima de entrada para evaluar elegibilidad de reprocesamiento."""

    model_config = ConfigDict(extra="forbid")

    caso_id: StrictStr
    usuario_id: StrictStr

    @field_validator("caso_id", "usuario_id", mode="after")
    @classmethod
    def validar_cadena_no_vacia(cls, valor: str) -> str:
        limpio = valor.strip()
        if not limpio:
            raise ValueError("El identificador no puede estar vacío ni contener solo espacios.")
        return limpio


class EvaluarResponse(BaseModel):
    """Contrato mínimo de salida de 4 campos (sin campos extra ni alertas S2)."""

    model_config = ConfigDict(extra="forbid")

    puede_reprocesar: bool
    motivos: list[str]
    accion_recomendada: str
    referencias_normativas: list[str]


@lru_cache(maxsize=1)
def _cargar_datos_cacheados() -> DatosOperativos:
    return cargar_datos_excel()


def get_datos() -> DatosOperativos:
    """Dependencia FastAPI que carga bajo demanda los datos en modo solo lectura."""
    return _cargar_datos_cacheados()


def create_app(datos: DatosOperativos | None = None) -> FastAPI:
    """Fábrica de aplicación FastAPI con soporte de datos inyectados en memoria."""
    app = FastAPI(
        title="MIRA CU-2 · Elegibilidad de reprocesamiento",
        version="0.1.0",
        description="Evaluación determinista de solo lectura conforme a MAN-INC v2 y CAT-ERR v2.",
    )

    if datos is not None:
        app.dependency_overrides[get_datos] = lambda: datos

    @app.post(
        "/reprocesamiento/evaluar",
        response_model=EvaluarResponse,
        status_code=status.HTTP_200_OK,
        responses={
            403: {"description": "Usuario no autorizado para evaluar reprocesamiento."},
            404: {"description": "Caso no encontrado."},
        },
    )
    def evaluar_reprocesamiento(
        payload: EvaluarRequest,
        datos_operativos: DatosOperativos = Depends(get_datos),
    ) -> EvaluarResponse:
        try:
            resultado = evaluar_elegibilidad(
                datos=datos_operativos,
                caso_id=payload.caso_id,
                usuario_id=payload.usuario_id,
            )
        except UsuarioNoAutorizadoError as exc:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario no autorizado para evaluar reprocesamiento.",
            ) from exc
        except CasoNoEncontradoError as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Caso no encontrado.",
            ) from exc

        return EvaluarResponse(
            puede_reprocesar=resultado.puede_reprocesar,
            motivos=resultado.motivos,
            accion_recomendada=resultado.accion_recomendada,
            referencias_normativas=resultado.referencias_normativas,
        )

    return app


app = create_app()
