# Import Git and Icon modules
Import-Module posh-git
Import-Module -Name Terminal-Icons

# Initialize Oh My Posh with the Paradox theme (Modern Syntax)
oh-my-posh init pwsh --config "https://raw.githubusercontent.com/JanDeDobbeleer/oh-my-posh/main/themes/paradox.omp.json" | Invoke-Expression

# fastfetch boot screen
if (Get-Command fastfetch -ErrorAction SilentlyContinue) {
    fastfetch --config "D:\python\luketools\my-fastfetch.jsonc"
}

# Navigate to your coding directory
cd D:\Python
Get-ChildItem | Sort-Object LastWriteTime -Descending | Select-Object -First 15


# Print your custom hotkey reminders
echo ""
echo "--------------- Hotkeys ----------------"
echo "split right: [alt] [shift] [=]"
echo "split below: [alt] [shift] [-]"
echo "resize:      [alt] [shift] [arrows]"
echo "navigation:  [alt] [arrows]"
echo "close pane:  [ctrl] [shift] [w]"
echo "----------------------------------------"
echo ""

echo ""
echo "-------------- AI TOOLS ----------------"
Write-Host "> opencode     - TUI" -ForegroundColor Magenta
Write-Host "> opencode web - Web UI"
echo ""
Write-Host "> openclaw     - OpenClaw TUI" -ForegroundColor Magenta
Write-Host "> openclaw web - Open Claw dashboard"
Write-Host "> openclaw ws  - Open workspace in VS Code"
echo ""
Write-Host "> " -NoNewline; Write-Host "profile" -NoNewline -ForegroundColor Magenta; Write-Host " - Edit your PS1 (luketools/powershell/profile.ps1)"

function Start-OpenClawServices {
    Write-Host "[*] Checking gateway..." -ForegroundColor Cyan
    npx.cmd openclaw gateway health 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[*] Starting gateway..." -ForegroundColor Cyan
        npx.cmd openclaw gateway start 2>$null
        Start-Sleep -Seconds 2
    } else {
        Write-Host "[*] Gateway already running 🦞" -ForegroundColor Green
    }
    Write-Host "[*] Ready 🦞" -ForegroundColor Green
}

function openclaw {
    if ($args.Count -eq 0) {
        Start-OpenClawServices
        npx.cmd openclaw tui
    }
    elseif ($args[0] -eq "web") {
        Start-OpenClawServices
        npx.cmd openclaw dashboard
    }
    elseif ($args[0] -eq "ws") {
        code "C:\Users\luked\.openclaw\workspace"
    }
    else {
        npx.cmd openclaw $args
    }
}

# The emergency kill switch
function Stop-OpenClaw {
    Write-Host "[X] Killing all OpenClaw Node processes..." -ForegroundColor Red
    Stop-Process -Name "node" -ErrorAction SilentlyContinue
}

# Aliases
Set-Alias which where.exe
Set-Alias py python
function soul { code "C:\Users\luked\.openclaw\workspace\SOUL.md" }
function profile { code "D:\Python\luketools\powershell\profile.ps1" }

# fnm (Node version manager)
if (Get-Command fnm -ErrorAction SilentlyContinue) {
    fnm env --use-on-cd --shell powershell | Out-String | Invoke-Expression
}

# 8. Chocolatey Autocomplete
$ChocolateyProfile = "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
if (Test-Path($ChocolateyProfile)) {
  Import-Module "$ChocolateyProfile"
}
