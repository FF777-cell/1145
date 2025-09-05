#!/bin/bash

# 学生管理系统启动器
# Student Management System Launcher

echo "=============================================="
echo "    学生管理系统启动器"
echo "=============================================="
echo
echo "请选择启动方式："
echo "1. 命令行界面"
echo "2. 图形界面"
echo "3. 运行测试"
echo "4. 生成演示数据"
echo "0. 退出"
echo

read -p "请输入选项(0-4): " choice

case $choice in
    1)
        echo "启动命令行界面..."
        python3 student_management_system.py
        ;;
    2)
        echo "启动图形界面..."
        python3 student_gui.py
        ;;
    3)
        echo "运行系统测试..."
        python3 test_system.py
        ;;
    4)
        echo "生成演示数据..."
        python3 test_system.py demo
        ;;
    0)
        echo "感谢使用！"
        ;;
    *)
        echo "无效选项，请重新运行"
        ;;
esac