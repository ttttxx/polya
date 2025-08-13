"""
把「十二面体 20 顶点染色方案」直接映射到「二十面体 20 个面」
并在浏览器中交互展示。

使用方法：
    python plotly_dodeca_from_icosa.py
"""
import numpy as np
import plotly.graph_objects as go
import colorsys, matplotlib.colors as mc
import sys, os, re, glob
from datetime import datetime
from dodecahedron.utils import BASIC_COLORS

# -------------------------------------------------
# 1. 二十面体几何
# -------------------------------------------------
def create_dodecahedron():
    # 黄金比例
    phi = (1 + np.sqrt(5)) / 2

    # 正十二面体的顶点坐标 (20个顶点)
    vertices = np.array([
        # 第一组：(±1, ±1, ±1) 的奇偶排列（含奇数个负号）
        [1, 1, 1], [1, 1, -1], [1, -1, 1], [1, -1, -1],
        [-1, 1, 1], [-1, 1, -1], [-1, -1, 1], [-1, -1, -1],
        # 第二组：(0, ±1/φ, ±φ) 的偶置换
        [0, 1 / phi, phi], [0, 1 / phi, -phi], [0, -1 / phi, phi], [0, -1 / phi, -phi],
        # 第三组：(±φ, 0, ±1/φ) 的偶置换
        [phi, 0, 1 / phi], [phi, 0, -1 / phi], [-phi, 0, 1 / phi], [-phi, 0, -1 / phi],
        # 第四组：(±1/φ, ±φ, 0) 的偶置换
        [1 / phi, phi, 0], [1 / phi, -phi, 0], [-1 / phi, phi, 0], [-1 / phi, -phi, 0]
    ], dtype=float)

    # 将所有顶点归一化（单位球面）
    vertices = vertices / np.linalg.norm(vertices[0])

    # 定义正十二面体的面（12个五边形面）
    faces = [
        # 第一个五边形面（上方）
        [0, 8, 10, 2, 16],
        # 第二个五边形面（下方）
        [3, 11, 9, 1, 17],
        # 连接上方和下方的侧面（共10个面）
        [0, 16, 18, 4, 8],
        [8, 4, 14, 12, 10],
        [10, 12, 6, 2, 16],
        [2, 6, 19, 17, 3],
        [3, 17, 1, 15, 19],
        [1, 9, 5, 15, 17],
        [9, 11, 7, 13, 5],
        [11, 3, 19, 7, 13],
        [7, 19, 15, 5, 13],
        [14, 6, 19, 15, 5]
    ]


    return vertices, faces


VERTICES, FACES = create_dodecahedron()

# -------------------------------------------------
# 2) 颜色降饱和度
# -------------------------------------------------
def desaturate(c, factor=0.6):
    r, g, b = mc.to_rgb(c)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    s *= factor
    return colorsys.hsv_to_rgb(h, s, v)

# -------------------------------------------------
# 3) 读取 txt
# -------------------------------------------------
def load_colorings_from_txt(txt_path):
    colorings = []
    with open(txt_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith("Class"):  # 改为根据 Class 解析
                try:
                    # 获取颜色字符串，去除 "Class xxx: " 这一部分
                    colors_str = line.split(":", 1)[1].strip()
                    colorings.append(colors_str.split())
                except Exception:
                    continue
    return colorings


# -------------------------------------------------
# 4) 主程序：选文件 → 选方案 → 绘图
# -------------------------------------------------
def main():
    folder = os.path.join(os.path.dirname(__file__), "..", "icosahedron/result")
    pattern = os.path.join(folder, "vertex_colorings_*.txt")
    files = sorted(glob.glob(pattern))

    if not files:
        print(f"在 {folder}/ 目录下没有找到 vertex_colorings_*.txt")
        sys.exit(1)

    print("找到以下顶点染色文件：")
    for idx, fp in enumerate(files, 1):
        print(f"  {idx}: {os.path.basename(fp)}")

    try:
        file_idx = int(input("\n选择要加载的文件编号：")) - 1
        txt_path = files[file_idx]
    except (ValueError, IndexError):
        print("输入错误"); sys.exit(1)

    colorings = load_colorings_from_txt(txt_path)
    if not colorings:
        print("该文件没有可解析的方案")
        sys.exit(1)

    print("\n共读取到方案：", len(colorings))
    show_n = min(len(colorings), 5)
    for idx, c in enumerate(colorings[:show_n], 1):
        print(f"方案 {idx}: {'-'.join(c)}")

    try:
        scheme_idx = int(input(f"\n输入要展示的方案编号(1-{len(colorings)})："))
        coloring = colorings[scheme_idx - 1]
    except (ValueError, IndexError):
        print("输入错误"); sys.exit(1)

    # 颜色映射
    color_map = BASIC_COLORS
    rgb_colors = [f"rgb{tuple(int(255*x) for x in desaturate(color_map.get(c, c)))}"
                  for c in coloring]

    # -------------------------------------------------
    # 5) Plotly 绘图
    # -------------------------------------------------
    fig = go.Figure()
    for face, clr in zip(FACES, rgb_colors):
        tri = VERTICES[face]
        fig.add_trace(go.Mesh3d(
            x=tri[:,0], y=tri[:,1], z=tri[:,2],
            i=[0], j=[1], k=[2],
            color=clr,
            opacity=1.0,
            flatshading=False,
            lighting=dict(
                ambient=0.2, diffuse=0.8, specular=0.9,
                roughness=0.25, fresnel=0.5
            ),
            lightposition=dict(x=300, y=300, z=200)
        ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            bgcolor='white',
            aspectmode='cube',
            camera=dict(eye=dict(x=2, y=2, z=2))
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )

    ts = datetime.now().strftime("%H%M%S")
    html_name = f"dodeca_face_{os.path.splitext(os.path.basename(txt_path))[0]}_scheme{scheme_idx}_{ts}.html"
    fig.write_html(html_name)
    print(f"已保存 {html_name}")
    fig.show()

if __name__ == "__main__":
    main()