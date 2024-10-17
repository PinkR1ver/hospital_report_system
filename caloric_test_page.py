import tkinter as tk
from tkinter import ttk

class CaloricTestPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="25 25 25 25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # 创建三个部分
        self.create_unilateral_weakness_section(main_frame)
        self.create_directional_preponderance_section(main_frame)
        self.create_spv_section(main_frame)

        # 固视抑制指数
        self.create_fixation_index_section(main_frame)

        # 检查结果
        self.create_result_section(main_frame)

    def create_unilateral_weakness_section(self, parent):
        frame = ttk.LabelFrame(parent, text="单侧减弱 (UW)", padding="10 10 10 10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        ttk.Label(frame, text="侧别:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.uw_side_var = tk.StringVar()
        uw_side_combobox = ttk.Combobox(frame, textvariable=self.uw_side_var, width=20)
        uw_side_combobox['values'] = ["右耳", "左耳", "左右对称"]
        uw_side_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(frame, text="数值 (%):").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.uw_value_var = tk.StringVar()
        uw_value_entry = ttk.Entry(frame, textvariable=self.uw_value_var, width=10)
        uw_value_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    def create_directional_preponderance_section(self, parent):
        frame = ttk.LabelFrame(parent, text="优势偏向 (DP)", padding="10 10 10 10")
        frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        ttk.Label(frame, text="侧别:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.dp_side_var = tk.StringVar()
        dp_side_combobox = ttk.Combobox(frame, textvariable=self.dp_side_var, width=20)
        dp_side_combobox['values'] = ["右耳", "左耳", "左右对称"]
        dp_side_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(frame, text="数值 (度/秒):").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.dp_value_var = tk.StringVar()
        dp_value_entry = ttk.Entry(frame, textvariable=self.dp_value_var, width=10)
        dp_value_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    def create_spv_section(self, parent):
        frame = ttk.LabelFrame(parent, text="最大慢相速度总和", padding="10 10 10 10")
        frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        ttk.Label(frame, text="右耳 (度/秒):").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.right_ear_spv_var = tk.StringVar()
        right_ear_spv_entry = ttk.Entry(frame, textvariable=self.right_ear_spv_var, width=10)
        right_ear_spv_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(frame, text="左耳 (度/秒):").grid(row=0, column=2, sticky=tk.E, padx=5, pady=5)
        self.left_ear_spv_var = tk.StringVar()
        left_ear_spv_entry = ttk.Entry(frame, textvariable=self.left_ear_spv_var, width=10)
        left_ear_spv_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=5, pady=5)

    def create_fixation_index_section(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(frame, text="固视抑制指数 (FI, %):").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.fi_var = tk.StringVar()
        fi_entry = ttk.Entry(frame, textvariable=self.fi_var, width=10)
        fi_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    def create_result_section(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(frame, text="温度试验检查结果:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.result_var = tk.StringVar()
        result_combobox = ttk.Combobox(frame, textvariable=self.result_var, width=40)
        result_combobox['values'] = [
            "左外半规管功能减退", "右外半规管功能减退",
            "双外半规管功能减退", "双外半规管功能正常",
            "配合欠佳"
        ]
        result_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    def get_data(self):
        return {
            "温度试验": {
                "单侧减弱侧别 (UW)": self.uw_side_var.get(),
                "单侧减弱数值 (UW, %)": self.uw_value_var.get(),
                "优势偏向侧别 (DP)": self.dp_side_var.get(),
                "优势偏向数值 (DP, 度/秒)": self.dp_value_var.get(),
                "最大慢相速度总和（右耳, 度/秒）": self.right_ear_spv_var.get(),
                "最大慢相速度总和（左耳, 度/秒）": self.left_ear_spv_var.get(),
                "固视抑制指数 (FI, %)": self.fi_var.get(),
                "检查结果": self.result_var.get()
            }
        }
