# INF-05010 Otimização Combinatória
# Trabalho: Meta-Heurísticas

# Bruno Grohs Vergara 00324256
# Erick Larratéa Knoblich 00324422

import random, math

# ----------------------------------------------------------------------------------------------------

class Professor:

  def __init__(self, x, y, s, i):

    self.x = x
    self.y = y
    self.s = s
    self.i = i

class Student:

  def __init__(self, x, y, h, j):

    self.x = x
    self.y = y
    self.h = h
    self.j = j

# ----------------------------------------------------------------------------------------------------

def ReadFile(FN):

  content = open("file{}.csv".format(FN), "r").readlines()
  PN, SN = content[0].split(",")
  PN, SN = int(PN), int(SN.strip())
  H, D = content[1].split(",")
  H, D = int(H), float(D.strip())
  P, S = [], []

  for i in range(2, 2 + PN):

    id, x, y, s = content[i].split(",")
    x, y, s = float(x), float(y), int(s.strip())
    P.append(Professor(x, y, s, 1))

  for j in range(2 + PN, 2 + PN + SN):
    
      id, x, y, h = content[j].split(",")
      x, y, h = float(x), float(y), int(h.strip())
      S.append(Student(x, y, h, 0))

  return P, PN, S, SN, D, H

def ValidateSolution(P, S, D, H):

  for p in P:

    if p.i == 0:

      continue

    for s in S:

      if math.sqrt((p.x - s.x)**2 + (p.y - s.y)**2) <= D:

        s.j = 1

  return True if sum(j.h * j.j for j in S) >= H else False

def SumSalaries(P):

  return sum(p.s * p.i for p in P)

def BetterSolution(P, S):

  objectiveA = SumSalaries(P)
  print("Iteration #0: {}".format(objectiveA))

  for k in range(100):

    for p in P:

      p.i = random.randint(0, 1)

    for s in S:

      s.j = 0
      
    if ValidateSolution(P, S, D, H):

      objectiveB = SumSalaries(P)

      if (objectiveB < objectiveA):

        objectiveA = objectiveB
        print("Iteration #{}: {} - SUCESS".format(k + 1, objectiveA))

      else:

        print("Iteration #{}: {} - FAILURE".format(k + 1, objectiveB))

  return objectiveA

# ----------------------------------------------------------------------------------------------------

P, PN, S, SN, D, H = ReadFile(1)
solution = BetterSolution(P, S)