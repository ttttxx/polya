import ast

SYMMETRY_CACHE = {}

def generate_dodecahedron_rotations():
    file_path = '/Users/xushi/PycharmProjects/polya/dodecahedron/dodecahedron_group.txt'

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            # 解析每一行的对称群置换操作
            # 使用 ast.literal_eval 安全地将字符串转换为 Python 对象（列表）
            try:
                rotation = ast.literal_eval(line.strip())
                SYMMETRY_CACHE[i] = rotation
            except Exception as e:
                print(f"Error parsing line {i + 1}: {line}. Error: {e}")

    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"Error reading file: {e}")

    return SYMMETRY_CACHE

if __name__ == "__main__":
    generate_dodecahedron_rotations()
    # 查看缓存的对称群操作
    print(SYMMETRY_CACHE)
