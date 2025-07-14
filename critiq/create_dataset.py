import pandas as pd
import json

# 配置文件路径
file1 = 'D:\\code\\count\\dataset\\badcase_train.xlsx'
file2 = 'D:\\code\\count\\dataset\\badcase_test.xlsx'

train_output_jsonl = 'D:\\code\\count\\jsonl\\badcase_train.jsonl'
test_output_jsonl = 'D:\\code\\count\\jsonl\\badcase_test.jsonl'

# 读取 Excel 文件
df_train = pd.read_excel(file1)
df_test = pd.read_excel(file2)

# 构造训练数据（文本对）
train_data = []
for _, row in df_train.iterrows():
    fangyan = str(row['fangyan'])
    zh_query = str(row['zh_query'])
    query = str(row['query'])         # 正确翻译
    fangyan_query = str(row['fangyan_query'])  # 错误翻译

    train_entry = {
        "A": f"普通话‘{zh_query}’的{fangyan}话翻译是‘{query}’",
        "B": f"普通话‘{zh_query}’的{fangyan}话翻译是‘{fangyan_query}’",
        "answer": "A"
    }
    train_data.append(json.dumps(train_entry, ensure_ascii=False))

# 构造测试数据（仅文本）
test_data = []
for _, row in df_test.iterrows():
    fangyan = str(row['fangyan'])
    zh_query = str(row['zh_query'])
    fangyan_query = str(row['fangyan_query'])

    test_entry = {
        "text": f"普通话‘{zh_query}’的{fangyan}话翻译是‘{fangyan_query}’"
    }
    test_data.append(json.dumps(test_entry, ensure_ascii=False))

# 写入 JSONL 文件
with open(train_output_jsonl, 'w', encoding='utf-8') as f:
    f.write('\n'.join(train_data))

with open(test_output_jsonl, 'w', encoding='utf-8') as f:
    f.write('\n'.join(test_data))

print(f"✅ 已生成训练集：{train_output_jsonl}")
print(f"✅ 已生成测试集：{test_output_jsonl}")