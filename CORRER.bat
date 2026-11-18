@echo off
chcp 65001 >nul
cd /d "%~dp0"
title Multilista DIVIPOLA - servidor Flask
set PY=
where py >nul 2>nul && set PY=py
if not defined PY where python >nul 2>nul && set PY=python
if not defined PY (
  echo NO_PYTHON > log.txt
  echo No se encontro Python. Instalalo desde python.org marcando "Add Python to PATH".
  pause
  exit /b
)
echo Usando %PY% > log.txt
%PY% --version >> log.txt 2>&1
echo Instalando Flask...
%PY% -m pip install flask >> log.txt 2>&1
echo.
echo === Arbol de la multilista (resumido) ===
%PY% -X utf8 multilista.py
%PY% -X utf8 multilista.py > arbol.txt 2>&1
echo.
echo Abriendo el mapa en el navegador... (cierra esta ventana para apagar el servidor)
start "" cmd /c "timeout /t 4 >nul & start http://127.0.0.1:8000"
%PY% -X utf8 app.py >> log.txt 2>&1
pause
