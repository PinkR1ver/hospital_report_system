import tkinter as tk
from tkinter import ttk, messagebox
import json
from tkcalendar import DateEntry
from datetime import datetime
import os
import shutil

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
        self.create_menu()
        self.create_widgets()
        self.load_data()

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="保存", command=self.save_data)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.destroy)

    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 绑定鼠标滚轮事件到整个窗口
        self.bind("<MouseWheel>", self._on_mousewheel)
        self.bind("<Button-4>", self._on_mousewheel)
        self.bind("<Button-5>", self._on_mousewheel)

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

    def load_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for key, page in self.pages.items():
            page.set_data(data.get(key, {}))

    def save_data(self):
        current_file_path = os.path.abspath(self.file_path)
        db_path = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
        arch_dir = os.path.join(db_path, 'arch', 'modified')
        report_arch_dir = os.path.join(arch_dir, 'report')
        pic_arch_dir = os.path.join(arch_dir, 'pic')
        if not os.path.exists(arch_dir):
            os.makedirs(arch_dir)
        if not os.path.exists(report_arch_dir):
            os.makedirs(report_arch_dir)
        if not os.path.exists(pic_arch_dir):
            os.makedirs(pic_arch_dir)

        # 生成归档文件名
        original_filename = os.path.basename(self.file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        arch_filename = f"{os.path.splitext(original_filename)[0]}_{timestamp}.json"
        arch_path = os.path.join(report_arch_dir, arch_filename)

        # 复制原始文件到归档目录
        shutil.copy2(self.file_path, arch_path)

        # 保存新数据
        data = {}
        for key, page in self.pages.items():
            page_data = page.get_data()
            if isinstance(page_data, dict) and len(page_data) == 1 and key in page_data:
                data[key] = page_data[key]
            else:
                data[key] = page_data

        # 处理图片
        self.process_images(data, pic_arch_dir, arch_path)

        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        messagebox.showinfo("保存成功", f"报告已成功保存\n原始文件已归档为: {arch_filename}")
        self.destroy()

    def process_images(self, data, pic_arch_dir, arch_path):
        db_path = os.path.dirname(os.path.dirname(os.path.dirname(self.file_path)))
        # read archive file get old_path
        with open(arch_path, 'r', encoding='utf-8') as f:
            archive_data = json.load(f)
            
        for test_name in ['头脉冲试验', '头脉冲抑制试验']:
            if test_name in archive_data and (test_name + '示意图') in archive_data[test_name]:
                old_path = archive_data[test_name][test_name + '示意图']
                if os.path.exists(os.path.join(db_path, old_path)):
                    new_path = data[test_name][test_name + '示意图']
                    if old_path != new_path:
                        # 移动旧图片到归档目录
                        old_filename = os.path.basename(old_path)
                        old_path = os.path.join(db_path, old_path)
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        arch_filename = f"{os.path.splitext(old_filename)[0]}_{timestamp}{os.path.splitext(old_filename)[1]}"
                        arch_pic_path = os.path.join(pic_arch_dir, arch_filename)
                        shutil.move(old_path, arch_pic_path)

                        # 复制新图片到原位置
                        shutil.copy2(new_path, old_path)

                        # 更新数据中的图片路径（保持不变）
                        data[test_name][test_name + '示意图'] = os.path.relpath(old_path, db_path)

    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")

# 在主应用程序中使用这个页面的示例
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = "path/to/your/json/file.json"
    edit_page = EditReportPage(root, file_path)
    root.mainloop()
