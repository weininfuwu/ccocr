@echo off
rem  vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
rem
rem     ccocr_260105.bat    260105  cy
rem                         260303  cy ccocrSTANDALONE
rem
rem --------1---------2---------3---------4---------5---------6---------7--------#

powershell.exe -NoProfile -ExecutionPolicy RemoteSigned ^
    -Command "& '%~dp0ccocr_260303.ps1' *> '%~dp0ccocr_log.txt'"

