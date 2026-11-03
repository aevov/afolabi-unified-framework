#!/usr/bin/env bash
# check_links.sh — verify every external URL referenced in the repo's markdown.
# Run from the repo root on a machine with open outbound network:
#     bash tools/check_links.sh
#
# Extracts all http(s) URLs from *.md, drops known API-doc placeholders,
# de-dupes, and prints the HTTP status for each (following redirects).

set -u
UA="Mozilla/5.0 (link-check)"

# Placeholder / example URLs that are intentionally not live — skip these.
SKIP_RE='localhost|your-server\.com|usr_abc123|/errors/|/authorize|/token|cdn\.auf\.technology|sandbox-api|img\.shields\.io|zenodo\.org/badge'

mapfile -t urls < <(
  grep -rhoE 'https?://[a-zA-Z0-9./?=_%:+#@-]+' --include='*.md' . \
    | sed 's/[).,]*$//' \
    | grep -vE "$SKIP_RE" \
    | sort -u
)

printf '%-56s %s\n' "URL" "STATUS"
printf '%-56s %s\n' "---" "------"
fail=0
for u in "${urls[@]}"; do
  code=$(curl -s -o /dev/null -w '%{http_code}' -L --max-time 20 -A "$UA" "$u")
  printf '%-56s %s\n' "$u" "$code"
  case "$code" in 2*|3*) ;; *) fail=$((fail+1)) ;; esac
done
echo
echo "Checked ${#urls[@]} URLs — ${fail} not OK (non-2xx/3xx)."
