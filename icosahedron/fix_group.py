import re

input_file = "icosahedron_rotation_group.txt"   # 你刚才贴的内容保存的文件
output_file = "icosahedron_group.txt"      # 转换后的文件

with open(input_file, "r") as f:
    content = f.read()

# 用正则找到所有数字并减去 1
def shift_num(match):
    return str(int(match.group()) - 1)

converted = re.sub(r"\d+", shift_num, content)

with open(output_file, "w") as f:
    f.write(converted)

print(f"已完成转换，结果保存到 {output_file}")
