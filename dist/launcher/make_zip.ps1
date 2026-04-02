# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   make_zip.ps1    260402  cy
#   Build ccocr distribution ZIP
#   Run from: dist/launcher/
#
#--------1---------2---------3---------4---------5---------6---------7--------#

$launcherFld = Split-Path $MyInvocation.MyCommand.Path
$distFld     = Split-Path $launcherFld -Parent
$repoFld     = Split-Path $distFld     -Parent
$outZip      = Join-Path  $launcherFld 'ccocr.zip'

# 作業用一時フォルダ
$tmpFld  = Join-Path $env:TEMP 'ccocr_zip_tmp'
$pkgFld  = Join-Path $tmpFld   'ccocr'

if (Test-Path $tmpFld) { Remove-Item $tmpFld -Recurse -Force }
New-Item $pkgFld -ItemType Directory | Out-Null

# コピー
Copy-Item (Join-Path $launcherFld 'ccocr.exe')  $pkgFld
Copy-Item (Join-Path $launcherFld 'MinGit')      $pkgFld -Recurse
$pyFld = Join-Path $distFld 'python'
if (Test-Path $pyFld) { Copy-Item $pyFld $pkgFld -Recurse }
Copy-Item (Join-Path $distFld     'doc')         $pkgFld -Recurse
Copy-Item (Join-Path $distFld     'sample')      $pkgFld -Recurse
Copy-Item (Join-Path $distFld     'README.txt')  $pkgFld

# ZIP 作成
if (Test-Path $outZip) { Remove-Item $outZip }
Compress-Archive -Path $pkgFld -DestinationPath $outZip

# 後片付け
Remove-Item $tmpFld -Recurse -Force

$size = (Get-Item $outZip).Length
Write-Host "Done: ccocr.zip ($size bytes)"
