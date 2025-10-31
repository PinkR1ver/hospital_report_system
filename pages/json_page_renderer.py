import tkinter as tk
from tkinter import ttk, filedialog
from tkcalendar import DateEntry
import json
import os


class JSONPageRenderer(ttk.Frame):
    """通用的JSON页面渲染器"""
    
    def __init__(self, master, controller, page_config):
        super().__init__(master)
        self.controller = controller
        self.page_config = page_config
        self.widgets = {}
        self.labels = {}
        self.grid_params = {}
        self.vars = {}
        self.field_types = {}
        self.checkbox_groups = {}
        self.field_configs = {}
        self._build_ui()

    def _build_ui(self):
        """根据JSON配置构建UI"""
        # 创建主容器
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 页面标题
        title = self.page_config.get("title", "页面")
        title_label = ttk.Label(main_container, text=title, font=("TkDefaultFont", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 按order排序sections
        sections = sorted(self.page_config.get("sections", []), key=lambda x: x.get("order", 0))
        
        for section in sections:
            self._create_section(main_container, section)

    def _create_section(self, parent, section):
        """创建分区"""
        section_name = section.get("name", "")
        section_frame = ttk.LabelFrame(parent, text=section_name)
        section_frame.pack(fill=tk.X, pady=10)
        
        # 按order排序fields
        fields = sorted(section.get("fields", []), key=lambda x: x.get("order", 0))
        
        # 创建字段网格
        for i, field in enumerate(fields):
            self._create_field(section_frame, field, i)
        
        # 初始化条件显示
        for field in fields:
            self._init_field_visibility(field)

    def _create_field(self, parent, field, index):
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
        
        label_widget = ttk.Label(parent, text=label_text)
        
        # 创建输入控件
        if field_type == "entry":
            widget = ttk.Entry(parent)
            if "placeholder" in field:
                widget.insert(0, field["placeholder"])
        elif field_type == "number":
            vcmd = (parent.register(self._validate_number), '%P')
            widget = ttk.Entry(parent, validate='key', validatecommand=vcmd)
        elif field_type == "combobox":
            var = tk.StringVar()
            widget = ttk.Combobox(parent, textvariable=var, values=field.get("values", []))
            self.vars[key] = var
        elif field_type == "radio":
            var = tk.StringVar()
            self.vars[key] = var
            widget = ttk.Frame(parent)
            for val in field.get("values", []):
                rb = ttk.Radiobutton(widget, text=val, value=val, variable=var)
                rb.pack(side=tk.LEFT, padx=6)
        elif field_type == "checkboxes":
            widget = ttk.Frame(parent)
            group = []
            for val in field.get("values", []):
                var = tk.BooleanVar()
                cb = ttk.Checkbutton(widget, text=val, variable=var)
                cb.pack(side=tk.LEFT, padx=6)
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
            path_var = tk.StringVar()
            self.vars[key] = path_var
            frame = ttk.Frame(parent)
            entry = ttk.Entry(frame, textvariable=path_var)
            entry.configure(state='readonly')
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))

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

            btn_browse = ttk.Button(frame, text="选择", command=browse_file)
            btn_browse.pack(side=tk.LEFT, padx=3)
            btn_open = ttk.Button(frame, text="打开", command=open_file)
            btn_open.pack(side=tk.LEFT, padx=3)
            btn_clear = ttk.Button(frame, text="清除", command=clear_file)
            btn_clear.pack(side=tk.LEFT, padx=3)

            widget = frame
        else:
            widget = ttk.Entry(parent)
        
        # 网格布局
        row = index // 2
        col = (index % 2) * 2
        
        label_widget.grid(row=row, column=col, sticky=tk.E, padx=(10, 5), pady=5)
        widget.grid(row=row, column=col+1, sticky=tk.EW, padx=(5, 10), pady=5)
        
        # 配置列权重
        parent.columnconfigure(col+1, weight=1)
        
        # 存储控件引用
        self.widgets[key] = widget
        self.labels[key] = label_widget
        self.grid_params[key] = {
            'label': {'row': row, 'column': col, 'sticky': tk.E, 'padx': (10, 5), 'pady': 5},
            'widget': {'row': row, 'column': col+1, 'sticky': tk.EW, 'padx': (5, 10), 'pady': 5}
        }

        # 为依赖添加trace
        depends_on = field.get('show_when', {}).get('key') if field.get('show_when') else None
        if depends_on and depends_on in self.vars:
            self.vars[depends_on].trace_add('write', lambda *args, f=field: self._apply_visibility(f))

        # 默认值支持
        if 'default' in field:
            default_val = field['default']
            if field_type in ("entry", "number"):
                try:
                    widget.delete(0, tk.END)
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
        if should_show:
            # 重新grid显示
            lp = self.grid_params[key]['label']
            wp = self.grid_params[key]['widget']
            label.grid(**lp)
            widget.grid(**wp)
        else:
            label.grid_remove()
            widget.grid_remove()

    def _get_value(self, key):
        w = self.widgets.get(key)
        if key in self.vars:
            return self.vars[key].get()
        if isinstance(w, ttk.Combobox):
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
            elif isinstance(widget, ttk.Combobox):
                value = widget.get()
            elif isinstance(widget, DateEntry):
                try:
                    value = widget.get_date().strftime("%Y/%m/%d")
                except Exception:
                    value = ""
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

        return {root_key: page_data}

    def set_data(self, data):
        """设置页面数据"""
        basic = data.get("基本信息", {})
        
        for key, widget in self.widgets.items():
            value = basic.get(key, "")
            if key in self.checkbox_groups:
                sel = set(value if isinstance(value, list) else [value])
                for val, var in self.checkbox_groups[key]:
                    var.set(val in sel)
            elif key in self.vars:
                self.vars[key].set(value)
            elif isinstance(widget, DateEntry):
                if value:
                    try:
                        widget.set_date(value)
                    except Exception:
                        pass
            elif hasattr(widget, 'set') and not isinstance(widget, ttk.Entry):
                widget.set(value)
            else:
                widget.delete(0, tk.END)
                if value:
                    widget.insert(0, value)

    def clear_inputs(self):
        """清空所有输入"""
        for key, widget in self.widgets.items():
            if key in self.vars:
                self.vars[key].set("")
            elif isinstance(widget, DateEntry):
                widget.delete(0, tk.END)
            else:
                widget.delete(0, tk.END)


def load_page_config(page_id):
    """加载页面配置"""
    config_path = os.path.join("pages", f"{page_id}.json")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
