#!/usr/bin/env bash
# Rebuild the notes hub and five mini-book handbooks into docs/ for GitHub Pages.
#
#   docs/index.html                         hub at /notes/
#   docs/genomics/index.html                /notes/genomics/
#   docs/databricks/index.html              /notes/databricks/
#   docs/software-engineering/index.html    /notes/software-engineering/
#   docs/statistics/index.html              /notes/statistics/
#   docs/data-generation/index.html         /notes/data-generation/
#
# Shared styling stays in docs/styles.css. Each handbook links to ../styles.css
# so the sheet resolves when the page is served from /notes/<slug>/.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "pandoc is required (https://pandoc.org/)." >&2
  exit 1
fi

if [[ ! -f docs/styles.css ]]; then
  echo "Missing docs/styles.css" >&2
  exit 1
fi

mkdir -p docs
BUILD_DIR="$(mktemp -d)"
trap 'rm -rf "$BUILD_DIR"' EXIT

python3 "$ROOT/scripts/assemble_handbooks.py" "$BUILD_DIR"

FROM='markdown+yaml_metadata_block+fenced_code_blocks+pipe_tables+strikeout+link_attributes'
COMMON=(
  --from "$FROM"
  --standalone
  --toc
  --eol=lf
  --metadata lang=en-AU
)

pandoc "$BUILD_DIR/hub.md" \
  "${COMMON[@]}" \
  --toc-depth=1 \
  -c styles.css \
  -o docs/index.html

while IFS=$'\t' read -r slug title; do
  [[ -n "$slug" ]] || continue
  mkdir -p "docs/$slug"
  pandoc "$BUILD_DIR/$slug.md" \
    "${COMMON[@]}" \
    --toc-depth=2 \
    -c ../styles.css \
    -o "docs/$slug/index.html"
  echo "Wrote docs/$slug/index.html ($title)"
done < "$BUILD_DIR/books.tsv"

# Pages must not run Jekyll over the static build.
: > docs/.nojekyll

python3 "$ROOT/scripts/assemble_handbooks.py" --verify

echo "Wrote docs/index.html ($(wc -c < docs/index.html) bytes)"
echo "Kept docs/styles.css and docs/.nojekyll"
