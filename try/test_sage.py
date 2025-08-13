from z3 import *
import itertools
from sage.all import *


class PolyhedronCounter:
    def __init__(self, polyhedron, obj_type):
        """
        通用多面体染色计数器

        :param polyhedron: SageMath 多面体对象
        :param obj_type: 'face'(面), 'edge'(边), 'vertex'(顶点)
        """
        self.poly = polyhedron
        self.obj_type = obj_type
        self.n, self.objects = self._get_objects()
        self.symmetry_group = self._generate_symmetries()
        print(f"已生成 {len(self.symmetry_group)} 个对称操作")

    def _get_objects(self):
        """获取多面体对象（面/边/顶点）及其索引"""
        if self.obj_type == 'face':
            faces = self.poly.faces(2)
            return len(faces), [frozenset(v.index() for v in face.vertices()) for face in faces]
        elif self.obj_type == 'edge':
            edges = []
            for edge in self.poly.faces(1):
                vertices = tuple(sorted(v.index() for v in edge.vertices()))
                edges.append(vertices)
            return len(edges), edges
        else:  # vertex
            return len(self.poly.vertices()), list(range(len(self.poly.vertices())))

    def _generate_symmetries(self):
        """使用 SageMath 生成旋转对称群"""
        # 获取旋转对称群（仅保持方向的对称）
        G = self.poly.restricted_automorphism_group(output='permutation', orientation_preserving=True)

        # 将对称操作转换为对象置换
        symmetries = []
        for g in G:
            if self.obj_type == 'vertex':
                symmetries.append(list(g))
            elif self.obj_type == 'face':
                # 创建面的置换
                face_perm = [-1] * self.n
                for i, face_set in enumerate(self.objects):
                    # 应用对称变换到面的顶点
                    transformed_set = frozenset(g(v) for v in face_set)
                    # 查找变换后的面对应哪个面
                    for j, target_set in enumerate(self.objects):
                        if transformed_set == target_set:
                            face_perm[i] = j
                            break
                symmetries.append(face_perm)
            else:  # edge
                # 创建边的置换
                edge_perm = [-1] * self.n
                for i, (v1, v2) in enumerate(self.objects):
                    # 应用对称变换到边的顶点
                    new_v1, new_v2 = g(v1), g(v2)
                    # 标准化边表示（排序顶点）
                    new_edge = tuple(sorted((new_v1, new_v2)))
                    # 查找变换后的边
                    for j, target_edge in enumerate(self.objects):
                        if new_edge == target_edge:
                            edge_perm[i] = j
                            break
                symmetries.append(edge_perm)

        return symmetries

    def count_colorings(self, color_counts):
        """计算满足颜色分配条件的染色方案数"""
        s = Solver()
        colors = [Int(f'c_{i}') for i in range(self.n)]

        # 约束1：每个对象的颜色在合法范围内
        for c in colors:
            s.add(c >= 0, c < len(color_counts))

        # 约束2：颜色使用次数限制
        for col_idx, cnt in enumerate(color_counts):
            s.add(sum([If(c == col_idx, 1, 0) for c in colors]) == cnt)

        # 约束3：对称性规约（选择字典序最小的代表元）
        for sym in self.symmetry_group:
            sym_colors = [colors[i] for i in sym]
            s.add(self.lex_le(colors, sym_colors))

        # 解计数
        count = 0
        while s.check() == sat:
            count += 1
            model = s.model()
            # 添加排除当前解的约束
            s.add(Or([c != model[c] for c in colors]))

        return count

    def lex_le(self, v1, v2):
        """生成字典序 v1 <= v2 的约束"""
        constraints = []
        n = len(v1)

        # 相等的情况
        constraints.append(And([v1[i] == v2[i] for i in range(n)]))

        # 在某个位置首次小于的情况
        for i in range(n):
            prefix_eq = [v1[j] == v2[j] for j in range(i)]
            constraints.append(And(prefix_eq + [v1[i] < v2[i]]))

        return Or(constraints)


# 示例：立方体染色计算
if __name__ == "__main__":
    # 使用 SageMath 创建立方体
    cube = polytopes.cube()

    # 面染色：两种颜色各3面
    print("=== 立方体面染色 ===")
    face_counter = PolyhedronCounter(cube, 'face')
    print(f"两种颜色各3面: {face_counter.count_colorings([3, 3])} 种方案")  # 应输出10

    # 边染色：三种颜色各4条边
    print("\n=== 立方体边染色 ===")
    edge_counter = PolyhedronCounter(cube, 'edge')
    print(f"三种颜色各4条边: {edge_counter.count_colorings([4, 4, 4])} 种方案")  # 应输出218

    # 顶点染色：两种颜色各4个顶点
    print("\n=== 立方体顶点染色 ===")
    vertex_counter = PolyhedronCounter(cube, 'vertex')
    print(f"两种颜色各4个顶点: {vertex_counter.count_colorings([4, 4])} 种方案")  # 应输出5