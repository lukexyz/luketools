# Project: luketools

> **Note:** Always run terminal commands through PowerShell (not bash).

---

## Profile Comparison

| # | Status | Feature | Home | Work |
|---|---|---|---|---|
| 1 | ✅ | **Oh My Posh** | `oh-my-posh init pwsh \| Invoke-Expression` (modern) | `oh-my-posh init pwsh \| Invoke-Expression` (modern) |
| 2 | ✅ | **Oh My Posh theme** | Paradox | Default (no theme specified) |
| 3 | ✅ | **Terminal-Icons** | Yes | Yes |
| 4 | ✅ | **posh-git** | Yes | No |
| 5 | ✅ | **Chocolatey autocomplete** | Yes | Yes |
| 6 | ✅ | **fnm (Node)** | Yes (`--use-on-cd`) | Yes (`--use-on-cd`) |
| 7 | ✅ | **fastfetch boot screen** | Yes (shared config) | Yes (custom config) |
| 8 | ✅ | **Python PATH** | Yes (miniforge3) | Yes (Python 3.12 + Scripts) |
| 9 | ✅ | **Python alias** | N/A (miniforge3) | Yes (`Set-Alias python`) |
| 10 | ✅ | **Claude Code PATH** | N/A (using opencode) | Yes (`~/.local/bin`) |
| 11 | ✅ | **Start directory** | `D:\Python` | `jet\` |
| 12 | ✅ | **Startup listing** | `Get-ChildItem` (sorted by date) | `dir` |
| 13 | ✅ | **Hotkey reminders** | Yes (echo'd) | No |
| 14 | ✅ | **Profile edit reminder** | Yes (`>code $PROFILE`) | Yes (`>code $PROFILE`) |

---

## PowerShell Profiles

### Home PC (`profile.ps1` — current file: `powershell/profile.ps1`)

```powershell
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
echo "-------------- AI TOOLS ----------------"
echo "> opencode    - Multi-model open-source agent"
echo "--------------- Hotkeys ----------------"
echo "split right: [alt] [shift] [=]"
echo "split below: [alt] [shift] [-]"
echo "resize:      [alt] [shift] [arrows]"
echo "navigation:  [alt] [arrows]"
echo "close pane:  [ctrl] [shift] [w]"
echo "----------------------------------------"
echo ""
echo "> code `$PROFILE - to edit this script"

# Aliases
Set-Alias which where.exe

# fnm (Node version manager)
if (Get-Command fnm -ErrorAction SilentlyContinue) {
    fnm env --use-on-cd --shell powershell | Out-String | Invoke-Expression
}

# Chocolatey Autocomplete
$ChocolateyProfile = "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
if (Test-Path($ChocolateyProfile)) {
  Import-Module "$ChocolateyProfile"
}
```

---

### Work PC (`powershell_profile.ps1`)

```powershell
# 1. Define the non-admin Chocolatey location
$env:ChocolateyInstall = "$env:LocalAppData\chocolatey"

# 2. Add the Chocolatey bin folder to the PATH for this session
$env:Path += ";$env:ChocolateyInstall\bin"

# 3. Add pip to PATH
$env:Path += ";C:\Program Files\Python312\Scripts"

# 4. Add python to PATH
$env:Path += ";C:\Program Files\Python312"
Set-Alias python "C:\Program Files\Python312\python.exe"

# 5. Initialize fnm (This links 'node', 'npm', and 'npx' to your session)
if (Get-Command fnm -ErrorAction SilentlyContinue) {
    fnm env --use-on-cd --shell powershell | Out-String | Invoke-Expression
}

# 5.1 Add Claude Code to PATH
$env:Path += ";C:\Users\LukeWoods\.local\bin"

# 6. Cool boot screen
fastfetch --config "C:\Users\LukeWoods\jet\luketools\my-fastfetch.jsonc"

# 7. Helpful reminder
Write-Host ""
Write-Host "   (Note: >code `$PROFILE   # to open powershell profile)"

# 8. Chocolatey Autocomplete
$ChocolateyProfile = "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
if (Test-Path($ChocolateyProfile)) {
  Import-Module "$ChocolateyProfile"
}

# 9. Initialize Oh My Posh
oh-my-posh init pwsh | Invoke-Expression
Import-Module Terminal-Icons

cd jet
dir
```
