from z3 import Solver, Int, sat
x = Int('x')
s = Solver()
s.add(x > 5)
print(s.check())  # 应输出 "sat"