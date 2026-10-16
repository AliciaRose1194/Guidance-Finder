@echo off
setlocal
cd /d "%~dp0"

where uv >nul 2>&1
if errorlevel 1 (
    echo uv is required to run Guidance Finder but was not found.
    echo Install it from https://docs.astral.sh/uv/getting-started/installation/
    pause
    exit /b 1
)

uv run streamlit run streamlit_app.py --server.showEmailPrompt false
if errorlevel 1 pause
