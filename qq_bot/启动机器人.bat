@echo off
chcp 65001 >nul
title 秀动余票查询QQ机器人

echo ========================================
echo   秀动余票查询 QQ 机器人启动器
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)
echo       Python 环境检查通过

echo.
echo [2/3] 安装依赖...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)
echo       依赖安装完成

echo.
echo [3/3] 启动 NoneBot2...
echo.
echo ========================================
echo   启动完成！
echo   - NoneBot2 运行中
echo   - 确保 go-cqhttp 已启动
echo ========================================
echo.

python bot.py

pause
