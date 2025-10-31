#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
读取Excel文件内容的脚本
用于分析前庭功能检查报告的新设计说明
"""

import pandas as pd
import os
import sys

def read_excel_file(file_path):
    """读取Excel文件的所有工作表内容"""
    try:
        # 读取Excel文件的所有工作表
        excel_file = pd.ExcelFile(file_path)
        print(f"\n=== 文件: {os.path.basename(file_path)} ===")
        print(f"工作表列表: {excel_file.sheet_names}")
        
        for sheet_name in excel_file.sheet_names:
            print(f"\n--- 工作表: {sheet_name} ---")
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # 显示基本信息
            print(f"行数: {len(df)}, 列数: {len(df.columns)}")
            print(f"列名: {list(df.columns)}")
            
            # 显示前几行数据
            print("\n前5行数据:")
            print(df.head().to_string())
            
            # 如果有空值，显示空值统计
            if df.isnull().any().any():
                print("\n空值统计:")
                print(df.isnull().sum())
            
            print("\n" + "="*50)
            
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")

def main():
    # 要读取的Excel文件列表
    excel_files = [
        "前庭功能检查子模块设计和填写说明.xlsx",
        "新前庭功能检查模板报告生成样板20251012(1).xlsx"
    ]
    
    for file_path in excel_files:
        if os.path.exists(file_path):
            read_excel_file(file_path)
        else:
            print(f"文件不存在: {file_path}")

if __name__ == "__main__":
    main()
