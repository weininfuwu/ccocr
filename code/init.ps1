# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   init.ps1        251127  cy
#   ccocr(单独版)   251228  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

###################### CHANGE BLW FOR EACH APP ######################
$usePython  = $true
$pyModules  = @("flask", "keyring", "numpy", "opencv-python", "openpyxl",
                "pandas", "pdf2image", "pillow", "requests", "selenium",
                "scikit-image", "sqlparse", "urllib3")
    #
    #   install INSTALL_NAME    -> import IMPORT_NAME
    #
    #   install opencv-python   -> import cv2
    #   install pillow          -> import PIL
    #   install scikit-image    -> import skimage
###################### CHANGE ABV FOR EACH APP ######################
Add-Type -AssemblyName System.Windows.Forms
$flwid      = $Args[0]
$sysFLd     = $Args[1]
$codeFld    = $Args[2]
$thisName   = Split-Path $codeFld -Leaf
write-Host "$thisName init.ps1"
. "$PSScriptRoot\errmsg.ps1"
#
#   main
#
Set-Location $codeFld
$pwd = Get-Location
Write-Host "current woking dir: $pwd"
Write-Host "flwid $flwid"
Write-Host "sysFld $sysFld"
#
#   if use python
#
if($usePython){
    . "$PSScriptRoot\usepython.ps1"
}
#
#   kick program
#
Set-Content -Path "rerun.ps1" -Value `
    "python main.py `"$sysFld`" $flwid `"$thisName`"" -Encoding UTF8
python main.py `"$sysFld`" $flwid `"$thisName`"
