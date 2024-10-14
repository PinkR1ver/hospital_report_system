import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
from basic_info_page import BasicInfoPage
from spontaneous_nystagmus_page import SpontaneousNystagmusPage
from gaze_nystagmus_page import GazeNystagmusPage

class VestibularFunctionReport:
    def __init__(self, master):
        self.master = master
        self.master.title("前庭功能检查报告系统")
        self.master.geometry("600x500")
        
        self.create_menu()
        
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.basic_info_page = BasicInfoPage(self.notebook, self)
        self.notebook.add(self.basic_info_page, text="基本信息")
        
        self.spontaneous_nystagmus_page = SpontaneousNystagmusPage(self.notebook, self)
        self.notebook.add(self.spontaneous_nystagmus_page, text="自发性眼震")
        
        self.gaze_nystagmus_page = GazeNystagmusPage(self.notebook, self)
        self.notebook.add(self.gaze_nystagmus_page, text="凝视性眼震")
        
        # 在这里添加其他页面
        # self.other_page1 = OtherPage1(self.notebook, self)
        # self.notebook.add(self.other_page1, text="其他页面1")
        # ...

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
        required_fields = ["ID", "姓名", "性别", "出生日期", "检查项目", "检查时间", "检查医生", "检查设备",]
        missing_fields = [field for field in required_fields if not basic_info.get(field)]
        
        if missing_fields:
            messagebox.showerror("错误", f"以下基本信息字段未填写完整:\n{', '.join(missing_fields)}\n请填写完整后再保存。")
            return
        
        # 收集所有数据
        data = {}
        data.update(self.basic_info_page.get_data())
        data.update(self.spontaneous_nystagmus_page.get_data())
        data.update(self.gaze_nystagmus_page.get_data())
        
        # 创建保存路径
        documents_path = os.path.expanduser("~\\Documents")
        vestibular_save_path = os.path.join(documents_path, "vestibular_save")
        if not os.path.exists(vestibular_save_path):
            os.makedirs(vestibular_save_path)
        
        # 创建日期文件夹
        current_date = datetime.now().strftime("%Y-%m-%d")
        date_folder = os.path.join(vestibular_save_path, current_date)
        if not os.path.exists(date_folder):
            os.makedirs(date_folder)
        
        # 生成文件名
        patient_id = basic_info["ID"]
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"{patient_id}_{timestamp}.json"
        
        # 完整的文件路径
        file_path = os.path.join(date_folder, filename)
        
        # 保存数据到文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        messagebox.showinfo("保存成功", f"数据已成功保存到:\n{file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VestibularFunctionReport(root)
    root.mainloop()
