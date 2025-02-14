import sys
import os

def process_file(file_path, keyword):
    # 获取文件所在目录和文件名
    directory = os.path.dirname(file_path)
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 筛选包含关键词的行
    filtered_lines = [line for line in lines if keyword.lower() in line.split(':')[0].lower()]
    
    # 创建输出文件路径
    output_file = os.path.join(directory, f'{keyword}.txt')
    
    # 写入筛选后的内容
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(filtered_lines)
    
    print(f'处理完成！已生成文件：{output_file}')

def main():
    # 检查是否有文件拖拽到脚本上
    if len(sys.argv) < 2:
        print('请将文件拖拽到此脚本上运行！')
        return
    
    # 获取文件路径
    file_path = sys.argv[1]
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print('文件不存在！')
        return
    
    # 获取用户输入的关键词
    keyword = input('请输入要筛选的关键词：').strip()
    
    if not keyword:
        print('关键词不能为空！')
        return
    
    # 处理文件
    process_file(file_path, keyword)

if __name__ == '__main__':
    main()
