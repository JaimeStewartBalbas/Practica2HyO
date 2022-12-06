class State:
    #Estado que representa
    def __init__(self,alumnosXX,alumnosXR,alumnosCX,alumnosCR):
        self.alumnosXX = alumnosXX
        self.alumnosXR = alumnosXR
        self.alumnosCX = alumnosCX
        self.alumnosCR = alumnosCR
        self.prevAl = None
        self.coste = 0


    def addXX(self):
        if len(self.alumnosXX) > 0:
            self.prevAl = "XX"
            self.alumnosXX.pop(0)
            if self.prevAl==None:
                return 1
            elif self.prevAl == "XR":
                return 0
            elif self.prevAl == "CX":
                return 2
            elif self.prevAl == "CR":
                return  3

    def addXR(self):
        if len(self.alumnosXR) > 0:
            self.prevAl = "XR"
            self.alumnosXR.pop(0)
            if self.prevAl == None:
                return 3
            elif self.prevAl = "XR":
                return iny('inf')
            elif self.prevAl == "CX":
                return 2


    def addCX(self):
        pass


    def addCR(self):
        pass


    def heuristica(self,estado:state)->int:
        pass


