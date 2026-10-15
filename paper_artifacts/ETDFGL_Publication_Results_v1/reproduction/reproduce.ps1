# ETD-FGL Artifact Reproduction Script (PowerShell)
$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Resolve-Path "$ScriptDir\..\..\..\.."
Set-Location $ProjectRoot

Write-Host "Running ETD-FGL Complete Reproduction Pipeline..." -ForegroundColor Cyan
& .\.venv\Scripts\python.exe extract_and_consolidate_results.py
& .\.venv\Scripts\python.exe generate_publication_figures.py
& .\.venv\Scripts\python.exe build_publication_tables.py
& .\.venv\Scripts\python.exe build_manuscript_sections.py
& .\.venv\Scripts\python.exe paper_artifacts/ETDFGL_Publication_Results_v1/validation/validate_publication_package.py
Write-Host "Reproduction finished successfully!" -ForegroundColor Green
