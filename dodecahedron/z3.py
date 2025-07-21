def dodecahedron_coloring(c):
    """
    计算使用c种颜色对十二面体面染色的不同方案数（考虑旋转对称性）

    参数:
        c (int): 颜色数量

    返回:
        int: 在旋转对称下的不同染色方案数
    """
    # 根据Polya计数定理公式计算：
    # (1/60) * [c^12 + 15*c^6 + 20*c^4 + 24*c^4]
    # 简化后： (c^12 + 15*c^6 + 44*c^4) // 60
    return (c ** 12 + 15 * c ** 6 + 44 * c ** 4) // 60


# 测试不同颜色数量下的染色方案
if __name__ == "__main__":
    colors = [1, 2, 3, 4, 5]  # 测试1-5种颜色的情况

    print("十二面体染色方案数（考虑旋转对称）：")
    for c in colors:
        result = dodecahedron_coloring(c)
        print(f"使用 {c} 种颜色: {result} 种方案")