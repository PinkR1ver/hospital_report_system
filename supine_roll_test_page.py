import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
from datetime import datetime
import subprocess

class SupineRollTestPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.video_path = ""
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="25 25 25 25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        sides = [("右侧", "right"), ("左侧", "left")]

        for i, (side_name, side_prefix) in enumerate(sides):
            side_frame = ttk.LabelFrame(main_frame, text=f"{side_name}仰卧滚转试验", padding="15 15 15 15")
            side_frame.grid(row=0, column=i, sticky=(tk.N, tk.S, tk.E, tk.W), padx=10, pady=10)
            side_frame.columnconfigure(1, weight=1)

            # 眼震模式
            ttk.Label(side_frame, text="眼震模式:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
            setattr(self, f"{side_prefix}_nystagmus_mode", ttk.Combobox(side_frame, values=[
                "", "上跳伴右扭眼震", "上跳伴左扭眼震", "下跳伴右扭眼震", "下跳伴左扭眼震",
                "右跳眼震", "左跳眼震", "右跳+右扭眼震", "左跳+左扭眼震",
                "右扭眼震", "左扭眼震", "上跳眼震", "下跳眼震",
                "其他", "阴性", "配合欠佳"
            ], width=25))
            getattr(self, f"{side_prefix}_nystagmus_mode").grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

            # 出现眩晕/头晕
            ttk.Label(side_frame, text="出现眩晕/头晕:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
            setattr(self, f"{side_prefix}_nystagmus_dizziness", ttk.Combobox(side_frame, values=["是", "否", "配合欠佳"], width=25))
            getattr(self, f"{side_prefix}_nystagmus_dizziness").grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

            # 眼震潜伏期
            ttk.Label(side_frame, text="眼震潜伏期 (秒):").grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
            setattr(self, f"{side_prefix}_latency", ttk.Entry(side_frame, width=25))
            getattr(self, f"{side_prefix}_latency").grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

            # 眼震持续时长
            ttk.Label(side_frame, text="眼震持续时长 (秒):").grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
            setattr(self, f"{side_prefix}_duration", ttk.Entry(side_frame, width=25))
            getattr(self, f"{side_prefix}_duration").grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

            # 眼震最大速度
            ttk.Label(side_frame, text="眼震最大速度 (度/秒):").grid(row=4, column=0, sticky=tk.E, padx=5, pady=5)
            setattr(self, f"{side_prefix}_max_speed", ttk.Entry(side_frame, width=25))
            getattr(self, f"{side_prefix}_max_speed").grid(row=4, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 位置试验检查结果
        result_frame = ttk.LabelFrame(main_frame, text="位置试验 (仰卧滚转试验) 检查结果", padding="10 10 10 10")
        result_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        result_frame.columnconfigure(0, weight=1)

        self.test_result = ttk.Combobox(result_frame, values=[
            "", "右外水平半规管良性阵发性位置性眩晕", "左外水平半规管良性阵发性位置性眩晕",
            "右外水平半规管椭圆囊瘘", "左外水平半规管椭圆囊瘘",
            "右外水平半规管杯囊瘘", "左外水平半规管杯囊瘘",
            "不典型位置性眼震", "阴性", "配合欠佳"
        ], width=50)
        self.test_result.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 添加视频导入部分
        video_frame = ttk.Frame(main_frame)
        video_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.video_button = ttk.Button(video_frame, text="导入视频", command=self.import_video)
        self.video_button.grid(row=0, column=0, padx=5)

        self.open_video_button = ttk.Button(video_frame, text="打开视频", command=self.open_video, state=tk.DISABLED)
        self.open_video_button.grid(row=0, column=1, padx=5)

        self.cancel_video_button = ttk.Button(video_frame, text="取消视频", command=self.cancel_video, state=tk.DISABLED)
        self.cancel_video_button.grid(row=0, column=2, padx=5)

        self.video_label = ttk.Label(video_frame, text="未选择视频")
        self.video_label.grid(row=1, column=0, columnspan=3, pady=5)

    def import_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")])
        if file_path:
            self.video_path = file_path
            video_filename = os.path.basename(file_path)
            self.video_label.config(text=f"已选择视频: {video_filename}")
            self.open_video_button.config(state=tk.NORMAL)
            self.cancel_video_button.config(state=tk.NORMAL)

    def open_video(self):
        if self.video_path:
            if os.path.exists(self.video_path):
                if os.name == 'nt':  # Windows
                    os.startfile(self.video_path)
                elif os.name == 'posix':  # macOS and Linux
                    subprocess.call(('open', self.video_path))
            else:
                tk.messagebox.showerror("错误", "视频文件不存在")

    def cancel_video(self):
        if self.video_path:
            result = messagebox.askyesno("确认", "确定要取消选择的视频吗？")
            if result:
                db_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                full_path = os.path.join(db_path, self.video_path)
                if os.path.exists(full_path):
                    os.remove(full_path)
                self.video_path = ""
                self.video_label.config(text="未选择视频")
                self.open_video_button.config(state=tk.DISABLED)
                self.cancel_video_button.config(state=tk.DISABLED)

    def get_data(self):
        data = {
            "位置试验 (仰卧滚转试验)": {
                "右侧眼震模式": self.right_nystagmus_mode.get(),
                "右侧出现眩晕/头晕": self.right_nystagmus_dizziness.get(),
                "右侧眼震潜伏期 (秒)": self.right_latency.get(),
                "右侧眼震持续时长 (秒)": self.right_duration.get(),
                "右侧眼震最大速度 (度/秒)": self.right_max_speed.get(),
                "左侧眼震模式": self.left_nystagmus_mode.get(),
                "左侧出现眩晕/头晕": self.left_nystagmus_dizziness.get(),
                "左侧眼震潜伏期 (秒)": self.left_latency.get(),
                "左侧眼震持续时长 (秒)": self.left_duration.get(),
                "左侧眼震最大速度 (度/秒)": self.left_max_speed.get(),
                "检查结果": self.test_result.get(),
                "视频": self.video_path
            }
        }
        return data
        
    def set_data(self, data):
        sides = [('right', '右侧'), ('left', '左侧')]
        for side_prefix, side_name in sides:
            getattr(self, f"{side_prefix}_nystagmus_mode").set(data.get(f"{side_name}眼震模式", ""))
            getattr(self, f"{side_prefix}_nystagmus_dizziness").set(data.get(f"{side_name}出现眩晕/头晕", ""))
            getattr(self, f"{side_prefix}_latency").delete(0, tk.END)
            getattr(self, f"{side_prefix}_latency").insert(0, data.get(f"{side_name}眼震潜伏期 (秒)", ""))
            getattr(self, f"{side_prefix}_duration").delete(0, tk.END)
            getattr(self, f"{side_prefix}_duration").insert(0, data.get(f"{side_name}眼震持续时长 (秒)", ""))
            getattr(self, f"{side_prefix}_max_speed").delete(0, tk.END)
            getattr(self, f"{side_prefix}_max_speed").insert(0, data.get(f"{side_name}眼震最大速度 (度/秒)", ""))
        self.test_result.set(data.get("检查结果", ""))
        self.video_path = data.get("视频", "")
        if self.video_path:
            self.video_label.config(text=f"已选择视频: {os.path.basename(self.video_path)}")
            self.open_video_button.config(state=tk.NORMAL)
            self.cancel_video_button.config(state=tk.NORMAL)
        else:
            self.video_label.config(text="未选择视频")
            self.open_video_button.config(state=tk.DISABLED)
            self.cancel_video_button.config(state=tk.DISABLED)


    def clear_inputs(self):
        self.right_nystagmus_mode.set("")
        self.right_nystagmus_dizziness.set("")
        self.right_latency.delete(0, tk.END)
        self.right_duration.delete(0, tk.END)
        self.right_max_speed.delete(0, tk.END)
        self.left_nystagmus_mode.set("")
        self.left_nystagmus_dizziness.set("")
        self.left_latency.delete(0, tk.END)
        self.left_duration.delete(0, tk.END)
        self.left_max_speed.delete(0, tk.END)
        self.test_result.set("")
        self.video_path = ""
        self.video_label.config(text="未选择视频")
        self.open_video_button.config(state=tk.DISABLED)
        self.cancel_video_button.config(state=tk.DISABLED)



