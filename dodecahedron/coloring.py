import time


def get_cycle_structure(perm):
    """计算置换的循环结构"""
    n = len(perm)
    visited = [False] * n
    cycles = []

    for i in range(n):
        if not visited[i]:
            cycle = []
            j = i
            while not visited[j]:
                visited[j] = True
                cycle.append(j)
                j = perm[j]
            cycles.append(cycle)

    return cycles


from math import factorial

def count_colorings(colors, perm_group, color_counts):
    n_colors = len(colors)
    n_elements = sum(color_counts)
    total_fixed = 0

    for perm in perm_group:
        cycles = get_cycle_structure(perm)
        cycle_lengths = [len(cycle) for cycle in cycles]
        # 检查是否可以为每个循环分配相同颜色
        possible = True
        for cycle_length in cycle_lengths:
            if any(count % cycle_length != 0 for count in color_counts):
                possible = False
                break
        if not possible:
            continue
        # 计算固定点数量
        fixed = 1
        for cycle_length in cycle_lengths:
            choices = 0
            for count in color_counts:
                if count % cycle_length == 0:
                    choices += 1
            fixed *= choices
        total_fixed += fixed

    return total_fixed // len(perm_group)

def get_cycle_structure(perm):
    n = len(perm)
    visited = [False] * n
    cycles = []
    for i in range(n):
        if not visited[i]:
            cycle = []
            j = i
            while not visited[j]:
                visited[j] = True
                cycle.append(j)
                j = perm[j]
            cycles.append(cycle)
            cycles.append(cycle)
    return cycles


def build_stabilizer_chain(perm_group):
    """
    构建稳定子群链
    返回一个列表，其中每个元素是 (点, 轨道, 稳定子群) 的元组
    """
    n = len(perm_group[0])
    chain = []
    current_group = perm_group
    points = list(range(n))

    for i in range(n):
        # 选择当前最小点（按顺序）
        point = i

        # 计算当前点的轨道
        orbit = set()
        stabilizer = []

        for perm in current_group:
            image = perm[point]
            orbit.add(image)

        # 计算稳定当前点的子群
        for perm in current_group:
            if perm[point] == point:
                stabilizer.append(perm)

        chain.append((point, orbit, stabilizer))
        current_group = stabilizer

    return chain


def get_orbit_and_stabilizer(chain, depth):
    """
    从稳定子群链中获取指定深度的轨道和稳定子群
    """
    if depth < len(chain):
        return chain[depth][1], chain[depth][2]
    return set(), []  # 超出深度返回空


def get_all_colorings(colors, perm_group, color_counts):
    """
    获取所有不等价染色方案（考虑对称性）
    使用基于子群链的陪集分解方法高效枚举代表元

    :param colors: 颜色列表
    :param perm_group: 对称群（置换列表）
    :param color_counts: 每种颜色的数量
    :return: 不等价方案列表
    """
    n_colors = len(colors)
    n_elements = len(perm_group[0])
    total_colorings = n_colors ** n_elements

    # 检查是否为大尺寸问题
    if total_colorings > 1000000:
        print(f"警告: 染色方案总数 ({total_colorings}) 过大，可能需要很长时间")
        print("是否继续? (y/n)")
        choice = input().strip().lower()
        if choice != 'y':
            print("已跳过具体方案枚举")
            return []

    print(f"正在使用子群链方法枚举不等价染色方案...")
    start_time = time.time()

    # 步骤1: 构建稳定子群链
    stabilizer_chain = build_stabilizer_chain(perm_group)

    # 步骤2: 使用陪集分解枚举代表元
    representatives = []
    coloring = [-1] * n_elements  # 当前部分染色方案
    depth = 0  # 当前处理的位置

    # 使用DFS递归枚举
    def dfs(depth):
        if depth == n_elements:
            # 检查颜色数量是否符合要求
            counts = [0] * n_colors
            for c in coloring:
                counts[c] += 1
            if counts == color_counts:
                # 找到一个完整染色方案
                representatives.append(tuple(coloring))
            return

        # 获取当前位置的轨道
        orbit, stabilizer = get_orbit_and_stabilizer(stabilizer_chain, depth)

        # 尝试当前轨道上的所有可能值
        used_colors = set()
        for point in orbit:
            # 尝试所有可能的颜色
            for color_idx in range(n_colors):
                # 如果这个颜色已经在这个等价类中尝试过，跳过
                if color_idx in used_colors:
                    continue

                coloring[point] = color_idx
                valid = True

                # 检查对称性约束
                for perm in stabilizer:
                    # 如果存在对称操作使当前点映射到更小的点且颜色不同，则无效
                    if perm[point] < point and coloring[perm[point]] != color_idx:
                        valid = False
                        break

                if valid:
                    used_colors.add(color_idx)
                    # 递归处理下一个位置
                    dfs(depth + 1)

    # 启动DFS
    dfs(0)

    # 转换为颜色名称
    result = []
    for rep in representatives:
        named_rep = [colors[i] for i in rep]
        result.append(named_rep)

    print(f"成功枚举出 {len(result)} 个不等价方案, 耗时: {time.time() - start_time:.2f}秒")

    return result


def save_colorings_to_file(colorings, filename, element_type):
    """
    将染色方案保存到文本文件

    :param colorings: 染色方案列表
    :param filename: 输出文件名
    :param element_type: 元素类型 ('vertex' 或 'face')
    """
    with open(filename, 'w', encoding='utf-8') as f:
        if element_type == 'vertex':
            f.write("正十二面体顶点染色方案 (20个顶点)\n")
            f.write("=" * 50 + "\n")
            for i, coloring in enumerate(colorings):
                f.write(f"方案 {i + 1}: {'-'.join(map(str, coloring))}\n")
        else:
            f.write("正十二面体面染色方案 (12个面)\n")
            f.write("=" * 50 + "\n")
            for i, coloring in enumerate(colorings):
                f.write(f"方案 {i + 1}: {'-'.join(map(str, coloring))}\n")

    print(f"已保存 {len(colorings)} 个染色方案到文件: {filename}")