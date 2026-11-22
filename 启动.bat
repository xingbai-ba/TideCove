@echo off
cd /d "%~dp0"
set "TIDECOVE_ROOT=%~dp0TideGleam"

echo.
echo   TideCove x TideGleam 1.3.0
echo   ---------------------------------
echo   Starting server...
echo.
echo   NOTE: keep this window open. Closing it stops the server.
echo   AI clients are detected automatically - see the list below.
echo.

rem Check optional tools (speech-to-text / text-to-speech).
rem Missing tools are skipped, never block startup.
if exist "%~dp0check-tools.ps1" (
  powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0check-tools.ps1"
  echo.
)

start "" powershell -WindowStyle Hidden -Command "Start-Sleep -Seconds 5; Start-Process 'http://127.0.0.1:8080/admin'"
"%~dp0TideGleam\TideGleam.exe"

echo.
echo   Server stopped. Press any key to close.
pause >nul
