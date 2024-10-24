import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
from datetime import datetime
import subprocess

class OtherPositionTestPage(ttk.Frame):
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
                combobox['values'] = ["", "仰卧右侧转", "仰卧左侧转", "其他", "阴性", "配合欠佳"]
            else:
                combobox['values'] = ["", "右跳性眼震", "左跳性眼震", "其他", "阴性", "配合欠佳"]
            
            combobox.grid(row=i, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 位置试验(其他)检查结果
        ttk.Label(main_frame, text="位置试验(其他)检查结果:").grid(row=len(tests), column=0, sticky=tk.E, padx=5, pady=5)
        self.result_var = tk.StringVar()
        result_combobox = ttk.Combobox(main_frame, textvariable=self.result_var, width=30)
        result_combobox['values'] = ["", "正常", "异常", "配合欠佳"]
        result_combobox.grid(row=len(tests), column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 添加视频相关控件
        video_frame = ttk.Frame(main_frame)
        video_frame.grid(row=len(tests)+1, column=0, columnspan=2, pady=10)

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
            db_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            video_dir = os.path.join(db_path, "video", datetime.now().strftime("%Y-%m-%d"))
            os.makedirs(video_dir, exist_ok=True)

            video_filename = os.path.basename(file_path)
            new_video_path = os.path.join(video_dir, video_filename)
            shutil.copy2(file_path, new_video_path)

            self.video_path = os.path.relpath(new_video_path, db_path)
            self.video_label.config(text=f"已选择视频: {video_filename}")
            self.open_video_button.config(state=tk.NORMAL)
            self.cancel_video_button.config(state=tk.NORMAL)

    def open_video(self):
        if self.video_path:
            db_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            full_path = os.path.join(db_path, self.video_path)
            if os.path.exists(full_path):
                if os.name == 'nt':  # Windows
                    os.startfile(full_path)
                elif os.name == 'posix':  # macOS and Linux
                    subprocess.call(('open', full_path))
            else:
                messagebox.showerror("错误", "视频文件不存在")

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
            "位置试验(其他)": {
                "坐位-平卧试验": self.sitting_supine_var.get(),
                "坐位-低头试验": self.sitting_head_down_var.get(),
                "坐位-仰头试验": self.sitting_head_up_var.get(),
                "零平面": self.zero_plane_var.get(),
                "检查结果": self.result_var.get(),
                "视频": self.video_path
            }
        }
        return data
        
    def set_data(self, data):
        self.sitting_supine_var.set(data.get("坐位-平卧试验", ""))
        self.sitting_head_down_var.set(data.get("坐位-低头试验", ""))
        self.sitting_head_up_var.set(data.get("坐位-仰头试验", ""))
        self.zero_plane_var.set(data.get("零平面", ""))
        self.result_var.set(data.get("检查结果", ""))
        self.video_path = data.get("视频", "")
        if self.video_path:
            self.video_label.config(text=f"已选择视频: {os.path.basename(self.video_path)}")
            self.open_video_button.config(state=tk.NORMAL)
            self.cancel_video_button.config(state=tk.NORMAL)
        else:
            self.video_label.config(text="未选择视频")
            self.open_video_button.config(state=tk.DISABLED)
            self.cancel_video_button.config(state=tk.DISABLED)
