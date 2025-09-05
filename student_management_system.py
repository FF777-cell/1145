#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学生管理系统
Student Management System
一个功能完整的学生信息管理系统
"""

import json
import os
import datetime
from typing import Dict, List, Optional, Any
import uuid


class Student:
    """学生类"""
    
    def __init__(self, student_id: str, name: str, age: int, grade: str, class_name: str):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade
        self.class_name = class_name
        self.courses = []  # 选修的课程列表
        self.scores = {}   # 课程成绩字典
        
    def to_dict(self) -> Dict:
        """将学生对象转换为字典"""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'age': self.age,
            'grade': self.grade,
            'class_name': self.class_name,
            'courses': self.courses,
            'scores': self.scores
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Student':
        """从字典创建学生对象"""
        student = cls(
            data['student_id'],
            data['name'],
            data['age'],
            data['grade'],
            data['class_name']
        )
        student.courses = data.get('courses', [])
        student.scores = data.get('scores', {})
        return student


class Course:
    """课程类"""
    
    def __init__(self, course_id: str, name: str, teacher: str, credit: float):
        self.course_id = course_id
        self.name = name
        self.teacher = teacher
        self.credit = credit
        self.students = []  # 选课学生列表
        
    def to_dict(self) -> Dict:
        """将课程对象转换为字典"""
        return {
            'course_id': self.course_id,
            'name': self.name,
            'teacher': self.teacher,
            'credit': self.credit,
            'students': self.students
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Course':
        """从字典创建课程对象"""
        course = cls(
            data['course_id'],
            data['name'],
            data['teacher'],
            data['credit']
        )
        course.students = data.get('students', [])
        return course


class StudentManagementSystem:
    """学生管理系统主类"""
    
    def __init__(self, data_file: str = "students_data.json"):
        self.data_file = data_file
        self.students: Dict[str, Student] = {}
        self.courses: Dict[str, Course] = {}
        self.load_data()
    
    def load_data(self):
        """从文件加载数据"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # 加载学生数据
                for student_data in data.get('students', []):
                    student = Student.from_dict(student_data)
                    self.students[student.student_id] = student
                    
                # 加载课程数据
                for course_data in data.get('courses', []):
                    course = Course.from_dict(course_data)
                    self.courses[course.course_id] = course
                    
                print("数据加载成功！")
            except Exception as e:
                print(f"数据加载失败: {e}")
                self.students = {}
                self.courses = {}
    
    def save_data(self):
        """保存数据到文件"""
        try:
            data = {
                'students': [student.to_dict() for student in self.students.values()],
                'courses': [course.to_dict() for course in self.courses.values()]
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print("数据保存成功！")
        except Exception as e:
            print(f"数据保存失败: {e}")
    
    def generate_student_id(self) -> str:
        """生成唯一的学生ID"""
        return f"S{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4())[:4]}"
    
    def generate_course_id(self) -> str:
        """生成唯一的课程ID"""
        return f"C{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4())[:4]}"
    
    def add_student(self, name: str, age: int, grade: str, class_name: str) -> str:
        """添加学生"""
        student_id = self.generate_student_id()
        student = Student(student_id, name, age, grade, class_name)
        self.students[student_id] = student
        self.save_data()
        return student_id
    
    def remove_student(self, student_id: str) -> bool:
        """删除学生"""
        if student_id in self.students:
            # 从所有课程中移除该学生
            for course in self.courses.values():
                if student_id in course.students:
                    course.students.remove(student_id)
            
            del self.students[student_id]
            self.save_data()
            return True
        return False
    
    def update_student(self, student_id: str, **kwargs) -> bool:
        """更新学生信息"""
        if student_id in self.students:
            student = self.students[student_id]
            for key, value in kwargs.items():
                if hasattr(student, key):
                    setattr(student, key, value)
            self.save_data()
            return True
        return False
    
    def add_course(self, name: str, teacher: str, credit: float) -> str:
        """添加课程"""
        course_id = self.generate_course_id()
        course = Course(course_id, name, teacher, credit)
        self.courses[course_id] = course
        self.save_data()
        return course_id
    
    def remove_course(self, course_id: str) -> bool:
        """删除课程"""
        if course_id in self.courses:
            # 从所有学生的课程列表中移除该课程
            for student in self.students.values():
                if course_id in student.courses:
                    student.courses.remove(course_id)
                if course_id in student.scores:
                    del student.scores[course_id]
            
            del self.courses[course_id]
            self.save_data()
            return True
        return False
    
    def enroll_student_in_course(self, student_id: str, course_id: str) -> bool:
        """学生选课"""
        if student_id in self.students and course_id in self.courses:
            student = self.students[student_id]
            course = self.courses[course_id]
            
            if course_id not in student.courses:
                student.courses.append(course_id)
                course.students.append(student_id)
                self.save_data()
                return True
        return False
    
    def drop_course(self, student_id: str, course_id: str) -> bool:
        """学生退课"""
        if student_id in self.students and course_id in self.courses:
            student = self.students[student_id]
            course = self.courses[course_id]
            
            if course_id in student.courses:
                student.courses.remove(course_id)
                if course_id in student.scores:
                    del student.scores[course_id]
                
                if student_id in course.students:
                    course.students.remove(student_id)
                
                self.save_data()
                return True
        return False
    
    def add_score(self, student_id: str, course_id: str, score: float) -> bool:
        """添加或更新学生成绩"""
        if student_id in self.students and course_id in self.courses:
            student = self.students[student_id]
            if course_id in student.courses:
                student.scores[course_id] = score
                self.save_data()
                return True
        return False
    
    def get_student_info(self, student_id: str) -> Optional[Dict]:
        """获取学生详细信息"""
        if student_id in self.students:
            student = self.students[student_id]
            student_info = student.to_dict()
            
            # 添加课程详细信息
            course_details = []
            for course_id in student.courses:
                if course_id in self.courses:
                    course = self.courses[course_id]
                    course_details.append({
                        'course_id': course_id,
                        'name': course.name,
                        'teacher': course.teacher,
                        'credit': course.credit,
                        'score': student.scores.get(course_id, None)
                    })
            
            student_info['course_details'] = course_details
            return student_info
        return None
    
    def get_course_info(self, course_id: str) -> Optional[Dict]:
        """获取课程详细信息"""
        if course_id in self.courses:
            course = self.courses[course_id]
            course_info = course.to_dict()
            
            # 添加学生详细信息
            student_details = []
            for student_id in course.students:
                if student_id in self.students:
                    student = self.students[student_id]
                    student_details.append({
                        'student_id': student_id,
                        'name': student.name,
                        'grade': student.grade,
                        'class_name': student.class_name,
                        'score': student.scores.get(course_id, None)
                    })
            
            course_info['student_details'] = student_details
            return course_info
        return None
    
    def get_all_students(self) -> List[Dict]:
        """获取所有学生列表"""
        return [student.to_dict() for student in self.students.values()]
    
    def get_all_courses(self) -> List[Dict]:
        """获取所有课程列表"""
        return [course.to_dict() for course in self.courses.values()]
    
    def search_students(self, keyword: str) -> List[Dict]:
        """搜索学生"""
        results = []
        keyword = keyword.lower()
        
        for student in self.students.values():
            if (keyword in student.name.lower() or 
                keyword in student.student_id.lower() or
                keyword in student.grade.lower() or
                keyword in student.class_name.lower()):
                results.append(student.to_dict())
        
        return results
    
    def search_courses(self, keyword: str) -> List[Dict]:
        """搜索课程"""
        results = []
        keyword = keyword.lower()
        
        for course in self.courses.values():
            if (keyword in course.name.lower() or 
                keyword in course.teacher.lower() or
                keyword in course.course_id.lower()):
                results.append(course.to_dict())
        
        return results
    
    def get_class_statistics(self, grade: str, class_name: str) -> Dict:
        """获取班级统计信息"""
        class_students = [
            student for student in self.students.values()
            if student.grade == grade and student.class_name == class_name
        ]
        
        if not class_students:
            return {}
        
        total_students = len(class_students)
        age_distribution = {}
        course_enrollment = {}
        
        for student in class_students:
            # 年龄分布
            age = student.age
            age_distribution[age] = age_distribution.get(age, 0) + 1
            
            # 课程选课统计
            for course_id in student.courses:
                course_enrollment[course_id] = course_enrollment.get(course_id, 0) + 1
        
        # 获取课程名称
        course_names = {}
        for course_id, count in course_enrollment.items():
            if course_id in self.courses:
                course_names[course_id] = self.courses[course_id].name
        
        return {
            'total_students': total_students,
            'age_distribution': age_distribution,
            'course_enrollment': course_enrollment,
            'course_names': course_names
        }


def main():
    """主函数 - 命令行界面"""
    system = StudentManagementSystem()
    
    print("=" * 50)
    print("    学生管理系统")
    print("=" * 50)
    
    while True:
        print("\n请选择操作：")
        print("1. 学生管理")
        print("2. 课程管理")
        print("3. 选课管理")
        print("4. 成绩管理")
        print("5. 查询统计")
        print("0. 退出系统")
        
        choice = input("\n请输入选项: ").strip()
        
        if choice == "0":
            print("感谢使用学生管理系统！")
            break
        
        elif choice == "1":
            # 学生管理
            print("\n--- 学生管理 ---")
            print("1. 添加学生")
            print("2. 删除学生")
            print("3. 更新学生信息")
            print("4. 查看学生信息")
            print("5. 查看所有学生")
            print("6. 搜索学生")
            
            sub_choice = input("请选择操作: ").strip()
            
            if sub_choice == "1":
                name = input("姓名: ")
                age = int(input("年龄: "))
                grade = input("年级: ")
                class_name = input("班级: ")
                student_id = system.add_student(name, age, grade, class_name)
                print(f"学生添加成功，学号: {student_id}")
            
            elif sub_choice == "2":
                student_id = input("请输入要删除的学生学号: ")
                if system.remove_student(student_id):
                    print("学生删除成功！")
                else:
                    print("未找到该学生！")
            
            elif sub_choice == "3":
                student_id = input("请输入要更新的学生学号: ")
                if student_id in system.students:
                    print("可更新的字段: name, age, grade, class_name")
                    field = input("要更新的字段: ")
                    value = input("新值: ")
                    if field == "age":
                        value = int(value)
                    if system.update_student(student_id, **{field: value}):
                        print("学生信息更新成功！")
                    else:
                        print("更新失败！")
                else:
                    print("未找到该学生！")
            
            elif sub_choice == "4":
                student_id = input("请输入学生学号: ")
                info = system.get_student_info(student_id)
                if info:
                    print("\n学生详细信息:")
                    print(f"学号: {info['student_id']}")
                    print(f"姓名: {info['name']}")
                    print(f"年龄: {info['age']}")
                    print(f"年级: {info['grade']}")
                    print(f"班级: {info['class_name']}")
                    print("\n已选课程:")
                    for course in info['course_details']:
                        print(f"  {course['name']} - 教师: {course['teacher']} - 学分: {course['credit']} - 成绩: {course['score']}")
                else:
                    print("未找到该学生！")
            
            elif sub_choice == "5":
                students = system.get_all_students()
                if students:
                    print("\n所有学生:")
                    for student in students:
                        print(f"{student['student_id']} - {student['name']} - {student['grade']}{student['class_name']}")
                else:
                    print("暂无学生信息")
            
            elif sub_choice == "6":
                keyword = input("请输入搜索关键词: ")
                results = system.search_students(keyword)
                if results:
                    print("\n搜索结果:")
                    for student in results:
                        print(f"{student['student_id']} - {student['name']} - {student['grade']}{student['class_name']}")
                else:
                    print("未找到匹配的学生")
        
        elif choice == "2":
            # 课程管理
            print("\n--- 课程管理 ---")
            print("1. 添加课程")
            print("2. 删除课程")
            print("3. 查看课程信息")
            print("4. 查看所有课程")
            print("5. 搜索课程")
            
            sub_choice = input("请选择操作: ").strip()
            
            if sub_choice == "1":
                name = input("课程名称: ")
                teacher = input("任课教师: ")
                credit = float(input("学分: "))
                course_id = system.add_course(name, teacher, credit)
                print(f"课程添加成功，课程号: {course_id}")
            
            elif sub_choice == "2":
                course_id = input("请输入要删除的课程号: ")
                if system.remove_course(course_id):
                    print("课程删除成功！")
                else:
                    print("未找到该课程！")
            
            elif sub_choice == "3":
                course_id = input("请输入课程号: ")
                info = system.get_course_info(course_id)
                if info:
                    print("\n课程详细信息:")
                    print(f"课程号: {info['course_id']}")
                    print(f"名称: {info['name']}")
                    print(f"教师: {info['teacher']}")
                    print(f"学分: {info['credit']}")
                    print("\n选课学生:")
                    for student in info['student_details']:
                        print(f"  {student['name']} - {student['grade']}{student['class_name']} - 成绩: {student['score']}")
                else:
                    print("未找到该课程！")
            
            elif sub_choice == "4":
                courses = system.get_all_courses()
                if courses:
                    print("\n所有课程:")
                    for course in courses:
                        print(f"{course['course_id']} - {course['name']} - 教师: {course['teacher']} - 学分: {course['credit']}")
                else:
                    print("暂无课程信息")
            
            elif sub_choice == "5":
                keyword = input("请输入搜索关键词: ")
                results = system.search_courses(keyword)
                if results:
                    print("\n搜索结果:")
                    for course in results:
                        print(f"{course['course_id']} - {course['name']} - 教师: {course['teacher']}")
                else:
                    print("未找到匹配的课程")
        
        elif choice == "3":
            # 选课管理
            print("\n--- 选课管理 ---")
            print("1. 学生选课")
            print("2. 学生退课")
            
            sub_choice = input("请选择操作: ").strip()
            
            if sub_choice == "1":
                student_id = input("学生学号: ")
                course_id = input("课程号: ")
                if system.enroll_student_in_course(student_id, course_id):
                    print("选课成功！")
                else:
                    print("选课失败！请检查学号和课程号是否正确")
            
            elif sub_choice == "2":
                student_id = input("学生学号: ")
                course_id = input("课程号: ")
                if system.drop_course(student_id, course_id):
                    print("退课成功！")
                else:
                    print("退课失败！请检查学号和课程号是否正确")
        
        elif choice == "4":
            # 成绩管理
            print("\n--- 成绩管理 ---")
            print("1. 录入成绩")
            print("2. 修改成绩")
            
            sub_choice = input("请选择操作: ").strip()
            
            if sub_choice in ["1", "2"]:
                student_id = input("学生学号: ")
                course_id = input("课程号: ")
                score = float(input("成绩: "))
                if system.add_score(student_id, course_id, score):
                    print("成绩录入/更新成功！")
                else:
                    print("操作失败！请检查学号和课程号是否正确")
        
        elif choice == "5":
            # 查询统计
            print("\n--- 查询统计 ---")
            print("1. 班级统计")
            print("2. 查看学生成绩")
            
            sub_choice = input("请选择操作: ").strip()
            
            if sub_choice == "1":
                grade = input("年级: ")
                class_name = input("班级: ")
                stats = system.get_class_statistics(grade, class_name)
                if stats:
                    print(f"\n{grade}{class_name}班统计信息:")
                    print(f"总人数: {stats['total_students']}")
                    print("年龄分布:")
                    for age, count in stats['age_distribution'].items():
                        print(f"  {age}岁: {count}人")
                    print("课程选课统计:")
                    for course_id, count in stats['course_enrollment'].items():
                        course_name = stats['course_names'].get(course_id, "未知课程")
                        print(f"  {course_name}: {count}人")
                else:
                    print("该班级暂无学生")
            
            elif sub_choice == "2":
                student_id = input("学生学号: ")
                info = system.get_student_info(student_id)
                if info:
                    print(f"\n{info['name']}的成绩:")
                    for course in info['course_details']:
                        score = course['score'] if course['score'] is not None else "暂无成绩"
                        print(f"{course['name']}: {score}")
                else:
                    print("未找到该学生！")


if __name__ == "__main__":
    main()