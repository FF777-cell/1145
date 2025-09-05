#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学生管理系统 - 图形界面版本
Student Management System - GUI Version
使用tkinter创建的图形界面学生管理系统
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from student_management_system import StudentManagementSystem


class StudentManagementGUI:
    """学生管理系统图形界面"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("学生管理系统")
        self.root.geometry("1000x700")
        
        # 初始化系统
        self.system = StudentManagementSystem()
        
        # 创建界面
        self.create_widgets()
        
        # 加载数据
        self.refresh_all_data()
    
    def create_widgets(self):
        """创建界面组件"""
        # 创建菜单栏
        self.create_menu()
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建标签页
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 创建各个标签页
        self.create_student_tab()
        self.create_course_tab()
        self.create_enrollment_tab()
        self.create_score_tab()
        self.create_statistics_tab()
    
    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="保存数据", command=self.save_data)
        file_menu.add_command(label="重新加载", command=self.refresh_all_data)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self.show_about)
    
    def create_student_tab(self):
        """创建学生管理标签页"""
        student_frame = ttk.Frame(self.notebook)
        self.notebook.add(student_frame, text="学生管理")
        
        # 创建左右分割面板
        paned = ttk.PanedWindow(student_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # 左侧面板 - 学生列表
        left_frame = ttk.Frame(paned)
        paned.add(left_frame)
        
        # 搜索框架
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_frame, text="搜索:").pack(side=tk.LEFT, padx=5)
        self.student_search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.student_search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        search_entry.bind('<KeyRelease>', self.search_students)
        
        # 学生列表
        self.student_tree = ttk.Treeview(left_frame, columns=('ID', 'Name', 'Age', 'Grade', 'Class'), 
                                        show='headings', height=15)
        self.student_tree.heading('ID', text='学号')
        self.student_tree.heading('Name', text='姓名')
        self.student_tree.heading('Age', text='年龄')
        self.student_tree.heading('Grade', text='年级')
        self.student_tree.heading('Class', text='班级')
        
        self.student_tree.column('ID', width=120)
        self.student_tree.column('Name', width=100)
        self.student_tree.column('Age', width=50)
        self.student_tree.column('Grade', width=80)
        self.student_tree.column('Class', width=80)
        
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.student_tree.yview)
        self.student_tree.configure(yscrollcommand=scrollbar.set)
        
        self.student_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.student_tree.bind('<Double-1>', self.show_student_details)
        
        # 按钮框架
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="添加学生", command=self.add_student_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="编辑学生", command=self.edit_student_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="删除学生", command=self.delete_student).pack(side=tk.LEFT, padx=5)
        
        # 右侧面板 - 学生详细信息
        right_frame = ttk.Frame(paned)
        paned.add(right_frame)
        
        # 学生详细信息
        detail_frame = ttk.LabelFrame(right_frame, text="学生详细信息")
        detail_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.student_detail_text = tk.Text(detail_frame, height=20, width=40)
        self.student_detail_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_course_tab(self):
        """创建课程管理标签页"""
        course_frame = ttk.Frame(self.notebook)
        self.notebook.add(course_frame, text="课程管理")
        
        # 创建左右分割面板
        paned = ttk.PanedWindow(course_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # 左侧面板 - 课程列表
        left_frame = ttk.Frame(paned)
        paned.add(left_frame)
        
        # 搜索框架
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_frame, text="搜索:").pack(side=tk.LEFT, padx=5)
        self.course_search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.course_search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        search_entry.bind('<KeyRelease>', self.search_courses)
        
        # 课程列表
        self.course_tree = ttk.Treeview(left_frame, columns=('ID', 'Name', 'Teacher', 'Credit'), 
                                       show='headings', height=15)
        self.course_tree.heading('ID', text='课程号')
        self.course_tree.heading('Name', text='课程名称')
        self.course_tree.heading('Teacher', text='任课教师')
        self.course_tree.heading('Credit', text='学分')
        
        self.course_tree.column('ID', width=120)
        self.course_tree.column('Name', width=150)
        self.course_tree.column('Teacher', width=100)
        self.course_tree.column('Credit', width=50)
        
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.course_tree.yview)
        self.course_tree.configure(yscrollcommand=scrollbar.set)
        
        self.course_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.course_tree.bind('<Double-1>', self.show_course_details)
        
        # 按钮框架
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="添加课程", command=self.add_course_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="编辑课程", command=self.edit_course_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="删除课程", command=self.delete_course).pack(side=tk.LEFT, padx=5)
        
        # 右侧面板 - 课程详细信息
        right_frame = ttk.Frame(paned)
        paned.add(right_frame)
        
        # 课程详细信息
        detail_frame = ttk.LabelFrame(right_frame, text="课程详细信息")
        detail_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.course_detail_text = tk.Text(detail_frame, height=20, width=40)
        self.course_detail_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_enrollment_tab(self):
        """创建选课管理标签页"""
        enrollment_frame = ttk.Frame(self.notebook)
        self.notebook.add(enrollment_frame, text="选课管理")
        
        # 学生选择框架
        student_frame = ttk.LabelFrame(enrollment_frame, text="选择学生")
        student_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 学生列表
        self.enrollment_student_tree = ttk.Treeview(student_frame, columns=('ID', 'Name', 'Grade', 'Class'), 
                                                   show='headings', height=8)
        self.enrollment_student_tree.heading('ID', text='学号')
        self.enrollment_student_tree.heading('Name', text='姓名')
        self.enrollment_student_tree.heading('Grade', text='年级')
        self.enrollment_student_tree.heading('Class', text='班级')
        
        self.enrollment_student_tree.column('ID', width=120)
        self.enrollment_student_tree.column('Name', width=100)
        self.enrollment_student_tree.column('Grade', width=80)
        self.enrollment_student_tree.column('Class', width=80)
        
        scrollbar = ttk.Scrollbar(student_frame, orient=tk.VERTICAL, 
                                  command=self.enrollment_student_tree.yview)
        self.enrollment_student_tree.configure(yscrollcommand=scrollbar.set)
        
        self.enrollment_student_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 课程选择框架
        course_frame = ttk.LabelFrame(enrollment_frame, text="选择课程")
        course_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 可用课程列表
        self.available_course_tree = ttk.Treeview(course_frame, columns=('ID', 'Name', 'Teacher', 'Credit'), 
                                                show='headings', height=8)
        self.available_course_tree.heading('ID', text='课程号')
        self.available_course_tree.heading('Name', text='课程名称')
        self.available_course_tree.heading('Teacher', text='教师')
        self.available_course_tree.heading('Credit', text='学分')
        
        self.available_course_tree.column('ID', width=120)
        self.available_course_tree.column('Name', width=150)
        self.available_course_tree.column('Teacher', width=100)
        self.available_course_tree.column('Credit', width=50)
        
        scrollbar2 = ttk.Scrollbar(course_frame, orient=tk.VERTICAL, 
                                 command=self.available_course_tree.yview)
        self.available_course_tree.configure(yscrollcommand=scrollbar2.set)
        
        self.available_course_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 按钮框架
        button_frame = ttk.Frame(enrollment_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="选课", command=self.enroll_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="退课", command=self.drop_course).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="刷新", command=self.refresh_enrollment_data).pack(side=tk.LEFT, padx=5)
    
    def create_score_tab(self):
        """创建成绩管理标签页"""
        score_frame = ttk.Frame(self.notebook)
        self.notebook.add(score_frame, text="成绩管理")
        
        # 创建左右分割面板
        paned = ttk.PanedWindow(score_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # 左侧面板
        left_frame = ttk.Frame(paned)
        paned.add(left_frame)
        
        # 学生选择
        student_frame = ttk.LabelFrame(left_frame, text="选择学生")
        student_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.score_student_tree = ttk.Treeview(student_frame, columns=('ID', 'Name'), 
                                             show='headings', height=10)
        self.score_student_tree.heading('ID', text='学号')
        self.score_student_tree.heading('Name', text='姓名')
        
        self.score_student_tree.column('ID', width=120)
        self.score_student_tree.column('Name', width=100)
        
        scrollbar = ttk.Scrollbar(student_frame, orient=tk.VERTICAL, 
                                command=self.score_student_tree.yview)
        self.score_student_tree.configure(yscrollcommand=scrollbar.set)
        
        self.score_student_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.score_student_tree.bind('<<TreeviewSelect>>', self.on_student_select_for_score)
        
        # 右侧面板
        right_frame = ttk.Frame(paned)
        paned.add(right_frame)
        
        # 成绩管理
        score_manage_frame = ttk.LabelFrame(right_frame, text="成绩管理")
        score_manage_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 课程成绩列表
        self.score_course_tree = ttk.Treeview(score_manage_frame, columns=('Course', 'Score'), 
                                            show='headings', height=10)
        self.score_course_tree.heading('Course', text='课程')
        self.score_course_tree.heading('Score', text='成绩')
        
        self.score_course_tree.column('Course', width=200)
        self.score_course_tree.column('Score', width=80)
        
        scrollbar2 = ttk.Scrollbar(score_manage_frame, orient=tk.VERTICAL, 
                                 command=self.score_course_tree.yview)
        self.score_course_tree.configure(yscrollcommand=scrollbar2.set)
        
        self.score_course_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 按钮框架
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="录入成绩", command=self.add_score_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="修改成绩", command=self.edit_score_dialog).pack(side=tk.LEFT, padx=5)
    
    def create_statistics_tab(self):
        """创建统计标签页"""
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="统计查询")
        
        # 班级统计框架
        class_frame = ttk.LabelFrame(stats_frame, text="班级统计")
        class_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 输入框架
        input_frame = ttk.Frame(class_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="年级:").pack(side=tk.LEFT, padx=5)
        self.grade_var = tk.StringVar()
        grade_entry = ttk.Entry(input_frame, textvariable=self.grade_var, width=10)
        grade_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(input_frame, text="班级:").pack(side=tk.LEFT, padx=5)
        self.class_var = tk.StringVar()
        class_entry = ttk.Entry(input_frame, textvariable=self.class_var, width=10)
        class_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(input_frame, text="查询", command=self.show_class_statistics).pack(side=tk.LEFT, padx=10)
        
        # 统计结果显示
        self.stats_text = tk.Text(class_frame, height=15, width=60)
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def refresh_all_data(self):
        """刷新所有数据"""
        self.refresh_student_list()
        self.refresh_course_list()
        self.refresh_enrollment_data()
        self.refresh_score_data()
    
    def refresh_student_list(self):
        """刷新学生列表"""
        # 清空现有数据
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        
        # 加载学生数据
        students = self.system.get_all_students()
        for student in students:
            self.student_tree.insert('', 'end', values=(
                student['student_id'],
                student['name'],
                student['age'],
                student['grade'],
                student['class_name']
            ))
    
    def refresh_course_list(self):
        """刷新课程列表"""
        # 清空现有数据
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)
        
        # 加载课程数据
        courses = self.system.get_all_courses()
        for course in courses:
            self.course_tree.insert('', 'end', values=(
                course['course_id'],
                course['name'],
                course['teacher'],
                course['credit']
            ))
    
    def refresh_enrollment_data(self):
        """刷新选课数据"""
        # 清空学生列表
        for item in self.enrollment_student_tree.get_children():
            self.enrollment_student_tree.delete(item)
        
        # 加载学生
        students = self.system.get_all_students()
        for student in students:
            self.enrollment_student_tree.insert('', 'end', values=(
                student['student_id'],
                student['name'],
                student['grade'],
                student['class_name']
            ))
        
        # 清空课程列表
        for item in self.available_course_tree.get_children():
            self.available_course_tree.delete(item)
        
        # 加载课程
        courses = self.system.get_all_courses()
        for course in courses:
            self.available_course_tree.insert('', 'end', values=(
                course['course_id'],
                course['name'],
                course['teacher'],
                course['credit']
            ))
    
    def refresh_score_data(self):
        """刷新成绩数据"""
        # 清空学生列表
        for item in self.score_student_tree.get_children():
            self.score_student_tree.delete(item)
        
        # 加载学生
        students = self.system.get_all_students()
        for student in students:
            self.score_student_tree.insert('', 'end', values=(
                student['student_id'],
                student['name']
            ))
    
    def search_students(self, event=None):
        """搜索学生"""
        keyword = self.student_search_var.get()
        
        # 清空现有数据
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        
        if keyword:
            students = self.system.search_students(keyword)
        else:
            students = self.system.get_all_students()
        
        for student in students:
            self.student_tree.insert('', 'end', values=(
                student['student_id'],
                student['name'],
                student['age'],
                student['grade'],
                student['class_name']
            ))
    
    def search_courses(self, event=None):
        """搜索课程"""
        keyword = self.course_search_var.get()
        
        # 清空现有数据
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)
        
        if keyword:
            courses = self.system.search_courses(keyword)
        else:
            courses = self.system.get_all_courses()
        
        for course in courses:
            self.course_tree.insert('', 'end', values=(
                course['course_id'],
                course['name'],
                course['teacher'],
                course['credit']
            ))
    
    def add_student_dialog(self):
        """添加学生对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加学生")
        dialog.geometry("300x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 创建输入字段
        fields = [
            ("姓名", tk.StringVar()),
            ("年龄", tk.StringVar()),
            ("年级", tk.StringVar()),
            ("班级", tk.StringVar())
        ]
        
        for i, (label, var) in enumerate(fields):
            ttk.Label(dialog, text=f"{label}:").grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(dialog, textvariable=var)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='we')
        
        def save_student():
            try:
                name = fields[0][1].get()
                age = int(fields[1][1].get())
                grade = fields[2][1].get()
                class_name = fields[3][1].get()
                
                if name and grade and class_name:
                    student_id = self.system.add_student(name, age, grade, class_name)
                    messagebox.showinfo("成功", f"学生添加成功，学号: {student_id}")
                    self.refresh_student_list()
                    dialog.destroy()
                else:
                    messagebox.showwarning("警告", "请填写所有必填字段")
            except ValueError:
                messagebox.showerror("错误", "年龄必须是数字")
        
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="保存", command=save_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def edit_student_dialog(self):
        """编辑学生对话框"""
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要编辑的学生")
            return
        
        item = self.student_tree.item(selected[0])
        student_id = item['values'][0]
        student_info = self.system.get_student_info(student_id)
        
        if not student_info:
            messagebox.showerror("错误", "未找到学生信息")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("编辑学生")
        dialog.geometry("300x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 创建输入字段
        fields = [
            ("姓名", tk.StringVar(value=student_info['name'])),
            ("年龄", tk.StringVar(value=str(student_info['age']))),
            ("年级", tk.StringVar(value=student_info['grade'])),
            ("班级", tk.StringVar(value=student_info['class_name']))
        ]
        
        for i, (label, var) in enumerate(fields):
            ttk.Label(dialog, text=f"{label}:").grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(dialog, textvariable=var)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='we')
        
        def update_student():
            try:
                name = fields[0][1].get()
                age = int(fields[1][1].get())
                grade = fields[2][1].get()
                class_name = fields[3][1].get()
                
                if name and grade and class_name:
                    self.system.update_student(student_id, name=name, age=age, 
                                             grade=grade, class_name=class_name)
                    messagebox.showinfo("成功", "学生信息更新成功")
                    self.refresh_student_list()
                    dialog.destroy()
                else:
                    messagebox.showwarning("警告", "请填写所有必填字段")
            except ValueError:
                messagebox.showerror("错误", "年龄必须是数字")
        
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="更新", command=update_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def delete_student(self):
        """删除学生"""
        selected = self.student_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要删除的学生")
            return
        
        item = self.student_tree.item(selected[0])
        student_id = item['values'][0]
        student_name = item['values'][1]
        
        if messagebox.askyesno("确认", f"确定要删除学生 {student_name} 吗？"):
            if self.system.remove_student(student_id):
                messagebox.showinfo("成功", "学生删除成功")
                self.refresh_student_list()
            else:
                messagebox.showerror("错误", "删除学生失败")
    
    def add_course_dialog(self):
        """添加课程对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加课程")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 创建输入字段
        fields = [
            ("课程名称", tk.StringVar()),
            ("任课教师", tk.StringVar()),
            ("学分", tk.StringVar())
        ]
        
        for i, (label, var) in enumerate(fields):
            ttk.Label(dialog, text=f"{label}:").grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(dialog, textvariable=var)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='we')
        
        def save_course():
            try:
                name = fields[0][1].get()
                teacher = fields[1][1].get()
                credit = float(fields[2][1].get())
                
                if name and teacher:
                    course_id = self.system.add_course(name, teacher, credit)
                    messagebox.showinfo("成功", f"课程添加成功，课程号: {course_id}")
                    self.refresh_course_list()
                    dialog.destroy()
                else:
                    messagebox.showwarning("警告", "请填写所有必填字段")
            except ValueError:
                messagebox.showerror("错误", "学分必须是数字")
        
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="保存", command=save_course).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def edit_course_dialog(self):
        """编辑课程对话框"""
        selected = self.course_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要编辑的课程")
            return
        
        item = self.course_tree.item(selected[0])
        course_id = item['values'][0]
        course_info = self.system.get_course_info(course_id)
        
        if not course_info:
            messagebox.showerror("错误", "未找到课程信息")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("编辑课程")
        dialog.geometry("300x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 创建输入字段
        fields = [
            ("课程名称", tk.StringVar(value=course_info['name'])),
            ("任课教师", tk.StringVar(value=course_info['teacher'])),
            ("学分", tk.StringVar(value=str(course_info['credit'])))
        ]
        
        for i, (label, var) in enumerate(fields):
            ttk.Label(dialog, text=f"{label}:").grid(row=i, column=0, padx=5, pady=5, sticky='e')
            entry = ttk.Entry(dialog, textvariable=var)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky='we')
        
        def update_course():
            try:
                # 课程更新逻辑类似学生更新
                messagebox.showinfo("提示", "课程编辑功能开发中...")
                dialog.destroy()
            except ValueError:
                messagebox.showerror("错误", "学分必须是数字")
        
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="更新", command=update_course).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def delete_course(self):
        """删除课程"""
        selected = self.course_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要删除的课程")
            return
        
        item = self.course_tree.item(selected[0])
        course_id = item['values'][0]
        course_name = item['values'][1]
        
        if messagebox.askyesno("确认", f"确定要删除课程 {course_name} 吗？"):
            if self.system.remove_course(course_id):
                messagebox.showinfo("成功", "课程删除成功")
                self.refresh_course_list()
            else:
                messagebox.showerror("错误", "删除课程失败")
    
    def enroll_student(self):
        """学生选课"""
        student_selected = self.enrollment_student_tree.selection()
        course_selected = self.available_course_tree.selection()
        
        if not student_selected or not course_selected:
            messagebox.showwarning("警告", "请同时选择学生和课程")
            return
        
        student_item = self.enrollment_student_tree.item(student_selected[0])
        course_item = self.available_course_tree.item(course_selected[0])
        
        student_id = student_item['values'][0]
        course_id = course_item['values'][0]
        
        if self.system.enroll_student_in_course(student_id, course_id):
            messagebox.showinfo("成功", "选课成功")
        else:
            messagebox.showerror("错误", "选课失败，可能已选过该课程")
    
    def drop_course(self):
        """学生退课"""
        student_selected = self.enrollment_student_tree.selection()
        course_selected = self.available_course_tree.selection()
        
        if not student_selected or not course_selected:
            messagebox.showwarning("警告", "请同时选择学生和课程")
            return
        
        student_item = self.enrollment_student_tree.item(student_selected[0])
        course_item = self.available_course_tree.item(course_selected[0])
        
        student_id = student_item['values'][0]
        course_id = course_item['values'][0]
        
        if self.system.drop_course(student_id, course_id):
            messagebox.showinfo("成功", "退课成功")
        else:
            messagebox.showerror("错误", "退课失败")
    
    def on_student_select_for_score(self, event):
        """选择学生时更新成绩列表"""
        selected = self.score_student_tree.selection()
        if not selected:
            return
        
        item = self.score_student_tree.item(selected[0])
        student_id = item['values'][0]
        
        # 清空成绩列表
        for item in self.score_course_tree.get_children():
            self.score_course_tree.delete(item)
        
        # 加载学生成绩
        student_info = self.system.get_student_info(student_id)
        if student_info:
            for course in student_info['course_details']:
                score = course['score'] if course['score'] is not None else "暂无成绩"
                self.score_course_tree.insert('', 'end', values=(
                    course['name'],
                    score
                ))
    
    def add_score_dialog(self):
        """添加成绩对话框"""
        student_selected = self.score_student_tree.selection()
        if not student_selected:
            messagebox.showwarning("警告", "请先选择学生")
            return
        
        student_item = self.score_student_tree.item(student_selected[0])
        student_id = student_item['values'][0]
        
        # 获取学生已选但未录入成绩的课程
        student_info = self.system.get_student_info(student_id)
        if not student_info:
            return
        
        available_courses = []
        for course in student_info['course_details']:
            if course['score'] is None:
                available_courses.append(course)
        
        if not available_courses:
            messagebox.showinfo("提示", "该学生所有课程都已录入成绩")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("录入成绩")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 课程选择
        ttk.Label(dialog, text="课程:").grid(row=0, column=0, padx=5, pady=5)
        course_var = tk.StringVar()
        course_combo = ttk.Combobox(dialog, textvariable=course_var, state="readonly")
        course_combo['values'] = [f"{c['course_id']} - {c['name']}" for c in available_courses]
        course_combo.grid(row=0, column=1, padx=5, pady=5)
        if available_courses:
            course_combo.current(0)
        
        # 成绩输入
        ttk.Label(dialog, text="成绩:").grid(row=1, column=0, padx=5, pady=5)
        score_var = tk.StringVar()
        score_entry = ttk.Entry(dialog, textvariable=score_var)
        score_entry.grid(row=1, column=1, padx=5, pady=5)
        
        def save_score():
            try:
                selected_course = course_combo.get()
                course_id = selected_course.split(' - ')[0]
                score = float(score_var.get())
                
                if 0 <= score <= 100:
                    if self.system.add_score(student_id, course_id, score):
                        messagebox.showinfo("成功", "成绩录入成功")
                        self.on_student_select_for_score(None)
                        dialog.destroy()
                    else:
                        messagebox.showerror("错误", "成绩录入失败")
                else:
                    messagebox.showwarning("警告", "成绩必须在0-100之间")
            except ValueError:
                messagebox.showerror("错误", "成绩必须是数字")
        
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="保存", command=save_score).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def edit_score_dialog(self):
        """修改成绩对话框"""
        student_selected = self.score_student_tree.selection()
        course_selected = self.score_course_tree.selection()
        
        if not student_selected or not course_selected:
            messagebox.showwarning("警告", "请先选择学生和课程")
            return
        
        student_item = self.score_student_tree.item(student_selected[0])
        course_item = self.score_course_tree.item(course_selected[0])
        
        student_id = student_item['values'][0]
        course_name = course_item['values'][0]
        current_score = course_item['values'][1]
        
        if current_score == "暂无成绩":
            messagebox.showwarning("警告", "该课程暂无成绩，请先录入")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("修改成绩")
        dialog.geometry("300x120")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 显示当前信息
        info_label = ttk.Label(dialog, text=f"学生: {student_item['values'][1]}\n课程: {course_name}\n当前成绩: {current_score}")
        info_label.pack(pady=10)
        
        # 新成绩输入
        score_frame = ttk.Frame(dialog)
        score_frame.pack(pady=5)
        
        ttk.Label(score_frame, text="新成绩:").pack(side=tk.LEFT, padx=5)
        new_score_var = tk.StringVar(value=str(current_score))
        score_entry = ttk.Entry(score_frame, textvariable=new_score_var, width=10)
        score_entry.pack(side=tk.LEFT, padx=5)
        
        def update_score():
            try:
                new_score = float(new_score_var.get())
                if 0 <= new_score <= 100:
                    # 获取课程ID
                    student_info = self.system.get_student_info(student_id)
                    course_id = None
                    for course in student_info['course_details']:
                        if course['name'] == course_name:
                            course_id = course['course_id']
                            break
                    
                    if course_id and self.system.add_score(student_id, course_id, new_score):
                        messagebox.showinfo("成功", "成绩修改成功")
                        self.on_student_select_for_score(None)
                        dialog.destroy()
                    else:
                        messagebox.showerror("错误", "成绩修改失败")
                else:
                    messagebox.showwarning("警告", "成绩必须在0-100之间")
            except ValueError:
                messagebox.showerror("错误", "成绩必须是数字")
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="更新", command=update_score).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def show_class_statistics(self):
        """显示班级统计"""
        grade = self.grade_var.get().strip()
        class_name = self.class_var.get().strip()
        
        if not grade or not class_name:
            messagebox.showwarning("警告", "请输入年级和班级")
            return
        
        stats = self.system.get_class_statistics(grade, class_name)
        
        self.stats_text.delete(1.0, tk.END)
        
        if stats:
            self.stats_text.insert(tk.END, f"{grade}{class_name}班统计信息\n")
            self.stats_text.insert(tk.END, f"{'='*30}\n")
            self.stats_text.insert(tk.END, f"总人数: {stats['total_students']}\n\n")
            
            self.stats_text.insert(tk.END, "年龄分布:\n")
            for age, count in sorted(stats['age_distribution'].items()):
                self.stats_text.insert(tk.END, f"  {age}岁: {count}人\n")
            
            self.stats_text.insert(tk.END, "\n课程选课统计:\n")
            for course_id, count in stats['course_enrollment'].items():
                course_name = stats['course_names'].get(course_id, "未知课程")
                self.stats_text.insert(tk.END, f"  {course_name}: {count}人\n")
        else:
            self.stats_text.insert(tk.END, "该班级暂无学生")
    
    def show_student_details(self, event):
        """显示学生详细信息"""
        selected = self.student_tree.selection()
        if not selected:
            return
        
        item = self.student_tree.item(selected[0])
        student_id = item['values'][0]
        student_info = self.system.get_student_info(student_id)
        
        if student_info:
            self.student_detail_text.delete(1.0, tk.END)
            self.student_detail_text.insert(tk.END, f"学生详细信息\n")
            self.student_detail_text.insert(tk.END, f"{'='*20}\n")
            self.student_detail_text.insert(tk.END, f"学号: {student_info['student_id']}\n")
            self.student_detail_text.insert(tk.END, f"姓名: {student_info['name']}\n")
            self.student_detail_text.insert(tk.END, f"年龄: {student_info['age']}\n")
            self.student_detail_text.insert(tk.END, f"年级: {student_info['grade']}\n")
            self.student_detail_text.insert(tk.END, f"班级: {student_info['class_name']}\n\n")
            
            self.student_detail_text.insert(tk.END, "已选课程:\n")
            for course in student_info['course_details']:
                score = course['score'] if course['score'] is not None else "暂无成绩"
                self.student_detail_text.insert(tk.END, f"  {course['name']} - {score}\n")
    
    def show_course_details(self, event):
        """显示课程详细信息"""
        selected = self.course_tree.selection()
        if not selected:
            return
        
        item = self.course_tree.item(selected[0])
        course_id = item['values'][0]
        course_info = self.system.get_course_info(course_id)
        
        if course_info:
            self.course_detail_text.delete(1.0, tk.END)
            self.course_detail_text.insert(tk.END, f"课程详细信息\n")
            self.course_detail_text.insert(tk.END, f"{'='*20}\n")
            self.course_detail_text.insert(tk.END, f"课程号: {course_info['course_id']}\n")
            self.course_detail_text.insert(tk.END, f"名称: {course_info['name']}\n")
            self.course_detail_text.insert(tk.END, f"教师: {course_info['teacher']}\n")
            self.course_detail_text.insert(tk.END, f"学分: {course_info['credit']}\n\n")
            
            self.course_detail_text.insert(tk.END, "选课学生:\n")
            for student in course_info['student_details']:
                score = student['score'] if student['score'] is not None else "暂无成绩"
                self.course_detail_text.insert(tk.END, f"  {student['name']} - {score}\n")
    
    def save_data(self):
        """保存数据"""
        self.system.save_data()
        messagebox.showinfo("成功", "数据保存成功")
    
    def show_about(self):
        """显示关于信息"""
        messagebox.showinfo("关于", "学生管理系统\n版本: 1.0\n作者: AI Assistant")


def main():
    """GUI主函数"""
    root = tk.Tk()
    app = StudentManagementGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()