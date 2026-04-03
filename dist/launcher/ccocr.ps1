<#
    vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :

    ccocr.ps1       260403  cy
    launcher: version-aware install/upgrade, bundled Python/MinGit

    -------1---------2---------3---------4---------5---------6---------7--------
#>

Add-Type -AssemblyName System.Windows.Forms


$thisName   = 'ccocr'
$appVer     = 'v2.3.2'
$repoUrl    = 'https://github.com/weininfuwu/ccocr.git'
$sysFld     = Join-Path $env:LOCALAPPDATA 'ChuanlaiApps\ccocr'
$cfgMapFile = Join-Path $sysFld 'config_map.json'
$verFile    = Join-Path $sysFld 'ccocr_version.txt'

# ps2exe では $scriptDir / $MyInvocation が使えないためプロセスから取得
$exePath   = [System.Diagnostics.Process]::GetCurrentProcess().MainModule.FileName
$scriptDir = Split-Path $exePath -Parent

#------------------------------------------------------------
# helpers
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

function ParseVer($v) { [System.Version]($v -replace '^v','') }

#------------------------------------------------------------
# 1. インストール状態・バージョン確認
#------------------------------------------------------------
$isFirstRun   = -not (Test-Path (Join-Path $sysFld '.git'))
$installedVer = if (Test-Path $verFile) {
                    (Get-Content $verFile -Encoding UTF8).Trim()
                } else { 'v0.0.0' }

$srcPy  = Join-Path $scriptDir 'python'
$srcGit = Join-Path $scriptDir 'MinGit'
$dstPy  = Join-Path $sysFld   'dist\python'
$dstGit = Join-Path $sysFld   'dist\launcher\MinGit'

$needSetup = $isFirstRun
if (-not $isFirstRun) {
    $verCmp = (ParseVer $appVer).CompareTo((ParseVer $installedVer))

    if ($verCmp -lt 0) {
        # このexeは古い
        errmsg ("起動した ccocr.exe はバージョンが古いです。`n`n" +
                "他のフォルダにある最新のものを使うか、`n" +
                "再度 zip のダウンロードからお願いします。")
        exit
    }

    if ($verCmp -gt 0) {
        # アップグレード必要 — パーツが隣に揃っているか確認（何が変わったか不明なため全部必要）
        $needSetup  = $true
        $missingPy  = -not (Test-Path $srcPy)
        $missingGit = -not (Test-Path $srcGit)
        if ($missingPy -or $missingGit) {
            errmsg ("PCに保存されているパーツの更新が必要です。`n`n" +
                    "ccocr.exe`n設定エクセル`n処理する帳表`n" +
                    "の他に`n`n" +
                    "　MinGit フォルダ`n　Python フォルダ`n`n" +
                    "全部同じフォルダに入れて、再度動かしてください。")
            exit
        }
    }
}

#------------------------------------------------------------
# 2. 初回インストール（git clone）
#------------------------------------------------------------
if ($isFirstRun) {
    if (-not (Test-Path $srcGit)) {
        errmsg ("MinGit が見つかりません。`n`n" +
                "exe と同じフォルダに MinGit フォルダを置いてください。")
        exit
    }
    # 空フォルダが存在する場合は削除（git clone のため）
    if ((Test-Path $sysFld) -and
        (Get-ChildItem $sysFld -Force | Measure-Object).Count -eq 0) {
        Remove-Item $sysFld
    }
    $git      = Join-Path $srcGit 'cmd\git.exe'
    $cloneOut = & $git clone $repoUrl $sysFld 2>&1
    if ($LASTEXITCODE -ne 0) {
        errmsg ("git clone に失敗しました。`n`n" +
                "エラー詳細:`n" + ($cloneOut -join "`n"))
        exit
    }

    [System.Windows.Forms.MessageBox]::Show(
        "インストールが完了しました。",
        "$thisName $appVer",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Information
    ) | Out-Null
}

#------------------------------------------------------------
# 3. パーツコピー（初回 or アップグレード時のみ）
#------------------------------------------------------------
if ($needSetup) {
    # Python
    if (Test-Path $srcPy) {
        if (Test-Path $dstPy) { Remove-Item $dstPy -Recurse -Force }
        Copy-Item $srcPy $dstPy -Recurse
        Remove-Item $srcPy -Recurse -Force
    }
    # MinGit（初回はclone済みのrepo内MinGitを使うためコピー不要、削除のみ）
    if (Test-Path $srcGit) {
        if (-not $isFirstRun) {
            if (Test-Path $dstGit) { Remove-Item $dstGit -Recurse -Force }
            Copy-Item $srcGit $dstGit -Recurse
        }
        Remove-Item $srcGit -Recurse -Force
    }
    # バージョン記録
    Set-Content -Path $verFile -Value $appVer -Encoding UTF8
}

#------------------------------------------------------------
# 4. git pull
#------------------------------------------------------------
$appFld    = $sysFld
$gitInRepo = Join-Path $sysFld 'dist\launcher\MinGit\cmd\git.exe'
$gitLocal  = Join-Path $scriptDir 'MinGit\cmd\git.exe'
if     (Test-Path $gitInRepo) { $git = $gitInRepo }
elseif (Test-Path $gitLocal)  { $git = $gitLocal  }
else {
    errmsg "MinGit が見つかりません。"
    exit
}
& $git -C $sysFld remote set-url origin $repoUrl 2>&1 | Out-Null
& $git -C $sysFld pull 2>&1 | Out-Null

#------------------------------------------------------------
# 5. 設定 Excel の確認
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
# 5b. 開始ダイアログ
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
# 6. flowid (Python 互換のため exe 隣に隠しファイルで保持)
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
# 7. Python 確認
#------------------------------------------------------------
$codeFld   = Join-Path $appFld 'code'
$bundledPy = Join-Path $appFld 'dist\python\python.exe'
if (Test-Path $bundledPy) {
    $pyExe      = $bundledPy
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
# 8. モジュール確認 / インストール
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
# 9. main.py 起動
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
