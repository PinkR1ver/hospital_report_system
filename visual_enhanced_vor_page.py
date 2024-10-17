import tkinter as tk
from tkinter import ttk

class VisualEnhancedVORPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="30 30 30 30")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # 检查结果
        ttk.Label(main_frame, text="视觉增强前庭-眼反射试验检查结果:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.vor_result = ttk.Combobox(main_frame, values=["正常", "异常", "配合欠佳"], width=20)
        self.vor_result.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

    def get_data(self):
        return {
            "视觉增强前庭-眼反射试验": {
                "检查结果": self.vor_result.get()
            }
        }
