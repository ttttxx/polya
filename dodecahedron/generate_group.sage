import os
from sage.misc.persist import save

# 确保在项目目录下操作
project_dir = "/Users/xushi/PycharmProjects/polya/dodecahedron"  # 改为你的实际目录名
if not os.path.exists(project_dir):
    os.makedirs(project_dir)
os.chdir(project_dir)

# 生成群
dodec = polytopes.dodecahedron()
G = dodec.restricted_automorphism_group(output='permutation')
group_elements = [list(g) for g in G]

# 保存文件
filename = "dodecahedron_group.sobj"
save(group_elements, filename)

# txt输出
with open('dodecahedron_group.txt', 'w') as f:
    for perm in group_elements:
        f.write(str(list(perm)) + '\n')

# 验证文件存在
if os.path.isfile(filename):
    print(f"成功保存到: {os.path.abspath(filename)}")
    print(f"文件大小: {os.path.getsize(filename)} 字节")
else:
    print("保存失败！请检查权限和路径")