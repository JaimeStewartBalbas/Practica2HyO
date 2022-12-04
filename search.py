
alumnos = []

""""
Conjunto de estados   --> Todas las posibilidades de combiniaciones de alumnos en el bus, junto con los 
estados en los que se va llenado el bus
Conjunto de operadores   --> Diferente alumno que puedes meter en el bus
Estado(s) inicial(es)   --> Bus vacío
Meta(s) o estado(s) final(es)  --->
"""


class Alumno:
    def __init__(self, asiento, reducido, conflictivo):
        self.asiento = asiento
        if reducido:
            self.movilidad= "R"
        else:
            self.movilidad = "X"
        if conflictivo:
            self.condicion = "C"
        else:
            self.conflictivo = "X"

class Node:
    def __init__(self, father, info):
        self.father = father
        self.info = info

    def depth(self):
        if not self.father:
            return 0
        curr_node = self.father
        counter = 1
        while not curr_node.father:
            curr_node = curr_node.father
            counter += 1
        return counter

    def costeReducido(self):
        if self.father.info.movilidad == "R":
            return int('inf')
        elif self.father.info.condicion == "C":
            return 6
        else:
            return 3

    def costeNormal(self):
        if self.father.info.movilidad == "R":
            return 0
        elif self.father.info.condicion == "C":
            return 2
        else:
            return 1

    def añadirConflictivo(self):
        if self.father.info.movilidad == "R":
            return 3
        elif self.father.info.condicion == "C":
            return 3
        else:
            return 1


class State:
    def __init__(self, normales, reducidos, conflictivos):
        self.normales = normales
        self.reducidos = reducidos
        self.conflictivos = conflictivos

    def removeRed(self):
        if len(self.reducidos) > 0:
            return 3
        else:
            return int('inf')



def f(alumnos_restantes):
    coste = 0
    if alumnos_restantes[len(alumnos_restantes)].movilidad == "R":
        return 6*len(alumnos_restantes)
    for i in range(len(alumnos_restantes)):
        if (alumnos_restantes[i].movilidad == "R" and alumnos_restantes[i + 1].movilidad == "R"):
            return 6*len(alumnos_restantes)
        if alumnos_restantes[i].movilidad == "R":
            coste_alumno = 3
        else:
            coste_alumno = 1
        if i != 0:
            if alumnos_restantes[i - 1].movilidad == "R":
                coste_alumno = 3
            if alumnos_restantes[i - 1].condicion == "C":
                coste_alumno *= 2
            elif i != len(alumnos_restantes) and alumnos_restantes[i + 1].condicion == "C":
                coste_alumno += 2

        coste += coste_alumno
    return coste


def preconditions(alumnos_restantes):
    normal, reducido, conflictivo = False, False, False
    for i in alumnos_restantes:
        if i.movilidad == "R":
            reducido = True
        if i.condicion == "C":
            conflictivo = True
        else:
            normal = True
        if normal and reducido and conflictivo:
            return True, True, True
    return normal, reducido, conflictivo

def bestChoice(alumnos):
    alumnos_restantes = alumnos #open list
    closed = []
    end = False
    while not end:
        node = alumnos_restantes.pop[0]
        closed.append(node)
        if  alumnos_restantes == []:
            end = True
