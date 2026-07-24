# Start backend: crea/usa venv, instala dependencias y arranca uvicorn
$root = if ($PSScriptRoot) { $PSScriptRoot } else { Get-Location }
Set-Location $root

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

$venvPy = Join-Path $root ".venv\Scripts\python.exe"

& $venvPy -m pip install --upgrade pip
& $venvPy -m pip install -r backend\requirements.txt

Set-Location (Join-Path $root "backend")
& $venvPy -m uvicorn main:app --host 127.0.0.1 --port 8001 --reload
