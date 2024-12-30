import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
from datetime import datetime
import subprocess

class GazeNystagmusPage(ttk.Frame):
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
                                              values=["", "阴性", "右跳性眼震", "左跳性眼震", "右跳+左转性眼震", "左跳+右转性眼震", 
                                                      "上跳性眼震", "下跳性眼震", "右转性眼震", "左转性眼震", 
                                                      "其他", "配合欠佳", "NULL"])
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
                                                 values=["", "阳性", "阴性", "配合欠佳"])
        self.exam_result_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 视频导入
        video_frame = ttk.Frame(main_frame)
        video_frame.grid(row=3, column=0, columnspan=2, pady=10)

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
        data = {"凝视性眼震": {}}
        for direction in ["上", "下", "左", "右"]:
            data["凝视性眼震"][f"凝视性眼震模式（{direction}）"] = self.nystagmus_vars[direction].get()
            data["凝视性眼震"][f"凝视性眼震速度（{direction}）"] = self.speed_entries[direction].get()
        data["凝视性眼震"]["凝视性眼震检查结果"] = self.exam_result_var.get()
        data["凝视性眼震"]["视频"] = self.video_path
        return data
    
    def set_data(self, data):
        for direction in ['上', '下', '左', '右']:
            self.nystagmus_vars[direction].set(data.get(f"凝视性眼震模式（{direction}）", ""))
            self.speed_entries[direction].delete(0, tk.END)
            self.speed_entries[direction].insert(0, data.get(f"凝视性眼震速度（{direction}）", ""))
        self.exam_result_var.set(data.get("凝视性眼震检查结果", ""))
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
        for direction in ['上', '下', '左', '右']:
            self.nystagmus_vars[direction].set("")
            self.speed_entries[direction].delete(0, tk.END)
        self.exam_result_var.set("")
        self.video_path = ""
        self.video_label.config(text="未选择视频")
        self.open_video_button.config(state=tk.DISABLED)
        self.cancel_video_button.config(state=tk.DISABLED)
