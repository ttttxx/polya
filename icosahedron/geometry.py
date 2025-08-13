# result/geometry.py
import numpy as np
import math
# 黄金比例
phi = (1 + math.sqrt(5)) / 2

# 正二十面体顶点坐标（12个，归一化到单位球）
ICOSAHEDRON_VERTICES = np.array([
    [0, 0, 1], [0, 0, -1],  # 极点
    [1, 1, 1]/np.sqrt(3), [1, -1, -1]/np.sqrt(3),
    [-1, 1, -1]/np.sqrt(3), [-1, -1, 1]/np.sqrt(3),
    [1, 1, -1]/np.sqrt(3), [1, -1, 1]/np.sqrt(3),
    [-1, 1, 1]/np.sqrt(3), [-1, -1, -1]/np.sqrt(3),
    [1, 0, phi], [-1, 0, -phi],  # phi为黄金比例
    # 补充完整12个顶点的坐标（需精确计算）
])

# 归一化顶点坐标到单位球面
vertex_norms = np.linalg.norm(ICOSAHEDRON_VERTICES, axis=1)
ICOSAHEDRON_VERTICES = ICOSAHEDRON_VERTICES / vertex_norms[:, np.newaxis]