# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   mymail.ps1      251030  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

Add-Type -AssemblyName System.DirectoryServices.AccountManagement
$mymail = [System.DirectoryServices.AccountManagement.UserPrincipal]::`
                                                        Current.EmailAddress
Write-Host -NoNewLine $mymail

