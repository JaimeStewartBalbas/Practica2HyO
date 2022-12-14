
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
    #Estado que representa el problema
    def __init__(self,alumnosXX,alumnosXR,alumnosCX,alumnosCR):
        self.alumnosXX = alumnosXX
        self.alumnosXR = alumnosXR
        self.alumnosCX = alumnosCX
        self.alumnosCR = alumnosCR




class Node:
    """Clase para los nodos del arbol"""
    def __init__(self,coste:int,state:State,prevAl=None,sitio=None,prev_confl=[]):
        self.father = None
        self.state = state
        self.coste = coste
        self.prevAl = prevAl
        self.sitio = sitio
        self.prev_confl = prev_confl


class ASTAR:
    """Clase para implementar los algoritmos de A*"""

    def heuristica1(self,estado:State)->int:
        """ Relajando todas las retricciones, es decir solo hay coste 1"""
        return len(estado.alumnosXR) + len(estado.alumnosCR) +  len(estado.alumnosXX) + len(estado.alumnosCX)


    def heuristica2(self,estado:State)->int:
        """Relajando restricciones de conflictivos """
        reducidos = len(estado.alumnosXR) + len(estado.alumnosCR)
        normales = len(estado.alumnosXX) + len(estado.alumnosCX)
        if normales >= reducidos:
            return 3*reducidos + 1*(normales-reducidos)
        return float('inf')




    def isFinal(self,N:State):
        """Comprobamos el estado final """
        if not len(N.alumnosCR) and not len(N.alumnosXX) and not len(N.alumnosXR) and not len(N.alumnosCX):
            return True
        return False

    def addXX(self,state:State,prevAl,index,prev_confl):
        """Operador para añadir una persona XX a la cola"""
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
        """Operador para añadir una persona XR a la cola"""
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
        """Operador para añadir una persona CX a la cola"""
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
        """Operador para añadir una persona CR a la cola"""
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
        """Función para expandir el nodo que entra por parámetro"""
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
        """Funcion para mergear nodos NO LO UTILIZAMOS AL FINAL"""
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
        """Función para hacer mergesort a los nodos NO LO UTILIZAMOS AL FINAL"""

        if len(lista) <= 1:
            return lista

        mid = len(lista) // 2
        left = self.mergesortNodes(lista[:mid])
        right = self.mergesortNodes(lista[mid:])
        return self.mergeNodes(left,right)

    def insertNode(self,a, x,heuristica, lo=0, hi=None):
        """Función para hallar indice con binary search e insertar ordenadamente"""
        if hi is None:
            hi = len(a)
        if heuristica == '1':
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
        elif heuristica == "2":
            while lo < hi:
                mid = (lo + hi) // 2
                if(x.coste + self.heuristica2(x.state) == a[mid].coste + self.heuristica2(a[mid].state)):
                    if x.coste < a[mid].coste:
                        hi = mid
                    else:
                        lo = mid + 1
                elif x.coste + self.heuristica2(x.state)< a[mid].coste + self.heuristica2(a[mid].state):
                    hi = mid
                else:
                    lo = mid + 1
            a.insert(lo, x)
            return a

    def algorithm(self,initstate,heuristica):
        """implementación de A*"""
        node = Node(0,initstate,None)
        open = [node]
        closed = []
        exito = False
        nodos_expandidos = 1
        while len(open) and not exito:
            N = open.pop(0)
            while N in closed:
                N = open.pop(0)
            if self.isFinal(N.state):
                exito = True
            else:
                closed.append(N)
                succesors =  self.expand(N)
                nodos_expandidos += len(succesors)
                for i in succesors:
                    open = self.insertNode(open,i,heuristica)

        resultado = []
        costefin = 0
        longitud = 0
        if exito:
            costefin = N.coste
            while N:
                longitud +=1
                if N.prevAl:
                    resultado.append(N.sitio)

                N = N.father
            return resultado,costefin,(longitud-1),nodos_expandidos
        else:
            return resultado,costefin,longitud,nodos_expandidos


#-----------MAIN PROGRAM----------#
"""Extraemos los argumentos de teclado"""
import sys

filePath = sys.argv[1]
heuristica = sys.argv[2]


def extractFile(myfilepath):
    """Método para extraer el nombre del archivo, dado un path"""
    file = ""
    revFile = myfilepath[::-1]
    char = revFile[0]
    i = 0
    while char != "/":
        char = revFile[i]
        file = file + char
        i+=1

    temp = file[::-1]
    temp2 = temp[1:]
    return temp2[:-4]
file = extractFile(filePath)

fileoutput = "./ASTAR-tests/" + file[:-1] +"-" + heuristica + ".output"

filestat = "./ASTAR-tests/" + file[:-1] +"-" + heuristica + ".stat"

"""Leemos el input de entrada"""
with open(filePath) as f:
    input = eval(f.readline())

alumnosXX,alumnosXR,alumnosCX,alumnosCR = [],[],[],[]

"""Extraemos los datos y los guardamos en listas"""
for i in input:
    if i[-2:] == "XX":
        alumnosXX.append(input[i])
    elif  i[-2:] == "CX":
        alumnosCX.append(input[i])
    elif i[-2:] == "XR":
        alumnosXR.append(input[i])
    elif i[-2:] == "CR":
        alumnosCR.append(input[i])


"""Creamos el estado inicial"""
initstate = State(alumnosXX,alumnosXR,alumnosCX,alumnosCR)

import time

"""Realizamos las mediciones de tiempo e invocamos ASTAR """
init_time = time.time()
astar = ASTAR()
result , coste ,longitud_plan,nodos_expandidos = astar.algorithm(initstate,heuristica)
end = (time.time() - init_time)

new = result[::-1]
inv_map = {v: k for k, v in input.items()}
output = {}
for i in new:
    output[inv_map[int(i)]] = int(i)


"""Escribimos los resultados en los archibos de salida"""
with open(fileoutput,"w") as f:
    f.write(("INICIAL: " + str(input) + "\n"))
    f.write( ("FINAL: " + str(output) + "\n"))


with open(filestat,"w") as f:
    f.write(("Tiempo total: " + str(end) + "\n"))
    f.write(("Coste total: " + str(coste) + "\n"))
    f.write(("Longitud del plan: " + str(longitud_plan) + "\n"))
    f.write(("Nodos expandidos: " + str(nodos_expandidos) + "\n"))






