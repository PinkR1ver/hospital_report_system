import flet as ft
import json
from datetime import date
import os

def main(page: ft.Page):
    page.title = "前庭功能检测报告单"
    page.scroll = "auto"

    # 基本信息
    reg_number = ft.TextField(label="登记号/住院号")
    name = ft.TextField(label="姓名")
    gender = ft.TextField(label="性别")
    age = ft.TextField(label="年龄", input_filter=ft.NumbersOnlyInputFilter())
    medical_order = ft.TextField(label="医嘱项目")
    test_device = ft.TextField(label="测试设备")
    
    test_date = ft.DatePicker(
        on_change=lambda e: setattr(test_date_text, 'value', e.date.strftime("%Y-%m-%d") if e.date else "")
    )
    page.overlay.append(test_date)
    test_date_text = ft.Text()

    def open_date_picker(e):
        test_date.open = True
        page.update()

    # Dix-Hallpike试验
    def create_dix_hallpike_form(ear):
        return ft.Column([
            ft.Text(f"{ear}耳向下", style=ft.TextThemeStyle.TITLE_MEDIUM),
            ft.Dropdown(label="躺下向天", options=[ft.dropdown.Option(x) for x in ["", "向天", "向地", "其他类型眼震", "无眼震"]]),
            ft.Dropdown(label="躺下向地", options=[ft.dropdown.Option(x) for x in ["", "向天", "向地", "其他类型眼震", "无眼震"]]),
            ft.Dropdown(label="坐起反向", options=[ft.dropdown.Option(x) for x in ["", "反向", "同向", "其他类型眼震", "无眼震"]]),
            ft.Dropdown(label="坐起同向", options=[ft.dropdown.Option(x) for x in ["", "反向", "同向", "其他类型眼震", "无眼震"]]),
            ft.Checkbox(label="眩晕出现"),
            ft.TextField(label="潜伏期(秒)", input_filter=ft.NumbersOnlyInputFilter()),
            ft.TextField(label="持续时间(秒)", input_filter=ft.NumbersOnlyInputFilter()),
            ft.Checkbox(label="易疲劳性"),
        ])

    right_ear_form = create_dix_hallpike_form("右")
    left_ear_form = create_dix_hallpike_form("左")

    # 滚转试验
    def create_rolling_test_form(direction):
        return ft.Column([
            ft.Text(f"{direction}侧偏头", style=ft.TextThemeStyle.TITLE_MEDIUM),
            ft.Dropdown(label="向左", options=[ft.dropdown.Option(x) for x in ["", "向左", "向右", "其他类型眼震", "无眼震"]]),
            ft.Dropdown(label="向右", options=[ft.dropdown.Option(x) for x in ["", "向左", "向右", "其他类型眼震", "无眼震"]]),
            ft.Checkbox(label="眩晕出现"),
            ft.TextField(label="潜伏期(秒)", input_filter=ft.NumbersOnlyInputFilter()),
            ft.TextField(label="持续时间(秒)", input_filter=ft.NumbersOnlyInputFilter()),
            ft.Checkbox(label="易疲劳性"),
        ])

    right_side_form = create_rolling_test_form("右")
    left_side_form = create_rolling_test_form("左")

    # 手法复位
    reposition = ft.RadioGroup(content=ft.Column([
        ft.Radio(value="未进行", label="未进行"),
        ft.Radio(value="已进行", label="已进行"),
    ]))
    reposition_method = ft.TextField(label="复位方法")

    # 结论和建议
    conclusion = ft.TextField(label="结论", multiline=True)
    recommendation = ft.TextField(label="建议", multiline=True)

    # 检查者
    examiner = ft.TextField(label="检查者")

    def get_report_data():
        return {
            "基本信息": {
                "登记号/住院号": reg_number.value,
                "姓名": name.value,
                "性别": gender.value,
                "年龄": age.value,
                "医嘱项目": medical_order.value,
                "测试设备": test_device.value,
                "检查日期": test_date_text.value
            },
            "Dix-Hallpike试验": {
                "右耳向下": {control.label: control.value for control in right_ear_form.controls if hasattr(control, 'label')},
                "左耳向下": {control.label: control.value for control in left_ear_form.controls if hasattr(control, 'label')}
            },
            "滚转试验": {
                "向右侧偏头": {control.label: control.value for control in right_side_form.controls if hasattr(control, 'label')},
                "向左侧偏头": {control.label: control.value for control in left_side_form.controls if hasattr(control, 'label')}
            },
            "手法复位": {
                "是否进行": reposition.value,
                "复位方法": reposition_method.value
            },
            "结论": conclusion.value,
            "建议": recommendation.value,
            "检查者": examiner.value
        }

    def save_report(e):
        save_path = ft.FilePicker(dialog_title="保存报告")
        save_path.save_file(
            dialog_title="保存报告",
            file_name="vestibular_function_report.json",
            allowed_extensions=["json"]
        )
        page.overlay.append(save_path)
        page.update()

        def save_file_result(e: ft.FilePickerResultEvent):
            if e.path:
                report_data = get_report_data()
                with open(e.path, "w", encoding="utf-8") as f:
                    json.dump(report_data, f, ensure_ascii=False, indent=2)
                page.show_snack_bar(ft.SnackBar(content=ft.Text(f"报告已保存到: {e.path}")))
            else:
                page.show_snack_bar(ft.SnackBar(content=ft.Text("保存取消")))

        save_path.on_result = save_file_result
        page.update()

    def load_report(e):
        load_path = ft.FilePicker(dialog_title="打开报告")
        load_path.pick_files(dialog_title="打开报告", allowed_extensions=["json"])
        page.overlay.append(load_path)
        page.update()

        def load_file_result(e: ft.FilePickerResultEvent):
            if e.files and len(e.files) > 0:
                file_path = e.files[0].path
                with open(file_path, "r", encoding="utf-8") as f:
                    report_data = json.load(f)
                
                # 填充表单数据
                reg_number.value = report_data["基本信息"]["登记号/住院号"]
                name.value = report_data["基本信息"]["姓名"]
                gender.value = report_data["基本信息"]["性别"]
                age.value = report_data["基本信息"]["年龄"]
                medical_order.value = report_data["基本信息"]["医嘱项目"]
                test_device.value = report_data["基本信息"]["测试设备"]
                test_date_text.value = report_data["基本信息"]["检查日期"]

                # 填充Dix-Hallpike试验数据
                for ear, form in [("右耳向下", right_ear_form), ("左耳向下", left_ear_form)]:
                    for control in form.controls:
                        if hasattr(control, 'label') and control.label in report_data["Dix-Hallpike试验"][ear]:
                            control.value = report_data["Dix-Hallpike试验"][ear][control.label]

                # 填充滚转试验数据
                for direction, form in [("向右侧偏头", right_side_form), ("向左侧偏头", left_side_form)]:
                    for control in form.controls:
                        if hasattr(control, 'label') and control.label in report_data["滚转试验"][direction]:
                            control.value = report_data["滚转试验"][direction][control.label]

                # 填充手法复位数据
                reposition.value = report_data["手法复位"]["是否进行"]
                reposition_method.value = report_data["手法复位"]["复位方法"]

                conclusion.value = report_data["结论"]
                recommendation.value = report_data["建议"]
                examiner.value = report_data["检查者"]

                page.show_snack_bar(ft.SnackBar(content=ft.Text(f"报告已从 {file_path} 加载")))
                page.update()
            else:
                page.show_snack_bar(ft.SnackBar(content=ft.Text("打开取消")))

        load_path.on_result = load_file_result
        page.update()

    save_button = ft.ElevatedButton("保存报告", on_click=save_report)
    load_button = ft.ElevatedButton("打开报告", on_click=load_report)

    page.add(
        ft.Text("前庭功能检测报告单", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
        ft.Text("基本信息", style=ft.TextThemeStyle.TITLE_MEDIUM),
        reg_number, name, gender, age, medical_order, test_device,
        ft.Row([ft.Text("检查日期: "), test_date_text, ft.ElevatedButton("选择日期", on_click=open_date_picker)]),
        ft.Text("Dix-Hallpike试验", style=ft.TextThemeStyle.TITLE_MEDIUM),
        ft.Row([right_ear_form, left_ear_form]),
        ft.Text("滚转试验", style=ft.TextThemeStyle.TITLE_MEDIUM),
        ft.Row([right_side_form, left_side_form]),
        ft.Text("手法复位", style=ft.TextThemeStyle.TITLE_MEDIUM),
        reposition, reposition_method,
        ft.Text("结论和建议", style=ft.TextThemeStyle.TITLE_MEDIUM),
        conclusion, recommendation,
        ft.Text("检查者", style=ft.TextThemeStyle.TITLE_MEDIUM),
        examiner,
        ft.Row([save_button, load_button])
    )

ft.app(target=main)