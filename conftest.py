"""Stops a bare `pytest` at the repo root with a pointer instead of ten import errors.

Each problem is its own pytest project (its folder holds the pytest.ini), so this
file is only ever loaded when pytest is started from here, above all of them.
"""
import pytest


def pytest_configure(config):
    pytest.exit(
        "Run pytest from inside a problem folder (for example: cd problems/p1_custom_exceptions), "
        "or run ./scripts/check.sh (scripts\\check.ps1 on Windows) from here to check every problem.",
        returncode=4,
    )
