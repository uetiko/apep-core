#!/usr/bin/env bash
# Regresión de approvals del harness contra el OMP instalado.
#
# Resuelve cada caso de `cases.ts` con el resolutor de approvals del runtime y la
# config efectiva del session root. NO ejecuta comandos ni tools y NO llama al
# modelo: la extensión termina el proceso en `session_start`.
#
#   .omp/tests/approvals/run.sh              # informe legible; exit 0 = todo PASS
#   APPROVAL_REGRESSION_JSON=out.json .omp/tests/approvals/run.sh
#
# Exit: 0 PASS · 1 algún FAIL · 2 error del harness.
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
workspace="${APEP_TEST_WORKSPACE:-$PWD}"

echo "OMP_VERSION: $(omp --version)"
# `--cwd` fija el session root canónico, aunque se invoque desde otro directorio.
# `--tools read` y `--no-session` acotan la sesión por si el guard fallara.
exec omp --cwd "$workspace" --no-session --tools read -e "$here/approval-regression.ts" -p "approval-regression" </dev/null
