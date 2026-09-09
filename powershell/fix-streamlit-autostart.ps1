<#
.SYNOPSIS
    Finds (and optionally removes) whatever is auto-starting a Streamlit app on boot.

.DESCRIPTION
    Streamlit was launching itself in a cmd.exe window at logon on port 8501.
    Windows has four common places that can do this:
      1. The per-user / all-users Startup folders
      2. Registry Run and RunOnce keys
      3. Task Scheduler tasks with a logon trigger
      4. A Windows service

    By default this script only reports what it finds. Nothing is changed until
    you re-run it with -Fix.

.PARAMETER Port
    Port the app listens on. Defaults to 8501 (Streamlit's default).

.PARAMETER Fix
    Actually remove the autostart entries and kill the running process.
    Startup-folder files are moved to a timestamped backup folder rather than
    deleted, and scheduled tasks are disabled rather than unregistered, so
    everything is recoverable.

.EXAMPLE
    .\fix-streamlit-autostart.ps1
    Report only. Shows what is running and what would be removed.

.EXAMPLE
    .\fix-streamlit-autostart.ps1 -Fix
    Kill the running app and remove the autostart entries.

.NOTES
    Run in an elevated PowerShell to see (and clean) HKLM keys and machine-wide
    scheduled tasks. Without elevation the HKCU and per-user results are still
    accurate, and those are the most likely culprits.
#>

[CmdletBinding()]
param(
    [int]$Port = 8501,
    [switch]$Fix
)

$ErrorActionPreference = 'Continue'

# Anything whose command line matches this is considered a suspect.
$Pattern = 'streamlit|app\.py|luketools'

$Backup  = Join-Path $env:USERPROFILE ("Desktop\startup-backup-{0}" -f (Get-Date -Format 'yyyyMMdd-HHmmss'))
$Found   = @()

function Write-Section($Text) {
    Write-Host ""
    Write-Host "=== $Text " -ForegroundColor Cyan -NoNewline
    Write-Host ("=" * [Math]::Max(0, 60 - $Text.Length)) -ForegroundColor Cyan
}

function Test-Elevated {
    $id = [Security.Principal.WindowsIdentity]::GetCurrent()
    (New-Object Security.Principal.WindowsPrincipal $id).IsInRole(
        [Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not (Test-Elevated)) {
    Write-Host "[!] Not running as Administrator - HKLM keys and machine-wide tasks may be hidden." -ForegroundColor Yellow
}

# ---------------------------------------------------------------------------
# 1. What is actually listening on the port right now
# ---------------------------------------------------------------------------
Write-Section "Running process on port $Port"

$listenerPids = @(
    Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty OwningProcess -Unique
)

if (-not $listenerPids) {
    Write-Host "Nothing is listening on port $Port right now." -ForegroundColor Yellow
    Write-Host "(If you already closed the window, the autostart entry below is still there.)"
} else {
    foreach ($procId in $listenerPids) {
        $proc = Get-CimInstance Win32_Process -Filter "ProcessId=$procId" -ErrorAction SilentlyContinue
        if (-not $proc) { continue }

        Write-Host "PID         : $($proc.ProcessId)"
        Write-Host "Name        : $($proc.Name)"
        Write-Host "CommandLine : $($proc.CommandLine)" -ForegroundColor Green

        # Walk up the parent chain - the launcher is usually 1-3 levels up.
        $parentId = $proc.ParentProcessId
        $depth    = 0
        while ($parentId -and $depth -lt 4) {
            $parent = Get-CimInstance Win32_Process -Filter "ProcessId=$parentId" -ErrorAction SilentlyContinue
            if (-not $parent) { break }
            Write-Host ("  ^ parent {0}: [{1}] {2}" -f $depth, $parent.ProcessId, $parent.Name)
            if ($parent.CommandLine) {
                Write-Host ("      {0}" -f $parent.CommandLine) -ForegroundColor DarkGray
            }
            $parentId = $parent.ParentProcessId
            $depth++
        }
    }
}

# ---------------------------------------------------------------------------
# 2. Startup folders
# ---------------------------------------------------------------------------
Write-Section "Startup folders"

$startupDirs = @(
    "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
    "$env:ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"
)

foreach ($dir in $startupDirs) {
    if (-not (Test-Path $dir)) { continue }
    Write-Host "-- $dir"

    Get-ChildItem $dir -File -ErrorAction SilentlyContinue | ForEach-Object {
        $file    = $_
        $details = ''

        if ($file.Extension -in '.bat', '.cmd', '.ps1', '.vbs') {
            $details = (Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue)
        } elseif ($file.Extension -eq '.lnk') {
            try {
                $link    = (New-Object -ComObject WScript.Shell).CreateShortcut($file.FullName)
                $details = "$($link.TargetPath) $($link.Arguments)"
            } catch { }
        }

        $isSuspect = ($file.Name -match $Pattern) -or ($details -match $Pattern)
        $colour    = if ($isSuspect) { 'Red' } else { 'Gray' }

        Write-Host ("   {0}" -f $file.Name) -ForegroundColor $colour
        if ($details) {
            Write-Host ("      {0}" -f ($details.Trim() -replace '\s+', ' ')) -ForegroundColor DarkGray
        }

        if ($isSuspect) {
            $script:Found += [pscustomobject]@{ Kind = 'StartupFile'; Name = $file.Name; Path = $file.FullName }
        }
    }
}

# ---------------------------------------------------------------------------
# 3. Registry Run keys
# ---------------------------------------------------------------------------
Write-Section "Registry Run keys"

$runKeys = @(
    'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
    'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce'
    'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
    'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce'
    'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run'
)

foreach ($key in $runKeys) {
    if (-not (Test-Path $key)) { continue }
    Write-Host "-- $key"

    (Get-ItemProperty $key).PSObject.Properties |
        Where-Object { $_.Name -notlike 'PS*' } |
        ForEach-Object {
            $isSuspect = ("$($_.Name) $($_.Value)" -match $Pattern)
            $colour    = if ($isSuspect) { 'Red' } else { 'Gray' }
            Write-Host ("   {0} = {1}" -f $_.Name, $_.Value) -ForegroundColor $colour

            if ($isSuspect) {
                $script:Found += [pscustomobject]@{ Kind = 'RegistryRun'; Name = $_.Name; Path = $key }
            }
        }
}

# ---------------------------------------------------------------------------
# 4. Scheduled tasks
# ---------------------------------------------------------------------------
Write-Section "Scheduled tasks"

Get-ScheduledTask -ErrorAction SilentlyContinue | ForEach-Object {
    $task = $_
    $cmd  = ($task.Actions | ForEach-Object { "$($_.Execute) $($_.Arguments)" }) -join ' ; '

    if ($cmd -match $Pattern) {
        Write-Host ("   {0}{1}  [{2}]" -f $task.TaskPath, $task.TaskName, $task.State) -ForegroundColor Red
        Write-Host ("      {0}" -f $cmd.Trim()) -ForegroundColor DarkGray
        $script:Found += [pscustomobject]@{
            Kind = 'ScheduledTask'; Name = $task.TaskName; Path = $task.TaskPath
        }
    }
}

# ---------------------------------------------------------------------------
# 5. Services
# ---------------------------------------------------------------------------
Write-Section "Services"

Get-CimInstance Win32_Service -ErrorAction SilentlyContinue |
    Where-Object { $_.PathName -match $Pattern } |
    ForEach-Object {
        Write-Host ("   {0}  [{1}/{2}]" -f $_.Name, $_.State, $_.StartMode) -ForegroundColor Red
        Write-Host ("      {0}" -f $_.PathName) -ForegroundColor DarkGray
        $script:Found += [pscustomobject]@{ Kind = 'Service'; Name = $_.Name; Path = $_.PathName }
    }

# ---------------------------------------------------------------------------
# Summary / fix
# ---------------------------------------------------------------------------
Write-Section "Summary"

if (-not $Found) {
    Write-Host "No autostart entry matched /$Pattern/." -ForegroundColor Yellow
    Write-Host "Widen the search and re-run, e.g. edit `$Pattern, or check the parent"
    Write-Host "process command line printed in section 1 for the path to look for."
    return
}

$Found | Format-Table Kind, Name, Path -AutoSize

if (-not $Fix) {
    Write-Host "Report only. Re-run with -Fix to remove these and kill the running app:" -ForegroundColor Yellow
    Write-Host "    .\fix-streamlit-autostart.ps1 -Fix" -ForegroundColor Yellow
    return
}

Write-Host "Applying fixes..." -ForegroundColor Magenta

foreach ($procId in $listenerPids) {
    Write-Host "   Stopping PID $procId"
    Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue
}

foreach ($item in $Found) {
    switch ($item.Kind) {
        'StartupFile' {
            if (-not (Test-Path $Backup)) { New-Item -ItemType Directory -Path $Backup -Force | Out-Null }
            Write-Host "   Moving $($item.Path) -> $Backup"
            Move-Item -LiteralPath $item.Path -Destination $Backup -Force
        }
        'RegistryRun' {
            Write-Host "   Removing $($item.Path)\$($item.Name)"
            Remove-ItemProperty -Path $item.Path -Name $item.Name -Force -ErrorAction Continue
        }
        'ScheduledTask' {
            Write-Host "   Disabling task $($item.Path)$($item.Name)"
            Disable-ScheduledTask -TaskName $item.Name -TaskPath $item.Path -ErrorAction Continue | Out-Null
        }
        'Service' {
            Write-Host "   Disabling service $($item.Name)"
            Stop-Service  -Name $item.Name -Force -ErrorAction Continue
            Set-Service   -Name $item.Name -StartupType Disabled -ErrorAction Continue
        }
    }
}

Write-Host ""
Write-Host "Done. Reboot to confirm it stays gone." -ForegroundColor Green
if (Test-Path $Backup) {
    Write-Host "Startup files backed up to: $Backup" -ForegroundColor Green
}
