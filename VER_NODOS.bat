@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Multilista DIVIPOLA - nodos
py -X utf8 ver_nodos.py
echo.
pause
