# dodecahedron/utils.py

# 扩展基础颜色映射
BASIC_COLORS = {
    'r': 'red', '红': 'red', 'red': 'red',
    'b': 'blue', '蓝': 'blue', 'blue': 'blue',
    'g': 'green', '绿': 'green', 'green': 'green',
    'y': 'yellow', '黄': 'yellow', 'yellow': 'yellow',
    'k': 'black', '黑': 'black', 'black': 'black',
    'w': 'white', '白': 'white', 'white': 'white',
    'v': 'violet', '紫': 'purple', 'purple': 'purple',
    'o': 'orange', '橙': 'orange', 'orange': 'orange',
    'p': 'pink', '粉': 'pink', 'pink': 'pink',
    'c': 'cyan', '青': 'cyan', 'cyan': 'cyan',
    'm': 'magenta', '品红': 'magenta', 'magenta': 'magenta',
    'br': 'brown', '棕': 'brown', 'brown': 'brown',
    'gr': 'gray', '灰': 'gray', 'gray': 'gray'
}


def create_color_mapping(color_names):
    """创建颜色名称到实际颜色的映射"""
    # 预定义颜色列表
    predefined_colors = ['red', 'blue', 'green', 'cyan', 'magenta', 'yellow',
                         'black', 'orange', 'purple', 'pink', 'brown', 'gray',
                         'lime', 'teal', 'lavender', 'maroon', 'navy', 'olive']

    color_mapping = {}
    for i, name in enumerate(color_names):
        name_lower = name.lower()
        if name_lower in BASIC_COLORS:
            color_mapping[name] = BASIC_COLORS[name_lower]
        else:
            # 如果不在基础颜色中，使用预定义颜色列表
            color_mapping[name] = predefined_colors[i % len(predefined_colors)]
    return color_mapping