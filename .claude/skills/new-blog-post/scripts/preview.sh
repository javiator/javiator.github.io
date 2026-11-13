#!/usr/bin/env bash
# Build the site locally and render a post for review.
#   preview.sh <path/to/post.md>     -> .preview/<slug>.png, .preview/<slug>.pdf and a check report
#   preview.sh --build-only          -> just build into .preview/site
# Exit code 1 means the build failed or the rendered page has problems to fix.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../../.." && pwd)"
OUT="$ROOT/.preview"
export BUNDLE_GEMFILE="$HERE/Gemfile" LANG=C.UTF-8 LC_ALL=C.UTF-8
mkdir -p "$OUT"
cd "$ROOT"

if ! bundle check >/dev/null 2>&1; then
  echo "Installing preview gems (first run only)..."
  bundle install --quiet 2>&1 | grep -v -i "warning\|root" || true
fi
JEKYLL="$(bundle exec ruby -e 'puts Gem.loaded_specs["jekyll"].bin_file("jekyll")')"

echo "Building site..."
if ! bundle exec ruby "$JEKYLL" build --future --quiet \
      --config "_config.yml,$HERE/_config.preview.yml" -d "$OUT/site" >"$OUT/build.log" 2>&1; then
  grep -v "^\s*from \|warning:" "$OUT/build.log" | tail -25
  echo "BUILD FAILED (full log: .preview/build.log)"
  exit 1
fi
grep -i "liquid\|error" "$OUT/build.log" | grep -v "faraday" || true
echo "Build OK"

[ "${1:-}" = "--build-only" ] && exit 0
[ -n "${1:-}" ] || { echo "usage: preview.sh <post.md>"; exit 2; }
URL="$(python3 "$HERE/validate_post.py" --url "$1")"
node "$HERE/render_preview.js" "$OUT/site" "$URL" "$OUT" "$1"
