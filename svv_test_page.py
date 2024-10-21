import tkinter as tk
from tkinter import ttk

class SVVTestPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="25 25 25 25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # 主观视觉垂直线偏斜方向
        ttk.Label(main_frame, text="主观视觉垂直线偏斜方向:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.direction_var = tk.StringVar()
        direction_combobox = ttk.Combobox(main_frame, textvariable=self.direction_var, width=20)
        direction_combobox['values'] = ["左偏", "右偏", "无偏斜", "配合欠佳"]
        direction_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 主观视觉垂直线偏斜角度（度）
        ttk.Label(main_frame, text="主观视觉垂直线偏斜角度（度）:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.angle_var = tk.StringVar()
        angle_entry = ttk.Entry(main_frame, textvariable=self.angle_var, width=10)
        angle_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 主观视觉垂直线检查结果
        ttk.Label(main_frame, text="主观视觉垂直线检查结果:").grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        self.result_var = tk.StringVar()
        result_combobox = ttk.Combobox(main_frame, textvariable=self.result_var, width=20)
        result_combobox['values'] = ["正常", "异常", "配合欠佳"]
        result_combobox.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    def get_data(self):
        return {
            "主观视觉垂直线 (SVV)": {
                "偏斜方向": self.direction_var.get(),
                "偏斜角度（度）": self.angle_var.get(),
                "检查结果": self.result_var.get()
            }
        }
        
    def set_data(self, data):
        self.direction_entry.delete(0, tk.END)
        self.direction_entry.insert(0, data.get("偏斜方向", ""))
        self.angle_entry.delete(0, tk.END)
        self.angle_entry.insert(0, data.get("偏斜角度（度）", ""))
        self.result_entry.delete(0, tk.END)
        self.result_entry.insert(0, data.get("检查结果", ""))