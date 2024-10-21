import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile
import subprocess
import platform
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from edit_report_page import EditReportPage
import shutil

class DatabasePage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.db_path = self.controller.db_path
        self.config_file = self.controller.config_file
        self.load_config()
        self.create_widgets()


    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # 创建搜索框
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        ttk.Label(search_frame, text="搜索:").grid(row=0, column=0, padx=(0, 5))
        self.search_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_var, width=30).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(search_frame, text="搜索", command=self.search_reports).grid(row=0, column=2)

        # 创建报告列表
        self.report_tree = ttk.Treeview(main_frame, columns=('ID', '姓名', '检查时间'), show='headings')
        self.report_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.report_tree.heading('ID', text='患者ID')
        self.report_tree.heading('姓名', text='姓名')
        self.report_tree.heading('检查时间', text='检查时间')

        # 添加滚动条
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.report_tree.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.report_tree.configure(yscrollcommand=scrollbar.set)

        # 创建按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        ttk.Button(button_frame, text="查看详情", command=self.view_report).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="编辑报告", command=self.edit_report).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(button_frame, text="删除报告", command=self.delete_report).grid(row=0, column=2)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.report_tree.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.report_tree.configure(yscrollcommand=scrollbar.set)
        
        ttk.Button(button_frame, text="刷新列表", command=self.load_reports).grid(row=0, column=3, padx=(5, 0))

        # 加载报告数据
        self.load_reports()

    def load_reports(self):
        self.report_tree.delete(*self.report_tree.get_children())  # 清空现有的报告列表
        report_folder = os.path.join(self.db_path, "report")
        
        for date_folder in os.listdir(report_folder):
            date_path = os.path.join(report_folder, date_folder)
            if os.path.isdir(date_path):
                for report_file in os.listdir(date_path):
                    if report_file.endswith('.json'):
                        file_path = os.path.join(date_path, report_file)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        basic_info = data.get("基本信息", {})
                        patient_id = basic_info.get("ID", "未知")
                        name = basic_info.get("姓名", "未知")
                        exam_time = basic_info.get("检查时间", "未知")
                        
                        self.report_tree.insert("", "end", values=(patient_id, name, exam_time), tags=(file_path,))

        # 按检查时间排序
        # self.report_tree.set_children('', sorted(self.report_tree.get_children(''), key=lambda x: self.report_tree.item(x)['values'][2], reverse=True))

    def search_reports(self):
        # 实现搜索功能
        pass

    def view_report(self):
        selected_item = self.report_tree.selection()
        if not selected_item:
            messagebox.showwarning("警告", "请先选择一个报告")
            return

        file_path = self.report_tree.item(selected_item)['tags'][0]
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            pdf_path = tmp_file.name

        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        pdfmetrics.registerFont(TTFont(self.font_name, self.font_path))
        styles['Title'].fontName = self.font_name
        styles['Heading2'].fontName = self.font_name
        styles['Normal'].fontName = self.font_name

        elements.append(Paragraph("前庭功能检查报告", styles['Title']))
        elements.append(Spacer(1, 12))

        def add_table(data):
            table_data = []
            for key, value in data.items():
                if isinstance(value, dict):
                    table_data.append([Paragraph(key, styles['Heading2']), ''])
                    table_data.extend(add_table(value))
                elif value:
                    table_data.append([Paragraph(key, styles['Normal']), Paragraph(str(value), styles['Normal'])])
            
            if table_data:
                t = Table(table_data, colWidths=[doc.width/2.5, doc.width/2.5])
                t.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), self.font_name),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('TOPPADDING', (0, 0), (-1, -1), 3),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                return t
            return None

        for test_name, test_data in data.items():
            elements.append(Paragraph(test_name, styles['Heading2']))
            elements.append(Spacer(1, 6))
            if isinstance(test_data, dict):
                table = add_table(test_data)
                if table:
                    elements.append(table)
            elements.append(Spacer(1, 12))

        doc.build(elements)

        if platform.system() == "Windows":
            os.startfile(pdf_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.call(["open", pdf_path])
        else:  # Linux和其他类Unix系统
            subprocess.call(["xdg-open", pdf_path])

    def edit_report(self):
        selected_item = self.report_tree.selection()
        if not selected_item:
            messagebox.showwarning("警告", "请先选择一个报告")
            return

        file_path = self.report_tree.item(selected_item)['tags'][0]
        edit_page = EditReportPage(self, file_path)
        self.wait_window(edit_page)
        # 刷新报告列表
        self.load_reports()

    def delete_report(self):
        selected_item = self.report_tree.selection()
        if not selected_item:
            messagebox.showwarning("警告", "请先选择一个报告")
            return

        if messagebox.askyesno("确认", "确定要删除选中的报告吗？"):
            file_path = self.report_tree.item(selected_item)['tags'][0]
            
            # 创建删除的归档目录
            deleted_report_dir = os.path.join(self.db_path, "arch", "deleted", "report")
            deleted_pic_dir = os.path.join(self.db_path, "arch", "deleted", "pic")
            os.makedirs(deleted_report_dir, exist_ok=True)
            os.makedirs(deleted_pic_dir, exist_ok=True)

            # 获取当前日期和时间
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

            # 移动报告文件
            report_filename = os.path.basename(file_path)
            new_report_filename = f"{os.path.splitext(report_filename)[0]}_{current_time}{os.path.splitext(report_filename)[1]}"
            shutil.move(file_path, os.path.join(deleted_report_dir, new_report_filename))

            # 移动相关图片
            with open(os.path.join(deleted_report_dir, new_report_filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for test_name in ['头脉冲试验', '头脉冲抑制试验']:
                if test_name in data and f'{test_name}示意图' in data[test_name]:
                    pic_path = data[test_name][f'{test_name}示意图']
                    if os.path.exists(os.path.join(self.db_path, pic_path)):
                        pic_filename = os.path.basename(pic_path)
                        new_pic_filename = f"{os.path.splitext(pic_filename)[0]}_{current_time}{os.path.splitext(pic_filename)[1]}"
                        shutil.move(os.path.join(self.db_path, pic_path), os.path.join(deleted_pic_dir, new_pic_filename))

            # 从树形视图中删除项目
            self.report_tree.delete(selected_item)

            messagebox.showinfo("成功", "报告已成功删除并归档")

    def load_config(self):
        config = json.load(open(self.config_file, 'r'))
        self.font_name = config['font_name']
        self.font_path = config['font_path']
    
    def get_data(self):
        return {}
