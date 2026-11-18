@echo off
chcp 65001 >nul
title TideGleam
cd /d "%~dp0TideGleam"
set TIDECOVE_ROOT=%~dp0TideGleam
echo ============================================
echo    TideGleam 启动中...
echo ============================================
echo.
echo  启动完成后会自动打开配对页面。
echo  页面上能看到：服务器地址、配对码、手机安装包下载。
echo.
start "" powershell -NoProfile -WindowStyle Hidden -Command "Start-Sleep -Seconds 5; Start-Process 'http://127.0.0.1:8080/admin'"
"%~dp0TideGleam\TideGleam.exe"
echo.
echo 服务已停止。按任意键关闭。
pause >nul