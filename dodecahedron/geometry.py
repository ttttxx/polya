# dodecahedron/geometry.py
import numpy as np
import math

# 黄金比例
phi = (1 + math.sqrt(5)) / 2

# 正十二面体顶点坐标（20个）
DODECAHEDRON_VERTICES = np.array([
    [1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
    [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1],
    [0, 1 / phi, phi], [0, 1 / phi, -phi], [0, -1 / phi, phi], [0, -1 / phi, -phi],
    [1 / phi, phi, 0], [1 / phi, -phi, 0], [-1 / phi, phi, 0], [-1 / phi, -phi, 0],
    [phi, 0, 1 / phi], [phi, 0, -1 / phi], [-phi, 0, 1 / phi], [-phi, 0, -1 / phi]
])

# 归一化顶点坐标到单位球面
vertex_norms = np.linalg.norm(DODECAHEDRON_VERTICES, axis=1)
DODECAHEDRON_VERTICES = DODECAHEDRON_VERTICES / vertex_norms[:, np.newaxis]

# 修正的面定义（使用正确的12个面）
DODECAHEDRON_FACES = [
    [0, 8, 10, 2, 16],  # 面0
    [0, 16, 17, 1, 8],   # 面1
    [0, 8, 1, 13, 12],   # 面2
    [8, 1, 9, 5, 13],    # 面3
    [1, 17, 3, 9, 5],    # 面4
    [17, 3, 15, 19, 9],  # 面5
    [16, 17, 3, 15, 18], # 面6
    [2, 16, 18, 6, 10],  # 面7
    [10, 2, 12, 4, 14],  # 面8
    [10, 8, 12, 13, 14], # 面9
    [18, 6, 11, 7, 15],  # 面10
    [6, 11, 19, 7, 14]   # 面11
]

# 计算每个面的中心点
FACE_CENTERS = []
for face in DODECAHEDRON_FACES:
    face_vertices = DODECAHEDRON_VERTICES[face]
    FACE_CENTERS.append(np.mean(face_vertices, axis=0))