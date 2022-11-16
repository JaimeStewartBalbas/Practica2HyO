from constraint import *

problem = Problem()

#hardcodeamos los  asientos del bus en este caso 8 asientos
asientos_totales = list(range(1,8+1))

#diccionario que me dice si una persona de movilidad reducida se sienta en una asiento, donde no se puede sentar el otro
#Es decir si una persona con mov.red. se sienta en el 1,  en el 2 no se puede sentar nadie.
dict = {1:2,2:1,5:6,6:5}

#asientos de movilidad reducida
asientos_reducidos = dict.keys()


#Tenemos 3 alumnos dos de ellos es de movilidad reducida.
data  = [[1,1,"X","R",3],
         [2,2,"X","X",0],
         [3,2,"X","R",1]]

alumnos_totales = list(range(1,len(data)+1))
alumnos_reducidos = []
#por cada persona en nuestro data-set, añadimos una variable con su id
for i in range(len(data)):
    #Si la persona no es de movilidad reducida su dominio es asientos_totales
    if data[i][3] == "X":
        problem.addVariable(data[i][0],asientos_totales)
    # Si la persona  es de movilidad reducida su dominio es asientos_reducidos
    else:
        problem.addVariable(data[i][0], asientos_reducidos)
        alumnos_reducidos.append(data[i][0])



#Verifica que un único alumno se sienta en un solo sitio.
problem.addConstraint(AllDifferentConstraint(),alumnos_totales)



def notTogether(a,b):
    """Se asegura que, los alumnos de movilidad reducida se sienten solos"""
    for i in dict:
      if a == i and b != dict[i]:
          return True
    return False






for i in alumnos_reducidos:
    for j in alumnos_totales:
        if i != j:
            problem.addConstraint(notTogether,(i,j))




print(problem.getSolutions())
