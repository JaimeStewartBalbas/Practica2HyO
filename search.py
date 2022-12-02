
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
            self.condicion = "R"
        elif conflictivo:
            self.condicion = "C"
        else:
            self.condicion = "N"

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


def añadirNormal():
    pass

def añadirReducido():
    pass

def añadirConflictivo():
    pass


def bestChoice(alumnos):
    alumnos_restantes = alumnos #open list
    closed = []
    end = False
    while not end:
        node = alumnos_restantes.pop[0]
        closed.append(node)
        if  alumnos_restantes == []:
            end = True
