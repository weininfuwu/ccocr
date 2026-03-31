# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   errmsg.ps1      251120  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#

function errmsg($msg){
    if ($m -ne $true){
        $f = New-Object Windows.Forms.Form
        $f.TopMost = $True
        [System.Windows.Forms.MessageBox]::Show(
            $f                                              ,
            "$msg"                                          ,
            "$thisName"                                     ,
            [System.Windows.Forms.MessageBoxButtons]::OK    ,
            [System.Windows.Forms.MessageBoxIcon]::Error
        )
    }
}
