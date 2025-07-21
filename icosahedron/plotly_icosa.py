import numpy as np
import plotly.graph_objects as go
import colorsys, matplotlib.colors as mc

# -------------------------------------------------
# 1) 二十面体几何
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
# 2) 降饱和度 & 随机/手动颜色
# -------------------------------------------------
def random_colors(n=20, sat=0.4):
    import matplotlib.cm as cm
    base = [cm.hsv(i/n) for i in range(n)]
    return [tuple(int(255*x) for x in colorsys.hsv_to_rgb(h, s*sat, v))
            for h, s, v in (colorsys.rgb_to_hsv(*c[:3]) for c in base)]

colors = [f'rgb{c}' for c in random_colors()]   # 可替换为手动列表

# -------------------------------------------------
# 3) 绘制（白色背景、强光照、投影、实心）
# -------------------------------------------------
fig = go.Figure()

for face, clr in zip(FACES, colors):
    tri = VERTICES[face]
    fig.add_trace(go.Mesh3d(
        x=tri[:,0], y=tri[:,1], z=tri[:,2],
        i=[0], j=[1], k=[2],
        color=clr,
        opacity=1.0,                         # 实心
        flatshading=False,                   # 平滑
        lighting=dict(
            ambient=0.25,                   # 更低环境光
            diffuse=0.7,
            specular=0.9,                   # 更高镜面光
            roughness=0.3,
            fresnel=0.4
        ),
        lightposition=dict(x=200, y=200, z=300)
    ))

fig.update_layout(
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        bgcolor='white',                    # 白色背景
        aspectmode='cube',
        camera=dict(
            eye=dict(x=1.8, y=1.8, z=1.8)  # 拉远视角，投影更明显
        ),
        # 启用阴影（Plotly 5.14+ 支持）
        dragmode='orbit'
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    showlegend=False
)

fig.show()
fig.write_html("icosa_white_shadow.html")
print("已保存：icosa_white_shadow.html")