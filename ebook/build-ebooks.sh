#!/usr/bin/env bash
# Genera los ebooks del harness y de la governance desde su Markdown canónico.
#
#   .omp/ebook/build-ebooks.sh manual       → .omp/MANUAL.epub
#   .omp/ebook/build-ebooks.sh user-guide   → .omp/USER_GUIDE.epub
#   .omp/ebook/build-ebooks.sh cookbook     → .omp/COOKBOOK.epub
#   .omp/ebook/build-ebooks.sh governance   → docs/governance/ENGINEERING_GOVERNANCE.epub
#   .omp/ebook/build-ebooks.sh all          → los cuatro
#
# Cada EPUB queda junto a su fuente.
# Markdown es la fuente; el EPUB se genera y nunca se edita a mano.
# Configuración compartida: epub.yaml (pandoc), kindle.css, local-links.lua, wide-tables.lua.
# Los documentos del harness toman la versión de .omp/VERSION; la governance tiene la suya
# propia y su título es su primer encabezado. La fecha es la del build; EBOOK_DATE=AAAA-MM-DD la fija.
# Cada EPUB se valida (validate_epub.py) antes de sustituir al anterior.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OMP="$(dirname "$HERE")"
GOV="$(dirname "$OMP")/docs/governance/ENGINEERING_GOVERNANCE.md"
VERSION="$(tr -d '[:space:]' < "$OMP/VERSION")"
DATE="${EBOOK_DATE:-$(date +%F)}"
# Marca de tiempo estable dentro del ZIP: mismo día + misma fuente → mismo EPUB.
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-$(date -u -d "$DATE 00:00" +%s)}"

command -v pandoc >/dev/null || { echo "pandoc no está instalado" >&2; exit 2; }

TMP=""
cleanup() { if [[ -n "$TMP" ]]; then rm -f "$TMP"; fi; }
trap cleanup EXIT

build() {
  local name="$1" src="$2" title="$3" id="$4"   # rótulo · fuente · título · identificador EPUB
  local out="${src%.md}.epub"
  if [[ ! -f "$src" ]]; then
    echo "$name: NOT_PRESENT ($src no existe)"
    return 0
  fi
  local before
  before="$(sha256sum "$src")"
  TMP="$(mktemp "$HERE/.$name.XXXXXX.epub")"
  pandoc "$src" --defaults "$HERE/epub.yaml" -o "$TMP" \
    --metadata title="$title" --metadata date="$DATE" --metadata identifier="$id"
  [[ "$(sha256sum "$src")" == "$before" ]] || { echo "$name: el build modificó la fuente" >&2; return 1; }
  echo "$name: validando"
  python3 -I "$HERE/validate_epub.py" "$TMP" "$title" "$HERE/kindle.css"
  chmod --reference="$src" "$TMP"   # mktemp crea 0600; el EPUB hereda los permisos de su fuente
  mv -f "$TMP" "$out"
  TMP=""
  echo "$name: $out · $(stat -c%s "$out") bytes · sha256 $(sha256sum "$out" | cut -d' ' -f1)"
}

harness() {   # MANUAL | USER_GUIDE | COOKBOOK
  build "$1" "$OMP/$1.md" "${1//_/ } — Apep Core Engineering Harness v$VERSION" \
    "urn:apep-core:omp-harness:$(tr '_' '-' <<<"${1,,}")"
}

governance() {
  local title=""
  [[ -f "$GOV" ]] && title="$(sed -n '1s/^# *//p' "$GOV")"
  build ENGINEERING_GOVERNANCE "$GOV" "$title" "urn:apep-core:engineering-governance"
}


case "${1:-}" in
  manual)     harness MANUAL ;;
  user-guide) harness USER_GUIDE ;;
  cookbook)   harness COOKBOOK ;;
  governance) governance ;;
  all)        harness MANUAL; harness USER_GUIDE; harness COOKBOOK; governance ;;
  *)          echo "uso: $0 manual|user-guide|cookbook|governance|all" >&2; exit 2 ;;
esac
