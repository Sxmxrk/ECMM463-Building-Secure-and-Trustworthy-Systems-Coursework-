$ErrorActionPreference = "Stop"

function Assert-LastExitCode {
    param(
        [string]$Step
    )
    if ($LASTEXITCODE -ne 0) {
        throw "$Step failed with exit code $LASTEXITCODE."
    }
}

$Commit = "ff7fc804f5c02e9b0a279790294350869663b4e2"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Work = Join-Path $Root "vendor"
$Repo = Join-Path $Work "KubeSec"
$Controlled = (Resolve-Path (Join-Path $Root "experiments\controlled")).Path
$ResultsCsv = Join-Path $Controlled "slikube_results.csv"
$Sarif = Join-Path $Controlled "SLIKUBE.sarif"
$Summary = Join-Path $Root "results\controlled_summary.csv"

Write-Host "Checking Docker engine..."
docker info *> $null
if ($LASTEXITCODE -ne 0) {
    throw @"
Docker is installed but the Docker engine is not reachable.

Start Docker Desktop and wait until it reports that the engine is running.
Then verify with:
    docker info

After that, rerun:
    .\scripts\run_controlled.ps1
"@
}

New-Item -ItemType Directory -Force -Path $Work | Out-Null

if (-not (Test-Path (Join-Path $Repo ".git"))) {
    Write-Host "Cloning KubeSec..."
    git clone https://github.com/paser-group/KubeSec.git $Repo
    Assert-LastExitCode "git clone"
}

Push-Location $Repo
try {
    Write-Host "Checking out pinned SLI-KUBE commit..."
    git fetch --all --tags
    Assert-LastExitCode "git fetch"

    git checkout $Commit
    Assert-LastExitCode "git checkout"

    # Ensure every run starts from the exact pinned upstream source, even if the
    # previous reproduction run patched main.py in-place.
    git reset --hard $Commit
    Assert-LastExitCode "git reset --hard"

    Write-Host "Applying documented reproduction patch..."
    python (Join-Path $Root "patches\apply_repro_patch.py") $Repo
    Assert-LastExitCode "reproduction patch"

    Write-Host "Building Docker image..."
    docker build -f Dockerfile.repro -t "slikube-repro:$($Commit.Substring(0,8))" .
    Assert-LastExitCode "docker build"

    Write-Host "Running controlled SLI-KUBE scan..."
    docker run --rm -v "${Controlled}:/iac" "slikube-repro:$($Commit.Substring(0,8))" /iac
    Assert-LastExitCode "docker run"
}
finally {
    Pop-Location
}

if (-not (Test-Path $ResultsCsv)) {
    throw "SLI-KUBE finished without producing expected CSV: $ResultsCsv"
}

if (-not (Test-Path $Sarif)) {
    throw "SLI-KUBE finished without producing expected SARIF: $Sarif"
}

Write-Host "Analysing controlled results..."
python (Join-Path $Root "scripts\analyze_results.py") `
    $ResultsCsv `
    --expectations (Join-Path $Root "experiments\controlled_expectations.csv") `
    --out $Summary
Assert-LastExitCode "result analysis"

if (-not (Test-Path $Summary)) {
    throw "Analysis finished without producing expected summary: $Summary"
}

Write-Host ""
Write-Host "Controlled reproduction complete."
Write-Host "CSV:   $ResultsCsv"
Write-Host "SARIF: $Sarif"
Write-Host "Check: $Summary"
