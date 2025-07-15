import os
import json
from collections import defaultdict
import string

# ========== 用户配置 ==========
input_filter_jsonl = 'D:\\code\\CritiQ\\result\\one\\0701\\0.9doubao\\0714.jsonl'
input_filter_jsonl1 = 'D:\\code\\CritiQ\\result\\one\\0701\\0.9doubao\\0714_yue.jsonl'
other_filter_jsonl = 'D:\\code\\count\\jsonl\\base\\0714_common.jsonl'
input_data_file = 'D:\\code\\count\\jsonl\\base\\train.jsonl'
output_new_jsonl_file = 'D:\\code\\count\\jsonl\\base\\train_0714.jsonl'


def remove_punctuation(text):
    keep_punctuation = ":%-."
    all_punctuation = string.punctuation + "。！？，、；：“”‘’《》（）【】?…"
    translation_table = str.maketrans('', '', ''.join([p for p in all_punctuation if p not in keep_punctuation]))
    cleaned_text = text.translate(translation_table)
    return cleaned_text


# ========== 第一步：从两个文件中提取所有 (fangyan_query, mandarin) -> 多个方言类型 ==========
pair_to_types = defaultdict(set)  # {(f, m): {'四川话', '广东话'}, ...}
def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as fin:
        for line in fin:
            data = json.loads(line.strip())
            A = data['text']
            try:
                zh_query = A.split("‘")[1].split("’")[0]
                fangyan = A.split("’的")[1].split("话")[0] + "话"
                fangyan_query = A.split("‘")[-1].split("’")[0]
            except IndexError:
                continue
            answer = data.get('label')
            if answer == None:
                pair = (fangyan_query, zh_query)
                pair_to_types[pair].add(fangyan)
            else:
                if answer == 1 and abs(len(zh_query) - len(fangyan_query)) < 8:
                    pair = (fangyan_query, zh_query)
                    pair_to_types[pair].add(fangyan)
                # 如果粤语忘记改阈值
                # all_label = data.get('all_label')
                # sum1 = 0
                # for v in all_label.values():
                #     if v==1 or v==0:
                #         sum1 += int(v)

                # if fangyan == "粤语话":
                #     if sum1 > 9 and abs(len(zh_query) - len(fangyan_query)) < 8:
                #         pair = (fangyan_query, zh_query)
                #         pair_to_types[pair].add(fangyan)

                # else:  
                #     if answer == 1 and abs(len(zh_query) - len(fangyan_query)) < 8:
                #         pair = (fangyan_query, zh_query)
                #         pair_to_types[pair].add(fangyan)

# 读取两个文件
process_file(input_filter_jsonl)
print(f"✅ 共收集到 {len(pair_to_types)} 个 (fangyan_query, mandarin) 对，每个对可能包含多种方言类型")

process_file(input_filter_jsonl1)
print(f"✅ 共收集到 {len(pair_to_types)} 个 (fangyan_query, mandarin) 对，每个对可能包含多种方言类型")

process_file(other_filter_jsonl)
print(f"✅ 共收集到 {len(pair_to_types)} 个 (fangyan_query, mandarin) 对，每个对可能包含多种方言类型")

# ========== 第二步：读取 train.jsonl 并进行匹配，每匹配一次就删除该 pair ==========
reformatted_data = []

with open(input_data_file, 'r', encoding='utf-8') as fin:
    for line in fin:
        data = json.loads(line.strip())

        messages = data.get("messages", "")
        if "方言Query:" in messages and "\n对应的普通话翻译文本:" in messages:
            fangyan_query = messages.split("方言Query:")[1].split("\n对应的普通话翻译文本:")[0].strip()
            fangyan_query = remove_punctuation(fangyan_query)
            zh_query = data.get("output", "").strip()
            zh_query = remove_punctuation(zh_query)
            pair = (fangyan_query, zh_query)

            if pair in pair_to_types:
                # 取出一个 type
                selected_type = pair_to_types[pair].pop()
                data["type"] = selected_type
                reformatted_data.append(data)
                # 如果这个 pair 的集合为空了，就删除它
                if not pair_to_types[pair]:
                    del pair_to_types[pair]

print(f"✅ 共筛选出 {len(reformatted_data)} 条数据，已添加方言类型字段")

# ========== 第三步：写入新文件 ==========
os.makedirs(os.path.dirname(output_new_jsonl_file), exist_ok=True)

with open(output_new_jsonl_file, 'w', encoding='utf-8') as fout:
    for item in reformatted_data:
        fout.write(json.dumps(item, ensure_ascii=False) + '\n')

print(f"✅ 已将数据写入文件：{output_new_jsonl_file}")