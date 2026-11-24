@echo off
title Arena Mercado em Conexao (Python + SQLite)
echo ========================================================
echo   Iniciando Arena Mercado em Conexao...
echo ========================================================
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
python run.py
if errorlevel 1 (
    echo.
    echo [ERRO] Ocorreu uma falha ao iniciar o servidor.
    pause
)
