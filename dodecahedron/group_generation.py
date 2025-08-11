import ast

SYMMETRY_CACHE = {}

def normalize_cycles(cycle_decomp, n=20):
    """补齐缺失的单点循环"""
    covered = set()
    for cycle in cycle_decomp:
        covered |= set(cycle)
    uncovered = set(range(n)) - covered
    return cycle_decomp + [(v,) for v in uncovered]

def generate_dodecahedron_rotations():
    file_path = '/Users/xushi/PycharmProjects/polya/dodecahedron/dodecahedron_group.txt'

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            try:
                rotation = ast.literal_eval(line.strip())
                rotation = normalize_cycles(rotation, 20)  # ✅ 补齐 20 个顶点
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
    print(SYMMETRY_CACHE)
    for idx, cycle_decomp in SYMMETRY_CACHE.items():
        covered = set()
        for cycle in cycle_decomp:
            covered |= set(cycle)
        if len(covered) != 20:
            print(f"❌ Element {idx} still only covers {len(covered)} vertices")
