import tkinter as tk
from tkinter import ttk, filedialog
import os
from datetime import datetime
import shutil

class HeadImpulseSuppressionTestPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.image_path = ""
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="30 30 30 30")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # 左外半规管增益
        ttk.Label(main_frame, text="头脉冲抑制试验增益 (左外半规管):").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.left_gain = ttk.Entry(main_frame)
        self.left_gain.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 右外半规管增益
        ttk.Label(main_frame, text="头脉冲抑制试验增益 (右外半规管):").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.right_gain = ttk.Entry(main_frame)
        self.right_gain.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 补偿性扫视波
        ttk.Label(main_frame, text="头脉冲抑制试验补偿性扫视波:").grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        self.compensatory_saccade = ttk.Combobox(main_frame, 
                                                 values=["左外半规管", "右外半规管", "阴性", "配合欠佳", "NULL"])
        self.compensatory_saccade.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 示意图
        ttk.Label(main_frame, text="头脉冲抑制试验示意图:").grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
        self.image_button = ttk.Button(main_frame, text="选择图片", command=self.select_image)
        self.image_button.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 检查结果
        ttk.Label(main_frame, text="头脉冲抑制试验检查结果:").grid(row=4, column=0, sticky=tk.E, padx=5, pady=5)
        self.test_result = ttk.Combobox(main_frame, 
                                        values=["左外半规管功能低下", "右外半规管功能低下", "双侧外半规管功能低下", "配合欠佳"])
        self.test_result.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    def select_image(self):
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if self.image_path:
            self.image_button.config(text="图片已选择")

    def get_data(self):
        return {
            "头脉冲抑制试验": {
                "头脉冲抑制试验增益 (左外半规管)": self.left_gain.get(),
                "头脉冲抑制试验增益 (右外半规管)": self.right_gain.get(),
                "头脉冲抑制试验补偿性扫视波": self.compensatory_saccade.get(),
                "头脉冲抑制试验示意图": self.image_path,
                "头脉冲抑制试验检查结果": self.test_result.get()
            }
        }

    def set_data(self, data):
        self.left_gain.delete(0, tk.END)
        self.left_gain.insert(0, data.get("头脉冲抑制试验增益 (左外半规管)", ""))
        
        self.right_gain.delete(0, tk.END)
        self.right_gain.insert(0, data.get("头脉冲抑制试验增益 (右外半规管)", ""))
        
        self.compensatory_saccade.set(data.get("头脉冲抑制试验补偿性扫视波", ""))
        
        self.image_path = data.get("头脉冲抑制试验示意图", "")
        if self.image_path:
            self.image_button.config(text="图片已选择")
        else:
            self.image_button.config(text="选择图片")
        
        self.test_result.set(data.get("头脉冲抑制试验检查结果", ""))