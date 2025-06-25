import numpy as np
import math
import random
import pygame
import re

def smotsError(err):
    pygame.quit()
    print(f"Error! {err}")
    input("(Press any key to close)")
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
    game = None
    graphics = {
        "verts":[],
        "color":pygame.Color(255, 0, 0)
    }

    def __init__(self, file, game):
        f = open(file, "r")
        self.prgmArr = re.split("\\s+", f.read())
        f.close()
        self.workingFile = file
        self.define_tokens()
        self.game = game

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

        # wind
        token_wind = Token()
        token_wind.name = "wind"
        def token_windfunc(prgm):
            adrInt = prgm.parseTokenAsNumber(prgm.consumeToken())
            if len(prgm.memArr) > adrInt:
                prgm.memArr[adrInt] = prgm.currentMemValue()
            else:
                smotsError(f"Wind attempts to copy over the maximum memory limit ({len(prgm.memArr)} Adresses)!")
        token_wind.func = token_windfunc
        self.defs.append(token_wind)

        # dash
        token_dash = Token()
        token_dash.name = "dash"
        def token_dashfunc(prgm):
            adrInt = prgm.parseTokenAsNumber(prgm.consumeToken())
            if len(prgm.memArr) > adrInt:
                prgm.memPointer = adrInt
            else:
                smotsError(f"Dash attempts to move to a memory adress that is out of range! ({len(prgm.memArr)} Adresses)")
        token_dash.func = token_dashfunc
        self.defs.append(token_dash)

        # jump
        token_jump = Token()
        token_jump.name = "jump"
        def token_jumpfunc(prgm):
            prgm.springLocs[prgm.parseTokenAsNumber(prgm.consumeToken())] = prgm.pc
        token_jump.func = token_jumpfunc
        self.defs.append(token_jump)

        # spring
        token_spring = Token()
        token_spring.name = "spring"
        def token_springfunc(prgm):
            if prgm.currentMemValue() != 0:
                prgm.pc = prgm.springLocs[prgm.parseTokenAsNumber(prgm.consumeToken())]
        token_spring.func = token_springfunc
        self.defs.append(token_spring)

        # crumble
        token_crumble = Token()
        token_crumble.name = "crumble"
        def token_crumblefunc(prgm):
            prgm.setCurrentMemValue(prgm.parseTokenAsNumber(prgm.consumeToken()))
        token_crumble.func = token_crumblefunc
        self.defs.append(token_crumble)

        # spinner
        token_spinner = Token()
        token_spinner.name = "spinner"
        def token_spinnerfunc(prgm):
            if random.randint(1,3) == 1:
                prgm.setCurrentMemValue(1)
            else:
                prgm.setCurrentMemValue(0)
        token_spinner.func = token_spinnerfunc
        self.defs.append(token_spinner)

        # smots5 :fear:
        token_smots5 = Token()
        token_smots5.name = "smots5"
        def token_smots5func(prgm):
            prgm.game.running = False
        token_smots5.func = token_smots5func
        self.defs.append(token_smots5)

        # spike
        token_spike = Token()
        token_spike.name = "spike"
        def token_spikefunc(prgm):
            adrInt = prgm.parseTokenAsNumber(prgm.consumeToken())
            adrInt2 = -7

            if prgm.currentMemValue() == 0:
                while adrInt2 != adrInt:
                    while prgm.currentToken() != "jump":
                        prgm.pc += 1
                    adrInt2 = prgm.parseTokenAsNumber(prgm.consumeToken())
                prgm.pc -= 2
        token_spike.func = token_spikefunc
        self.defs.append(token_spike)

        # trigspike
        token_trigspike = Token()
        token_trigspike.name = "trigspike"
        def token_trigspikefunc(prgm):
            givenVal = prgm.parseTokenAsNumber(prgm.consumeToken())
            adrInt = prgm.parseTokenAsNumber(prgm.consumeToken())
            adrInt2 = -7

            if prgm.currentMemValue() != givenVal:
                while adrInt2 != adrInt:
                    while prgm.currentToken() != "jump":
                        prgm.pc += 1
                    adrInt2 = prgm.parseTokenAsNumber(prgm.consumeToken())
                prgm.pc -= 2
        token_trigspike.func = token_trigspikefunc
        self.defs.append(token_trigspike)

        # comments! :3
        token_com = Token()
        token_com.name = "--"
        def token_comfunc(prgm):
            prgm.pc += 1
            while not ("--" in prgm.currentToken()):
                prgm.pc += 1
        token_com.func = token_comfunc
        self.defs.append(token_com)

        # smonocle specific tokens
        self.define_mono_tokens()

    def define_mono_tokens(self):
        # graphics module
        self.define_mono_graphics()
        # input module
        self.define_mono_input()

    def define_mono_graphics(self):
        # begin poly
        token_beginp = Token()
        token_beginp.name = "smonocle.graphics.begin_poly"
        def token_beginpfunc(prgm):
            prgm.graphics["verts"] = []
        token_beginp.func = token_beginpfunc
        self.defs.append(token_beginp)

        # add vert
        token_addp = Token()
        token_addp.name = "smonocle.graphics.add_vert"
        def token_addpfunc(prgm):
            prgm.graphics["verts"].append((prgm.parseTokenAsNumber(prgm.consumeToken()), prgm.parseTokenAsNumber(prgm.consumeToken())))
        token_addp.func = token_addpfunc
        self.defs.append(token_addp)

        # end poly
        token_endp = Token()
        token_endp.name = "smonocle.graphics.end_poly"
        def token_endpfunc(prgm):
            pygame.draw.polygon(prgm.game.screen, prgm.graphics["color"], prgm.graphics["verts"])
        token_endp.func = token_endpfunc
        self.defs.append(token_endp)

        # set color
        token_setc = Token()
        token_setc.name = "smonocle.graphics.set_color"
        def token_setcfunc(prgm):
            prgm.graphics["color"] = pygame.Color(prgm.consumeNum(),prgm.consumeNum(),prgm.consumeNum(),a=prgm.consumeNum())
        token_setc.func = token_setcfunc
        self.defs.append(token_setc)

    def define_mono_input(self):
        # poll key
        token_poll = Token()
        token_poll.name = "smonocle.input.poll"
        def token_pollfunc(prgm):
            if pygame.key.get_pressed()[pygame.key.key_code(prgm.consumeToken())]:
                prgm.setCurrentMemValue(1)
            else:
                prgm.setCurrentMemValue(0)
        token_poll.func = token_pollfunc
        self.defs.append(token_poll)

        # mouse pos
        token_mx = Token()
        token_mx.name = "smonocle.input.mousex"
        def token_mxfunc(prgm):
            prgm.setCurrentMemValue(pygame.mouse.get_pos()[0])
        token_mx.func = token_mxfunc
        self.defs.append(token_mx)
        
        token_my = Token()
        token_my.name = "smonocle.input.mousey"
        def token_myfunc(prgm):
            prgm.setCurrentMemValue(pygame.mouse.get_pos()[1])
        token_my.func = token_myfunc
        self.defs.append(token_my)

        # poll mouse
        token_pollm = Token()
        token_pollm.name = "smonocle.input.poll_mouse"
        def token_pollmfunc(prgm):
            if pygame.mouse.get_pressed(num_buttons=5)[prgm.parseTokenAsNumber(prgm.consumeToken())]:
                prgm.setCurrentMemValue(1)
            else:
                prgm.setCurrentMemValue(0)
        token_pollm.func = token_pollmfunc
        self.defs.append(token_pollm)

    def currentMemValue(self):
        return self.memArr[self.memPointer]
    def setCurrentMemValue(self, val):
        self.memArr[self.memPointer] = val
    def currentToken(self):
        return self.prgmArr[self.pc]
    def consumeToken(self):
        self.pc += 1
        return self.currentToken()
    def consumeNum(self):
        return self.parseTokenAsNumber(self.consumeToken())
    
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
    
    def programFromSelf(self, file, game):
        prgm = Program(file, game)
        prgm.memArr = self.memArr
        prgm.springLocs = self.springLocs
        prgm.workingFile = self.workingFile
        return prgm
