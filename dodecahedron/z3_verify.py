from z3 import *
import pickle
from pathlib import Path

# === 用户输入部分 ===
def get_user_input():
    try:
        num_colors = int(input("请输入颜色种类数（例如3）: "))
        color_counts = []
        print(f"请输入每种颜色的数量，总和必须为20（正十二面体顶点数）:")
        for i in range(num_colors):
            count = int(input(f"颜色{i} 的数量: "))
            color_counts.append(count)

        if sum(color_counts) != 20:
            print(f"颜色总数为 {sum(color_counts)}，必须为20，请重新运行程序。")
            exit(1)

        return num_colors, color_counts
    except Exception as e:
        print(f"输入有误: {e}")
        exit(1)

# 正十二面体参数
num_vertices = 20  # 顶点数固定

# 加载对称群函数
def load_symmetry_group():
    file_path = Path(r'/Users/xushi/PycharmProjects/polya/dodecahedron/vertex_symmetry_group.pkl')
    try:
        with open(file_path, 'rb') as f:
            symmetry_group = pickle.load(f)
            print("群元素类型:", type(symmetry_group))
            if isinstance(symmetry_group, dict):
                print("群元素示例:", list(symmetry_group.items())[:5])
            return symmetry_group
    except Exception as e:
        print(f"加载群文件错误: {e}")
        return {}

# 使用动态规划计算群元素的不变染色数
def burnside(group_elements, color_counts):
    num_colors = len(color_counts)
    invariant_count = 0

    for g in group_elements:
        if not isinstance(g, list):
            print(f"跳过非列表群元素: {g}")
            continue

        # 构造完整轮换（包括1-轮换）
        covered = set()
        for cycle in g:
            if not isinstance(cycle, tuple):
                print(f"跳过非元组轮换: {cycle}")
                continue
            covered.update(cycle)
        uncovered = set(range(num_vertices)) - covered
        full_g = list(g)
        for v in uncovered:
            full_g.append((v,))

        # 统计轮换长度
        cycle_lengths = []
        for cycle in full_g:
            if not isinstance(cycle, tuple):
                print(f"跳过无效轮换: {cycle}")
                continue
            cycle_lengths.append(len(cycle))

        if sum(cycle_lengths) != num_vertices:
            print(f"轮换长度错误，跳过: {sum(cycle_lengths)} != {num_vertices}")
            continue

        # 多维动态规划
        from collections import defaultdict

        dp = defaultdict(int)
        dp[(0,) * num_colors] = 1
        current_total = 0

        for L in cycle_lengths:
            new_dp = defaultdict(int)
            current_total += L

            for state, count in dp.items():
                for color in range(num_colors):
                    # 尝试将L长度轮换染为某个颜色
                    new_state = list(state)
                    new_state[color] += L

                    if new_state[color] > color_counts[color]:
                        continue

                    if sum(new_state) <= current_total and all(new_state[i] <= color_counts[i] for i in range(num_colors)):
                        new_dp[tuple(new_state)] += count

            dp = new_dp

        # 最终目标状态
        target_state = tuple(color_counts)
        count_this_g = dp[target_state]
        invariant_count += count_this_g
        print(f"群元素贡献: {count_this_g}")

    return invariant_count


# 主程序入口
if __name__ == "__main__":
    num_colors, color_counts = get_user_input()

    group_dict = load_symmetry_group()
    if not group_dict:
        print("无法加载对称群，退出")
        exit()

    group_elements = list(group_dict.values())
    print(f"加载群元素数量: {len(group_elements)}")

    total_fixed = burnside(group_elements, color_counts)
    group_order = len(group_elements)
    num_equivalence = total_fixed / group_order

    print(f"\n=== 结果 ===")
    print(f"总不变染色数: {total_fixed}")
    print(f"对称群阶数: {group_order}")
    print(f"不等价染色方案数: {num_equivalence}")
