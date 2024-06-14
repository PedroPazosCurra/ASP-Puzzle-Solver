@echo off
echo Bienvenido al programa de setup de ASP Puzzle Solver. Preparando sistema para su ejecución...
echo.
call pip install -r .requirements --quiet || exit /b
cd ./src
call npm install --silent || exit /b
echo Programa correctamente preparado. Pulse cualquier tecla para salir
echo.
pause >nul
exit
