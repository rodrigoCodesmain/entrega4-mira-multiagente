#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../../.." && pwd)"
SUMS_FILE="${REPO_ROOT}/docs/kit-sha256sums.txt"

MODE="run"
if [[ "${1:-}" == "--check-only" ]]; then
  MODE="check-only"
  shift
fi

if [[ ! -f "${SUMS_FILE}" ]]; then
  echo "[ERROR] No existe ${SUMS_FILE}" >&2
  exit 1
fi

echo "[INFO] Verificando integridad del kit CU-2..."
(cd "${REPO_ROOT}" && sha256sum -c "${SUMS_FILE}")

find_pytest() {
  if [[ -x "${REPO_ROOT}/.venv/bin/pytest" ]]; then
    echo "${REPO_ROOT}/.venv/bin/pytest"
    return 0
  fi
  if command -v pytest >/dev/null 2>&1; then
    command -v pytest
    return 0
  fi
  if command -v uv >/dev/null 2>&1 && [[ -f "${REPO_ROOT}/pyproject.toml" ]]; then
    echo "uv run --no-sync pytest"
    return 0
  fi
  return 1
}

if [[ "${MODE}" == "check-only" ]]; then
  echo "[INFO] Python: $(python3 --version 2>&1)"
  if PYTEST_CMD="$(find_pytest)"; then
    echo "[INFO] pytest detectado: ${PYTEST_CMD}"
  else
    echo "[INFO] pytest aun no disponible (esperado antes de instalar dependencias en fase de implementacion)."
  fi
  if [[ -d "${REPO_ROOT}/tests" ]]; then
    echo "[INFO] Directorio tests/: presente"
  else
    echo "[INFO] Directorio tests/: aun no creado (esperado en fase de preparacion)."
  fi
  echo "[OK] Chequeo en modo solo lectura completado."
  exit 0
fi

if [[ ! -d "${REPO_ROOT}/tests" ]]; then
  echo "[ERROR] No existe el directorio tests/ en ${REPO_ROOT}" >&2
  exit 1
fi

if ! PYTEST_CMD="$(find_pytest)"; then
  echo "[ERROR] No se encontró pytest (.venv/bin/pytest, PATH ni uv run)." >&2
  exit 1
fi

echo "[INFO] Ejecutando pytest sin escribir bytecode ni cache en el repositorio..."
export PYTHONDONTWRITEBYTECODE=1
cd "${REPO_ROOT}"
# shellcheck disable=SC2086
exec ${PYTEST_CMD} -p no:cacheprovider -v "$@"
