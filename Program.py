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
        print("Iteration #{}: {} - SUCCESS".format(k + 1, objectiveA))

      else:

        print("Iteration #{}: {} - FAILURE".format(k + 1, objectiveB))

  return objectiveA

def CalculaObjetivo(Xi, professores):

  objt = 0
  for i in range(len(Xi)):
    objt+= professores.s * Xi[i]

  return objt


def VerificarSolucao(professores, alunos, distancia, horas, Xi):
  #Verifica se um cromossomo Xi é uma solução válida
  i = 0
  for x in Xi:
    if x == 0:  #Se um professor não for usado na solução, não existe necessidade de verificar os alunos que ele atende
      continue

    for a in alunos:
      if math.sqrt((professores[i].x - a.x)**2 + (professores[i].y - a.y)**2) <= distancia:
        #Descobre todos os alunos que o professor atende baseado na distância e no limite preestabelecido
        a.j = 1
    i += 1
  
  return True if sum(j.h * j.j for j in alunos) >= horas else False


def gerarPopulacaoInicial(professores, alunos, distancia, horas, n, numProf):  
#Gera uma populacao inicial randomica de tamanho n somente com solucoes viaveis

  populacao = []
  cromossomo = []

  for i in range(n):  #loop que gera os n cromossomos

    for j in range(numProf):  #loop que gera os genes do cromossomo
      cromossomo.append(random.randint(0,1))
    
    if VerificarSolucao(professores,alunos,distancia,horas,cromossomo): #Testa se a solucao gerada eh valida
      populacao.append(cromossomo)

    cromossomo = []
  
  return populacao


def SelecaoPorTorneio(professores, populacao):
#Realiza a selecao de dois individuos atraves de um torneio de tamanho k

  k = random.randint(2,round(0.25*len(populacao))) #Gera um numero aleatorio para o tamanho do torneio
  torneio = []
  cromossomo1 = []
  cromossomo2 = []

  for i in range(k):  #Seleciona k cromossomos da populacao aleatoriamente
    torneio.append(populacao[random.randint(0,len(populacao))])

  cromossomo1 = torneio[0]  #Pega os dois primeiros cromossomos
  cromossomo2 = torneio[1]

  if CalculaObjetivo(cromossomo2, professores) < CalculaObjetivo(cromossomo1,professores):
    #Caso o segundo cromossomo tenha valor menor que o primeiro
    aux = cromossomo1
    cromossomo1 = cromossomo2
    cromossomo2 = aux

  for i in range(2,len(torneio)): #Seleciona os dois cromossomos com menos valor da funcao objetivo
    if CalculaObjetivo(torneio[i],professores) < CalculaObjetivo(cromossomo1,professores):
      cromossomo1 = torneio[i]
    elif CalculaObjetivo(torneio[i],professores) < CalculaObjetivo(cromossomo2,professores):
      cromossomo2 = torneio[i]
  
  return cromossomo1,cromossomo2


# ----------------------------------------------------------------------------------------------------

P, PN, S, SN, D, H = ReadFile(1)

#populacaoInic = gerarPopulacaoInicial(P,S,D,H,30,PN)
#SelecaoPorTorneio(P,populacaoInic)