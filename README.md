# Python OOP & Exceptions — problem set

Five short, independent problems. Each one hands you a small piece of working code and
a list of requirements to build against it — the shape of a timed coding evaluation,
without the timer. Suggested time for the whole set: 75 minutes.

## How to work

1. Open a folder under `problems/` and read its `PROBLEM.md`.
2. Change the code in that folder until its tests pass. Leave `tests/` as it shipped.
3. Check one problem from inside its folder:

   ```bash
   cd problems/p1_custom_exceptions
   python -m pytest
   ```

4. Check everything from the repository root:

   ```bash
   ./scripts/check.sh        # scripts\check.ps1 on Windows
   ```

The problems do not depend on each other — take them in any order.

Each problem is its own pytest project, so `pytest` only works from inside a problem
folder. Started from the repository root it stops and points you back here.

## Stack

Python 3.11 · pytest. The devcontainer (or a Codespace) has both installed. Working
locally instead: install Python 3.11, then `pip install -r requirements.txt`.

## Scoring

Every push runs the `Grade` workflow and writes a scorecard to the run summary.
`./scripts/check.sh` prints the same numbers locally.

- **Partial credit.** A problem earns points in proportion to how many of its
  `tests/test_requirements.py` tests pass, rounded down to a whole point. All of them
  passing earns the full 20.
- **Existing behavior.** `tests/test_existing.py` covers what already worked. Those
  tests earn nothing, but while any of them fails, that problem earns half of what it
  otherwise would (rounded down). Other problems are unaffected.
- **The tests are counted.** A problem whose tests were removed, added to, or skipped
  scores 0 until `tests/` matches what shipped. Experiments of your own belong
  outside `tests/`.
- **A problem that cannot be imported scores 0** and shows as `error` — a syntax
  error, for instance. It never affects another problem's score.

<!-- grading-table:start -->
| Problem | Points |
| --- | --- |
| P1 — Custom exception hierarchy | 20 |
| P2 — Inheritance and abstract bases | 20 |
| P3 — Data-model methods | 20 |
| P4 — Runtime object manipulation | 20 |
| P5 — Properties and validation | 20 |
<!-- grading-table:end -->
