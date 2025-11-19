# Excel报告生成器 - 配置说明

## 概述

这是一个基于JSON配置文件的Excel报告生成系统，完全通过配置文件控制Excel的生成逻辑，无需修改Python代码。

## 文件结构

所有模板相关文件都存放在数据库的 `templates/` 目录下：

```
vest_database/
  templates/
    templates_index.json          # 模板索引文件（列出所有可用模板）
    default_template_config.json   # 默认模板配置文件
    template1_config.json         # 其他模板配置文件
    template2_config.json
    ...
```

## 模板管理

### 模板索引 (templates_index.json)

模板索引文件定义了所有可用的Excel报告模板：

```json
{
  "description": "Excel报告模板索引",
  "version": "1.0.0",
  "default_template": "default_template",
  "templates": [
    {
      "id": "default_template",
      "name": "默认模板",
      "description": "标准前庭功能检查报告模板",
      "config_file": "default_template_config.json",
      "template_file": "template/report_template.xlsx",
      "enabled": true
    }
  ]
}
```

### 添加新模板

1. 在 `vest_database/templates/` 目录下创建新的配置文件（如 `custom_template_config.json`）
2. 在 `templates_index.json` 中添加新模板条目
3. 使用模板ID加载对应的模板

### 使用多个模板

```python
# 使用默认模板
generator = ExcelGenerator(database_path="vest_database")

# 使用指定模板
generator = ExcelGenerator(
    database_path="vest_database", 
    template_id="custom_template"
)
```

## 配置文件结构

### 顶层配置

```json
{
  "description": "Excel报告生成模板配置",
  "version": "1.0.0",
  "template_file": "template/report_template.xlsx",  // Excel模板文件路径
  "output_directory": "vest_database/excel",          // 输出目录
  "worksheets": [...],                                // 工作表配置数组
  "styles": {...},                                     // 样式定义
  "data_formatters": {...},                           // 数据格式化配置
  "empty_value_handling": {...}                       // 空值处理配置
}
```

### 工作表配置 (worksheets)

每个工作表包含：
- `name`: 工作表名称
- `index`: 工作表索引（0开始）
- `page_setup`: 页面设置（打印方向、页边距、打印区域等）
- `sections`: 数据区域配置数组

### Section类型

#### 1. fixed (固定位置)
```json
{
  "name": "基本信息",
  "type": "fixed",
  "start_row": 3,        // 固定的起始行
  "cells": [...]         // 单元格配置数组
}
```

#### 2. conditional (条件显示)
```json
{
  "name": "自发性眼震",
  "type": "conditional",
  "condition": {
    "check_empty": "自发性眼震",    // 检查的数据路径
    "skip_if_empty": true          // 如果为空则跳过整个section
  },
  "dynamic_start_row": {
    "base": 6,
    "previous_section": "基本信息"  // 从上一个section结束处开始
  },
  "layout": [...]                  // 布局配置
}
```

### Layout布局配置

Layout支持三种类型：

#### 1. section_title (节标题)
```json
{
  "row_offset": 0,
  "type": "section_title",
  "merge_range": "A{row}:M{row}",  // 合并单元格范围，{row}会被替换为当前行
  "text": "自发性眼震 (spontaneous nystagmus)",
  "style": "section_title"
}
```

#### 2. header_row / data_row (表头行/数据行)
```json
{
  "row_offset": 1,
  "type": "header_row",
  "cells": [
    {
      "merge_range": "A{row}:C{row}",
      "text": "模式",               // 固定文本
      "style": "header"
    },
    {
      "merge_range": "D{row}:F{row}",
      "data_path": "自发性眼震.自发性眼震模式",  // 数据路径
      "format": "text",             // 格式化类型
      "style": "data_cell"
    }
  ]
}
```

#### 3. spacer (间距)
```json
{
  "row_offset": 3,
  "type": "spacer",
  "height": 1  // 空行数
}
```

### 数据路径 (data_path)

支持嵌套路径，使用点号分隔：
- `基本信息.ID` → `data["基本信息"]["ID"]`
- `自发性眼震.自发性眼震模式` → `data["自发性眼震"]["自发性眼震模式"]`

### 样式配置 (styles)

```json
{
  "section_title": {
    "font": {
      "name": "宋体",
      "size": 12,
      "bold": true
    },
    "fill": {
      "type": "solid",
      "color": "F0F0F0"  // RGB颜色（无#号）
    },
    "alignment": {
      "horizontal": "left",
      "vertical": "center"
    },
    "border": {
      "all": "thin",
      "color": "000000"
    }
  }
}
```

### 数据格式化 (data_formatters)

```json
{
  "date": {
    "input_format": "%Y/%m/%d",
    "output_format": "%Y/%m/%d"
  },
  "number": {
    "decimal_places": 2
  },
  "list": {
    "separator": "、",
    "join": true
  }
}
```

## 使用示例

### Python代码

```python
from excel_generator import ExcelGenerator

# 方式1: 从数据库templates目录加载（推荐）
generator = ExcelGenerator(
    database_path="vest_database",
    template_id="default_template"  # 可选，不指定则使用默认模板
)

# 方式2: 直接指定配置文件路径
generator = ExcelGenerator(
    config_path="vest_database/templates/custom_template_config.json"
)

# 准备JSON数据（与页面保存的JSON格式一致）
json_data = {
    "基本信息": {
        "ID": "12345",
        "姓名": "张三",
        "性别": "男",
        "出生日期": "1990/01/01",
        "检查时间": "2025/01/15",
        "检查设备": "设备A"
    },
    "自发性眼震": {
        "自发性眼震模式": "右跳性眼震",
        "自发性眼震速度": "5.2",
        "自发性眼震固视抑制": "正常",
        "自发性眼震检查结果": "异常"
    }
}

# 生成Excel
output_path = generator.generate(json_data)
print(f"Excel已生成: {output_path}")
```

## 高级功能

### 1. 条件显示
通过 `condition.skip_if_empty` 控制section是否显示：
```json
{
  "condition": {
    "check_empty": "自发性眼震",
    "skip_if_empty": true
  }
}
```

### 2. 动态行号
使用 `{row}` 占位符和 `row_offset` 实现动态布局：
```json
{
  "merge_range": "A{row}:C{row}",
  "row_offset": 1
}
```

### 3. 列表数据格式化
如果数据是列表，自动使用分隔符连接：
```json
{
  "data_path": "头脉冲试验.头脉冲试验检查结果",
  "format": "list"
}
```

### 4. 空值处理
自动处理空值，可配置默认值：
```json
{
  "empty_value_handling": {
    "default": "",
    "check_empty_values": ["", null, [], {}, "未知", "无", "N/A"]
  }
}
```

## 配置优势

1. **完全配置化**：无需修改Python代码，只需修改JSON配置文件
2. **灵活布局**：支持固定位置、动态位置、条件显示
3. **样式统一**：通过样式配置统一管理外观
4. **易于维护**：配置结构清晰，易于理解和修改
5. **扩展性强**：可以轻松添加新的section、样式、格式化规则

## 注意事项

1. 确保Excel模板文件存在且格式正确
2. JSON数据路径必须与配置文件中的 `data_path` 匹配
3. 样式名称必须在 `styles` 中定义
4. 合并单元格范围使用Excel标准格式（如 `A1:C1`）
5. 动态行号使用 `{row}` 占位符，会在运行时替换

## 后续扩展建议

1. 支持图片插入（已在配置中预留）
2. 支持公式计算
3. 支持图表生成
4. 支持多语言
5. 支持模板变量（如日期、时间戳等）

