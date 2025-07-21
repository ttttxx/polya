import time
import sys
import os
import pickle
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from dodecahedron.group_generation import generate_symmetry_group
from dodecahedron.coloring import count_colorings, get_all_colorings, save_colorings_to_file
from dodecahedron.visualization import visualize_vertex_coloring, visualize_face_coloring, \
    visualize_dodecahedron_rotation
from dodecahedron.utils import create_color_mapping, BASIC_COLORS


# 二十面体顶点和面定义
def create_icosahedron():
    """创建正二十面体的顶点和面"""
    # 黄金分割比例
    phi = (1 + np.sqrt(5)) / 2

    # 12个顶点
    vertices = np.array([
        [0, 1, phi], [0, -1, phi], [0, 1, -phi], [0, -1, -phi],
        [1, phi, 0], [-1, phi, 0], [1, -phi, 0], [-1, -phi, 0],
        [phi, 0, 1], [-phi, 0, 1], [phi, 0, -1], [-phi, 0, -1]
    ])

    # 规范化顶点到单位球面
    vertices /= np.linalg.norm(vertices[0])

    # 20个三角形面
    faces = [
        [0, 1, 4], [0, 4, 8], [0, 8, 9], [0, 9, 5], [0, 5, 1],
        [1, 5, 7], [1, 7, 11], [1, 11, 4], [4, 11, 10], [4, 10, 8],
        [8, 10, 2], [8, 2, 9], [9, 2, 6], [9, 6, 5], [5, 6, 7],
        [2, 10, 3], [10, 11, 3], [11, 7, 3], [7, 6, 3], [6, 2, 3]
    ]

    return vertices, faces


# 全局变量
ICOSAHEDRON_VERTICES, ICOSAHEDRON_FACES = create_icosahedron()

from matplotlib.colors import to_rgba  # 确保导入这个模块


def visualize_icosa_face_from_dodeca_vertex(color_mapping, coloring_dodeca_vertex, ax=None):
    """
    将十二面体顶点染色方案转化为二十面体面染色方案并可视化

    参数:
        color_mapping: 颜色名称到颜色值的映射
        coloring_dodeca_vertex: 十二面体顶点染色方案 (20个颜色)
        ax: 可选的matplotlib坐标轴对象
    """
    # 建立十二面体顶点到二十面体面的映射
    # 每个十二面体顶点对应一个二十面体面
    face_centers = [np.mean(ICOSAHEDRON_VERTICES[face], axis=0) for face in ICOSAHEDRON_FACES]

    # 创建面集合
    faces = []
    rgba_colors = []  # 存储带有透明度的RGBA颜色

    # 计算每个面的颜色
    for face_idx, face in enumerate(ICOSAHEDRON_FACES):
        face_vertices = ICOSAHEDRON_VERTICES[face]
        faces.append(face_vertices)

        # 获取对应的十二面体顶点颜色
        color_name = coloring_dodeca_vertex[face_idx]
        base_color = color_mapping.get(color_name, color_name)

        # 添加透明度（根据深度调整）
        depth = np.mean(face_vertices[:, 2])
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


def animate_icosa_face_coloring(color_mapping, coloring):
    """可视化二十面体的旋转动画"""
    fig, ax = visualize_icosa_face_from_dodeca_vertex(color_mapping, coloring)

    def update(frame):
        ax.view_init(elev=25, azim=frame)
        return ax.collections

    ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 2), interval=50, blit=True)
    plt.show()
    return ani


