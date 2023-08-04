from gekko import GEKKO
import math

class Professor:

  def __init__(self, x, y, s):

    self.x = x
    self.y = y
    self.s = s

class Student:

  def __init__(self, x, y, h):

    self.x = x
    self.y = y
    self.h = h

professors, students = [[] for k in range(10)], [[] for k in range(10)]

for k in range(1, 2):

  content = open("file{}.csv".format(k), "r").readlines()
  np, ns = content[0].split(",")
  np, ns = int(np), int(ns.strip())
  H, D = content[1].split(",")
  H, D = int(H), float(D.strip())

  for i in range(2, 2 + np):

    id, x, y, s = content[i].split(",")
    professors[k - 1].append(Professor(float(x), float(y), int(s.strip())))
    
  for j in range(2 + np, 2 + np + ns):
     
    id, x, y, h = content[j].split(",")
    students[k - 1].append(Student(float(x), float(y), int(h.strip())))

px = [p.x for p in professors[k - 1]]
py = [p.y for p in professors[k - 1]]
ps = [p.s for p in professors[k - 1]]

sx = [s.x for s in students[k - 1]]
sy = [s.y for s in students[k - 1]]
sh = [s.h for s in students[k - 1]]

ns = 10000
sh = sh[:10000]
H = 200

m = GEKKO(remote = False)

c = [list(range(1, np + 1))] + [[s for s in ps]]
b = [[1, 2], [H, 0]]

Xi = m.Array(m.Var, np, integer = True, lb = 0, ub = 1)
Yi = m.Array(m.Var, ns, integer = True, lb = 0, ub = 1) 
sp = [[] for j in range(ns)]
A = [[1] * ns + [2] * ns, list(range(1, ns + 1)) + list(range(1, ns + 1)), sh + [0] * ns]

m.qobj(c, x = Xi, otype = 'min', sparse = True)
m.axb(A, b, x = Yi, etype = '>=', sparse = True)

for i in range(np):

  for j in range(ns):

    d = math.sqrt((px[i] - sx[j])**2 + (py[i] - sy[j])**2)

    if d <= D:

      sp[j].append(Xi[i])

for j in range(ns):

  m.Equation(Yi[j] <= sum(sp[j]))

m.solver_options = ['minlp_gap_tol 1.0e-4',\
                    'minlp_maximum_iterations 50000',\
                    'minlp_max_iter_with_int_sol 40000']

m.options.SOLVER = 1
m.solve(disp = False)
print('Objective: ', m.options.OBJFCNVAL)