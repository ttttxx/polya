"""
把「十二面体 20 顶点染色方案」直接映射到「二十面体 20 个面」
并在浏览器中交互展示。
使用方法：
    python plotly_icosa_from_dodeca.py
随后按提示输入即可。
"""
import numpy as np
import plotly.graph_objects as go
import colorsys, matplotlib.colors as mc
import sys, os, pickle
from datetime import datetime
# 复用你已有的工具
from dodecahedron.coloring import get_all_colorings
from dodecahedron.utils import create_color_mapping

# -------------------------------------------------
# 1. 二十面体几何（与之前定义一致）
# -------------------------------------------------
def create_icosahedron():
    phi = (1 + np.sqrt(5)) / 2
    vertices = np.array([
        [-1, phi, 0], [1, phi, 0], [-1, -phi, 0], [1, -phi, 0],
        [0, -1, phi], [0, 1, phi], [0, -1, -phi], [0, 1, -phi],
        [phi, 0, -1], [phi, 0, 1], [-phi, 0, -1], [-phi, 0, 1]
    ])
    vertices = vertices / np.linalg.norm(vertices[0])
    faces = [
        [0,11,5],[0,5,1],[0,1,7],[0,7,10],[0,10,11],
        [1,5,9],[5,11,4],[11,10,2],[10,7,6],[7,1,8],
        [3,9,4],[3,4,2],[3,2,6],[3,6,8],[3,8,9],
        [4,9,5],[2,4,11],[6,2,10],[8,6,7],[9,8,1]
    ]
    return vertices, faces

VERTICES, FACES = create_icosahedron()

# -------------------------------------------------
# 2) 颜色降饱和度函数
# -------------------------------------------------
def desaturate(c, factor=0.6):
    r, g, b = mc.to_rgb(c)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    s *= factor
    return colorsys.hsv_to_rgb(h, s, v)

# -------------------------------------------------
# 3) 主函数：读取方案 → 映射 → 绘图
# -------------------------------------------------
def main():
    cache_file = "vertex_symmetry_group.pkl"
    if not os.path.exists(cache_file):
        print("请先运行原程序生成 vertex_symmetry_group.pkl")
        sys.exit(1)

    with open(cache_file, "rb") as f:
        perm_group = pickle.load(f)

    print("沿用原程序的颜色配置：")
    color_names = ["r", "b"]          # 或根据你实际输入改动
    color_counts = [5, 15]            # 示例：5红 15蓝，总和=20
    color_mapping = create_color_mapping(color_names)

    all_reps = get_all_colorings(color_names, perm_group, color_counts)

    print("\n共有方案：", len(all_reps))
    show_n = min(len(all_reps), 5)
    for idx, coloring in enumerate(all_reps[:show_n], 1):
        print(f"方案 {idx}: {'-'.join(coloring)}")

    try:
        sel = int(input(f"\n输入要展示的方案编号(1-{len(all_reps)})："))
        coloring = all_reps[sel-1]
    except (ValueError, IndexError):
        print("输入错误"); sys.exit(1)

    # 把 20 种颜色映射为 RGB
    rgb_colors = [f"rgb{tuple(int(255*x) for x in desaturate(color_mapping.get(c,c)))}"
                  for c in coloring]

    # -------------------------------------------------
    # 4) Plotly 绘图
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
                ambient=0.2,
                diffuse=0.8,
                specular=0.9,
                roughness=0.25,
                fresnel=0.5
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
        margin=dict(l=0,r=0,t=0,b=0),
        showlegend=False
    )

    ts = datetime.now().strftime("%H%M%S")
    html_name = f"icosa_face_scheme_{sel}_{ts}.html"
    fig.write_html(html_name)
    print(f"已保存 {html_name}")
    fig.show()

if __name__ == "__main__":
    main()