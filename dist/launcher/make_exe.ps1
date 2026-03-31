# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   make_exe.ps1    260331  cy
#   ccocr.ps1 から ccocr.exe を生成する
#   実行環境: Windows PowerShell
#   事前準備: Install-Module -Name ps2exe -Scope CurrentUser
#
#--------1---------2---------3---------4---------5---------6---------7--------#

$workFld = Split-Path $MyInvocation.MyCommand.Path
$ps1Path = Join-Path $workFld 'ccocr.ps1'
$exePath = Join-Path $workFld 'ccocr.exe'
$icoPath = Join-Path $workFld 'ccocr.ico'

# ps2exe が未インストールの場合はインストール
if (-not (Get-Module -ListAvailable -Name ps2exe)) {
    Write-Host "ps2exe をインストールしています..."
    Install-Module -Name ps2exe -Scope CurrentUser -Force
}

# アイコンファイルが存在しない場合は make_ico.ps1 を実行
if (-not (Test-Path $icoPath)) {
    Write-Host "ccocr.ico が見つかりません。make_ico.ps1 を実行してください。"
    Write-Host "  1. dist/launcher/ に large.png (256x256以上) を置く"
    Write-Host "  2. make_ico.ps1 を実行して ccocr.ico を生成する"
    exit 1
}

Write-Host "exe を生成しています: $exePath"
Invoke-ps2exe `
    -inputFile  $ps1Path `
    -outputFile $exePath `
    -iconFile   $icoPath `
    -title      'ccocr' `
    -version    '2.0.8' `
    -noConsole:$false

if ($LASTEXITCODE -eq 0) {
    $size = (Get-Item $exePath).Length
    Write-Host "完了: ccocr.exe ($size bytes)"
} else {
    Write-Host "エラーが発生しました。"
}
