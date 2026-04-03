# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   make_exe.ps1    260331  cy
#   Build ccocr.exe from ccocr.ps1
#   Requirements: Windows PowerShell
#   Setup: Install-Module -Name ps2exe -Scope CurrentUser
#
#--------1---------2---------3---------4---------5---------6---------7--------#

$workFld    = Split-Path $MyInvocation.MyCommand.Path
$ps1Path    = Join-Path $workFld 'ccocr.ps1'
$exePath    = Join-Path $workFld 'ccocr.exe'
$runPs1Path = Join-Path $workFld 'ccocr_run.ps1'
$runExePath = Join-Path $workFld 'ccocr_run.exe'
$icoPath    = Join-Path $workFld 'ccocr.ico'

# ccocr.ps1 の $appVer からバージョン番号を取得
$verLine = Get-Content $ps1Path | Where-Object { $_ -match '^\$appVer\s*=' }
$exeVer  = ($verLine -replace ".*'v(.*)'.*", '$1')

# Install ps2exe if not available
if (-not (Get-Module -ListAvailable -Name ps2exe)) {
    Write-Host "Installing ps2exe..."
    Install-Module -Name ps2exe -Scope CurrentUser -Force
}

# Check icon file
if (-not (Test-Path $icoPath)) {
    Write-Host "ccocr.ico not found."
    Write-Host "  1. Place large.png (256x256 or larger) in dist/launcher/"
    Write-Host "  2. Run make_ico.ps1 to generate ccocr.ico"
    exit 1
}

Write-Host "Building: $exePath"
Invoke-ps2exe `
    -inputFile  $ps1Path `
    -outputFile $exePath `
    -iconFile   $icoPath `
    -title      'ccocr' `
    -version    $exeVer `
    -noConsole

if (Test-Path $exePath) {
    $size = (Get-Item $exePath).Length
    Write-Host "Done: ccocr.exe ($size bytes)"
} else {
    Write-Host "Build failed."
}

Write-Host "Building: $runExePath"
Invoke-ps2exe `
    -inputFile  $runPs1Path `
    -outputFile $runExePath `
    -iconFile   $icoPath `
    -title      'ccocr' `
    -version    $exeVer

if (Test-Path $runExePath) {
    $size = (Get-Item $runExePath).Length
    Write-Host "Done: ccocr_run.exe ($size bytes)"
} else {
    Write-Host "Build failed."
}
