"""
build_dodeca_sage.py
利用 SageMath 生成标准正十二面体并导出拓扑数据
"""

import json
from sage.geometry.polyhedron.library import polytopes
from sage.all import vector
from collections import defaultdict


def main():
    # 生成单位正十二面体
    dodeca = polytopes.dodecahedron()

    # ---------- 顶点 ----------
    vertices = []
    for v in dodeca.vertices():
        vec = v.vector()
        normalized_vec = vec / vec.norm()
        vertices.append(normalized_vec)
    VERTICES = [list(map(float, v)) for v in vertices]

    # ---------- 面 ----------
    face_poly = dodeca.faces(2)
    FACES = []
    v2i = {v: i for i, v in enumerate(dodeca.vertices())}
    for f in face_poly:
        idx = [v2i[v] for v in f.vertices()]
        FACES.append(idx)

    # ---------- 顶点邻接关系（正确方法）----------
    # 使用边信息构建邻接关系
    VERTEX_ADJACENCY = [[] for _ in range(20)]

    # 收集所有边
    edges = []
    for face in FACES:
        n = len(face)
        for i in range(n):
            # 每条边连接两个顶点
            v1 = face[i]
            v2 = face[(i + 1) % n]
            # 确保边是排序的（避免重复）
            edge = tuple(sorted([v1, v2]))
            if edge not in edges:
                edges.append(edge)

    # 根据边构建邻接关系
    for v1, v2 in edges:
        VERTEX_ADJACENCY[v1].append(v2)
        VERTEX_ADJACENCY[v2].append(v1)

    # 排序每个邻居列表（可选）
    for neighbors in VERTEX_ADJACENCY:
        neighbors.sort()

    # ---------- 面邻接关系 ----------
    FACE_ADJACENCY = [[] for _ in range(12)]

    # 创建边到面的映射
    edge_to_faces = defaultdict(list)
    for face_idx, face in enumerate(FACES):
        n = len(face)
        for i in range(n):
            v1 = face[i]
            v2 = face[(i + 1) % n]
            edge = tuple(sorted([v1, v2]))
            edge_to_faces[edge].append(face_idx)

    # 根据共享边确定邻接面
    for edge, faces in edge_to_faces.items():
        if len(faces) == 2:  # 内部边连接两个面
            f1, f2 = faces
            FACE_ADJACENCY[f1].append(f2)
            FACE_ADJACENCY[f2].append(f1)

    # 排序每个邻居列表（可选）
    for neighbors in FACE_ADJACENCY:
        neighbors.sort()

    # ---------- 保存 ----------
    data = {
        "DODECAHEDRON_VERTICES": VERTICES,
        "DODECAHEDRON_FACES": FACES,
        "VERTEX_ADJACENCY": VERTEX_ADJACENCY,
        "FACE_ADJACENCY": FACE_ADJACENCY
    }
    with open("dodeca_sage.json", "w") as f:
        json.dump(data, f, indent=2)
    print("✅ 数据已写入 dodeca_sage.json")

    # ---------- 校验 ----------
    # 顶点邻居数应为3
    for i, nb in enumerate(VERTEX_ADJACENCY):
        assert len(nb) == 3, f"顶点 {i} 邻居数错误: {len(nb)} (应为3)"

    # 面邻居数应为5
    for i, nb in enumerate(FACE_ADJACENCY):
        assert len(nb) == 5, f"面 {i} 邻居数错误: {len(nb)} (应为5)"

    # 额外校验：总边数应为30 (欧拉公式: V-E+F=2 => 20-30+12=2)
    assert len(edges) == 30, f"边数错误: {len(edges)} (应为30)"

    print("✅ 校验通过！")


if __name__ == "__main__":
    main()