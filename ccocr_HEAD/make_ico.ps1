# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   make_ico.ps1    260330  cy
#   PNG -> ICO 変換（256x256 PNG形式埋め込み）
#
#--------1---------2---------3---------4---------5---------6---------7--------#

Add-Type -AssemblyName System.Drawing

$workFld = Split-Path $MyInvocation.MyCommand.Path
$pngPath = Join-Path $workFld 'large.png'
$icoPath = Join-Path $workFld 'ccocr.ico'
$size    = 256

$src = [System.Drawing.Image]::FromFile($pngPath)
$bmp = New-Object System.Drawing.Bitmap($size, $size)
$g   = [System.Drawing.Graphics]::FromImage($bmp)
$g.DrawImage($src, 0, 0, $size, $size)
$g.Dispose()
$src.Dispose()

$ms       = New-Object System.IO.MemoryStream
$bmp.Save($ms, [System.Drawing.Imaging.ImageFormat]::Png)
$pngBytes = $ms.ToArray()
$ms.Close()
$bmp.Dispose()

$fs = [System.IO.File]::OpenWrite($icoPath)
$bw = New-Object System.IO.BinaryWriter($fs)
$bw.Write([uint16]0)
$bw.Write([uint16]1)
$bw.Write([uint16]1)
$bw.Write([byte]0)
$bw.Write([byte]0)
$bw.Write([byte]0)
$bw.Write([byte]0)
$bw.Write([uint16]1)
$bw.Write([uint16]32)
$bw.Write([uint32]$pngBytes.Length)
$bw.Write([uint32]22)
$bw.Write($pngBytes)
$bw.Close()
$fs.Close()

$size = (Get-Item $icoPath).Length
Write-Host "ccocr.ico saved: $size bytes"
