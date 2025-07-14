import os
import json

def count_jsonl_lines(folder):
    """统计指定文件夹内所有 .jsonl 文件的有效行数"""
    total_lines = 0
    for root, _, files in os.walk(folder):
        for file_name in files:
            if file_name.endswith(".jsonl"):
                file_path = os.path.join(root, file_name)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        for line_number, line in enumerate(f, start=1):
                            stripped_line = line.strip()
                            if not stripped_line:
                                continue
                            try:
                                json.loads(stripped_line)
                                total_lines += 1
                            except json.JSONDecodeError:
                                pass  # 忽略非法行
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
    return total_lines


def merge_all_jsonl_files(input_folders, output_folder, output_file_name="merged_output.jsonl"):
    """
    合并多个输入文件夹中所有 .jsonl 文件的内容，
    输出到输出文件夹下的单个文件中。
    """
    output_file_path = os.path.join(output_folder, output_file_name)

    # 确保输出目录存在
    os.makedirs(output_folder, exist_ok=True)

    new_lines_added = 0

    # 清空或创建输出文件（覆盖模式）
    with open(output_file_path, "w", encoding="utf-8") as outfile:
        for input_folder in input_folders:
            print(f"\n🔍 Processing input folder: {input_folder}")
            for root, _, files in os.walk(input_folder):
                for file_name in files:
                    if file_name.endswith(".jsonl"):
                        input_file_path = os.path.join(root, file_name)
                        print(f"Processing: {input_file_path}")

                        try:
                            with open(input_file_path, "r", encoding="utf-8") as infile:
                                lines = infile.readlines()
                        except Exception as e:
                            print(f"Error reading file {input_file_path}: {e}")
                            continue

                        valid_lines = []
                        for line_number, line in enumerate(lines, start=1):
                            stripped_line = line.strip()
                            if not stripped_line:
                                continue
                            try:
                                data = json.loads(stripped_line)
                                valid_lines.append(data)
                            except json.JSONDecodeError:
                                continue  # 跳过非法行

                        # 写入到目标文件
                        for item in valid_lines:
                            json.dump(item, outfile, ensure_ascii=False)
                            outfile.write("\n")

                        new_lines_added += len(valid_lines)

    print(f"\n✅ 合并完成。输出文件为：{output_file_path}")
    print(f"🆕 新增行数（来自两个输入文件夹）: {new_lines_added}")

    return new_lines_added


# 示例用法
if __name__ == "__main__":
    input_folder1 = r"D:\code\count\dataset\add_contentCopilot_sichuan_critiq"
    input_folder2 = r"D:\code\count\dataset\contentCopilot-sichuan-reject1p2"
    output_folder = r"D:\code\count\dataset\contentCopilot-sichuan-critiq_0710"

    # 统计输入文件夹各自的行数
    count1 = count_jsonl_lines(input_folder1)
    count2 = count_jsonl_lines(input_folder2)

    print(f"\n📊 输入文件夹1 总行数（有效）: {count1}")
    print(f"📊 输入文件夹2 总行数（有效）: {count2}")

    # 合并到输出文件夹下的单个文件
    merged_count = merge_all_jsonl_files([input_folder1, input_folder2], output_folder)

    # 可选：再次统计输出文件的总行数以确保一致性
    output_file_path = os.path.join(output_folder, "merged_output.jsonl")
    with open(output_file_path, "r", encoding="utf-8") as f:
        final_line_count = sum(1 for line in f if line.strip())

    print(f"📊 输出文件总行数（最终结果）: {final_line_count}")