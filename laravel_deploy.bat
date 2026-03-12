@echo off
chcp 65001 >nul
title Laravel Deploy Packager

:: Path ke python script (sesuaikan!)
set "SCRIPT_PATH=C:\Tools\laravel_deploy.py"
set "TARGET_FOLDER=%~1"

if "%TARGET_FOLDER%"=="" (
    echo Drag and drop folder ke batch file ini, atau
    echo Usage: laravel_deploy.bat "C:\path\to\laravel\project"
    pause
    exit /b 1
)

:: Cek Python
python --version >nul 2>&1
if errorlevel 1 (
    msg * "Python tidak ditemukan! Mohon install Python terlebih dahulu."
    exit /b 1
)

:: Jalankan GUI
python "%SCRIPT_PATH%" "%TARGET_FOLDER%"