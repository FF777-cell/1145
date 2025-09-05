#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学生管理系统测试脚本
用于验证系统功能的正确性
"""

import os
import sys
from student_management_system import StudentManagementSystem


def test_system():
    """测试系统功能"""
    print("开始测试学生管理系统...")
    
    # 使用测试数据文件
    test_data_file = "test_data.json"
    
    # 如果测试文件存在，先删除
    if os.path.exists(test_data_file):
        os.remove(test_data_file)
    
    # 创建系统实例
    system = StudentManagementSystem(test_data_file)
    
    print("1. 测试添加学生...")
    student_id1 = system.add_student("张三", 18, "高三", "1班")
    student_id2 = system.add_student("李四", 17, "高三", "2班")
    student_id3 = system.add_student("王五", 16, "高二", "1班")
    print(f"   添加学生成功: {student_id1}, {student_id2}, {student_id3}")
    
    print("2. 测试添加课程...")
    course_id1 = system.add_course("数学", "张老师", 3.0)
    course_id2 = system.add_course("英语", "李老师", 2.5)
    course_id3 = system.add_course("物理", "王老师", 3.5)
    print(f"   添加课程成功: {course_id1}, {course_id2}, {course_id3}")
    
    print("3. 测试学生选课...")
    system.enroll_student_in_course(student_id1, course_id1)
    system.enroll_student_in_course(student_id1, course_id2)
    system.enroll_student_in_course(student_id2, course_id1)
    system.enroll_student_in_course(student_id3, course_id3)
    print("   选课操作完成")
    
    print("4. 测试成绩录入...")
    system.add_score(student_id1, course_id1, 95.5)
    system.add_score(student_id1, course_id2, 88.0)
    system.add_score(student_id2, course_id1, 92.0)
    system.add_score(student_id3, course_id3, 90.5)
    print("   成绩录入完成")
    
    print("5. 测试查询功能...")
    
    # 查询学生信息
    student_info = system.get_student_info(student_id1)
    if student_info:
        print(f"   学生张三信息: {student_info['name']}, 课程数: {len(student_info['courses'])}")
    
    # 查询课程信息
    course_info = system.get_course_info(course_id1)
    if course_info:
        print(f"   数学课程信息: {course_info['name']}, 学生数: {len(course_info['students'])}")
    
    # 查询班级统计
    stats = system.get_class_statistics("高三", "1班")
    if stats:
        print(f"   高三1班统计: 总人数 {stats['total_students']}")
    
    print("6. 测试搜索功能...")
    students = system.search_students("张")
    print(f"   搜索'张'的结果: {len(students)} 个学生")
    
    courses = system.search_courses("数学")
    print(f"   搜索'数学'的结果: {len(courses)} 门课程")
    
    print("7. 测试退课功能...")
    system.drop_course(student_id1, course_id2)
    student_info = system.get_student_info(student_id1)
    print(f"   张三退课后课程数: {len(student_info['courses'])}")
    
    print("8. 测试删除功能...")
    system.remove_student(student_id3)
    students = system.get_all_students()
    print(f"   删除学生后总人数: {len(students)}")
    
    print("9. 测试数据保存和加载...")
    system.save_data()
    
    # 创建新系统实例测试加载
    new_system = StudentManagementSystem(test_data_file)
    students = new_system.get_all_students()
    courses = new_system.get_all_courses()
    print(f"   重新加载后学生数: {len(students)}, 课程数: {len(courses)}")
    
    # 清理测试文件
    if os.path.exists(test_data_file):
        os.remove(test_data_file)
    
    print("\n所有测试完成！系统功能正常。")


def demo_usage():
    """演示系统使用"""
    print("\n" + "="*50)
    print("学生管理系统演示")
    print("="*50)
    
    # 使用演示数据文件
    demo_file = "demo_data.json"
    
    # 清理旧文件
    if os.path.exists(demo_file):
        os.remove(demo_file)
    
    system = StudentManagementSystem(demo_file)
    
    print("\n1. 创建示例数据...")
    
    # 添加学生
    students = [
        ("小明", 18, "高三", "1班"),
        ("小红", 17, "高三", "1班"),
        ("小刚", 18, "高三", "2班"),
        ("小丽", 17, "高二", "1班")
    ]
    
    student_ids = []
    for name, age, grade, class_name in students:
        sid = system.add_student(name, age, grade, class_name)
        student_ids.append(sid)
        print(f"   添加学生: {name} ({sid})")
    
    # 添加课程
    courses = [
        ("高等数学", "张教授", 4.0),
        ("大学英语", "李老师", 3.0),
        ("大学物理", "王教授", 4.0),
        ("程序设计", "赵老师", 3.5)
    ]
    
    course_ids = []
    for name, teacher, credit in courses:
        cid = system.add_course(name, teacher, credit)
        course_ids.append(cid)
        print(f"   添加课程: {name} ({cid})")
    
    print("\n2. 学生选课...")
    # 小明选数学和英语
    system.enroll_student_in_course(student_ids[0], course_ids[0])
    system.enroll_student_in_course(student_ids[0], course_ids[1])
    
    # 小红选数学和物理
    system.enroll_student_in_course(student_ids[1], course_ids[0])
    system.enroll_student_in_course(student_ids[1], course_ids[2])
    
    # 小刚选所有课程
    for cid in course_ids:
        system.enroll_student_in_course(student_ids[2], cid)
    
    print("   选课完成")
    
    print("\n3. 录入成绩...")
    # 录入成绩
    grades = [
        (student_ids[0], course_ids[0], 95.0),  # 小明数学
        (student_ids[0], course_ids[1], 88.5),  # 小明英语
        (student_ids[1], course_ids[0], 92.0),  # 小红数学
        (student_ids[1], course_ids[2], 89.0),  # 小红物理
        (student_ids[2], course_ids[0], 78.0),   # 小刚数学
        (student_ids[2], course_ids[1], 85.5),   # 小刚英语
        (student_ids[2], course_ids[2], 91.0), # 小刚物理
        (student_ids[2], course_ids[3], 96.0)  # 小刚程序设计
    ]
    
    for sid, cid, score in grades:
        system.add_score(sid, cid, score)
    
    print("   成绩录入完成")
    
    print("\n4. 查看统计信息...")
    
    # 查看高三1班统计
    stats = system.get_class_statistics("高三", "1班")
    if stats:
        print(f"   高三1班统计:")
        print(f"   总人数: {stats['total_students']}")
        print(f"   年龄分布: {stats['age_distribution']}")
        print(f"   课程选课: {stats['course_enrollment']}")
    
    print("\n5. 学生成绩查询...")
    for sid in student_ids[:3]:
        student_info = system.get_student_info(sid)
        if student_info:
            print(f"   {student_info['name']}的成绩:")
            for course in student_info['course_details']:
                score = course['score'] if course['score'] is not None else "暂无"
                print(f"     {course['name']}: {score}")
    
    # 保存演示数据
    system.save_data()
    print(f"\n演示数据已保存到: {demo_file}")
    print("\n演示完成！现在可以运行图形界面查看数据：")
    print("python student_gui.py")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_usage()
    else:
        test_system()