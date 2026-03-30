# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   ccocr.ps1       260330  cy
#   new launcher: AppData-based state, git clone/pull, config_map
#
#--------1---------2---------3---------4---------5---------6---------7--------#

Add-Type -AssemblyName System.Windows.Forms

$thisName   = 'ccocr'
$repoUrl    = 'https://github.com/ykawate1114/ccocr_with_claude'
$appDataDir = Join-Path $env:LOCALAPPDATA 'chuanlai_apps\ccocr'
$sysFldFile = Join-Path $appDataDir 'sysFld.txt'
$cfgMapFile = Join-Path $appDataDir 'config_map.json'
$exePath    = $MyInvocation.MyCommand.Path

New-Item -ItemType Directory -Path $appDataDir -Force | Out-Null

#------------------------------------------------------------
# errmsg helper
#------------------------------------------------------------
function errmsg($msg) {
    $f = New-Object Windows.Forms.Form
    $f.TopMost = $True
    [System.Windows.Forms.MessageBox]::Show(
        $f, "$msg", $thisName,
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Error
    ) | Out-Null
}

#------------------------------------------------------------
# 1. sysFld の確認 / 初回インストール
#------------------------------------------------------------
$sysFld = $null
if (Test-Path $sysFldFile) {
    $sysFld = (Get-Content $sysFldFile -Encoding UTF8).Trim()
    if (-not (Test-Path $sysFld)) { $sysFld = $null }
}

if ($null -eq $sysFld) {
    $dlg = New-Object System.Windows.Forms.FolderBrowserDialog
    $dlg.Description         = 'ccocr のインストール先フォルダを選択してください'
    $dlg.ShowNewFolderButton = $true
    if ($dlg.ShowDialog() -ne 'OK') { exit }
    $sysFld = Join-Path $dlg.SelectedPath 'ccocr'

    # git は exe 隣の MinGit を使う
    $git = Join-Path $PSScriptRoot 'MinGit\cmd\git.exe'
    if (-not (Test-Path $git)) {
        errmsg ("MinGit が見つかりません。`n`n" +
                "exe と同じフォルダに MinGit フォルダを置いてください。")
        exit
    }
    Write-Host "git clone $repoUrl"
    & $git clone $repoUrl $sysFld
    if ($LASTEXITCODE -ne 0) {
        errmsg ("git clone に失敗しました。`n`n" +
                "ネットワーク接続を確認してください。")
        exit
    }

    Set-Content -Path $sysFldFile -Value $sysFld -Encoding UTF8

    [System.Windows.Forms.MessageBox]::Show(
        ("インストールが完了しました。`n`n" +
         "exe と同じフォルダの MinGit フォルダは削除してかまいません。"),
        $thisName,
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Information
    ) | Out-Null
}

#------------------------------------------------------------
# 2. git pull (sysFld 内の MinGit を優先、なければ exe 隣)
#------------------------------------------------------------
$gitInRepo = Join-Path $sysFld 'MinGit\cmd\git.exe'
$gitLocal  = Join-Path $PSScriptRoot 'MinGit\cmd\git.exe'
if     (Test-Path $gitInRepo) { $git = $gitInRepo }
elseif (Test-Path $gitLocal)  { $git = $gitLocal  }
else {
    errmsg "MinGit が見つかりません。"
    exit
}
Write-Host "git pull"
& $git -C $sysFld pull

#------------------------------------------------------------
# 3. 設定 Excel の確認
#------------------------------------------------------------
$xlPath = $null
$cfgMap = @()
if (Test-Path $cfgMapFile) {
    $raw = Get-Content $cfgMapFile -Encoding UTF8 -Raw
    if ($raw) { $cfgMap = $raw | ConvertFrom-Json }
    if ($null -eq $cfgMap) { $cfgMap = @() }
}
# 配列に強制変換（1要素の場合 ConvertFrom-Json が object を返すため）
$cfgMap = @($cfgMap)

foreach ($entry in $cfgMap) {
    if ($entry.exe -eq $exePath) {
        if (Test-Path $entry.xl) { $xlPath = $entry.xl }
        break
    }
}

if ($null -eq $xlPath) {
    $dlg = New-Object System.Windows.Forms.OpenFileDialog
    $dlg.Title            = '設定 Excel ファイルを選択してください'
    $dlg.Filter           = 'Excel Files (*.xlsx;*.xlsm)|*.xlsx;*.xlsm'
    $dlg.InitialDirectory = $PSScriptRoot
    if ($dlg.ShowDialog() -ne 'OK') { exit }
    $xlPath = $dlg.FileName

    $newEntry = [PSCustomObject]@{ exe = $exePath; xl = $xlPath }
    $cfgMap  += $newEntry
    $cfgMap | ConvertTo-Json | Set-Content -Path $cfgMapFile -Encoding UTF8
}

#------------------------------------------------------------
# 4. flowid (Python 互換のため exe 隣に隠しファイルで保持)
#------------------------------------------------------------
$flowidFile = Join-Path $PSScriptRoot '.flowid'
if (Test-Path $flowidFile) {
    $flowid = (Get-Content $flowidFile -Encoding UTF8).Trim()
} else {
    $flowid = [guid]::NewGuid().ToString()
    Set-Content -Path $flowidFile -Value $flowid -Encoding UTF8
    (Get-Item $flowidFile).Attributes += 'Hidden'
}

#------------------------------------------------------------
# 5. Python 確認
#------------------------------------------------------------
$codeFld = Join-Path $sysFld 'code'
Set-Location $codeFld

try {
    $pyVer = python -V 2>&1
    if ($LASTEXITCODE -ne 0) { throw }
    Write-Host "Python: $pyVer"
} catch {
    errmsg ("Python が見つかりません。`n`n" +
            "Python をインストールしてから再度起動してください。`n" +
            "https://www.python.org/downloads/")
    exit
}

#------------------------------------------------------------
# 6. モジュール確認 / インストール
#------------------------------------------------------------
$pyModules = @("flask", "keyring", "numpy", "opencv-python", "openpyxl",
               "pandas", "pdf2image", "pillow", "requests", "selenium",
               "scikit-image", "sqlparse", "urllib3")

foreach ($module in $pyModules) {
    python ifHasModule.py $module
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installing $module..."
        pip config set global.trusted-host "pypi.org files.pythonhosted.org" | Out-Null
        pip install --user $module
        if ($LASTEXITCODE -ne 0) {
            errmsg ("モジュールのインストールに失敗しました。`n`n" +
                    "モジュール名: $module`n`n" +
                    "ネットワーク接続を確認して再度お試しください。")
            exit
        }
    }
    Write-Host "module ready: $module"
}

#------------------------------------------------------------
# 7. main.py 起動
#------------------------------------------------------------
python main.py $sysFld $flowid $thisName --config $xlPath
