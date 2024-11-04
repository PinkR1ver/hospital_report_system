import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageGrab
import os
from datetime import datetime

# 添加 ScreenshotWindow 类定义
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

class CaloricTestPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="25 25 25 25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # 创建三个部分
        self.create_unilateral_weakness_section(main_frame)
        self.create_directional_preponderance_section(main_frame)
        self.create_spv_section(main_frame)

        # 固视抑制指数
        self.create_fixation_index_section(main_frame)

        # 检查结果
        self.create_result_section(main_frame)

        # 温度试验示意图
        self.create_image_section(main_frame)

    def create_unilateral_weakness_section(self, parent):
        frame = ttk.LabelFrame(parent, text="单侧减弱 (UW)", padding="10 10 10 10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        ttk.Label(frame, text="侧别:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.uw_side_var = tk.StringVar()
        uw_side_combobox = ttk.Combobox(frame, textvariable=self.uw_side_var, width=20)
        uw_side_combobox['values'] = ["", "右耳", "左耳", "左右对称"]
        uw_side_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(frame, text="数值 (%):").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.uw_value_var = tk.StringVar()
        uw_value_entry = ttk.Entry(frame, textvariable=self.uw_value_var, width=10)
        uw_value_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    def create_directional_preponderance_section(self, parent):
        frame = ttk.LabelFrame(parent, text="优势偏向 (DP)", padding="10 10 10 10")
        frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        ttk.Label(frame, text="侧别:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.dp_side_var = tk.StringVar()
        dp_side_combobox = ttk.Combobox(frame, textvariable=self.dp_side_var, width=20)
        dp_side_combobox['values'] = ["", "右耳", "左耳", "左右对称"]
        dp_side_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(frame, text="数值 (度/秒):").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.dp_value_var = tk.StringVar()
        dp_value_entry = ttk.Entry(frame, textvariable=self.dp_value_var, width=10)
        dp_value_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    def create_spv_section(self, parent):
        frame = ttk.LabelFrame(parent, text="最大慢相速度总和", padding="10 10 10 10")
        frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        ttk.Label(frame, text="右耳 (度/秒):").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.right_ear_spv_var = tk.StringVar()
        right_ear_spv_entry = ttk.Entry(frame, textvariable=self.right_ear_spv_var, width=10)
        right_ear_spv_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(frame, text="左耳 (度/秒):").grid(row=0, column=2, sticky=tk.E, padx=5, pady=5)
        self.left_ear_spv_var = tk.StringVar()
        left_ear_spv_entry = ttk.Entry(frame, textvariable=self.left_ear_spv_var, width=10)
        left_ear_spv_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=5, pady=5)

    def create_fixation_index_section(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(frame, text="固视抑制指数 (FI, %):").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.fi_var = tk.StringVar()
        fi_entry = ttk.Entry(frame, textvariable=self.fi_var, width=10)
        fi_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    def create_result_section(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(frame, text="温度试验检查结果:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.result_var = tk.StringVar()
        result_combobox = ttk.Combobox(frame, textvariable=self.result_var, width=40)
        result_combobox['values'] = [
            "", "左外半规管功能减退", "右外半规管功能减退",
            "双外半规管功能减退", "双外半规管功能正常",
            "配合欠佳"
        ]
        result_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

    def create_image_section(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Label(frame, text="温度试验示意图:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        
        self.image_path = ""
        self.screenshot = None
        self.screenshot_window = None
        
        self.image_button = ttk.Button(frame, text="截取图片", command=self.select_image)
        self.image_button.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        self.cancel_button = ttk.Button(frame, text="取消截图", command=self.cancel_screenshot, state=tk.DISABLED)
        self.cancel_button.grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        
        self.image_label = ttk.Label(frame)
        self.image_label.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=5, pady=5)

    def get_data(self):
        return {
            "温度试验": {
                "单侧减弱侧别 (UW)": self.uw_side_var.get(),
                "单侧减弱数值 (UW, %)": self.uw_value_var.get(),
                "优势偏向侧别 (DP)": self.dp_side_var.get(),
                "优势偏向数值 (DP, 度/秒)": self.dp_value_var.get(),
                "最大慢相速度总和（右耳, 度/秒）": self.right_ear_spv_var.get(),
                "最大慢相速度总和（左耳, 度/秒）": self.left_ear_spv_var.get(),
                "固视抑制指数 (FI, %)": self.fi_var.get(),
                "温度试验示意图": self.image_path,
                "检查结果": self.result_var.get()
            }
        }
        
        
    def set_data(self, data):
        self.uw_side_var.set(data.get("单侧减弱侧别 (UW)", ""))
        self.uw_value_var.set(data.get("单侧减弱数值 (UW, %)", ""))
        self.dp_side_var.set(data.get("优势偏向侧别 (DP)", ""))
        self.dp_value_var.set(data.get("优势偏向数值 (DP, 度/秒)", ""))
        self.right_ear_spv_var.set(data.get("最大慢相速度总和（右耳, 度/秒）", ""))
        self.left_ear_spv_var.set(data.get("最大慢相速度总和（左耳, 度/秒）", ""))
        self.fi_var.set(data.get("固视抑制指数 (FI, %)", ""))
        self.image_path = data.get("温度试验示意图", "")
        self.image_label.config(text=self.image_path.split("/")[-1] if self.image_path else "未选择图片")
        self.result_var.set(data.get("检查结果", ""))

        # 设置图片路径
        if self.image_path:
            self.image_button.config(text="重新截图")
            # 如果需要显示图片，使用完整路径加载
            full_path = os.path.join(os.path.dirname(__file__), self.image_path)
            if os.path.exists(full_path):
                image = Image.open(full_path)
                # 调整图片大小
                width = 300
                ratio = width / image.width
                height = int(image.height * ratio)
                resized_image = image.resize((width, height), Image.LANCZOS)
                photo = ImageTk.PhotoImage(resized_image)
                self.image_label.config(image=photo)
                self.image_label.image = photo
        else:
            self.image_button.config(text="截取图片")
            self.image_label.config(image="")

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

    def save_screenshot(self):
        if self.screenshot:
            # 创建保存截图的目录
            save_dir = os.path.join(os.path.dirname(__file__), "screenshots")
            os.makedirs(save_dir, exist_ok=True)
            
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"caloric_test_{timestamp}.png"
            
            # 保存为相对路径
            self.image_path = os.path.join("screenshots", filename)  # 修改这里，只保存相对路径
            
            # 使用完整路径保存文件
            full_path = os.path.join(os.path.dirname(__file__), self.image_path)
            self.screenshot.save(full_path)

    def cancel_screenshot(self):
        if hasattr(self, 'screenshot_window') and self.screenshot_window:
            self.screenshot_window.destroy()
        
        # 清除已截取的图片
        self.screenshot = None
        self.image_path = ""
        self.image_label.config(image="")
        self.image_button.config(text="截取图片")
        
        root = self.winfo_toplevel()
        root.deiconify()
        self.cancel_button.config(state=tk.DISABLED)  # 禁用取消按钮
