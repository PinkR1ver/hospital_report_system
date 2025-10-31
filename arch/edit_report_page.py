import tkinter as tk
from tkinter import ttk, messagebox
import json
from tkcalendar import DateEntry
from datetime import datetime
import os
import shutil
from utils import *

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
from conclusion_page import ConclusionPage

class EditReportPage(tk.Toplevel):
    def __init__(self, master, file_path):
        super().__init__(master)
        self.title("编辑报告")
        self.geometry("1000x700")
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
            "主观视觉垂直线 (SVV)": SVVTestPage(self.content_frame, self),
            "检查结论": ConclusionPage(self.content_frame, self)
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
        his_arch_dir = os.path.join(db_path, 'HIS')
        
        if not os.path.exists(arch_dir):
            os.makedirs(arch_dir)
        if not os.path.exists(report_arch_dir):
            os.makedirs(report_arch_dir)
        if not os.path.exists(pic_arch_dir):
            os.makedirs(pic_arch_dir)
        if not os.path.exists(video_arch_dir):
            os.makedirs(video_arch_dir)
        if not os.path.exists(his_arch_dir):
            os.makedirs(his_arch_dir)

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
        for test_name in ['头脉冲试验', '头脉冲抑制试验', '温度试验']:
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
            # 如果新文件不存在，则将该键值置为空字符串
            data_dict[key] = ""
            
            
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
            "瘘管试验": "fistula_test",
            "温度试验": "caloric_test"
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
            
    def save_his_report(self, data):
            
            # 收集所有检查结果
            results = []
            
            # 自发性眼震
            spontaneous = data.get("自发性眼震", {})
            if not is_dict_empty(spontaneous):
                if spontaneous.get("自发性眼震模式", "") != "":
                    results.append("自发性眼震模式：" + spontaneous.get("自发性眼震模式", ""))
                if spontaneous.get("自发性眼震速度", "") != "":
                    results.append("自发性眼震速度：" + spontaneous.get("自发性眼震速度", ""))
                if spontaneous.get("自发性眼震固视抑制", "") != "":
                    results.append("自发性眼震固视抑制：" + spontaneous.get("自发性眼震固视抑制", ""))
            
            # 凝视性眼震
            gaze = data.get("凝视性眼震", {})
            if not is_dict_empty(gaze):
                if gaze.get("凝视性眼震模式（上）", "") != "":
                    results.append("凝视性眼震模式（上）: " + gaze.get("凝视性眼震模式（上）", ""))
                if gaze.get("凝视性眼震速度（上）", "") != "":
                    results.append("凝视性眼震速度（上，度/秒）: " + gaze.get("凝视性眼震速度（上）", ""))
                if gaze.get("凝视性眼震模式（下）", "") != "":
                    results.append("凝视性眼震模式（下）: " + gaze.get("凝视性眼震模式（下）", ""))
                if gaze.get("凝视性眼震速度（下）", "") != "":
                    results.append("凝视性眼震速度（下，度/秒）: " + gaze.get("凝视性眼震速度（下）", ""))
                if gaze.get("凝视性眼震模式（左）", "") != "":
                    results.append("凝视性眼震模式（左）: " + gaze.get("凝视性眼震模式（左）", ""))
                if gaze.get("凝视性眼震速度（右）", "") != "":
                    results.append("凝视性眼震速度（右，度/秒）: " + gaze.get("凝视性眼震速度（右）", ""))
            
            # 头脉冲试验
            hit = data.get("头脉冲试验", {})
            if not is_dict_empty(hit):
                if hit.get("VOR增益（左外半规管）", "") != "":
                    results.append("VOR增益（左外半规管）：" + hit.get("VOR增益（左外半规管）", ""))
                if hit.get("PR分数（左外半规管）", "") != "":
                    results.append("PR分数（左外半规管，%）：" + hit.get("PR分数（左外半规管）", ""))
                if hit.get("VOR增益（右外半规管）", "") != "":
                    results.append("VOR增益（右外半规管）：" + hit.get("VOR增益（右外半规管）", ""))
                if hit.get("PR分数（右外半规管）", "") != "":
                    results.append("PR分数（右外半规管，%）：" + hit.get("PR分数（右外半规管）", ""))
                if hit.get("VOR增益（左前半规管）", "") != "":
                    results.append("VOR增益（左前半规管）：" + hit.get("VOR增益（左前半规管）", ""))
                if hit.get("PR分数（右前半规管）", "") != "":
                    results.append("PR分数（右前半规管，%）：" + hit.get("PR分数（右前半规管）", ""))
                if hit.get("VOR增益（左后半规管）", "") != "":
                    results.append("VOR增益（左后半规管）：" + hit.get("VOR增益（左后半规管）", ""))
                if hit.get("PR分数（左后半规管）", "") != "":
                    results.append("PR分数（左后半规管，%）：" + hit.get("PR分数（左后半规管）", ""))
                if hit.get("VOR增益（右后半规管）", "") != "":
                    results.append("VOR增益（右后半规管）：" + hit.get("VOR增益（右后半规管）", ""))
                if hit.get("PR分数（右后半规管）", "") != "":
                    results.append("PR分数（右后半规管，%）：" + hit.get("PR分数（右后半规管）", ""))
            
                # 补偿性扫视波（多选项）
                compensatory_waves = hit.get("头脉冲试验补偿性扫视波", [])
                if compensatory_waves != []:
                    if isinstance(compensatory_waves, list):
                        results.append("头脉冲试验补偿性扫视波: " + "、".join(compensatory_waves))
                    else:
                        results.append("头脉冲试验补偿性扫视波: " + str(compensatory_waves))
            
            # 头脉冲抑制试验
            hit_suppression = data.get("头脉冲抑制试验", {})
            if not is_dict_empty(hit_suppression):
                if hit_suppression.get("头脉冲抑制试验增益（左外半规管）", "") != "":
                    results.append("头脉冲抑制试验增益（左外半规管）：" + hit_suppression.get("头脉冲抑制试验增益 (左外半规管)", ""))
                if hit_suppression.get("头脉冲抑制试验增益（右外半规管）", "") != "":
                    results.append("头脉冲抑制试验增益（右外半规管）： " + hit_suppression.get("头脉冲抑制试验增益 (右外半规管)", ""))
                
                # 补偿性扫视波（多选项）
                compensation_waves = hit_suppression.get("头脉冲抑制试验补偿性扫视波", [])
                if compensation_waves != []:
                    if isinstance(compensation_waves, list):
                        results.append("头脉冲抑制试验补偿性扫视波：" + "、".join(compensation_waves))
                    else:
                        results.append("头脉冲抑制试验补偿性扫视波：" + str(compensation_waves))
            
            # 眼位反向偏斜
            skew = data.get("眼位反向偏斜", {})
            if not is_dict_empty(skew):
                if skew.get("眼位反向偏斜（HR, 度）", "") != "":
                    results.append("眼位反向偏斜（HR, 度）：" + skew.get("眼位反向偏斜 (HR, 度)", ""))
                if skew.get("眼位反向偏斜（VR, 度）", "") != "":
                    results.append("眼位反向偏斜（VR, 度）：" + skew.get("眼位反向偏斜 (VR, 度)", ""))
            
            # 扫视检查
            saccade = data.get("扫视检查", {})
            if not is_dict_empty(saccade):
                if saccade.get("扫视延迟时间（右向, 毫秒）", "") != "":
                    results.append("扫视延迟时间（右向, 毫秒）：" + saccade.get("扫视延迟时间 (右向, 毫秒)", ""))
                if saccade.get("扫视延迟时间（左向, 毫秒）", "") != "":
                    results.append("扫视延迟时间（左向, 毫秒）：" + saccade.get("扫视延迟时间 (左向, 毫秒)", ""))
                if saccade.get("扫视峰速度（右向, 度/秒）", "") != "":
                    results.append("扫视峰速度（右向, 度/秒）：" + saccade.get("扫视峰速度 (右向, 度/秒)", ""))
                if saccade.get("扫视峰速度（左向, 度/秒）", "") != "":
                    results.append("扫视峰速度（左向, 度/秒）：" + saccade.get("扫视峰速度 (左向, 度/秒)", ""))
                if saccade.get("扫视精确度（右向, %）", "") != "":
                    results.append("扫视精确度（右向, %）：" + saccade.get("扫视精确度 (右向, %)", ""))
                if saccade.get("扫视精确度（左向, %）", "") != "":
                    results.append("扫视精确度（左向, %）：" + saccade.get("扫视精确度 (左向, %)", ""))
            
            # 视觉增强前庭-眼反射试验
            vevor = data.get("视觉增强前庭-眼反射试验", {})
            if not is_dict_empty(vevor):
                if vevor.get("检查结果", "") != "":
                    results.append("视觉增强前庭-眼反射试验检查结果：" + vevor.get("检查结果", ""))
            
            # 前庭-眼反射抑制试验
            vor_suppression = data.get("前庭-眼反射抑制试验", {})
            if not is_dict_empty(vor_suppression):
                if vor_suppression.get("检查结果", "") != "":
                    results.append("前庭-眼反射抑制试验检查结果：" + vor_suppression.get("检查结果", ""))
            
            # 摇头试验
            hst = data.get("摇头试验", {})
            if not is_dict_empty(hst):
                if hst.get("眼震模式", "") != "":
                    results.append("眼震模式（摇头试验）：" + hst.get("眼震模式", ""))
                if hst.get("眼震速度", "") != "":
                    results.append("眼震速度（摇头试验，度/秒）：" + hst.get("眼震速度", ""))
                if hst.get("摇头方向", "") != "":
                    results.append("摇头诱发眼震方向： " + hst.get("摇头方向", ""))
            
            # Dix-Hallpike试验
            dix = data.get("位置试验 (Dix-Hallpike试验)", {})
            if not is_dict_empty(dix):
                if dix.get("右侧眼震模式", "") != "":   
                    results.append("眼震模式（右侧D-H试验）：" + dix.get("右侧眼震模式", ""))
                if dix.get("右侧坐起眼震模式", "") != "":
                    results.append("坐起眼震模式（右侧D-H试验）：" + dix.get("右侧坐起眼震模式", ""))
                if dix.get("右侧出现眩晕/头晕", "") != "":
                    results.append("出现眩晕/头晕（右侧D-H试验）：" + dix.get("右侧出现眩晕/头晕", ""))
                if dix.get("右侧眼震潜伏期 (秒)", "") != "":
                    results.append("眼震潜伏期（右侧D-H试验，秒）：" + dix.get("右侧眼震潜伏期 (秒)", ""))
                if dix.get("右侧眼震持续时长 (秒)", "") != "":
                    results.append("眼震持续时长（右侧D-H试验，秒）：" + dix.get("右侧眼震持续时长 (秒)", ""))
                if dix.get("右侧眼震最大速度 (度/秒)", "") != "":
                    results.append("眼震最大速度（右侧D-H试验，度/秒）：" + dix.get("右侧眼震最大速度 (度/秒)", ""))
                if dix.get("右侧眼震疲劳性", "") != "": 
                    results.append("眼震疲劳性（右侧D-H试验）：" + dix.get("右侧眼震疲劳性", ""))
                if dix.get("左侧眼震模式", "") != "":
                    results.append("眼震模式（左侧D-H试验）：" + dix.get("左侧眼震模式", ""))
                if dix.get("左侧坐起眼震模式", "") != "":
                    results.append("坐起眼震模式（左侧D-H试验）：" + dix.get("左侧坐起眼震模式", ""))
                if dix.get("左侧出现眩晕/头晕", "") != "":
                    results.append("出现眩晕/头晕（左侧D-H试验）：" + dix.get("左侧出现眩晕/头晕", ""))
                if dix.get("左侧眼震潜伏期 (秒)", "") != "":
                    results.append("眼震潜伏期（左侧D-H试验，秒）：" + dix.get("左侧眼震潜伏期 (秒)", ""))
                if dix.get("左侧眼震持续时长 (秒)", "") != "":
                    results.append("眼震持续时长（左侧D-H试验，秒）：" + dix.get("左侧眼震持续时长 (秒)", ""))
                if dix.get("左侧眼震最大速度 (度/秒)", "") != "":
                    results.append("眼震最大速度（左侧D-H试验，度/秒）：" + dix.get("左侧眼震最大速度 (度/秒)", ""))
                if dix.get("左侧眼震疲劳性", "") != "":
                    results.append("眼震疲劳性（左侧D-H试验）：" + dix.get("左侧眼震疲劳性", ""))
                    
            # 仰卧滚转试验
            roll = data.get("位置试验 (仰卧滚转试验)", {})
            if not is_dict_empty(roll):
                if roll.get("右侧眼震模式", "") != "":  
                    results.append("眼震模式（右侧仰卧滚转试验）：" + roll.get("右侧眼震模式", ""))
                if roll.get("右侧出现眩晕/头晕", "") != "":
                    results.append("出现眩晕/头晕（右侧仰卧滚转试验）：" + roll.get("右侧出现眩晕/头晕", ""))
                if roll.get("右侧眼震潜伏期 (秒)", "") != "":
                    results.append("眼震潜伏期（右侧仰卧滚转试验，秒）：" + roll.get("右侧眼震潜伏期 (秒)", ""))
                if roll.get("右侧眼震持续时长 (秒)", "") != "":
                    results.append("眼震持续时长（右侧仰卧滚转试验，秒）：" + roll.get("右侧眼震持续时长 (秒)", ""))
                if roll.get("右侧眼震最大速度 (度/秒)", "") != "":
                    results.append("眼震最大速度（右侧仰卧滚转试验，度/秒）：" + roll.get("右侧眼震最大速度 (度/秒)", ""))
                if roll.get("左侧眼震模式", "") != "":
                    results.append("眼震模式（左侧仰卧滚转试验）：" + roll.get("左侧眼震模式", ""))
                if roll.get("左侧出现眩晕/头晕", "") != "":
                    results.append("出现眩晕/头晕（左侧仰卧滚转试验）：" + roll.get("左侧出现眩晕/头晕", ""))
                if roll.get("左侧眼震潜伏期 (秒)", "") != "":
                    results.append("眼震潜伏期（左侧仰卧滚转试验，秒）：" + roll.get("左侧眼震潜伏期 (秒)", ""))
                if roll.get("左侧眼震持续时长 (秒)", "") != "":
                    results.append("眼震持续时长（左侧仰卧滚转试验，秒）：" + roll.get("左侧眼震持续时长 (秒)", ""))
                if roll.get("左侧眼震最大速度 (度/秒)", "") != "":
                    results.append("眼震最大速度（左侧仰卧滚转试验，度/秒）：" + roll.get("左侧眼震最大速度 (度/秒)", ""))
        
            # 其他位置试验
            other = data.get("位置试验（其他）", {})
            if not is_dict_empty(other):
                if other.get("坐位-平卧试验", "") != "":    
                    results.append("坐位-平卧试验：" + other.get("坐位-平卧试验", ""))
                if other.get("坐位-低头试验", "") != "":
                    results.append("坐位-低头试验：" + other.get("坐位-低头试验", ""))
                if other.get("坐位-仰头试验", "") != "":
                    results.append("坐位-仰头试验：" + other.get("坐位-仰头试验", ""))
                if other.get("零平面", "") != "":
                    results.append("零平面: " + other.get("零平面", ""))
            
            # 视跟踪
            tracking = data.get("视跟踪", {})
            if not is_dict_empty(tracking):
                if tracking.get("视跟踪曲线分型", "") != "":    
                    results.append("视跟踪曲线分型: " + tracking.get("视跟踪曲线分型", ""))
                if tracking.get("视跟踪增益", "") != "":
                    results.append("视跟踪增益: " + tracking.get("视跟踪增益", ""))
            
            # 视动性眼震
            okn = data.get("视动性眼震", {})
            if not is_dict_empty(okn):
                if okn.get("水平视标不对称性 (%)", "") != "":
                    results.append("视动性眼震（水平视靶）不对称性 (%): " + okn.get("水平视标不对称性 (%)", ""))
                if okn.get("向右视标增益", "") != "":
                    results.append("视动性眼震增益（向右视靶）: " + okn.get("向右视标增益", ""))
                if okn.get("向左视标增益", "") != "":
                    results.append("视动性眼震增益（向左视靶）: " + okn.get("向左视标增益", ""))
                if okn.get("垂直视标不对称性 (%)", "") != "":
                    results.append("视动性眼震（垂直视靶）不对称性 (%): " + okn.get("垂直视标不对称性 (%)", ""))
                if okn.get("向上视标增益", "") != "":
                    results.append("视动性眼震增益（向上视靶）: " + okn.get("向上视标增益", ""))
                if okn.get("向下视标增益", "") != "":
                    results.append("视动性眼震增益（向下视靶）: " + okn.get("向下视标增益", ""))
                if okn.get("检查结果", "") != "":
                    results.append("视动性眼震检查结果: " + okn.get("检查结果", ""))
        
            # 瘘管试验
            fistula = data.get("瘘管试验", {})
            if not is_dict_empty(fistula):
                fistula_results = fistula.get("瘘管试验", [])
                if fistula_results != []:
                    if isinstance(fistula_results, list):
                        results.append("瘘管试验：" + "、".join(fistula_results))
                    else:
                        results.append("瘘管试验：" + str(fistula_results))
                
            
            # 温度试验
            caloric = data.get("温度试验", {})
            if not is_dict_empty(caloric):
                if caloric.get("单侧减弱侧别 (UW)", "") != "":  
                    results.append("单侧减弱侧别 (UW): " + caloric.get("单侧减弱侧别 (UW)", ""))
                if caloric.get("单侧减弱数值 (UW, %)", "") != "":
                    results.append("单侧减弱数值 (UW, %): " + caloric.get("单侧减弱数值 (UW, %)", ""))
                if caloric.get("优势偏向侧别 (DP)", "") != "":
                    results.append("优势偏向侧别 (DP, 度/秒): " + caloric.get("优势偏向侧别 (DP)", ""))
                if caloric.get("优势偏向数值 (DP, 度/秒)", "") != "":
                    results.append("优势偏向数值 (DP, 度/秒): " + caloric.get("优势偏向数值 (DP, 度/秒)", ""))
                if caloric.get("最大慢相速度总和（右耳，度/秒）", "") != "":
                    results.append("最大慢相速度总和（右耳，度/秒）: " + caloric.get("最大慢相速度总和（右耳, 度/秒）", ""))
                if caloric.get("最大慢相速度总和（左耳，度/秒）", "") != "":
                    results.append("最大慢相速度总和（左耳，度/秒）: " + caloric.get("最大慢相速度总和（左耳, 度/秒）", ""))
                if caloric.get("固视抑制指数 (FI, %)", "") != "":
                    results.append("固视抑制指数 (FI, %): " + caloric.get("固视抑制指数 (FI, %)", ""))
            
            # cVEMP
            cvemp = data.get("颈肌前庭诱发肌源性电位", {})
            if not is_dict_empty(cvemp):
                
                if cvemp.get("右耳声强阈值 (分贝)", "") != "":
                    results.append("声强阈值（cVEMP，右耳，分贝）: " + cvemp.get("右耳声强阈值 (分贝)", ""))
                if cvemp.get("右耳P13波潜伏期 (毫秒)", "") != "":
                    results.append("P13波潜伏期（右耳，毫秒）: " + cvemp.get("右耳P13波潜伏期 (毫秒)", ""))
                if cvemp.get("右耳N23波潜伏期 (毫秒)", "") != "":
                    results.append("N23波潜伏期（右耳，毫秒）: " + cvemp.get("右耳N23波潜伏期 (毫秒)", ""))
                if cvemp.get("右耳P13-N23波间期 (毫秒)", "") != "":
                    results.append("P13-N23波间期（右耳，毫秒）: " + cvemp.get("右耳P13-N23波间期 (毫秒)", ""))
                if cvemp.get("右耳P13波振幅 (微伏)", "") != "":
                    results.append("P13波振幅（右耳，微伏）: " + cvemp.get("右耳P13波振幅 (微伏)", ""))
                if cvemp.get("右耳P13-N23波振幅 (微伏)", "") != "":
                    results.append("P13-N23波振幅（右耳，微伏）: " + cvemp.get("右耳P13-N23波振幅 (微伏)", ""))
                if cvemp.get("左耳声强阈值 (分贝)", "") != "":
                    results.append("声强阈值（cVEMP，左耳，分贝）: " + cvemp.get("左耳声强阈值 (分贝)", ""))
                if cvemp.get("左耳P13波潜伏期 (毫秒)", "") != "":
                    results.append("P13波潜伏期（左耳，毫秒）: " + cvemp.get("左耳P13波潜伏期 (毫秒)", ""))
                if cvemp.get("左耳N23波潜伏期 (毫秒)", "") != "":
                    results.append("N23波潜伏期（左耳，毫秒）: " + cvemp.get("左耳N23波潜伏期 (毫秒)", ""))
                if cvemp.get("左耳P13-N23波间期 (毫秒)", "") != "":
                    results.append("P13-N23波间期（左耳，毫秒）: " + cvemp.get("左耳P13-N23波间期 (毫秒)", ""))
                if cvemp.get("左耳P13波振幅 (微伏)", "") != "":
                    results.append("P13波振幅（左耳，微伏）: " + cvemp.get("左耳P13波振幅 (微伏)", ""))
                if cvemp.get("左耳N23波振幅 (微伏)", "") != "":
                    results.append("N23波振幅（左耳，微伏）: " + cvemp.get("左耳N23波振幅 (微伏)", ""))
                if cvemp.get("左耳P13-N23波振幅 (微伏)", "") != "":
                    results.append("P13-N23波振幅（左耳，微伏）: " + cvemp.get("左耳P13-N23波振幅 (微伏)", ""))
                if cvemp.get("cVEMP耳间不对称比 (%)", "") != "":
                    results.append("cVEMP耳间不对称比 (%): " + cvemp.get("cVEMP耳间不对称比 (%)", ""))
            
            # oVEMP
            ovemp = data.get("眼肌前庭诱发肌源性电位 (oVEMP)", {})
            if not is_dict_empty(ovemp):
                if ovemp.get("右耳声强阈值 (分贝)", "") != "":
                    results.append("声强阈值（oVEMP，右耳，分贝）: " + ovemp.get("右耳声强阈值 (分贝)", ""))
                if ovemp.get("右耳N10波潜伏期 (毫秒)", "") != "":
                    results.append("N10波潜伏期（右耳，毫秒）: " + ovemp.get("右耳N10波潜伏期 (毫秒)", ""))
                if ovemp.get("右耳P15波潜伏期 (毫秒)", "") != "":
                    results.append("P15波潜伏期（右耳，毫秒）: " + ovemp.get("右耳P15波潜伏期 (毫秒)", ""))
                if ovemp.get("右耳N10-P15波间期 (毫秒)", "") != "":
                    results.append("N10-P15波间期（右耳，毫秒）: " + ovemp.get("右耳N10-P15波间期 (毫秒)", ""))
                if ovemp.get("右耳N10波振幅 (微伏)", "") != "":
                    results.append("N10波振幅（右耳，微伏）: " + ovemp.get("右耳N10波振幅 (微伏)", ""))
                if ovemp.get("右耳N10-P15波振幅 (微伏)", "") != "":
                    results.append("N10-P15波振幅（右耳，微伏）: " + ovemp.get("右耳N10-P15波振幅 (微伏)", ""))
                if ovemp.get("左耳声强阈值 (分贝)", "") != "":
                    results.append("声强阈值（oVEMP，左耳，分贝）: " + ovemp.get("左耳声强阈值 (分贝)", ""))
                if ovemp.get("左耳N10波潜伏期 (毫秒)", "") != "":
                    results.append("N10波潜伏期（左耳，毫秒）: " + ovemp.get("左耳N10波潜伏期 (毫秒)", ""))
                if ovemp.get("左耳P15波潜伏期 (毫秒)", "") != "":
                    results.append("P15波潜伏期（左耳，毫秒）: " + ovemp.get("左耳P15波潜伏期 (毫秒)", ""))
                if ovemp.get("左耳N10-P15波间期 (毫秒)", "") != "":
                    results.append("N10-P15波间期（左耳，毫秒）: " + ovemp.get("左耳N10-P15波间期 (毫秒)", ""))
                if ovemp.get("左耳N10波振幅 (微伏)", "") != "":
                    results.append("N10波振幅（左耳，微伏）: " + ovemp.get("左耳N10波振幅 (微伏)", ""))
                if ovemp.get("左耳P15波振幅 (微伏)", "") != "":
                    results.append("P15波振幅（左耳，微伏）: " + ovemp.get("左耳P15波振幅 (微伏)", ""))
                if ovemp.get("左耳N10-P15波振幅 (微伏)", "") != "":
                    results.append("N10-P15波振幅（左耳，微伏）: " + ovemp.get("左耳N10-P15波振幅 (微伏)", ""))
                if ovemp.get("oVEMP耳间不对称性 (%)", "") != "":
                    results.append("oVEMP耳间不对称性 (%): " + ovemp.get("oVEMP耳间不对称性 (%)", ""))
            
            # SVV
            svv = data.get("主观视觉垂直线 (SVV)", {})
            if not is_dict_empty(svv):
                if svv.get("偏斜方向", "") != "":
                    results.append("主观视觉垂直线偏斜方向: " + svv.get("偏斜方向", ""))
                if svv.get("偏斜角度（度）", "") != "":
                    results.append("主观视觉垂直线偏斜角度（度）: " + svv.get("偏斜角度（度）", ""))
                
                
            # 结果中间用;隔开
            results = ';'.join(results)

            return results

# 在主应用程序中使用这个页面的示例
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = "path/to/your/json/file.json"
    edit_page = EditReportPage(root, file_path)
    root.mainloop()
