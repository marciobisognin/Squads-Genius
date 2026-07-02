#!/bin/bash
# Verify squad compliance: check LICENSE, required directories, and squad.yaml syntax
# Usage: ./scripts/verify-squad-compliance.sh

set -e

REPO_ROOT="${1:-.}"
PASS=0
FAIL=0
WARN=0

echo "🔍 Verifying squad compliance in: $REPO_ROOT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

# Find all squad.yaml files
while IFS= read -r squad_yaml; do
  squad_dir=$(dirname "$squad_yaml")
  squad_name=$(basename "$squad_dir")
  has_error=0

  # Check for LICENSE
  if [ ! -f "$squad_dir/LICENSE" ]; then
    echo "❌ $squad_name — missing LICENSE"
    has_error=1
    FAIL=$((FAIL+1))
  fi

  # Check for required directories
  for dir in agents tasks workflows; do
    if [ ! -d "$squad_dir/$dir" ]; then
      echo "⚠️  $squad_name — missing $dir/ directory"
      has_error=1
      WARN=$((WARN+1))
    fi
  done

  # Check for README
  if [ ! -f "$squad_dir/README.md" ]; then
    echo "⚠️  $squad_name — missing README.md"
    has_error=1
    WARN=$((WARN+1))
  fi

  if [ $has_error -eq 0 ]; then
    echo "✅ $squad_name — PASS"
    PASS=$((PASS+1))
  fi

done < <(find "$REPO_ROOT" -name "squad.yaml" | sort)

echo
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Results: ✅ $PASS PASS, ⚠️  $WARN warnings, ❌ $FAIL failures"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $FAIL -gt 0 ]; then
  exit 1
fi
