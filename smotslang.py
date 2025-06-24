import numpy as np
import math
import pygame
import re

def smotsError(err):
    print(f"Error! {err}")
    input("(Press any key to close)")
    pygame.quit()
    exit()


class Token:
    name = ""
    func = None


class Program:
    defs = []
    memArr = np.full(4096, 0)
    springLocs = np.full(4096, 0)
    memPointer = 0
    pc = 0
    prgmArr = None
    workingFile = None

    def __init__(self, file):
        f = open(file, "r")
        self.prgmArr = re.split("\\s+", f.read())
        f.close()
        self.workingFile = file
        self.define_tokens()

    def define_tokens(self):
        self.defs = []
        '''
        token = Token()
        token.name = ""
        def tokenfunc(prgm):
            pass
        token.func = tokenfunc
        self.defs.append(token)
        '''

        # climb
        token_climb = Token()
        token_climb.name = "climb"
        def token_climbfunc(prgm):
            prgm.setCurrentMemValue(prgm.currentMemValue() + 1)
        token_climb.func = token_climbfunc
        self.defs.append(token_climb)

        # fall
        token_fall = Token()
        token_fall.name = "fall"
        def token_fallfunc(prgm):
            prgm.setCurrentMemValue(prgm.currentMemValue() - 1)
        token_fall.func = token_fallfunc
        self.defs.append(token_fall)

        # run (might deprecate as there should not be a console)
        token_run = Token()
        token_run.name = "run"
        def token_runfunc(prgm):
            print(str(prgm.currentMemValue()))
        token_run.func = token_runfunc
        self.defs.append(token_run)

    def currentMemValue(self):
        return self.memArr[self.memPointer]
    def setCurrentMemValue(self, val):
        self.memArr[self.memPointer] = val
    def currentToken(self):
        return self.prgmArr[self.pc]
    def consumeToken(self):
        self.pc += 1
        return self.currentToken()
    
    def interpret(self):
        # :smearful:
        while self.pc < len(self.prgmArr):
            for i in self.defs:
                if self.currentToken() == i.name:
                    i.func(self)
                    break
            self.pc += 1

    def parseTokenAsNumber(self, token):
        # even more :smearful:
        if token[0] == "$":
            addr = self.parseTokenAsNumber(token[1:])
            if addr > len(self.memArr):
                smotsError(f"Attempted to read value from address {addr}, which is outside of the bounds of the memory array.")
            return self.memArr[addr]
        elif token[0] == "^":
            out = int(token[1:])
            if math.isnan(out):
                smotsError(f"Error parsing Smotsinary value: {token}")
            return out
        elif token[0] == "'":
            return ord(token[1])
        else:
            return self.parseSmotsinary(token)

    def parseSmotsinary(self, token):
        out_str = ""
        for i in token:
            if i == "7":
                out_str += "0"
            elif i == "8":
                out_str += "1"
            else:
                smotsError(f"Unexpected character {i} in Smotsinary literal.")
        out = int(out_str, 2)
        if math.isnan(out):
            smotsError(f"Error parsing Smotsinary value: {token}")
        return out
    
    def programFromSelf(self, file):
        prgm = Program(file)
        prgm.memArr = self.memArr
        prgm.springLocs = self.springLocs
        prgm.workingFile = self.workingFile
        return prgm
