import tkinter as tk
from tkinter import ttk

class ConclusionPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # 创建标题标签
        title_label = ttk.Label(self, text="检查结论", font=("SimSun", 12, "bold"))
        title_label.pack(pady=10)
        
        # 创建结论选项
        self.conclusions = [
            "请结合临床",
            "未见明显异常",
            "不典型位置性眼震",
            "右侧周围前庭功能损害",
            "左侧周围前庭功能损害",
            "双侧周围前庭功能损害",
            "右侧外半规管功能损害",
            "左侧外半规管功能损害",
            "双侧外半规管功能损害",
            "右后半规管功能损害",
            "左后半规管功能损害",
            "右前半规管功能损害",
            "左前半规管功能损害",
            "右侧外半规管增益降低",
            "左侧外半规管增益降低",
            "双侧外半规管增益降低",
            "右后半规管增益降低",
            "左后半规管增益降低",
            "右前半规管增益降低",
            "左前半规管增益降低",
            "右侧外半规管增益增高",
            "左侧外半规管增益增高",
            "双侧外半规管增益增高",
            "右前半规管良性阵发性位置性眩晕可能",
            "左前半规管良性阵发性位置性眩晕可能",
            "右后半规管良性阵发性位置性眩晕可能",
            "左后半规管良性阵发性位置性眩晕可能",
            "右外半规管良性阵发性位置性眩晕（管石症）可能",
            "左外半规管良性阵发性位置性眩晕（管石症）可能",
            "右外半规管良性阵发性位置性眩晕（嵴石症）可能",
            "左外半规管良性阵发性位置性眩晕（嵴石症）可能",
            "右外半规管良性阵发性位置性眩晕（嵴石症转管石症）可能",
            "左外半规管良性阵发性位置性眩晕（嵴石症转管石症）可能",
            "右外半规管轻嵴帽可能",
            "左外半规管轻嵴帽可能",
            "右外半规管重嵴帽可能",
            "左外半规管重嵴帽可能",
            "凝视眼震阳性",
            "自发眼震阳性",
            "摇头眼震阳性",
            "凝视变向眼震",
            "位置性旋转性眼震阳性",
            "中枢性眼震可能",
            "先天性眼球震颤可能",
            "方波急跳性眼震可能",
            "前庭眼反射试验异常",
            "前庭眼反射抑制试验异常",
            "扫视试验异常",
            "反向偏斜试验阳性",
            "瘘管试验阳性",
            "病理性内耳第三窗可能"
        ]
        
        # 创建自定义结论输入框
        custom_frame = ttk.Frame(self)
        custom_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(custom_frame, text="其它结论（用分号;分隔多个结论）:").pack(side="left", padx=5)
        self.custom_conclusion = tk.Text(custom_frame, height=1, width=30)
        self.custom_conclusion.pack(side="left", padx=5, fill="x", expand=True)
        
        # 创建滚动框架
        self.canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # 创建3列框架
        columns_frame = ttk.Frame(self.scrollable_frame)
        columns_frame.pack(fill="both", expand=True, padx=5)
        
        column1 = ttk.Frame(columns_frame)
        column2 = ttk.Frame(columns_frame)
        column3 = ttk.Frame(columns_frame)
        
        column1.pack(side="left", fill="both", expand=True, padx=5)
        column2.pack(side="left", fill="both", expand=True, padx=5)
        column3.pack(side="left", fill="both", expand=True, padx=5)
        
        # 计算每列应显示的项目数
        items_per_column = len(self.conclusions) // 3
        if len(self.conclusions) % 3:
            items_per_column += 1
        
        # 创建复选框变量和控件，按列分布
        self.checkboxes = {}
        for i, conclusion in enumerate(self.conclusions):
            var = tk.BooleanVar()
            # 确定当前项目应该放在哪一列
            if i < items_per_column:
                parent_frame = column1
            elif i < items_per_column * 2:
                parent_frame = column2
            else:
                parent_frame = column3
                
            cb = ttk.Checkbutton(parent_frame, text=conclusion, variable=var)
            cb.pack(anchor="w", pady=2)
            self.checkboxes[conclusion] = var
            
        # 布局
        self.canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")
        
        # # 绑定鼠标滚轮事件
        # self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # 将焦点设置到主框架
        # self.focus_set()
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def get_data(self):
        selected_conclusions = []
        # 获取选中的预设结论
        for conclusion, var in self.checkboxes.items():
            if var.get():
                selected_conclusions.append(conclusion)
        
        # 获取自定义结论
        custom_text = self.custom_conclusion.get("1.0", "end-1c").strip()
        if custom_text:
            # 分割自定义结论（支持中文分号和英文分号）
            custom_conclusions = [c.strip() for c in custom_text.replace("；", ";").split(";")]
            # 只添加非空的结论
            selected_conclusions.extend([c for c in custom_conclusions if c])
            
        return {"检查结论": selected_conclusions}

    def set_data(self, data):
        # 如果传入的是字典，就从字典中获取列表
        if isinstance(data, dict):
            conclusions = data.get("检查结论", [])
        # 如果传入的直接是列表，就直接使用
        elif isinstance(data, list):
            conclusions = data
        else:
            conclusions = []
        
        # 重置所有复选框
        for conclusion, var in self.checkboxes.items():
            var.set(conclusion in conclusions)
        
        # 找出不在预设选项中的结论，作为自定义结论
        custom_conclusions = [c for c in conclusions if c not in self.checkboxes]
        if custom_conclusions:
            self.custom_conclusion.delete("1.0", "end")
            self.custom_conclusion.insert("1.0", "; ".join(custom_conclusions))

    def clear_inputs(self):
        # 清空所有复选框
        for conclusion, var in self.checkboxes.items():
            var.set(False)
        # 清空自定义结论
        self.custom_conclusion.delete("1.0", "end")

