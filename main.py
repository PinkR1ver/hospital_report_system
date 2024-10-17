import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import shutil
from datetime import datetime
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

class VestibularFunctionReport:
    def __init__(self, master):
        self.master = master
        self.master.title("前庭功能检查报告系统")
        self.master.geometry("800x700")
        
        self.create_menu()
        
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.basic_info_page = BasicInfoPage(self.notebook, self)
        self.notebook.add(self.basic_info_page, text="基本信息")
        
        self.spontaneous_nystagmus_page = SpontaneousNystagmusPage(self.notebook, self)
        self.notebook.add(self.spontaneous_nystagmus_page, text="自发性眼震")
        
        self.gaze_nystagmus_page = GazeNystagmusPage(self.notebook, self)
        self.notebook.add(self.gaze_nystagmus_page, text="凝视性眼震")
        
        self.head_impulse_test_page = HeadImpulseTestPage(self.notebook, self)
        self.notebook.add(self.head_impulse_test_page, text="头脉冲试验")
        
        self.head_impulse_suppression_test_page = HeadImpulseSuppressionTestPage(self.notebook, self)
        self.notebook.add(self.head_impulse_suppression_test_page, text="头脉冲抑制试验")
        
        self.reverse_skew_page = ReverseSkewPage(self.notebook, self)
        self.notebook.add(self.reverse_skew_page, text="眼位反向偏斜")
        
        self.saccade_page = SaccadePage(self.notebook, self)
        self.notebook.add(self.saccade_page, text="扫视检查")
        
        self.visual_enhanced_vor_page = VisualEnhancedVORPage(self.notebook, self)
        self.notebook.add(self.visual_enhanced_vor_page, text="视觉增强VOR")
        
        self.vor_suppression_page = VORSuppressionPage(self.notebook, self)
        self.notebook.add(self.vor_suppression_page, text="前庭-眼反射抑制试验")
        
        self.head_shaking_test_page = HeadShakingTestPage(self.notebook, self)
        self.notebook.add(self.head_shaking_test_page, text="摇头试验")
        
        self.dix_hallpike_test_page = DixHallpikeTestPage(self.notebook, self)
        self.notebook.add(self.dix_hallpike_test_page, text="位置试验 (Dix-Hallpike)")
        
        self.supine_roll_test_page = SupineRollTestPage(self.notebook, self)
        self.notebook.add(self.supine_roll_test_page, text="位置试验 (仰卧滚转)")

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="保存", command=self.save_data)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.master.quit)

    def save_data(self):
        # 获取基本信息
        basic_info = self.basic_info_page.get_data()["基本信息"]
        
        # 检查基本信息是否填写完整
        required_fields = ["ID", "姓名", "性别", "检查时间", "检查医生", "检查设备"]
        missing_fields = [field for field in required_fields if not basic_info.get(field)]
        
        if missing_fields:
            messagebox.showerror("错误", f"以下基本信息字段未填写完整:\n{', '.join(missing_fields)}\n请填写完整后再保存。")
            return
        
        # 收集所有数据
        data = {}
        data.update(self.basic_info_page.get_data())
        data.update(self.spontaneous_nystagmus_page.get_data())
        data.update(self.gaze_nystagmus_page.get_data())
        data.update(self.head_impulse_test_page.get_data())
        data.update(self.head_impulse_suppression_test_page.get_data())
        data.update(self.reverse_skew_page.get_data())
        data.update(self.saccade_page.get_data())
        data.update(self.visual_enhanced_vor_page.get_data())
        data.update(self.vor_suppression_page.get_data())
        data.update(self.head_shaking_test_page.get_data())
        data.update(self.dix_hallpike_test_page.get_data())
        data.update(self.supine_roll_test_page.get_data())
        
        # 创建保存路径
        documents_path = os.path.expanduser("~\\Documents")
        vestibular_save_path = os.path.join(documents_path, "vestibular_save")
        if not os.path.exists(vestibular_save_path):
            os.makedirs(vestibular_save_path)
        
        # 创建日期文件夹
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # 创建report文件夹
        report_folder = os.path.join(vestibular_save_path, "report", current_date)
        if not os.path.exists(report_folder):
            os.makedirs(report_folder)
        
        # 创建图片日期文件夹
        pic_date_folder = os.path.join(vestibular_save_path, "pic", current_date)
        if not os.path.exists(pic_date_folder):
            os.makedirs(pic_date_folder)
        
        # 生成文件名
        patient_id = basic_info["ID"]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{patient_id}_{timestamp}.json"
        
        # 完整的文件路径（现在保存在report文件夹中）
        file_path = os.path.join(report_folder, filename)
        
        # 处理头脉冲试验图片
        hit_image_path = data["头脉冲试验"]["头脉冲试验示意图"]
        if hit_image_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"head_impulse_test_{timestamp}{os.path.splitext(hit_image_path)[1]}"
            new_path = os.path.join(pic_date_folder, new_filename)
            shutil.copy(hit_image_path, new_path)
            data["头脉冲试验"]["头脉冲试验示意图"] = os.path.relpath(new_path, vestibular_save_path)
        
        # 处理头脉冲抑制试验图片
        his_image_path = data["头脉冲抑制试验"]["头脉冲抑制试验示意图"]
        if his_image_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"head_impulse_suppression_{timestamp}{os.path.splitext(his_image_path)[1]}"
            new_path = os.path.join(pic_date_folder, new_filename)
            shutil.copy(his_image_path, new_path)
            data["头脉冲抑制试验"]["头脉冲抑制试验示意图"] = os.path.relpath(new_path, vestibular_save_path)
        
        # 保存数据到文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        messagebox.showinfo("保存成功", f"数据已成功保存到:\n{file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VestibularFunctionReport(root)
    root.mainloop()
