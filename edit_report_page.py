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
        self.geometry("1000x600")
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
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 创建侧边栏
        self.sidebar = ttk.Frame(self.main_frame, width=200, relief="sunken", borderwidth=1)
        self.sidebar.pack(side="left", fill="y", padx=5, pady=5)

        # 创建主内容区域
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # 创建所有测试页面
        self.pages = {
            "基本信息": BasicInfoPage(self.content_frame, self),
            "自发性眼震": SpontaneousNystagmusPage(self.content_frame, self),
            "凝视性眼震": GazeNystagmusPage(self.content_frame, self),
            "头脉冲试验": HeadImpulseTestPage(self.content_frame, self),
            "头脉冲抑制试验": HeadImpulseSuppressionTestPage(self.content_frame, self),
            "眼位反向偏斜": ReverseSkewPage(self.content_frame, self),
            "扫视检查": SaccadePage(self.content_frame, self),
            "视觉增强前庭-眼反射试验": VisualEnhancedVORPage(self.content_frame, self),
            "前庭-眼反射抑制试验": VORSuppressionPage(self.content_frame, self),
            "摇头试验": HeadShakingTestPage(self.content_frame, self),
            "位置试验 (Dix-Hallpike试验)": DixHallpikeTestPage(self.content_frame, self),
            "位置试验 (仰卧滚转试验)": SupineRollTestPage(self.content_frame, self),
            "位置试验(其他)": OtherPositionTestPage(self.content_frame, self),
            "视跟踪": VisualTrackingPage(self.content_frame, self),
            "视动性眼震": OptoKineticNystagmusPage(self.content_frame, self),
            "瘘管试验": FistulaTestPage(self.content_frame, self),
            "温度试验": CaloricTestPage(self.content_frame, self),
            "颈肌前庭诱发肌源性电位 (cVEMP)": CVEMPTestPage(self.content_frame, self),
            "眼肌前庭诱发肌源性电位 (oVEMP)": OVEMPTestPage(self.content_frame, self),
            "主观视觉垂直线 (SVV)": SVVTestPage(self.content_frame, self)
        }

        # 在侧边栏中添加按钮
        for i, (name, page) in enumerate(self.pages.items()):
            btn = ttk.Button(self.sidebar, text=name, command=lambda p=page: self.show_page(p))
            btn.pack(fill="x", padx=5, pady=2)
            page.pack_forget()  # 初始时隐藏所有页面

        # 默认显示第一个页面
        self.current_page = list(self.pages.values())[0]
        self.show_page(self.current_page)

    def show_page(self, page):
        if self.current_page:
            self.current_page.pack_forget()
        page.pack(fill="both", expand=True)
        self.current_page = page

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
        video_arch_dir = os.path.join(arch_dir, 'video')
        
        if not os.path.exists(arch_dir):
            os.makedirs(arch_dir)
        if not os.path.exists(report_arch_dir):
            os.makedirs(report_arch_dir)
        if not os.path.exists(pic_arch_dir):
            os.makedirs(pic_arch_dir)
        if not os.path.exists(video_arch_dir):
            os.makedirs(video_arch_dir)

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
        self.process_images(data, pic_arch_dir, video_arch_dir, arch_path)

        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        messagebox.showinfo("保存成功", f"报告已成功保存\n原始文件已归档为: {arch_filename}")
        self.destroy()

    def process_images(self, data, pic_arch_dir, vedio_arch_dir, arch_path):
        db_path = os.path.dirname(os.path.dirname(os.path.dirname(self.file_path)))
        self.db_path = db_path
        # 读取归档文件获取旧路径
        with open(arch_path, 'r', encoding='utf-8') as f:
            archive_data = json.load(f)
            
        # 处理图片
        for test_name in ['头脉冲试验', '头脉冲抑制试验']:
            if test_name in archive_data and (test_name + '示意图') in archive_data[test_name]:
                old_path = archive_data[test_name][test_name + '示意图']
                if old_path and os.path.exists(os.path.join(db_path, old_path)):
                    new_path = data.get(test_name, {}).get(test_name + '示意图')
                    if new_path and old_path != new_path:
                        self.archive_and_update_file(db_path, old_path, new_path, pic_arch_dir, data[test_name], test_name + '示意图')
                    elif not new_path:
                        # 如果新数据中没有图片，则删除旧图片
                        os.remove(os.path.join(db_path, old_path))
                        data[test_name].pop(test_name + '示意图', None)
                if old_path == '':
                    new_path = data.get(test_name, {}).get(test_name + '示意图')
                    if new_path:
                        pic_data_dir = os.path.join(db_path, 'pic', datetime.now().strftime("%Y-%m-%d"))
                        self.process_image(data, test_name, test_name + '示意图', pic_data_dir)
                        
        # 处理视频
        video_tests = [
            '仰卧滚转试验', '自发性眼震', '位置试验(其他)', '瘘管试验',
            '摇头试验', '凝视性眼震', '位置试验 (Dix-Hallpike试验)'
        ]
        for test_name in video_tests:
            if test_name in archive_data and '视频' in archive_data[test_name]:
                old_path = archive_data[test_name]['视频']
                if old_path and os.path.exists(os.path.join(db_path, old_path)):
                    new_path = data.get(test_name, {}).get('视频')
                    if new_path and old_path != new_path:
                        self.archive_and_update_file(db_path, old_path, new_path, vedio_arch_dir, data[test_name], '视频')
                    elif not new_path:
                        # 如果新数据中没有视频，则删除旧视频
                        os.remove(os.path.join(db_path, old_path))
                        data[test_name].pop('视频', None)
                if old_path == '':
                    new_path = data.get(test_name, {}).get('视频')
                    if new_path:
                        vedio_data_dir = os.path.join(db_path, 'video', datetime.now().strftime("%Y-%m-%d"))
                        self.process_video(data, test_name, vedio_data_dir)
                

    def archive_and_update_file(self, db_path, old_path, new_path, arch_dir, data_dict, key):
        old_full_path = os.path.join(db_path, old_path)
        new_full_path = os.path.join(db_path, new_path)
        
        if os.path.exists(old_full_path):
            # 生成归档文件名
            old_filename = os.path.basename(old_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            arch_filename = f"{os.path.splitext(old_filename)[0]}_{timestamp}{os.path.splitext(old_filename)[1]}"
            arch_file_path = os.path.join(arch_dir, arch_filename)

            # 移动旧文件到归档目录
            shutil.move(old_full_path, arch_file_path)

        if os.path.exists(new_full_path):
            # 复制新文件到原位置
            shutil.copy2(new_full_path, old_full_path)
            # 更新数据中的文件路径（保持相对路径不变）
            data_dict[key] = old_path
        else:
            # 如果新文件不存在，则从数据字典中删除该键
            data_dict.pop(key, None)
            
            
    def translate_test_name(self, test_name):
        translation = {
            "头脉冲试验": "head_impulse_test",
            "头脉冲抑制试验": "head_impulse_suppression_test",
            "位置试验 (Dix-Hallpike试验)": "dix_hallpike_test",
            "仰卧滚转试验": "supine_roll_test",
            "自发性眼震": "spontaneous_nystagmus",
            "位置试验(其他)": "other_position_test",
            "视动性眼震": "optokinetic_nystagmus",
            "摇头试验": "head_shaking_test",
            "凝视性眼震": "gaze_nystagmus",
            "瘘管试验": "fistula_test"
        }
        return translation.get(test_name, test_name.lower().replace(' ', '_'))

    def process_image(self, data, test_name, image_key, pic_folder):
        image_path = data.get(test_name, {}).get(image_key)
        if image_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name_en = self.translate_test_name(test_name)
            new_filename = f"{test_name_en}_{timestamp}{os.path.splitext(image_path)[1]}"
            new_path = os.path.join(pic_folder, new_filename)
            shutil.copy(image_path, new_path)
            data[test_name][image_key] = os.path.relpath(new_path, self.db_path)

    def process_video(self, data, test_name, video_folder):
        video_path = data.get(test_name, {}).get("视频")
        if video_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name_en = self.translate_test_name(test_name)
            new_filename = f"{test_name_en}_{timestamp}{os.path.splitext(video_path)[1]}"
            new_path = os.path.join(video_folder, new_filename)
            shutil.copy(video_path, new_path)
            data[test_name]["视频"] = os.path.relpath(new_path, self.db_path)

# 在主应用程序中使用这个页面的示例
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = "path/to/your/json/file.json"
    edit_page = EditReportPage(root, file_path)
    root.mainloop()
