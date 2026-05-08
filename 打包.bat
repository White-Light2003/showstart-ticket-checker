@echo off
chcp 65001 > nul
echo ========================================
echo    秀动余票查询机器人 - 打包工具
echo ========================================
echo.

echo [1/3] 正在安装依赖...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [错误] 依赖安装失败，请检查网络连接
    pause
    exit /b 1
)

echo.
echo [2/3] 正在安装 PyInstaller...
pip install pyinstaller

if errorlevel 1 (
    echo.
    echo [错误] PyInstaller 安装失败
    pause
    exit /b 1
)

echo.
echo [3/3] 正在打包程序...
echo.

pyinstaller --onefile --noconsole --name "showstart_ticket_checker" showstart_ticket_checker.py

if errorlevel 1 (
    echo.
    echo [错误] 打包失败
    pause
    exit /b 1
)

echo.
echo ========================================
echo    打包完成！
echo ========================================
echo.
echo 运行文件: dist\showstart_ticket_checker.exe
echo.
echo 首次运行会自动下载 Chrome 驱动
echo.
pause
