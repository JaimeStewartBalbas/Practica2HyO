
"""
Los alumnos con movilidad reducida tardan tres veces mas en montar en el autob ´ us que el resto de ´
alumnos.

El alumno que se encuentre en la cola justo detras de un alumno con ´ movilidad reducida debera ayudarle ´
a subir al autobus, por lo que no puede haber dos alumnos con ´ movilidad reducida uno a continuacion´
del otro ni ocupando la ultima posici ´ on en la cola. ´

Cuando un alumno ayuda a subir a otro con movilidad reducida el tiempo que tardan los dos es el tiempo
que tarda el alumno con movilidad reducida puesto que suben a la vez.

Un alumno conflictivo duplicara el tiempo necesario para subir al autob ´ us tanto del compa ´ nero que se ˜
encuentre justo delante de el como del compa ´ nero que se encuentre justo detr ˜ as, de este modo, si un ´
alumno conflictivo ayuda a un alumno con movilidad reducida a subir al autobus, el tiempo empleado por ´
los dos se duplicara respecto al tiempo que se invertir ´ ´ıa si quien ayudase fuese un alumno no conflictivo.


"""

class State:
    #Estado que representa
    def __init__(self,alumnosXX,alumnosXR,alumnosCX,alumnosCR,prev_confl=[]):
        self.alumnosXX = alumnosXX
        self.alumnosXR = alumnosXR
        self.alumnosCX = alumnosCX
        self.alumnosCR = alumnosCR
        self.prev_confl = prev_confl



class Node:
    def __init__(self,coste:int,state:State,prevAl=None):
        self.father = None
        self.state = state
        self.coste = coste
        self.prevAl = prevAl


