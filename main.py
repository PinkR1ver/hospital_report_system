import customtkinter as ctk
from tkinter import filedialog, messagebox
import json
import os
from datetime import datetime
import subprocess
import platform

# 导入JSON页面渲染器
from pages.json_page_renderer import JSONPageRenderer, load_page_config
# 导入数据管理器
from data import DataManager

# 设置CustomTkinter主题 - 使用深色模式，更现代美观
ctk.set_appearance_mode("dark")  # 使用深色模式，更高级
ctk.set_default_color_theme("blue")  # 蓝色主题

# 设置清晰的字体
import platform
if platform.system() == "Windows":
    DEFAULT_FONT = ("Microsoft YaHei UI", 11)  # 微软雅黑UI，更清晰
    DEFAULT_FONT_BOLD = ("Microsoft YaHei UI", 11, "bold")
    DEFAULT_FONT_LARGE = ("Microsoft YaHei UI", 14, "bold")
elif platform.system() == "Darwin":  # macOS
    DEFAULT_FONT = ("PingFang SC", 11)
    DEFAULT_FONT_BOLD = ("PingFang SC", 11, "bold")
    DEFAULT_FONT_LARGE = ("PingFang SC", 14, "bold")
else:  # Linux
    DEFAULT_FONT = ("Noto Sans CJK SC", 11)
    DEFAULT_FONT_BOLD = ("Noto Sans CJK SC", 11, "bold")
    DEFAULT_FONT_LARGE = ("Noto Sans CJK SC", 14, "bold")


