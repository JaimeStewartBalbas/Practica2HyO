from constraint import *

problem = Problem()

#hardcodeamos los  asientos del bus en este caso 8 asientos
filas_bus = 3
columnas_bus = 2
n_asientos = filas_bus*columnas_bus
asientos_totales = list(range(1,n_asientos+1))

#diccionario que me dice si una persona de movilidad reducida se sienta en una asiento, donde no se puede sentar el otro
#Es decir si una persona con mov.red. se sienta en el 1,  en el 2 no se puede sentar nadie.
dict = {1:2,2:1,3:4,4:3}

#asientos de movilidad reducida
asientos_reducidos = list(dict.keys())



#Tenemos 3 alumnos dos de ellos es de movilidad reducida.
data  = [[1,1,"C","X",1],
         [2,1,"X","R",0],
         [3,2,"X","X",0],
         [4,2,"C","X",1],
         [5,1,"X","R",0]]

alumnos_totales = list(range(1,len(data)+1))
alumnos_reducidos = []
alumnos_problematicos = []
alumnos_menores = []
alumnos_mayores = []
alumnos_hermanos = {}
#por cada persona en nuestro data-set, añadimos una variable con su id
for i in range(len(data)):
    #Si la persona no es de movilidad reducida su dominio es asientos_totales
    if data[i][3] == "X":
        problem.addVariable(data[i][0],asientos_totales)
    # Si la persona  es de movilidad reducida su dominio es asientos_reducidos
    else:
        problem.addVariable(data[i][0], asientos_reducidos)
        alumnos_reducidos.append(data[i][0])
    if data[i][2] == "C":
        alumnos_problematicos.append(data[i][0])
    if  data[i][1] == 1:
        alumnos_menores.append(data[i][0])
    else:
        alumnos_mayores.append(data[i][0])
    if data[i][4] != 0:
        for j in range(len(data)):
            if data[j][4] == data[i][4] and i != j:
                alumnos_hermanos[data[i][0]] = data[j][0]


print(alumnos_hermanos)

# Verifica que un único alumno se sienta en un solo sitio.
problem.addConstraint(AllDifferentConstraint(),alumnos_totales)

#
def notTogether(a,b):
    """Se asegura que, los alumnos de movilidad reducida se sienten solos"""
    for i in dict:
      if a == i and b != dict[i]:
          return True
    return False

#Función que devuelve los asientos próximos al asiento que entra como parámetro
def getColindant(n_sit):
    if n_sit % columnas_bus == 0:
        if n_sit // columnas_bus == 1:
            return [n_sit -1, n_sit + columnas_bus - 1, n_sit + columnas_bus]
        elif n_sit // columnas_bus == filas_bus:
            return [n_sit - columnas_bus - 1, n_sit - columnas_bus, n_sit - 1]
        else:
            return[n_sit - columnas_bus - 1, n_sit - columnas_bus, n_sit - 1, n_sit + columnas_bus - 1 , n_sit + columnas_bus]
    elif n_sit % columnas_bus == 1:
        if n_sit // columnas_bus == 0:
            return [n_sit + 1, n_sit + columnas_bus, n_sit + columnas_bus + 1]
        elif n_sit // columnas_bus == (filas_bus - 1):
            return [n_sit - columnas_bus, n_sit - columnas_bus + 1, n_sit + 1]
        else:
            return [n_sit - columnas_bus, n_sit - columnas_bus + 1, n_sit + 1, n_sit + columnas_bus, n_sit + columnas_bus + 1]
    else:
        if n_sit // columnas_bus == 0:
            return [n_sit - 1, n_sit + 1, n_sit + columnas_bus - 1, n_sit + columnas_bus, n_sit + columnas_bus + 1]
        elif n_sit // columnas_bus == (filas_bus - 1):
            return [n_sit - columnas_bus - 1, n_sit - columnas_bus, n_sit - columnas_bus + 1, n_sit - 1, n_sit + 1 ]
        else:
            return [n_sit - columnas_bus - 1, n_sit - columnas_bus, n_sit - columnas_bus + 1, n_sit - 1, n_sit + 1,
                    n_sit + columnas_bus - 1, n_sit + columnas_bus, n_sit + columnas_bus + 1]

def getCloseSits(n_sit):
    if n_sit % columnas_bus == 0:
        return [n_sit - 1]
    elif n_sit % columnas_bus == 1:
        return [n_sit + 1]
    elif n_sit % columnas_bus == (columnas_bus//2):
        return [n_sit - 1]
    elif n_sit % columnas_bus == (columnas_bus//2 + 1):
        return [n_sit + 1]
    else:
        return [n_sit - 1, n_sit + 1]

def problematicStudents(a, b):
    sitios_no_validos = getColindant(a)
    if b not in sitios_no_validos:
        return True
    return False

#Verificamos que los estudiantes menores se sienten en el módulo de delante
def minorStudents(a):
    if a <= n_asientos//2:
        return True
    return False

#Verificamos que los estudiantes mayores se sienten en el módulo de atras
def mayorStudents(a):
    if a > n_asientos//2:
        return True
    return False

def hermanos_juntos(a, b):
    sitios_cercanos = getCloseSits(a)
    if b in sitios_cercanos:
        return True
    return False

#Verificamos que los alumnos reducidos tengan hueco al lado.
for i in alumnos_reducidos:
    for j in alumnos_totales:
        if i != j:
            problem.addConstraint(notTogether,(i,j))

# Restringimos que los alumnos problemáticos no se sienten cerca
for i in alumnos_problematicos:
    for j in (alumnos_problematicos + alumnos_reducidos):
        if i != j:
            if(i not in alumnos_hermanos) or (i in alumnos_hermanos and alumnos_hermanos[i] != j):
                problem.addConstraint(problematicStudents,(i,j))

# Restringimos que los del ciclo 1 se sienten delante y los del ciclo 2 detrás
for i in alumnos_menores:
    if i not in alumnos_hermanos:
        problem.addConstraint(minorStudents,(i,))

for i in alumnos_mayores:
    if i not in alumnos_hermanos:
        problem.addConstraint(mayorStudents,(i,))

# Restringimos que los hermanos solo se puedan sentar al lado
for hermano_referencia in alumnos_hermanos:
    for hermano in alumnos_hermanos:
        if hermano != hermano_referencia:
            problem.addConstraint(hermanos_juntos,(hermano_referencia, hermano))


print(problem.getSolutions())
