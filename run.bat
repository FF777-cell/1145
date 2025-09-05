@echo off
echo ================================================
echo    学生管理系统启动器
echo ================================================
echo.
echo 请选择启动方式：
echo 1. 命令行界面
echo 2. 图形界面
echo 3. 运行测试
echo 4. 生成演示数据
echo 0. 退出
echo.
set /p choice=请输入选项(0-4): 

if "%choice%"=="1" (
    echo 启动命令行界面...
    python student_management_system.py
) else if "%choice%"=="2" (
    echo 启动图形界面...
    python student_gui.py
) else if "%choice%"=="3" (
    echo 运行系统测试...
    python test_system.py
) else if "%choice%"=="4" (
    echo 生成演示数据...
    python test_system.py demo
) else if "%choice%"=="0" (
    echo 感谢使用！
) else (
    echo 无效选项，请重新运行
)

pause