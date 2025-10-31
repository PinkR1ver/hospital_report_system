import tkinter as tk
from tkinter import ttk

class VORSuppressionPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="30 30 30 30")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # 前庭-眼反射抑制试验检查结果
        ttk.Label(main_frame, text="前庭-眼反射抑制试验检查结果:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.vor_suppression_result = ttk.Combobox(main_frame, values=["", "正常", "异常", "配合欠佳"], width=20)
        self.vor_suppression_result.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

    def get_data(self):
        return {
            "前庭-眼反射抑制试验": {
                "检查结果": self.vor_suppression_result.get()
            }
        }

    def set_data(self, data):
        self.vor_suppression_result.set(data.get("检查结果", ""))
        
    def clear_inputs(self):
        self.vor_suppression_result.set("")

