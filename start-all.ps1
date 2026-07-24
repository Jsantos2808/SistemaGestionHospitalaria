# Abre backend y frontend en ventanas separadas
$root = if ($PSScriptRoot) { $PSScriptRoot } else { Get-Location }
$backendScript = Join-Path $root "start-backend.ps1"
$frontendScript = Join-Path $root "start-frontend.ps1"

Start-Process powershell -ArgumentList "-NoExit","-ExecutionPolicy","Bypass","-File","$backendScript"
Start-Process powershell -ArgumentList "-NoExit","-ExecutionPolicy","Bypass","-File","$frontendScript"
