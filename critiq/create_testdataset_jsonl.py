import json
import pandas as pd
import os

# 输入和输出路径
input_jsonl = r'D:\\code\\count\\jsonl\\base\\0419.jsonl'
output_jsonl = r'D:\\code\\count\\jsonl\\base\\0714.jsonl'
yue_jsonl = r'D:\\code\\count\\jsonl\\base\\0714_yue.jsonl'
common_jsonl = r'D:\\code\\count\\jsonl\\base\\0714_common.jsonl'

# 读取原始 JSONL 文件
with open(input_jsonl, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 构造新数据
converted_data = []
converted_yue = []
converted_common = []
for line in lines:
    data = json.loads(line.strip())
    zh_query = data.get("zh_query", "")
    dialect_query = data.get("dialect_query", "")
    dialect_type = data.get("dialect_type", "")

    # 构建文本格式
    if dialect_type == "粤语":
        text = f"普通话‘{zh_query}’的{dialect_type}话翻译是‘{dialect_query}’"
        if zh_query == dialect_query:
            converted_common.append(json.dumps({"text": text}, ensure_ascii=False))
        else:
            converted_yue.append(json.dumps({"text": text}, ensure_ascii=False))
    else:
        text = f"普通话‘{zh_query}’的{dialect_type}翻译是‘{dialect_query}’"
        converted_data.append(json.dumps({"text": text}, ensure_ascii=False))

# 写入新的 JSONL 文件
os.makedirs(os.path.dirname(output_jsonl), exist_ok=True)
with open(output_jsonl, 'w', encoding='utf-8') as f:
    f.write('\n'.join(converted_data))

os.makedirs(os.path.dirname(yue_jsonl), exist_ok=True)
with open(yue_jsonl, 'w', encoding='utf-8') as f:
    f.write('\n'.join(converted_yue))

os.makedirs(os.path.dirname(common_jsonl), exist_ok=True)
with open(common_jsonl, 'w', encoding='utf-8') as f:
    f.write('\n'.join(converted_common))
print(f"✅ 已生成测试集：{output_jsonl}")