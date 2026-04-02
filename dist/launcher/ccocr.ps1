<#
    vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :

    ccocr.ps1       260331  cy
    launcher: AppData fixed install, git clone/pull, config_map

    -------1---------2---------3---------4---------5---------6---------7--------
#>

Add-Type -AssemblyName System.Windows.Forms


$thisName   = 'ccocr'
$appVer     = 'v2.2.11'
$repoUrl    = 'https://github.com/ykawase1114/ccocr.git'
$sysFld     = Join-Path $env:LOCALAPPDATA 'ChuanlaiApps\ccocr'
$cfgMapFile = Join-Path $sysFld 'config_map.json'

# ps2exe では $scriptDir / $MyInvocation が使えないためプロセスから取得
$exePath   = [System.Diagnostics.Process]::GetCurrentProcess().MainModule.FileName
$scriptDir = Split-Path $exePath -Parent

#------------------------------------------------------------
# errmsg helper
#------------------------------------------------------------
function errmsg($msg) {
    $f = New-Object Windows.Forms.Form
    $f.TopMost = $True
    [System.Windows.Forms.MessageBox]::Show(
        $f, "$msg", "$thisName $appVer",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Error
    ) | Out-Null
}

#------------------------------------------------------------
# 1. 初回インストール判定 (.git の有無)
#------------------------------------------------------------
$isFirstRun = -not (Test-Path (Join-Path $sysFld '.git'))

if ($isFirstRun) {
    $git = Join-Path $scriptDir 'MinGit\cmd\git.exe'
    if (-not (Test-Path $git)) {
        errmsg ("MinGit が見つかりません。`n`n" +
                "exe と同じフォルダに MinGit フォルダを置いてください。")
        exit
    }
    # 空フォルダが存在する場合は削除（git clone のため）
    if ((Test-Path $sysFld) -and
        (Get-ChildItem $sysFld -Force | Measure-Object).Count -eq 0) {
        Remove-Item $sysFld
    }
    $cloneOut = & $git clone $repoUrl $sysFld 2>&1
    if ($LASTEXITCODE -ne 0) {
        errmsg ("git clone に失敗しました。`n`n" +
                "エラー詳細:`n" + ($cloneOut -join "`n"))
        exit
    }
    # bundled python を AppData 配下にコピーして元フォルダを削除
    $srcPy = Join-Path $scriptDir 'python'
    $dstPy = Join-Path $sysFld   'dist\python'
    if ((Test-Path $srcPy) -and -not (Test-Path $dstPy)) {
        Copy-Item $srcPy $dstPy -Recurse
        Remove-Item $srcPy -Recurse -Force
    }

    # MinGit も不要になるため削除
    $localGit = Join-Path $scriptDir 'MinGit'
    if (Test-Path $localGit) { Remove-Item $localGit -Recurse -Force }

    [System.Windows.Forms.MessageBox]::Show(
        "インストールが完了しました。",
        "$thisName $appVer",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Information
    ) | Out-Null
}

#------------------------------------------------------------
# 2. git pull (sysFld 内の MinGit を優先、なければ exe 隣)
#------------------------------------------------------------
$appFld    = $sysFld                           # repo内の実コードroot
$gitInRepo = Join-Path $sysFld 'dist\launcher\MinGit\cmd\git.exe'
$gitLocal  = Join-Path $scriptDir 'MinGit\cmd\git.exe'
if     (Test-Path $gitInRepo) { $git = $gitInRepo }
elseif (Test-Path $gitLocal)  { $git = $gitLocal  }
else {
    errmsg "MinGit が見つかりません。"
    exit
}
& $git -C $sysFld pull 2>&1 | Out-Null

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

# 自分のエントリ（exe パス一致）から xl パスを取得
$myXl = $null
foreach ($entry in $cfgMap) {
    if ($entry.exe -eq $exePath) { $myXl = $entry.xl; break }
}

