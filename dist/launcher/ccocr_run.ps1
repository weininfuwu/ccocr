<#
    vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :

    ccocr_run.ps1   260402  cy
    python launcher with ccocr icon (called from ccocr.exe)
    args: appFld flowid thisName xlPath
#>

$appFld   = $args[0]
$flowid   = $args[1]
$thisName = $args[2]
$xlPath   = $args[3]
$codeFld  = Join-Path $appFld 'code'

# bundled python を優先、なければシステム python
$bundledPy = Join-Path $appFld 'dist\python\python.exe'
if (Test-Path $bundledPy) { $pyExe = $bundledPy } else { $pyExe = 'python' }

$env:PYTHONIOENCODING = 'utf-8'
Set-Location $codeFld
& $pyExe -u main.py "$appFld" $flowid "$thisName" --config "$xlPath"
exit $LASTEXITCODE
