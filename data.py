"""
数据管理模块 - 处理报告数据的保存、加载、数据库操作等
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple


class DataManager:
    """数据管理器 - 负责所有数据相关操作"""
    
    def __init__(self, db_path: str, config: Dict):
        """
        初始化数据管理器
        
        Args:
            db_path: 数据库路径
            config: 系统配置
        """
        self.db_path = db_path
        self.config = config
        self.report_template_config = config.get("report_template", {})
    
    def get_basic_info_page_id(self, load_page_config_func) -> str:
        """
        从pages/index.json中获取基本信息页面ID
        
        Args:
            load_page_config_func: 加载页面配置的函数
            
        Returns:
            基本信息页面ID
        """
        from json_page_renderer import load_page_config
        
        # 读取页面索引
        index_path = os.path.join("pages", "index.json")
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
                pages = index_data.get("pages", [])
        except FileNotFoundError:
            # 如果没有索引文件，从enabled_pages生成
            enabled_pages = self.report_template_config.get("enabled_pages", [])
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
        
        # 优先查找required=true的页面
        for page in pages:
            if page.get("required", False):
                return page["id"]
        
        # 如果没有required的，查找order=1的页面
        for page in pages:
            if page.get("order", 999) == 1:
                return page["id"]
        
        # 默认返回第一个启用的页面
        enabled_pages = [p for p in pages if p.get("enabled", True)]
        if enabled_pages:
            enabled_pages.sort(key=lambda x: x.get("order", 999))
            return enabled_pages[0]["id"]
        
        return "basic_info"
    
    def get_patient_id_key(self, load_page_config_func) -> str:
        """
        从基本信息页面配置中获取患者ID字段的key
        
        Args:
            load_page_config_func: 加载页面配置的函数
            
        Returns:
            患者ID字段的key
        """
        from json_page_renderer import load_page_config
        
        basic_info_page_id = self.get_basic_info_page_id(load_page_config_func)
        page_config = load_page_config(basic_info_page_id)
        if not page_config:
            return "ID"
        
        # 查找患者ID字段（通常命名为ID）
        for section in page_config.get("sections", []):
            for field in section.get("fields", []):
                if field.get("key") == "ID":
                    return "ID"
        
        return "ID"
    
    def generate_exam_findings_text(self, data: Dict) -> str:
        """
        基于各检查页面的结果字段，汇总生成“检查所见”文本（旧版规则的等价实现）
        """
        def is_empty(v: Any) -> bool:
            return v in ("", None, [], {}, "未知", "无", "N/A", "NULL")
        
        # 使用各页面的标题（作为根key）及其结果字段key
        item_to_result_fields: Dict[str, List[str]] = {
            "自发性眼震": ["结果判读"],
            "凝视性眼震": ["凝视性眼震检查结果"],
            "头脉冲试验": ["头脉冲试验检查结果"],
            "头脉冲抑制试验 (SHIMP)": ["头脉冲抑制试验检查结果"],
            "眼位反向偏斜": ["眼位反向偏斜检查结果"],
            "扫视检查": ["扫视检查结果"],
            "视觉增强前庭-眼反射试验": ["检查结果"],
            "前庭-眼反射抑制试验": ["检查结果"],
            "摇头眼震": ["检查结果"],
            "位置试验 (Dix-Hallpike试验)": ["检查结果"],
            "位置试验 (仰卧滚转试验)": ["检查结果"],
            "位置试验(其他)": ["检查结果"],  # 旧版为全角括号，这里使用现有标题
            "视跟踪": ["视跟踪检查结果"],
            "视动性眼震": ["检查结果"],
            "瘘管试验": ["瘘管试验", "检查结果"],  # 优先使用“瘘管试验”复选结果
            "温度试验": ["检查结果"],
            "颈肌前庭诱发肌源性电位 (cVEMP)": ["检查结果"],
            "眼肌前庭诱发肌源性电位 (oVEMP)": ["检查结果"],
            "主观视觉垂直线 (SVV)": ["检查结果"],
        }
        
        findings: List[str] = []
        for item_title, fields in item_to_result_fields.items():
            section = data.get(item_title, {})
            if not isinstance(section, dict) or not section:
                continue
            for field_key in fields:
                value = section.get(field_key, "")
                if is_empty(value):
                    continue
                if isinstance(value, list):
                    value_str = "、".join(str(x) for x in value if not is_empty(x))
                else:
                    value_str = str(value)
                if not is_empty(value_str):
                    findings.append(f"{item_title}：{value_str}")
                    break  # 一个项目命中一个字段即可
        return ";".join(findings)
    
    def collect_page_data(self, pages: Dict) -> Dict:
        """
        收集所有页面的数据
        
        Args:
            pages: 页面字典，key为页面ID，value为页面对象
            
        Returns:
            包含所有页面数据的字典
        """
        data = {}
        
        for page_name, page in pages.items():
            # 跳过数据库管理页面（它不是数据页面）
            if page_name == "database_management":
                continue
            
            # 只处理有get_data方法的页面
            if hasattr(page, 'get_data'):
                try:
                    page_data = page.get_data()
                    if page_data:
                        data.update(page_data)
                except Exception as e:
                    print(f"获取页面 {page_name} 的数据时出错: {e}")
        
        return data
    
    def validate_required_fields(self, data: Dict, basic_info_page_id: str, 
                                 load_page_config_func) -> Tuple[bool, List[str]]:
        """
        验证必需字段是否填写完整
        
        Args:
            data: 收集的数据
            basic_info_page_id: 基本信息页面ID
            load_page_config_func: 加载页面配置的函数
            
        Returns:
            (是否通过验证, 缺失字段列表)
        """
        from json_page_renderer import load_page_config
        
        page_config = load_page_config(basic_info_page_id)
        if not page_config:
            return True, []
        
        # 获取基本信息页面的数据key
        basic_info_key = page_config.get("title") or page_config.get("name") or "基本信息"
        basic_info = data.get(basic_info_key, {})
        
        # 获取必需字段
        required_fields = []
        for section in page_config.get("sections", []):
            for field in section.get("fields", []):
                if field.get("required", False):
                    required_fields.append(field["key"])
        
        # 检查缺失字段
        missing_fields = [field for field in required_fields if not basic_info.get(field)]
        
        return len(missing_fields) == 0, missing_fields
    
    def save_report(self, data: Dict, pages: Dict = None, load_page_config_func = None, 
                    file_path: str = None) -> Tuple[bool, str]:
        """
        保存报告数据
        
        Args:
            data: 要保存的数据（如果为None，则从pages收集）
            pages: 页面字典（可选，如果data为None则需要）
            load_page_config_func: 加载页面配置的函数（可选）
            file_path: 保存的文件路径（可选，如果为None则创建新文件）
            
        Returns:
            (是否成功, 消息或文件路径)
        """
        from json_page_renderer import load_page_config
        
        # 如果data为None，从pages收集数据
        if data is None:
            if pages is None:
                return False, "未提供数据或页面"
            data = self.collect_page_data(pages)
        
        # 如果指定了文件路径，直接保存（编辑现有文件）
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                return True, file_path
            except Exception as e:
                return False, f"保存失败: {str(e)}"
        
        # 否则创建新文件（需要验证）
        if load_page_config_func is None:
            load_page_config_func = load_page_config
        
        # 获取基本信息页面ID
        basic_info_page_id = self.get_basic_info_page_id(load_page_config_func)
        
        # 验证必需字段
        is_valid, missing_fields = self.validate_required_fields(
            data, basic_info_page_id, load_page_config_func
        )
        
        if not is_valid:
            return False, f"以下基本信息字段未填写完整:\n{', '.join(missing_fields)}\n请填写完整后再保存。"
        
        # 获取基本信息页面配置
        basic_info_page_config = load_page_config(basic_info_page_id)
        if not basic_info_page_config:
            return False, "无法加载基本信息页面配置"
        
        basic_info_key = basic_info_page_config.get("title") or basic_info_page_config.get("name") or "基本信息"
        basic_info = data.get(basic_info_key, {})
        
        # 自动补全“检查所见”页面内容（若为空）
        try:
            exam_findings_root = "检查所见"
            exam_findings = data.get(exam_findings_root, {})
            if not isinstance(exam_findings, dict):
                exam_findings = {}
            current_text = exam_findings.get("检查所见", "")
            if not current_text:
                auto_text = self.generate_exam_findings_text(data)
                if auto_text:
                    exam_findings["检查所见"] = auto_text
                    data[exam_findings_root] = exam_findings
        except Exception:
            # 忽略自动补全失败，不影响保存
            pass
        
        # 创建日期文件夹
        current_date = datetime.now().strftime("%Y-%m-%d")
        report_folder = os.path.join(self.db_path, "report", current_date)
        if not os.path.exists(report_folder):
            os.makedirs(report_folder, exist_ok=True)
        
        # 获取患者ID
        patient_id_key = self.get_patient_id_key(load_page_config_func)
        patient_id = basic_info.get(patient_id_key, "unknown")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{patient_id}_{timestamp}.json"
        
        # 完整的文件路径
        file_path = os.path.join(report_folder, filename)
        
        # 保存数据到文件
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True, file_path
        except Exception as e:
            return False, f"保存失败: {str(e)}"
    
    def load_report(self, file_path: str) -> Optional[Dict]:
        """
        加载报告数据
        
        Args:
            file_path: JSON文件路径
            
        Returns:
            报告数据字典，如果加载失败返回None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载报告失败 {file_path}: {e}")
            return None
    
    def delete_report(self, file_path: str) -> Tuple[bool, str]:
        """
        删除报告
        
        Args:
            file_path: 报告文件路径
            
        Returns:
            (是否成功, 消息)
        """
        if not os.path.exists(file_path):
            return False, "报告文件不存在"
        
        try:
            os.remove(file_path)
            return True, "报告已删除"
        except Exception as e:
            return False, f"删除失败: {str(e)}"
    
    def list_reports(self, basic_info_key: str = "基本信息") -> List[Dict]:
        """
        列出所有报告
        
        Args:
            basic_info_key: 基本信息在JSON中的key
            
        Returns:
            报告列表，每个报告包含 file_path, patient_id, name, exam_time, data
        """
        reports = []
        report_folder = os.path.join(self.db_path, "report")
        
        if not os.path.exists(report_folder):
            return reports
        
        # 遍历所有日期文件夹
        for date_folder in sorted(os.listdir(report_folder), reverse=True):
            date_path = os.path.join(report_folder, date_folder)
            if os.path.isdir(date_path):
                for report_file in sorted(os.listdir(date_path), reverse=True):
                    if report_file.endswith('.json'):
                        file_path = os.path.join(date_path, report_file)
                        data = self.load_report(file_path)
                        if data:
                            basic_info = data.get(basic_info_key, {})
                            reports.append({
                                'file_path': file_path,
                                'patient_id': basic_info.get("ID", "未知"),
                                'name': basic_info.get("姓名", "未知"),
                                'exam_time': basic_info.get("检查时间", "未知"),
                                'data': data
                            })
        
        return reports
    
    def search_reports(self, search_text: str, basic_info_key: str = "基本信息") -> List[Dict]:
        """
        搜索报告
        
        Args:
            search_text: 搜索关键词
            basic_info_key: 基本信息在JSON中的key
            
        Returns:
            匹配的报告列表
        """
        all_reports = self.list_reports(basic_info_key)
        search_text_lower = search_text.lower()
        
        filtered_reports = []
        for report in all_reports:
            if (search_text_lower in report['patient_id'].lower() or
                search_text_lower in report['name'].lower() or
                search_text_lower in report['exam_time'].lower() or
                search_text_lower in report['file_path'].lower()):
                filtered_reports.append(report)
        
        return filtered_reports

