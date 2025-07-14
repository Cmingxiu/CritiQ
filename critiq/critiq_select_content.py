import os
import json
from collections import Counter
import random
import pandas as pd

# ========== 用户配置 ==========
input_filter_jsonl = 'D:\\code\\CritiQ\\result\\one\\0701\\doubao15\\contentyue_train.jsonl'
input_data_folder = 'D:\\code\\count\\contentCopilot-yue-trans-distill1'
input_excel = 'D:\\code\\count\\contentCopilot-yue-distill1\\train_rejection.xlsx'

# 输出主目录（用于保存筛选后的数据）
output_main_dir = 'D:\\code\\count\\dataset\\add_contentCopilot_sichuan_critiq'

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

# ========== 第二步：读取 Excel，筛选 equal + multi_qa_equal == 0 的 llm_mandarin ==========
df_excel = pd.read_excel(input_excel)
excel_filtered = df_excel[df_excel['equal'] + df_excel['multi_qa_equal'] == 0]
excel_llm_mandarin_set = set(excel_filtered['llm_mandarin'].str.strip().dropna())

print(f"✅ 从 Excel 中筛选出 {len(excel_llm_mandarin_set)} 条 equal + multi_qa_equal == 0 的 llm_mandarin")

# ========== 第三步：遍历 input_data_folder 及其子文件夹中所有 .jsonl 文件，进行双重匹配 ==========
file_data_map = {}        # 缓存所有文件的数据 {relative_path: data_list}
total_count = 0  # 总共筛选出的条目数

for root, dirs, files in os.walk(input_data_folder):
    for filename in files:
        if filename.endswith('.jsonl'):
            file_path = os.path.join(root, filename)
            relative_path = os.path.relpath(root, input_data_folder)

            with open(file_path, 'r', encoding='utf-8') as fin:
                reformatted_data = []

                for line in fin:
                    record = json.loads(line.strip())

                    dialect_query = record.get('llm_dialect')
                    mandarin = record.get('llm_mandarin')
                    zh_query = record.get('zh_query')

                    if not dialect_query or not mandarin:
                        continue

                    pair = (dialect_query, mandarin)

                    # 增加 Excel 中的 mandarin 匹配条件
                    if pair in filtered_pairs and mandarin in excel_llm_mandarin_set and record.get('is_testcase') == 'n':
                    # if pair in filtered_pairs and record.get('is_testcase') == 'n':
                        score_0 = random.random()
                        if score_0 < 0.1:
                            reformatted_data.append({
                                "session_id": str(record.get("session_id", "")),
                                "request_id": str(record.get("request_id", "")),
                                "system": "你是一个精通普通话和多种方言的中国人，请你把这句方言文本翻译成普通话。\n翻译要求是：\n1.翻译时遵循普通话的表达方式，注意术语的一致性，符合日常口语习惯；\n2.首先输出该句方言文本Query对应的普通话翻译，然后输出分步推理、思考过程及最终答案总结。\n",
                                "messages": f"方言Query:{record.get('zh_query', '')}\n对应的普通话翻译文本:",
                                "output": f"{record.get('zh_query', '')}",
                                "semantic_code": record.get("semantic_code", ""),
                                "agent_template": "Query:{query}\ncode:",
                                "md5": record.get("category", ""),
                                "zh_query": record.get("zh_query", ""),
                                "fangyan_query": dialect_query,
                                "llm_mandarin": mandarin,
                                "is_reject_sampling": True   
                            })
                        elif score_0 > 0.2:
                            reformatted_data.append({
                                "session_id": str(record.get("session_id", "")),
                                "request_id": str(record.get("request_id", "")),
                                "system": "你是一个精通普通话和多种方言的中国人，请你把这句方言文本翻译成普通话。\n翻译要求是：\n1.翻译时遵循普通话的表达方式，注意术语的一致性，符合日常口语习惯；\n2.首先输出该句方言文本Query对应的普通话翻译，然后输出分步推理、思考过程及最终答案总结。\n",
                                "messages": f"方言Query:{record.get('llm_dialect', '')}\n对应的普通话翻译文本:",
                                "output": f"{record.get('llm_mandarin', '')}\n\n{record.get('thought', '')}\n\n<answer>\n{record.get('answer', '')}\n<answer>",
                                "semantic_code": record.get("semantic_code", ""),
                                "agent_template": "Query:{query}\ncode:",
                                "md5": record.get("category", ""),
                                "zh_query": record.get("zh_query", ""),
                                "fangyan_query": dialect_query,
                                "llm_mandarin": mandarin,
                                "is_reject_sampling": True   
                            })
                        else:
                            reformatted_data.append({
                                "session_id": str(record.get("session_id", "")),
                                "request_id": str(record.get("request_id", "")),
                                "system": "你是一个精通普通话和多种方言的中国人，请你把这句方言文本翻译成普通话。\n翻译要求是：\n1.翻译时遵循普通话的表达方式，注意术语的一致性，符合日常口语习惯；\n2.首先输出该句方言文本Query对应的普通话翻译，然后输出分步推理、思考过程及最终答案总结。\n",
                                "messages": f"方言Query:{record.get('llm_dialect', '')}\n对应的普通话翻译文本:",
                                "output": f"{record.get('llm_mandarin', '')}",
                                "semantic_code": record.get("semantic_code", ""),
                                "agent_template": "Query:{query}\ncode:",
                                "md5": record.get("category", ""),
                                "zh_query": record.get("zh_query", ""),
                                "fangyan_query": dialect_query,
                                "llm_mandarin": mandarin,
                                "is_reject_sampling": True   
                            })

                if reformatted_data:
                    total_count += len(reformatted_data)
                    file_key = os.path.join(relative_path, os.path.splitext(filename)[0])
                    file_data_map[file_key] = reformatted_data
                    print(f"✅ 文件 {file_key}.jsonl 中共筛选出 {len(reformatted_data)} 条数据")

# ========== 第四步：写入主文件（保持目录结构）==========
for file_key, reformatted_data in file_data_map.items():
    base_name = os.path.basename(file_key)
    relative_dir = os.path.dirname(file_key)

    output_subdir = os.path.join(output_main_dir, relative_dir)
    os.makedirs(output_subdir, exist_ok=True)
    output_file = os.path.join(output_subdir, f"train_{base_name}.jsonl")

    with open(output_file, 'w', encoding='utf-8') as fout:
        for item in reformatted_data:
            fout.write(json.dumps(item, ensure_ascii=False) + '\n')

    print(f"✅ 已将数据写入文件：{output_file}")

# ========== 最终统计输出 ==========
print(f"✅ 总共筛选出 {total_count} 条数据")