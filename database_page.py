import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, FrameBreak, PageTemplate, BaseDocTemplate, Frame
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
import tempfile
import subprocess
import platform
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from edit_report_page import EditReportPage
import shutil

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

    def calculate_age(self, birth_date):
        today = datetime.now()
        birth_date = datetime.strptime(birth_date, "%Y/%m/%d")
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age

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
            
        basic_info = data.get("基本信息", {})

        examiner = basic_info.get('检查医生', '_________________')
        doc = CustomDocTemplate(pdf_path, examiner, self.font_name, pagesize=letter,
                                leftMargin=20, rightMargin=20,
                                topMargin=20, bottomMargin=20)
        
        elements = []
        styles = getSampleStyleSheet()
        
        pdfmetrics.registerFont(TTFont(self.font_name, self.font_path))
        styles['Title'].fontName = self.font_name
        styles['Heading1'].fontName = self.font_name
        styles['Heading2'].fontName = self.font_name
        styles['Heading2'].fontSize = 12
        styles['Heading2'].bold = True
        styles['Heading2'].alignment = 0
        styles['Normal'].fontName = self.font_name

        # 标题
        # elements.append(Paragraph("四川大学华西医院耳鼻咽喉头颈外科", styles['Title']))
        # I want the title to be left aligned and more left offset
        title_paragraph = Paragraph("前庭功能检测报告单", styles['Title'])
        elements.append(title_paragraph)
        elements.append(Spacer(1, 4))
        
        # 添加双横线
        elements.append(Paragraph("=" * 100, styles['Normal']))

        # 基本信息
        birth_date = basic_info.get("出生日期", "")
        age = f"{self.calculate_age(birth_date)}岁" if birth_date else ""
        
        basic_info_data = [
            ["登记号/住院号:", basic_info.get("ID", ""), "姓名:", basic_info.get("姓名", ""), "性别:", basic_info.get("性别", ""), "年龄:", age],
            ["医嘱项目:", basic_info.get("检查项目", ""), "测试设备:", basic_info.get("检查设备", ""),  "检查日期:", basic_info.get("检查时间", "")],
        ]

        basic_info_table = Table(basic_info_data, colWidths=[doc.width/8, doc.width/8, doc.width/8, doc.width/8, doc.width/8, doc.width/8, doc.width/8, doc.width/8])
        basic_info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 1),
            ('BOTTOMPADDING', (0, 0), (0, 0), 0),
        ]))
        elements.append(basic_info_table)
        
        # 添加单横线
        elements.append(Paragraph("-" * 100, styles['Normal']))
        
        test_results_list = []
        
        # 凝视性眼震
        
        ## check if gaze data exists
        
        gaze_data = data.get("凝视性眼震", {})

        has_gaze_data = any([
            gaze_data.get("凝视性眼震模式（右）"),
            gaze_data.get("凝视性眼震速度（右）"),
            gaze_data.get("凝视性眼震模式（左）"),
            gaze_data.get("凝视性眼震速度（左）"),
            gaze_data.get("凝视性眼震模式（上）"),
            gaze_data.get("凝视性眼震速度（上）"),
            gaze_data.get("凝视性眼震模式（下）"),
            gaze_data.get("凝视性眼震速度（下）"),
            gaze_data.get("凝视性眼震检查结果")
        ])

        if has_gaze_data:
            
            gaze_data_title = Paragraph("凝视试验 (gaze test):", styles['Heading2'])
            elements.append(gaze_data_title)
            elements.append(Spacer(1, 6))

            # 创建一个表格来呈现凝视眼震的结果
            gaze_table_data = [
                ["方向", "凝视性眼震模式", "凝视性眼震速度 (°/s)"],
                ["右凝视", gaze_data.get("凝视性眼震模式（右）", ""), gaze_data.get("凝视性眼震速度（右）", "")],
                ["左凝视", gaze_data.get("凝视性眼震模式（左）", ""), gaze_data.get("凝视性眼震速度（左）", "")],
                ["上凝视", gaze_data.get("凝视性眼震模式（上）", ""), gaze_data.get("凝视性眼震速度（上）", "")],
                ["下凝视", gaze_data.get("凝视性眼震模式（下）", ""), gaze_data.get("凝视性眼震速度（下）", "")]
            ]

            gaze_table = Table(gaze_table_data, colWidths=[doc.width/8, doc.width/3, doc.width/5])
            gaze_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), self.font_name),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(gaze_table)
            elements.append(Spacer(1, 6))

            gaze_result = Paragraph(f"凝视性眼震检查结果: {gaze_data.get('凝视性眼震检查结果', '')}", styles['Normal'])
            test_results_list.append(gaze_result)
            elements.append(gaze_result)
            elements.append(Spacer(1, 6))
            
        # 自发性眼震
        spontaneous_data = data.get("自发性眼震", {})

        # 检查是否有任何自发性眼震的具体数据
        has_spontaneous_data = any([
            spontaneous_data.get("自发性眼震模式"),
            spontaneous_data.get("自发性眼震速度"),
            spontaneous_data.get("自发性眼震检查结果")
        ])

        if has_spontaneous_data:
            spontaneous_title = Paragraph("自发性眼震 (spontaneous nystagmus):", styles['Heading2'])
            spontaneous_title.alignment = 0  # 左对齐
            elements.append(spontaneous_title)
            elements.append(Spacer(1, 6))

            # 创建一个表格来呈现自发性眼震的结果
            spontaneous_table_data = [
                ["模式:", spontaneous_data.get("自发性眼震模式", ""), "速度（度/s）:", spontaneous_data.get("自发性眼震速度", ""), "结果:", spontaneous_data.get("自发性眼震检查结果", "")],
            ]

            # 创建表格
            spontaneous_table = Table(spontaneous_table_data, colWidths=[doc.width/6, doc.width/6, doc.width/6])
            spontaneous_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), self.font_name),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 1),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
                ('RIGHTPADDING', (0, 0), (0, -1), 20),  # 在标签和值之间添加更多空间
            ]))
            elements.append(spontaneous_table)
            elements.append(Spacer(1, 6))
            
            # 温度试验
            caloric_data = data.get("温度试验", {})

            if caloric_data:
                caloric_title = Paragraph("温度试验 (caloric test):", styles['Heading2'])
                elements.append(caloric_title)
                elements.append(Spacer(1, 6))

                caloric_table_data = [
                    ["项目", "结果"],
                    ["单侧减弱侧别 (UW)", caloric_data.get("单侧减弱侧别 (UW)", "")],
                    ["单侧减弱数值 (UW, %)", caloric_data.get("单侧减弱数值 (UW, %)", "")],
                    ["优势偏向侧别 (DP)", caloric_data.get("优势偏向侧别 (DP)", "")],
                    ["优势偏向数值 (DP, 度/秒)", caloric_data.get("优势偏向数值 (DP, 度/秒)", "")],
                    ["最大慢相速度总和（右耳, 度/秒）", caloric_data.get("最大慢相速度总和（右耳, 度/秒）", "")],
                    ["最大慢相速度总和（左耳, 度/秒）", caloric_data.get("最大慢相速度总和（左耳, 度/秒）", "")],
                    ["固视抑制指数 (FI, %)", caloric_data.get("固视抑制指数 (FI, %)", "")]
                ]

                caloric_table = Table(caloric_table_data, colWidths=[doc.width/3, doc.width/4])
                caloric_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, -1), self.font_name),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                elements.append(caloric_table)
                elements.append(Spacer(1, 6))

                caloric_result = Paragraph(f"温度试验检查结果: {caloric_data.get('检查结果', '')}", styles['Normal'])
                elements.append(caloric_result)
                elements.append(Spacer(1, 12))
            
        
        # all test results
        # for result in test_results_list:
        #     elements.append(result)
        #     elements.append(Spacer(1, 6))

        # # 检查者
        # examiner = Paragraph(f"检查者: {basic_info.get('检查医生', '_________________')}", styles['Normal'])
        # examiner.alignment = 2  # 右对齐
        # elements.append(examiner)

        # 生成PDF
        doc.build(elements)

        # 打开生成的PDF
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



