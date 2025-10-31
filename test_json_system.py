#!/usr/bin/env python3
"""
测试JSON驱动的页面系统
"""

import json
import os
import sys

def test_json_structure():
    """测试JSON文件结构"""
    print("🔍 测试JSON文件结构...")
    
    # 测试basic_info.json
    json_path = "pages/basic_info.json"
    if not os.path.exists(json_path):
        print(f"❌ JSON文件不存在: {json_path}")
        return False
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 检查必要字段
        required_fields = ['page_id', 'title', 'sections']
        for field in required_fields:
            if field not in config:
                print(f"❌ 缺少必要字段: {field}")
                return False
        
        print("✅ JSON文件结构正确")
        
        # 检查sections
        sections = config.get('sections', [])
        if not sections:
            print("❌ 没有定义sections")
            return False
        
        print(f"✅ 找到 {len(sections)} 个sections")
        
        # 检查fields
        total_fields = 0
        for section in sections:
            fields = section.get('fields', [])
            total_fields += len(fields)
            print(f"  - {section.get('name', 'Unknown')}: {len(fields)} 个字段")
        
        print(f"✅ 总共 {total_fields} 个字段")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON格式错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def test_renderer_import():
    """测试渲染器导入"""
    print("🔍 测试页面渲染器导入...")
    
    try:
        from pages.json_page_renderer import JSONPageRenderer, load_page_config
        print("✅ JSONPageRenderer 导入成功")
        
        # 测试加载配置
        config = load_page_config("basic_info")
        if config:
            print("✅ 页面配置加载成功")
            return True
        else:
            print("❌ 页面配置加载失败")
            return False
            
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def test_main_import():
    """测试主程序导入"""
    print("🔍 测试主程序导入...")
    
    try:
        import main
        print("✅ main.py 导入成功")
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 50)
    print("JSON驱动页面系统 - 测试脚本")
    print("=" * 50)
    
    tests = [
        ("JSON文件结构测试", test_json_structure),
        ("页面渲染器测试", test_renderer_import),
        ("主程序导入测试", test_main_import)
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
        print("🎉 所有测试通过！JSON驱动系统工作正常。")
        print("\n运行命令: python main.py")
        return True
    else:
        print("⚠️  部分测试失败，请检查上述错误信息。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

