# Location: > $profile
# Edit:     > nano $profile
# Reload:   > . $profile

Import-Module posh-git
Import-Module oh-my-posh
Set-PoshPrompt Paradox # using Get-PoshThemes
# oh-my-posh --init --shell pwsh --config "~/jandedobbeleer.omp.json" | Invoke-Expression

Import-Module -Name Terminal-Icons

cd C:\python\
ls
echo "hotkeys"
echo "split right using alt shift ="
echo "split below using alt shift -"
echo "resize panes alt shift + arrows"
echo "jump between panes using [alt] + arrows"
echo "close with ctrl shift w"
