import tkinter as tk
from tkinter import ttk

class HeadShakingTestPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="30 30 30 30")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # 眼震模式（摇头试验）
        ttk.Label(main_frame, text="眼震模式（摇头试验）:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.nystagmus_mode = ttk.Combobox(main_frame, values=[
            "", "I型摇头眼震", "II型摇头眼震", "III型摇头眼震", "IV型摇头眼震", 
            "其他", "阴性", "配合欠佳"
        ], width=20)
        self.nystagmus_mode.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # 眼震速度（摇头试验，度/秒）
        ttk.Label(main_frame, text="眼震速度（摇头试验，度/秒）:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.nystagmus_speed = ttk.Entry(main_frame, width=20)
        self.nystagmus_speed.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # 摇头试验检查结果
        ttk.Label(main_frame, text="摇头试验检查结果:").grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        self.test_result = ttk.Combobox(main_frame, values=["", "正常", "异常", "配合欠佳"], width=20)
        self.test_result.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

    def get_data(self):
        return {
            "摇头试验": {
                "眼震模式": self.nystagmus_mode.get(),
                "眼震速度": self.nystagmus_speed.get(),
                "检查结果": self.test_result.get()
            }
        }

    def set_data(self, data):
        self.nystagmus_mode.set(data.get("眼震模式", ""))
        self.nystagmus_speed.delete(0, tk.END)
        self.nystagmus_speed.insert(0, data.get("眼震速度", ""))
        self.test_result.set(data.get("检查结果", ""))