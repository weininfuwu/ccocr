# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   install_python.ps1
#
#--------1---------2---------3---------4---------5---------6---------7--------#

$url      = "https://www.python.org/ftp/python/3.11.2/" +
            "python-3.11.2-amd64.exe"
$md5      = "4331ca54d9eacdbe6e97d6ea63526e57"
$dwnldFld = Join-Path $env:USERPROFILE "Downloads"
$exeFile  = Join-Path $dwnldFld "DigNavPython.exe"

. "$PSScriptRoot\errmsg.ps1"

# cleanup
if (Test-Path -LiteralPath $exeFile) {
    Remove-Item -LiteralPath $exeFile -Force
}

# download & MD5 check
try {
    Invoke-WebRequest -Uri $url -OutFile $exeFile -UseBasicParsing
} catch {
    errmsg ("Python インストーラーのダウンロードに失敗しました。`n" +
            $_.Exception.Message)
    exit 1
}

$hash = Get-FileHash -Path $exeFile -Algorithm MD5
Write-Host ("MD5 " + $hash.Hash)

if ($hash.Hash -ne $md5) {
    errmsg ("ダウンロードしたファイルの MD5 が一致しません。`n" +
            "詳しい人に相談しましょう。。。")
    exit 1
} else {
    Write-Host "md5 check OK"
}

# install
Set-Location -LiteralPath $dwnldFld

$cmdArgs = @("/c",
  "DigNavPython.exe /quiet PrependPath=1 InstallAllUsers=1"
)

$proc = Start-Process -FilePath "cmd.exe" -ArgumentList $cmdArgs `
        -WindowStyle Minimized -Wait -PassThru

if ($proc.ExitCode -ne 0) {
    errmsg ("Python インストールが異常終了しました。`n" +
            "ExitCode: $($proc.ExitCode)")
    exit $proc.ExitCode
}

# cleanup installer
Remove-Item -LiteralPath $exeFile -Force
Write-Host "Python 3.11.2 のインストールが完了しました。"

