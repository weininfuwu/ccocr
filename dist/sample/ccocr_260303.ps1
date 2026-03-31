# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   ccocr.ps1       251229  cy
#                   260303  cy  ccocrSTANDALONE
#   updated: 260320.111431 by cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#
###
###     change this line only for other project
###
$codeFld    = "${env:USERPROFILE}\DigNav\code\ccocr"

###
###     initial remote codte to run == init.ps1
###
Add-Type -AssemblyName System.Windows.Forms
#
#   get flow id
#
$flowidTxt = Join-Path $PSScriptRoot "flowid.txt"
if (Test-Path -LiteralPath $flowidTxt) {
    $flowid = (Get-Content -LiteralPath $flowidTxt -Encoding UTF8).Trim()
} else {
    $flowid = [guid]::NewGuid().ToString()
    $flowid | Out-File -FilePath $flowidTxt -Encoding utf8
    Set-ItemProperty -Path $flowidTxt -Name Attributes -Value (
                                        [System.IO.FileAttributes]::Hidden)
}
#
#   make flow dir
#
$flowd  = "${env:USERPROFILE}\DigNav\flows\$flowid"
New-Item -ItemType Directory -Path $flowd -Force > $null
#
#   get system dir (on Box)
#
$askSysFld = $true
$sysFLdFile = "$flowd\sysFld.txt"
if (Test-Path $sysFLdFile) {
    $sysFld = Get-Content $sysFLdFile -Raw
    $sysFLd = $sysFld.TrimEnd("`r", "`n")
    if(Test-Path $sysFld){
        $askSysFld = $false
    }
}
if ($askSysFld){
    while ($true){
        $dialg = New-Object System.Windows.Forms.FolderBrowserDialog
        $dialg.ShowNewFolderButton = $false
        $dialg.Description = "このアプリ用のシステムフォルダを選択してください"
        $rtn = $dialg.ShowDialog()
        if ($rtn -eq [System.Windows.Forms.DialogResult]::OK) {
            $sysFld = $dialg.SelectedPath
            Set-Content -Path "$flowd\sysFld.txt" -Value $sysFld -Encoding utf8
            break
        }
    }
}
#
#   robocopy code
#
robocopy "$sysFld\code" $codeFld /MIR /XD "__pycache__"
#
#   start (copied) remote code
#
$args = @(
    "-File"
    "`"$codeFld\init.ps1`""
    "`"$flowid`""
    "`"$sysFld`""
    "`"$codeFld`""
)
Start-Process powershell.exe -ArgumentList $args -WindowStyle Minimized
