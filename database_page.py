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
import uuid

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
        
        
        # 头脉冲试验
        head_impulse = data.get("头脉冲试验", "")
        if not is_dict_empty(head_impulse):
            
            ws.merge_cells('J20:M22')
            
            ws['C20'] = head_impulse.get("VOR增益 (左外半规管)", "")
            ws['D20'] = head_impulse.get("VOR增益 (右外半规管)", "")
            ws['E20'] = head_impulse.get("VOR增益 (左前半规管)", "")
            ws['F20'] = head_impulse.get("VOR增益 (右后半规管)", "")
            ws['G20'] = head_impulse.get("VOR增益 (左后半规管)", "")
            ws['H20'] = head_impulse.get("VOR增益 (右前半规管)", "")
            
            ws['C21'] = head_impulse.get("PR分数 (左外半规管)", "")
            ws['D21'] = head_impulse.get("PR分数 (右外半规管)", "")
            ws['E21'] = head_impulse.get("PR分数 (左前半规管)", "")
            ws['F21'] = head_impulse.get("PR分数 (右后半规管)", "")
            ws['G21'] = head_impulse.get("PR分数 (左后半规管)", "")
            ws['H21'] = head_impulse.get("PR分数 (右前半规管)", "")
        
            ws['J20'] = head_impulse.get("头脉冲试验检查结果", "")
            
            sccade_wave = head_impulse.get("头脉冲试验扫视波", [])
            if '阴性' in sccade_wave or '配合欠佳' in sccade_wave:
                ws.merge_cells('C22:H22')
                
                if '配合欠佳' in sccade_wave:
                    ws['C22'] = '配合欠佳'
                else:
                    ws['C22'] = '阴性'
                
            else:
                for i, option in enumerate(sccade_wave):
                    if option == "左外半规管":
                        ws['C22'] = '√'
                    elif option == "右外半规管":
                        ws['D22'] = '√'
                    elif option == "左前半规管":
                        ws['E22'] = '√'
                    elif option == "右后半规管":
                        ws['F22'] = '√'
                    elif option == "左后半规管":
                        ws['G22'] = '√'
                    elif option == "右前半规管":
                        ws['H22'] = '√'
            
            if head_impulse.get("头脉冲试验示意图") != "":
                pic_path = os.path.join(self.db_path, head_impulse.get("头脉冲试验示意图"))
                if os.path.exists(pic_path):
                    img = openpyxl.drawing.image.Image(pic_path)
                    img.anchor = 'O7'
                    
                    cell_width = 6
                    cell_height = 9
                    
                    img.width = cell_width * 60
                    img.height = cell_height * 18
                    
                    ws.add_image(img)
            
        else:
            pass
        
        # 头脉冲抑制试验
        head_suppression = data.get("头脉冲抑制试验", "")
        if not is_dict_empty(head_suppression):
            
            ws.merge_cells('C26:D26')
            ws.merge_cells('C27:D27')
            ws.merge_cells('E26:F26')
            ws.merge_cells('E27:F27')
            ws.merge_cells('H26:M27')
            
            ws['C26'] = head_suppression.get("头脉冲抑制试验增益 (左外半规管)", "")
            ws['C27'] = head_suppression.get("头脉冲抑制试验增益 (右外半规管)", "")
            
            sccade_wave = head_suppression.get("头脉冲抑制试验补偿性扫视波", [])
            if '阴性' in sccade_wave:
                ws['E26'] = '阴性'
                ws['E27'] = '阴性'
            elif '配合欠佳' in sccade_wave:
                ws['E26'] = '配合欠佳'
                ws['E27'] = '配合欠佳'
            
            else:
                if '左外半规管' in sccade_wave:
                    ws['E26'] = '√'
                if '右外半规管' in sccade_wave:
                    ws['E27'] = '√'
            
            ws['H26'] = head_suppression.get("头脉冲抑制试验检查结果", "")
            
            if head_suppression.get("头脉冲抑制试验示意图") != "":
                pic_path = os.path.join(self.db_path, head_suppression.get("头脉冲抑制试验示意图"))
                if os.path.exists(pic_path):
                    img = openpyxl.drawing.image.Image(pic_path)
                    img.anchor = 'O18'
                    
                    cell_width = 6
                    cell_height = 20
                    
                    img.width = cell_width * 60
                    img.height = cell_height * 18
                    
                    ws.add_image(img)
        else:
            pass
        
        # 眼位反向偏斜（skew deviation）
        skew_deviation = data.get("眼位反向偏斜", "")
        if not is_dict_empty(skew_deviation):
            
            ws.merge_cells('A31:C31')
            ws.merge_cells('D31:F31')
            ws.merge_cells('H31:M31')
            
            ws['A31'] = skew_deviation.get("眼位反向偏斜 (HR, 度)", "")
            ws['D31'] = skew_deviation.get("眼位反向偏斜 (VR, 度)", "")
            ws['H31'] = skew_deviation.get("眼位反向偏斜检查结果", "")
            
        else:
            pass
        
        # 视觉增强前庭-眼反射试验 (VVOR)
        vvor = data.get("视觉增强前庭-眼反射试验", "")
        if not is_dict_empty(vvor):
            
            ws.merge_cells('C34:F34')
            ws['C34'] = vvor.get("检查结果", "")
            
        else:
            pass
        
        # 前庭-眼反射抑制试验（VOR suppression）
        vor_suppression = data.get("前庭-眼反射抑制试验", "")
        if not is_dict_empty(vor_suppression):
            
            ws.merge_cells('J34:M34')
            ws['J34'] = vor_suppression.get("检查结果", "")
            
        else:
            pass
        
        # 扫视检查
        pursuit_test = data.get("扫视检查", "")
        if not is_dict_empty(pursuit_test):
            
            ws.merge_cells('B38:C38')
            ws.merge_cells('D38:E38')
            ws.merge_cells('F38:G38')
            ws.merge_cells('B39:C39')
            ws.merge_cells('D39:E39')
            ws.merge_cells('F39:G39')
            ws.merge_cells('I38:M39')
            
            ws['B38'] = pursuit_test.get("扫视延迟时间 (左向, 毫秒)", "")
            ws['B39'] = pursuit_test.get("扫视延迟时间 (右向, 毫秒)", "")
            ws['D38'] = pursuit_test.get("扫视峰速度 (左向, 度/秒)", "")
            ws['D39'] = pursuit_test.get("扫视峰速度 (右向, 度/秒)", "")
            ws['F38'] = pursuit_test.get("扫视精确度 (左向, %)", "")
            ws['F39'] = pursuit_test.get("扫视精确度 (右向, %)", "")
            
            ws['I38'] = pursuit_test.get("扫视检查结果", "")
            
        else:
            pass
        
        # Dix-Hallpike试验
        dix_hallpike = data.get("位置试验 (Dix-Hallpike试验)", "")
        if not is_dict_empty(dix_hallpike):
            
            ws.merge_cells('B43:C43')
            ws.merge_cells('D43:E43')
            ws.merge_cells('F43:G43')
            ws.merge_cells('J43:K43')
            ws.merge_cells('L43:M43')
            
            ws.merge_cells('B44:C44')
            ws.merge_cells('D44:E44')
            ws.merge_cells('F44:G44')
            ws.merge_cells('J44:K44')
            ws.merge_cells('L44:M44')
            
            ws.merge_cells('C46:M46')
            
            ws['B43'] = dix_hallpike.get("左侧眼震模式", "")
            ws['D43'] = dix_hallpike.get("左侧坐起眼震模式", "")
            ws['F43'] = dix_hallpike.get("左侧出现眩晕/头晕", "")
            ws['H43'] = dix_hallpike.get("左侧眼震潜伏期 (秒)", "")
            ws['I43'] = dix_hallpike.get("左侧眼震持续时长 (秒)", "")
            ws['J43'] = dix_hallpike.get("左侧眼震最大速度 (度/秒)", "")
            ws['L43'] = dix_hallpike.get("左侧眼震疲劳性", "")
            
            ws['B44'] = dix_hallpike.get("右侧眼震模式", "")
            ws['D44'] = dix_hallpike.get("右侧坐起眼震模式", "")
            ws['F44'] = dix_hallpike.get("右侧出现眩晕/头晕", "")
            ws['H44'] = dix_hallpike.get("右侧眼震潜伏期 (秒)", "")
            ws['I44'] = dix_hallpike.get("右侧眼震持续时长 (秒)", "")
            ws['J44'] = dix_hallpike.get("右侧眼震最大速度 (度/秒)", "")
            ws['L44'] = dix_hallpike.get("右侧眼震疲劳性", "")
            
            ws['C46'] = dix_hallpike.get("检查结果", "")
            
        else:
            pass
        
        # 仰卧滚转试验
        supine_roll = data.get("位置试验 (仰卧滚转试验)", "")
        if not is_dict_empty(supine_roll):
            
            ws.merge_cells('B50:C50')
            ws.merge_cells('D50:E50')
            ws.merge_cells('H50:I50')
            
            ws.merge_cells('B51:C51')
            ws.merge_cells('D51:E51')
            ws.merge_cells('H51:I51')
            
            ws.merge_cells('K50:M51')
            
            ws['B50'] = supine_roll.get("左侧眼震模式", "")
            ws['D50'] = supine_roll.get("左侧出现眩晕/头晕", "")
            ws['F50'] = supine_roll.get("左侧眼震潜伏期 (秒)", "")
            ws['G50'] = supine_roll.get("左侧眼震持续时长 (秒)", "")
            ws['H50'] = supine_roll.get("左侧眼震最大速度 (度/秒)", "")
            
            ws['B51'] = supine_roll.get("右侧眼震模式", "")
            ws['D51'] = supine_roll.get("右侧出现眩晕/头晕", "")
            ws['F51'] = supine_roll.get("右侧眼震潜伏期 (秒)", "")
            ws['G51'] = supine_roll.get("右侧眼震持续时长 (秒)", "")
            ws['H51'] = supine_roll.get("右侧眼震最大速度 (度/秒)", "")
            
            ws['K50'] = supine_roll.get("检查结果", "")
            
        else:
            pass
        
        
        # 位置试验（其他）
        other_position_test = data.get("位置试验(其他)", "")
        if not is_dict_empty(other_position_test):
            
            ws.merge_cells('A57:C57')
            ws.merge_cells('D57:F57')
            ws.merge_cells('G57:I57')
            ws.merge_cells('J57:M57')
            
            ws.merge_cells('C59:M59')
            
            ws['A57'] = other_position_test.get("坐位-平卧试验", "")
            ws['D57'] = other_position_test.get("坐位-低头试验", "")
            ws['G57'] = other_position_test.get("坐位-仰头试验", "")
            ws['J57'] = other_position_test.get("零平面", "")
            
            ws['C59'] = other_position_test.get("检查结果", "")
            
        else:
            pass
        
        # 视跟踪
        visual_tracking = data.get("视跟踪", "")
        if not is_dict_empty(visual_tracking):
            
            ws.merge_cells('A63:B63')
            ws.merge_cells('C63:D63')
            
            ws.merge_cells('F63:M63')
            
            ws['A63'] = visual_tracking.get("视跟踪曲线分型", "")
            ws['C63'] = visual_tracking.get("视跟踪增益", "")
            ws['F63'] = visual_tracking.get("视跟踪检查结果", "")
            
        else:
            pass
        
        # 视动性眼震
        spontaneous_nystagmus = data.get("视动性眼震", "")
        if not is_dict_empty(spontaneous_nystagmus):
            
            ws.merge_cells('L67:M67')
            
            ws['B67'] = spontaneous_nystagmus.get("向左视标增益", "")
            ws['C67'] = spontaneous_nystagmus.get("向右视标增益", "")
            ws['D67'] = spontaneous_nystagmus.get("向上视标增益", "")
            ws['E67'] = spontaneous_nystagmus.get("向下视标增益", "")
            
            ws['I67'] = spontaneous_nystagmus.get("水平视标不对称性（%）", "")
            ws['J67'] = spontaneous_nystagmus.get("垂直视标不对称性（%）", "")
            
            ws['L67'] = spontaneous_nystagmus.get("检查结果", "")
            
        else:
            pass
        
        # 瘘管试验
        laceration_test = data.get("瘘管试验", "")
        if not is_dict_empty(laceration_test):
            
            positive_options = laceration_test.get("瘘管试验", [])
            
            if '配合欠佳' in positive_options:
                
                ws.merge_cells('B71:C72')
                ws['B71'] = '配合欠佳'
                
            elif '阴性' in positive_options:
                
                ws['B71'] = '阴性'
                ws['B72'] = '阴性'
                    
            elif '双耳阳性' in positive_options:
                ws['B71'] = "阳性"
                ws['B72'] = "阳性"
                
            elif '双耳弱阳性' in positive_options:
                ws['B71'] = "弱阳性"
                ws['B72'] = "弱阳性"
            
            elif '右耳阳性' in positive_options:
                ws['B72'] = "阳性"
                ws['B71'] = "阴性"
                
            elif '左耳阳性' in positive_options:
                ws['B72'] = "阴性"
                ws['B71'] = "阳性"
                
            elif '右耳弱阳性' in positive_options:
                ws['B72'] = "弱阳性"
                ws['B71'] = "阴性"
                
            elif '左耳弱阳性' in positive_options:
                ws['B72'] = "阴性"
                ws['B71'] = "弱阳性"
            
            ws['E71'] = laceration_test.get("检查结果", "")
            
        else:
            pass
        
        # 温度试验
        temperature_test = data.get("温度试验", "")
        if not is_dict_empty(temperature_test):
            
            ws.merge_cells('D75:E75')
            ws.merge_cells('J75:K75')
            ws.merge_cells('Q75:R75')
            ws.merge_cells('D76:E76')
            ws.merge_cells('J76:K76')
            ws.merge_cells('Q76:R76')
            
            ws.merge_cells('D78:E78')
            ws.merge_cells('J78:R78')
            
            ws.merge_cells('O57:T72')
            
            ws['D75'] = temperature_test.get("单侧减弱侧别 (UW)", "")
            ws['D76'] = temperature_test.get("单侧减弱数值 (UW, %)", "")
            ws['J75'] = temperature_test.get("优势偏向侧别 (DP)", "")
            ws['J76'] = temperature_test.get("优势偏向数值 (DP, 度/秒)", "")
            ws['Q75'] = temperature_test.get("最大慢相速度总和（右耳, 度/秒）", "")
            ws['Q76'] = temperature_test.get("最大慢相速度总和（左耳, 度/秒）", "")
            ws['D78'] = temperature_test.get("固视抑制指数 (FI, %)", "")
            ws['J78'] = temperature_test.get("检查结果", "")
            
            pic_path = temperature_test.get("温度试验示意图", "")
            if pic_path != '':
                pic_path = os.path.join(self.db_path, head_impulse.get("头脉冲试验示意图"))
                if os.path.exists(pic_path):
                    img = openpyxl.drawing.image.Image(pic_path)
                    img.anchor = 'O58'
                    
                    cell_width = 6
                    cell_height = 22
                    
                    img.width = cell_width * 60
                    img.height = cell_height * 18
                    
                    ws.add_image(img)
            
            
            
        else:
            pass
        
        # 颈肌前庭诱发肌源性电位
        cervical_evoked_myogenic_potential = data.get("颈肌前庭诱发肌源性电位 (cVEMP)", "")
        if not is_dict_empty(cervical_evoked_myogenic_potential):
            
            ws.merge_cells('B82:C82')
            ws.merge_cells('D82:E82')
            ws.merge_cells('F82:G82')
            ws.merge_cells('H82:J82')
            ws.merge_cells('K82:M82')
            ws.merge_cells('N82:O82')
            ws.merge_cells('P82:R82')
            
            ws.merge_cells('B83:C83')
            ws.merge_cells('D83:E83')
            ws.merge_cells('F83:G83')
            ws.merge_cells('H83:J83')
            ws.merge_cells('K83:M83')
            ws.merge_cells('N83:O83')
            ws.merge_cells('P83:R83')
            
            ws.merge_cells('A86:C86')
            ws.merge_cells('E86:R86')
            
            ws['B82'] = cervical_evoked_myogenic_potential.get("左耳声强阈值 (分贝)", "")
            ws['D82'] = cervical_evoked_myogenic_potential.get("左耳P13波潜伏期 (毫秒)", "")
            ws['F82'] = cervical_evoked_myogenic_potential.get("左耳N23波潜伏期 (毫秒)", "")
            ws['H82'] = cervical_evoked_myogenic_potential.get("左耳P13-N23波间期 (毫秒)", "")
            ws['K82'] = cervical_evoked_myogenic_potential.get("左耳P13波振幅 (微伏)", "")
            ws['N82'] = cervical_evoked_myogenic_potential.get("左耳N23波振幅 (微伏)", "")
            ws['P82'] = cervical_evoked_myogenic_potential.get("左耳P13-N23波振幅 (微伏)", "")
            
            ws['B83'] = cervical_evoked_myogenic_potential.get("右耳声强阈值 (分贝)", "")
            ws['D83'] = cervical_evoked_myogenic_potential.get("右耳P13波潜伏期 (毫秒)", "")
            ws['F83'] = cervical_evoked_myogenic_potential.get("右耳N23波潜伏期 (毫秒)", "")
            ws['H83'] = cervical_evoked_myogenic_potential.get("右耳P13-N23波间期 (毫秒)", "")
            ws['K83'] = cervical_evoked_myogenic_potential.get("右耳P13波振幅 (微伏)", "")
            ws['N83'] = cervical_evoked_myogenic_potential.get("右耳N23波振幅 (微伏)", "")
            ws['P83'] = cervical_evoked_myogenic_potential.get("右耳P13-N23波振幅 (微伏)", "")
            
            
            ws['A86'] = cervical_evoked_myogenic_potential.get("cVEMP耳间不对称性 (%)", "")
            ws['E86'] = cervical_evoked_myogenic_potential.get("检查结果", "")
            
        else:
            pass
        
        # 眼肌前庭诱发肌源性电位 (oVEMP)
        ocular_evoked_myogenic_potential = data.get("眼肌前庭诱发肌源性电位 (oVEMP)", "")
        if not is_dict_empty(ocular_evoked_myogenic_potential):
            
            ws.merge_cells('B90:C90')
            ws.merge_cells('D90:E90')
            ws.merge_cells('F90:G90')
            ws.merge_cells('H90:J90')
            ws.merge_cells('K90:M90')
            ws.merge_cells('N90:O90')
            ws.merge_cells('P90:R90')
            
            ws.merge_cells('B91:C91')
            ws.merge_cells('D91:E91')
            ws.merge_cells('F91:G91')
            ws.merge_cells('H91:J91')
            ws.merge_cells('K91:M91')
            ws.merge_cells('N91:O91')
            ws.merge_cells('P91:R91')
            
            ws.merge_cells('A94:C94')
            ws.merge_cells('E94:R94')
            
            ws['B90'] = ocular_evoked_myogenic_potential.get("左耳声强阈值 (分贝)", "")
            ws['D90'] = ocular_evoked_myogenic_potential.get("左耳N10波潜伏期 (毫秒)", "")
            ws['F90'] = ocular_evoked_myogenic_potential.get("左耳P15波潜伏期 (毫秒)", "")
            ws['H90'] = ocular_evoked_myogenic_potential.get("左耳N10-P15波间期 (毫秒)", "")
            ws['K90'] = ocular_evoked_myogenic_potential.get("左耳N10波振幅 (微伏)", "")
            ws['N90'] = ocular_evoked_myogenic_potential.get("左耳P15波振幅 (微伏)", "")
            ws['P90'] = ocular_evoked_myogenic_potential.get("左耳N10-P15波振幅 (微伏)", "")
            
            ws['B91'] = ocular_evoked_myogenic_potential.get("右耳声强阈值 (分贝)", "")
            ws['D91'] = ocular_evoked_myogenic_potential.get("右耳N10波潜伏期 (毫秒)", "")
            ws['F91'] = ocular_evoked_myogenic_potential.get("右耳P15波潜伏期 (毫秒)", "")
            ws['H91'] = ocular_evoked_myogenic_potential.get("右耳N10-P15波间期 (毫秒)", "")
            ws['K91'] = ocular_evoked_myogenic_potential.get("右耳N10波振幅 (微伏)", "")
            ws['N91'] = ocular_evoked_myogenic_potential.get("右耳P15波振幅 (微伏)", "")
            ws['P91'] = ocular_evoked_myogenic_potential.get("右耳N10-P15波振幅 (微伏)", "")
            
            ws['A94'] = ocular_evoked_myogenic_potential.get("oVEMP耳间不对称性 (%)", "")
            ws['E94'] = ocular_evoked_myogenic_potential.get("检查结果", "")
            
        else:
            pass
        
        # 主观视觉垂直线
        subjective_visual_vertical_line = data.get("主观视觉垂直线 (SVV)", "")
        if not is_dict_empty(subjective_visual_vertical_line):
        
            ws.merge_cells('A98:B98')
            ws.merge_cells('C98:D98')
            ws.merge_cells('F98:M98')
            
            ws['A98'] = subjective_visual_vertical_line.get("偏斜方向", "")
            ws['C98'] = subjective_visual_vertical_line.get("偏斜角度（度）", "")
            ws['F98'] = subjective_visual_vertical_line.get("检查结果", "")
            
        else:
            pass
        
        # 保存生成的报告
        random_id = str(uuid.uuid4())
        excel_path = os.path.join(tempfile.gettempdir(), f"report_{basic_info.get('ID', 'temp')}_{random_id}.xlsx")
        
        # 设置页面布局
        ws.page_setup.paperSize = 9  # A4纸
        ws.page_setup.orientation = 'landscape'  # 横向
        ws.page_setup.fitToWidth = 1  # 调整为1页宽
        ws.page_setup.fitToHeight = 1  # 调整为1页高
        
        # 设置打印区域边距（单位：英寸）
        ws.page_margins.left = 0.5
        ws.page_margins.right = 0.5
        ws.page_margins.top = 0.5
        ws.page_margins.bottom = 0.5
        
        wb.save(excel_path)
        
        # 将Excel转换为PDF
        pdf_path = os.path.join(tempfile.gettempdir(), f"report_{basic_info.get('ID', 'temp')}_{random_id}.pdf")
        
        try:
            # 使用win32com将Excel转换为PDF (Windows系统)
            if platform.system() == "Windows":
                import win32com.client
                excel = win32com.client.Dispatch("Excel.Application")
                excel.Visible = False
                wb = excel.Workbooks.Open(excel_path)
                
                # 设置页面布局
                for ws in wb.Worksheets:
                    ws.PageSetup.PaperSize = 9  # A4纸
                    ws.PageSetup.Orientation = 1  # xlLandscape
                    ws.PageSetup.Zoom = False  # 禁用缩放
                    ws.PageSetup.FitToPagesWide = 1  # 调整为1页宽
                    ws.PageSetup.FitToPagesTall = 1  # 调整为1页高
                    
                    # 设置页边距（单位：点，72点=1英寸）
                    ws.PageSetup.LeftMargin = 36  # 0.5英寸
                    ws.PageSetup.RightMargin = 36
                    ws.PageSetup.TopMargin = 36
                    ws.PageSetup.BottomMargin = 36
                
                wb.ExportAsFixedFormat(0, pdf_path)  # 0 表示PDF格式
                wb.Close()
                excel.Quit()
                os.remove(excel_path)  # 删除临时Excel文件
            
            # 使用其他方法转换PDF (Mac/Linux系统)
            else:
                try:
                    import subprocess
                    libreoffice_cmd = "soffice"
                    # 添加页面大小和方向参数
                    subprocess.run([
                        libreoffice_cmd,
                        '--headless',
                        '--convert-to', 
                        'pdf:writer_pdf_Export',
                        '--outdir', 
                        os.path.dirname(pdf_path),
                        excel_path
                    ])
                    os.remove(excel_path)
                except Exception as e:
                    messagebox.showwarning("警告", f"PDF转换失败，将打开Excel文件。错误信息: {str(e)}")
                    pdf_path = excel_path

            # 打开生成的PDF文件
            if platform.system() == "Windows":
                os.startfile(pdf_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.call(["open", pdf_path])
            else:  # Linux
                subprocess.call(["xdg-open", pdf_path])
                
        except Exception as e:
            messagebox.showwarning("警告", f"PDF转换失败，将打开Excel文件。错误信息: {str(e)}")
            # 如果PDF转换失败，打开Excel文件
            if platform.system() == "Windows":
                os.startfile(excel_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.call(["open", excel_path])
            else:  # Linux
                subprocess.call(["xdg-open", excel_path])

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



