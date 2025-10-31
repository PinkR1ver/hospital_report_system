#!/usr/bin/env python3
"""
测试脚本 - 验证前庭功能检查报告系统 v2.0
"""

import json
import os
import sys
from datetime import datetime

def test_config_file():
    """测试配置文件格式"""
    print("🔍 测试配置文件...")
    
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 检查必要的配置项
        required_sections = ['system', 'database', 'pages', 'report_template']
        for section in required_sections:
            if section not in config:
                print(f"❌ 缺少配置节: {section}")
                return False
        
        print("✅ 配置文件格式正确")
        return True
        
    except FileNotFoundError:
        print("❌ 配置文件不存在")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ 配置文件JSON格式错误: {e}")
        return False

def test_dependencies():
    """测试依赖包"""
    print("🔍 测试依赖包...")
    
    required_packages = [
        'customtkinter',
        'tkcalendar', 
        'reportlab',
        'cryptography',
        'openpyxl',
        'pandas',
        'pillow',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    print("✅ 所有依赖包已安装")
    return True

def test_directory_structure():
    """测试目录结构"""
    print("🔍 测试目录结构...")
    
    required_dirs = ['pages']
    required_files = ['main.py', 'config.json', 'requirements.txt']
    
    # 检查目录
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            print(f"❌ 缺少目录: {dir_name}")
            return False
        print(f"✅ 目录存在: {dir_name}")
    
    # 检查文件
    for file_name in required_files:
        if not os.path.exists(file_name):
            print(f"❌ 缺少文件: {file_name}")
            return False
        print(f"✅ 文件存在: {file_name}")
    
    # 检查页面模块
    page_files = ['pages/__init__.py', 'pages/basic_info_page.py']
    for file_name in page_files:
        if not os.path.exists(file_name):
            print(f"❌ 缺少页面文件: {file_name}")
            return False
        print(f"✅ 页面文件存在: {file_name}")
    
    print("✅ 目录结构正确")
    return True

def test_import_modules():
    """测试模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        # 测试主模块导入
        import main
        print("✅ main.py 导入成功")
        
        # 测试页面模块导入
        from pages.basic_info_page import BasicInfoPage
        print("✅ basic_info_page.py 导入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("前庭功能检查报告系统 v2.0 - 测试脚本")
    print("=" * 50)
    
    tests = [
        ("配置文件测试", test_config_file),
        ("依赖包测试", test_dependencies),
        ("目录结构测试", test_directory_structure),
        ("模块导入测试", test_import_modules)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} 失败")
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统可以正常运行。")
        print("\n运行命令: python main.py")
        return True
    else:
        print("⚠️  部分测试失败，请检查上述错误信息。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

