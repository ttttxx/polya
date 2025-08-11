import os
from sage.misc.persist import save
from sage.groups.perm_gps.permgroup_named import AlternatingGroup

# 确保在项目目录下操作
project_dir = "/Users/xushi/PycharmProjects/polya/dodecahedron"  # 改为你的实际目录名
if not os.path.exists(project_dir):
    os.makedirs(project_dir)
os.chdir(project_dir)

# 生成群
dodec = polytopes.dodecahedron()
G = dodec.restricted_automorphism_group(output='permutation')

# 关键修改：提取纯旋转子群（60阶交错群A5）
# 方法1：通过换位子群获取（推荐）
rot_group = G.commutator()  # 换位子群即旋转对称群[2,5](@ref)

# 验证关键属性
print("阶数:", rot_group.order())               # 应输出 60
print("是否为偶置换群:", all(g.sign()==1 for g in rot_group)) # 应输出 True
rot_elements = list(rot_group)
# 方法2：显式构造交错群（需验证同构性）
# rot_group = AlternatingGroup(5)  # 直接构造A5群[3](@ref)
# 验证同构：print(rot_group.is_isomorphic(G.commutator()))

# 获取群元素
group_elements = [list(g) for g in rot_group]

# 保存文件
filename = "dodecahedron_rotation_group.sobj"
save(group_elements, filename)

# txt输出
with open('dodecahedron_rotation_group.txt', 'w') as f:
    for perm in group_elements:
        f.write(str(list(perm)) + '\n')

# 验证文件存在
if os.path.isfile(filename):
    print(f"成功保存到: {os.path.abspath(filename)}")
    print(f"文件大小: {os.path.getsize(filename)} 字节")
    print(f"旋转群阶数: {len(group_elements)}")  # 应为60
else:
    print("保存失败！请检查权限和路径")