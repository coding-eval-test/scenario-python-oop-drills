#!/usr/bin/env bash
# Scores every problem the same way the grader does.
set -uo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root" || exit 1
manifest="$root/scenario.json"

if [ ! -f "$manifest" ]; then
  echo "scenario.json not found at ${manifest} — cannot tell which problems to check."
  exit 1
fi

# scenario.json is the same file the grader reads. Parsed with sed rather than jq
# because jq is not installed everywhere this runs; CI keeps the file in the
# one-key-per-line shape this depends on.
text() { sed -n "s/.*\"$1\"[[:space:]]*:[[:space:]]*\"\([^\"]*\)\".*/\1/p" "$manifest"; }
number() { sed -n "s/.*\"$1\"[[:space:]]*:[[:space:]]*\([0-9][0-9]*\).*/\1/p" "$manifest"; }

mapfile -t ids < <(text category)
mapfile -t paths < <(text path)
mapfile -t worths < <(number points)
mapfile -t pins < <(number tests)
mapfile -t guard_pins < <(number guards)

count=${#ids[@]}
if [ "$count" -eq 0 ]; then
  echo "No problems found in ${manifest}. Expected \"category\" entries — is the file valid JSON?"
  exit 1
fi
for list in paths worths pins guard_pins; do
  declare -n values="$list"
  if [ "${#values[@]}" -ne "$count" ]; then
    echo "scenario.json is malformed: ${count} problems but ${#values[@]} '${list}' values."
    exit 1
  fi
  unset -n values
done

# One attribute of the report's <testsuite ...> tag. The trailing space in the
# anchor keeps the <testsuites> wrapper from ever being the matched line.
attr() { sed -n "s/.*<testsuite [^>]*$2=\"\([0-9]*\)\".*/\1/p" "$1" | head -1; }

# pytest exits 0 (all passed), 1 (some failed) or 5 (nothing collected) on a run
# that actually ran. Anything else — 2 is a collection or import error — is not a
# score, it is a broken problem.
ran() { [ "$1" -eq 0 ] || [ "$1" -eq 1 ] || [ "$1" -eq 5 ]; }

reports="$root/reports"
lines=()
total=0
max=0
overall=0

for i in "${!ids[@]}"; do
  id="${ids[$i]}"
  dir="${paths[$i]}"
  worth="${worths[$i]}"
  pinned="${pins[$i]}"
  guards="${guard_pins[$i]}"
  max=$((max + worth))

  echo ""
  echo "=== ${id} (${dir}) ==="
  rm -rf "$reports"
  mkdir -p "$reports"

  result=""
  earned=0
  passed=0
  scored_exit=0
  guard_exit=0

  if [ "$pinned" -lt 1 ]; then
    result="ERROR"
  elif [ ! -d "$root/$dir" ]; then
    echo "Problem folder ${dir} is missing."
    result="ERROR"
  else
    # Each problem is its own pytest project: run from inside its folder, in a
    # subshell so the working directory is back here afterwards. stdin is closed
    # so nothing a test reads can swallow the rest of this script's input.
    ( cd "$root/$dir" && python -m pytest -m "not guard" --junitxml="$reports/${id}.xml" < /dev/null )
    scored_exit=$?
    if [ "$guards" -gt 0 ]; then
      ( cd "$root/$dir" && python -m pytest -m guard --junitxml="$reports/${id}-guard.xml" < /dev/null )
      guard_exit=$?
    fi
  fi

  scored_report="$reports/${id}.xml"
  guard_report="$reports/${id}-guard.xml"
  if [ -z "$result" ]; then
    if ! ran "$scored_exit" || ! ran "$guard_exit" || [ ! -e "$scored_report" ]; then
      result="ERROR"
    elif [ "$guards" -gt 0 ] && [ ! -e "$guard_report" ]; then
      result="ERROR"
    fi
  fi

  if [ -z "$result" ]; then
    collected=$(attr "$scored_report" tests)
    skipped=$(attr "$scored_report" skipped)
    failures=$(attr "$scored_report" failures)
    errors=$(attr "$scored_report" errors)
    passed=$(( ${collected:-0} - ${failures:-0} - ${errors:-0} - ${skipped:-0} ))

    guard_collected=0
    guard_skipped=0
    guard_passed=0
    if [ "$guards" -gt 0 ]; then
      guard_collected=$(attr "$guard_report" tests)
      guard_skipped=$(attr "$guard_report" skipped)
      guard_failures=$(attr "$guard_report" failures)
      guard_errors=$(attr "$guard_report" errors)
      guard_passed=$(( ${guard_collected:-0} - ${guard_failures:-0} - ${guard_errors:-0} - ${guard_skipped:-0} ))
    fi

    # Whole-number points, rounded down.
    base=$(( worth * passed / pinned ))

    # Order matters: the first matching row wins, same as the grader.
    if [ "${collected:-0}" -ne "$pinned" ] || [ "${guard_collected:-0}" -ne "$guards" ]; then
      result="TAMPERED"
    elif [ "${skipped:-0}" -gt 0 ] || [ "${guard_skipped:-0}" -gt 0 ]; then
      result="SKIPPED"
    elif [ "$guard_passed" -ne "$guards" ]; then
      result="GUARD-BROKEN"
      earned=$(( base / 2 ))
    elif [ "$passed" -eq "$pinned" ]; then
      result="PASS"
      earned="$worth"
    elif [ "$passed" -gt 0 ]; then
      result="PARTIAL"
      earned="$base"
    else
      result="FAIL"
    fi
  fi

  if [ "$result" != "PASS" ]; then
    overall=1
  fi
  total=$((total + earned))
  lines+=("$(printf '%-6s %-13s %2s / %-4s %3s / %s' "$id" "$result" "$passed" "$pinned" "$earned" "$worth")")
done

echo ""
echo "================ SUMMARY ================"
echo "       Result        Tests     Points"
for line in "${lines[@]}"; do
  echo "$line"
done
printf '%-6s %-13s %9s %3s / %s\n' "TOTAL" "" "" "$total" "$max"
echo "========================================="

exit $overall
