import tkinter as tk
from tkinter import ttk, filedialog
import os
import shutil
from datetime import datetime

class HeadImpulseTestPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.image_path = ""
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="25 25 25 25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        canals = [
            ("左外半规管", "vor_left_lateral", "pr_left_lateral"),
            ("右外半规管", "vor_right_lateral", "pr_right_lateral"),
            ("左前半规管", "vor_left_anterior", "pr_left_anterior"),
            ("右后半规管", "vor_right_posterior", "pr_right_posterior"),
            ("左后半规管", "vor_left_posterior", "pr_left_posterior"),
            ("右前半规管", "vor_right_anterior", "pr_right_anterior")
        ]

        for i, (canal_name, vor_attr, pr_attr) in enumerate(canals):
            canal_frame = ttk.LabelFrame(main_frame, text=canal_name, padding="15 15 15 15")
            canal_frame.grid(row=i//2, column=i%2, sticky=(tk.W, tk.E), padx=10, pady=10)
            canal_frame.columnconfigure(1, weight=1)

            # VOR增益
            ttk.Label(canal_frame, text="VOR增益:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
            setattr(self, vor_attr, ttk.Entry(canal_frame))
            getattr(self, vor_attr).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

            # PR分数
            ttk.Label(canal_frame, text="PR分数 (%):").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
            setattr(self, pr_attr, ttk.Entry(canal_frame))
            getattr(self, pr_attr).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 头脉冲试验性眼跳抑制
        suppression_frame = ttk.LabelFrame(main_frame, text="头脉冲试验性眼跳抑制", padding="10 10 10 10")
        suppression_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        suppression_frame.columnconfigure(0, weight=1)

        self.hit_suppression_var = tk.StringVar()
        self.hit_suppression_combobox = ttk.Combobox(suppression_frame, textvariable=self.hit_suppression_var, 
                                                     values=["左外半规管", "右外半规管", "左前半规管", "右前半规管", "左后半规管", "右后半规管", "阴性", "配合欠佳", "NULL"])
        self.hit_suppression_combobox.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 头脉冲试验示意图
        image_frame = ttk.LabelFrame(main_frame, text="头脉冲试验示意图", padding="10 10 10 10")
        image_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        image_frame.columnconfigure(0, weight=1)

        self.image_button = ttk.Button(image_frame, text="选择图片", command=self.select_image)
        self.image_button.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 头脉冲试验检查结果
        result_frame = ttk.LabelFrame(main_frame, text="头脉冲试验检查结果", padding="10 10 10 10")
        result_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        result_frame.columnconfigure(0, weight=1)

        self.hit_result_var = tk.StringVar()
        self.hit_result_combobox = ttk.Combobox(result_frame, textvariable=self.hit_result_var, 
                                                values=["左外半规管功能低下", "右外半规管功能低下", "左前半规管功能低下", "右前半规管功能低下", 
                                                        "左后半规管功能低下", "右后半规管功能低下", "半规管功能正常", "配合欠佳"])
        self.hit_result_combobox.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

    def select_image(self):
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if self.image_path:
            self.image_button.config(text="图片已选择")

    def get_data(self):
        return {
            "头脉冲试验": {
                "VOR增益 (左外半规管)": self.vor_left_lateral.get(),
                "PR分数 (左外半规管)": self.pr_left_lateral.get(),
                "VOR增益 (右外半规管)": self.vor_right_lateral.get(),
                "PR分数 (右外半规管)": self.pr_right_lateral.get(),
                "VOR增益 (左前半规管)": self.vor_left_anterior.get(),
                "PR分数 (左前半规管)": self.pr_left_anterior.get(),
                "VOR增益 (右后半规管)": self.vor_right_posterior.get(),
                "PR分数 (右后半规管)": self.pr_right_posterior.get(),
                "VOR增益 (左后半规管)": self.vor_left_posterior.get(),
                "PR分数 (左后半规管)": self.pr_left_posterior.get(),
                "VOR增益 (右前半规管)": self.vor_right_anterior.get(),
                "PR分数 (右前半规管)": self.pr_right_anterior.get(),
                "头脉冲试验性眼跳抑制": self.hit_suppression_var.get(),
                "头脉冲试验示意图": self.image_path,
                "头脉冲试验检查结果": self.hit_result_var.get()
            }
        }

    def set_data(self, data):
        canals = [
            ("左外半规管", "vor_left_lateral", "pr_left_lateral"),
            ("右外半规管", "vor_right_lateral", "pr_right_lateral"),
            ("左前半规管", "vor_left_anterior", "pr_left_anterior"),
            ("右后半规管", "vor_right_posterior", "pr_right_posterior"),
            ("左后半规管", "vor_left_posterior", "pr_left_posterior"),
            ("右前半规管", "vor_right_anterior", "pr_right_anterior")
        ]
        
        for canal_name, vor_attr, pr_attr in canals:
            getattr(self, vor_attr).delete(0, tk.END)
            getattr(self, vor_attr).insert(0, data.get(f"VOR增益 ({canal_name})", ""))
            getattr(self, pr_attr).delete(0, tk.END)
            getattr(self, pr_attr).insert(0, data.get(f"PR分数 ({canal_name})", ""))
        
        self.hit_suppression_var.set(data.get("头脉冲试验性眼跳抑制", ""))
        
        if data.get("头脉冲试验示意图"):
            self.image_path = data.get("头脉冲试验示意图")
            self.image_button.config(text="图片已选择")
        else:
            self.image_path = ""
            self.image_button.config(text="选择图片")
        
        self.hit_result_var.set(data.get("头脉冲试验检查结果", ""))