import customtkinter as ctk
from tkinter import filedialog
from tkcalendar import DateEntry
import json
import os
import platform

# 设置清晰的字体
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


class JSONPageRenderer(ctk.CTkScrollableFrame):
    """通用的JSON页面渲染器"""
    
    def __init__(self, master, controller, page_config, theme_colors=None):
        self.theme_colors = theme_colors or {}
        super().__init__(master, fg_color=self._color("content_bg", ("gray96", "gray14")))
        self.controller = controller
        self.page_config = page_config
        self.widgets = {}
        self.labels = {}
        self.grid_params = {}
        self.vars = {}
        self.field_types = {}
        self.checkbox_groups = {}
        self.field_configs = {}
        self.field_frames = {}  # 存储字段容器，用于条件显示
        self.prev_radio_values = {}  # 记录各radio字段上一次已选值
        self._build_ui()

    def _color(self, key, fallback):
        value = self.theme_colors.get(key)
        if isinstance(value, (list, tuple)):
            if len(value) >= 2:
                return (value[0], value[1])
            if len(value) == 1:
                return (value[0], value[0])
        if isinstance(value, str):
            return value
        return fallback

    def _build_ui(self):
        """根据JSON配置构建UI"""
        # 页面标题 - 使用清晰字体
        title = self.page_config.get("title", "页面")
        title_label = ctk.CTkLabel(
            self, 
            text=title, 
            font=ctk.CTkFont(family=DEFAULT_FONT_LARGE[0], size=15, weight="bold"),
            text_color=self._color("text_primary", ("gray20", "gray90"))
        )
        title_label.pack(pady=(12, 8))
        
        # 按order排序sections
        sections = sorted(self.page_config.get("sections", []), key=lambda x: x.get("order", 0))
        
        for section in sections:
            self._create_section(self, section)

    def _create_section(self, parent, section):
        """创建分区"""
        section_name = section.get("name", "")
        # 美化分区样式 - 增加透明度和高级感
        section_frame = ctk.CTkFrame(
            parent, 
            corner_radius=12,
            fg_color=self._color("section_bg", ("gray96", "gray19")),  # 更浅的背景，增加层次感
            border_width=1,
            border_color=self._color("border", ("gray85", "gray28"))  # 更柔和的边框
        )
        section_frame.pack(fill="x", pady=4, padx=20)
        
        # 添加分区标题 - 使用清晰字体
        if section_name:
            section_title = ctk.CTkLabel(
                section_frame,
                text=section_name,
                font=ctk.CTkFont(family=DEFAULT_FONT_BOLD[0], size=12, weight="bold"),
                text_color=self._color("text_primary", ("gray25", "gray85"))
            )
            section_title.pack(pady=(8, 4))
        
        # 创建字段容器（使用grid布局）- 完全透明，增加层次感
        fields_container = ctk.CTkFrame(
            section_frame, 
            fg_color="transparent",
            corner_radius=0
        )
        fields_container.pack(fill="both", expand=True, padx=0, pady=(0, 8))
        
        # 按order排序fields
        fields = sorted(section.get("fields", []), key=lambda x: x.get("order", 0))
        
        # 使用网格布局让字段更紧凑（两列布局）
        # 先计算需要多少行
        regular_fields = [f for f in fields if f.get("type") not in ("textarea", "checkboxes", "radio")]
        special_fields = [f for f in fields if f.get("type") in ("textarea", "checkboxes", "radio")]
        
        # 创建普通字段（两列布局）
        row = 0
        for i, field in enumerate(regular_fields):
            col = (i % 2) * 2  # 0, 2, 0, 2...
            if i > 0 and i % 2 == 0:
                row += 1
            self._create_field(fields_container, field, row, col)
        
        # 创建特殊字段（占据整行）
        for field in special_fields:
            row += 1
            self._create_field(fields_container, field, row, 0, span=True)
        
        # 初始化条件显示
        for field in fields:
            self._init_field_visibility(field)

    def _create_field(self, parent, field, row, col, span=False):
        """创建字段"""
        key = field["key"]
        field_type = field.get("type", "entry")
        self.field_types[key] = field_type
        label = field.get("label", key)
        required = field.get("required", False)
        # 保存原始字段配置，供get_data时通用规则使用
        self.field_configs[key] = field
        
        # 创建标签
        label_text = f"{label}:"
        if required:
            label_text += " *"
        
        label_widget = ctk.CTkLabel(
            parent, 
            text=label_text,
            font=ctk.CTkFont(family=DEFAULT_FONT[0], size=DEFAULT_FONT[1]),
            text_color=self._color("text_secondary", ("gray30", "gray80"))
        )
        
        # 创建输入控件
        if field_type == "entry":
            widget = ctk.CTkEntry(
                parent,
                placeholder_text=field.get("placeholder", ""),
                width=280,
                height=32,
                font=ctk.CTkFont(family=DEFAULT_FONT[0], size=DEFAULT_FONT[1]),
                corner_radius=8,
                border_width=1,
                fg_color=self._color("input_bg", ("gray98", "gray16")),
                border_color=self._color("input_border", ("gray75", "gray32"))
            )
        elif field_type == "number":
            widget = ctk.CTkEntry(
                parent,
                placeholder_text=field.get("placeholder", "仅填数字"),
                width=280,
                height=32,
                font=ctk.CTkFont(family=DEFAULT_FONT[0], size=DEFAULT_FONT[1]),
                corner_radius=8,
                border_width=1,
                fg_color=self._color("input_bg", ("gray98", "gray16")),
                border_color=self._color("input_border", ("gray75", "gray32")),
                validate="key",
                validatecommand=(parent.register(self._validate_number), '%P')
            )
        elif field_type == "combobox":
            var = ctk.StringVar()
            widget = ctk.CTkComboBox(
                parent,
                values=field.get("values", []),
                variable=var,
                width=280,
                height=32,
                font=ctk.CTkFont(family=DEFAULT_FONT[0], size=DEFAULT_FONT[1]),
                dropdown_font=ctk.CTkFont(family=DEFAULT_FONT[0], size=DEFAULT_FONT[1]),
                corner_radius=8,
                border_width=1,
                fg_color=self._color("input_bg", ("gray98", "gray16")),
                border_color=self._color("input_border", ("gray75", "gray32")),
                button_color=self._color("accent_primary", ("gray70", "gray30")),
                button_hover_color=self._color("accent_hover", ("gray65", "gray35")),
                dropdown_fg_color=self._color("dropdown_bg", ("gray90", "gray20")),
                dropdown_hover_color=self._color("dropdown_hover", ("gray80", "gray28")),
                dropdown_text_color=self._color("dropdown_text", ("gray10", "gray90"))
            )
            self.vars[key] = var
        elif field_type == "radio":
            var = ctk.StringVar()
            self.vars[key] = var
            # 初始化上一次值
            self.prev_radio_values[key] = ""
            widget = ctk.CTkFrame(parent, fg_color="transparent")
            for i, val in enumerate(field.get("values", [])):
                rb = ctk.CTkRadioButton(
                    widget,
                    text=val,
                    variable=var,
                    value=val,
                    command=(lambda v=val, k=key: self._toggle_radio(k, v)),
                    font=ctk.CTkFont(family=DEFAULT_FONT[0], size=DEFAULT_FONT[1]),
                    text_color=self._color("text_secondary", ("gray30", "gray80"))
                )
                rb.grid(row=0, column=i, padx=10, pady=5)
        elif field_type == "checkboxes":
            widget = ctk.CTkFrame(parent, fg_color="transparent")
            group = []
            # 创建两列布局
            for i, val in enumerate(field.get("values", [])):
                var = ctk.BooleanVar()
                cb = ctk.CTkCheckBox(
                    widget,
                    text=val,
                    variable=var,
                    font=ctk.CTkFont(family=DEFAULT_FONT[0], size=DEFAULT_FONT[1]),
                    text_color=self._color("text_secondary", ("gray30", "gray80"))
                )
                row = i // 2
                col = i % 2
                cb.grid(row=row, column=col, padx=10, pady=5, sticky="w")
                group.append((val, var))
            self.checkbox_groups[key] = group
        elif field_type == "date":
            widget = DateEntry(
                parent, 
                width=12, 
                background='darkblue', 
                foreground='white', 
                borderwidth=2, 
                date_pattern=field.get("format", "yyyy/mm/dd")
            )
        elif field_type == "file":
            # 文件选择复合控件：只读输入+按钮组
            path_var = ctk.StringVar()
            self.vars[key] = path_var
            frame = ctk.CTkFrame(parent, fg_color="transparent")
            entry = ctk.CTkEntry(
                frame,
                textvariable=path_var,
                state='readonly',
                width=280,
                height=32,
                font=ctk.CTkFont(family=DEFAULT_FONT[0], size=DEFAULT_FONT[1]),
                corner_radius=8,
                border_width=1,
                fg_color=self._color("input_bg", ("gray98", "gray16")),
                border_color=self._color("input_border", ("gray75", "gray32"))
            )
            entry.pack(side="left", fill="x", expand=True, padx=(0, 6))

            def browse_file():
                file_path = filedialog.askopenfilename()
                if file_path:
                    path_var.set(file_path)

            def open_file():
                p = path_var.get()
                if p and os.path.exists(p):
                    if os.name == 'nt':
                        os.startfile(p)
                    elif os.name == 'posix':
                        try:
                            os.system(f'open "{p}"')
                        except Exception:
                            pass

            def clear_file():
                path_var.set("")

            btn_browse = ctk.CTkButton(
                frame, 
                text="选择", 
                command=browse_file, 
                width=55, 
                height=28,
                corner_radius=8,
                font=ctk.CTkFont(family=DEFAULT_FONT[0], size=10),
                fg_color=self._color("accent_primary", ("gray70", "gray30")),
                hover_color=self._color("accent_hover", ("gray65", "gray35")),
                border_width=0,
                text_color=("white", "white")
            )
            btn_browse.pack(side="left", padx=3)
            btn_open = ctk.CTkButton(
                frame, 
                text="打开", 
                command=open_file, 
                width=55, 
                height=28,
                corner_radius=8,
                font=ctk.CTkFont(family=DEFAULT_FONT[0], size=10),
                fg_color=self._color("accent_primary", ("gray70", "gray30")),
                hover_color=self._color("accent_hover", ("gray65", "gray35")),
                border_width=0,
                text_color=("white", "white")
            )
            btn_open.pack(side="left", padx=3)
            btn_clear = ctk.CTkButton(
                frame, 
                text="清除", 
                command=clear_file, 
                width=55, 
                height=28,
                corner_radius=8,
                font=ctk.CTkFont(family=DEFAULT_FONT[0], size=10),
                fg_color=self._color("accent_primary", ("gray70", "gray30")),
                hover_color=self._color("accent_hover", ("gray65", "gray35")),
                border_width=0,
                text_color=("white", "white")
            )
            btn_clear.pack(side="left", padx=3)

            widget = frame
        elif field_type == "textarea":
            widget = ctk.CTkTextbox(
                parent,
                height=field.get("height", 3) * 22,
                width=600,
                font=ctk.CTkFont(family=DEFAULT_FONT[0], size=DEFAULT_FONT[1]),
                corner_radius=8,
                border_width=1,
                fg_color=self._color("input_bg", ("gray98", "gray16")),
                border_color=self._color("input_border", ("gray75", "gray32"))
            )
        else:
            widget = ctk.CTkEntry(
                parent,
                width=280,
                height=32,
                font=ctk.CTkFont(family=DEFAULT_FONT[0], size=DEFAULT_FONT[1]),
                corner_radius=8,
                border_width=1,
                fg_color=self._color("input_bg", ("gray98", "gray16")),
                border_color=self._color("input_border", ("gray75", "gray32"))
            )
        
        # 使用grid布局让字段更紧凑
        field_frame = None
        if span or field_type in ("textarea", "checkboxes", "radio"):
            # 占据整行的字段
            label_widget.grid(row=row, column=0, sticky="w", padx=(15, 5), pady=(3, 0))
            widget.grid(row=row, column=1, columnspan=3, sticky="ew", padx=(5, 15), pady=(3, 3))
            parent.columnconfigure(1, weight=1)
        else:
            # 两列布局的普通字段 - 直接grid到parent
            label_widget.grid(row=row, column=col, sticky="e", padx=(15 if col == 0 else 10, 5), pady=3)
            widget.grid(row=row, column=col+1, sticky="ew", padx=(5, 15 if col == 0 else 10), pady=3)
            parent.columnconfigure(col+1, weight=1)
        
        # 存储控件引用
        self.widgets[key] = widget
        self.labels[key] = label_widget
        self.field_frames[key] = field_frame  # 存储字段容器
        
        # 存储布局信息（用于条件显示）
        self.grid_params[key] = {
            'field_type': field_type,
            'label': label_widget,
            'widget': widget
        }

        # 为依赖添加trace
        depends_on = field.get('show_when', {}).get('key') if field.get('show_when') else None
        if depends_on and depends_on in self.vars:
            # CustomTkinter的StringVar使用trace_add
            self.vars[depends_on].trace_add('write', lambda *args, f=field: self._apply_visibility(f))

        # 默认值支持
        if 'default' in field:
            default_val = field['default']
            if field_type in ("entry", "number"):
                try:
                    widget.delete(0, "end")
                    widget.insert(0, str(default_val))
                except Exception:
                    pass
            elif field_type == "combobox":
                self.vars[key].set(str(default_val))
            elif field_type == "radio":
                self.vars[key].set(str(default_val))
            elif field_type == "date":
                try:
                    widget.set_date(default_val)
                except Exception:
                    pass
            elif field_type == "checkboxes":
                sel = set(default_val if isinstance(default_val, list) else [default_val])
                for val, var in self.checkbox_groups.get(key, []):
                    var.set(val in sel)

    def _validate_number(self, value: str) -> bool:
        if value == "":
            return True
        try:
            float(value)
            return True
        except Exception:
            return False

    def _init_field_visibility(self, field):
        # 初始应用一次
        if field.get('show_when'):
            self._apply_visibility(field)

    def _toggle_radio(self, key, value):
        """支持再次点击已选中的单选按钮以取消选择"""
        try:
            # 使用上一次的值来判断是否取消；因为命令回调执行时变量已被按钮设为当前value
            prev = self.prev_radio_values.get(key, "")
            var = self.vars.get(key)
            if var is None:
                return
            if prev == value:
                var.set("")
                self.prev_radio_values[key] = ""
            else:
                var.set(value)
                self.prev_radio_values[key] = value
        except Exception:
            pass

    def _apply_visibility(self, field):
        cond = field.get('show_when')
        if not cond:
            return
        key = field['key']
        master_key = cond.get('key')
        equals_val = cond.get('equals')
        master_val = self._get_value(master_key)
        should_show = (master_val == equals_val)
        label = self.labels.get(key)
        widget = self.widgets.get(key)
        field_frame = self.field_frames.get(key)
        field_type = self.field_types.get(key)
        
        if should_show:
            # 显示控件
            label.grid()
            widget.grid()
        else:
            # 隐藏控件
            label.grid_remove()
            widget.grid_remove()

    def _get_value(self, key):
        w = self.widgets.get(key)
        if key in self.vars:
            return self.vars[key].get()
        if isinstance(w, ctk.CTkComboBox):
            return w.get()
        if isinstance(w, DateEntry):
            try:
                return w.get_date().strftime("%Y/%m/%d")
            except Exception:
                return ""
        if hasattr(w, 'get'):
            try:
                return w.get()
            except Exception:
                return ""
        return ""

    def get_data(self):
        """获取页面数据，根据页面JSON生成结构"""
        root_key = self.page_config.get('title') or self.page_config.get('name') or self.page_config.get('page_id', 'page')
        page_data = {}
        
        for key, widget in self.widgets.items():
            if key in self.checkbox_groups:
                selected = [val for val, var in self.checkbox_groups[key] if var.get()]
                value = selected
            elif key in self.vars:
                value = self.vars[key].get()
            elif isinstance(widget, ctk.CTkComboBox):
                value = widget.get()
            elif isinstance(widget, DateEntry):
                try:
                    value = widget.get_date().strftime("%Y/%m/%d")
                except Exception:
                    value = ""
            elif isinstance(widget, ctk.CTkTextbox):
                value = widget.get("1.0", "end-1c").strip()
            else:
                value = widget.get()

            # 通用自动填充：当满足条件且当前为空时，按JSON的autofill_when设置
            cfg = self.field_configs.get(key, {})
            cond = cfg.get('autofill_when')
            if cond and (value == "" or value == []):
                master_key = cond.get('key')
                equals_val = cond.get('equals')
                fill_val = cond.get('value', "")
                master_current = page_data.get(master_key)
                if master_current is None:
                    if master_key in self.vars:
                        master_current = self.vars[master_key].get()
                    elif master_key in self.widgets and hasattr(self.widgets[master_key], 'get'):
                        try:
                            master_current = self.widgets[master_key].get()
                        except Exception:
                            master_current = None
                if master_current == equals_val:
                    value = fill_val

            page_data[key] = value

        # 特定页面处理：结论页面
        if self.page_config.get('page_id') == 'conclusion':
            # 合并自定义结论和预设结论
            preset_conclusions = page_data.get("检查结论", [])
            custom_text = page_data.get("其它结论", "").strip()
            if custom_text:
                # 分割自定义结论（支持中文分号和英文分号）
                custom_conclusions = [c.strip() for c in custom_text.replace("；", ";").split(";")]
                custom_conclusions = [c for c in custom_conclusions if c]
                preset_conclusions.extend(custom_conclusions)
            page_data["检查结论"] = preset_conclusions
            # 移除"其它结论"字段，因为已经合并到检查结论中
            if "其它结论" in page_data:
                del page_data["其它结论"]

        return {root_key: page_data}

    def set_data(self, data):
        """设置页面数据"""
        # 获取页面数据key
        root_key = self.page_config.get('title') or self.page_config.get('name') or self.page_config.get('page_id', 'page')
        page_data = data.get(root_key, {})
        
        # 特定页面处理：结论页面
        if self.page_config.get('page_id') == 'conclusion':
            conclusions = page_data.get("检查结论", [])
            if isinstance(conclusions, list):
                # 找出预设结论（在checkbox_groups中的）
                preset_values = set()
                if "检查结论" in self.checkbox_groups:
                    preset_values = {val for val, var in self.checkbox_groups["检查结论"]}
                
                # 分离预设结论和自定义结论
                preset_conclusions = [c for c in conclusions if c in preset_values]
                custom_conclusions = [c for c in conclusions if c not in preset_values]
                
                # 设置预设结论
                page_data["检查结论"] = preset_conclusions
                # 设置自定义结论
                if custom_conclusions:
                    page_data["其它结论"] = "; ".join(custom_conclusions)
                else:
                    page_data["其它结论"] = ""
        
        for key, widget in self.widgets.items():
            value = page_data.get(key, "")
            if key in self.checkbox_groups:
                sel = set(value if isinstance(value, list) else [value])
                for val, var in self.checkbox_groups[key]:
                    var.set(val in sel)
            elif key in self.vars:
                self.vars[key].set(value)
                if self.field_types.get(key) == "radio":
                    self.prev_radio_values[key] = value or ""
            elif isinstance(widget, DateEntry):
                if value:
                    try:
                        widget.set_date(value)
                    except Exception:
                        pass
            elif isinstance(widget, ctk.CTkTextbox):
                widget.delete("1.0", "end")
                if value:
                    widget.insert("1.0", value)
            elif isinstance(widget, DateEntry):
                if value:
                    try:
                        widget.set_date(value)
                    except Exception:
                        pass
            elif hasattr(widget, 'set') and not isinstance(widget, ctk.CTkEntry):
                widget.set(value)
            else:
                widget.delete(0, "end")
                if value:
                    widget.insert(0, value)

    def clear_inputs(self):
        """清空所有输入"""
        for key, widget in self.widgets.items():
            try:
                # 复选框组
                if key in self.checkbox_groups:
                    for _, var in self.checkbox_groups[key]:
                        var.set(False)
                    continue
                # 通过变量管理的字段（radio/combobox/自定义等）
                if key in self.vars:
                    self.vars[key].set("")
                    # 若为单选，重置上一次值
                    if self.field_types.get(key) == "radio":
                        self.prev_radio_values[key] = ""
                    continue
                # 日期
                if isinstance(widget, DateEntry):
                    try:
                        # 尝试清空
                        widget.set_date("")
                    except Exception:
                        try:
                            widget.delete(0, "end")
                        except Exception:
                            pass
                    continue
                # 多行文本
                if isinstance(widget, ctk.CTkTextbox):
                    widget.delete("1.0", "end")
                    continue
                # 组合框（无变量的极少数情况）
                if hasattr(widget, "set") and not isinstance(widget, ctk.CTkEntry):
                    try:
                        widget.set("")
                        continue
                    except Exception:
                        pass
                # 普通输入
                if hasattr(widget, "delete"):
                    widget.delete(0, "end")
            except Exception:
                # 忽略单个字段清理异常，避免中断“新建”流程
                pass


def load_page_config(page_id):
    """加载页面配置"""
    config_path = os.path.join("pages", f"{page_id}.json")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None


