import tkinter as tk
from tkinter import ttk

class OtherPositionTestPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="25 25 25 25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        tests = [
            ("坐位-平卧试验", "sitting_supine"),
            ("坐位-低头试验", "sitting_head_down"),
            ("坐位-仰头试验", "sitting_head_up"),
            ("零平面", "zero_plane")
        ]

        for i, (test_name, test_prefix) in enumerate(tests):
            ttk.Label(main_frame, text=f"{test_name}:").grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            setattr(self, f"{test_prefix}_var", tk.StringVar())
            combobox = ttk.Combobox(main_frame, textvariable=getattr(self, f"{test_prefix}_var"), width=30)
            
            if test_prefix == "zero_plane":
                combobox['values'] = ["仰卧右侧转", "仰卧左侧转", "其他", "阴性", "配合欠佳", "NULL"]
            else:
                combobox['values'] = ["右跳性眼震", "左跳性眼震", "其他", "阴性", "配合欠佳", "NULL"]
            
            combobox.grid(row=i, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 位置试验(其他)检查结果
        ttk.Label(main_frame, text="位置试验(其他)检查结果:").grid(row=len(tests), column=0, sticky=tk.E, padx=5, pady=5)
        self.result_var = tk.StringVar()
        result_combobox = ttk.Combobox(main_frame, textvariable=self.result_var, width=30)
        result_combobox['values'] = ["正常", "异常", "配合欠佳"]
        result_combobox.grid(row=len(tests), column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    def get_data(self):
        return {
            "位置试验(其他)": {
                "坐位-平卧试验": self.sitting_supine_var.get(),
                "坐位-低头试验": self.sitting_head_down_var.get(),
                "坐位-仰头试验": self.sitting_head_up_var.get(),
                "零平面": self.zero_plane_var.get(),
                "检查结果": self.result_var.get()
            }
        }