# vim: set ts=4 sw=4 sts=4 et ff=unix fenc=utf-8 ai :
#
#   toys_askFld.ps1     251225  cy
#
#--------1---------2---------3---------4---------5---------6---------7--------#


param(
    # 第1引数: フォルダ選択ダイアログに表示する説明文（Description）
    [Parameter(Mandatory = $true)]
    [string]$Description,

    # 第2引数: BOMなしUTF-8のテキストファイル（最初の非空行を defaultPath として読む）※オプション
    [Parameter(Mandatory = $false)]
    [string]$DefaultPathFile
)

# アセンブリ読み込み
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# --- デスクトップパス ---
$rootSpecialFolder   = [System.Environment+SpecialFolder]::Desktop
$desktopPhysicalPath = [System.Environment]::GetFolderPath($rootSpecialFolder)

# --- テキストファイルから defaultPath を読み込む ---
function Get-DefaultPathFromFile {
    param([string]$PathFile)

    if ([string]::IsNullOrWhiteSpace($PathFile)) {
        return $null
    }
    if (-not (Test-Path -LiteralPath $PathFile)) {
        Write-Warning "指定された defaultPath ファイルが見つかりません: $PathFile"
        return $null
    }

    # BOMなしUTF-8で読み込み（PS5）
    $lines = Get-Content -LiteralPath $PathFile -Encoding utf8
    foreach ($line in $lines) {
        $t = $line.Trim()
        if (-not [string]::IsNullOrWhiteSpace($t)) {
            return $t
        }
    }

    Write-Warning "defaultPath ファイルに有効なパスが見つかりません: $PathFile"
    return $null
}

# --- 最も長い既存パスに解決（C以外は存在しない扱いだが、Cの場合は親を確実に辿る） ---
function Resolve-ExistingDefaultPath {
    param([string]$Path)

    if ([string]::IsNullOrWhiteSpace($Path)) {
        return $desktopPhysicalPath
    }

    $probe = $Path.TrimEnd('\')

    # ドライブ判定
    $m = [regex]::Match($probe, '^(?<drive>[A-Za-z]):\\')
    if (-not $m.Success) {
        return $desktopPhysicalPath
    }
    $drive = $m.Groups['drive'].Value.ToUpper()
    if ($drive -ne 'C') {
        return 'C:\'
    }

    # 既存ならそのまま
    if ([System.IO.Directory]::Exists($probe)) {
        return $probe
    }

    # 親を辿る
    while ($true) {
        $parent = Split-Path -Path $probe -Parent   # ← 修正済み
        if ([string]::IsNullOrWhiteSpace($parent) -or $parent -eq $probe) {
            break
        }
        if ([System.IO.Directory]::Exists($parent)) {
            return $parent
        }
        $probe = $parent
    }

    return 'C:\'
}

# --- defaultPath を取得（無効ならデスクトップに） ---
$defaultPathRaw = $null
if (-not [string]::IsNullOrWhiteSpace($DefaultPathFile)) {
    $defaultPathRaw = Get-DefaultPathFromFile -PathFile $DefaultPathFile
}
if ([string]::IsNullOrWhiteSpace($defaultPathRaw)) {
    $defaultPathRaw = $desktopPhysicalPath
}

# --- 最初に選択されるパスを決定 ---
$initialSelected = Resolve-ExistingDefaultPath -Path $defaultPathRaw

while ($true) {
    # 最前面オーナーフォーム
    $owner = New-Object System.Windows.Forms.Form
    $owner.ShowInTaskbar   = $false
    $owner.StartPosition   = [System.Windows.Forms.FormStartPosition]::CenterScreen
    $owner.Size            = New-Object System.Drawing.Size(0,0)
    $owner.TopMost         = $true
    $owner.FormBorderStyle = [System.Windows.Forms.FormBorderStyle]::FixedToolWindow
    $owner.Opacity         = 0.0
    $owner.Show()
    $owner.Activate()
    $owner.BringToFront()

    try {
        $dialog = New-Object System.Windows.Forms.FolderBrowserDialog
        $dialog.Description          = $Description
        $dialog.ShowNewFolderButton  = $false
        $dialog.RootFolder           = $rootSpecialFolder

        # 最初の選択
        if ([System.IO.Directory]::Exists($initialSelected)) {
            $dialog.SelectedPath = $initialSelected
        } else {
            # 念のため、ここでもデスクトップへ
            $dialog.SelectedPath = $desktopPhysicalPath
        }

        $result = $dialog.ShowDialog($owner)

        if ($result -eq [System.Windows.Forms.DialogResult]::OK) {
            # 選択したパスを表示
            Write-Host $dialog.SelectedPath

            # ★ DefaultPathFile が指定されていれば上書き保存（BOMなしUTF-8）
            if (-not [string]::IsNullOrWhiteSpace($DefaultPathFile)) {
                try {
                    Set-Content -LiteralPath $DefaultPathFile -Value $dialog.SelectedPath -Encoding utf8
                } catch {
                    Write-Warning "defaultPath ファイルへの保存に失敗しました: $DefaultPathFile"
                }
            }
            break
        }
        # キャンセルの場合は while により再表示
    }
    finally {
        $owner.Close()
        $owner.Dispose()
    }
}

