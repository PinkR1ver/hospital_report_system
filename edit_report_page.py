import tkinter as tk
from tkinter import ttk, messagebox
import json
from tkcalendar import DateEntry
from datetime import datetime

# 导入所有测试页面
from basic_info_page import BasicInfoPage
from spontaneous_nystagmus_page import SpontaneousNystagmusPage
from gaze_nystagmus_page import GazeNystagmusPage
from head_impulse_test_page import HeadImpulseTestPage
from head_impulse_suppression_test_page import HeadImpulseSuppressionTestPage
from reverse_skew_page import ReverseSkewPage
from saccade_page import SaccadePage
from visual_enhanced_vor_page import VisualEnhancedVORPage
from vor_suppression_page import VORSuppressionPage
from head_shaking_test_page import HeadShakingTestPage
from dix_hallpike_test_page import DixHallpikeTestPage
from supine_roll_test_page import SupineRollTestPage
from other_position_test_page import OtherPositionTestPage
from visual_tracking_page import VisualTrackingPage
from optokinetic_nystagmus_page import OptoKineticNystagmusPage
from fistula_test_page import FistulaTestPage
from caloric_test_page import CaloricTestPage
from cvemp_test_page import CVEMPTestPage
from ovemp_test_page import OVEMPTestPage
from svv_test_page import SVVTestPage

class EditReportPage(tk.Toplevel):
    def __init__(self, master, file_path):
        super().__init__(master)
        self.title("编辑报告")
        self.geometry("800x600")
        self.file_path = file_path
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 创建所有测试页面
        self.pages = {
            "基本信息": BasicInfoPage(self.scrollable_frame, self),
            "自发性眼震": SpontaneousNystagmusPage(self.scrollable_frame, self),
            "凝视性眼震": GazeNystagmusPage(self.scrollable_frame, self),
            "头脉冲试验": HeadImpulseTestPage(self.scrollable_frame, self),
            "头脉冲抑制试验": HeadImpulseSuppressionTestPage(self.scrollable_frame, self),
            "眼位反向偏斜": ReverseSkewPage(self.scrollable_frame, self),
            "扫视检查": SaccadePage(self.scrollable_frame, self),
            "视觉增强前庭-眼反射试验": VisualEnhancedVORPage(self.scrollable_frame, self),
            "前庭-眼反射抑制试验": VORSuppressionPage(self.scrollable_frame, self),
            "摇头试验": HeadShakingTestPage(self.scrollable_frame, self),
            "位置试验 (Dix-Hallpike试验)": DixHallpikeTestPage(self.scrollable_frame, self),
            "位置试验 (仰卧滚转试验)": SupineRollTestPage(self.scrollable_frame, self),
            "位置试验(其他)": OtherPositionTestPage(self.scrollable_frame, self),
            "视跟踪": VisualTrackingPage(self.scrollable_frame, self),
            "视动性眼震": OptoKineticNystagmusPage(self.scrollable_frame, self),
            "瘘管试验": FistulaTestPage(self.scrollable_frame, self),
            "温度试验": CaloricTestPage(self.scrollable_frame, self),
            "颈肌前庭诱发肌源性电位 (cVEMP)": CVEMPTestPage(self.scrollable_frame, self),
            "眼肌前庭诱发肌源性电位 (oVEMP)": OVEMPTestPage(self.scrollable_frame, self),
            "主观视觉垂直线 (SVV)": SVVTestPage(self.scrollable_frame, self)
        }

        for page in self.pages.values():
            page.pack(fill=tk.X, padx=10, pady=5)

        # 保存按钮
        ttk.Button(self.scrollable_frame, text="保存", command=self.save_data).pack(pady=10)

    def load_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for key, page in self.pages.items():
            page.set_data(data.get(key, {}))

    def save_data(self):
        data = {}
        for key, page in self.pages.items():
            data[key] = page.get_data()

        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        messagebox.showinfo("保存成功", "报告已成功保存")
        self.destroy()

# 在主应用程序中使用这个页面的示例
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = "path/to/your/json/file.json"
    edit_page = EditReportPage(root, file_path)
    root.mainloop()