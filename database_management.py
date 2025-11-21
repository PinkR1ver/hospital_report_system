import customtkinter as ctk
from tkinter import messagebox, filedialog
import json
import os
from datetime import datetime
import platform
import subprocess


class DatabaseManagementPage(ctk.CTkScrollableFrame):
    """数据库管理页面 - 实现报告的增删查改功能"""
    
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.db_path = controller.db_path
        self.selected_file_path = None
        self.reports_data = []  # 存储报告列表数据
        
        # 设置清晰的字体
        import platform as plat
        if plat.system() == "Windows":
            DEFAULT_FONT = ("Microsoft YaHei UI", 11)
            DEFAULT_FONT_BOLD = ("Microsoft YaHei UI", 11, "bold")
        elif plat.system() == "Darwin":
            DEFAULT_FONT = ("PingFang SC", 11)
            DEFAULT_FONT_BOLD = ("PingFang SC", 11, "bold")
        else:
            DEFAULT_FONT = ("Noto Sans CJK SC", 11)
            DEFAULT_FONT_BOLD = ("Noto Sans CJK SC", 11, "bold")
        
        self.DEFAULT_FONT = DEFAULT_FONT
        self.DEFAULT_FONT_BOLD = DEFAULT_FONT_BOLD
        
        self._build_ui()
        self.load_reports()
    
    def _build_ui(self):
        """构建UI界面"""
        # 页面标题
        title_label = ctk.CTkLabel(
            self,
            text="数据库管理",
            font=ctk.CTkFont(family=self.DEFAULT_FONT_BOLD[0], size=16, weight="bold"),
            text_color=("gray20", "gray90")
        )
        title_label.pack(pady=(15, 10))
        
        # 搜索区域
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=5)
        
        search_label = ctk.CTkLabel(
            search_frame,
            text="搜索:",
            font=ctk.CTkFont(family=self.DEFAULT_FONT[0], size=self.DEFAULT_FONT[1])
        )
        search_label.pack(side="left", padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=300,
            height=32,
            font=ctk.CTkFont(family=self.DEFAULT_FONT[0], size=self.DEFAULT_FONT[1]),
            corner_radius=8,
            placeholder_text="输入患者ID、姓名或检查时间搜索..."
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.search_reports())
        
        search_btn = ctk.CTkButton(
            search_frame,
            text="搜索",
            command=self.search_reports,
            width=80,
            height=32,
            corner_radius=8,
            font=ctk.CTkFont(family=self.DEFAULT_FONT[0], size=self.DEFAULT_FONT[1]),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40")
        )
        search_btn.pack(side="left", padx=(0, 10))
        
        clear_search_btn = ctk.CTkButton(
            search_frame,
            text="清空",
            command=self.clear_search,
            width=80,
            height=32,
            corner_radius=8,
            font=ctk.CTkFont(family=self.DEFAULT_FONT[0], size=self.DEFAULT_FONT[1]),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40")
        )
        clear_search_btn.pack(side="left")
        
        # 报告列表区域
        list_frame = ctk.CTkFrame(self, corner_radius=12, fg_color=("gray96", "gray19"))
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # 列表标题
        header_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(10, 5))
        
        headers = ["患者ID", "姓名", "检查时间", "文件路径"]
        widths = [120, 150, 150, 400]
        for i, (header, width) in enumerate(zip(headers, widths)):
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(family=self.DEFAULT_FONT_BOLD[0], size=12, weight="bold"),
                width=width,
                anchor="w"
            )
            label.grid(row=0, column=i, padx=5, sticky="w")
        
        # 创建滚动框架用于显示报告列表
        self.reports_list_frame = ctk.CTkScrollableFrame(
            list_frame,
            fg_color="transparent",
            corner_radius=0
        )
        self.reports_list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # 初始化单选按钮变量
        self.radio_var = ctk.StringVar(value="")
        
        # 按钮区域
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=10)
        
        # 操作按钮
        view_btn = ctk.CTkButton(
            button_frame,
            text="查看详情",
            command=self.view_report,
            width=100,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(family=self.DEFAULT_FONT[0], size=self.DEFAULT_FONT[1]),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40")
        )
        view_btn.pack(side="left", padx=5)
        
        edit_btn = ctk.CTkButton(
            button_frame,
            text="编辑报告",
            command=self.edit_report,
            width=100,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(family=self.DEFAULT_FONT[0], size=self.DEFAULT_FONT[1]),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40")
        )
        edit_btn.pack(side="left", padx=5)
        
        delete_btn = ctk.CTkButton(
            button_frame,
            text="删除报告",
            command=self.delete_report,
            width=100,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(family=self.DEFAULT_FONT[0], size=self.DEFAULT_FONT[1]),
            fg_color=("red", "darkred"),
            hover_color=("darkred", "red")
        )
        delete_btn.pack(side="left", padx=5)
        
        refresh_btn = ctk.CTkButton(
            button_frame,
            text="刷新列表",
            command=self.load_reports,
            width=100,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(family=self.DEFAULT_FONT[0], size=self.DEFAULT_FONT[1]),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40")
        )
        refresh_btn.pack(side="left", padx=5)
        
        # 生成报告按钮
        self.generate_report_btn = ctk.CTkButton(
            button_frame,
            text="生成报告 ▼",
            command=self.toggle_template_menu,
            width=110,
            height=35,
            corner_radius=8,
            font=ctk.CTkFont(family=self.DEFAULT_FONT[0], size=self.DEFAULT_FONT[1]),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40")
        )
        self.generate_report_btn.pack(side="left", padx=5)
        
        # 模板菜单（初始隐藏）
        self.template_menu_frame = None
        self.menu_visible = False
        
        # 统计信息
        self.stats_label = ctk.CTkLabel(
            button_frame,
            text="共 0 条记录",
            font=ctk.CTkFont(family=self.DEFAULT_FONT[0], size=self.DEFAULT_FONT[1]),
            text_color=("gray40", "gray60")
        )
        self.stats_label.pack(side="right", padx=10)
    
    def load_reports(self):
        """加载所有报告"""
        self.reports_data = []
        self._all_reports_data = []  # 保存所有原始数据用于搜索
        report_folder = os.path.join(self.db_path, "report")
        
        if not os.path.exists(report_folder):
            self._update_display()
            return
        
        # 使用DataManager加载报告
        from json_page_renderer import load_page_config
        basic_info_page_id = self.controller._get_basic_info_page_id()
        basic_info_page_config = load_page_config(basic_info_page_id)
        
        basic_info_key = "基本信息"  # 默认
        if basic_info_page_config:
            basic_info_key = basic_info_page_config.get("title") or basic_info_page_config.get("name") or "基本信息"
        
        # 使用DataManager获取报告列表
        all_reports = self.controller.data_manager.list_reports(basic_info_key)
        
        for report in all_reports:
            self.reports_data.append(report)
            self._all_reports_data.append(report)
        
        self._update_display()
    
    def _update_display(self):
        """更新显示"""
        # 清空现有显示
        for widget in self.reports_list_frame.winfo_children():
            widget.destroy()
        
        # 显示报告列表
        for i, report in enumerate(self.reports_data):
            row_frame = ctk.CTkFrame(
                self.reports_list_frame,
                fg_color=("gray98", "gray16") if i % 2 == 0 else ("gray95", "gray19"),
                corner_radius=8,
                height=40
            )
            row_frame.pack(fill="x", padx=5, pady=2)
            row_frame.pack_propagate(False)
            
            # 创建单选按钮用于选择
            radio = ctk.CTkRadioButton(
                row_frame,
                text="",
                variable=self.radio_var,
                value=report['file_path'],
                command=lambda p=report['file_path']: self._select_report(p),
                width=20
            )
            radio.pack(side="left", padx=10)
            
            # 绑定点击行选择
            row_frame.bind("<Button-1>", lambda e, p=report['file_path']: self._select_report(p))
            for child in row_frame.winfo_children():
                child.bind("<Button-1>", lambda e, p=report['file_path']: self._select_report(p))
            
            # 患者ID
            id_label = ctk.CTkLabel(
                row_frame,
                text=report['patient_id'],
                font=ctk.CTkFont(family=self.DEFAULT_FONT[0], size=self.DEFAULT_FONT[1]),
                width=120,
                anchor="w"
            )
            id_label.pack(side="left", padx=5)
            
            # 姓名
            name_label = ctk.CTkLabel(
                row_frame,
                text=report['name'],
                font=ctk.CTkFont(family=self.DEFAULT_FONT[0], size=self.DEFAULT_FONT[1]),
                width=150,
                anchor="w"
            )
            name_label.pack(side="left", padx=5)
            
            # 检查时间
            time_label = ctk.CTkLabel(
                row_frame,
                text=report['exam_time'],
                font=ctk.CTkFont(family=self.DEFAULT_FONT[0], size=self.DEFAULT_FONT[1]),
                width=150,
                anchor="w"
            )
            time_label.pack(side="left", padx=5)
            
            # 文件路径（截断显示）
            file_path_display = report['file_path']
            if len(file_path_display) > 50:
                file_path_display = "..." + file_path_display[-47:]
            path_label = ctk.CTkLabel(
                row_frame,
                text=file_path_display,
                font=ctk.CTkFont(family=self.DEFAULT_FONT[0], size=10),
                width=400,
                anchor="w",
                text_color=("gray50", "gray50")
            )
            path_label.pack(side="left", padx=5, fill="x", expand=True)
        
        # 更新统计信息
        self.stats_label.configure(text=f"共 {len(self.reports_data)} 条记录")
    
    def _select_report(self, file_path):
        """选择报告"""
        self.selected_file_path = file_path
        self.radio_var.set(file_path)
    
    def search_reports(self):
        """搜索报告"""
        search_text = self.search_entry.get().strip()
        
        if not search_text:
            self.load_reports()
            return
        
        # 使用DataManager搜索报告
        from json_page_renderer import load_page_config
        basic_info_page_id = self.controller._get_basic_info_page_id()
        basic_info_page_config = load_page_config(basic_info_page_id)
        
        basic_info_key = "基本信息"  # 默认
        if basic_info_page_config:
            basic_info_key = basic_info_page_config.get("title") or basic_info_page_config.get("name") or "基本信息"
        
        filtered_reports = self.controller.data_manager.search_reports(search_text, basic_info_key)
        
        # 显示过滤后的数据
        self.reports_data = filtered_reports
        self._update_display()
    
    def clear_search(self):
        """清空搜索"""
        self.search_entry.delete(0, "end")
        self.load_reports()
    
    def load_templates(self):
        """加载可用模板列表"""
        templates_index_path = os.path.join(self.db_path, "templates", "templates_index.json")
        if not os.path.exists(templates_index_path):
            return []
        
        try:
            with open(templates_index_path, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
                templates = index_data.get("templates", [])
                # 只返回启用的模板
                return [t for t in templates if t.get("enabled", True)]
        except Exception as e:
            print(f"加载模板索引失败: {e}")
            return []
    
    def toggle_template_menu(self):
        """切换模板菜单显示/隐藏（点击按钮）"""
        if self.menu_visible:
            self.hide_template_menu()
        else:
            self.show_template_menu()
    
    def show_template_menu(self):
        """显示模板选择菜单"""
        if not self.selected_file_path:
            messagebox.showwarning("提示", "请先选择要生成报告的数据")
            return
        
        # 加载模板列表
        templates = self.load_templates()
        if not templates:
            messagebox.showwarning("提示", "没有可用的报告模板")
            return
        
        # 如果菜单已存在，先销毁
        if self.template_menu_frame:
            self.template_menu_frame.destroy()
        
        # 计算需要的菜单高度
        menu_height = len(templates) * 34 + 10
        
        # 创建菜单框架（下拉菜单样式）- width和height需要在构造函数中设置
        # 使用主窗口作为父窗口，确保菜单显示在最上层
        self.template_menu_frame = ctk.CTkFrame(
            self.controller.root,
            width=200,
            height=menu_height,
            corner_radius=8,
            fg_color=("gray90", "gray20"),
            border_width=1,
            border_color=("gray75", "gray30")
        )
        
        # 计算菜单位置（在按钮下方）- 使用绝对坐标
        button_frame = self.generate_report_btn.master
        # 获取按钮在主窗口中的绝对位置
        btn_x = self.generate_report_btn.winfo_rootx() - self.controller.root.winfo_rootx()
        btn_y = self.generate_report_btn.winfo_rooty() - self.controller.root.winfo_rooty()
        btn_h = self.generate_report_btn.winfo_height()
        
        self.template_menu_frame.place(
            x=btn_x,
            y=btn_y + btn_h + 5
        )
        
        # 提升菜单到最前面，确保不被遮挡
        self.template_menu_frame.lift()
        self.template_menu_frame.update_idletasks()
        
        # 添加模板按钮
        for i, template in enumerate(templates):
            template_name = template.get("name", template.get("id", "未知模板"))
            template_id = template.get("id")
            
            template_btn = ctk.CTkButton(
                self.template_menu_frame,
                text=template_name,
                command=lambda tid=template_id: self.generate_report_with_template(tid),
                width=180,
                height=30,
                corner_radius=6,
                font=ctk.CTkFont(family=self.DEFAULT_FONT[0], size=self.DEFAULT_FONT[1]),
                fg_color=("gray80", "gray25"),
                hover_color=("gray70", "gray35"),
                anchor="w",
                text_color=("gray20", "gray90")
            )
            template_btn.pack(pady=2, padx=10)
        
        self.menu_visible = True
        
        # 绑定点击外部关闭菜单
        def close_menu_on_click(event):
            if self.template_menu_frame and self.menu_visible:
                # 检查点击是否在菜单外
                x = event.x_root
                y = event.y_root
                menu_x = self.template_menu_frame.winfo_rootx()
                menu_y = self.template_menu_frame.winfo_rooty()
                menu_w = self.template_menu_frame.winfo_width()
                menu_h = self.template_menu_frame.winfo_height()
                
                btn_x = self.generate_report_btn.winfo_rootx()
                btn_y = self.generate_report_btn.winfo_rooty()
                btn_w = self.generate_report_btn.winfo_width()
                btn_h = self.generate_report_btn.winfo_height()
                
                if not (menu_x <= x <= menu_x + menu_w and menu_y <= y <= menu_y + menu_h) and \
                   not (btn_x <= x <= btn_x + btn_w and btn_y <= y <= btn_y + btn_h):
                    self.hide_template_menu()
        
        # 绑定到主窗口，点击外部关闭菜单
        if not hasattr(self.controller.root, '_menu_close_bound'):
            self.controller.root.bind("<Button-1>", close_menu_on_click)
            self.controller.root._menu_close_bound = True
    
    def hide_template_menu(self):
        """隐藏模板菜单"""
        if self.template_menu_frame:
            self.template_menu_frame.destroy()
            self.template_menu_frame = None
        self.menu_visible = False
    
    def _open_generated_report(self, path):
        if not path or not os.path.exists(path):
            return
        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(path)  # type: ignore[attr-defined]
            elif system == "Darwin":
                subprocess.call(["open", path])
            else:
                subprocess.call(["xdg-open", path])
        except Exception:
            pass
    
    def generate_report_with_template(self, template_id):
        """使用指定模板生成报告"""
        # 关闭菜单
        self.hide_template_menu()
        
        if not self.selected_file_path:
            messagebox.showerror("错误", "未选择报告")
            return
        
        try:
            # 加载报告数据
            data = self.controller.data_manager.load_report(self.selected_file_path)
            if not data:
                messagebox.showerror("错误", "无法加载报告数据")
                return
            
            # 导入Excel生成器
            from excel_generator import ExcelGenerator
            
            # 创建生成器（使用指定模板）
            generator = ExcelGenerator(
                database_path=self.db_path,
                template_id=template_id
            )
            
            # 生成Excel报告（保存到database/excel目录）
            output_path = generator.generate(data)
            self._open_generated_report(output_path)
            messagebox.showinfo("成功", f"报告已成功生成:\n{output_path}")
            
        except Exception as e:
            import traceback
            error_msg = f"生成报告失败:\n{str(e)}\n\n详细信息:\n{traceback.format_exc()}"
            messagebox.showerror("错误", error_msg)
    
    def view_report(self):
        """查看报告详情"""
        if not self.selected_file_path:
            messagebox.showwarning("提示", "请先选择要查看的报告")
            return
        
        if not os.path.exists(self.selected_file_path):
            messagebox.showerror("错误", "报告文件不存在")
            return
        
        try:
            with open(self.selected_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 创建详情窗口
            detail_window = ctk.CTkToplevel(self)
            detail_window.title("报告详情")
            detail_window.geometry("800x600")
            detail_window.transient(self.controller.root)  # 设置为父窗口的临时窗口
            detail_window.lift()  # 提升到最前面
            detail_window.focus_force()  # 获得焦点
            
            # 创建滚动文本区域
            text_frame = ctk.CTkScrollableFrame(detail_window)
            text_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # 格式化显示JSON数据
            formatted_text = json.dumps(data, ensure_ascii=False, indent=2)
            
            text_widget = ctk.CTkTextbox(
                text_frame,
                width=750,
                height=550,
                font=ctk.CTkFont(family="Consolas", size=11),
                corner_radius=8
            )
            text_widget.pack(fill="both", expand=True)
            text_widget.insert("1.0", formatted_text)
            text_widget.configure(state="disabled")
            
        except Exception as e:
            messagebox.showerror("错误", f"读取报告失败: {str(e)}")
    
    def edit_report(self):
        """编辑报告 - 在文本编辑器中直接编辑JSON文件"""
        if not self.selected_file_path:
            messagebox.showwarning("提示", "请先选择要编辑的报告")
            return
        
        if not os.path.exists(self.selected_file_path):
            messagebox.showerror("错误", "报告文件不存在")
            return
        
        try:
            # 读取JSON文件
            with open(self.selected_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 创建编辑窗口
            edit_window = ctk.CTkToplevel(self)
            edit_window.title("编辑报告")
            edit_window.geometry("900x700")
            edit_window.transient(self.controller.root)  # 设置为父窗口的临时窗口
            edit_window.lift()  # 提升到最前面
            edit_window.focus_force()  # 获得焦点
            
            # 创建主框架
            main_frame = ctk.CTkFrame(edit_window)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # 标题
            title_label = ctk.CTkLabel(
                main_frame,
                text=f"编辑报告: {os.path.basename(self.selected_file_path)}",
                font=ctk.CTkFont(family=self.DEFAULT_FONT_BOLD[0], size=14, weight="bold")
            )
            title_label.pack(pady=(0, 10))
            
            # 创建滚动文本区域
            text_frame = ctk.CTkScrollableFrame(main_frame)
            text_frame.pack(fill="both", expand=True, pady=(0, 10))
            
            # 文本编辑器
            text_widget = ctk.CTkTextbox(
                text_frame,
                width=850,
                height=550,
                font=ctk.CTkFont(family="Consolas", size=11),
                corner_radius=8
            )
            text_widget.pack(fill="both", expand=True)
            
            # 格式化显示JSON数据
            formatted_text = json.dumps(data, ensure_ascii=False, indent=2)
            text_widget.insert("1.0", formatted_text)
            
            # 按钮区域
            button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            button_frame.pack(fill="x", pady=(10, 0))
            
            def save_changes():
                """保存更改"""
                try:
                    # 获取文本内容
                    content = text_widget.get("1.0", "end-1c")
                    
                    # 验证JSON格式
                    json_data = json.loads(content)
                    
                    # 保存到文件
                    with open(self.selected_file_path, 'w', encoding='utf-8') as f:
                        json.dump(json_data, f, ensure_ascii=False, indent=2)
                    
                    messagebox.showinfo("成功", "报告已成功保存")
                    edit_window.destroy()
                    # 刷新报告列表
                    self.load_reports()
                    
                except json.JSONDecodeError as e:
                    messagebox.showerror("错误", f"JSON格式错误，无法保存:\n{str(e)}")
                except Exception as e:
                    messagebox.showerror("错误", f"保存失败: {str(e)}")
            
            def cancel_edit():
                """取消编辑"""
                if messagebox.askyesno("确认", "确定要取消编辑吗？未保存的更改将丢失。"):
                    edit_window.destroy()
            
            # 保存按钮
            save_btn = ctk.CTkButton(
                button_frame,
                text="保存",
                command=save_changes,
                width=100,
                height=35,
                corner_radius=8,
                font=ctk.CTkFont(family=self.DEFAULT_FONT[0], size=self.DEFAULT_FONT[1]),
                fg_color=("gray70", "gray30"),
                hover_color=("gray60", "gray40")
            )
            save_btn.pack(side="left", padx=5)
            
            # 取消按钮
            cancel_btn = ctk.CTkButton(
                button_frame,
                text="取消",
                command=cancel_edit,
                width=100,
                height=35,
                corner_radius=8,
                font=ctk.CTkFont(family=self.DEFAULT_FONT[0], size=self.DEFAULT_FONT[1]),
                fg_color=("gray70", "gray30"),
                hover_color=("gray60", "gray40")
            )
            cancel_btn.pack(side="left", padx=5)
            
            # 关闭窗口事件
            edit_window.protocol("WM_DELETE_WINDOW", cancel_edit)
            
        except Exception as e:
            messagebox.showerror("错误", f"读取报告失败: {str(e)}")
    
    def delete_report(self):
        """删除报告"""
        if not self.selected_file_path:
            messagebox.showwarning("提示", "请先选择要删除的报告")
            return
        
        # 确认删除
        if messagebox.askyesno("确认删除", f"确定要删除以下报告吗？\n{self.selected_file_path}\n\n此操作不可恢复！"):
            # 使用DataManager删除报告
            success, message = self.controller.data_manager.delete_report(self.selected_file_path)
            if success:
                messagebox.showinfo("成功", message)
                self.selected_file_path = None
                self.load_reports()
            else:
                messagebox.showerror("错误", message)


