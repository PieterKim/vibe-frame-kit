param(
    [ValidateSet("project", "global")][string]$Scope = "project",
    [string]$Project = (Get-Location).Path,
    [switch]$DryRun,
    [switch]$MigrateLegacy
)
$ErrorActionPreference = "Stop"
$Installer = Join-Path $PSScriptRoot "install.py"
$InstallArgs = @($Installer, "--scope", $Scope, "--project", $Project)
if ($DryRun) { $InstallArgs += "--dry-run" }
if ($MigrateLegacy) { $InstallArgs += "--migrate-legacy" }
& python @InstallArgs
exit $LASTEXITCODE
