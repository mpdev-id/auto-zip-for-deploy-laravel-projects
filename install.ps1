# Laravel Deploy Packager Installer
# Jalankan sebagai Administrator

$installDir = "C:\Tools\LaravelDeploy"
$regFile = "$env:TEMP\laravel_deploy_context.reg"

Write-Host "=== Laravel Deploy Packager Installer ===" -ForegroundColor Cyan

# Buat direktori
if (!(Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir -Force | Out-Null
    Write-Host "Created directory: $installDir" -ForegroundColor Green
}

# Copy files (asumsi file berada di direktori yang sama dengan install.ps1)
$sourceDir = $PSScriptRoot

Copy-Item "$sourceDir\laravel_deploy.py" $installDir -Force
Copy-Item "$sourceDir\laravel_deploy.bat" $installDir -Force

Write-Host "Files copied to $installDir" -ForegroundColor Green

# Update path di batch file
$batchContent = Get-Content "$installDir\laravel_deploy.bat" -Raw
$batchContent = $batchContent -replace 'set "SCRIPT_PATH=C:\\Tools\\laravel_deploy.py"', "set `"SCRIPT_PATH=$installDir\laravel_deploy.py`""
Set-Content "$installDir\laravel_deploy.bat" $batchContent

# Buat registry file dengan path yang benar
$regContent = @"
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\Directory\shell\LaravelDeploy]
@="🚀 Deploy Laravel Project"
"Icon"="C:\\Windows\\System32\\shell32.dll,14"

[HKEY_CLASSES_ROOT\Directory\shell\LaravelDeploy\command]
@="\\`"$installDir\laravel_deploy.bat\\`" \`"%V\\`""

[HKEY_CLASSES_ROOT\Directory\Background\shell\LaravelDeploy]
@="🚀 Deploy Laravel Project"
"Icon"="C:\\Windows\\System32\\shell32.dll,14"

[HKEY_CLASSES_ROOT\Directory\Background\shell\LaravelDeploy\command]
@="\\`"$installDir\laravel_deploy.bat\\`" \`"%V\\`""
"@

Set-Content -Path $regFile -Value $regContent -Encoding ASCII

Write-Host "`nInstalling context menu..." -ForegroundColor Yellow
Start-Process regedit.exe -ArgumentList "/s `"$regFile`"" -Wait

Write-Host "`n✅ Installation Complete!" -ForegroundColor Green
Write-Host "Cara pakai:" -ForegroundColor Cyan
Write-Host "1. Klik kanan folder Laravel project" 
Write-Host "2. Pilih '🚀 Deploy Laravel Project'"
Write-Host "3. Pilih Preview atau Create ZIP"

Remove-Item $regFile -Force

pause