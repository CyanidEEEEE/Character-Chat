import pandas as pd
import sys
import re  # 导入正则表达式模块
from pathlib import Path
from tkinter import messagebox

def process_file(file_path):
    try:
        file_path = Path(file_path)
        df = pd.read_csv(file_path, sep='\t')

        if not all(col in df.columns for col in ["Character", "Dialogue", "Identifier"]):
            messagebox.showerror("错误", "输入文件缺少 Character、Dialogue 或 Identifier 列")
            return

        output_file = file_path.with_suffix('.txt')
        with open(output_file, 'w', encoding='utf-8') as file:
            for _, row in df.iterrows():
                identifier = row["Identifier"]
                character = str(row["Character"]) if not pd.isna(row["Character"]) else "bac"
                dialogue = str(row["Dialogue"]) if not pd.isna(row["Dialogue"]) else ""

                identifier_value = '_'.join(identifier.split('_')[:-1])
                character_abbr_value = character[:3].lower()
                formatted_identifier = f"{identifier_value}-{character_abbr_value}"
                formatted_message = f"{formatted_identifier}: {dialogue.strip()}"

                # 使用正则表达式去除 {} 及其内容
                formatted_message = re.sub(r'\{.*?\}', '', formatted_message)

                file.write(formatted_message + '\n')

        messagebox.showinfo("成功", f"文件转换完成，输出保存为 {output_file}")

    except Exception as e:
        messagebox.showerror("错误", f"处理文件时出现错误：{e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if Path(file_path).suffix == '.tab':
             process_file(file_path)
        else:
            messagebox.showwarning("警告", "请拖拽一个 .tab 文件！")

    else:
        messagebox.showwarning("警告", "请将 .tab 文件拖拽到此程序上！")
