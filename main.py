import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import shutil
from datetime import datetime
import subprocess
import platform
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 导入所有页面
from basic_info_page import BasicInfoPage
from spontaneous_nystagmus_page import SpontaneousNystagmusPage
from gaze_nystagmus_page import GazeNystagmusPage
from head_impulse_test_page import HeadImpulseTestPage
from head_impulse_suppression_test_page import HeadImpulseSuppressionTestPage
from reverse_skew_page import ReverseSkewPage
from saccade_page import SaccadePage
from visual_enhanced_vor_page import VisualEnhancedVORPage
from vor_suppression_page import VORSuppressionPage
from head_shaking_test_page import HeadShakingTestPage
from dix_hallpike_test_page import DixHallpikeTestPage
from supine_roll_test_page import SupineRollTestPage
from other_position_test_page import OtherPositionTestPage
from visual_tracking_page import VisualTrackingPage
from optokinetic_nystagmus_page import OptoKineticNystagmusPage
from fistula_test_page import FistulaTestPage
from caloric_test_page import CaloricTestPage
from cvemp_test_page import CVEMPTestPage
from ovemp_test_page import OVEMPTestPage
from svv_test_page import SVVTestPage

from database_page import DatabasePage

class VestibularFunctionReport:
    def __init__(self, master):
        self.master = master
        self.master.title("前庭功能检查报告系统")
        self.master.geometry("1000x700")  # 增加窗口宽度以适应侧边栏
        
        self.config_file = "config.json"
        self.load_config()
        
        self.create_menu()
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建侧边栏
        self.sidebar = ttk.Frame(self.main_frame, width=200, relief="sunken", borderwidth=1)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # 创建内容区域
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.create_sidebar()
        self.create_pages()
        
    def create_sidebar(self):
        pages = [
            ("基本信息", self.show_basic_info),
            ("自发性眼震", self.show_spontaneous_nystagmus),
            ("凝视性眼震", self.show_gaze_nystagmus),
            ("头脉冲试验", self.show_head_impulse_test),
            ("头脉冲抑制试验", self.show_head_impulse_suppression_test),
            ("眼位反向偏斜", self.show_reverse_skew),
            ("扫视检查", self.show_saccade),
            ("视觉增强VOR", self.show_visual_enhanced_vor),
            ("前庭-眼反射抑制试验", self.show_vor_suppression),
            ("摇头试验", self.show_head_shaking_test),
            ("位置试验 (Dix-Hallpike)", self.show_dix_hallpike_test),
            ("位置试验 (仰卧滚转)", self.show_supine_roll_test),
            ("位置试验 (其他)", self.show_other_position_test),
            ("视跟踪", self.show_visual_tracking),
            ("视动性眼震", self.show_optokinetic_nystagmus),
            ("瘘管试验", self.show_fistula_test),
            ("温度试验", self.show_caloric_test),
            ("颈肌前庭诱发肌源性电位", self.show_cvemp_test),
            ("眼肌前庭诱发肌源性电位", self.show_ovemp_test),
            ("主观视觉垂直线", self.show_svv_test)
        ]
        
        for text, command in pages:
            ttk.Button(self.sidebar, text=text, command=command, width=25).pack(pady=2)
        
    def create_pages(self):
        self.pages = {
            "basic_info": BasicInfoPage(self.content_frame, self),
            "spontaneous_nystagmus": SpontaneousNystagmusPage(self.content_frame, self),
            "gaze_nystagmus": GazeNystagmusPage(self.content_frame, self),
            "head_impulse_test": HeadImpulseTestPage(self.content_frame, self),
            "head_impulse_suppression_test": HeadImpulseSuppressionTestPage(self.content_frame, self),
            "reverse_skew": ReverseSkewPage(self.content_frame, self),
            "saccade": SaccadePage(self.content_frame, self),
            "visual_enhanced_vor": VisualEnhancedVORPage(self.content_frame, self),
            "vor_suppression": VORSuppressionPage(self.content_frame, self),
            "head_shaking_test": HeadShakingTestPage(self.content_frame, self),
            "dix_hallpike_test": DixHallpikeTestPage(self.content_frame, self),
            "supine_roll_test": SupineRollTestPage(self.content_frame, self),
            "other_position_test": OtherPositionTestPage(self.content_frame, self),
            "visual_tracking": VisualTrackingPage(self.content_frame, self),
            "optokinetic_nystagmus": OptoKineticNystagmusPage(self.content_frame, self),
            "fistula_test": FistulaTestPage(self.content_frame, self),
            "caloric_test": CaloricTestPage(self.content_frame, self),
            "cvemp_test": CVEMPTestPage(self.content_frame, self),
            "ovemp_test": OVEMPTestPage(self.content_frame, self),
            "svv_test": SVVTestPage(self.content_frame, self),
            "database": DatabasePage(self.content_frame, self)
        }
        
        for page in self.pages.values():
            page.pack(fill=tk.BOTH, expand=True)
            page.pack_forget()
        
        self.current_page = None
        self.show_basic_info()  # 默认显示基本信息页面
    
    def show_page(self, page_name):
        if self.current_page:
            self.current_page.pack_forget()
        self.pages[page_name].pack(fill=tk.BOTH, expand=True)
        self.current_page = self.pages[page_name]
    
    def show_basic_info(self):
        self.show_page("basic_info")
    
    def show_spontaneous_nystagmus(self):
        self.show_page("spontaneous_nystagmus")
    
    def show_gaze_nystagmus(self):
        self.show_page("gaze_nystagmus")
    
    def show_head_impulse_test(self):
        self.show_page("head_impulse_test")
    
    def show_head_impulse_suppression_test(self):
        self.show_page("head_impulse_suppression_test")
    
    def show_reverse_skew(self):
        self.show_page("reverse_skew")
    
    def show_saccade(self):
        self.show_page("saccade")
    
    def show_visual_enhanced_vor(self):
        self.show_page("visual_enhanced_vor")
    
    def show_vor_suppression(self):
        self.show_page("vor_suppression")
    
    def show_head_shaking_test(self):
        self.show_page("head_shaking_test")
    
    def show_dix_hallpike_test(self):
        self.show_page("dix_hallpike_test")
    
    def show_supine_roll_test(self):
        self.show_page("supine_roll_test")
    
    def show_other_position_test(self):
        self.show_page("other_position_test")
    
    def show_visual_tracking(self):
        self.show_page("visual_tracking")
    
    def show_optokinetic_nystagmus(self):
        self.show_page("optokinetic_nystagmus")
    
    def show_fistula_test(self):
        self.show_page("fistula_test")
    
    def show_caloric_test(self):
        self.show_page("caloric_test")
    
    def show_cvemp_test(self):
        self.show_page("cvemp_test")
    
    def show_ovemp_test(self):
        self.show_page("ovemp_test")
    
    def show_svv_test(self):
        self.show_page("svv_test")

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="保存", command=self.save_data)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.master.quit)

        # 添加数据库菜单
        db_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="数据库", menu=db_menu)
        db_menu.add_command(label="浏览报告", command=self.show_database)
        db_menu.add_command(label="打开数据库文件夹", command=self.open_db_folder)
        db_menu.add_command(label="更改数据库文件夹", command=self.change_db_folder)

    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            # create empty config file
            with open(self.config_file, 'w') as f:
                json.dump({}, f)
                
        self.load_database_path()
        self.load_fonts()
        self.save_config()
        
    def load_database_path(self):
        config = json.load(open(self.config_file, 'r'))
        try:
            self.db_path = config['db_path']
            if not os.path.exists(self.db_path):
                os.makedirs(self.db_path, exist_ok=True)
        except Exception as e:
            self.db_path = os.path.join(os.getcwd(), "vest_database")
            if not os.path.exists(self.db_path):
                os.makedirs(self.db_path, exist_ok=True)
        
    def load_fonts(self):
        config = json.load(open(self.config_file, 'r'))
        try:
            ttfont = TTFont(config['font_name'], config['font_path'])
            self.font_name = config['font_name']
            self.font_path = config['font_path']
            pdfmetrics.registerFont(ttfont)
        except Exception as e:
            font_name = "SimSun"
            font_path = os.path.join(os.getcwd(), "SIMSUN.ttf")
            
            try:
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                self.font_name = font_name
                self.font_path = font_path
            except Exception as e:
                messagebox.showerror("错误", f"无法加载字体: {e}\n将使用默认字体。")
                self.font_name = None
                self.font_path = None

    def save_config(self):
        config = {'db_path': self.db_path, 'font_name': self.font_name, 'font_path': self.font_path}
        with open(self.config_file, 'w') as f:
            json.dump(config, f)

    def change_db_folder(self):
        new_path = filedialog.askdirectory(title="选择新的数据库文件夹")
        if new_path:
            self.db_path = new_path
            self.save_config()
            messagebox.showinfo("成功", f"数据库文件夹已更改为: {self.db_path}")
            
    def open_db_folder(self):
        if os.path.exists(self.db_path):
            if platform.system() == "Windows":
                os.startfile(self.db_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.call(["open", self.db_path])
            else:  # Linux和其他类Unix系统
                subprocess.call(["xdg-open", self.db_path])
        else:
            messagebox.showerror("错误", f"数据库文件夹不存在: {self.db_path}")

    def save_data(self):
        # 获取所有页面的数据
        data = {}
        for page_name, page in self.pages.items():
            data.update(page.get_data())
        
        # 检查基本信息是否填写完整
        basic_info = data.get("基本信息", {})
        required_fields = ["ID", "姓名", "性别", "检查时间", "检查医生", "检查设备"]
        missing_fields = [field for field in required_fields if not basic_info.get(field)]
        
        if missing_fields:
            messagebox.showerror("错误", f"以下基本信息字段未填写完整:\n{', '.join(missing_fields)}\n请填写完整后再保存。")
            return
        
        # 使用配置的数据库路径
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)
        
        # 创建日期文件夹
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # 创建report文件夹
        report_folder = os.path.join(self.db_path, "report", current_date)
        if not os.path.exists(report_folder):
            os.makedirs(report_folder)
        
        # 创建图片日期文件夹
        pic_date_folder = os.path.join(self.db_path, "pic", current_date)
        if not os.path.exists(pic_date_folder):
            os.makedirs(pic_date_folder)
        
        # 生成文件名
        patient_id = basic_info["ID"]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{patient_id}_{timestamp}.json"
        
        # 完整的文件路径（现在保存在report文件夹中）
        file_path = os.path.join(report_folder, filename)
        
        # 处理头脉冲试验图片
        hit_image_path = data.get("头脉冲试验", {}).get("头脉冲试验示意图")
        if hit_image_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"head_impulse_test_{timestamp}{os.path.splitext(hit_image_path)[1]}"
            new_path = os.path.join(pic_date_folder, new_filename)
            shutil.copy(hit_image_path, new_path)
            data["头脉冲试验"]["头脉冲试验示意图"] = os.path.relpath(new_path, self.db_path)
        
        # 处理头脉冲抑制试验图片
        his_image_path = data.get("头脉冲抑制试验", {}).get("头脉冲抑制试验示意图")
        if his_image_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"head_impulse_suppression_{timestamp}{os.path.splitext(his_image_path)[1]}"
            new_path = os.path.join(pic_date_folder, new_filename)
            shutil.copy(his_image_path, new_path)
            data["头脉冲抑制试验"]["头脉冲抑制试验示意图"] = os.path.relpath(new_path, self.db_path)
        
        # 保存数据到文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        messagebox.showinfo("保存成功", f"数据已成功保存到:\n{file_path}")
        
    def show_database(self):
        self.show_page("database")

if __name__ == "__main__":
    root = tk.Tk()
    app = VestibularFunctionReport(root)
    root.mainloop()
