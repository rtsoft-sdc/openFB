Write-Host "Cleaning project directories..." -ForegroundColor Cyan

Get-ChildItem -Path . -Filter "__pycache__" -Directory -Recurse -ErrorAction SilentlyContinue | ForEach-Object { 
    Remove-Item $_.FullName -Recurse -Force 
}

Get-ChildItem -Path . -Include "*.pyc", "*.pyo" -File -Recurse -ErrorAction SilentlyContinue | ForEach-Object { 
    Remove-Item $_.FullName -Force 
}

$DirectoriesToClean = @(
    "dist",
    "openfb.egg-info"
)

$FilesToClean = @(
    "openfb.deb",
    "deb-packaging/openfb.deb",
    "deb-packaging/openfb/opt/openfb/openfb-*-py3-none-any.whl",
    "openfb/resources/data_model.fboot",
    "openfb/resources/error_list.log"
)

foreach ($dir in $DirectoriesToClean) {
    if (Test-Path $dir) {
        Remove-Item -Path $dir -Recurse -Force
    }
}

foreach ($file in $FilesToClean) {
    if (Test-Path $file) {
        Remove-Item -Path $file -Force
    }
}

Write-Host "Clean inside Windows completed successfully." -ForegroundColor Green