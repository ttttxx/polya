import numpy as np
from collections import deque, defaultdict
from .geometry import DODECAHEDRON_FACES, FACE_CENTERS, DODECAHEDRON_VERTICES

# 用于缓存生成的对称群
SYMMETRY_CACHE = {}

def generate_dodecahedron_rotations():
    """生成正十二面体的60个旋转对称（顶点置换）"""
    if 'vertex_rotations' in SYMMETRY_CACHE:
        return SYMMETRY_CACHE['vertex_rotations']

    # 使用生成元
    a = [1, 2, 3, 4, 0, 6, 7, 8, 9, 5, 11, 12, 13, 14, 10, 16, 17, 18, 19, 15]
    b = [5, 8, 6, 9, 7, 10, 11, 12, 14, 13, 0, 2, 3, 1, 4, 15, 16, 17, 18, 19]

    # 缓存逆置换
    a_inv = [0] * len(a)
    b_inv = [0] * len(b)
    for i, x in enumerate(a):
        a_inv[x] = i
    for i, x in enumerate(b):
        b_inv[x] = i

    # 置换乘法
    def perm_mult(p, q):
        return [p[q[i]] for i in range(len(q))]

    # 初始化群
    identity = list(range(20))
    group = {tuple(identity)}
    queue = deque([identity])

    # 添加生成元
    generators = [a, b, a_inv, b_inv]  # 包含逆置换

    # 使用BFS生成整个群
    while queue:
        p = queue.popleft()
        for gen in generators:
            new_perm = perm_mult(p, gen)
            new_perm_tuple = tuple(new_perm)
            if new_perm_tuple not in group:
                group.add(new_perm_tuple)
                queue.append(new_perm)

    result = [list(perm) for perm in group]
    SYMMETRY_CACHE['vertex_rotations'] = result
    return result

def generate_symmetry_group(mode='vertex'):
    """生成对称操作（顶点或面的置换）"""
    cache_key = f"{mode}_group"
    if cache_key in SYMMETRY_CACHE:
        return SYMMETRY_CACHE[cache_key]

    if mode == 'vertex':
        result = generate_dodecahedron_rotations()
    else:
        vertex_rotations = generate_dodecahedron_rotations()
        face_perms = []

        # 直接使用面的中心点来进行匹配
        for vertex_perm in vertex_rotations:
            face_perm = []
            for face in DODECAHEDRON_FACES:
                rotated_face_vertices = [DODECAHEDRON_VERTICES[vertex_perm[i]] for i in face]
                rotated_face_center = np.mean(rotated_face_vertices, axis=0)

                # 找到最接近的面
                min_dist = float('inf')
                min_idx = -1
                for idx, center in enumerate(FACE_CENTERS):
                    dist = np.linalg.norm(rotated_face_center - center)
                    if dist < min_dist:
                        min_dist = dist
                        min_idx = idx

                face_perm.append(min_idx)

            face_perms.append(face_perm)

        result = face_perms

    SYMMETRY_CACHE[cache_key] = result
    return result