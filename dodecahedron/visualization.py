# dodecahedron/visualization.py
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgba
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation  # 导入动画库

from .geometry import DODECAHEDRON_VERTICES, DODECAHEDRON_FACES


def visualize_vertex_coloring(color_mapping, coloring, ax=None):
    """可视化正十二面体的顶点染色方案 - 表面优化版"""
    vertices = DODECAHEDRON_VERTICES

    if ax is None:
        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = fig.add_subplot(111, projection='3d')
    else:
        fig = ax.figure

    # 设置视角以获得更好的3D效果
    ax.view_init(elev=30, azim=45)

    # 创建面集合（只显示表面）
    faces = []
    for face_indices in DODECAHEDRON_FACES:
        face_vertices = vertices[face_indices]
        faces.append(face_vertices)

    # 绘制表面（无填充，只显示边缘）
    surface = Poly3DCollection(faces, alpha=0.0, linewidths=1.0, edgecolors='gray')
    ax.add_collection3d(surface)

    # 绘制顶点（更大更明显）
    for i, color_name in enumerate(coloring):
        valid_color = color_mapping.get(color_name, color_name)
        x, y, z = vertices[i]
        ax.scatter(x, y, z, color=valid_color, s=180, depthshade=True,
                   edgecolors='k', linewidths=1.2, zorder=10)

    # 设置坐标轴属性
    max_range = 1.2
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    ax.set_zlim(-max_range, max_range)

    # 添加坐标轴标签
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_zlabel('Z', fontsize=12)

    # 添加标题
    ax.set_title("正十二面体顶点染色方案", fontsize=16, pad=20)

    # 添加网格以增强3D效果
    ax.grid(True, alpha=0.2)

    # 移除背景色
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    return fig, ax


def visualize_face_coloring(color_mapping, coloring, ax=None):
    """可视化正十二面体的面染色方案 - 表面优化版"""
    vertices = DODECAHEDRON_VERTICES

    if ax is None:
        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = fig.add_subplot(111, projection='3d')
    else:
        fig = ax.figure

    # 设置视角以获得更好的3D效果
    ax.view_init(elev=30, azim=45)

    # 按深度排序面以确保正确渲染
    face_centers = [np.mean(vertices[face], axis=0) for face in DODECAHEDRON_FACES]
    sorted_faces = sorted(enumerate(DODECAHEDRON_FACES),
                          key=lambda x: face_centers[x[0]][2],
                          reverse=True)

    # 创建面集合
    faces = []
    colors = []
    alphas = []

    for face_idx, face in sorted_faces:
        face_vertices = vertices[face]
        faces.append(face_vertices)

        face_color_name = coloring[face_idx]
        face_color = to_rgba(color_mapping.get(face_color_name, face_color_name))

        # 添加透明度（根据深度调整）
        depth = face_centers[face_idx][2]
        alpha = max(0.6, 0.9 - abs(depth) * 0.2)
        colors.append(face_color[:3])
        alphas.append(alpha)

    # 绘制面（只显示表面）
    surface = Poly3DCollection(faces, alpha=alphas, linewidths=1.0, edgecolors='k')
    surface.set_facecolor(colors)
    ax.add_collection3d(surface)

    # 设置坐标轴属性
    max_range = 1.2
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    ax.set_zlim(-max_range, max_range)

    # 添加坐标轴标签
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_zlabel('Z', fontsize=12)

    # 添加标题
    ax.set_title("正十二面体面染色方案", fontsize=16, pad=20)

    # 添加网格以增强3D效果
    ax.grid(True, alpha=0.2)

    # 移除背景色
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False

    return fig, ax


def visualize_dodecahedron_rotation(color_mapping, coloring, mode='face'):
    """可视化正十二面体的旋转动画"""
    if mode == 'face':
        fig, ax = visualize_face_coloring(color_mapping, coloring)
    else:
        fig, ax = visualize_vertex_coloring(color_mapping, coloring)

    def update(frame):
        ax.view_init(elev=30, azim=frame)
        return ax.collections

    ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 2), interval=50, blit=True)
    plt.show()
    return ani