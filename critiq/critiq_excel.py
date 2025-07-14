import os
import json
import pandas as pd

# 定义根目录和输出Excel文件路径
root_folder = 'D:\\code\\CritiQ\\result\\one\\0701'  # 替换为你的根目录路径
output_excel_file = 'D:\\code\\count\\dataset\\0701_critiq_result.xlsx'  # 输出的Excel文件名

# 创建一个空字典用于存储每个sheet的数据
sheet_data = {}

# 遍历根目录下的所有子文件夹
for subdir in os.listdir(root_folder):
    subdir_path = os.path.join(root_folder, subdir)
    
    if os.path.isdir(subdir_path):
        for file_name in os.listdir(subdir_path):
            if file_name.endswith('.jsonl'):
                file_path = os.path.join(subdir_path, file_name)
                data_list = []  # 每个文件单独一个列表

                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        data = json.loads(line.strip())
                        
                        if 'A' in data and 'B' in data:
                            A = data['A']
                            B = data['B']

                            # 提取普通话部分（zh_query）
                            zh_query = A.split("‘")[1].split("’")[0]

                            # 提取方言种类（fangyan）：如“粤语”
                            fangyan = A.split("’的")[1].split("话")[0]

                            # 提取方言表达（fangyan_query）
                            fangyan_query = A.split("‘")[-1].split("’")[0]

                            # 提取错误方言表达（bad_query）
                            bad_query = B.split("‘")[-1].split("’")[0]

                            answer = data.get('answer')
                            thought = data.get('thought')

                            data_list.append({
                                'zh_query': zh_query,
                                'fangyan': fangyan,
                                'fangyan_query': fangyan_query,
                                'bad_query': bad_query,
                                'answer': answer,
                                'thought': thought
                            })
                        
                        elif "text" in data:
                            A = data['text']

                            # 提取普通话部分（zh_query）
                            zh_query = A.split("‘")[1].split("’")[0]

                            # 提取方言种类（fangyan）：如“粤语”
                            fangyan = A.split("’的")[1].split("话")[0]

                            # 提取方言表达（fangyan_query）
                            fangyan_query = A.split("‘")[-1].split("’")[0]

                            answer = data.get('label')
                            thought = data.get('thought')
                            if data.get('all_label'):
                                all_label = data.get('all_label')
                                sum1 = 0
                                for v in all_label.values():
                                    if v==1 or v==0:
                                        sum1 += int(v)
                                data_list.append({
                                'zh_query': zh_query,
                                'fangyan': fangyan,
                                'fangyan_query': fangyan_query,
                                'sum':sum1,
                                'label': answer,
                
                                'all_label':all_label,
                            
                                'thought': thought
                                })
                            else:
                                data_list.append({
                                    'zh_query': zh_query,
                                    'fangyan': fangyan,
                                    'fangyan_query': fangyan_query,
                                    'label': answer,
                                    'thought': thought
                                })

                if data_list:
                    # 使用 文件夹名_文件名 作为 sheet 名，避免重复
                    sheet_name = f"{subdir}_{file_name}"[:31]  # sheet 名最多31字符
                    df = pd.DataFrame(data_list)
                    sheet_data[sheet_name] = df

# 写入Excel，每个 .jsonl 文件对应一个 sheet
with pd.ExcelWriter(output_excel_file, engine='xlsxwriter') as writer:
    for sheet_name, df in sheet_data.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"✅ Excel 文件已成功生成: {output_excel_file}")