class ASTAR:

    def heuristica1(self,estado:State)->int:
        reducidos = len(estado.alumnosXR) + len(estado.alumnosCR)
        normales = len(estado.alumnosXX) + len(estado.alumnosCX)
        if normales >= reducidos:
            return 3*reducidos + 1*(normales-reducidos)
        return float('inf')

    def heuristica2(self, estado):
        reducidos = len(estado.alumnosXR) + len(estado.alumnosCR)
        normales = len(estado.alumnosXX)
        conflictivos = len(estado.alumnosCX)
        if normales + conflictivos >= reducidos:
            if reducidos < normales:
                return 3*reducidos + 1*(normales-reducidos) + 2*(conflictivos-2)+ 2
            else:
                return 3*reducidos + (reducidos - normales)*3 + 2*(normales+conflictivos-reducidos - 2) + 2
        return float('inf')

    def isFinal(self,N:State):
        if not len(N.alumnosCR) and not len(N.alumnosXX) and not len(N.alumnosXR) and not len(N.alumnosCX):
            return True
        return False

    def addXX(self,state:State,prevAl):
        if len(state.alumnosXX) > 0:
            if prevAl == None:
                newstate = State(state.alumnosXX[1:],state.alumnosXR,state.alumnosCX,state.alumnosCR)
                return [newstate,1,"XX"]
            elif prevAl == "XX":
                newstate = State(state.alumnosXX[1:],state.alumnosXR,state.alumnosCX,state.alumnosCR)
                return [newstate,1,"XX"]
            elif prevAl == "XR":
                newstate = State(state.alumnosXX[1:],state.alumnosXR,state.alumnosCX,state.alumnosCR)
                return [newstate,0,"XX"]
            elif prevAl == "CX":
                newstate = State(state.alumnosXX[1:],state.alumnosXR,state.alumnosCX,state.alumnosCR)
                return [newstate,2,"XX"]
            elif prevAl == "CR":
                newstate = State(state.alumnosXX[1:],state.alumnosXR,state.alumnosCX,state.alumnosCR)
                return [newstate,0,"XX"]
        return float('inf')


    def addXR(self,state:State,prevAl):
        if len(state.alumnosXR) > 0 and (len(state.alumnosXX) + len(state.alumnosCX)) > 0:
            if prevAl == None:
                newstate = State(state.alumnosXX, state.alumnosXR[1:], state.alumnosCX, state.alumnosCR)
                return [newstate, 3, "XR"]
            elif prevAl == "XX":
                newstate = State(state.alumnosXX, state.alumnosXR[1:], state.alumnosCX, state.alumnosCR)
                return [newstate, 3, "XR"]
            elif prevAl == "XR":
                return float('inf')
            elif prevAl == "CX":
                newstate = State(state.alumnosXX, state.alumnosXR[1:], state.alumnosCX, state.alumnosCR)
                return [newstate, 6, "XR"]
            elif prevAl == "CR":
                return float('inf')

        return float('inf')

    def addCX(self,state:State,prevAl, grandpa,index):
        extra = 0
        if len(state.alumnosCX) > 0:
            if prevAl == None:
                lista = state.alumnosCX.copy()
                del lista[index]
                newstate = State(state.alumnosXX, state.alumnosXR, lista, state.alumnosCR,state.prev_confl)
                newstate.prev_confl.append(state.alumnosCX[index])
                return [newstate, 1, "CX"]
            elif prevAl == "XX":
                if grandpa != "XR":
                    asiento = state.alumnosCX[index]
                    for i in state.prev_confl:
                        if asiento > i:
                            extra += 1

                    lista = state.alumnosCX.copy()
                    del lista[index]
                    newstate = State(state.alumnosXX, state.alumnosXR, lista, state.alumnosCR,
                                     state.prev_confl)
                    newstate.prev_confl.append(state.alumnosCX[index])
                    return [newstate, 2, "CX"]
                else:
                    lista = state.alumnosCX.copy()
                    del lista[index]
                    newstate = State(state.alumnosXX, state.alumnosXR, lista, state.alumnosCR,
                                     state.prev_confl)
                    newstate.prev_confl.append(state.alumnosCX[index])
                    return [newstate, 1, "CX"]
            elif prevAl == "XR":
                lista = state.alumnosCX.copy()
                del lista[index]
                newstate = State(state.alumnosXX, state.alumnosXR, lista, state.alumnosCR, state.prev_confl)
                newstate.prev_confl.append(state.alumnosCX[index])
                return [newstate, 3, "CX"]
            elif prevAl == "CX":
                if grandpa != "XR" and grandpa != "CR":
                    lista = state.alumnosCX.copy()
                    del lista[index]
                    newstate = State(state.alumnosXX, state.alumnosXR, lista, state.alumnosCR,
                                     state.prev_confl)
                    newstate.prev_confl.append(state.alumnosCX[index])
                    return [newstate, 3, "CX"]
                else:
                    lista = state.alumnosCX.copy()
                    del lista[index]
                    newstate = State(state.alumnosXX, state.alumnosXR, lista, state.alumnosCR,
                                     state.prev_confl)
                    newstate.prev_confl.append(state.alumnosCX[index])
                    return [newstate, 2, "CX"]
            elif prevAl == "CR":
                lista = state.alumnosCX.copy()
                del lista[index]
                newstate = State(state.alumnosXX, state.alumnosXR, lista, state.alumnosCR, state.prev_confl)
                newstate.prev_confl.append(state.alumnosCX[index])
                return [newstate, 3, "CX"]
        return float('inf')

    def addCR(self,state:State,prevAl, grandpa):
        if len(state.alumnosCR) > 0 and (len(state.alumnosXX) + len(state.alumnosCX)) > 0:
            if prevAl == None:
                newstate = State(state.alumnosXX, state.alumnosXR, state.alumnosCX, state.alumnosCR[1:])
                return [newstate, 3, "CR"]
            elif prevAl == "XX":
                if grandpa != "XR" and grandpa != "CR":
                    newstate = State(state.alumnosXX, state.alumnosXR, state.alumnosCX, state.alumnosCR[1:])
                    return [newstate, 4, "CR"]
                else:
                    newstate = State(state.alumnosXX, state.alumnosXR, state.alumnosCX, state.alumnosCR[1:])
                    return [newstate, 3, "CR"]
            elif prevAl == "XR":
                return float('inf')
            elif prevAl == "CX":
                if grandpa != "XR" and grandpa != "CR":
                    newstate = State(state.alumnosXX, state.alumnosXR, state.alumnosCX, state.alumnosCR[1:])
                    return [newstate, 7, "CR"]
                else:
                    newstate = State(state.alumnosXX, state.alumnosXR, state.alumnosCX, state.alumnosCR[1:])
                    return [newstate, 6, "CR"]
            elif prevAl == "CR":
                return float('inf')
        return float('inf')



    def expand(self,node:Node):
        succesors = []
        x = self.addXX(node.state,node.prevAl)
        y = self.addXR(node.state,node.prevAl)
        if node.father is None:
            z = self.addCX(node.state, node.prevAl, None)
            w = self.addCR(node.state, node.prevAl, None)
        else:
            z = self.addCX(node.state,node.prevAl, node.father.prevAl)
            w = self.addCR(node.state,node.prevAl, node.father.prevAl)
        if  type(x) != float:
            newnode = Node(node.coste + x[1],x[0],x[2])
            newnode.father = node
            succesors.append(newnode)

        if type(y) != float:
            newnode = Node(node.coste + y[1],y[0], y[2])
            newnode.father = node
            succesors.append(newnode)

        if  type(z) != float:
            newnode = Node(node.coste + z[1],z[0], z[2])
            newnode.father = node
            succesors.append(newnode)

        if  type(w) != float:
            newnode = Node( node.coste + w[1],w[0], w[2])
            newnode.father = node
            succesors.append(newnode)

        result = self.mergesortNodes(succesors)
        return result
    def mergeNodes(self,list_left,list_right):
        left, right = 0,0
        resultado =  []
        while right < len(list_right) and left < len(list_left):
            if (list_left[left].coste+self.heuristica2(list_left[left].state)) < (list_right[right].coste+self.heuristica1(list_right[right].state)):
                resultado.append(list_left[left])
                left+=1
            else:
                resultado.append(list_right[right])
                right+=1

        resultado += list_left[left:]
        resultado += list_right[right:]
        return resultado

    def mergesortNodes(self,lista):

        if len(lista) <= 1:
            return lista

        mid = len(lista) // 2
        left = self.mergesortNodes(lista[:mid])
        right = self.mergesortNodes(lista[mid:])
        return self.mergeNodes(left,right)

    def algorithm(self):
        initstate = State([1,2,6,7,5,6,7,3],[4],[5,5,5],[7,3,1,3])
        node = Node(0,initstate,None)
        open = [node]
        closed = []
        exito = False
        while len(open) and not exito:
            N = open.pop(0)
            while N in closed:
                N = open.pop(0)
            if self.isFinal(N.state):
                exito = True
            else:
                closed.append(N)
                open = self.mergeNodes(open,self.expand(N))
        if exito:
            print("Coste: " + str(N.coste))
            while N:
                if N.prevAl:
                    print(N.prevAl)

                N = N.father
        else:
            print("No hay solución")

astar = ASTAR()
astar.algorithm()














