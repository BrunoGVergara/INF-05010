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

  ns = 100
  H = 100

  for i in range(2, 2 + np):

    id, x, y, s = content[i].split(",")
    professors[k - 1].append(Professor(float(x), float(y), int(s.strip())))
    
  for j in range(2 + np, 2 + np + ns):
     
    id, x, y, h = content[j].split(",")
    students[k - 1].append(Student(float(x), float(y), int(h.strip())))

px = [p.x for p in professors[0]]
py = [p.y for p in professors[0]]
ps = [p.s for p in professors[0]]

sx = [s.x for s in students[0]]
sy = [s.y for s in students[0]]
sh = [s.h for s in students[0]]

m = GEKKO(remote = False)

xi = m.Array(m.Var, np, integer = True, lb = 0, ub = 1)
yj = m.Array(m.Var, ns, integer = True, lb = 0, ub = 1) 
sp = [[] for j in range(ns)]

m.Minimize(sum(ps[i] * xi[i] for i in range(np)))
m.Equation(sum(sh[j] * yj[j] for j in range(ns)) >= H)

for i in range(np):

  for j in range(ns):

    d = math.sqrt((px[i] - sx[j])**2 + (py[i] - sy[j])**2)

    if d <= D:

      sp[j].append(xi[i])

for j in range(np):

  m.Equation(yj[j] <= sum(sp[j]))

m.options.SOLVER = 1
m.solve()
print('Objective: ', m.options.OBJFCNVAL)