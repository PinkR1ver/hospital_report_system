import tkinter as tk
from tkinter import ttk

class CVEMPTestPage(ttk.Frame):
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
        
        ttk.Label(frame, text="声强阈值 (cVEMP, 分贝):").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        setattr(self, f"{prefix}_threshold_var", tk.StringVar())
        ttk.Entry(frame, textvariable=getattr(self, f"{prefix}_threshold_var"), width=10).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        labels = [
            ("P13波潜伏期 (毫秒):", "p13_latency"),
            ("N23波潜伏期 (毫秒):", "n23_latency"),
            ("P13-N23波间期 (毫秒):", "p13_n23_interval"),
            ("P13波振幅 (微伏):", "p13_amplitude"),
            ("N23波振幅 (微伏):", "n23_amplitude"),
            ("P13-N23波振幅 (微伏):", "p13_n23_amplitude")
        ]

        for i, (label, var_suffix) in enumerate(labels, start=1):
            ttk.Label(frame, text=label).grid(row=i, column=0, sticky=tk.E, padx=5, pady=5)
            var_name = f"{prefix}_{var_suffix}_var"
            setattr(self, var_name, tk.StringVar())
            ttk.Entry(frame, textvariable=getattr(self, var_name), width=10).grid(row=i, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    def create_bottom_section(self, frame):
        ttk.Label(frame, text="cVEMP耳间不对称性 (%):").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.asymmetry_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.asymmetry_var, width=10).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(frame, text="cVEMP检查结果:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.result_var = tk.StringVar()
        result_combobox = ttk.Combobox(frame, textvariable=self.result_var, width=20)
        result_combobox['values'] = ["正常", "异常", "配合欠佳"]
        result_combobox.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    def get_data(self):
        data = {
            "颈肌前庭诱发肌源性电位 (cVEMP)": {
                "右耳声强阈值 (分贝)": self.right_threshold_var.get(),
                "右耳P13波潜伏期 (毫秒)": self.right_p13_latency_var.get(),
                "右耳N23波潜伏期 (毫秒)": self.right_n23_latency_var.get(),
                "右耳P13-N23波间期 (毫秒)": self.right_p13_n23_interval_var.get(),
                "右耳P13波振幅 (微伏)": self.right_p13_amplitude_var.get(),
                "右耳N23波振幅 (微伏)": self.right_n23_amplitude_var.get(),
                "右耳P13-N23波振幅 (微伏)": self.right_p13_n23_amplitude_var.get(),
                "左耳声强阈值 (分贝)": self.left_threshold_var.get(),
                "左耳P13波潜伏期 (毫秒)": self.left_p13_latency_var.get(),
                "左耳N23波潜伏期 (毫秒)": self.left_n23_latency_var.get(),
                "左耳P13-N23波间期 (毫秒)": self.left_p13_n23_interval_var.get(),
                "左耳P13波振幅 (微伏)": self.left_p13_amplitude_var.get(),
                "左耳N23波振幅 (微伏)": self.left_n23_amplitude_var.get(),
                "左耳P13-N23波振幅 (微伏)": self.left_p13_n23_amplitude_var.get(),
                "cVEMP耳间不对称性 (%)": self.asymmetry_var.get(),
                "检查结果": self.result_var.get()
            }
        }
        return data

def set_data(self, data):
    sides = ['右耳', '左耳']
    for side in sides:
        self.threshold_entries[side].delete(0, tk.END)
        self.threshold_entries[side].insert(0, data.get(f"{side}声强阈值 (分贝)", ""))
        self.p13_latency_entries[side].delete(0, tk.END)
        self.p13_latency_entries[side].insert(0, data.get(f"{side}P13波潜伏期 (毫秒)", ""))
        self.n23_latency_entries[side].delete(0, tk.END)
        self.n23_latency_entries[side].insert(0, data.get(f"{side}N23波潜伏期 (毫秒)", ""))
        self.p13_n23_interval_entries[side].delete(0, tk.END)
        self.p13_n23_interval_entries[side].insert(0, data.get(f"{side}P13-N23波间期 (毫秒)", ""))
        self.p13_amplitude_entries[side].delete(0, tk.END)
        self.p13_amplitude_entries[side].insert(0, data.get(f"{side}P13波振幅 (微伏)", ""))
        self.n23_amplitude_entries[side].delete(0, tk.END)
        self.n23_amplitude_entries[side].insert(0, data.get(f"{side}N23波振幅 (微伏)", ""))
        self.p13_n23_amplitude_entries[side].delete(0, tk.END)
        self.p13_n23_amplitude_entries[side].insert(0, data.get(f"{side}P13-N23波振幅 (微伏)", ""))
    self.asymmetry_entry.delete(0, tk.END)
    self.asymmetry_entry.insert(0, data.get("cVEMP耳间不对称性 (%)", ""))
    self.result_entry.delete(0, tk.END)
    self.result_entry.insert(0, data.get("检查结果", ""))