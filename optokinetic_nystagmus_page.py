import tkinter as tk
from tkinter import ttk

class OptoKineticNystagmusPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="25 25 25 25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # 视动性眼震（水平视标）不对称性（%）
        ttk.Label(main_frame, text="视动性眼震（水平视标）不对称性（%）:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.asymmetry_var = tk.StringVar()
        asymmetry_entry = ttk.Entry(main_frame, textvariable=self.asymmetry_var, width=10)
        asymmetry_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 视动性眼震增益（向右视标）
        ttk.Label(main_frame, text="视动性眼震增益（向右视标）:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.right_gain_var = tk.StringVar()
        right_gain_entry = ttk.Entry(main_frame, textvariable=self.right_gain_var, width=10)
        right_gain_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 视动性眼震增益（向左视标）
        ttk.Label(main_frame, text="视动性眼震增益（向左视标）:").grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        self.left_gain_var = tk.StringVar()
        left_gain_entry = ttk.Entry(main_frame, textvariable=self.left_gain_var, width=10)
        left_gain_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 视动性眼震检查结果
        ttk.Label(main_frame, text="视动性眼震检查结果:").grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
        self.result_var = tk.StringVar()
        result_combobox = ttk.Combobox(main_frame, textvariable=self.result_var, width=20)
        result_combobox['values'] = ["正常", "异常", "配合欠佳"]
        result_combobox.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    def get_data(self):
        return {
            "视动性眼震": {
                "不对称性（%）": self.asymmetry_var.get(),
                "向右视标增益": self.right_gain_var.get(),
                "向左视标增益": self.left_gain_var.get(),
                "检查结果": self.result_var.get()
            }
        }

    def set_data(self, data):
        self.asymmetry_var.set(data.get("不对称性（%）", ""))
        self.right_gain_var.set(data.get("向右视标增益", ""))
        self.left_gain_var.set(data.get("向左视标增益", ""))
        self.result_var.set(data.get("检查结果", ""))