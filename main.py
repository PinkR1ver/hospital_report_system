import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
from datetime import datetime
import subprocess
import platform

# 导入JSON页面渲染器
from pages.json_page_renderer import JSONPageRenderer, load_page_config


class VestibularFunctionReport:
    def __init__(self):
        self.root = tk.Tk()
        self.config_file = "config.json"

        self.load_config()

        # 设置窗口（宽度缩小为配置的一半）
        self.root.title(self.config["system"].get("name", "前庭功能检查报告系统"))
        window_size = self.config["system"].get("window_size", {"width": 1200, "height": 800})
        half_width = max(600, int(window_size.get('width', 1200) * 0.5))
        height = int(window_size.get('height', 800))
        self.root.geometry(f"{half_width}x{height}")

        # 创建数据库文件夹
        self.create_database_folders()

        # 创建界面
        self.create_interface()

    def load_config(self):
        """加载配置文件（明文 JSON）"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            # 最小默认配置
            self.config = {
                "system": {
                    "name": "前庭功能检查报告系统",
                    "version": "2.0.0",
                    "window_size": {"width": 1200, "height": 800}
                },
                "database": {"path": "vest_database", "folders": ["report"]},
                "report_template": {"enabled_pages": ["basic_info"]},
                "pages": {"basic_info": {"name": "基本信息", "enabled": True}}
            }
        except Exception as e:
            messagebox.showerror("错误", f"配置文件读取失败: {e}")
            self.config = {
                "system": {
                    "name": "前庭功能检查报告系统",
                    "version": "2.0.0",
                    "window_size": {"width": 1200, "height": 800}
                },
                "database": {"path": "vest_database", "folders": ["report"]},
                "report_template": {"enabled_pages": ["basic_info"]},
                "pages": {"basic_info": {"name": "基本信息", "enabled": True}}
            }

    def create_database_folders(self):
        """创建数据库文件夹"""
        self.db_path = self.config["database"]["path"]
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path, exist_ok=True)

        # 创建必要的子文件夹
        current_date = datetime.now().strftime("%Y-%m-%d")
        for folder in self.config["database"]["folders"]:
            folder_path = os.path.join(self.db_path, folder, current_date)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path, exist_ok=True)

    def create_interface(self):
        """创建主界面"""
        # 创建主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建侧边栏
        self.sidebar = ttk.Frame(self.main_frame, width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # 创建内容区域
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 创建菜单
        self.create_menu()
        
        # 创建侧边栏按钮
        self.create_sidebar()
        
        # 创建页面
        self.create_pages()

    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="新建", command=self.new_report)
        file_menu.add_command(label="保存", command=self.save_data)
        file_menu.add_command(label="退出", command=self.root.quit)

        # 数据库菜单
        db_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="数据库", menu=db_menu)
        db_menu.add_command(label="更改数据库文件夹", command=self.change_db_folder)
        db_menu.add_command(label="打开数据库文件夹", command=self.open_db_folder)

        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self.show_about)

    def load_page_index(self):
        """加载页面索引"""
        index_path = os.path.join("pages", "index.json")
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
                return index_data.get("pages", [])
        except FileNotFoundError:
            # 如果没有索引文件，从enabled_pages生成
            enabled_pages = self.config["report_template"]["enabled_pages"]
            pages = []
            for i, page_id in enumerate(enabled_pages):
                page_config = load_page_config(page_id)
                if page_config:
                    pages.append({
                        "id": page_id,
                        "name": page_config.get("name", page_id),
                        "enabled": page_config.get("enabled", True),
                        "required": page_config.get("required", False),
                        "order": page_config.get("order", i + 1)
                    })
            return pages

    def create_sidebar(self):
        """创建侧边栏按钮"""
        # 从页面索引读取页面信息
        pages = self.load_page_index()
        
        # 按order排序并过滤启用的页面
        enabled_pages = [p for p in pages if p.get("enabled", True)]
        enabled_pages.sort(key=lambda x: x.get("order", 999))
        
        for page_info in enabled_pages:
            button = ttk.Button(
                self.sidebar,
                text=page_info.get("name", page_info["id"]),
                command=lambda p=page_info["id"]: self.show_page(p)
            )
            button.pack(pady=6, padx=8, fill=tk.X)

    def create_pages(self):
        """创建页面"""
        self.pages = {}
        enabled_pages = self.config["report_template"]["enabled_pages"]
        
        for page_key in enabled_pages:
            # 加载页面配置
            page_config = load_page_config(page_key)
            if page_config:
                self.pages[page_key] = JSONPageRenderer(self.content_frame, self, page_config)
        
        # 隐藏所有页面
        for page in self.pages.values():
            page.pack_forget()

        self.current_page = None
        # 默认显示第一个启用的页面
        if enabled_pages:
            self.show_page(enabled_pages[0])

    def show_page(self, page_name):
        """显示指定页面"""
        if self.current_page:
            self.current_page.pack_forget()
        
        if page_name in self.pages:
            self.pages[page_name].pack(fill=tk.BOTH, expand=True)
            self.current_page = self.pages[page_name]

    def save_data(self):
        """保存数据"""
        # 获取所有页面的数据
        data = {}
        for page_name, page in self.pages.items():
            page_data = page.get_data()
            if page_data:
                data.update(page_data)

        # 检查基本信息是否填写完整
        basic_info = data.get("基本信息", {})
        required_fields = ["ID", "姓名", "性别", "检查时间", "检查医生", "检查设备"]
        missing_fields = [field for field in required_fields if not basic_info.get(field)]

        if missing_fields:
            messagebox.showerror("错误", f"以下基本信息字段未填写完整:\n{', '.join(missing_fields)}\n请填写完整后再保存。")
            return

        # 创建日期文件夹
        current_date = datetime.now().strftime("%Y-%m-%d")
        report_folder = os.path.join(self.db_path, "report", current_date)
        if not os.path.exists(report_folder):
            os.makedirs(report_folder)

        # 生成文件名
        patient_id = basic_info["ID"]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{patient_id}_{timestamp}.json"

        # 完整的文件路径
        file_path = os.path.join(report_folder, filename)

        # 保存数据到文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        messagebox.showinfo("保存成功", f"数据已成功保存到:\n{file_path}")

    def new_report(self):
        """创建新报告，清空所有字段"""
        if messagebox.askyesno("确认", "是否要创建新报告？这将清空所有字段。"):
            # 清空所有页面的输入
            for page in self.pages.values():
                if hasattr(page, 'clear_inputs'):
                    page.clear_inputs()

            # 切换到第一个页面
            enabled_pages = self.config["report_template"]["enabled_pages"]
            if enabled_pages:
                self.show_page(enabled_pages[0])
            messagebox.showinfo("成功", "已创建新报告，请填写基本信息。")

    def change_db_folder(self):
        """更改数据库文件夹位置"""
        new_path = filedialog.askdirectory(title="选择数据库文件夹位置")
        if new_path:
            try:
                self.config['database']['path'] = new_path
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("成功", "数据库路径已更改。")
                self.db_path = new_path
            except Exception as e:
                messagebox.showerror("错误", f"更改数据库路径失败: {str(e)}")

    def open_db_folder(self):
        """打开数据库文件夹"""
        if os.path.exists(self.db_path):
            if platform.system() == "Windows":
                os.startfile(self.db_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.call(["open", self.db_path])
            else:  # Linux和其他类Unix系统
                subprocess.call(["xdg-open", self.db_path])
        else:
            messagebox.showerror("错误", f"数据库文件夹不存在: {self.db_path}")

    def show_about(self):
        """显示关于信息"""
        about_text = f"""
        {self.config["system"].get("name", "前庭功能检查报告系统")}
        版本: {self.config["system"].get("version", "2.0.0")}

        本软件遵循 MIT 许可证
        """
        messagebox.showinfo("关于", about_text)


    def run(self):
        """运行应用程序"""
        self.root.mainloop()

if __name__ == "__main__":
    app = VestibularFunctionReport()
    app.run()
