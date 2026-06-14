@echo off
title WoofPrix
cd /d "%~dp0"
echo Demarrage de WoofPrix...
start "" http://localhost:5173
npx vite --host
pause
