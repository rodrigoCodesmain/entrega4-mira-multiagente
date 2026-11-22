#!/usr/bin/env python3
"""Verificador de solo lectura para integridad del kit CU-2 y matriz de trazabilidad."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

REQUIRED_HEADERS = (
    "ID Regla",
    "Documento Vigente y Sección",
    "ID Requisito",
    "Componente / Función",
    "Caso de Prueba",
    "Estado",
)

FORBIDDEN_ACTIVE_PATTERNS = (
    re.compile(r"CAT-ERR[\s_]*v1", re.IGNORECASE),
    re.compile(r"CAT-ERR_v1_derogado", re.IGNORECASE),
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def check_kit_checksums(root: Path) -> list[str]:
    errors: list[str] = []
    sums_file = root / "docs" / "kit-sha256sums.txt"
    if not sums_file.is_file():
        return [f"No se encuentra archivo de checksums: {sums_file}"]

    entries = [line.strip() for line in sums_file.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not entries:
        return [f"Archivo de checksums vacío: {sums_file}"]

    for entry in entries:
        parts = entry.split(maxsplit=1)
        if len(parts) != 2:
            errors.append(f"Línea inválida en checksums: {entry}")
            continue
        expected_hash, rel_path = parts[0], parts[1].lstrip("* ")
        target = root / rel_path
        if not target.is_file():
            errors.append(f"Archivo faltante del kit: {rel_path}")
            continue
        actual_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            errors.append(f"Hash alterado en {rel_path}: esperado {expected_hash}, actual {actual_hash}")

    return errors


def check_matrix(matrix_path: Path) -> list[str]:
    errors: list[str] = []
    if not matrix_path.is_file():
        return [f"No existe la matriz de trazabilidad: {matrix_path}"]

    lines = matrix_path.read_text(encoding="utf-8").splitlines()
    table_lines = [ln.strip() for ln in lines if ln.strip().startswith("|")]
    if len(table_lines) < 3:
        return [f"La matriz {matrix_path} debe contener encabezado, separador y al menos una fila."]

    header_cells = [c.strip() for c in table_lines[0].strip("|").split("|")]
    missing = [h for h in REQUIRED_HEADERS if h not in header_cells]
    if missing:
        errors.append(f"Encabezados faltantes en matriz: {', '.join(missing)}")

    data_rows = [
        ln for ln in table_lines[2:]
        if not set(ln.replace("|", "").replace("-", "").replace(":", "").strip()) == set()
    ]
    if not data_rows:
        errors.append("La matriz no contiene filas de trazabilidad.")

    for idx, row in enumerate(data_rows, start=1):
        for pat in FORBIDDEN_ACTIVE_PATTERNS:
            if pat.search(row):
                errors.append(f"Fila {idx} referencia fuente derogada ({pat.pattern}): {row}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verifica integridad del kit CU-2 y matriz de trazabilidad.")
    parser.add_argument("--check-kit", action="store_true", help="Verifica hashes SHA-256 de kit/CU-2_soporte_operacion.")
    parser.add_argument("--matrix", type=Path, help="Ruta a specs/03-trazabilidad.md para validar su estructura.")
    args = parser.parse_args()

    if not args.check_kit and args.matrix is None:
        parser.error("Debes especificar --check-kit y/o --matrix.")

    root = repo_root()
    errors: list[str] = []

    if args.check_kit:
        kit_errors = check_kit_checksums(root)
        if kit_errors:
            errors.extend(kit_errors)
        else:
            print("[OK] Integridad del kit CU-2 verificada contra docs/kit-sha256sums.txt.")

    if args.matrix is not None:
        matrix_target = args.matrix if args.matrix.is_absolute() else (root / args.matrix)
        matrix_errors = check_matrix(matrix_target)
        if matrix_errors:
            errors.extend(matrix_errors)
        else:
            print(f"[OK] Matriz de trazabilidad válida: {matrix_target}")

    if errors:
        for err in errors:
            print(f"[ERROR] {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
