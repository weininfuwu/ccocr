# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   mymail.ps1      251030  cy
#                   251229  cy deployed copilot code
#
#--------1---------2---------3---------4---------5---------6---------7--------#

#
#   original
#
#Add-Type -AssemblyName System.DirectoryServices.AccountManagement
#$mymail = [System.DirectoryServices.AccountManagement.UserPrincipal]::`
#                                                        Current.EmailAddress
#Write-Host -NoNewLine $mymail

#
#   copiliot
#
function Get-CurrentUserEmail {
  # 1) AD: UserPrincipal（EmailAddress / UPN）
  try {
    Add-Type -AssemblyName System.DirectoryServices.AccountManagement -ErrorAction Stop
    $up  = [System.DirectoryServices.AccountManagement.UserPrincipal]::Current
    if ($up -and $up.EmailAddress) { return $up.EmailAddress }
    if ($up -and $up.UserPrincipalName -and $up.UserPrincipalName -match '@') {
      # UPN が SMTP と同一ならそのまま返す
      return $up.UserPrincipalName
    }
  } catch { }

  # 2) AD: DirectorySearcher で mail / proxyAddresses を直接見る（オンプレAD想定）
  try {
    Add-Type -AssemblyName System.DirectoryServices -ErrorAction Stop
    $sid = [System.Security.Principal.WindowsIdentity]::GetCurrent().User.Value
    $ctx = New-Object System.DirectoryServices.ActiveDirectory.DirectoryContext('Domain')
    $dom = [System.DirectoryServices.ActiveDirectory.Domain]::GetDomain($ctx)
    $root = "LDAP://$($dom.Name)"
    $ds   = New-Object System.DirectoryServices.DirectorySearcher([System.DirectoryServices.DirectoryEntry]$root)
    $ds.Filter = "(objectSid=$sid)"
    $ds.PropertiesToLoad.AddRange(@('mail','proxyAddresses')) | Out-Null
    $res = $ds.FindOne()
    if ($res) {
      $mail = $res.Properties['mail'] | Select-Object -First 1
      if ($mail) { return $mail }
      $proxy = $res.Properties['proxyAddresses'] |
               Where-Object { $_ -like 'SMTP:*' } |
               ForEach-Object { $_ -replace '^SMTP:', '' } |
               Select-Object -First 1
      if ($proxy) { return $proxy }
    }
  } catch { }

  # 3) Microsoft Graph（Azure AD）：Mg モジュールが入っていて、ログイン済なら
  try {
    if (Get-Module -ListAvailable Microsoft.Graph.Users) {
      if (-not (Get-MgContext)) { Connect-MgGraph -Scopes 'User.Read' -ErrorAction Stop }
      $me = Get-MgUser -UserId 'me' -Property mail,userPrincipalName
      if ($me.mail) { return $me.mail }
      if ($me.userPrincipalName) { return $me.userPrincipalName }
    }
  } catch { }

  # 4) Outlook プロファイル（MAPI）：Outlook が使える端末なら
  try {
    $ol = New-Object -ComObject Outlook.Application
    $ns = $ol.Session
    # DisplayName は氏名のことが多いので、SMTP を優先
    $ex = $ns.CurrentUser.AddressEntry
    if ($ex -and $ex.Type -eq 'EX') {
      $smtp = $ex.GetExchangeUser().PrimarySmtpAddress
      if ($smtp) { return $smtp }
    }
    if ($ns.CurrentUser.Address -match '@') { return $ns.CurrentUser.Address }
  } catch { }

  # 5) 最後の手段：UPN（ドメイン\ユーザ → UPN へ）を推測して返す
  try {
    $name = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name  # DOMAIN\user
    $domain,$user = $name.Split('\',2)
    # ここは組織の UPN 既定ドメインに合わせて変更
#    $defaultSuffix = '@toyota-tsusho.com'  # 例
#    $defaultSuffix = '@DOMEIN.NOT.DETECTED'
    $defaultSuffix = "@$domain"
    if ($user) { return "$user$defaultSuffix" }
  } catch { }

  return $null
}

$mymail = Get-CurrentUserEmail
Write-Host -NoNewLine $mymail

