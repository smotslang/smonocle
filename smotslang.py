import numpy as np
import re

class Token:
    name = ""
    func = None

def define_tokens():
    defs = []
    
    climb = Token()
    climb.name = climb
    def climbfunc():
        pass
    climb.func = climbfunc
    defs.append(climb)


class Program:
    memArr = np.full(4096, 0)
    springLocs = np.full(4096, 0)
    memPointer = 0
    pc = 0
    prgmArr = None
    workingFile = None

    def __init__(self, prgmArr, file):
        f = open(file, "r")
        self.prgmArr = re.split("\s+", f.read())
        f.close()
        self.workingFile = file

    def currentMemValue(self):
        return self.memArr[self.memPointer]
    def setCurrentMemValue(self, val):
        self.memArr[self.memPointer] = val
    def currentToken(self):
        return self.prgmArr[self.pc]