import os
import re
import math
from collections import defaultdict


def build_inverted_index_from_files(folder_path):
    index = defaultdict(lambda: defaultdict(int))
    files = [filename for filename in os.listdir(folder_path) if filename.endswith(".txt")]
    total_files = len(files)

    # حساب عدد الملفات لكل مجموعة (تقسيمها على 15 مجموعة)
    files_per_group = math.ceil(total_files / 15)

    # تقسيم الملفات إلى 15 مجموعة
    file_groups = [files[i:i + files_per_group] for i in range(0, total_files, files_per_group)]

    for group_num, file_group in enumerate(file_groups, start=1):
        # بناء الفهرس لكل مجموعة
        for filename in file_group:
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    for line in file:
                        words = re.findall(r'[A-Za-z0-9ء-ي]+', line.lower())
                        for word in words:
                            index[word][filename] += 1
            except Exception as e:
                print(f"[!] Error reading {filename}: {e}")
        
        # حفظ الفهرس الخاص بكل مجموعة
        with open(f"index_group_{group_num}.txt", "w", encoding="utf-8") as f:
            for word, file_dict in sorted(index.items()):
                line = f"{word} : " + " ; ".join(f"{file} {count}" for file, count in sorted(file_dict.items()))
                f.write(line + "\n")
        
        # إعادة تعيين الفهرس بعد كل مجموعة
        index = defaultdict(lambda: defaultdict(int))

    print("✓ Done — indices saved to 'index_group_1.txt', 'index_group_2.txt', etc.'")


folder_path = "D:\\Pages"
build_inverted_index_from_files(folder_path)
