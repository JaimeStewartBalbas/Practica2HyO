
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
    def __init__(self,alumnosXX,alumnosXR,alumnosCX,alumnosCR):
        self.alumnosXX = alumnosXX
        self.alumnosXR = alumnosXR
        self.alumnosCX = alumnosCX
        self.alumnosCR = alumnosCR




class Node:
    def __init__(self,coste:int,state:State,prevAl=None,sitio=None,prev_confl=[]):
        self.father = None
        self.state = state
        self.coste = coste
        self.prevAl = prevAl
        self.sitio = sitio
        self.prev_confl = prev_confl


class ASTAR:

    def heuristica0(self)->int:
        return 0

    def heuristica1(self,estado:State)->int:
        reducidos = len(estado.alumnosXR) + len(estado.alumnosCR)
        normales = len(estado.alumnosXX) + len(estado.alumnosCX)
        if normales >= reducidos:
            return 3*reducidos + 1*(normales-reducidos)
        return float('inf')

    def heuristica2(self,):
        pass


    def heuristica01(self, estado):
        """Sobreestimamos"""
        conflictivos = len(estado.alumnosCX) + len(estado.alumnosCR)
        normales = len(estado.alumnosXX) + len(estado.alumnosXR)
        if conflictivos == 0:
            return normales
        elif conflictivos == 1 or conflictivos == 2:
            return normales + conflictivos*2
        elif conflictivos > 2:
            return 2*2 + 3*(conflictivos - 2) + normales
        return float('inf')


    def isFinal(self,N:State):
        if not len(N.alumnosCR) and not len(N.alumnosXX) and not len(N.alumnosXR) and not len(N.alumnosCX):
            return True
        return False

    def addXX(self,state:State,prevAl,index,prev_confl):
        extra = 0
        asiento = state.alumnosXX[index]
        for i in prev_confl:
            if asiento > i:
                extra += 1
        if len(state.alumnosXX) > 0:
            if prevAl == None:

                lista = state.alumnosXX.copy()
                del lista[index]
                newstate = State(lista,state.alumnosXR,state.alumnosCX,state.alumnosCR)
                return [newstate,1+extra,"XX",prev_confl]
            elif prevAl == "XX":
                lista = state.alumnosXX.copy()
                del lista[index]
                newstate = State(lista, state.alumnosXR, state.alumnosCX, state.alumnosCR)
                return [newstate,1+extra,"XX",prev_confl]
            elif prevAl == "XR":
                lista = state.alumnosXX.copy()
                del lista[index]
                newstate = State(lista, state.alumnosXR, state.alumnosCX, state.alumnosCR)
                return [newstate,0,"XX",prev_confl]
            elif prevAl == "CX":
                lista = state.alumnosXX.copy()
                del lista[index]
                newstate = State(lista, state.alumnosXR, state.alumnosCX, state.alumnosCR)
                return [newstate,2+extra,"XX",prev_confl]
            elif prevAl == "CR":
                lista = state.alumnosXX.copy()
                del lista[index]
                newstate = State(lista, state.alumnosXR, state.alumnosCX, state.alumnosCR)
                return [newstate,0,"XX",prev_confl]
        return float('inf')


    def addXR(self,state:State,prevAl,index,prev_confl):
        extra = 0
        asiento = state.alumnosXR[index]

        for i in prev_confl:
            if asiento > i:
                extra += 1
        if len(state.alumnosXR) > 0 and (len(state.alumnosXX) + len(state.alumnosCX)) > 0:
            if prevAl == None:
                lista = state.alumnosXR.copy()
                del lista[index]
                newstate = State(state.alumnosXX, lista, state.alumnosCX, state.alumnosCR)
                return [newstate, 3+3*extra, "XR",prev_confl]
            elif prevAl == "XX":
                lista = state.alumnosXR.copy()
                del lista[index]
                newstate = State(state.alumnosXX, lista, state.alumnosCX, state.alumnosCR)
                return [newstate, 3+3*extra, "XR",prev_confl]
            elif prevAl == "XR":
                return float('inf')
            elif prevAl == "CX":
                lista = state.alumnosXR.copy()
                del lista[index]
                newstate = State(state.alumnosXX, lista, state.alumnosCX, state.alumnosCR)
                return [newstate, 6+3*extra, "XR",prev_confl]
            elif prevAl == "CR":
                return float('inf')

        return float('inf')

    def addCX(self,state:State,prevAl, grandpa,index,prev_confl):
        extra = 0
        asiento = state.alumnosCX[index]
        for i in prev_confl:
            if asiento > i:
                extra += 1
        if len(state.alumnosCX) > 0:
            if prevAl == None:
                lista = state.alumnosCX.copy()
                del lista[index]
                newstate = State(state.alumnosXX, state.alumnosXR, lista, state.alumnosCR)

                return [newstate, 1, "CX",prev_confl+[asiento]]
            elif prevAl == "XX":
                if grandpa != "XR" and grandpa != "CR":
                    lista = state.alumnosCX.copy()
                    del lista[index]
                    newstate = State(state.alumnosXX, state.alumnosXR, lista, state.alumnosCR)
                    return [newstate, 2+extra, "CX",prev_confl+[asiento]]
                else:
                    lista = state.alumnosCX.copy()
                    del lista[index]
                    newstate = State(state.alumnosXX, state.alumnosXR, lista, state.alumnosCR)
                    return [newstate, 1+extra, "CX",prev_confl+[asiento]]
            elif prevAl == "XR":
                lista = state.alumnosCX.copy()
                del lista[index]
                newstate = State(state.alumnosXX, state.alumnosXR, lista, state.alumnosCR)
                return [newstate, 3, "CX",prev_confl+[asiento]]
            elif prevAl == "CX":
                if grandpa != "XR" and grandpa != "CR":
                    lista = state.alumnosCX.copy()
                    del lista[index]
                    newstate = State(state.alumnosXX, state.alumnosXR, lista, state.alumnosCR)
                    return [newstate, 3+extra, "CX",prev_confl+[asiento]]
                else:
                    lista = state.alumnosCX.copy()
                    del lista[index]
                    newstate = State(state.alumnosXX, state.alumnosXR, lista, state.alumnosCR)
                    return [newstate, 2+extra, "CX",prev_confl+[asiento]]
            elif prevAl == "CR":
                lista = state.alumnosCX.copy()
                del lista[index]
                newstate = State(state.alumnosXX, state.alumnosXR, lista, state.alumnosCR)
                return [newstate, 3, "CX",prev_confl+[asiento]]

        return float('inf')

    def addCR(self,state:State,prevAl, grandpa,index,prev_confl):
        extra = 0
        asiento = state.alumnosCR[index]
        for i in prev_confl:
            if asiento > i:
                extra += 1
        if len(state.alumnosCR) > 0 and (len(state.alumnosXX) + len(state.alumnosCX)) > 0:
            if prevAl == None:
                lista = state.alumnosCR.copy()
                del lista[index]
                newstate = State(state.alumnosXX, state.alumnosXR, state.alumnosCX, lista)
                return [newstate, 3+3*extra, "CR",prev_confl+[asiento]]
            elif prevAl == "XX":
                if grandpa != "XR" and grandpa != "CR":
                    lista = state.alumnosCR.copy()
                    del lista[index]
                    newstate = State(state.alumnosXX, state.alumnosXR, state.alumnosCX, lista)
                    return [newstate, 4+3*extra, "CR",prev_confl+[asiento]]
                else:
                    lista = state.alumnosCR.copy()
                    del lista[index]
                    newstate = State(state.alumnosXX, state.alumnosXR, state.alumnosCX, lista)
                    return [newstate, 3+3*extra, "CR",prev_confl+[asiento]]
            elif prevAl == "XR":
                return float('inf')
            elif prevAl == "CX":
                if grandpa != "XR" and grandpa != "CR":
                    lista = state.alumnosCR.copy()
                    del lista[index]
                    newstate = State(state.alumnosXX, state.alumnosXR, state.alumnosCX, lista)
                    return [newstate, 7+3*extra, "CR",prev_confl+[asiento]]
                else:
                    lista = state.alumnosCR.copy()
                    del lista[index]
                    newstate = State(state.alumnosXX, state.alumnosXR, state.alumnosCX, lista)
                    return [newstate, 6+3*extra, "CR",prev_confl+[asiento]]
            elif prevAl == "CR":
                return float('inf')
        return float('inf')



    def expand(self,node:Node):
        succesors = []
        for i in range(len(node.state.alumnosXX)):
         x = self.addXX(node.state,node.prevAl,i,node.prev_confl)
         if type(x) != float:
             newnode = Node(node.coste + x[1], x[0], x[2])
             newnode.father = node
             newnode.sitio = str(node.state.alumnosXX[i])
             newnode.prev_confl=x[3]
             succesors.append(newnode)
        for j in range(len(node.state.alumnosXR)):
            y = self.addXR(node.state,node.prevAl,j,node.prev_confl)
            if type(y) != float:
                newnode = Node(node.coste + y[1], y[0], y[2])
                newnode.father = node
                newnode.sitio = str(node.state.alumnosXR[j])
                newnode.prev_confl = y[3]
                succesors.append(newnode)
        if node.father is None:
            for k in range(len(node.state.alumnosCX)):
                z = self.addCX(node.state, node.prevAl, None,k,node.prev_confl)
                if type(z) != float:
                    newnode = Node(node.coste + z[1], z[0], z[2])
                    newnode.father = node
                    newnode.sitio = str(node.state.alumnosCX[k])
                    newnode.prev_confl = z[3]
                    succesors.append(newnode)
            for l in range(len(node.state.alumnosCR)):
                w = self.addCR(node.state, node.prevAl, None,l,node.prev_confl)
                if type(w) != float:
                    newnode = Node(node.coste + w[1], w[0], w[2])
                    newnode.father = node
                    newnode.sitio = str(node.state.alumnosCR[l])
                    newnode.prev_confl = w[3]
                    succesors.append(newnode)
        else:
            for k in range(len(node.state.alumnosCX)):
                z = self.addCX(node.state,node.prevAl, node.father.prevAl,k,node.prev_confl)
                if type(z) != float:
                    newnode = Node(node.coste + z[1], z[0], z[2])
                    newnode.father = node
                    newnode.sitio = str(node.state.alumnosCX[k])
                    newnode.prev_confl = z[3]
                    succesors.append(newnode)
            for l in range(len(node.state.alumnosCR)):
                w = self.addCR(node.state,node.prevAl, node.father.prevAl,l,node.prev_confl)
                if type(w) != float:
                    newnode = Node(node.coste + w[1], w[0], w[2])
                    newnode.father = node
                    newnode.sitio = str(node.state.alumnosCR[l])
                    newnode.prev_confl = w[3]
                    succesors.append(newnode)
        return succesors

    def mergeNodes(self,list_left,list_right):
        left, right = 0,0
        resultado =  []
        while right < len(list_right) and left < len(list_left):
            if (list_left[left].coste+self.heuristica0(list_left[left].state)) == (list_right[right].coste+self.heuristica0(list_right[right].state)):
                if list_left[left].coste < list_right[right].coste:
                    resultado.append(list_left[left])
                    left += 1
                else:
                    resultado.append(list_right[right])
                    right += 1
            elif (list_left[left].coste+self.heuristica0(list_left[left].state)) < (list_right[right].coste+self.heuristica0(list_right[right].state)):
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

    def insertNode(self,a, x, lo=0, hi=None):
        if hi is None:
            hi = len(a)
        while lo < hi:
            mid = (lo + hi) // 2
            if(x.coste + self.heuristica1(x.state) == a[mid].coste + self.heuristica1(a[mid].state)):
                if x.coste < a[mid].coste:
                    hi = mid
                else:
                    lo = mid + 1
            elif x.coste + self.heuristica1(x.state)< a[mid].coste + self.heuristica1(a[mid].state):
                hi = mid
            else:
                lo = mid + 1
        a.insert(lo, x)
        return a

    def algorithm(self,initstate):
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
                succesors =  self.expand(N)
                for i in succesors:
                    open = self.insertNode(open,i)

        resultado = []
        if exito:
            print("Coste:" + str(N.coste))
            while N:
                if N.prevAl:
                    resultado.append(N.sitio)

                N = N.father
            return resultado
        else:
            print("No hay solución")
            return resultado



import sys

filePath = "./ASTAR-tests/alumnos10.prob"
with open(filePath) as f:
    input = eval(f.readline())

alumnosXX,alumnosXR,alumnosCX,alumnosCR = [],[],[],[]


for i in input:
    if i[-2:] == "XX":
        alumnosXX.append(input[i])
    elif  i[-2:] == "CX":
        alumnosCX.append(input[i])
    elif i[-2:] == "XR":
        alumnosXR.append(input[i])
    elif i[-2:] == "CR":
        alumnosCR.append(input[i])



initstate = State(alumnosXX,alumnosXR,alumnosCX,alumnosCR)

astar = ASTAR()
result = astar.algorithm(initstate)
new = result[::-1]
inv_map = {v: k for k, v in input.items()}
output = {}
for i in new:
    output[inv_map[int(i)]] = int(i)


print(output)











