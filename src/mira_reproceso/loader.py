"""Cargador en modo estrictamente de solo lectura para CU-2_datos.xlsx."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import openpyxl

from mira_reproceso.models import Caso, DatosOperativos, Servicio, Usuario

DEFAULT_EXCEL_PATH = (
    Path(__file__).resolve().parents[2]
    / "kit"
    / "CU-2_soporte_operacion"
    / "datos"
    / "CU-2_datos.xlsx"
)

_HOJAS_LEIDAS = ("usuarios", "servicios", "casos")
_VALORES_VERDADEROS = frozenset({"sí", "si", "true", "1"})
_VALORES_FALSOS = frozenset({"no", "false", "0"})


def _normalizar_texto(valor: Any, *, campo: str, minusculas: bool = False) -> str:
    if valor is None:
        raise ValueError(f"El campo obligatorio '{campo}' no puede ser nulo.")
    texto = str(valor).strip()
    if not texto:
        raise ValueError(f"El campo obligatorio '{campo}' no puede estar vacío.")
    return texto.lower() if minusculas else texto


def _normalizar_texto_opcional(valor: Any, *, minusculas: bool = False) -> str | None:
    if valor is None:
        return None
    texto = str(valor).strip()
    if not texto:
        return None
    return texto.lower() if minusculas else texto


def _normalizar_entero(valor: Any, *, campo: str) -> int:
    if isinstance(valor, bool) or valor is None:
        raise ValueError(f"Valor inválido para campo entero '{campo}': {valor!r}")
    if isinstance(valor, int):
        return valor
    if isinstance(valor, float) and valor.is_integer():
        return int(valor)
    texto = str(valor).strip()
    try:
        return int(texto)
    except ValueError as exc:
        raise ValueError(f"Valor inválido para campo entero '{campo}': {valor!r}") from exc


def normalizar_decision_final(valor: Any) -> bool:
    """Normaliza valores booleanos/textuales de `tiene_decision_final`."""
    if isinstance(valor, bool):
        return valor
    if isinstance(valor, int) and valor in (0, 1):
        return bool(valor)
    if isinstance(valor, float) and valor in (0.0, 1.0):
        return bool(int(valor))
    if valor is None:
        raise ValueError("El campo 'tiene_decision_final' no puede ser nulo.")
    texto = str(valor).strip().lower()
    if texto in _VALORES_VERDADEROS:
        return True
    if texto in _VALORES_FALSOS:
        return False
    raise ValueError(f"Valor inválido para 'tiene_decision_final': {valor!r}")


def _extraer_filas_con_encabezado(ws: Any, hoja: str, requeridas: tuple[str, ...]) -> list[dict[str, Any]]:
    filas_iter = ws.iter_rows(values_only=True)
    encabezados: list[str] | None = None
    registros: list[dict[str, Any]] = []

    for fila in filas_iter:
        if fila is None or all(celda is None or str(celda).strip() == "" for celda in fila):
            continue
        if encabezados is None:
            encabezados = [
                str(celda).strip() if celda is not None else ""
                for celda in fila
            ]
            faltantes = [col for col in requeridas if col not in encabezados]
            if faltantes:
                raise ValueError(
                    f"La hoja '{hoja}' no contiene las columnas requeridas: {', '.join(faltantes)}"
                )
            continue

        registro = {
            encabezados[idx]: fila[idx] if idx < len(fila) else None
            for idx in range(len(encabezados))
            if encabezados[idx]
        }
        registros.append(registro)

    if encabezados is None:
        raise ValueError(f"La hoja '{hoja}' no contiene fila de encabezados.")
    return registros


def cargar_datos_excel(excel_path: Path | str | None = None) -> DatosOperativos:
    """Carga usuarios, servicios y casos en modo solo lectura desde CU-2_datos.xlsx.

    Omite completamente `registro_tecnico` y demás hojas no operativas para
    impedir que texto libre no confiable entre al modelo de dominio.
    """
    ruta = DEFAULT_EXCEL_PATH if excel_path is None else Path(excel_path)
    if not ruta.is_file():
        raise FileNotFoundError(f"No se encontró el archivo Excel operativo: {ruta}")

    wb = openpyxl.load_workbook(ruta, read_only=True, data_only=True)
    try:
        for hoja in _HOJAS_LEIDAS:
            if hoja not in wb.sheetnames:
                raise ValueError(f"Falta la hoja obligatoria '{hoja}' en {ruta}.")

        filas_usuarios = _extraer_filas_con_encabezado(
            wb["usuarios"], "usuarios", ("usuario_id", "rol")
        )
        filas_servicios = _extraer_filas_con_encabezado(
            wb["servicios"], "servicios", ("servicio_id", "estado")
        )
        filas_casos = _extraer_filas_con_encabezado(
            wb["casos"],
            "casos",
            (
                "caso_id",
                "estado",
                "codigo_error",
                "servicio_dependiente",
                "reprocesos_realizados",
                "tiene_decision_final",
            ),
        )
    finally:
        wb.close()

    usuarios: dict[str, Usuario] = {}
    for fila in filas_usuarios:
        usuario_id = _normalizar_texto(fila.get("usuario_id"), campo="usuario_id")
        org_raw = fila.get("organizacion_id")
        if org_raw is None:
            org_raw = fila.get("organizacion")
        usuarios[usuario_id] = Usuario(
            usuario_id=usuario_id,
            rol=_normalizar_texto(fila.get("rol"), campo="rol", minusculas=True),
            nombre=_normalizar_texto_opcional(fila.get("nombre")),
            organizacion_id=_normalizar_texto_opcional(org_raw),
        )

    servicios: dict[str, Servicio] = {}
    for fila in filas_servicios:
        servicio_id = _normalizar_texto(fila.get("servicio_id"), campo="servicio_id")
        servicios[servicio_id] = Servicio(
            servicio_id=servicio_id,
            estado=_normalizar_texto(fila.get("estado"), campo="estado", minusculas=True),
            nombre=_normalizar_texto_opcional(fila.get("nombre")),
            tipo=_normalizar_texto_opcional(fila.get("tipo"), minusculas=True),
        )

    casos: dict[str, Caso] = {}
    for fila in filas_casos:
        caso_id = _normalizar_texto(fila.get("caso_id"), campo="caso_id")
        org_raw = fila.get("organizacion_id")
        if org_raw is None:
            org_raw = fila.get("org_id")
        casos[caso_id] = Caso(
            caso_id=caso_id,
            estado=_normalizar_texto(fila.get("estado"), campo="estado", minusculas=True),
            codigo_error=_normalizar_texto(fila.get("codigo_error"), campo="codigo_error"),
            servicio_dependiente=_normalizar_texto(
                fila.get("servicio_dependiente"), campo="servicio_dependiente"
            ),
            reprocesos_realizados=_normalizar_entero(
                fila.get("reprocesos_realizados"), campo="reprocesos_realizados"
            ),
            tiene_decision_final=normalizar_decision_final(fila.get("tiene_decision_final")),
            organizacion_id=_normalizar_texto_opcional(org_raw),
        )

    return DatosOperativos(usuarios=usuarios, servicios=servicios, casos=casos)
