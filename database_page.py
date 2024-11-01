import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, FrameBreak, PageTemplate, BaseDocTemplate, Frame, Image as ReportLabImage
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
import tempfile
import subprocess
import platform
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from edit_report_page import EditReportPage
import shutil
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage
import io
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side

def is_dict_empty(d):
    """
    检查字典中的所有值是否为空
    空的定义: None, "", [], {}, 0, "0", "未知", "无"
    返回: True 如果所有值都为空，False 如果存在非空值
    """
    empty_values = [None, "", [], {}, 0, "0", "未知", "无"]
    return all(value in empty_values or (isinstance(value, str) and value.strip() == "") 
              for value in d.values())

class MyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        BaseDocTemplate.__init__(self, filename, **kw)
        frame = Frame(
            self.leftMargin, self.bottomMargin, 
            self.width, self.height, 
            id='normal'
        )
        template = PageTemplate('normal', [frame], onPage=self.add_page_elements)
        self.addPageTemplates([template])

    def add_page_elements(self, canvas, doc):
        canvas.saveState()
        canvas.setFont(self.font_name, 10)
        canvas.drawRightString(doc.pagesize[0] - 1*cm, 1*cm, f"检查者: {self.examiner}")
        canvas.restoreState()

class CustomDocTemplate(MyDocTemplate):
    def __init__(self, filename, examiner, font_name, **kw):
        self.examiner = examiner
        self.font_name = font_name
        MyDocTemplate.__init__(self, filename, **kw)

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

        # 创建按钮架
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

    def calculate_age(self, birth_date):
        today = datetime.now()
        birth_date = datetime.strptime(birth_date, "%Y/%m/%d")
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age

    def view_report(self):
        """生成检查报告"""
        selected_item = self.report_tree.selection()
        if not selected_item:
            messagebox.showwarning("警告", "请先选择一个报告")
            return

        # 读取报告数据
        file_path = self.report_tree.item(selected_item)['tags'][0]
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        base_path = os.path.dirname(__file__)

        # 加载Excel模板
        template_path = os.path.join(base_path, "template", "report_template.xlsx")
        wb = openpyxl.load_workbook(template_path)
        ws = wb.active

        # 填充基本信息
        basic_info = data.get("基本信息", {})
        ws['B3'] = basic_info.get("ID", "")
        ws['E3'] = basic_info.get("姓名", "")
        ws['H3'] = basic_info.get("性别", "")
        ws['K3'] = basic_info.get("出生日期", "")
        ws['N3'] = basic_info.get("检查时间", "")
        ws['Q3'] = basic_info.get("检查设备", "")
        ws['T3'] = basic_info.get("检查医生", "")

        # 填充自发性眼震动(spontaneous nystagmus)
        spontaneous_nystagmus = data.get("自发性眼震", {})
        if not is_dict_empty(spontaneous_nystagmus):
            ws.merge_cells('A7:C7')
            ws.merge_cells('D7:F7')
            ws.merge_cells('G7:I7')
            ws.merge_cells('K7:M7')
            
            ws['A7'] = spontaneous_nystagmus.get("自发性眼震模式", "")
            ws['D7'] = spontaneous_nystagmus.get("自发性眼震速度", "")
            ws['G7'] = spontaneous_nystagmus.get("自发性眼震固视抑制", "")
            ws['K7'] = spontaneous_nystagmus.get("自发性眼震检查结果", "")
        else:
            pass
        
        # 摇头试验
        head_shake_test = data.get("摇头试验", {})
        if not is_dict_empty(head_shake_test):
            
            ws.merge_cells('A11:C11')
            ws.merge_cells('D11:E11')
            ws.merge_cells('F11:G11')
            ws.merge_cells('I11:M11')
            
            ws['A11'] = head_shake_test.get("眼震模式", "")
            ws['D11'] = head_shake_test.get("摇头方向", "")
            ws['F11'] = head_shake_test.get("眼震速度", "")
            ws['I11'] = head_shake_test.get("检查结果", "")
            
        else:
            pass
        
        
        # 凝视性眼震
        gaze_nystagmus = data.get("凝视性眼震", {})
        if not is_dict_empty(gaze_nystagmus):
            
            ws.merge_cells('C15:D15')
            ws.merge_cells('E15:F15')
            ws.merge_cells('G15:H15')
            ws.merge_cells('I15:J15')
            
            ws.merge_cells('C16:D16')
            ws.merge_cells('E16:F16')
            ws.merge_cells('G16:H16')
            ws.merge_cells('I16:J16')
            
            ws.merge_cells('L15:M16')
            
            ws['C15'] = gaze_nystagmus.get("凝视性眼震模式（左）", "")
            ws['E15'] = gaze_nystagmus.get("凝视性眼震模式（右）", "")
            ws['G15'] = gaze_nystagmus.get("凝视性眼震模式（上）", "")
            ws['I15'] = gaze_nystagmus.get("凝视性眼震模式（下）", "")
            
            ws['C16'] = gaze_nystagmus.get("凝视性眼震速度（左）", "")
            ws['E16'] = gaze_nystagmus.get("凝视性眼震速度（右）", "")
            ws['G16'] = gaze_nystagmus.get("凝视性眼震速度（上）", "")
            ws['I16'] = gaze_nystagmus.get("凝视性眼震速度（下）", "")
            
            ws['L15'] = gaze_nystagmus.get("凝视性眼震检查结果", "")
            
        else:
            pass
        
        # 保存生成的报告
        output_path = os.path.join(tempfile.gettempdir(), f"report_{basic_info.get('ID', 'temp')}.xlsx")
        wb.save(output_path)
        
        # 打开生成的报告
        if platform.system() == "Windows":
            os.startfile(output_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.call(["open", output_path])
        else:  # Linux
            subprocess.call(["xdg-open", output_path])

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