if ($myXl -ne $null -and (Test-Path $myXl) -and
    ((Split-Path $myXl -Parent) -eq $scriptDir)) {
    # xl が存在し、同フォルダ → そのまま使用
    $xlPath = $myXl
} else {
    # xl が存在しない／別フォルダ → エントリ削除してダイアログ
    if ($myXl -ne $null) {
        $cfgMap = @($cfgMap | Where-Object { $_.xl -ne $myXl })
        $cfgMap | ConvertTo-Json | Set-Content -Path $cfgMapFile -Encoding UTF8
    }
    while ($true) {
        $dlg = New-Object System.Windows.Forms.OpenFileDialog
        $dlg.Title            = '設定 Excel ファイルを選択してください（このフォルダ内限定です）'
        $dlg.Filter           = 'Excel Files (*.xlsx;*.xlsm)|*.xlsx;*.xlsm'
        $dlg.InitialDirectory = $scriptDir
        if ($dlg.ShowDialog() -ne 'OK') { exit }
        if ((Split-Path $dlg.FileName -Parent) -eq $scriptDir) {
            $xlPath = $dlg.FileName
            break
        }
        [System.Windows.Forms.MessageBox]::Show(
            "ccocr.exe と設定エクセルは同じフォルダに置いてください。",
            "$thisName $appVer",
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Warning
        ) | Out-Null
    }
    $newEntry = [PSCustomObject]@{ exe = $exePath; xl = $xlPath }
    $cfgMap  += $newEntry
    $cfgMap | ConvertTo-Json | Set-Content -Path $cfgMapFile -Encoding UTF8
}

#------------------------------------------------------------
# 3b. 開始ダイアログ
#------------------------------------------------------------
$r = [System.Windows.Forms.MessageBox]::Show(
    ("OCR処理を始めます。`n`n" +
     "しばらくすると、タスクバー（画面下端）に`n" +
     "ccocr のアイコンが出てきます。`n`n" +
     "「閉じる」ボタンで消すと、処理が止まりますので、`n" +
     "処理が終わるまで閉じないでください。"),
    "$thisName $appVer",
    [System.Windows.Forms.MessageBoxButtons]::OKCancel,
    [System.Windows.Forms.MessageBoxIcon]::Information
)
if ($r -ne [System.Windows.Forms.DialogResult]::OK) { exit }

#------------------------------------------------------------
# 4. flowid (Python 互換のため exe 隣に隠しファイルで保持)
#------------------------------------------------------------
$flowidFile = Join-Path $scriptDir '.flowid'
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
$codeFld   = Join-Path $appFld 'code'
$bundledPy = Join-Path $appFld 'dist\python\python.exe'
if (Test-Path $bundledPy) {
    $pyExe     = $bundledPy
    $useBundled = $true
} else {
    $pyExe      = 'python'
    $useBundled = $false
}
Set-Location $codeFld

if (-not $useBundled) {
    try {
        & $pyExe -V 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) { throw }
    } catch {
        errmsg ("Python が見つかりません。`n`n" +
                "Python をインストールしてから再度起動してください。`n" +
                "https://www.python.org/downloads/")
        exit
    }
}

#------------------------------------------------------------
# 6. モジュール確認 / インストール
#------------------------------------------------------------
if (-not $useBundled) {
    $pyModules = @("flask", "keyring", "numpy", "opencv-python", "openpyxl",
                   "pandas", "pdf2image", "pillow", "requests", "selenium",
                   "scikit-image", "sqlparse", "urllib3")

    foreach ($module in $pyModules) {
        & $pyExe ifHasModule.py $module 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) {
            pip config set global.trusted-host "pypi.org files.pythonhosted.org" 2>&1 | Out-Null
            pip install --user $module 2>&1 | Out-Null
            if ($LASTEXITCODE -ne 0) {
                errmsg ("モジュールのインストールに失敗しました。`n`n" +
                        "モジュール名: $module`n`n" +
                        "ネットワーク接続を確認して再度お試しください。")
                exit
            }
        }
    }
}

#------------------------------------------------------------
# 7. main.py 起動
#------------------------------------------------------------
$runExe = Join-Path $sysFld 'dist\launcher\ccocr_run.exe'
$proc = Start-Process $runExe `
    -ArgumentList "`"$appFld`" $flowid `"$thisName $appVer`" `"$xlPath`"" `
    -WindowStyle Minimized `
    -PassThru -Wait
if ($proc.ExitCode -ne 0) {
    $cfgMap = @($cfgMap | Where-Object { $_.exe -ne $exePath })
    $cfgMap | ConvertTo-Json | Set-Content -Path $cfgMapFile -Encoding UTF8
}
