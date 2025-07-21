# dodecahedron/graph_utils.py
import networkx as nx
import numpy as np
from .geometry import VERTEX_ADJACENCY, FACE_ADJACENCY


def build_graph(element_type='vertex'):
    """
    构建多面体图表示
    :param element_type: 'vertex' 或 'face'
    :return: 图对象
    """
    G = nx.Graph()

    if element_type == 'vertex':
        # 顶点图
        num_elements = len(VERTEX_ADJACENCY)
        for i in range(num_elements):
            G.add_node(i)
        for i, neighbors in enumerate(VERTEX_ADJACENCY):
            for j in neighbors:
                if i < j:  # 避免重复添加边
                    G.add_edge(i, j)
    else:
        # 面图
        num_elements = len(FACE_ADJACENCY)
        for i in range(num_elements):
            G.add_node(i)
        for i, neighbors in enumerate(FACE_ADJACENCY):
            for j in neighbors:
                if i < j:  # 避免重复添加边
                    G.add_edge(i, j)

    return G


def coloring_to_labeled_graph(coloring, element_type='vertex'):
    """
    将染色方案转换为带标签的图
    :param coloring: 染色方案列表
    :param element_type: 'vertex' 或 'face'
    :return: 带标签的图对象
    """
    G = build_graph(element_type)

    # 为每个节点添加颜色标签
    for i, color in enumerate(coloring):
        G.nodes[i]['color'] = color

    return G


def are_equivalent(coloring1, coloring2, element_type='vertex'):
    """
    判断两个染色方案是否等价（图同构）
    :param coloring1: 第一个染色方案
    :param coloring2: 第二个染色方案
    :param element_type: 'vertex' 或 'face'
    :return: 是否等价
    """
    G1 = coloring_to_labeled_graph(coloring1, element_type)
    G2 = coloring_to_labeled_graph(coloring2, element_type)

    # 使用节点颜色作为同构匹配的标签
    return nx.is_isomorphic(G1, G2, node_match=lambda n1, n2: n1['color'] == n2['color'])