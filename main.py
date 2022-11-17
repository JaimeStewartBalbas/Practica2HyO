from constraint import *

problem = Problem()

alumnos = [1, 2, 3]

variables = [1,2,3,4,5]
total_domain = [0] + alumnos




problem.addVariables(variables, total_domain)

def differentPerson(a, b):
    if a != b:
        return True
    elif a == 0 or b == 0:
        return True
    return False

def allStudents(*combinations):
    n_alumnos = len(alumnos)
    counter = 0
    for i in combinations:
        pass

problem.addConstraint(allStudents,variables)

for i in variables:
    for j in variables:
        if i != j:
            problem.addConstraint(differentPerson,(i, j))






print(problem.getSolutions())