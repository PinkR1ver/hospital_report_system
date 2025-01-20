import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageGrab
import os
from datetime import datetime

class ScreenshotWindow(tk.Toplevel):
    def __init__(self, master, callback, cancel_callback):
        super().__init__(master)
        self.callback = callback
        self.cancel_callback = cancel_callback
        self.attributes('-fullscreen', True)
        self.attributes('-alpha', 0.3)
        self.configure(bg='grey')
        self.canvas = tk.Canvas(self, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Escape>", self.on_cancel)

    def on_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_release(self, event):
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)
        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.callback(screenshot)
        self.destroy()

    def on_cancel(self, event):
        self.cancel_callback()
        self.destroy()

class HeadImpulseTestPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.image_path = ""
        self.screenshot = None
        self.screenshot_window = None
        self.create_widgets()

    def create_widgets(self):
        # 创建一个带滚动条的画布，但只用于这个页面
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # 绑定鼠标滚轮事件到画布
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        main_frame = ttk.Frame(self.scrollable_frame, padding="25 25 25 25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        canals = [
            ("左外半规管", "vor_left_lateral", "pr_left_lateral"),
            ("右外半规管", "vor_right_lateral", "pr_right_lateral"),
            ("左前半规管", "vor_left_anterior", "pr_left_anterior"),
            ("右后半规管", "vor_right_posterior", "pr_right_posterior"),
            ("左后半规管", "vor_left_posterior", "pr_left_posterior"),
            ("右前半规管", "vor_right_anterior", "pr_right_anterior")
        ]

        for i, (canal_name, vor_attr, pr_attr) in enumerate(canals):
            canal_frame = ttk.LabelFrame(main_frame, text=canal_name, padding="15 15 15 15")
            canal_frame.grid(row=i//2, column=i%2, sticky=(tk.W, tk.E), padx=10, pady=10)
            canal_frame.columnconfigure(1, weight=1)

            # VOR增益
            ttk.Label(canal_frame, text="VOR增益:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
            setattr(self, vor_attr, ttk.Entry(canal_frame))
            getattr(self, vor_attr).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

            # PR分数
            ttk.Label(canal_frame, text="PR分数 (%):").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
            setattr(self, pr_attr, ttk.Entry(canal_frame))
            getattr(self, pr_attr).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
            getattr(self, pr_attr).insert(0, "NA")  # 添加这行代码设置默认值

        # 头脉冲试验补偿性扫视波
        compensatory_saccade_frame = ttk.LabelFrame(main_frame, text="头脉冲试验扫视波", padding="10 10 10 10")
        compensatory_saccade_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        compensatory_saccade_frame.columnconfigure(0, weight=1)

        # 使用字典存储每个选项的变量
        self.hit_compensatory_saccade_vars = {}
        options = ["阴性", "左外半规管", "右外半规管", "左前半规管", "右前半规管",
                  "左后半规管", "右后半规管", "配合欠佳"]

        # 创建两行选项
        for i, option in enumerate(options):
            var = tk.BooleanVar()
            self.hit_compensatory_saccade_vars[option] = var
            chk = ttk.Checkbutton(compensatory_saccade_frame, text=option, variable=var)
            chk.grid(row=i//4, column=i%4, sticky=tk.W, padx=3, pady=2)

        # 头脉冲试验示意图
        image_frame = ttk.LabelFrame(main_frame, text="头脉冲试验示意图", padding="10 10 10 10")
        image_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        image_frame.columnconfigure(0, weight=1)
        image_frame.columnconfigure(1, weight=1)

        self.image_button = ttk.Button(image_frame, text="截取图片", command=self.select_image)
        self.image_button.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)

        self.cancel_button = ttk.Button(image_frame, text="取消截图", command=self.cancel_screenshot, state=tk.DISABLED)
        self.cancel_button.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        self.image_label = ttk.Label(image_frame)
        self.image_label.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 头脉冲试验检查结果
        result_frame = ttk.LabelFrame(main_frame, text="头脉冲试验检查结果", padding="10 10 10 10")
        result_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        result_frame.columnconfigure(0, weight=1)

        # 使用字典存储检查结果的选项变量
        self.hit_result_vars = {}
        result_options = [
            "左外半规管功能低下",
            "右外半规管功能低下",
            "左前半规管功能低下",
            "右前半规管功能低下",
            "左后半规管功能低下",
            "右后半规管功能低下",
            "左外半规管增益降低",
            "右外半规管增益降低",
            "左前半规管增益降低",
            "右前半规管增益降低",
            "左后半规管增益降低",
            "右后半规管增益降低",
            "扫视波扫视阳性",
            "半规管功能正常",
            "配合欠佳"
        ]

        # 由于选项增多，调整为每行3个选项
        for i, option in enumerate(result_options):
            var = tk.BooleanVar()
            self.hit_result_vars[option] = var
            chk = ttk.Checkbutton(result_frame, text=option, variable=var)
            chk.grid(row=i//3, column=i%3, sticky=tk.W, padx=5, pady=2)

    def select_image(self):
        root = self.winfo_toplevel()  # 获取顶层窗口
        root.withdraw()  # 隐藏顶层窗口
        self.cancel_button.config(state=tk.NORMAL)  # 启用取消按钮
        self.after(100, self.start_screenshot)  # 短暂延迟后开始截图

    def start_screenshot(self):
        root = self.winfo_toplevel()  # 获取顶层窗口
        self.screenshot_window = ScreenshotWindow(root, self.show_screenshot, self.cancel_screenshot)
        self.screenshot_window.focus_force()

    def show_screenshot(self, screenshot):
        self.screenshot = screenshot
        root = self.winfo_toplevel()  # 获取顶层窗口
        root.deiconify()  # 显示顶层窗口

        # 调整图片大小以适应界面
        width = 300  # 设置期望的宽度
        ratio = width / screenshot.width
        height = int(screenshot.height * ratio)

        resized_image = screenshot.resize((width, height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)

        self.image_label.config(image=photo)
        self.image_label.image = photo  # 保持对图片的引用

        self.image_button.config(text="重新截图")
        self.cancel_button.config(state=tk.NORMAL)  # 保持取消按钮为启用状态

        # 保存图片
        self.save_screenshot()

        # 更新滚动区域
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def save_screenshot(self):
        if self.screenshot:
            # 创建保存截图的目录
            save_dir = os.path.join(os.path.dirname(__file__), "screenshots")
            os.makedirs(save_dir, exist_ok=True)

            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"head_impulse_test_{timestamp}.png"
            self.image_path = os.path.join(save_dir, filename)

            # 保存截图
            self.screenshot.save(self.image_path)

    def get_data(self):
        # 获取选中的扫视波选项
        selected_saccades = [option for option, var in self.hit_compensatory_saccade_vars.items()
                           if var.get()]

        # 获取选中的检查结果选项
        selected_results = [option for option, var in self.hit_result_vars.items()
                          if var.get()]

        return {
            "头脉冲试验": {
                "VOR增益 (左外半规管)": self.vor_left_lateral.get(),
                "PR分数 (左外半规管)": self.pr_left_lateral.get(),
                "VOR增益 (右外半规管)": self.vor_right_lateral.get(),
                "PR分数 (右外半规管)": self.pr_right_lateral.get(),
                "VOR增益 (左前半规管)": self.vor_left_anterior.get(),
                "PR分数 (左前半规管)": self.pr_left_anterior.get(),
                "VOR增益 (右后半规管)": self.vor_right_posterior.get(),
                "PR分数 (右后半规管)": self.pr_right_posterior.get(),
                "VOR增益 (左后半规管)": self.vor_left_posterior.get(),
                "PR分数 (左后半规管)": self.pr_left_posterior.get(),
                "VOR增益 (右前半规管)": self.vor_right_anterior.get(),
                "PR分数 (右前半规管)": self.pr_right_anterior.get(),
                "头脉冲试验扫视波": selected_saccades,
                "头脉冲试验示意图": self.image_path,
                "头脉冲试验检查结果": selected_results
            }
        }

    def set_data(self, data):
        canals = [
            ("左外半规管", "vor_left_lateral", "pr_left_lateral"),
            ("右外半规管", "vor_right_lateral", "pr_right_lateral"),
            ("左前半规管", "vor_left_anterior", "pr_left_anterior"),
            ("右后半规管", "vor_right_posterior", "pr_right_posterior"),
            ("左后半规管", "vor_left_posterior", "pr_left_posterior"),
            ("右前半规管", "vor_right_anterior", "pr_right_anterior")
        ]

        for canal_name, vor_attr, pr_attr in canals:
            getattr(self, vor_attr).delete(0, tk.END)
            getattr(self, vor_attr).insert(0, data.get(f"VOR增益 ({canal_name})", ""))
            getattr(self, pr_attr).delete(0, tk.END)
            getattr(self, pr_attr).insert(0, data.get(f"PR分数 ({canal_name})", ""))

        # 设置扫视波选项
        selected_saccades = data.get("头脉冲试验扫视波", [])
        for option, var in self.hit_compensatory_saccade_vars.items():
            var.set(option in selected_saccades)

        if data.get("头脉冲试验示意图"):
            self.image_path = data.get("头脉冲试验示意图")
            self.image_button.config(text="图片已选择")
        else:
            self.image_path = ""
            self.image_button.config(text="选择图片")

        # 设置检查结果选项
        selected_results = data.get("头脉冲试验检查结果", [])
        for option, var in self.hit_result_vars.items():
            var.set(option in selected_results)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def cancel_screenshot(self):
        if self.screenshot_window:
            self.screenshot_window.destroy()

        # 清除已截取的图片
        self.screenshot = None
        self.image_path = ""
        self.image_label.config(image="")
        self.image_button.config(text="截取图片")

        root = self.winfo_toplevel()
        root.deiconify()
        self.cancel_button.config(state=tk.DISABLED)  # 禁用取消按钮


    def clear_inputs(self):
        canals = [
            ("左外半规管", "vor_left_lateral", "pr_left_lateral"),
            ("右外半规管", "vor_right_lateral", "pr_right_lateral"),
            ("左前半规管", "vor_left_anterior", "pr_left_anterior"),
            ("右后半规管", "vor_right_posterior", "pr_right_posterior"),
            ("左后半规管", "vor_left_posterior", "pr_left_posterior"),
            ("右前半规管", "vor_right_anterior", "pr_right_anterior")
        ]

        for canal_name, vor_attr, pr_attr in canals:
            getattr(self, vor_attr).delete(0, tk.END)
            getattr(self, vor_attr).insert(0, "")
            getattr(self, pr_attr).delete(0, tk.END)
            getattr(self, pr_attr).insert(0, "")

        for option, var in self.hit_compensatory_saccade_vars.items():
            var.set(False)
        for option, var in self.hit_result_vars.items():
            var.set(False)

        self.image_path = ""
        self.image_label.config(image="")

