import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageGrab
import os
from datetime import datetime

class ScreenshotWindow(tk.Toplevel):
    def __init__(self, master, callback):
        super().__init__(master)
        self.callback = callback
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

class HeadImpulseSuppressionTestPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.image_path = ""
        self.screenshot = None
        self.create_widgets()

    def create_widgets(self):
        # 创建一个带滚动条的画布
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

        # 绑定鼠标滚轮事件
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        main_frame = ttk.Frame(self.scrollable_frame, padding="30 30 30 30")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # 左外半规管增益
        ttk.Label(main_frame, text="头脉冲抑制试验增益 (左外半规管):").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.left_gain = ttk.Entry(main_frame)
        self.left_gain.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 右外半规管增益
        ttk.Label(main_frame, text="头脉冲抑制试验增益 (右外半规管):").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.right_gain = ttk.Entry(main_frame)
        self.right_gain.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 补偿性扫视波
        ttk.Label(main_frame, text="头脉冲抑制试验补偿性扫视波:").grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        self.compensatory_saccade = ttk.Combobox(main_frame, 
                                                 values=["", "左外半规管", "右外半规管", "阴性", "配合欠佳"])
        self.compensatory_saccade.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 示意图
        ttk.Label(main_frame, text="头脉冲抑制试验示意图:").grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
        self.image_button = ttk.Button(main_frame, text="选择图片", command=self.select_image)
        self.image_button.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        self.image_label = ttk.Label(main_frame)
        self.image_label.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 检查结果
        ttk.Label(main_frame, text="头脉冲抑制试验检查结果:").grid(row=5, column=0, sticky=tk.E, padx=5, pady=5)
        self.test_result = ttk.Combobox(main_frame, 
                                        values=["", "左外半规管功能低下", "右外半规管功能低下", "双侧外半规管功能低下", "配合欠佳"])
        self.test_result.grid(row=5, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    def select_image(self):
        root = self.winfo_toplevel()  # 获取顶层窗口
        root.withdraw()  # 隐藏顶层窗口
        self.after(100, self.start_screenshot)  # 短暂延迟后开始截图

    def start_screenshot(self):
        root = self.winfo_toplevel()  # 获取顶层窗口
        screenshot_window = ScreenshotWindow(root, self.show_screenshot)
        screenshot_window.focus_force()

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
            filename = f"head_impulse_suppression_test_{timestamp}.png"
            self.image_path = os.path.join(save_dir, filename)
            
            # 保存截图
            self.screenshot.save(self.image_path)

    def get_data(self):
        return {
            "头脉冲抑制试验": {
                "头脉冲抑制试验增益 (左外半规管)": self.left_gain.get(),
                "头脉冲抑制试验增益 (右外半规管)": self.right_gain.get(),
                "头脉冲抑制试验补偿性扫视波": self.compensatory_saccade.get(),
                "头脉冲抑制试验示意图": self.image_path,
                "头脉冲抑制试验检查结果": self.test_result.get()
            }
        }

    def set_data(self, data):
        self.left_gain.delete(0, tk.END)
        self.left_gain.insert(0, data.get("头脉冲抑制试验增益 (左外半规管)", ""))
        
        self.right_gain.delete(0, tk.END)
        self.right_gain.insert(0, data.get("头脉冲抑制试验增益 (右外半规管)", ""))
        
        self.compensatory_saccade.set(data.get("头脉冲抑制试验补偿性扫视波", ""))
        
        if data.get("头脉冲抑制试验示意图"):
            self.image_path = data.get("头脉冲抑制试验示意图")
            self.image_button.config(text="重新截图")
            self.load_image()
        else:
            self.image_path = ""
            self.image_button.config(text="选择图片")
            self.image_label.config(image="")
        
        self.test_result.set(data.get("头脉冲抑制试验检查结果", ""))

    def load_image(self):
        if os.path.exists(self.image_path):
            image = Image.open(self.image_path)
            
            # 调整图片大小以适应界面
            width = 300  # 设置期望的宽度
            ratio = width / image.width
            height = int(image.height * ratio)
            
            resized_image = image.resize((width, height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(resized_image)
            
            self.image_label.config(image=photo)
            self.image_label.image = photo  # 保持对图片的引用

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