class VestibularFunctionReport:
    def __init__(self):
        self.root = ctk.CTk()
        self.config_file = "config.json"

        self.load_config()

        # 设置窗口大小（使用更大的窗口）
        window_size = self.config["system"].get("window_size", {"width": 1200, "height": 800})
        width = int(window_size.get('width', 1200) * 0.8)  # 使用80%宽度，更大
        height = int(window_size.get('height', 800))
        self.root.geometry(f"{width}x{height}")
        self.root.title(self.config["system"].get("name", "前庭功能检查报告系统"))

        # 初始化数据管理器
        self.db_path = self.config["database"]["path"]
        self.data_manager = DataManager(self.db_path, self.config)

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
            # 最小默认配置 - 页面信息从pages/目录读取，这里只保留系统配置
            self.config = {
                "system": {
                    "name": "前庭功能检查报告系统",
                    "version": "2.0.0",
                    "window_size": {"width": 1200, "height": 800}
                },
                "database": {"path": "vest_database", "folders": ["report"]},
                "report_template": {"enabled_pages": ["basic_info"]}
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
                "report_template": {"enabled_pages": ["basic_info"]}
            }

    def create_database_folders(self):
        """创建数据库文件夹"""
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path, exist_ok=True)

        # 创建必要的子文件夹
        current_date = datetime.now().strftime("%Y-%m-%d")
        for folder in self.config["database"]["folders"]:
            # templates和excel文件夹不需要日期子文件夹
            if folder in ["templates", "excel"]:
                folder_path = os.path.join(self.db_path, folder)
            else:
                folder_path = os.path.join(self.db_path, folder, current_date)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path, exist_ok=True)

    def create_interface(self):
        """创建主界面"""
        # 创建主框架
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 创建侧边栏 - 美化样式，添加透明度效果
        self.sidebar = ctk.CTkFrame(
            self.main_frame, 
            width=220, 
            corner_radius=15,
            fg_color=("gray85", "gray18"),  # 更浅的背景，增加高级感
            border_width=0
        )
        self.sidebar.pack(side="left", fill="y", padx=(0, 10))
        self.sidebar.pack_propagate(False)

        # 创建内容区域 - 美化样式，添加透明度效果
        self.content_frame = ctk.CTkFrame(
            self.main_frame, 
            corner_radius=15,
            fg_color=("gray92", "gray14"),  # 更浅的背景，增加高级感
            border_width=0
        )
        self.content_frame.pack(side="right", fill="both", expand=True)

        # 创建菜单
        self.create_menu()
        
        # 创建侧边栏按钮
        self.create_sidebar()
        
        # 创建页面
        self.create_pages()

    def create_menu(self):
        """创建菜单栏 - CustomTkinter使用顶部按钮栏替代传统菜单"""
        # 创建顶部菜单栏 - 美化样式，添加透明度效果
        menu_frame = ctk.CTkFrame(
            self.root, 
            height=45, 
            corner_radius=0,
            fg_color=("gray88", "gray22"),  # 与主内容区区分，增加层次感
            border_width=0
        )
        menu_frame.pack(fill="x", padx=0, pady=0)
        menu_frame.pack_propagate(False)
        
        # 文件菜单按钮 - 使用清晰字体和更高级的样式
        file_btn = ctk.CTkButton(
            menu_frame, 
            text="新建", 
            command=self.new_report, 
            width=75, 
            height=32,
            corner_radius=8,
            font=ctk.CTkFont(family=DEFAULT_FONT[0], size=DEFAULT_FONT[1]),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
            border_width=0
        )
        file_btn.pack(side="left", padx=6, pady=6)
        
        save_btn = ctk.CTkButton(
            menu_frame, 
            text="保存", 
            command=self.save_data, 
            width=75, 
            height=32,
            corner_radius=8,
            font=ctk.CTkFont(family=DEFAULT_FONT[0], size=DEFAULT_FONT[1]),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
            border_width=0
        )
        save_btn.pack(side="left", padx=3, pady=6)
        
        # 分隔 - 使用透明度效果
        separator = ctk.CTkFrame(menu_frame, width=1, fg_color=("gray65", "gray35"))
        separator.pack(side="left", fill="y", padx=8, pady=8)
        
        # 数据库菜单按钮
        db_change_btn = ctk.CTkButton(
            menu_frame, 
            text="更改数据库", 
            command=self.change_db_folder, 
            width=95, 
            height=32,
            corner_radius=8,
            font=ctk.CTkFont(family=DEFAULT_FONT[0], size=DEFAULT_FONT[1]),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
            border_width=0
        )
        db_change_btn.pack(side="left", padx=3, pady=6)
        
        db_open_btn = ctk.CTkButton(
            menu_frame, 
            text="打开数据库", 
            command=self.open_db_folder, 
            width=95, 
            height=32,
            corner_radius=8,
            font=ctk.CTkFont(family=DEFAULT_FONT[0], size=DEFAULT_FONT[1]),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
            border_width=0
        )
        db_open_btn.pack(side="left", padx=3, pady=6)
        
        # 分隔
        separator2 = ctk.CTkFrame(menu_frame, width=1, fg_color=("gray65", "gray35"))
        separator2.pack(side="left", fill="y", padx=8, pady=8)
        
        # 帮助菜单按钮
        about_btn = ctk.CTkButton(
            menu_frame, 
            text="关于", 
            command=self.show_about, 
            width=75, 
            height=32,
            corner_radius=8,
            font=ctk.CTkFont(family=DEFAULT_FONT[0], size=DEFAULT_FONT[1]),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
            border_width=0
        )
        about_btn.pack(side="right", padx=6, pady=6)

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
        # 侧边栏标题 - 使用清晰字体
        title_label = ctk.CTkLabel(
            self.sidebar, 
            text="页面导航", 
            font=ctk.CTkFont(family=DEFAULT_FONT_LARGE[0], size=13, weight="bold"),
            text_color=("gray30", "gray85")
        )
        title_label.pack(pady=(12, 8))
        
        # 创建可滚动的按钮容器
        scrollable_frame = ctk.CTkScrollableFrame(
            self.sidebar,
            fg_color="transparent",
            corner_radius=0
        )
        scrollable_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # 从页面索引读取页面信息
        pages = self.load_page_index()
        
        # 按order排序并过滤启用的页面
        enabled_pages = [p for p in pages if p.get("enabled", True)]
        enabled_pages.sort(key=lambda x: x.get("order", 999))
        
        self.sidebar_buttons = {}
        for page_info in enabled_pages:
            button = ctk.CTkButton(
                scrollable_frame,
                text=page_info.get("name", page_info["id"]),
                command=lambda p=page_info["id"]: self.show_page(p),
                width=190,
                height=32,
                corner_radius=10,
                font=ctk.CTkFont(family=DEFAULT_FONT[0], size=DEFAULT_FONT[1]),
                fg_color=("gray72", "gray28"),
                hover_color=("gray65", "gray35"),
                border_width=0,
                text_color=("gray20", "gray90")
            )
            button.pack(pady=3, padx=10)
            self.sidebar_buttons[page_info["id"]] = button

    def create_pages(self):
        """创建页面"""
        self.pages = {}
        # Use load_page_index to get all pages, then filter by enabled_pages from config
        all_pages_info = self.load_page_index()
        enabled_page_ids_from_config = set(self.config["report_template"]["enabled_pages"])

        for page_info in all_pages_info:
            if page_info["id"] in enabled_page_ids_from_config:
                page_config = load_page_config(page_info["id"])
                if page_config:
                    # 特殊处理：数据库管理页面使用专门的类
                    if page_info["id"] == "database_management":
                        from pages.database_management import DatabaseManagementPage
                        self.pages[page_info["id"]] = DatabaseManagementPage(self.content_frame, self)
                    else:
                        self.pages[page_info["id"]] = JSONPageRenderer(self.content_frame, self, page_config)
        
        # 隐藏所有页面
        for page in self.pages.values():
            page.pack_forget()

        self.current_page = None
        # Default to show the first enabled page from the sorted list
        if enabled_page_ids_from_config:
            first_enabled_page_id = next((p["id"] for p in all_pages_info if p["id"] in enabled_page_ids_from_config and p.get("enabled", True)), None)
            if first_enabled_page_id:
                self.show_page(first_enabled_page_id)

    def show_page(self, page_name):
        """显示指定页面"""
        if self.current_page:
            self.current_page.pack_forget()
        
        # 更新按钮状态 - 美化选中效果，增加高级感
        for btn_id, btn in self.sidebar_buttons.items():
            if btn_id == page_name:
                btn.configure(
                    fg_color=("gray60", "gray40"), 
                    hover_color=("gray55", "gray45"),
                    text_color=("white", "white")
                )
            else:
                btn.configure(
                    fg_color=("gray72", "gray28"), 
                    hover_color=("gray65", "gray35"),
                    text_color=("gray20", "gray90")
                )
        
        if page_name in self.pages:
            # 进入“检查所见”页面时，若为空则自动生成旧版汇总文本
            if page_name == "exam_findings":
                try:
                    page_obj = self.pages.get("exam_findings")
                    if hasattr(page_obj, "get_data") and hasattr(page_obj, "set_data"):
                        current = page_obj.get_data() or {}
                        root_key = "检查所见"
                        current_text = ""
                        if isinstance(current, dict):
                            section = current.get(root_key, {})
                            if isinstance(section, dict):
                                current_text = section.get("检查所见", "")
                        if not current_text:
                            # 收集现有页面数据并生成汇总
                            all_data = self.data_manager.collect_page_data(self.pages)
                            auto_text = self.data_manager.generate_exam_findings_text(all_data)
                            if auto_text:
                                page_obj.set_data({root_key: {"检查所见": auto_text}})
                except Exception:
                    pass
            self.pages[page_name].pack(fill="both", expand=True)
            self.current_page = self.pages[page_name]

    def _get_required_fields_from_page(self, page_id):
        """从页面配置中获取必需字段"""
        page_config = load_page_config(page_id)
        if not page_config:
            return []
        
        required_fields = []
        for section in page_config.get("sections", []):
            for field in section.get("fields", []):
                if field.get("required", False):
                    required_fields.append(field["key"])
        return required_fields

    def _get_basic_info_page_id(self):
        """从pages/index.json中获取基本信息页面ID（required=true或order=1的页面）"""
        return self.data_manager.get_basic_info_page_id(load_page_config)
    
    def _get_page_config(self, page_id):
        """获取页面配置（供其他模块使用）"""
        return load_page_config(page_id)
    
    def _get_patient_id_key(self):
        """从基本信息页面配置中获取患者ID字段的key"""
        return self.data_manager.get_patient_id_key(load_page_config)

    def save_data(self):
        """保存数据"""
        # 使用DataManager保存数据
        success, result = self.data_manager.save_report(None, self.pages, load_page_config)
        
        if success:
            messagebox.showinfo("保存成功", f"数据已成功保存到:\n{result}")
        else:
            messagebox.showerror("错误", result)

    def new_report(self):
        """创建新报告，清空所有字段"""
        if messagebox.askyesno("确认", "是否要创建新报告？这将清空所有字段。"):
            # 清空所有页面的输入
            for page in self.pages.values():
                if hasattr(page, 'clear_inputs'):
                    page.clear_inputs()

            # 切换到基本信息页面（从配置中动态获取）
            basic_info_page_id = self._get_basic_info_page_id()
            if basic_info_page_id:
                self.show_page(basic_info_page_id)
            else:
                # 如果找不到基本信息页面，显示第一个启用的页面
                all_pages_info = self.load_page_index()
                enabled_pages = [p for p in all_pages_info if p.get("enabled", True)]
                if enabled_pages:
                    enabled_pages.sort(key=lambda x: x.get("order", 999))
                    self.show_page(enabled_pages[0]["id"])
            
            # 获取基本信息页面名称用于提示
            basic_info_page_config = load_page_config(basic_info_page_id)
            basic_info_name = basic_info_page_config.get("name", "基本信息") if basic_info_page_config else "基本信息"
            messagebox.showinfo("成功", f"已创建新报告，请填写{basic_info_name}。")

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
