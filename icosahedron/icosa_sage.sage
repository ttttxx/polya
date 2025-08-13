import os
from sage.misc.persist import save
from sage.groups.perm_gps.permgroup_named import AlternatingGroup
# 修改导入路径：使用 polytopes 模块中的 icosahedron
from sage.geometry.polyhedron.library import polytopes

# 确保在项目目录下操作
project_dir = "/Users/xushi/PycharmProjects/polya/icosahedron"  # 改为你的实际目录名
if not os.path.exists(project_dir):
    os.makedirs(project_dir)
os.chdir(project_dir)

# 创建正二十面体（使用 polytopes.icosahedron()）
icosa = polytopes.icosahedron()

# 获取旋转对称群（作用在20个面上）
G = icosa.restricted_automorphism_group(output='permutation')

# 提取纯旋转子群（60阶交错群A5）
rot_group = G.commutator()  # 换位子群即旋转对称群

# 验证关键属性
print("阶数:", rot_group.order())  # 应输出 60
print("是否为偶置换群:", all(g.sign() == 1 for g in rot_group))  # 应输出 True
print("作用在顶点上的度:", rot_group.degree())  # 应输出 12（因为二十面体有12个顶点）
rot_elements = list(rot_group)

# 获取群元素（作为置换）
group_elements = [list(g) for g in rot_group]

# 保存文件
filename = "icosahedron_rotation_group.sobj"
save(group_elements, filename)

# txt输出
with open('icosahedron_rotation_group.txt', 'w') as f:
    for i, perm in enumerate(group_elements):
        f.write(f"旋转元素 #{i + 1}:\n")
        f.write(str(perm) + '\n\n')

# 保存群对象以备后续使用
save(rot_group, "icosahedron_rotation_group_object.sobj")

# 验证文件存在
if os.path.isfile(filename):
    print(f"成功保存到: {os.path.abspath(filename)}")
    print(f"文件大小: {os.path.getsize(filename)} 字节")
    print(f"旋转群阶数: {len(group_elements)}")  # 应为60
    print(f"作用在 {rot_group.degree()} 个顶点上")  # 应为12
else:
    print("保存失败！请检查权限和路径")