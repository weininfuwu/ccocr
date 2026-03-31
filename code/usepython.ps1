# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   usepython.ps1       251127  cy
#                       251229  cy deployed use of importlib.metadata
#
#--------1---------2---------3---------4---------5---------6---------7--------#

#
#   if has python
#
try {
    $pythonVersion = python -V 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Host "Python version: $pythonVersion"
    $hasPython = $true
}
catch {
    $hasPython = $false
}
Write-Host "hasPython $hasPython"
#
#   install python if needed
#
if ($hasPython -eq $false) {
    errmsg (@"
pythonが入っていないようですので
今からインストールを行います。

ちょっと時間かかりますm(_ _)m
"@)
    Write-Host "installing python"
    . "$PSScriptRoot\install_python.ps1"
    errmsg (@"
pythonのインストールができたはずです。

ただし、今のままだとプログラムから python が
見えないので、ここで１回プログラムを終わります。

再度、プログラムを起動してください m(_ _)m
"@)
    exit
}
Write-Host "python installed"
#
#   if has python module
#
foreach ($module in $pyModules) {
    # check module with install name (pip install INSTALL_NAME)
    python ifHasModule.py $module
    $hasModule = ($LASTEXITCODE -eq 0)
    if (-not $hasModule) {
        Write-Host "Installing $module..."
        # 251215 against Osaka issue
        pip config set global.trusted-host "pypi.org files.pythonhosted.org"
        pip install --user $module
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Failed to install $module" -ForegroundColor Red
            errmsg (@"
python モジュールのインストールに失敗しました。

失敗したモジュールの配布名 $module

ネットワーク接続に問題があるとか、
まだ他に使った人が少ないなら
プログラムを書いた人が
配布名と import 名を取り違えてるとか、
かもです。

プログラムはここで終了します。
再度試してもダメの場合は、偉い人に相談しましょう。
"@)
            throw   ## exit DONESN'T WORK
        }
        # check again
        python ifHasModule.py $module
        $hasModule = ($LASTEXITCODE -eq 0)
        if (-not $hasModule) {
            Write-Host "Still missing: $module" -ForegroundColor Yellow
            continue
        }
    }
    Write-Host "module ready: $module"
}
