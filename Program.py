# INF-05010 Otimização Combinatória
# Trabalho: Meta-Heurísticas

# Bruno Grohs Vergara 00324256
# Erick Larratéa Knoblich 00324422

from gekko import GEKKO
import math, time, os

# ----------------------------------------------------------------------------------------------------

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
solutions, X, Y = [], [], []

# ----------------------------------------------------------------------------------------------------

for k in range(1, 10 + 1):

  content = open("file{}.csv".format(k), "r").readlines()
  P, S = content[0].split(",")
  P, S = int(P), int(S.strip())
  H, D = content[1].split(",")
  H, D = int(H), float(D.strip())

  for i in range(2, 2 + P):

    id, x, y, s = content[i].split(",")
    x, y, s = float(x), float(y), int(s.strip())
    professors[k - 1].append(Professor(x, y, s))
    
  for j in range(2 + P, 2 + P + S):
     
    id, x, y, h = content[j].split(",")
    x, y, h = float(x), float(y), int(h.strip())
    students[k - 1].append(Student(x, y, h))

  px = [p.x for p in professors[k - 1]]
  py = [p.y for p in professors[k - 1]]
  ps = [p.s for p in professors[k - 1]]

  sx = [s.x for s in students[k - 1]]
  sy = [s.y for s in students[k - 1]]
  sh = [s.h for s in students[k - 1]]

  m = GEKKO(remote = False)
  Xi = m.Array(m.Var, P, integer = True, lb = 0, ub = 1)
  Yj = m.Array(m.Var, S, integer = True, lb = 0, ub = 1) 
  Pj = [[] for j in range(S)]
  m.qobj(ps, x = Xi, otype = 'min')
  m.axb([sh], [H], x = Yj, etype = '>=')

  for i in range(P):

    for j in range(S):

      if math.sqrt((px[i] - sx[j])**2 + (py[i] - sy[j])**2) <= D:

        Pj[j].append(Xi[i])

  for j in range(S):

    m.Equation(Yj[j] <= sum(Pj[j]))

  m.options.SOLVER = 1
  m.solver_options = ['minlp_gap_tol 1.0e-4',\
                    'minlp_maximum_iterations 50000',\
                    'minlp_max_iter_with_int_sol 40000']
  start = time.time()
  m.solve(disp = False)
  end = time.time()
  t = end - start
  solutions.append(("Objective: {}".format(m.options.OBJFCNVAL), "Time: {}".format((t))))
  X.append([i.value[0] for i in Xi])
  Y.append([j.value[0] for j in Yj])

os.system('cls||clear')
i = 1

for s in solutions:

  print("Instance #{}:\n\n{}\n{}\n".format(i, s[0], s[1]))
  i += 1

# ----------------------------------------------------------------------------------------------------