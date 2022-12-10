class State:
    #Estado que representa
    def __init__(self,alumnosXX,alumnosXR,alumnosCX,alumnosCR,prev_confl=[]):
        self.alumnosXX = alumnosXX
        self.alumnosXR = alumnosXR
        self.alumnosCX = alumnosCX
        self.alumnosCR = alumnosCR
        self.prev_confl = prev_confl


class Node:
    def __init__(self, coste: int, state: State, prevAl=None):
        self.father = None
        self.state = state
        self.coste = coste
        self.prevAl = prevAl