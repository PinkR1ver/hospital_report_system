import tkinter as tk
from tkinter import ttk

class ReverseSkewPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="30 30 30 30")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # 眼位反向偏斜 (HR, 度)
        ttk.Label(main_frame, text="眼位反向偏斜 (HR, 度):").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.hr_skew = ttk.Entry(main_frame)
        self.hr_skew.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 眼位反向偏斜 (VR, 度)
        ttk.Label(main_frame, text="眼位反向偏斜 (VR, 度):").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.vr_skew = ttk.Entry(main_frame)
        self.vr_skew.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 眼位反向偏斜检查结果
        ttk.Label(main_frame, text="眼位反向偏斜检查结果:").grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        self.skew_result = ttk.Combobox(main_frame, values=["阳性", "阴性", "配合欠佳"])
        self.skew_result.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    def get_data(self):
        return {
            "眼位反向偏斜": {
                "眼位反向偏斜 (HR, 度)": self.hr_skew.get(),
                "眼位反向偏斜 (VR, 度)": self.vr_skew.get(),
                "眼位反向偏斜检查结果": self.skew_result.get()
            }
        }