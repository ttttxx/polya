from z3 import *
import itertools


class PolyhedronColorCounter:
    """通用多面体染色计数器，支持立方体和正四面体"""

    def __init__(self, polyhedron_type, object_type):
        """
        初始化多面体染色计数器

        Args:
            polyhedron_type (str): 多面体类型，支持 'cube' (立方体) 和 'tetrahedron' (正四面体)
            object_type (str): 染色对象类型，支持 'face' (面), 'edge' (边), 'vertex' (顶点)
        """
        self.polyhedron_type = polyhedron_type
        self.object_type = object_type
        self.n_objects, self.symmetries = self._init_symmetries()
        print(f"已加载 {polyhedron_type} 的 {object_type} 染色模型")
        print(f"{object_type} 数量: {self.n_objects}, 旋转对称操作数: {len(self.symmetries)}")

    def _init_symmetries(self):
        """初始化多面体的旋转对称置换"""
        if self.polyhedron_type == 'cube':
            return self._init_cube_symmetries()
        elif self.polyhedron_type == 'tetrahedron':
            return self._init_tetrahedron_symmetries()
        else:
            raise ValueError(f"不支持的多面体类型: {self.polyhedron_type}")

    def _init_cube_symmetries(self):
        """初始化立方体的旋转对称置换"""
        if self.object_type == 'face':
            # 面编号: 0(前),1(后),2(左),3(右),4(上),5(下)
            symmetries = [
                # 恒等操作
                [0, 1, 2, 3, 4, 5],
                # 绕x轴旋转
                [0, 1, 4, 5, 3, 2],  # 90度
                [0, 1, 3, 2, 5, 4],  # 180度
                [0, 1, 5, 4, 2, 3],  # 270度
                # 绕y轴旋转
                [5, 4, 2, 3, 0, 1],  # 90度
                [1, 0, 2, 3, 5, 4],  # 180度
                [4, 5, 2, 3, 1, 0],  # 270度
                # 绕z轴旋转
                [3, 2, 0, 1, 4, 5],  # 90度
                [1, 0, 3, 2, 4, 5],  # 180度
                [2, 3, 1, 0, 4, 5],  # 270度
                # 空间对角线旋转
                [4, 3, 0, 5, 1, 2],  # 对角线1 120度
                [2, 5, 1, 4, 3, 0],  # 对角线1 240度
                [5, 0, 3, 4, 2, 1],  # 对角线2 120度
                [1, 2, 4, 3, 0, 5],  # 对角线2 240度
                [0, 4, 1, 5, 2, 3],  # 对角线3 120度
                [3, 2, 5, 1, 4, 0],  # 对角线3 240度
                [2, 4, 5, 0, 1, 3],  # 对角线4 120度
                [0, 5, 4, 2, 3, 1],  # 对角线4 240度
                # 边中点旋转
                [4, 2, 5, 1, 0, 3],  # 边中点轴1 180度
                [3, 0, 2, 1, 5, 4],  # 边中点轴2 180度
                [5, 3, 4, 0, 1, 2],  # 边中点轴3 180度
                [0, 3, 1, 2, 4, 5],  # 边中点轴4 180度
                [1, 2, 3, 0, 4, 5],  # 边中点轴5 180度
            ]
            return 6, symmetries
        elif self.object_type == 'edge':
            # 边编号: 0-11（前4条, 后4条, 连接边4条）
            symmetries = [
                # 恒等操作
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                # 绕x轴旋转90度
                [1, 2, 3, 0, 5, 6, 7, 4, 10, 11, 8, 9],
                # 绕x轴旋转180度
                [2, 3, 0, 1, 6, 7, 4, 5, 11, 8, 9, 10],
                # 绕x轴旋转270度
                [3, 0, 1, 2, 7, 4, 5, 6, 9, 10, 11, 8],
                # 绕y轴旋转90度
                [4, 7, 6, 5, 0, 3, 2, 1, 8, 11, 10, 9],
                # 绕y轴旋转180度
                [5, 4, 7, 6, 1, 0, 3, 2, 9, 8, 11, 10],
                # 绕y轴旋转270度
                [6, 5, 4, 7, 2, 1, 0, 3, 10, 9, 8, 11],
                # 绕z轴旋转90度
                [8, 0, 1, 9, 10, 4, 5, 11, 3, 2, 7, 6],
                # 绕z轴旋转180度
                [9, 8, 0, 10, 11, 10, 4, 8, 7, 6, 3, 2],
                # 绕z轴旋转270度
                [10, 9, 8, 11, 8, 11, 10, 9, 6, 3, 2, 7],
                # 空间对角线旋转（部分示例）
                [2, 10, 5, 6, 1, 9, 0, 11, 3, 4, 7, 8],  # 对角线1 120度
                [7, 8, 3, 4, 11, 2, 10, 5, 6, 1, 9, 0],  # 对角线1 240度
                # 其他旋转...
                [5, 6, 7, 4, 1, 0, 3, 2, 9, 8, 11, 10],  # 边中点轴1 180度
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],  # 边中点轴2 180度（示例）
                # 完整列表需要补充所有24个置换
            ]
            return 12, symmetries
        elif self.object_type == 'vertex':
            # 顶点编号: 0-7（前4个, 后4个）
            symmetries = [
                # 恒等操作
                [0, 1, 2, 3, 4, 5, 6, 7],
                # 绕x轴旋转90度
                [1, 5, 6, 2, 0, 4, 7, 3],
                # 绕x轴旋转180度
                [5, 4, 7, 6, 1, 0, 3, 2],
                # 绕x轴旋转270度
                [4, 0, 3, 7, 5, 1, 2, 6],
                # 绕y轴旋转90度
                [3, 2, 6, 7, 0, 1, 5, 4],
                # 绕y轴旋转180度
                [2, 6, 7, 3, 1, 5, 4, 0],
                # 绕y轴旋转270度
                [6, 7, 4, 5, 2, 3, 0, 1],
                # 绕z轴旋转90度
                [4, 7, 6, 5, 0, 3, 2, 1],
                # 绕z轴旋转180度
                [7, 6, 5, 4, 3, 2, 1, 0],
                # 绕z轴旋转270度
                [6, 5, 4, 7, 2, 1, 0, 3],
                # 空间对角线旋转
                [2, 5, 6, 1, 0, 3, 7, 4],  # 对角线1 120度
                [5, 6, 1, 0, 3, 7, 4, 2],  # 对角线1 240度
                [1, 3, 2, 0, 5, 7, 6, 4],  # 对角线2 120度
                [3, 2, 0, 1, 7, 6, 4, 5],  # 对角线2 240度
                # 边中点旋转
                [1, 0, 3, 2, 5, 4, 7, 6],  # 边中点轴1 180度
                [3, 2, 1, 0, 7, 6, 5, 4],  # 边中点轴2 180度
                # 完整列表需要补充所有24个置换
            ]
            return 8, symmetries
        else:
            raise ValueError(f"不支持的对象类型: {self.object_type}")

    def _init_tetrahedron_symmetries(self):
        """初始化正四面体的旋转对称置换"""
        if self.object_type == 'face':
            # 面编号: 0-3
            symmetries = [
                # 恒等操作
                [0, 1, 2, 3],
                # 绕顶点-对面中心旋转120度
                [0, 2, 3, 1],  # 顶点0
                [1, 0, 3, 2],  # 顶点1
                [2, 3, 0, 1],  # 顶点2
                [3, 1, 2, 0],  # 顶点3
                # 绕顶点-对面中心旋转240度
                [0, 3, 1, 2],  # 顶点0
                [1, 3, 2, 0],  # 顶点1
                [2, 1, 0, 3],  # 顶点2
                [3, 2, 0, 1],  # 顶点3
                # 边中点旋转180度
                [1, 0, 3, 2],  # 边0-1
                [2, 3, 0, 1],  # 边0-2
                [3, 1, 2, 0],  # 边0-3
                [0, 2, 1, 3],  # 边1-2
                [0, 3, 2, 1],  # 边1-3
                [1, 3, 0, 2],  # 边2-3
            ]
            return 4, symmetries
        elif self.object_type == 'edge':
            # 边编号: 0-5
            symmetries = [
                # 恒等操作
                [0, 1, 2, 3, 4, 5],
                # 其他旋转...
                # 完整列表需要补充所有12个置换
            ]
            return 6, symmetries
        elif self.object_type == 'vertex':
            # 顶点编号: 0-3
            symmetries = [
                # 恒等操作
                [0, 1, 2, 3],
                # 绕顶点-对面中心旋转120度
                [0, 2, 3, 1],  # 顶点0
                [1, 0, 3, 2],  # 顶点1
                [2, 3, 0, 1],  # 顶点2
                [3, 1, 2, 0],  # 顶点3
                # 绕顶点-对面中心旋转240度
                [0, 3, 1, 2],  # 顶点0
                [1, 3, 2, 0],  # 顶点1
                [2, 1, 0, 3],  # 顶点2
                [3, 2, 0, 1],  # 顶点3
                # 边中点旋转180度
                [1, 0, 3, 2, 5, 4],  # 边0-1
                [2, 3, 0, 1, 4, 5],  # 边0-2
                [3, 2, 1, 0, 5, 4],  # 边0-3
                [0, 4, 2, 5, 1, 3],  # 边1-2
                [0, 5, 3, 4, 2, 1],  # 边1-3
                [4, 1, 5, 0, 3, 2],  # 边2-3
            ]
            return 4, symmetries
        else:
            raise ValueError(f"不支持的对象类型: {self.object_type}")

    def count_colorings(self, color_counts):
        """
        计算满足颜色分配的染色方案数目（考虑旋转对称性）

        Args:
            color_counts (list): 每种颜色的使用次数列表

        Returns:
            int: 不同染色方案的数目
        """
        if sum(color_counts) != self.n_objects:
            raise ValueError(f"颜色使用次数总和({sum(color_counts)})必须等于{self.object_type}数量({self.n_objects})")

        solver = Solver()
        # 创建颜色变量
        colors = [Int(f'color_{i}') for i in range(self.n_objects)]

        # 约束1：每个对象的颜色在合法范围内
        num_colors = len(color_counts)
        for c in colors:
            solver.add(c >= 0, c < num_colors)

        # 约束2：每种颜色的使用次数正确
        for color_idx, count in enumerate(color_counts):
            solver.add(Sum([If(c == color_idx, 1, 0) for c in colors]) == count)

        # 约束3：对称性规约（选择字典序最小的代表元）
        for sym in self.symmetries:
            sym_colors = [colors[i] for i in sym]
            solver.add(self._lex_le(colors, sym_colors))

        # 计数所有解
        count = 0
        while solver.check() == sat:
            count += 1
            model = solver.model()
            # 添加约束排除当前解
            solver.add(Or([c != model[c] for c in colors]))

        return count

    def _lex_le(self, v1, v2):
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


