import tkinter as tk
from tkinter import ttk

class OVEMPTestPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="25 25 25 25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        left_frame = ttk.LabelFrame(main_frame, text="右耳", padding="10 10 10 10")
        left_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=(0, 10))
        right_frame = ttk.LabelFrame(main_frame, text="左耳", padding="10 10 10 10")
        right_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W), padx=(10, 0))

        self.create_ear_column(left_frame, "right")
        self.create_ear_column(right_frame, "left")

        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 0))
        self.create_bottom_section(bottom_frame)

    def create_ear_column(self, frame, ear):
        prefix = ear
        
        ttk.Label(frame, text="声强阈值 (oVEMP, 分贝):").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        setattr(self, f"{prefix}_threshold_var", tk.StringVar())
        ttk.Entry(frame, textvariable=getattr(self, f"{prefix}_threshold_var"), width=10).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        labels = [
            ("N10波潜伏期 (毫秒):", "n10_latency"),
            ("P15波潜伏期 (毫秒):", "p15_latency"),
            ("N10-P15波间期 (毫秒):", "n10_p15_interval"),
            ("N10波振幅 (微伏):", "n10_amplitude"),
            ("P15波振幅 (微伏):", "p15_amplitude"),
            ("N10-P15波振幅 (微伏):", "n10_p15_amplitude")
        ]

        for i, (label, var_suffix) in enumerate(labels, start=1):
            ttk.Label(frame, text=label).grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            var_name = f"{prefix}_{var_suffix}_var"
            setattr(self, var_name, tk.StringVar())
            ttk.Entry(frame, textvariable=getattr(self, var_name), width=10).grid(row=i, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    def create_bottom_section(self, frame):
        ttk.Label(frame, text="oVEMP耳间不对称性 (%):").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.asymmetry_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.asymmetry_var, width=10).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(frame, text="oVEMP检查结果:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.result_var = tk.StringVar()
        result_combobox = ttk.Combobox(frame, textvariable=self.result_var, width=20)
        result_combobox['values'] = ["正常", "异常", "配合欠佳"]
        result_combobox.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    def get_data(self):
        data = {
            "眼肌前庭诱发肌源性电位 (oVEMP)": {
                "右耳声强阈值 (分贝)": self.right_threshold_var.get(),
                "右耳N10波潜伏期 (毫秒)": self.right_n10_latency_var.get(),
                "右耳P15波潜伏期 (毫秒)": self.right_p15_latency_var.get(),
                "右耳N10-P15波间期 (毫秒)": self.right_n10_p15_interval_var.get(),
                "右耳N10波振幅 (微伏)": self.right_n10_amplitude_var.get(),
                "右耳P15波振幅 (微伏)": self.right_p15_amplitude_var.get(),
                "右耳N10-P15波振幅 (微伏)": self.right_n10_p15_amplitude_var.get(),
                "左耳声强阈值 (分贝)": self.left_threshold_var.get(),
                "左耳N10波潜伏期 (毫秒)": self.left_n10_latency_var.get(),
                "左耳P15波潜伏期 (毫秒)": self.left_p15_latency_var.get(),
                "左耳N10-P15波间期 (毫秒)": self.left_n10_p15_interval_var.get(),
                "左耳N10波振幅 (微伏)": self.left_n10_amplitude_var.get(),
                "左耳P15波振幅 (微伏)": self.left_p15_amplitude_var.get(),
                "左耳N10-P15波振幅 (微伏)": self.left_n10_p15_amplitude_var.get(),
                "oVEMP耳间不对称性 (%)": self.asymmetry_var.get(),
                "检查结果": self.result_var.get()
            }
        }
        return data

    def set_data(self, data):
        sides = ['右耳', '左耳']
        for side in sides:
            self.threshold_entries[side].delete(0, tk.END)
            self.threshold_entries[side].insert(0, data.get(f"{side}声强阈值 (分贝)", ""))
            self.n10_latency_entries[side].delete(0, tk.END)
            self.n10_latency_entries[side].insert(0, data.get(f"{side}N10波潜伏期 (毫秒)", ""))
            self.p15_latency_entries[side].delete(0, tk.END)
            self.p15_latency_entries[side].insert(0, data.get(f"{side}P15波潜伏期 (毫秒)", ""))
            self.n10_p15_interval_entries[side].delete(0, tk.END)
            self.n10_p15_interval_entries[side].insert(0, data.get(f"{side}N10-P15波间期 (毫秒)", ""))
            self.n10_amplitude_entries[side].delete(0, tk.END)
            self.n10_amplitude_entries[side].insert(0, data.get(f"{side}N10波振幅 (微伏)", ""))
            self.p15_amplitude_entries[side].delete(0, tk.END)
            self.p15_amplitude_entries[side].insert(0, data.get(f"{side}P15波振幅 (微伏)", ""))
            self.n10_p15_amplitude_entries[side].delete(0, tk.END)
            self.n10_p15_amplitude_entries[side].insert(0, data.get(f"{side}N10-P15波振幅 (微伏)", ""))
        self.asymmetry_entry.delete(0, tk.END)
        self.asymmetry_entry.insert(0, data.get("oVEMP耳间不对称性 (%)", ""))
        self.result_entry.delete(0, tk.END)
        self.result_entry.insert(0, data.get("检查结果", ""))