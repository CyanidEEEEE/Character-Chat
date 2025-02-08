import pandas as pd
import sys
from pathlib import Path
from tkinter import messagebox

def process_file(file_path):
    try:
        file_path = Path(file_path)
        # 读取Tab分隔的文件，指定分隔符为 \t
        df = pd.read_csv(file_path, sep='\t')

        # 检查必须的列是否存在
        if not all(col in df.columns for col in ["Character", "Dialogue", "Identifier"]):
            messagebox.showerror("错误", "输入文件缺少 Character、Dialogue 或 Identifier 列")
            return

        output_file = file_path.with_suffix('.txt')  # 输出文件路径与输入文件同名，只是扩展名为 .txt
        with open(output_file, 'w', encoding='utf-8') as file:
            for _, row in df.iterrows():
                identifier = row["Identifier"]
                character = str(row["Character"]) if not pd.isna(row["Character"]) else "bac"
                dialogue = str(row["Dialogue"]) if not pd.isna(row["Dialogue"]) else ""

                # 删除 _ 后的最后一段，只保留前面的部分
                identifier_value = '_'.join(identifier.split('_')[:-1])
                # 获取角色的前三个字母（小写）
                character_abbr_value = character[:3].lower()
                formatted_identifier = f"{identifier_value}-{character_abbr_value}"
                formatted_message = f"{formatted_identifier}: {dialogue.strip()}"

                file.write(formatted_message + '\n')

        messagebox.showinfo("成功", f"文件转换完成，输出保存为 {output_file}")

    except Exception as e:
        messagebox.showerror("错误", f"处理文件时出现错误：{e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:  # 检查是否有拖拽的文件
        file_path = sys.argv[1] #windows下直接拖拽文件到py文件上，会把文件路径作为argv传入
        if Path(file_path).suffix == '.tab':
             process_file(file_path)
        else:
            messagebox.showwarning("警告", "请拖拽一个 .tab 文件！")

    else:
        messagebox.showwarning("警告", "请将 .tab 文件拖拽到此程序上！")