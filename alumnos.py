from constraint import *

problem = Problem()

alumnos = [1, 2, 3]

asientos_totales = [1,2,3,4]

mov_red = [1,2]


problem.addVariable(1,mov_red)

problem.addVariables([2,3],asientos_totales)


problem.addConstraint(AllDifferentConstraint(),alumnos)



def notTogether(a,b):
    if a == 1 and b != 2:
        return True
    elif a==2 and b!=1:
        return True
    return False

for i in alumnos