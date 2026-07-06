@echo off
setlocal enabledelayedexpansion

chcp 65001 >nul

echo Cleaning up project directoyries...

for /d /r %%i in (__pycache__) do (
    if exist "%%i" (
        echo Deleting directory: %%i
        rmdir /s /q "%%i" 2>nul
    )
)

del /s /q /f "*.pyc" "*.pyo" 2>nul

set "DirectoriesToClean=dist openfb.egg-info"
for %%d in (%DirectoriesToClean%) do (
    if exist "%%d" (
        rd /s /q "%%d" 2>nul
    )
)

if exist "openfb.deb" del /f /q "openfb.deb" 2>nul
if exist "deb-packaging\openfb.deb" del /f /q "deb-packaging\openfb.deb" 2>nul

if exist "deb-packaging\openfb\opt\openfb\" (
    del /f /q "deb-packaging\openfb\opt\openfb\openfb-*-py3-none-any.whl" 2>nul
)

if exist "openfb\resources\data_model.fboot" del /f /q "openfb\resources\data_model.fboot" 2>nul
if exist "openfb\resources\error_list.log" del /f /q "openfb\resources\error_list.log" 2>nul

echo Project cleanup completed.