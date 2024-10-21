import tkinter as tk
from tkinter import ttk

class FistulaTestPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="25 25 25 25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # 瘘管试验结果
        ttk.Label(main_frame, text="瘘管试验结果:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.result_var = tk.StringVar()
        result_combobox = ttk.Combobox(main_frame, textvariable=self.result_var, width=30)
        result_combobox['values'] = ["阴性", "右侧阳性", "左侧阳性", "双侧阳性", "配合欠佳"]
        result_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    def get_data(self):
        return {
            "瘘管试验": {
                "结果": self.result_var.get()
            }
        }
    
    def set_data(self, data):
        self.result_var.set(data.get("结果", ""))