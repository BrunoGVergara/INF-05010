from gekko import GEKKO
import math

class Professor:
  def __init__(self, id, x, y, s, used):
    self.id = id
    self.x = x
    self.y = y
    self.s = s
    self.used = used

class Student:
  def __init__(self, id, x, y, h, used):
    self.id = id
    self.x = x
    self.y = y
    self.h = h
    self.used = used

professors, students = [[] for k in range(10)], [[] for k in range(10)]

for k in range(1, 2):

  content = open("file{}.csv".format(k), "r").readlines()
  np, ns = content[0].split(",")
  H, D = content[1].split(",")

  for i in range(2, 2 + int(np)):

    id, x, y, s = content[i].split(",")
    professors[k - 1].append(Professor(id, float(x), float(y), int(s.strip()), False))
    
  for j in range(2 + int(np), 2 + int(np) + int(ns)):
     
    id, x, y, h = content[j].split(",")
    students[k - 1].append(Student(id, float(x), float(h), int(h.strip()), False))

px = [p.x for p in professors[0]]
py = [p.y for p in professors[0]]
ps = [p.s for p in professors[0]]

sx = [s.x for s in students[0]]
sy = [s.y for s in students[0]]
sh = [s.h for s in students[0]]

print(sum(ps))

m = GEKKO()

x = m.Array(m.Var, 100, integer = True, lb = 0, ub = 1)
y = m.Array(m.Var, 100, integer = True, lb = 0, ub = 1)

m.qobj(ps, x = x, otype = 'min')
m.axb([sh[:100]], [2520320], x = y, etype = '>=')
m.axb([sh[:100]], [5.5], x = y, etype = '<=')
math.sqrt(())
m.options.SOLVER = 1
m.solve()
print('Objective: ', -m.options.OBJFCNVAL)