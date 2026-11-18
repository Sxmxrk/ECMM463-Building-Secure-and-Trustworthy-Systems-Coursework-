param(
    [string]$OutputDir = 'results\verification_run'
)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Dataset = Join-Path $Root 'experiments\figshare_recovery_M08'
$Image = 'slikube-figshare-paper:2021'
if (-not (Test-Path -LiteralPath $Dataset -PathType Container)) {
    throw 'M08 dataset is missing; check the extracted package.'
}
if ([System.IO.Path]::IsPathRooted($OutputDir)) {
    $Out = $OutputDir
} else {
    $Out = Join-Path $Root $OutputDir
}
$OutputReport = Join-Path $Out 'figshare_M08_full20_per_file.csv'
if (Test-Path -LiteralPath $OutputReport) {
    throw "Completed verification report already exists: $OutputReport. Choose a new -OutputDir."
}
New-Item -ItemType Directory -Force -Path $Out | Out-Null
$Out = (Resolve-Path -LiteralPath $Out).Path
docker info *> $null
if ($LASTEXITCODE -ne 0) {
    throw 'Docker Engine is not available. Start Docker Desktop and retry.'
}
docker image inspect $Image *> $null
if ($LASTEXITCODE -ne 0) {
    docker build -t $Image (Join-Path $Root 'figshare_tool')
    if ($LASTEXITCODE -ne 0) { throw 'Failed to build paper-era scanner image.' }
}
Write-Host 'Scanning all 2,031 M08 manifests with the unchanged Figshare scanner...'
docker run --rm `
    -v "${Root}:/project:ro" `
    -v "${Out}:/results" `
    --entrypoint python `
    $Image /project/scripts/scan_M08_docker.py --root /project --out /results
if ($LASTEXITCODE -ne 0) { throw "Scanner exited with code $LASTEXITCODE." }
Write-Host "Verification results saved to: $Out"
Write-Host 'Original M01–M08 snapshots and published result files remain unchanged.'
