import tkinter as tk
from tkinter import ttk

class GazeNystagmusPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="25 25 25 25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        directions = ["上", "下", "左", "右"]
        self.nystagmus_vars = {}
        self.speed_entries = {}

        for i, direction in enumerate(directions):
            direction_frame = ttk.LabelFrame(main_frame, text=f"{direction}方凝视", padding="15 15 15 15")
            direction_frame.grid(row=i//2, column=i%2, sticky=(tk.W, tk.E), padx=10, pady=10)
            direction_frame.columnconfigure(1, weight=1)

            # 凝视性眼震模式
            ttk.Label(direction_frame, text="凝视性眼震模式:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
            self.nystagmus_vars[direction] = tk.StringVar()
            nystagmus_combobox = ttk.Combobox(direction_frame, textvariable=self.nystagmus_vars[direction], 
                                              values=["右跳性眼震", "左跳性眼震", "右跳+左转性眼震", "左跳+右转性眼震", 
                                                      "上跳性眼震", "下跳性眼震", "右转性眼震", "左转性眼震", 
                                                      "其他", "阴性", "配合欠佳", "NULL"])
            nystagmus_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

            # 凝视性眼震速度
            ttk.Label(direction_frame, text="凝视性眼震速度 (度/秒):").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
            self.speed_entries[direction] = ttk.Entry(direction_frame)
            self.speed_entries[direction].grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 凝视性眼震检查结果
        result_frame = ttk.LabelFrame(main_frame, text="检查结果", padding="10 10 10 10")
        result_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        result_frame.columnconfigure(1, weight=1)

        ttk.Label(result_frame, text="凝视性眼震检查结果:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.exam_result_var = tk.StringVar()
        self.exam_result_combobox = ttk.Combobox(result_frame, textvariable=self.exam_result_var, 
                                                 values=["阳性", "阴性", "配合欠佳"])
        self.exam_result_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    def get_data(self):
        data = {"凝视性眼震": {}}
        for direction in ["上", "下", "左", "右"]:
            data["凝视性眼震"][f"凝视性眼震模式（{direction}）"] = self.nystagmus_vars[direction].get()
            data["凝视性眼震"][f"凝视性眼震速度（{direction}）"] = self.speed_entries[direction].get()
        data["凝视性眼震"]["凝视性眼震检查结果"] = self.exam_result_var.get()
        return data
