import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import base64

def get_download_link(data, filename, text):
    json_string = json.dumps(data, ensure_ascii=False, indent=2)
    b64 = base64.b64encode(json_string.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="{filename}">{text}</a>'
    return href



if __name__ == "__main__":

    st.set_page_config(page_title="Vestibular Function Test Report", page_icon="🧊")
    
    st.title("前庭功能检测报告单")

    # 基本信息
    st.header("基本信息")
    col1, col2, col3 = st.columns(3)
    with col1:
        reg_number = st.text_input("登记号/住院号")
        name = st.text_input("姓名")
    with col2:
        gender = st.text_input("性别")
        age = st.number_input("年龄", min_value=0, max_value=120)
    with col3:
        medical_order = st.text_input("医嘱项目")
        test_device = st.text_input("测试设备")
    test_date = st.date_input("检查日期")

    # Dix-Hallpike试验
    st.header("Dix-Hallpike试验眼震观察")
    tab1, tab2 = st.tabs(["右耳向下", "左耳向下"])

    def dix_hallpike_form(ear):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("躺下")
            lying_up = st.selectbox(f"{ear}躺下向天", ["", "向天", "向地", "其他类型眼震", "无眼震"])
            lying_down = st.selectbox(f"{ear}躺下向地", ["", "向天", "向地", "其他类型眼震", "无眼震"])
        with col2:
            st.subheader("重新坐起")
            sitting_reverse = st.selectbox(f"{ear}坐起反向", ["", "反向", "同向", "其他类型眼震", "无眼震"])
            sitting_same = st.selectbox(f"{ear}坐起同向", ["", "反向", "同向", "其他类型眼震", "无眼震"])
        
        vertigo = st.checkbox(f"{ear}眩晕出现")
        latency = st.number_input(f"{ear}潜伏期(秒)", min_value=0)
        duration = st.number_input(f"{ear}持续时间(秒)", min_value=0)
        fatigue = st.checkbox(f"{ear}易疲劳性")
        
        return {
            "躺下向天": lying_up,
            "躺下向地": lying_down,
            "坐起反向": sitting_reverse,
            "坐起同向": sitting_same,
            "眩晕出现": vertigo,
            "潜伏期": latency,
            "持续时间": duration,
            "易疲劳性": fatigue
        }

    with tab1:
        right_ear_data = dix_hallpike_form("右耳")
    with tab2:
        left_ear_data = dix_hallpike_form("左耳")

    # 滚转试验
    st.header("滚转试验(Rolling test)眼震观察")
    tab3, tab4 = st.tabs(["向右侧偏头", "向左侧偏头"])

    def rolling_test_form(direction):
        to_left = st.selectbox(f"{direction}向左", ["", "向左", "向右", "其他类型眼震", "无眼震"])
        to_right = st.selectbox(f"{direction}向右", ["", "向左", "向右", "其他类型眼震", "无眼震"])
        vertigo = st.checkbox(f"{direction}眩晕出现")
        latency = st.number_input(f"{direction}潜伏期(秒)", min_value=0)
        duration = st.number_input(f"{direction}持续时间(秒)", min_value=0)
        fatigue = st.checkbox(f"{direction}易疲劳性")
        
        return {
            "向左": to_left,
            "向右": to_right,
            "眩晕出现": vertigo,
            "潜伏期": latency,
            "持续时间": duration,
            "易疲劳性": fatigue
        }

    with tab3:
        right_side_data = rolling_test_form("右侧")
    with tab4:
        left_side_data = rolling_test_form("左侧")

    # 手法复位
    st.header("手法复位")
    reposition = st.radio("是否进行手法复位", ["未进行", "已进行"])
    reposition_method = st.text_input("复位方法")

    # 结论和建议
    st.header("结论和建议")
    conclusion = st.text_area("结论")
    recommendation = st.text_area("建议")

    # 检查者
    examiner = st.text_input("检查者")

    if st.button("提交报告"):
        report_data = {
            "基本信息": {
                "登记号/住院号": reg_number,
                "姓名": name,
                "性别": gender,
                "年龄": age,
                "医嘱项目": medical_order,
                "测试设备": test_device,
                "检查日期": str(test_date)
            },
            "Dix-Hallpike试验": {
                "右耳向下": right_ear_data,
                "左耳向下": left_ear_data
            },
            "滚转试验": {
                "向右侧偏头": right_side_data,
                "向左侧偏头": left_side_data
            },
            "手法复位": {
                "是否进行": reposition,
                "复位方法": reposition_method
            },
            "结论": conclusion,
            "建议": recommendation,
            "检查者": examiner
        }
        
        st.success("报告已成功提交!")
        
        # 生成下载链接
        st.markdown(get_download_link(report_data, "vestibular_function_report.json", "点击此处下载JSON报告"), unsafe_allow_html=True)
    
