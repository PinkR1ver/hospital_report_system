import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

class BasicInfoPage(ttk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)

        # 患者基本信息部分
        patient_info_frame = ttk.LabelFrame(main_frame, text="患者基本信息", padding="10 10 10 10")
        patient_info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        patient_info_frame.columnconfigure(1, weight=1)
        patient_info_frame.columnconfigure(3, weight=1)

        # ID
        ttk.Label(patient_info_frame, text="ID:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.id_entry = ttk.Entry(patient_info_frame)
        self.id_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 姓名
        ttk.Label(patient_info_frame, text="姓名:").grid(row=0, column=2, sticky=tk.E, padx=5, pady=5)
        self.name_entry = ttk.Entry(patient_info_frame)
        self.name_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 性别
        ttk.Label(patient_info_frame, text="性别:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.gender_var = tk.StringVar()
        self.gender_combobox = ttk.Combobox(patient_info_frame, textvariable=self.gender_var, values=["", "男", "女"])
        self.gender_combobox.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 出生日期
        ttk.Label(patient_info_frame, text="出生日期:").grid(row=1, column=2, sticky=tk.E, padx=5, pady=5)
        self.birth_date = DateEntry(patient_info_frame, width=12, background='darkblue', foreground='white', 
                                    borderwidth=2, date_pattern='yyyy/mm/dd', showweeknumbers=False)
        self.birth_date.delete(0, tk.END)  # 删除默认日期
        self.birth_date.grid(row=1, column=3, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 检查信息部分
        exam_info_frame = ttk.LabelFrame(main_frame, text="检查信息", padding="10 10 10 10")
        exam_info_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        exam_info_frame.columnconfigure(1, weight=1)
        exam_info_frame.columnconfigure(3, weight=1)

        # 检查项目
        ttk.Label(exam_info_frame, text="检查项目:").grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.exam_type_var = tk.StringVar()
        self.exam_type_combobox = ttk.Combobox(exam_info_frame, textvariable=self.exam_type_var, values=["", "前庭报告-1", "前庭报告-2", "前庭报告-3"])
        self.exam_type_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 检查时间
        ttk.Label(exam_info_frame, text="检查时间:").grid(row=0, column=2, sticky=tk.E, padx=5, pady=5)
        self.exam_date = DateEntry(exam_info_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy/mm/dd')
        self.exam_date.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 检查医生
        ttk.Label(exam_info_frame, text="检查医生:").grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.doctor_var = tk.StringVar()
        self.doctor_combobox = ttk.Combobox(exam_info_frame, textvariable=self.doctor_var, 
                                            values=["", "任文磊", "付敏郡", "刘译升", "郑郭嫄", "王锦雪", "唐沛", "吕志军", "赵晓瑜", "朱璐"])
        self.doctor_combobox.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # 检查设备
        ttk.Label(exam_info_frame, text="检查设备:").grid(row=1, column=2, sticky=tk.E, padx=5, pady=5)
        self.equipment_var = tk.StringVar()
        self.equipment_combobox = ttk.Combobox(exam_info_frame, textvariable=self.equipment_var, 
                                               values=["", "Otometrics", "ZEHINT", "Interacoustics"])
        self.equipment_combobox.grid(row=1, column=3, sticky=(tk.W, tk.E), padx=5, pady=5)

    def get_data(self):
        birth_date = self.birth_date.get_date() if self.birth_date.get() else None
        return {
            "基本信息": {
                "ID": self.id_entry.get(),
                "姓名": self.name_entry.get(),
                "性别": self.gender_var.get(),
                "出生日期": birth_date.strftime("%Y/%m/%d") if birth_date else "",
                "检查项目": self.exam_type_var.get(),
                "检查时间": self.exam_date.get_date().strftime("%Y/%m/%d"),
                "检查医生": self.doctor_var.get(),
                "检查设备": self.equipment_var.get()
            }
        }

    def set_data(self, data):
        self.id_entry.delete(0, tk.END)
        self.id_entry.insert(0, data.get("ID", ""))
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, data.get("姓名", ""))
        self.gender_var.set(data.get("性别", ""))
        self.birth_date.set_date(data.get("出生日期", ""))
        self.exam_type_var.set(data.get("检查项目", ""))
        self.exam_date.set_date(data.get("检查时间", ""))
        self.doctor_var.set(data.get("检查医生", ""))
        self.equipment_var.set(data.get("检查设备", ""))