def main():
    # 只进行顶点染色
    print("只进行十二面体顶点染色 (20个顶点)")
    mode = 1  # 固定为顶点染色模式

    n_elements = 20
    element_name = "顶点"
    symmetry_mode = 'vertex'
    element_type = 'vertex'

    # 尝试从本地文件加载对称群
    cache_filename = f"{symmetry_mode}_symmetry_group.pkl"
    if os.path.exists(cache_filename):
        with open(cache_filename, 'rb') as f:
            perm_group = pickle.load(f)
        print(f"已从本地文件加载对称群 ({len(perm_group)} 个对称操作)")
    else:
        # 生成对称群
        start_time = time.time()
        print(f"正在生成对称群...")
        perm_group = generate_symmetry_group(symmetry_mode)
        print(f"已生成对称群 ({len(perm_group)} 个对称操作), 耗时: {time.time() - start_time:.2f}秒")

        # 将对称群保存到本地文件
        with open(cache_filename, 'wb') as f:
            pickle.dump(perm_group, f)
        print(f"已将对称群保存到本地文件: {cache_filename}")

    # 用户输入颜色和数量
    color_names = []
    color_counts = []
    total_count = 0
    try:
        n = int(input(f"\n输入颜色种类数 (用于{n_elements}个{element_name}): "))
    except ValueError:
        print("无效输入! 请输入整数")
        sys.exit(1)

    print("\n可用的基础颜色: " + ", ".join(BASIC_COLORS.keys()))
    print("或使用任何有效的颜色名称\n")

    for i in range(n):
        name = input(f"输入颜色#{i + 1}的名称 (如'红'或'blue'): ").strip()
        try:
            count = int(input(f"输入颜色#{i + 1}的数量: "))
        except ValueError:
            print("无效输入! 请输入整数")
            sys.exit(1)
        color_names.append(name)
        color_counts.append(count)
        total_count += count

    if total_count != n_elements:
        print(
            f"输入的颜色数量总和 ({total_count}) 不等于 {n_elements} 个{element_name}，请重新运行程序并输入正确的数量。")
        sys.exit(1)

    # 创建颜色映射
    color_mapping = create_color_mapping(color_names)
    for name, color_val in color_mapping.items():
        print(f"  {name} 映射到: {color_val}")

    # 计算并显示方案数
    total = count_colorings(color_names, perm_group, color_counts)
    print(f"\n所有不等价染色方案数: {total}")

    # 枚举所有具体方案（仅当方案数合理时）
    if total > 1000:
        print(f"\n警告: 不等价方案数 ({total}) 较大，可能需要较长时间")
        print("是否继续枚举具体方案? (y/n)")
        choice = input().strip().lower()
        if choice != 'y':
            print("已跳过具体方案枚举")
            all_reps = []
        else:
            print(f"\n开始枚举所有 {total} 个不等价方案...")
            start_time = time.time()
            all_reps = get_all_colorings(color_names, perm_group, color_counts)
    else:
        print(f"\n开始枚举所有 {total} 个不等价方案...")
        start_time = time.time()
        all_reps = get_all_colorings(color_names, perm_group, color_counts)

    # 显示前5个方案
    if all_reps:
        print("\n前5个代表方案:")
        for i, coloring in enumerate(all_reps[:5]):
            print(f"方案{i + 1}: {'-'.join(coloring[:min(8, len(coloring))])}{'...' if len(coloring) > 8 else ''}")

        # 保存所有方案到文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{element_type}_colorings_{timestamp}.txt"
        save_colorings_to_file(all_reps, filename, element_type)

        # 询问用户是否可视化指定方案
        print("\n是否可视化指定方案? (y/n)")
        if input().strip().lower() == 'y':
            while True:
                try:
                    scheme_num = input(f"请输入要可视化的方案编号 (1 - {len(all_reps)}, 输入 'q' 退出): ")
                    if scheme_num.lower() == 'q':
                        break
                    scheme_num = int(scheme_num)
                    if 1 <= scheme_num <= len(all_reps):
                        coloring = all_reps[scheme_num - 1]

                        # 可视化二十面体面染色（源自十二面体顶点染色）
                        fig, ax = visualize_icosa_face_from_dodeca_vertex(color_mapping, coloring)

                        # 保存可视化结果为图片
                        img_filename = f"icosa_face_coloring_{timestamp}_scheme_{scheme_num}.png"
                        plt.savefig(img_filename, dpi=150, bbox_inches='tight')
                        print(f"已保存可视化结果为: {img_filename}")

                        plt.show()

                    else:
                        print("输入的方案编号超出范围，请输入有效编号。")
                except ValueError:
                    print("输入无效，请输入一个整数或 'q' 退出。")
    else:
        print("\n未生成具体方案列表")


if __name__ == "__main__":
    main()