import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
from datetime import datetime
import subprocess

class SpontaneousNystagmusPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.video_path = ""
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="25 25 25 25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # 自发性眼震模式
        ttk.Label(main_frame, text="自发性眼震模式:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.nystagmus_mode = ttk.Combobox(main_frame, values=[
            "", "右跳性眼震", "左跳性眼震", "右跳+左转性眼震", "左跳+右转性眼震", 
            "上跳性眼震", "下跳性眼震", "右转性眼震", "左转性眼震", 
            "其他", "阴性", "配合欠佳"
        ], width=30)
        self.nystagmus_mode.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 自发性眼震速度
        ttk.Label(main_frame, text="自发性眼震速度 (度/秒):").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.nystagmus_speed = ttk.Entry(main_frame, width=30)
        self.nystagmus_speed.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # 自发性眼震固视抑制
        ttk.Label(main_frame, text="自发性眼震固视抑制:").grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        self.fixation_suppression = ttk.Combobox(main_frame, values=["", "固视抑制", "固视不抑制", "配合欠佳"], width=30)
        self.fixation_suppression.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 自发性眼震检查结果
        ttk.Label(main_frame, text="自发性眼震检查结果:").grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
        self.exam_result = ttk.Combobox(main_frame, values=["", "正常", "异常", "配合欠佳"], width=30)
        self.exam_result.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 视频导入
        video_frame = ttk.Frame(main_frame)
        video_frame.grid(row=4, column=0, columnspan=2, pady=10)

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
        return {
            "自发性眼震": {
                "自发性眼震模式": self.nystagmus_mode.get(),
                "自发性眼震速度": self.nystagmus_speed.get(),
                "自发性眼震检查结果": self.exam_result.get(),
                "自发性眼震固视抑制": self.fixation_suppression.get(),
                "视频": self.video_path
            }
        }

    def set_data(self, data):
        self.nystagmus_mode.set(data.get("自发性眼震模式", ""))
        self.nystagmus_speed.delete(0, tk.END)
        self.nystagmus_speed.insert(0, data.get("自发性眼震速度", ""))
        self.fixation_suppression.set(data.get("自发性眼震固视抑制", ""))
        self.exam_result.set(data.get("自发性眼震检查结果", ""))
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
        self.nystagmus_mode.set("")
        self.nystagmus_speed.delete(0, tk.END)
        self.fixation_suppression.set("")
        self.exam_result.set("")
        self.video_path = ""
        self.video_label.config(text="未选择视频")
        self.open_video_button.config(state=tk.DISABLED)
        self.cancel_video_button.config(state=tk.DISABLED)
