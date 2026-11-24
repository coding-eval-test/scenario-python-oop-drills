# Scores every problem the same way the grader does.
$ErrorActionPreference = 'Continue'

$root = Split-Path -Parent $PSScriptRoot
$manifest = Join-Path $root 'scenario.json'

if (-not (Test-Path $manifest)) {
    Write-Host "scenario.json not found at $manifest - cannot tell which problems to check."
    exit 1
}

# scenario.json is the same file the grader reads.
$problems = @((Get-Content $manifest -Raw -Encoding UTF8 | ConvertFrom-Json).categories)

if ($problems.Count -eq 0) {
    Write-Host "No problems found in $manifest. Expected 'category' entries - is the file valid JSON?"
    exit 1
}

# pytest exits 0 (all passed), 1 (some failed) or 5 (nothing collected) on a run
# that actually ran. Anything else - 2 is a collection or import error - is not a
# score, it is a broken problem.
function Test-Ran {
    param([int]$ExitCode)
    return @(0, 1, 5) -contains $ExitCode
}

# The four counts on a report's <testsuite> element, or $null when it is unreadable.
function Read-Suite {
    param([string]$Path)
    if (-not (Test-Path $Path)) { return $null }
    $suite = ([xml](Get-Content $Path -Raw)).SelectSingleNode('//testsuite')
    if (-not $suite) { return $null }
    $collected = [int]$suite.tests
    $skipped = [int]$suite.skipped
    return [pscustomobject]@{
        Collected = $collected
        Skipped   = $skipped
        Passed    = $collected - [int]$suite.failures - [int]$suite.errors - $skipped
    }
}

$reports = Join-Path $root 'reports'
$rows = New-Object System.Collections.Generic.List[object]
$total = 0
$max = 0
$overall = 0

foreach ($problem in $problems) {
    $id = $problem.category
    $worth = [int]$problem.points
    $pinned = [int]$problem.tests
    $guards = [int]$problem.guards
    $dir = Join-Path $root $problem.path
    $max += $worth

    Write-Host ''
    Write-Host "=== $id ($($problem.path)) ==="
    if (Test-Path $reports) { Remove-Item -Recurse -Force $reports }
    New-Item -ItemType Directory -Path $reports | Out-Null

    $result = ''
    $earned = 0
    $passed = 0
    $scoredExit = 0
    $guardExit = 0
    $scoredReport = Join-Path $reports "$id.xml"
    $guardReport = Join-Path $reports "$id-guard.xml"

    if ($pinned -lt 1) {
        $result = 'ERROR'
    }
    elseif (-not (Test-Path $dir -PathType Container)) {
        Write-Host "Problem folder $($problem.path) is missing."
        $result = 'ERROR'
    }
    else {
        # Each problem is its own pytest project: run from inside its folder, and
        # always come back here afterwards.
        Push-Location $dir
        try {
            python -m pytest -m 'not guard' --junitxml="$scoredReport"
            $scoredExit = $LASTEXITCODE
            if ($guards -gt 0) {
                python -m pytest -m guard --junitxml="$guardReport"
                $guardExit = $LASTEXITCODE
            }
        }
        finally {
            Pop-Location
        }
    }

    $scored = $null
    $guard = [pscustomobject]@{ Collected = 0; Skipped = 0; Passed = 0 }
    if (-not $result) {
        $scored = Read-Suite $scoredReport
        if ($guards -gt 0) { $guard = Read-Suite $guardReport }
        if (-not (Test-Ran $scoredExit) -or -not (Test-Ran $guardExit) -or -not $scored -or -not $guard) {
            $result = 'ERROR'
        }
    }

    if (-not $result) {
        $passed = $scored.Passed
        # Whole-number points, rounded down. [math]::Floor, never an [int] cast:
        # a cast rounds to nearest.
        $base = [int][math]::Floor(($worth * $passed) / $pinned)

        # Order matters: the first matching row wins, same as the grader.
        if ($scored.Collected -ne $pinned -or $guard.Collected -ne $guards) {
            $result = 'TAMPERED'
        }
        elseif ($scored.Skipped -gt 0 -or $guard.Skipped -gt 0) {
            $result = 'SKIPPED'
        }
        elseif ($guard.Passed -ne $guards) {
            $result = 'GUARD-BROKEN'
            $earned = [int][math]::Floor($base / 2)
        }
        elseif ($passed -eq $pinned) {
            $result = 'PASS'
            $earned = $worth
        }
        elseif ($passed -gt 0) {
            $result = 'PARTIAL'
            $earned = $base
        }
        else {
            $result = 'FAIL'
        }
    }

    if ($result -ne 'PASS') { $overall = 1 }
    $total += $earned
    $rows.Add(('{0,-6} {1,-13} {2,2} / {3,-4} {4,3} / {5}' -f $id, $result, $passed, $pinned, $earned, $worth))
}

Write-Host ''
Write-Host '================ SUMMARY ================'
Write-Host '       Result        Tests     Points'
foreach ($row in $rows) { Write-Host $row }
Write-Host ('{0,-6} {1,-13} {2,9} {3,3} / {4}' -f 'TOTAL', '', '', $total, $max)
Write-Host '========================================='

exit $overall
