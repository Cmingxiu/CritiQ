import os
import json
from collections import Counter

# ========== 用户配置 ==========
input_filter_jsonl = 'D:\\code\\CritiQ\\result\\one\\0701\\doubao15\\soundbox_train.jsonl'
input_data_folder = 'D:\\code\\count\\mandarin'
additional_jsonl = 'D:\\code\\count\\豆包\\train.jsonl'  # 新增的 JSONL 文件
output_new_jsonl_file = 'D:\\code\\count\\dataset\\distill_soundbox_critiq\\doubao\\train.jsonl'
output_duplicate_jsonl_file = 'D:\\code\\count\\dataset\\distill_soundbox_critiq\\doubao\\duplicate_train.jsonl'

# ========== 第一步：从 filter_source.jsonl 提取符合条件的 (fangyan_query, mandarin) ==========
filtered_pairs = set()

with open(input_filter_jsonl, 'r', encoding='utf-8') as fin:
    for line in fin:
        data = json.loads(line.strip())
        if "text" in data:
            A = data['text']
            try:
                zh_query = A.split("‘")[1].split("’")[0]
                fangyan = A.split("’的")[1].split("话")[0]
                fangyan_query = A.split("‘")[-1].split("’")[0]
                answer = data.get('label')
            except IndexError:
                continue

            if answer == 1 and abs(len(zh_query) - len(fangyan_query)) < 8:
                filtered_pairs.add((fangyan_query, zh_query))

print(f"✅ 共筛选出 {len(filtered_pairs)} 个符合条件的 (fangyan_query, mandarin) 对")

# ========== 第二步：从 additional_jsonl 中提取所有 output，作为 valid_outputs ==========
valid_outputs = set()

with open(additional_jsonl, 'r', encoding='utf-8') as fin:
    for line in fin:
        data = json.loads(line.strip())
        output = data.get('output')
        if output:
            valid_outputs.add(output.strip())

print(f"✅ 从 additional_jsonl 中提取出 {len(valid_outputs)} 条有效的 output 用于匹配")

# ========== 第三步：遍历文件夹中所有 .jsonl 文件，进行双重匹配 ==========
reformatted_data = []
pair_counter = Counter()  # 统计每个 pair 出现的次数

for filename in os.listdir(input_data_folder):
    if filename.endswith('.jsonl'):
        file_path = os.path.join(input_data_folder, filename)
        with open(file_path, 'r', encoding='utf-8') as fin:
            for line in fin:
                record = json.loads(line.strip())

                dialect_query = record.get('dialect_qurey')
                mandarin = record.get('mandarin')
                zh_query = record.get('zh_query')

                if not dialect_query or not mandarin or not zh_query:
                    continue

                pair = (dialect_query, mandarin)

                # 新增条件：zh_query 必须出现在 additional_jsonl 的 output 列表中
                if pair in filtered_pairs and record.get('is_testcase') == 'n' and zh_query in valid_outputs:
                # if pair in filtered_pairs and record.get('is_testcase') == 'n' :
                    reformatted_data.append({
                        "session_id": str(record.get("session_id", "")),
                        "request_id": str(record.get("request_id", "")),
                        "system": "你是一个精通普通话和多种方言的中国人，请你把这句方言文本翻译成普通话。\n翻译要求是：\n1.翻译时遵循普通话的表达方式，注意术语的一致性，符合日常口语习惯；\n2.首先输出该句方言文本Query对应的普通话翻译，然后输出分步推理、思考过程及最终答案总结。\n",
                        "messages": f"方言Query:{record.get('dialect_qurey', '')}\n对应的普通话翻译文本:",
                        "output": f"{record.get('mandarin', '')}\n\n{record.get('thought', '')}\n\n<answer>\n{record.get('answer', '')}\n<answer>",
                        "md5": f"{record.get('domain', '')}#{os.path.splitext(filename)[0]}#{record.get('order_id', '')}",
                    })
                    pair_counter[pair] += 1  # 记录这个 pair 出现了多少次

print(f"✅ 共筛选出 {len(reformatted_data)} 条数据，已成功生成新格式的 JSONL 文件：{output_new_jsonl_file}")

# ========== 第四步：写入主文件 ==========
os.makedirs(os.path.dirname(output_new_jsonl_file), exist_ok=True)

with open(output_new_jsonl_file, 'w', encoding='utf-8') as fout:
    for item in reformatted_data:
        fout.write(json.dumps(item, ensure_ascii=False) + '\n')

print(f"✅ 已将数据写入文件：{output_new_jsonl_file}")