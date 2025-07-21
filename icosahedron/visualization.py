import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import to_rgba
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# 修正后的正二十面体顶点和面定义
def create_icosahedron():
    """创建正二十面体的顶点和面"""
    # 黄金分割比例
    phi = (1 + np.sqrt(5)) / 2

    # 12个顶点 - 修正后的定义
    vertices = np.array([
        [-1, phi, 0], [1, phi, 0], [-1, -phi, 0], [1, -phi, 0],
        [0, -1, phi], [0, 1, phi], [0, -1, -phi], [0, 1, -phi],
        [phi, 0, -1], [phi, 0, 1], [-phi, 0, -1], [-phi, 0, 1]
    ])

    # 规范化所有顶点到单位球面
    norms = np.linalg.norm(vertices, axis=1)
    vertices = vertices / norms[:, np.newaxis]

    # 20个三角形面 - 修正后的连接
    faces = [
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
    ]

    return vertices, faces


# 全局变量
ICOSAHEDRON_VERTICES, ICOSAHEDRON_FACES = create_icosahedron()


def visualize_icosa_face_from_dodeca_vertex(color_mapping, coloring_dodeca_vertex, ax=None):
    """
    将十二面体顶点染色方案转化为二十面体面染色方案并可视化

    参数:
        color_mapping: 颜色名称到颜色值的映射
        coloring_dodeca_vertex: 十二面体顶点染色方案 (20个颜色)
        ax: 可选的matplotlib坐标轴对象
    """
    # 创建面集合
    faces = []
    rgba_colors = []  # 存储带有透明度的RGBA颜色

    # 计算每个面的中心点用于深度排序
    face_centers = []
    for face in ICOSAHEDRON_FACES:
        face_vertices = ICOSAHEDRON_VERTICES[face]
        center = np.mean(face_vertices, axis=0)
        face_centers.append(center)

    # 按深度排序面以确保正确渲染
    sorted_faces = sorted(enumerate(ICOSAHEDRON_FACES),
                          key=lambda x: face_centers[x[0]][2],
                          reverse=True)

    # 计算每个面的颜色
    for face_idx, face in sorted_faces:
        face_vertices = ICOSAHEDRON_VERTICES[face]
        faces.append(face_vertices)

        # 获取对应的十二面体顶点颜色
        color_name = coloring_dodeca_vertex[face_idx]
        base_color = color_mapping.get(color_name, color_name)

        # 添加透明度（根据深度调整）
        depth = face_centers[face_idx][2]
        alpha = max(0.65, 0.95 - abs(depth) * 0.15)

        # 将基础颜色转换为RGBA并设置透明度
        rgba = to_rgba(base_color)
        rgba_with_alpha = (rgba[0], rgba[1], rgba[2], alpha)
        rgba_colors.append(rgba_with_alpha)

    if ax is None:
        fig = plt.figure(figsize=(12, 12), dpi=100)
        ax = fig.add_subplot(111, projection='3d')
    else:
        fig = ax.figure

    # 设置视角
    ax.view_init(elev=25, azim=35)

    # 绘制面 - 使用facecolors参数设置每个面的颜色
    surface = Poly3DCollection(faces, linewidths=1.5, edgecolors='k', facecolors=rgba_colors)
    ax.add_collection3d(surface)

    # 设置坐标轴属性
    max_range = 1.2
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    ax.set_zlim(-max_range, max_range)

    # 设置坐标轴等比例
    ax.set_box_aspect([1, 1, 1])

    # 添加坐标轴标签
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_zlabel('Z', fontsize=12)

    # 添加标题
    ax.set_title("二十面体面染色方案 (源自十二面体顶点染色)", fontsize=16, pad=20)

    # 添加网格以增强3D效果
    ax.grid(True, alpha=0.25)

    # 移除背景色
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    # 设置背景为浅灰色
    fig.patch.set_facecolor('#f0f0f0')

    return fig, ax