# Start frontend: instala dependencias y arranca Angular
$root = if ($PSScriptRoot) { $PSScriptRoot } else { Get-Location }
Set-Location (Join-Path $root "frontend")

npm install
npm start
