import tkinter as tk
from tkinter import ttk

class SpontaneousNystagmusPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)

        # 自发性眼震模式
        ttk.Label(main_frame, text="自发性眼震模式:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.nystagmus_mode_var = tk.StringVar()
        self.nystagmus_mode_combobox = ttk.Combobox(main_frame, textvariable=self.nystagmus_mode_var, 
                                                    values=["右跳性眼震", "左跳性眼震", "左跳+右转性眼震", "右跳+左转性眼震", 
                                                            "上跳性眼震", "下跳性眼震", "右转性眼震", "左转性眼震", "摆动性眼震", 
                                                            "垂直性眼震", "旋转性眼震", "周期交替性眼震", "其他", "阴性", "配合欠佳", "NULL"])
        self.nystagmus_mode_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 自发性眼震速度
        ttk.Label(main_frame, text="自发性眼震速度 (度/秒):").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.nystagmus_speed_entry = ttk.Entry(main_frame)
        self.nystagmus_speed_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 自发性眼震固视抑制
        ttk.Label(main_frame, text="自发性眼震固视抑制:").grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        self.fixation_suppression_var = tk.StringVar()
        self.fixation_suppression_combobox = ttk.Combobox(main_frame, textvariable=self.fixation_suppression_var, 
                                                          values=["固视抑制", "固视不抑制", "配合欠佳", "NULL"])
        self.fixation_suppression_combobox.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 自发性眼震检查结果
        ttk.Label(main_frame, text="自发性眼震检查结果:").grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
        self.exam_result_var = tk.StringVar()
        self.exam_result_combobox = ttk.Combobox(main_frame, textvariable=self.exam_result_var, 
                                                 values=["阳性", "阴性", "配合欠佳"])
        self.exam_result_combobox.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    def get_data(self):
        return {
            "自发性眼震": {
                "自发性眼震模式": self.nystagmus_mode_var.get(),
                "自发性眼震速度": self.nystagmus_speed_entry.get(),
                "自发性眼震固视抑制": self.fixation_suppression_var.get(),
                "自发性眼震检查结果": self.exam_result_var.get()
            }
        }