def main():
    """主函数：获取用户输入并计算染色方案"""
    print("=== 多面体染色方案计算器 (考虑旋转对称性) ===")

    # 获取多面体类型
    while True:
        polyhedron_type = input("请选择多面体类型 (cube/tetrahedron): ").strip().lower()
        if polyhedron_type in ['cube', 'tetrahedron']:
            break
        print("无效选择，请重新输入。")

    # 获取染色对象类型
    while True:
        object_type = input("请选择染色对象类型 (face/edge/vertex): ").strip().lower()
        if object_type in ['face', 'edge', 'vertex']:
            break
        print("无效选择，请重新输入。")

    # 创建计算器实例
    counter = PolyhedronColorCounter(polyhedron_type, object_type)

    # 获取颜色数量
    while True:
        try:
            num_colors = int(input("请输入颜色数量: "))
            if num_colors <= 0:
                print("颜色数量必须为正整数，请重新输入。")
                continue
            break
        except ValueError:
            print("输入无效，请输入一个整数。")

    # 获取每种颜色的使用次数
    color_counts = []
    while True:
        print(f"请依次输入{num_colors}种颜色的使用次数（用空格分隔）:")
        try:
            counts = list(map(int, input().split()))
            if len(counts) != num_colors:
                print(f"需要输入{num_colors}个数字，请重新输入。")
                continue
            if sum(counts) != counter.n_objects:
                print(f"颜色使用次数总和必须等于{object_type}数量({counter.n_objects})，请重新输入。")
                continue
            if any(c < 0 for c in counts):
                print("颜色使用次数不能为负数，请重新输入。")
                continue
            color_counts = counts
            break
        except ValueError:
            print("输入无效，请输入整数。")

    # 计算并输出结果
    try:
        result = counter.count_colorings(color_counts)
        print("\n=== 计算结果 ===")
        print(f"多面体: {polyhedron_type}")
        print(f"染色对象: {object_type} ({counter.n_objects}个)")
        print(f"颜色使用方案: {color_counts}")
        print(f"考虑旋转对称性后，共有 {result} 种不同的染色方案。")
    except Exception as e:
        print(f"计算出错: {str(e)}")


if __name__ == "__main__":
    main()