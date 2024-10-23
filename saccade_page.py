import tkinter as tk
from tkinter import ttk

class SaccadePage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="30 30 30 30")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # 创建左右两列
        left_frame = ttk.LabelFrame(main_frame, text="右向扫视", padding="10 10 10 10")
        left_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=(0, 10))
        right_frame = ttk.LabelFrame(main_frame, text="左向扫视", padding="10 10 10 10")
        right_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W), padx=(10, 0))

        # 右向扫视参数
        self.create_entry(left_frame, "扫视延迟时间 (毫秒):", "right_delay", 0)
        self.create_entry(left_frame, "扫视峰速度 (度/秒):", "right_peak_velocity", 1)
        self.create_entry(left_frame, "扫视精确度 (%):", "right_accuracy", 2)

        # 左向扫视参数
        self.create_entry(right_frame, "扫视延迟时间 (毫秒):", "left_delay", 0)
        self.create_entry(right_frame, "扫视峰速度 (度/秒):", "left_peak_velocity", 1)
        self.create_entry(right_frame, "扫视精确度 (%):", "left_accuracy", 2)

        # 扫视检查结果
        result_frame = ttk.LabelFrame(main_frame, text="扫视检查结果", padding="10 10 10 10")
        result_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.E, tk.W), pady=(20, 0))
        self.saccade_result = ttk.Combobox(result_frame, values=["", "正常", "异常", "配合欠佳"])
        self.saccade_result.grid(row=0, column=0, sticky=(tk.E, tk.W), padx=5, pady=5)
        result_frame.columnconfigure(0, weight=1)

    def create_entry(self, parent, label, attr_name, row):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky=tk.E, padx=5, pady=5)
        entry = ttk.Entry(parent)
        entry.grid(row=row, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        setattr(self, attr_name, entry)

    def get_data(self):
        return {
            "扫视检查": {
                "扫视延迟时间 (右向, 毫秒)": self.right_delay.get(),
                "扫视延迟时间 (左向, 毫秒)": self.left_delay.get(),
                "扫视峰速度 (右向, 度/秒)": self.right_peak_velocity.get(),
                "扫视峰速度 (左向, 度/秒)": self.left_peak_velocity.get(),
                "扫视精确度 (右向, %)": self.right_accuracy.get(),
                "扫视精确度 (左向, %)": self.left_accuracy.get(),
                "扫视检查结果": self.saccade_result.get()
            }
        }
        
    def set_data(self, data):
        self.right_delay.delete(0, tk.END)
        self.right_delay.insert(0, data.get("扫视延迟时间 (右向, 毫秒)", ""))
        self.left_delay.delete(0, tk.END)
        self.left_delay.insert(0, data.get("扫视延迟时间 (左向, 毫秒)", ""))
        self.right_peak_velocity.delete(0, tk.END)
        self.right_peak_velocity.insert(0, data.get("扫视峰速度 (右向, 度/秒)", ""))
        self.left_peak_velocity.delete(0, tk.END)
        self.left_peak_velocity.insert(0, data.get("扫视峰速度 (左向, 度/秒)", ""))
        self.right_accuracy.delete(0, tk.END)
        self.right_accuracy.insert(0, data.get("扫视精确度 (右向, %)", ""))
        self.left_accuracy.delete(0, tk.END)
        self.left_accuracy.insert(0, data.get("扫视精确度 (左向, %)", ""))
        self.saccade_result.set(data.get("扫视检查结果", ""))