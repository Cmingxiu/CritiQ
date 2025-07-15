import os
import json

# 根目录路径
root_folder = 'D:\code\count\contentCopilot-sichuan-trans-distill1'  # 替换为你的根目录路径

# contentCopilot-sichuan-trans-distill1
sheet_data = []
# 遍历根目录下的所有子目录
for subdir in os.listdir(root_folder):
    subdir_path = os.path.join(root_folder, subdir)
    
    if os.path.isdir(subdir_path):
        # 遍历子目录中的所有文件
        for file_name in os.listdir(subdir_path):
            # 检查文件是否以 .jsonl 结尾
            if file_name.endswith('.jsonl'):
                file_path = os.path.join(subdir_path, file_name)
                # 打开并读取文件
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        # 解析 JSON 数据
                        data = json.loads(line.strip())
                        is_testcase = data.get('is_testcase')
                        if is_testcase == 'n':
                            zh_query = data.get('llm_mandarin')
                            fangyan = data.get('llm_dialect')
                            if zh_query and fangyan:
                                entry1 = {
                                    "text": f"普通话‘{zh_query}’的四川话翻译是‘{fangyan}’"
                                }
                                sheet_data.append(entry1)

# sounboix
# sheet_data = []
# for file_name in os.listdir(root_folder):
#     if file_name.endswith('.jsonl'):
#         file_path = os.path.join(root_folder, file_name)
#         print(file_path)
#         with open(file_path, 'r', encoding='utf-8') as f:
#             for line in f:
#                 data = json.loads(line.strip())
#                 if data.get('is_testcase') == 'n':
#                     zh_query = data.get('mandarin')
#                     fangyan = data.get('dialect_qurey')
#                     if zh_query and fangyan:
#                         sheet_data.append({
#                             "text": f"普通话‘{zh_query}’的粤语话翻译是‘{fangyan}’"
#                         })


output_file_path = 'D:\code\count\jsonl\contentsichuan_train.jsonl'  # 替换为您想保存的路径
# 写入时统一处理
with open(output_file_path, 'w', encoding='utf-8') as f:
    for item in sheet_data:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')