from sage.all import *


def generate_cycle_index(polyhedron, element_type):
    """生成多面体指定元素类型的循环指标多项式"""
    # 获取多面体的对称群
    group = getattr(polyhedron, 'isometry_group', None)
    if group is None:
        raise ValueError("无法获取多面体的对称群")
    else:
        group = group()

    if element_type == 'vertex':
        elements = list(polyhedron.vertices())
        element_indices = list(range(1, len(elements) + 1))  # 索引从1开始
        permutations = []
        for g in group:
            perm = [0] * len(element_indices)
            for i, v in enumerate(elements):
                new_v = g(v)
                for j, w in enumerate(elements):
                    if w == new_v:
                        perm[i] = j + 1  # 转换为1-based索引
                        break
            permutations.append(Permutation(perm).to_cycles())
    elif element_type == 'edge':
        elements = list(polyhedron.edges())
        element_indices = list(range(1, len(elements) + 1))  # 索引从1开始
        permutations = []
        for g in group:
            perm = [0] * len(element_indices)
            for i, e in enumerate(elements):
                v1, v2 = e
                new_v1, new_v2 = g(v1), g(v2)
                for j, f in enumerate(elements):
                    f1, f2 = f
                    if (f1 == new_v1 and f2 == new_v2) or (f1 == new_v2 and f2 == new_v1):
                        perm[i] = j + 1  # 转换为1-based索引
                        break
            permutations.append(Permutation(perm).to_cycles())
    elif element_type == 'face':
        elements = list(polyhedron.faces())
        element_indices = list(range(1, len(elements) + 1))  # 索引从1开始
        permutations = []
        for g in group:
            perm = [0] * len(element_indices)
            for i, face in enumerate(elements):
                new_face = tuple(g(v) for v in face)
                for j, f in enumerate(elements):
                    if set(f) == set(new_face):
                        perm[i] = j + 1  # 转换为1-based索引
                        break
            permutations.append(Permutation(perm).to_cycles())
    else:
        raise ValueError("元素类型必须是 'vertex', 'edge' 或 'face'")

    n = len(elements)
    cycle_index = 0

    for cycles in permutations:
        cycle_lengths = [len(cycle) for cycle in cycles]
        term = 1
        for length in set(cycle_lengths):
            count = cycle_lengths.count(length)
            term *= var(f'x{length}') ** count
        cycle_index += term

    cycle_index = cycle_index / group.order()
    return cycle_index


def count_colorings(polyhedron, element_type, colors, color_counts=None):
    cycle_index = generate_cycle_index(polyhedron, element_type)

    if element_type == 'vertex':
        n = len(list(polyhedron.vertices()))
    elif element_type == 'edge':
        n = len(list(polyhedron.edges()))
    elif element_type == 'face':
        n = len(list(polyhedron.faces()))
    else:
        raise ValueError("元素类型必须是 'vertex', 'edge' 或 'face'")

    if color_counts is None:
        substituted = cycle_index.substitute({var(f'x{i}'): colors for i in range(1, n + 1)})
        return substituted
    else:
        if sum(color_counts) != n:
            raise ValueError(f"颜色计数总和必须等于{element_type}数 {n}")
        if len(color_counts) != colors:
            raise ValueError(f"颜色计数列表长度必须等于颜色数 {colors}")

        var_dict = {}
        for i in range(1, n + 1):
            var_dict[var(f'x{i}')] = sum(var(f'a{j}') ** i for j in range(colors))

        substituted = cycle_index.substitute(var_dict)

        from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
        R = PolynomialRing(QQ, [f'a{j}' for j in range(colors)])
        substituted = R(substituted)

        monomial = 1
        for j in range(colors):
            monomial *= R.gens()[j] ** color_counts[j]

        return substituted.monomial_coefficient(monomial)


def main():
    # 使用SageMath内置函数创建多面体
    polyhedrons = {
        "正四面体": tetrahedron(),
        "立方体": cube(),
        "正八面体": octahedron(),
        "正十二面体": dodecahedron(),
        "正二十面体": icosahedron()
    }

    print("可用的多面体:")
    for i, name in enumerate(polyhedrons.keys(), 1):
        print(f"{i}. {name}")

    poly_choice = int(input("选择多面体 (1-5): "))
    poly_name = list(polyhedrons.keys())[poly_choice - 1]
    polyhedron = polyhedrons[poly_name]

    print("\n可用的染色元素类型:")
    print("1. 顶点")
    print("2. 边")
    print("3. 面")
    element_choice = int(input("选择染色元素类型 (1-3): "))
    element_types = ['vertex', 'edge', 'face']
    element_type = element_types[element_choice - 1]
    element_names = ["顶点", "边", "面"]
    element_name = element_names[element_choice - 1]

    colors = int(input("\n输入颜色数量: "))

    print("\n是否要指定每种颜色的使用次数?")
    print("1. 是")
    print("2. 否")
    count_choice = int(input("选择 (1-2): "))

    if count_choice == 1:
        if element_type == 'vertex':
            total_elements = len(list(polyhedron.vertices()))
        elif element_type == 'edge':
            total_elements = len(list(polyhedron.edges()))
        else:
            total_elements = len(list(polyhedron.faces()))

        print(f"\n请输入每种颜色的使用次数 (总和必须等于{total_elements})")
        color_counts = []
        for i in range(colors):
            count = int(input(f"颜色 {i + 1} 的使用次数: "))
            color_counts.append(count)

        if sum(color_counts) != total_elements:
            raise ValueError(f"颜色计数总和必须等于{total_elements}")

        result = count_colorings(polyhedron, element_type, colors, color_counts)
    else:
        result = count_colorings(polyhedron, element_type, colors)

    print(f"\n{poly_name}的{element_name}用{colors}种颜色染色的方案数为: {result}")


if __name__ == "__main__":
    main()