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
from utils import *

class VestibularFunctionReport:
    def __init__(self, master):
        self.master = master
        self.config_file = "config.json"
        
        # 在创建主界面之前先检查密码
        if not self.check_password():
            self.master.quit()
            return
            
        self.master.title("前庭功能检查报告系统")
        self.master.geometry("1000x700")
        
        self.load_config()
        
        self.create_menu()
        
        # create database date folder
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.db_date_path = os.path.join(self.db_path, "report", current_date)
        if not os.path.exists(self.db_date_path):
            os.makedirs(self.db_date_path)
        
        self.db_pic_path = os.path.join(self.db_path, "pic", current_date)
        if not os.path.exists(self.db_pic_path):
            os.makedirs(self.db_pic_path)
        
        self.db_video_path = os.path.join(self.db_path, "video", current_date)
        if not os.path.exists(self.db_video_path):
            os.makedirs(self.db_video_path)
        
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

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="保存", command=self.save_data)
        file_menu.add_command(label="退出", command=self.master.quit)

        # 数据库菜单
        db_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="数据库", menu=db_menu)
        db_menu.add_command(label="查看数据库", command=self.show_database)
        db_menu.add_command(label="更改数据库文件夹", command=self.change_db_folder)
        db_menu.add_command(label="打开数据库文件夹", command=self.open_db_folder)

        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self.show_about)

    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                
            # 检查是否存在密码配置
            if 'password' not in config:
                # 如果没有密码，则设置密码
                self.set_initial_password()
                # 重新加载配置
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    
        except FileNotFoundError:
            # 如果配置文件不存在，创建新的配置文件并设置密码
            config = {}
            self.set_initial_password()
            # 重新加载配置
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                
        # 加载其他配置
        self.load_database_path()
        self.load_fonts()
        
        # 保存完整配置
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
                
        report_folder = os.path.join(self.db_path, "report")
        if not os.path.exists(report_folder):
            os.makedirs(report_folder, exist_ok=True)
            
        pic_folder = os.path.join(self.db_path, "pic")
        if not os.path.exists(pic_folder):
            os.makedirs(pic_folder, exist_ok=True)
            
        video_folder = os.path.join(self.db_path, "video")
        if not os.path.exists(video_folder):
            os.makedirs(video_folder, exist_ok=True)
        
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
        try:
            # 读取现有配置
            with open(self.config_file, 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {}
        
        # 更新配置
        config.update({
            'db_path': self.db_path,
            'font_name': self.font_name,
            'font_path': self.font_path
        })
        
        # 确保保留密码配置
        if 'password' not in config:
            config['password'] = ''  # 或者可以在这里触发密码设置
        
        # 保存配置
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
        
        # 弹出结论选择窗口
        conclusions = self.show_conclusion_dialog()
        if conclusions is None:  # 用户取消了操作
            return
        if not conclusions:  # 没有选择任何结论
            messagebox.showerror("错误", "请至少选择一项检查结论。")
            return
        
        # 将结论添加到数据中
        data["检查结论"] = conclusions
        
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
        
        # 创建视频日期文件夹
        video_date_folder = os.path.join(self.db_path, "video", current_date)
        if not os.path.exists(video_date_folder):
            os.makedirs(video_date_folder)
        
        # 生成文件名
        patient_id = basic_info["ID"]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{patient_id}_{timestamp}.json"
        
        # 完整的文件路径（现在保存在report文件夹中）
        file_path = os.path.join(report_folder, filename)
        
        # 处理头脉冲试验图片
        self.process_image(data, "头脉冲试验", "头脉冲试验示意图", pic_date_folder)
        
        # 处理头脉冲抑制试验图片
        self.process_image(data, "头脉冲抑制试验", "头脉冲抑制试验示意图", pic_date_folder)
        
        # 处理温度试验图片
        self.process_image(data, "温度试验", "温度试验示意图", pic_date_folder)
        
        # 处理视频
        video_tests = [
            '位置试验 (Dix-Hallpike试验)', '仰卧滚转试验', '自发性眼震', '位置试验(其他)', 
            '视动性眼震', '摇头试验', '凝视性眼震', '瘘管试验'
        ]
        for test_name in video_tests:
            self.process_video(data, test_name, video_date_folder)
        
        # 保存数据到文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        messagebox.showinfo("保存成功", f"数据已成功保存到:\n{file_path}")

    def translate_test_name(self, test_name):
        translation = {
            "头脉冲试验": "head_impulse_test",
            "头脉冲抑制试验": "head_impulse_suppression_test",
            "温度试验": "caloric_test",
            "位置试验 (Dix-Hallpike试验)": "dix_hallpike_test",
            "仰卧滚转试验": "supine_roll_test",
            "自发性眼震": "spontaneous_nystagmus",
            "位置试验(其他)": "other_position_test",
            "视动性眼震": "optokinetic_nystagmus",
            "摇头试验": "head_shaking_test",
            "凝视性眼震": "gaze_nystagmus",
            "瘘管试验": "fistula_test"
        }
        return translation.get(test_name, test_name.lower().replace(' ', '_'))

    def process_image(self, data, test_name, image_key, pic_folder):
        image_path = data.get(test_name, {}).get(image_key)
        if image_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name_en = self.translate_test_name(test_name)
            new_filename = f"{test_name_en}_{timestamp}{os.path.splitext(image_path)[1]}"
            new_path = os.path.join(pic_folder, new_filename)
            shutil.copy(image_path, new_path)
            data[test_name][image_key] = os.path.relpath(new_path, self.db_path)

    def process_video(self, data, test_name, video_folder):
        video_path = data.get(test_name, {}).get("视频")
        if video_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name_en = self.translate_test_name(test_name)
            new_filename = f"{test_name_en}_{timestamp}{os.path.splitext(video_path)[1]}"
            new_path = os.path.join(video_folder, new_filename)
            shutil.copy(video_path, new_path)
            data[test_name]["视频"] = os.path.relpath(new_path, self.db_path)

    def show_database(self):
        self.show_page("database")

    def show_about(self):
        about_text = """
        前庭功能检查报告系统
        版本: 1.0.0
        
        本软件遵循 MIT 许可证
        
        Copyright (c) 2024
        
        Author: JudeW
        Email: pinkr1veroops@gmail.com
        """
        messagebox.showinfo("关于", about_text)

    def set_initial_password(self):
        """设置初始密码"""
        password_window = tk.Toplevel(self.master)
        password_window.title("设置密码")
        password_window.geometry("300x300")  # 增加窗口高度以容纳按钮
        password_window.transient(self.master)
        
        # 创建主框架来组织控件
        main_frame = ttk.Frame(password_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 密码输入区域
        ttk.Label(main_frame, text="请设置系统密码:").pack(pady=5)
        password_var = tk.StringVar()
        password_entry = ttk.Entry(main_frame, show="*", textvariable=password_var)
        password_entry.pack(pady=5)
        
        # 确认密码区域
        ttk.Label(main_frame, text="请确认密码:").pack(pady=5)
        confirm_var = tk.StringVar()
        confirm_entry = ttk.Entry(main_frame, show="*", textvariable=confirm_var)
        confirm_entry.pack(pady=5)
        
        # 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        def save_password():
            if not password_var.get():
                messagebox.showerror("错误", "密码不能为空！")
                return
            
            if password_var.get() == confirm_var.get():
                config = {'password': password_var.get()}
                with open(self.config_file, 'w') as f:
                    json.dump(config, f)
                password_window.destroy()
            else:
                messagebox.showerror("错误", "两次输入的密码不一致！")
        
        def cancel():
            password_window.destroy()
            self.master.quit()
        
        # 添加确认和取消按钮
        ttk.Button(button_frame, text="确定", command=save_password, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=cancel, width=10).pack(side=tk.LEFT, padx=5)
        
        # 设置回车键绑定
        password_entry.bind('<Return>', lambda e: confirm_entry.focus())
        confirm_entry.bind('<Return>', lambda e: save_password())
        
        # 设置初始焦点
        password_entry.focus()
        
        password_window.grab_set()  # 模态窗口
        password_window.protocol("WM_DELETE_WINDOW", cancel)  # 处理窗口关闭按钮
        self.master.wait_window(password_window)

    def check_password(self):
        """检查密码"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                stored_password = config.get('password')
        except FileNotFoundError:
            return True  # 首次运行时返回True
            
        password_window = tk.Toplevel(self.master)
        password_window.title("密码验证")
        password_window.geometry("300x120")
        password_window.transient(self.master)
        
        ttk.Label(password_window, text="请输入系统密码:").pack(pady=10)
        password_var = tk.StringVar()
        password_entry = ttk.Entry(password_window, show="*", textvariable=password_var)
        password_entry.pack(pady=5)
        
        result = [False]
        
        def verify_password():
            if password_var.get() == stored_password:
                result[0] = True
                password_window.destroy()
            else:
                messagebox.showerror("错误", "密码错误！")
                result[0] = False
        
        ttk.Button(password_window, text="确定", command=verify_password).pack(pady=10)
        
        password_window.grab_set()  # 模态窗口
        self.master.wait_window(password_window)
        
        return result[0]

    def show_conclusion_dialog(self):
        # 创建一个新的顶层窗口
        dialog = tk.Toplevel(self.master)
        dialog.title("检查结论")
        dialog.geometry("400x300")
        dialog.transient(self.master)  # 设置为主窗口的临时窗口
        dialog.grab_set()  # 模态窗口
        
        # 创建一个框架来容纳选项
        frame = ttk.LabelFrame(dialog, text="请选择检查结论", padding="10 10 10 10")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建变量字典存储选择状态
        conclusion_vars = {}
        conclusions = [
            "未见明显异常",
            "左侧前庭功能低下",
            "右侧前庭功能低下",
            "双侧前庭功能低下"
        ]
        
        # 创建复选框
        for i, conclusion in enumerate(conclusions):
            var = tk.BooleanVar()
            conclusion_vars[conclusion] = var
            chk = ttk.Checkbutton(frame, text=conclusion, variable=var)
            chk.grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            
        #  # 添加“其他”选项
        # other_var = tk.BooleanVar()
        # conclusion_vars["其他"] = other_var
        # chk_other = ttk.Checkbutton(frame, text="其他", variable=other_var)
        # chk_other.grid(row=len(conclusions), column=0, sticky=tk.W, padx=5, pady=5)
        
        # # 添加输入框
        # other_entry = ttk.Entry(frame, state=tk.DISABLED)
        # other_entry.grid(row=len(conclusions), column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # # 启用或禁用输入框
        # def toggle_other_entry():
        #     if other_var.get():
        #         other_entry.config(state=tk.NORMAL)
        #     else:
        #         other_entry.config(state=tk.DISABLED)
        
        # other_var.trace_add("write", lambda *args: toggle_other_entry())
        
        # 结果变量
        result = {"selected": None}
        
        def on_ok():
            # 获取选中的结论
            selected = [c for c, v in conclusion_vars.items() if v.get()]
            result["selected"] = selected
            dialog.destroy()
        
        def on_cancel():
            result["selected"] = None
            dialog.destroy()
        
        # 创建按钮框架
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 添加确定和取消按钮
        ok_button = ttk.Button(button_frame, text="确定", command=on_ok)
        ok_button.pack(side=tk.RIGHT, padx=5)
        
        cancel_button = ttk.Button(button_frame, text="取消", command=on_cancel)
        cancel_button.pack(side=tk.RIGHT, padx=5)
        
        # 等待窗口关闭
        dialog.wait_window()
        
        return result["selected"]

if __name__ == "__main__":
    root = tk.Tk()
    app = VestibularFunctionReport(root)
    root.mainloop()
