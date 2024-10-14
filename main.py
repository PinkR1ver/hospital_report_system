import tkinter as tk
from tkinter import ttk, messagebox
import json
from basic_info_page import BasicInfoPage

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
        data = self.basic_info_page.get_data()
        # 在这里添加其他页面的数据
        # data.update(self.other_page1.get_data())
        # ...
        
        # 这里可以添加保存到文件或数据库的代码
        print(json.dumps(data, ensure_ascii=False, indent=2))
        messagebox.showinfo("保存成功", "数据已成功保存")

if __name__ == "__main__":
    root = tk.Tk()
    app = VestibularFunctionReport(root)
    root.mainloop()