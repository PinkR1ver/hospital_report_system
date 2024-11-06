def is_dict_empty(d):
    """
    检查字典中的所有值是否为空
    空的定义: None, "", [], {}, 0, "0", "未知", "无"
    返回: True 如果所有值都为空，False 如果存在非空值
    """
    empty_values = [None, "", [], {}, 0, "0", "未知", "无"]
    return all(value in empty_values or (isinstance(value, str) and value.strip() == "") 
              for value in d.values())
