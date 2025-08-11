import os
import pickle
import sys
import time
from datetime import datetime

from dodecahedron.coloring import count_colorings, get_all_colorings, save_colorings_to_file
from dodecahedron.group_generation import generate_dodecahedron_rotations
from dodecahedron.utils import create_color_mapping, BASIC_COLORS
from dodecahedron.visualization import visualize_vertex_coloring


def main():
    # 用户选择染色模式
    print("顶点染色 (20个顶点)")

    n_elements = 20
    element_name = "顶点"
    visualize_func = visualize_vertex_coloring
    symmetry_mode = 'vertex'
    element_type = 'vertex'


    # # 尝试从本地文件加载对称群
    # cache_filename = f"{symmetry_mode}_symmetry_group.pkl"
    # if os.path.exists(cache_filename):
    #     with open(cache_filename, 'rb') as f:
    #         perm_group = pickle.load(f)
    #     print(f"已从本地文件加载对称群 ({len(perm_group)} 个对称操作)")
    # else:
        # 生成对称群
    start_time = time.time()
    print(f"正在生成对称群...")
    perm_group = generate_dodecahedron_rotations()
    print(f"已生成对称群 ({len(perm_group)} 个对称操作), 耗时: {time.time() - start_time:.2f}秒")

        # # 将对称群保存到本地文件
        # with open(cache_filename, 'wb') as f:
        #     pickle.dump(perm_group, f)
        # print(f"已将对称群保存到本地文件: {cache_filename}")

    # 用户输入颜色和数量
    color_names = []
    color_counts = {}
    total_count = 0
    try:
        n = int(input(f"\n输入颜色种类数 (用于{n_elements}个{element_name}): "))
    except ValueError:
        print("无效输入! 请输入整数")
        sys.exit(1)

    print("\n可用的基础颜色: " + ", ".join(BASIC_COLORS.keys()))
    print("或使用任何有效的颜色名称\n")


    for i in range(n):
        name = input(f"输入颜色#{i + 1}的名称 (如'红'或'blue'): ").strip()
        try:
            count = int(input(f"输入颜色#{i + 1}的数量: "))
        except ValueError:
            print("无效输入! 请输入整数")
            sys.exit(1)
        color_names.append(name)
        color_counts[name] = count
        total_count += count

    if total_count != n_elements:
        print(f"输入的颜色数量总和 ({total_count}) 不等于 {n_elements} 个{element_name}，请重新运行程序并输入正确的数量。")
        sys.exit(1)

    # 创建颜色映射
    color_mapping = create_color_mapping(color_names)
    for name, color_val in color_mapping.items():
        print(f"  {name} 映射到: {color_val}")

    # 计算并显示方案数
    total = count_colorings(color_names, perm_group, color_counts)
    print(f"\n所有不等价染色方案数: {total}")

    # 枚举所有具体方案
    print(f"\n开始枚举所有不等价方案...")
    start_time = time.time()
    all_reps = get_all_colorings(color_names, perm_group, color_counts)

    # 显示前5个方案
    if all_reps:
        print("\n前5个代表方案:")
        for i, coloring in enumerate(all_reps[:5]):
            print(f"方案{i + 1}: {'-'.join(coloring[:min(8, len(coloring))])}{'...' if len(coloring) > 8 else ''}")

        # 保存所有方案到文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{element_type}_colorings_{timestamp}.txt"
        save_colorings_to_file(all_reps, filename)

        # 询问用户是否可视化指定方案
        # print("\n是否可视化指定方案? (y/n)")
        # if input().strip().lower() == 'y':
        #     while True:
        #         try:
        #             scheme_num = input(f"请输入要可视化的方案编号 (1 - {len(all_reps)}, 输入 'q' 退出): ")
        #             if scheme_num.lower() == 'q':
        #                 break
        #             scheme_num = int(scheme_num)
        #             if 1 <= scheme_num <= len(all_reps):
        #                 coloring = all_reps[scheme_num - 1]
        #                 fig, ax = visualize_func(color_mapping, coloring)
        #
        #                 # 保存可视化结果为图片
        #                 img_filename = f"{element_type}_coloring_{timestamp}_scheme_{scheme_num}.png"
        #                 plt.savefig(img_filename, dpi=150, bbox_inches='tight')
        #                 print(f"已保存可视化结果为: {img_filename}")
        #
        #                 plt.show()
        #
        #                 # 询问用户是否展示旋转动画
        #                 print("\n是否展示该方案的旋转动画? (y/n)")
        #                 if input().strip().lower() == 'y':
        #                     visualize_dodecahedron_rotation(color_mapping, coloring, mode=element_type)
        #             else:
        #                 print("输入的方案编号超出范围，请输入有效编号。")
        #         except ValueError:
        #             print("输入无效，请输入一个整数或 'q' 退出。")
    else:
        print("\n未生成具体方案列表")


if __name__ == "__main__":
    if __name__ == "__main__":
        # 用户选择染色模式
        print("顶点染色 (20个顶点)")

        n_elements = 20
        element_name = "顶点"
        visualize_func = visualize_vertex_coloring
        symmetry_mode = 'vertex'
        element_type = 'vertex'


        start_time = time.time()
        print(f"正在生成对称群...")
        perm_group = generate_dodecahedron_rotations()
        print(f"已生成对称群 ({len(perm_group)} 个对称操作), 耗时: {time.time() - start_time:.2f}秒")


        # 直接设置颜色和数量（红色10个，蓝色10个）
        color_names = ['红', '蓝', '绿']
        color_counts = {'红': 9, '蓝': 6,'绿': 5}
        total_count = sum(color_counts.values())

        if total_count != n_elements:
            print(
                f"输入的颜色数量总和 ({total_count}) 不等于 {n_elements} 个{element_name}，请重新运行程序并输入正确的数量。")
            sys.exit(1)

        # 创建颜色映射
        color_mapping = create_color_mapping(color_names)
        for name, color_val in color_mapping.items():
            print(f"  {name} 映射到: {color_val}")

        # 计算并显示方案数
        total = count_colorings(color_names, perm_group, color_counts)
        print(f"\n所有不等价染色方案数: {total}")

        # 枚举所有具体方案
        print(f"\n开始枚举所有不等价方案...")
        start_time = time.time()
        all_reps = get_all_colorings(color_names, perm_group, color_counts)

        # 显示前5个方案
        if all_reps:
            print("\n前5个代表方案:")
            for i, coloring in enumerate(all_reps[:5]):
                print(f"方案{i + 1}: {'-'.join(coloring[:min(8, len(coloring))])}{'...' if len(coloring) > 8 else ''}")

            # 保存所有方案到文件
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{element_type}_colorings_{timestamp}.txt"
            save_colorings_to_file(all_reps, filename)

        else:
            print("\n未生成具体方案列表")
