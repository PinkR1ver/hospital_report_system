import tkinter as tk
from tkinter import ttk

class VisualTrackingPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="25 25 25 25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # 视跟踪曲线分型
        ttk.Label(main_frame, text="视跟踪曲线分型:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.curve_type_var = tk.StringVar()
        curve_type_combobox = ttk.Combobox(main_frame, textvariable=self.curve_type_var, width=30)
        curve_type_combobox['values'] = ["I型曲线", "II型曲线", "III型曲线", "IV型曲线", "配合欠佳", "NULL"]
        curve_type_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 视跟踪增益
        ttk.Label(main_frame, text="视跟踪增益:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.gain_var = tk.StringVar()
        gain_entry = ttk.Entry(main_frame, textvariable=self.gain_var, width=30)
        gain_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 视跟踪检查结果
        ttk.Label(main_frame, text="视跟踪检查结果:").grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        self.result_var = tk.StringVar()
        result_combobox = ttk.Combobox(main_frame, textvariable=self.result_var, width=30)
        result_combobox['values'] = ["正常", "异常", "配合欠佳"]
        result_combobox.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    def get_data(self):
        return {
            "视跟踪": {
                "视跟踪曲线分型": self.curve_type_var.get(),
                "视跟踪增益": self.gain_var.get(),
                "视跟踪检查结果": self.result_var.get()
            }
        }