@echo off
chcp 65001 >nul
title TideCove 1.2.5
cd /d "%~dp0"
set "TIDECOVE_ROOT=%~dp0TideGleam"

echo.
echo   TideCove x TideGleam 1.2.5
echo   ---------------------------------
echo   正在启动服务端...
echo   几秒后会自动打开配对页面
echo   关闭这个窗口 = 停止服务
echo.

start "" powershell -WindowStyle Hidden -Command "Start-Sleep -Seconds 5; Start-Process 'http://127.0.0.1:8080/admin'"
"%~dp0TideGleam\TideGleam.exe"

echo.
echo   服务已停止。按任意键关闭。
pause >nul
