param(
    [switch]$ValidateOnly,
    [switch]$SkipSetup
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path -LiteralPath $PSScriptRoot).Path
$skillRoot = Join-Path $repoRoot 'skills\chc-seo'
$runtime = Join-Path $skillRoot 'scripts\runtime.py'
$pluginManifest = Join-Path $repoRoot '.claude-plugin\plugin.json'
$marketplaceManifest = Join-Path $repoRoot '.claude-plugin\marketplace.json'

foreach ($required in @((Join-Path $skillRoot 'SKILL.md'), $runtime, $pluginManifest, $marketplaceManifest)) {
    if (-not (Test-Path -LiteralPath $required -PathType Leaf)) {
        throw "CHC SEO is incomplete: $required"
    }
}

$claude = Get-Command claude.cmd, claude -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $claude) {
    throw 'Claude Code CLI is required. Install Claude Code, then run this script again.'
}

Write-Host 'Validating CHC Technology SEO plugin...'
& $claude.Source plugin validate $repoRoot
if ($LASTEXITCODE -ne 0) { throw 'Claude plugin validation failed.' }
if ($ValidateOnly) {
    Write-Host 'Validation completed. No plugin or runtime was installed.'
    return
}

Write-Host 'Installing CHC Technology SEO from this repository...'
& $claude.Source plugin install chc-technology-seo --marketplace $repoRoot
if ($LASTEXITCODE -ne 0) { throw 'Claude plugin installation failed.' }

if (-not $SkipSetup) {
    $pythonCandidates = @()
    if ($env:CHC_SEO_PYTHON) {
        $pythonCandidates += @{ Exe = $env:CHC_SEO_PYTHON; Args = @() }
    } else {
        $pythonCandidates += @{ Exe = 'py'; Args = @('-3') }
        $pythonCandidates += @{ Exe = 'python3'; Args = @() }
        $pythonCandidates += @{ Exe = 'python'; Args = @() }
    }
    $python = $null
    foreach ($candidate in $pythonCandidates) {
        if (-not (Get-Command $candidate.Exe -ErrorAction SilentlyContinue)) { continue }
        $version = & $candidate.Exe @($candidate.Args + @('-c', 'import sys; print(sys.version_info.major, sys.version_info.minor)')) 2>$null
        if ($LASTEXITCODE -ne 0) { continue }
        if ($version -match '^3 (11|12|13|14)$') {
            $python = $candidate
            break
        }
    }
    if (-not $python) {
        throw 'Plugin installed, but Python 3.11-3.14 was not found. Install a supported Python and run scripts/runtime.py setup.'
    }
    Write-Host 'Setting up CHC SEO Python runtime...'
    & $python.Exe @($python.Args + @($runtime, 'setup'))
    if ($LASTEXITCODE -notin @(0, 10)) { throw 'CHC SEO runtime setup failed.' }
    if ($LASTEXITCODE -eq 10) { Write-Warning 'Python setup completed; Chromium setup still needs attention.' }
}

Write-Host 'CHC Technology SEO is installed. Start a new Claude Code session and use /chc-technology-seo:chc-seo.'
