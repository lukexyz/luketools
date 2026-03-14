# Location: > $profile
# Edit:     > code $profile
# Reload:   > . $profile

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
