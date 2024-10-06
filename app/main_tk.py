import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from tkcalendar import DateEntry
import json
from datetime import date
import os
import subprocess
import hashlib

class VestibularFunctionReport:
    def __init__(self, master):
        self.master = master
        self.master.title("前庭功能检测报告单")
        self.master.geometry("800x600")

        self.save_directory = os.path.join(os.path.expanduser("~"), "Documents", "vestibular_save")
        
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)

        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="填写新报告", command=self.clear_form)
        file_menu.add_command(label="保存报告", command=self.save_report)
        file_menu.add_command(label="检索报告", command=self.search_report)
        file_menu.add_command(label="更改保存目录", command=self.change_save_directory)
        file_menu.add_command(label="打开保存目录", command=self.open_save_directory)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.master.quit)

    def create_widgets(self):
        notebook = ttk.Notebook(self.master)
        notebook.pack(fill=tk.BOTH, expand=True)

        # 基本信息
        basic_info_frame = ttk.Frame(notebook)
        notebook.add(basic_info_frame, text="基本信息")

        ttk.Label(basic_info_frame, text="登记号/住院号:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.reg_number = ttk.Entry(basic_info_frame)
        self.reg_number.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(basic_info_frame, text="姓名:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.name = ttk.Entry(basic_info_frame)
        self.name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(basic_info_frame, text="性别:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.gender = ttk.Entry(basic_info_frame)
        self.gender.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(basic_info_frame, text="年龄:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.age = ttk.Entry(basic_info_frame)
        self.age.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(basic_info_frame, text="医嘱项目:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.medical_order = ttk.Entry(basic_info_frame)
        self.medical_order.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(basic_info_frame, text="测试设备:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.test_device = ttk.Entry(basic_info_frame)
        self.test_device.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(basic_info_frame, text="检查日期:").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        self.test_date = DateEntry(basic_info_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.test_date.grid(row=6, column=1, padx=5, pady=5)
        
        # Dix-Hallpike试验
        dix_hallpike_frame = ttk.Frame(notebook)
        notebook.add(dix_hallpike_frame, text="Dix-Hallpike试验")

        self.create_dix_hallpike_form(dix_hallpike_frame, "右耳向下", 0, 0)
        self.create_dix_hallpike_form(dix_hallpike_frame, "左耳向下", 0, 1)

        # 滚转试验
        rolling_test_frame = ttk.Frame(notebook)
        notebook.add(rolling_test_frame, text="滚转试验")

        self.create_rolling_test_form(rolling_test_frame, "向右侧偏头", 0, 0)
        self.create_rolling_test_form(rolling_test_frame, "向左侧偏头", 0, 1)

        # 手法复位
        reposition_frame = ttk.Frame(notebook)
        notebook.add(reposition_frame, text="手法复位")

        self.reposition = tk.StringVar()
        ttk.Radiobutton(reposition_frame, text="未进行", variable=self.reposition, value="未进行").grid(row=0, column=0, padx=5, pady=5)
        ttk.Radiobutton(reposition_frame, text="已进行", variable=self.reposition, value="已进行").grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(reposition_frame, text="复位方法:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.reposition_method = ttk.Entry(reposition_frame)
        self.reposition_method.grid(row=1, column=1, padx=5, pady=5)

        # 结论和建议
        conclusion_frame = ttk.Frame(notebook)
        notebook.add(conclusion_frame, text="结论和建议")

        ttk.Label(conclusion_frame, text="结论:").grid(row=0, column=0, sticky="nw", padx=5, pady=5)
        self.conclusion = tk.Text(conclusion_frame, height=5, width=50)
        self.conclusion.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(conclusion_frame, text="建议:").grid(row=1, column=0, sticky="nw", padx=5, pady=5)
        self.recommendation = tk.Text(conclusion_frame, height=5, width=50)
        self.recommendation.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(conclusion_frame, text="检查者:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.examiner = ttk.Entry(conclusion_frame)
        self.examiner.grid(row=2, column=1, padx=5, pady=5)

    def create_dix_hallpike_form(self, parent, title, row, column):
        frame = ttk.LabelFrame(parent, text=title)
        frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        options = ["", "向天", "向地", "其他类型眼震", "无眼震"]

        ttk.Label(frame, text="躺下向天:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        setattr(self, f"{title}_lying_up", ttk.Combobox(frame, values=options))
        getattr(self, f"{title}_lying_up").grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="躺下向地:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        setattr(self, f"{title}_lying_down", ttk.Combobox(frame, values=options))
        getattr(self, f"{title}_lying_down").grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="坐起反向:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        setattr(self, f"{title}_sitting_reverse", ttk.Combobox(frame, values=options))
        getattr(self, f"{title}_sitting_reverse").grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="坐起同向:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        setattr(self, f"{title}_sitting_same", ttk.Combobox(frame, values=options))
        getattr(self, f"{title}_sitting_same").grid(row=3, column=1, padx=5, pady=5)

        setattr(self, f"{title}_vertigo", tk.BooleanVar())
        ttk.Checkbutton(frame, text="眩晕出现", variable=getattr(self, f"{title}_vertigo")).grid(row=4, column=0, columnspan=2, pady=5)

        ttk.Label(frame, text="潜伏期(秒):").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        setattr(self, f"{title}_latency", ttk.Entry(frame))
        getattr(self, f"{title}_latency").grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(frame, text="持续时间(秒):").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        setattr(self, f"{title}_duration", ttk.Entry(frame))
        getattr(self, f"{title}_duration").grid(row=6, column=1, padx=5, pady=5)

        setattr(self, f"{title}_fatigue", tk.BooleanVar())
        ttk.Checkbutton(frame, text="易疲劳性", variable=getattr(self, f"{title}_fatigue")).grid(row=7, column=0, columnspan=2, pady=5)

    def create_rolling_test_form(self, parent, title, row, column):
        frame = ttk.LabelFrame(parent, text=title)
        frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

        options = ["", "向左", "向右", "其他类型眼震", "无眼震"]

        ttk.Label(frame, text="向左:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        setattr(self, f"{title}_to_left", ttk.Combobox(frame, values=options))
        getattr(self, f"{title}_to_left").grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="向右:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        setattr(self, f"{title}_to_right", ttk.Combobox(frame, values=options))
        getattr(self, f"{title}_to_right").grid(row=1, column=1, padx=5, pady=5)

        setattr(self, f"{title}_vertigo", tk.BooleanVar())
        ttk.Checkbutton(frame, text="眩晕出现", variable=getattr(self, f"{title}_vertigo")).grid(row=2, column=0, columnspan=2, pady=5)

        ttk.Label(frame, text="潜伏期(秒):").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        setattr(self, f"{title}_latency", ttk.Entry(frame))
        getattr(self, f"{title}_latency").grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(frame, text="持续时间(秒):").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        setattr(self, f"{title}_duration", ttk.Entry(frame))
        getattr(self, f"{title}_duration").grid(row=4, column=1, padx=5, pady=5)

        setattr(self, f"{title}_fatigue", tk.BooleanVar())
        ttk.Checkbutton(frame, text="易疲劳性", variable=getattr(self, f"{title}_fatigue")).grid(row=5, column=0, columnspan=2, pady=5)

    def get_report_data(self):
        return {
            "基本信息": {
                "登记号/住院号": self.reg_number.get(),
                "姓名": self.name.get(),
                "性别": self.gender.get(),
                "年龄": self.age.get(),
                "医嘱项目": self.medical_order.get(),
                "测试设备": self.test_device.get(),
                "检查日期": self.test_date.get()
            },
            "Dix-Hallpike试验": {
                "右耳向下": self.get_dix_hallpike_data("右耳向下"),
                "左耳向下": self.get_dix_hallpike_data("左耳向下")
            },
            "滚转试验": {
                "向右侧偏头": self.get_rolling_test_data("向右侧偏头"),
                "向左侧偏头": self.get_rolling_test_data("向左侧偏头")
            },
            "手法复位": {
                "是否进行": self.reposition.get(),
                "复位方法": self.reposition_method.get()
            },
            "结论": self.conclusion.get("1.0", tk.END).strip(),
            "建议": self.recommendation.get("1.0", tk.END).strip(),
            "检查者": self.examiner.get()
        }

    def get_dix_hallpike_data(self, title):
        return {
            "躺下向天": getattr(self, f"{title}_lying_up").get(),
            "躺下向地": getattr(self, f"{title}_lying_down").get(),
            "坐起反向": getattr(self, f"{title}_sitting_reverse").get(),
            "坐起同向": getattr(self, f"{title}_sitting_same").get(),
            "眩晕出现": getattr(self, f"{title}_vertigo").get(),
            "潜伏期": getattr(self, f"{title}_latency").get(),
            "持续时间": getattr(self, f"{title}_duration").get(),
            "易疲劳性": getattr(self, f"{title}_fatigue").get()
        }

    def get_rolling_test_data(self, title):
        return {
            "向左": getattr(self, f"{title}_to_left").get(),
            "向右": getattr(self, f"{title}_to_right").get(),
            "眩晕出现": getattr(self, f"{title}_vertigo").get(),
            "潜伏期": getattr(self, f"{title}_latency").get(),
            "持续时间": getattr(self, f"{title}_duration").get(),
            "易疲劳性": getattr(self, f"{title}_fatigue").get()
        }

    def save_report(self):
        report_data = self.get_report_data()
        today = date.today()
        date_folder = today.strftime('%Y%m%d')
        save_path = os.path.join(self.save_directory, date_folder)
        
        # 如果日期文件夹不存在,创建它
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        
        # 生成SHA256哈希值
        name = report_data['基本信息']['姓名']
        date_str = today.strftime('%Y%m%d')
        hash_input = f"{name}{date_str}"
        hash_value = hashlib.sha256(hash_input.encode('utf-8')).hexdigest()
        
        file_name = f"{hash_value}.json"
        file_path = os.path.join(save_path, file_name)
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("保存成功", f"报告已保存到: {file_path}")

    def load_report(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                report_data = json.load(f)
            
            self.fill_form(report_data)
            messagebox.showinfo("加载成功", f"报告已从 {file_path} 加载")
            
    def search_report(self):
        name = simpledialog.askstring("输入姓名", "请输入患者姓名:")
        if not name:
            return
        
        date_str = simpledialog.askstring("输入日期", "请输入报告日期 (YYYYMMDD):")
        if not date_str:
            return

        index_path = os.path.join(self.save_directory, "report_index.json")
        if not os.path.exists(index_path):
            messagebox.showerror("错误", "索引文件不存在")
            return

        with open(index_path, "r", encoding="utf-8") as f:
            index = json.load(f)

        if date_str not in index or name not in index[date_str]:
            messagebox.showerror("错误", "未找到对应的报告")
            return

        hash_value = index[date_str][name]
        file_path = os.path.join(self.save_directory, date_str, f"{hash_value}.json")

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                report_data = json.load(f)
            
            self.fill_form(report_data)
            messagebox.showinfo("加载成功", f"报告已从 {file_path} 加载")
        else:
            messagebox.showerror("错误", "报告文件不存在")

    def fill_form(self, report_data):
        # 填充基本信息
        self.reg_number.set(report_data["基本信息"]["登记号/住院号"])
        self.name.set(report_data["基本信息"]["姓名"])
        self.gender.set(report_data["基本信息"]["性别"])
        self.age.set(report_data["基本信息"]["年龄"])
        self.medical_order.set(report_data["基本信息"]["医嘱项目"])
        self.test_device.set(report_data["基本信息"]["测试设备"])
        self.test_date.set(report_data["基本信息"]["检查日期"])

        # 填充Dix-Hallpike试验数据
        self.fill_dix_hallpike_data("右耳向下", report_data["Dix-Hallpike试验"]["右耳向下"])
        self.fill_dix_hallpike_data("左耳向下", report_data["Dix-Hallpike试验"]["左耳向下"])
        # 填充滚转试验数据
        self.fill_rolling_test_data("向右侧偏头", report_data["滚转试验"]["向右侧偏头"])
        self.fill_rolling_test_data("向左侧偏头", report_data["滚转试验"]["向左侧偏头"])
        # 填充手法复位数据
        self.reposition.set(report_data["手法复位"]["是否进行"])
        self.reposition_method.set(report_data["手法复位"]["复位方法"])
        # 填充结论和建议
        self.conclusion.delete("1.0", tk.END)
        self.conclusion.insert("1.0", report_data["结论"])
        self.recommendation.delete("1.0", tk.END)
        self.recommendation.insert("1.0", report_data["建议"])
        self.examiner.set(report_data["检查者"])
        
    def fill_dix_hallpike_data(self, title, data):
        
        getattr(self, f"{title}lying_up").set(data["躺下向天"])
        getattr(self, f"{title}lying_down").set(data["躺下向地"])
        getattr(self, f"{title}sitting_reverse").set(data["坐起反向"])
        getattr(self, f"{title}sitting_same").set(data["坐起同向"])
        getattr(self, f"{title}vertigo").set(data["眩晕出现"])
        getattr(self, f"{title}latency").set(data["潜伏期"])
        getattr(self, f"{title}duration").set(data["持续时间"])
        getattr(self, f"{title}fatigue").set(data["易疲劳性"])
        
    def fill_rolling_test_data(self, title, data):
        getattr(self, f"{title}to_left").set(data["向左"])
        getattr(self, f"{title}to_right").set(data["向右"])
        getattr(self, f"{title}vertigo").set(data["眩晕出现"])
        getattr(self, f"{title}latency").set(data["潜伏期"])
        getattr(self, f"{title}duration").set(data["持续时间"])
        getattr(self, f"{title}fatigue").set(data["易疲劳性"])
        
    def change_save_directory(self):
        new_directory = filedialog.askdirectory()
        if new_directory:
            self.save_directory = new_directory
            messagebox.showinfo("更改保存目录", f"保存目录已更改为: {self.save_directory}")

    def open_save_directory(self):
        subprocess.run(['explorer', self.save_directory])

    def clear_form(self):
        for widget in self.master.winfo_children():
            if isinstance(widget, ttk.Notebook):
                for tab in widget.winfo_children():
                    for child in tab.winfo_children():
                        if isinstance(child, (ttk.Entry, ttk.Combobox)):
                            child.delete(0, tk.END)
                        elif isinstance(child, tk.Text):
                            child.delete("1.0", tk.END)
                        elif isinstance(child, ttk.Checkbutton):
                            child.state(['!selected'])
                        elif isinstance(child, DateEntry):
                            child.set_date(date.today())

if __name__ == "__main__":
    root = tk.Tk()
    app = VestibularFunctionReport(root)
    root.mainloop()