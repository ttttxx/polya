# result/coloring.py
import time
import ast
import os
from math import factorial
from icosahedron.group_generation import SYMMETRY_CACHE
import math
from collections import defaultdict


def count_fixed_by_permutation(colors, color_counts, sizes):
    """
    计算在给定置换下保持不变的染色方案数。
    :param colors: 颜色列表
    :param color_counts: dict，颜色->该颜色应使用的次数
    :param sizes: 轮换大小列表
    :return: 整数，表示固定染色方案数
    """
    # 按 colors 顺序提取计数
    counts_list = [color_counts[c] for c in colors]
    sorted_sizes = sorted(sizes, reverse=True)
    memo = {}

    def dp(i, remaining):
        if i == len(sorted_sizes):
            return 1 if all(r == 0 for r in remaining) else 0

        key = (i, tuple(remaining))
        if key in memo:
            return memo[key]

        total = 0
        s = sorted_sizes[i]
        for c_idx in range(len(colors)):
            if remaining[c_idx] >= s:
                new_remaining = list(remaining)
                new_remaining[c_idx] -= s
                total += dp(i + 1, new_remaining)
        memo[key] = total
        return total

    return dp(0, counts_list)

def count_colorings(colors, perm_group, color_counts):
    """
    扩展支持正二十面体：
    :param poly_type: 'dodeca'（十二面体）或 'icosa'（二十面体）
    """
    total_vertices = 12   # 顶点总数切换
    group_size = len(perm_group)
    if group_size == 0:
        raise ValueError("对称群为空")

    total_fixed = 0
    for cycle_decomp in perm_group.values():
        covered = set()
        for cycle in cycle_decomp:
            covered |= set(cycle)
        uncovered = set(range(total_vertices)) - covered
        all_cycles = cycle_decomp + [(v,) for v in uncovered]
        sizes = [len(cycle) for cycle in all_cycles]
        fixed = count_fixed_by_permutation(colors, color_counts, sizes)
        total_fixed += fixed

    return total_fixed / group_size


def build_permutation(cycle_decomp, n=20):
    """
    从轮换分解构建置换函数及其逆函数。
    :param cycle_decomp: 轮换分解列表
    :param n: 顶点数
    :return: (置换函数p, 逆置换函数pinv)
    """
    p = list(range(n))
    for cycle in cycle_decomp:
        k = len(cycle)
        if k == 1:
            continue
        for idx in range(k):
            i = cycle[idx]
            j = cycle[(idx + 1) % k]
            p[i] = j
    pinv = [0] * n
    for i in range(n):
        pinv[p[i]] = i
    return p, pinv


def generate_all_valid_colorings(colors, color_counts, n=20):
    """
    生成所有满足颜色计数约束的染色方案。
    :param colors: 颜色列表
    :param color_counts: dict，颜色->该颜色应使用的次数
    :param n: 顶点数
    :return: 列表，每个元素是一个染色方案（元组）
    """
    colors_list = list(colors)
    counts_req = [color_counts[c] for c in colors_list]  # 改为按颜色名取值
    counts_curr = [0] * len(colors_list)
    results = []
    current_coloring = [None] * n

    def backtrack(i):
        if i == n:
            if all(c_curr == c_req for c_curr, c_req in zip(counts_curr, counts_req)):
                results.append(tuple(current_coloring))
            return

        for c_idx, c in enumerate(colors_list):
            if counts_curr[c_idx] < counts_req[c_idx]:
                current_coloring[i] = c
                counts_curr[c_idx] += 1
                backtrack(i + 1)
                counts_curr[c_idx] -= 1

    backtrack(0)
    return results


def is_representative(coloring, group_perms):
    """
    检查染色方案是否是其轨道的字典序最小代表。
    :param coloring: 染色方案（元组）
    :param group_perms: 列表，每个元素是(_, 逆置换函数)
    :return: 布尔值
    """
    return all(tuple(coloring[pinv[i]] for i in range(len(coloring))) >= coloring for _, pinv in group_perms)


def get_all_colorings(colors, perm_group, color_counts, max_results=5000):
    """
    枚举所有不等价的染色方案（每个轨道选一个代表）。
    如果不等价方案数大于 max_results，则只输出前 max_results 个。
    :param colors: 颜色列表
    :param perm_group: 字典，表示群
    :param color_counts: dict，颜色->该颜色应使用的次数
    :param max_results: 最大输出数量
    :return: 列表，每个元素是一个不等价染色方案（元组）
    """
    total_vertices = 12
    all_colorings = generate_all_valid_colorings(colors, color_counts, total_vertices)
    group_perms = []
    for cycle_decomp in perm_group.values():
        _, pinv = build_permutation(cycle_decomp, total_vertices)
        group_perms.append((None, pinv))  # 只需逆置换

    representatives = []
    for coloring in all_colorings:
        if is_representative(coloring, group_perms):
            representatives.append(coloring)
            # 新增：如果超过 max_results，就提前停止
            if len(representatives) >= max_results:
                print(f"超过 {max_results} 个方案，仅保留前 {max_results} 个。")
                break

    return representatives



def save_colorings_to_file(colorings, filename, element_type="vertex"):
    """
    将染色方案保存到文件。
    :param colorings: 染色方案列表
    :param filename: 文件名
    :param element_type: 元素类型（如'vertex'）
    """
    file_dir = "result"
    if not os.path.exists(file_dir):
        os.makedirs(file_dir, exist_ok=True)
    file_path = os.path.join(file_dir, filename)
    with open(file_path, 'w') as f:
        f.write(f"{element_type.capitalize()} colorings with {len(colorings)} classes\n")
        for idx, coloring in enumerate(colorings, 1):
            coloring_str = ' '.join(coloring)
            f.write(f"Class {idx}: {coloring_str}\n")
    print(f"Colorings saved to {file_path}")


# 使用示例
if __name__ == "__main__":
    colors = ['红', '蓝', '绿']
    color_counts = {'红': 2, '蓝': 6, '绿': 4}
    count = count_colorings(colors, SYMMETRY_CACHE, color_counts)
    print(f"Number of inequivalent colorings: {count}")
    all_colorings = get_all_colorings(colors, SYMMETRY_CACHE, color_counts)
