import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import subprocess

class FistulaTestPage(ttk.Frame):
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

        # 瘘管试验
        fistula_frame = ttk.LabelFrame(main_frame, text="瘘管试验", padding="10 10 10 10")
        fistula_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # 使用字典存储每个选项的变量
        self.fistula_vars = {}
        options = ["右耳阳性", "左耳阳性", "右耳弱阳性", "左耳弱阳性", "双耳阳性", "双耳弱阳性", "阴性", "配合欠佳"]
        
        # 创建两行选项
        for i, option in enumerate(options):
            var = tk.BooleanVar()
            self.fistula_vars[option] = var
            chk = ttk.Checkbutton(fistula_frame, text=option, variable=var)
            chk.grid(row=i//4, column=i%4, sticky=tk.W, padx=5, pady=2)

        # 瘘管试验检查结果
        ttk.Label(main_frame, text="瘘管试验检查结果:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.result_var = tk.StringVar()
        result_combobox = ttk.Combobox(main_frame, textvariable=self.result_var, width=30)
        result_combobox['values'] = ["", "正常", "异常", "配合欠佳"]
        result_combobox.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 视频导入部分
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
                self.video_path = ""
                self.video_label.config(text="未选择视频")
                self.open_video_button.config(state=tk.DISABLED)
                self.cancel_video_button.config(state=tk.DISABLED)

    def get_data(self):
        # 获取选中的瘘管试验选项
        selected_fistula = [option for option, var in self.fistula_vars.items() 
                           if var.get()]
        
        return {
            "瘘管试验": {
                "瘘管试验": selected_fistula,
                "检查结果": self.result_var.get(),
                "视频": self.video_path
            }
        }

    def set_data(self, data):
        # 设置瘘管试验选项
        selected_fistula = data.get("瘘管试验", [])
        for option, var in self.fistula_vars.items():
            var.set(option in selected_fistula)
        
        self.result_var.set(data.get("检查结果", ""))
        
        # 视频相关设置保持不变
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
        for option, var in self.fistula_vars.items():
            var.set(False)
        self.result_var.set("")
        self.video_path = ""
        self.video_label.config(text="未选择视频")
        self.open_video_button.config(state=tk.DISABLED)
        self.cancel_video_button.config(state=tk.DISABLED)
