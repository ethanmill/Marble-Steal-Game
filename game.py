import time #Test
import sys
import os
import pygame
import serial
import random
from datetime import datetime
from multiprocessing import Process
from multiprocessing import SimpleQueue
from multiprocessing import set_start_method

sys.path.insert(1, './lib/') #Add custom library to path
import sound
import sorter
#Functions for sorter
# sortLoop() <--- main
#  sortmarble(color)
#  calibrateSensor(scanTime, colorOUT)
#  pollColor(scanTime, colorOUT, redAmbient, blueAmbient)

import turntable
#Functions for turtable
# dispenseMarble(color, player) <--- main
#  sortmarble(color)
#  elevatorDump()
#
# Usage:
# dispenseProc = Process(target=callDispense, args=(color,player,))
# dispenseProc.start()
# dispenseProc.join()

def printD(text):
    print(datetime.now().strftime("%H:%M:%S.%f"),"PID:",os.getpid(),"|",text)

def startSorter():
    s = sorter.sorter()
    s.sorterLoop()

def callDispense(color, player):
    def callDispenseProc(color, player):
        printD(str("Dispensing: "+color+" to "+player))
        d = turntable.turntable()
        d.dispenseMarble(color, player)
    dispenseProc = Process(target=callDispenseProc, args=(color,player,))
    dispenseProc.start()
    dispenseProc.join() #Yes I know this defeats the whole purpose of mutliprocessing but whatever

def imageDraw(path, pos=None, scale=None, fadeTime=None): #os.join then (X,Y) and (H,W) to scale to prevent problems later on
    #printD("Displaying: "+str(path)+" at "+str(pos))
    pos = (int(pos[0]),int(pos[1])) # Make sure it is an int (this may cause problems later fuck you idc)

    # Hopefully this is the worst code in this file
    img = pygame.image.load(path).convert()
    img = pygame.transform.scale(img, scale)
    maxAlpha = 255
    alphaStep = int(maxAlpha/25)

    if fadeTime > 0: # Fade in (This is fucking terrible)
        alpha = 0
        while alpha < maxAlpha:
            alpha += alphaStep
            if alpha > maxAlpha:
                alpha = maxAlpha
            #printD("Fading in image: "+str(path)+", alpha: "+str(alpha))
            time.sleep(alphaStep*fadeTime/maxAlpha)
            img.set_alpha(alpha)
            screen.blit(img,pos)
            pygame.display.flip() #Display all new changes made
    elif fadeTime < 0: # Fade out (This is also fucking terrible)
        alpha = maxAlpha
        while alpha > 0:
            alpha -= alphaStep
            if alpha < 0:
                alpha = 0 
            #printD("Fading out image: "+str(path)+", alpha: "+str(alpha))
            time.sleep(alphaStep*fadeTime/maxAlpha)
            img.set_alpha(alpha)
            screen.blit(img,pos)
            pygame.display.flip() #Display all new changes made
        
    screen.blit(img,pos)

def textDraw(text, font, fontSize, color, pos, align): #This is messy as shit
    #printD("Displaying text: "+str(text)+" with font: "+str(font)+" at pos "+str(pos))
    Font = pygame.font.Font(os.path.join('assets','fonts',font), fontSize)
    renderedText = Font.render(text, False, color)
    if align == "left": # Align the text based on how large the text will be when displayed
        screen.blit(renderedText, pos)
    elif align == "right":
        screen.blit(renderedText, (pos[0]-Font.size(text)[0],pos[1]))
    elif align == "center":
        screen.blit(renderedText, (pos[0]-int(Font.size(text)[0]/2),pos[1]))
    
def pollSerial(cmdQueue): # Probably the most important function in this entire codebase
    while True:
        recieved = ser.readline() 
        recieved = str(recieved)[2:-5]
        printD("Recieved command: "+recieved)
        cmd = recieved.split(" ")
        cmdQueue.put(cmd)

# ------------------------------------------- BEGIN MORAL SUPPORT ------------------------------------------ #
#
#⠀⠀⠀⠀⣴⠾⣯⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠁⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⢻⣄⠈⠻⣤⡀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡏⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⣸⣿⣶⣶⣿⣷⣦⣤⣾⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣧⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⣰⣶⣿⣿⡿⣿⣿⠿⠿⠿⣿⣷⣶⣖⡀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣤⣤⣤⣶⣶⣶⣶⣶⣶⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣄⠀⠀⠀⠀⠀
#⠀⠀⢀⣴⣿⣿⣿⣿⡾⠉⠀⠀⠀⠀⠀⠈⠙⠻⣿⣶⣿⡉⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣤⡴⠶⠶⠟⠛⠉⠉⠉⠉⠁⠀⠁⠀⠀⠐⠑⣿⡟⠀⠀⠀⠀⠀⠀⣠⡴⠚⠉⠁⠀⠀⠀⠀⠀
#⠀⠀⢰⣿⣿⣿⣹⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠻⢿⣿⣦⣠⣤⠀⠀⠀⠀⢀⣤⣴⠿⠛⠋⠙⠀⠀⠀⣀⣀⣤⣤⣤⡴⠶⠟⠛⠛⢻⡦⠀⢀⣿⠃⠀⠀⠀⠀⣠⡾⠋⠀⢀⠀⠀⠀⠀⠀⠀⠀
#⠐⢿⣿⣿⣿⠿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⢿⣿⣦⣄⣤⣴⣿⣋⣀⣀⣤⣤⣤⣞⠛⠛⠋⠉⠁⠀⠀⠀⠀⠀⠀⢀⣾⠋⠀⣸⡇⠀⠀⠀⢀⣰⠟⠀⠀⣴⣿⣧⠀⠀⠀⠀⠀⠀
#⠀⠀⣿⡿⣿⢸⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣿⡾⠛⠉⠉⠀⠈⠀⠀⠉⠉⠉⠛⠛⠒⠶⢤⣤⣀⡀⠀⣸⡏⠀⢠⣿⣤⠔⠚⠉⠁⠉⠀⢀⣾⣿⢻⣿⡄⠀⠀⠀⠀⠀
#⠀⠀⣿⣷⣿⠻⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⠞⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢻⡿⠀⠀⣸⡇⠀⠀⠀⠀⠀⠀⢀⣾⣿⠃⣈⣿⣧⠀⠀⠀⠀⠀
#⠀⠀⣿⣿⣿⡄⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣟⡳⢦⡀⠀⠀⠀⠀⢰⣿⠃⠀⢘⣿⠓⠲⢤⣄⡀⠀⠀⢸⣿⣿⣿⠿⣿⣿⣄⠀⠀⠀⠀
#⠀⣠⣾⣿⣿⣿⡿⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣴⠟⠋⠀⠉⢻⡄⢿⡀⠀⠀⠀⢿⣏⡀⠀⣸⡏⠀⠀⠀⠈⠙⠳⢦⣄⠀⠀⠀⠀⠀⠹⣿⡄⠀⠀⠀
#⠀⠀⠀⠙⣿⣿⣿⣦⣙⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣧⡀⠀⠀⠀⣸⠇⠘⡇⠀⠀⠀⠀⠛⠻⠷⠿⠁⠀⠀⠀⠀⠀⠀⠀⠉⠛⢦⣀⠀⠀⠀⠸⣿⡄⠀⠀
#⠀⠀⠀⠀⠸⠻⣿⣾⣿⣿⣯⣟⣷⢦⣤⣄⡀⠀⠀⠀⣸⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠿⡏⢿⣵⣆⣘⣷⠟⠀⣸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢳⣄⠀⠀⢹⣧⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⣽⠿⠿⢿⣿⣿⣷⣾⣿⣿⣻⣶⣴⡇⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠻⣦⡉⠛⠉⠁⢀⣴⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠨⣳⣄⠈⣿⡇⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠿⡟⠻⢿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⣠⡾⠀⠀⠀⠀⠀⠈⠉⠙⠓⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⢷⡿⣧⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣄⣀⢘⣯⢿⣿⣧⡀⠀⠀⠀⣀⣴⣾⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠃⢿⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡟⢩⣿⡟⢿⣸⡏⠈⠛⠷⠶⠾⣿⣀⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⢸⣿⣷⡈⢻⣷⠀ ⠀⠀⠀⠉⠛⠃⣽⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠋⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣇⠀⣿⡾⢷⡌⢻⣧⠄⢴⣤⣶⡶⢶⣧⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⠶⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡆
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡀⢸⡇⠈⣿⣼⣿⢠⣾⡿⠉⢀⣴⠟⠉⢹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⢿⡇
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠈⢿⡌⣿⡿⣿⡿⠋⠀⣰⠟⠁⠀⢀⣼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡏⠸⡇
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡀⠘⢿⣽⣷⡿⠁⠀⠀⠀⠀⠀⢀⣾⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢺⠁⠰⡇
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢧⠀⠘⢿⣿⡁⠀⠀⣀⣀⣤⠾⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡄⠀⠀⠀⠀⠀⣰⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⡆⢸⠀⢀⡇
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⡀⠀⠈⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡆⠀⠀⠀⣸⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣧⡏⠀⢸⠃
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⡄⠀⢸⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠋⠀⠀⣼⠁
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡿⠃⢀⣼⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⡤⠶⠚⠋⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠘⢹⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣦⠀⠀⠀⠀
# ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡤⠞⠻⢦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⢀⣠⣼⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡟⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⠟⠃⠀⠀⠀⠀⠉⠛⠶⣤⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠘⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⠋⠁⠀⠀⠙⠳⣦⡀⠀⠀⠀⠀⠀⣵⡟⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣀⠀⠀⠀⣀⣀⣤⠴⠛⠋⠀⠀⠈⠉⠙⠛⠛⠓⠒⠒⠒⠒⠚⠻⣆⡀⠀⠀⠀⠀⠀⠀⠀⠈⣷⡄⠀⠀⠀⠀⠈⢻⡆⠀⠀⠀⠰⣿⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣦⠀⠀⠀⠀⠀⠀⠀⠟⣇⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠀⠀⠀⠀⠀⢠⣠⡾⠋⠀⠀⠀⠀⠀⣰⣇⠀⠀⠀⣼⣿⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠁⠀⠀⠀⠀⣠⠟⠁⠀⠀⠀⠀⠀⠀⢰⣿⠟⠀⠀⣼⡿⠋⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠋⠀⠀⠀⠀⣀⡶⠋⠀⠀⠀⠀⠀⠀⠀⠀⠾⣿⣀⣤⠶⠋⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⡏⠀⠀⠀⠀⣤⣾⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⡉⠀⠀⣀⣠⡾⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
# -------------------------------------------- END MORAL SUPPORT ------------------------------------------- #

# -------- LOOPS -------- #

def startScreenLoop(cmdQueue): # menu == 0

    P1Ready = False
    P2Ready = False

    # Set arduinos to ready menu
    resetCmd = "updateMenu P1 ready"
    ser.write(resetCmd.encode("utf-8"))

    def updateStartScreen():
        imageDraw(os.path.join('assets','startMenu.png'), (0,0), (1920,1080), 0) #Display background

        # Draw player 1 & 2  
        textDraw("Player 1", "OpenSans-Bold.ttf", 70, (255,255,255), (200,800), "left")
        textDraw("Player 2", "OpenSans-Bold.ttf", 70, (255,255,255), (1920-200,800), "right")

        if P1Ready: # Ready
            textDraw("Ready!", "OpenSans-Bold.ttf", 50, (0, 255,0), (250,900), "left")
        else:
            textDraw("Ready?", "OpenSans-Bold.ttf", 50, (255,0,0), (250,900), "left")
        if P2Ready:
            textDraw("Ready!", "OpenSans-Bold.ttf", 50, (0,255,0), (1920-250,900), "right")
        else:
            textDraw("Ready?", "OpenSans-Bold.ttf", 50, (255,0,0), (1920-250,900), "right")

        pygame.display.flip() #Display all new changes made

    updateStartScreen()

    while True:
        if not cmdQueue.empty():
            cmd = cmdQueue.get()
            if cmd[0] == 'P1Ready':
                P1Ready = True
                updateStartScreen()
            elif cmd[0] == 'P2Ready':
                P2Ready = True
                updateStartScreen()
            cmd = None

        key = ''
        if keyboard.kbhit(): #Get keyboard input
            key = keyboard.getch()
        if key == "a":
            P1Ready = True
            updateStartScreen()
            print("P1 Ready")
        if key == "s":
            P2Ready = True
            updateStartScreen()
            print("P2 Ready")

        if P1Ready and P2Ready:
            imageDraw(os.path.join('assets','blackBg.png'), (0,0), (1920,1080), 1) #Display background
            return 1

def tutorialLoop(cmdQueue): # menu == 1

    tutorialInd = 0

    P1Ready = False
    P2Ready = False

    # Set arduinos to ready menu
    resetCmd = "updateMenu P1 ready\n"
    ser.write(resetCmd.encode("utf-8"))

    imageDraw(os.path.join('assets','tutorial','tutorial1.png'), (0,0), (1920,1080), 1) #Display background with Fade!!!

    def updateTutorialScreen():
        if tutorialInd == 0:
            imageDraw(os.path.join('assets','tutorial','tutorial1.png'), (0,0), (1920,1080), 0) 
        elif tutorialInd == 1:
            imageDraw(os.path.join('assets','tutorial','tutorial2.png'), (0,0), (1920,1080), 0) 
        elif tutorialInd == 2:
            imageDraw(os.path.join('assets','tutorial','tutorial3.png'), (0,0), (1920,1080), 0) 
        elif tutorialInd == 3:
            imageDraw(os.path.join('assets','tutorial','tutorial4.png'), (0,0), (1920,1080), 0) 
        elif tutorialInd == 4:
            imageDraw(os.path.join('assets','tutorial','tutorial5.png'), (0,0), (1920,1080), 0) 
        elif tutorialInd == 5: # This should be last, add more tutorial screens as needed
            imageDraw(os.path.join('assets','blackBg.png'), (0,0), (1920,1080), 1) #Display background

        if tutorialInd != 5: # So the fade animation doesn't have the skips on top
            if P1Ready: # Ready
                textDraw("Skip!", "OpenSans-Bold.ttf", 50, (0, 255,0), (200,980), "left")
            else:
                textDraw("Skip?", "OpenSans-Bold.ttf", 50, (255,0,0), (200,980), "left")
            if P2Ready:
                textDraw("Skip!", "OpenSans-Bold.ttf", 50, (0,255,0), (1920-200,980), "right")
            else:
                textDraw("Skip?", "OpenSans-Bold.ttf", 50, (255,0,0), (1920-200,980), "right")

        pygame.display.flip() #Display all new changes made

    updateTutorialScreen()

    while True:
        if not cmdQueue.empty():
            cmd = cmdQueue.get()
            if cmd[0] == 'P1Ready':
                P1Ready = True
                updateTutorialScreen()
            elif cmd[0] == 'P2Ready':
                P2Ready = True
                updateTutorialScreen()
            cmd = None

        key = ''
        if keyboard.kbhit(): #Get keyboard input
            key = keyboard.getch()
        if key == "a":
            P1Ready = True
            updateTutorialScreen()
        if key == "s":
            P2Ready = True
            updateTutorialScreen()

        if P1Ready and P2Ready:
            tutorialInd += 1
            P1Ready = False
            P2Ready = False
            updateTutorialScreen()

        if tutorialInd == 5: #Return
            return 2

def inGameLoop(cmdQueue): # menu == 2

    # ITEM SETUP
    itemList = ['01_magGlass.png','02_steal.png','03_double.png','04_skip.png','05_gamble.png','06_spy.png','07_recycle.png']
    itemDescs = [ # list that will contain all the item desc to display (boy is this section gonna be verbose)
        "Magnifying Glass - See the next marble in queue", # 01_magGlass
        "Steal - Steal a point from your opponent, if they have points", # 02_lock
        "Double - Double the effect of the next marble", # 03_double
        "Skip - Bank takes the next marble in queue (No effect)", # 04_skip
        "Gamble - 50% chance to add +1 or -1 to your score",  # 05_gamble
        "Spy satellite - See a random marble in queue", # 06_skip
        "Recycle - Shift the next marble from red->white->blue" # 07_recycle
    ]
    itemPaths = [None]
    for item in itemList:
        itemPaths.append(os.path.join('assets', 'items', item))

    P1ItemGridPos = []
    P2ItemGridPos = []
    for i in range(4):
        for j in range(2):
            P2ItemGridPos.append((95+160*j,98+160*i)) #Initial position and offset generation
    for i in range(4):
        for j in range(2):
            P1ItemGridPos.append((1665+160*j,98+160*i)) #Initial position and offset generation
    #printD("P1 Grid"+str(P1ItemGridPos))
    #printD("P2 Grid"+str(P2ItemGridPos))

    imageDraw(os.path.join('assets','gameBg.png'), (0,0), (1920,1080), 1) # Display background with Fade!!!

    def genMarbles(num):
        marbleQueue = [] 
        random.seed()
        while len(marbleQueue) < num: # roundNum+starting amount of marbles
            marble = random.randint(0,2)
            if marble == 0 and marbleCount("white") <= 4: # 0 is white, 1 is red, and 2 is blue
                marbleQueue.append("white")
            elif marble == 1 and marbleCount("red") <= 4: # 0 is white, 1 is red, and 2 is blue
                marbleQueue.append("red")
            elif marble == 2 and marbleCount("blue") <= 4: # 0 is white, 1 is red, and 2 is blue
                marbleQueue.append("blue")
        printD("Generated marble queue of: "+str(marbleQueue))
        return marbleQueue

    def marbleCount(color):
        count = 0
        nonlocal marbleQueue
        for marble in marbleQueue:
            if marble == color:
                count += 1
        return count

    P1Items = [0,0,0,0,0,0,0,0]
    P2Items = [0,0,0,0,0,0,0,0]

    P1Score = 0
    P2Score = 0

    Effects = []

    marbleQueue = []
    showMarble = False

    def useItem(player, itemPos):
        Buzzer.useItem()
        nonlocal P1Items
        nonlocal P2Items
        itemPos = int(itemPos)
        if player == "P1":
            itemID = P1Items[itemPos]
        elif player == "P2":
            itemID = P2Items[itemPos]
        item = itemList[itemID-1]

        # Item Functions

        def magGlass():
            nonlocal marbleQueue
            marbleID = 0
            if marbleQueue[0] == "white":
                marbleID = 0
            elif marbleQueue[0] == "red":
                marbleID = 1
            elif marbleQueue[0] == "blue":
                marbleID = 2
            magGlassCmd = "showMarble "+player+" 1 "+str(marbleID)
            printD(magGlassCmd)
            printD(marbleQueue)
            ser.write(magGlassCmd.encode("utf-8"))

        def steal():
            nonlocal P1Score
            nonlocal P2Score
            if player == "P1":
                if P2Score == 0:
                    giveItem("P1", 2)
                else:
                    P1Score += 1
                    P2Score -= 1
            elif player == "P2":
                if P1Score == 0:
                    giveItem("P2", 2)
                else:
                    P1Score -= 1
                    P2Score += 1

        def double():
            if not "double" in Effects: # Effects list shows what effects the player has active currently
                Effects.append("double")
            else:
                giveItem("P2", 3)
            printD("Current effect queue: "+str(Effects))

        def skip():
            printD("Giving bank the next marble")
            callDispense(marbleQueue[0], "B") # next marble in queue and player to give to player
            marbleQueue.pop(0)

        def gamble():
            nonlocal P1Score
            nonlocal P2Score
            if random.randint(0,1) == 0:
                scoreAdd = 1
            else:
                scoreAdd = -1

            if player == "P1":
                P1Score += scoreAdd
            elif player == "P2":
                P2Score += scoreAdd

            printD("New P1 score "+str(P1Score))
            printD("New P2 score "+str(P2Score))

        def spySatellite():
            nonlocal marbleQueue
            marblePos = random.randint(0,len(marbleQueue)-1)
            marbleID = 0
            if marbleQueue[marblePos] == "white":
                marbleID = 0
            elif marbleQueue[marblePos] == "red":
                marbleID = 1
            elif marbleQueue[marblePos] == "blue":
                marbleID = 2
            spyCmd = "showMarble "+player+" "+str(marblePos+1)+" "+str(marbleID)
            printD(spyCmd)
            printD(marbleQueue)
            ser.write(spyCmd.encode("utf-8"))

        def recycle():
            nonlocal marbleQueue
            beforeMarble = marbleQueue[0]
            if marbleQueue[0] == "white":
                marbleQueue[0] = "blue"
            elif marbleQueue[0] == "blue":
                marbleQueue[0] = "red"
            elif marbleQueue[0] == "red":
                marbleQueue[0] = "white"
            printD("Shifting marble "+beforeMarble+" to "+marbleQueue[0])

        if item == "01_magGlass.png":
            printD(str(player)+" using magnifying glass")
            magGlass()
        elif item == "02_steal.png":
            printD(str(player)+" using steal")
            steal()
        elif item == "03_double.png":
            printD(str(player)+" using double")
            double()
        elif item == "04_skip.png":
            printD(str(player)+" using skip")
            skip()
        elif item == "05_gamble.png":
            printD(str(player)+" using gamble")
            gamble()
        elif item == "06_spy.png":
            printD(str(player)+" using spy")
            spySatellite()
        elif item == "07_recycle.png":
            printD(str(player)+" using recycle")
            recycle()

        if player == "P1":
            P1Items.pop(itemPos) # Remove item and shift everything
            P1Items.append(0) # Append to make sure it is the same length
        elif player == "P2":
            P2Items.pop(itemPos) # Remove item and shift everything
            P2Items.append(0) # Append to make sure it is the same length

    def giveItem(player, itemId):
        if player == 'P1':
            for ind, currentItem in enumerate(P1Items):
                if ind > len(P1Items)-1:
                    break
                if currentItem == 0:
                    P1Items[ind] = itemId
                    printD('Giving item: '+str(itemList[itemId-1])+' to Player 1, New items list: '+str(P1Items))
                    break
        if player == 'P2':
            for ind, currentItem in enumerate(P2Items):
                if ind > len(P2Items)-1:
                    break
                if currentItem == 0:
                    P2Items[ind] = itemId
                    printD('Giving item: '+str(itemList[itemId-1])+' to Player 2, New items list: '+str(P2Items))
                    break
        #updateGameScreen() # This accidently makes a good animation for recieving items
        sendItems()

    def weightedRandomItem(): # Randomize but with weighted item values (because steal is broken AF)
        # MagGlass, steal, double, skip, gamble, spy, recycle
        weights = [10,2,7,12,10,12,10]
        ranges = []
        total = 0
        for ind,w in enumerate(weights):
            total += w
            wRange = weights[0:ind]
            ranges.append(sum(wRange))
        ranges.append(total)
        
        randNum = random.randint(1,total)
        for ind,r in enumerate(ranges):
            if randNum < r:
                return ind

    def sendItems(): # sendItems("P1", )
        nonlocal P1Items
        nonlocal P2Items
        send = "updateItems P1 "
        for item in P1Items:
            send = send+str(item)

        send = send+"\n"
        ser.write(send.encode("utf-8"))

        time.sleep(0.1)
        send = "updateItems P2 "
        for item in P2Items:
            send = send+str(item)

        send = send+"\n"
        ser.write(send.encode("utf-8"))

    hover = ["0","0"]
    def updateHoverItem(player, ind):
        ind = int(ind)
        frameSize = (150,150)
        if player == "P1":
            imageDraw(os.path.join('assets','hoverFrame.png'), (P1ItemGridPos[ind][0]-frameSize[0]/2,P1ItemGridPos[ind][1]-frameSize[1]/2), frameSize, 0)
            textDraw(itemDescs[P1Items[ind]-1], "OpenSans-Bold.ttf", 50, (255,255,255), (960,950), "center")
        elif player == "P2":
            imageDraw(os.path.join('assets','hoverFrame.png'), (P2ItemGridPos[ind][0]-frameSize[0]/2,P2ItemGridPos[ind][1]-frameSize[1]/2), frameSize, 0)
            textDraw(itemDescs[P2Items[ind]-1], "OpenSans-Bold.ttf", 50, (255,255,255), (960,950), "center")

    def updateDispItems(): # Updates the items on display
        itemSize = (150,150)
        for ind, slotItem in enumerate(P1Items):
            if itemPaths[slotItem] is not None:
                imageDraw(itemPaths[slotItem], (P1ItemGridPos[ind][0]-itemSize[0]/2,P1ItemGridPos[ind][1]-itemSize[1]/2), itemSize, 0)
        for ind, slotItem in enumerate(P2Items):
            if itemPaths[slotItem] is not None:
                imageDraw(itemPaths[slotItem], (P2ItemGridPos[ind][0]-itemSize[0]/2,P2ItemGridPos[ind][1]-itemSize[1]/2), itemSize, 0)

    def updateDispMarbles():
        nonlocal marbleQueue
        nonlocal showMarble
        marbleSize = (92,92)
        #printD("Updating Marble Disp, showMarble: "+str(showMarble))
        for ind, _ in enumerate(marbleQueue):
            if showMarble:
                if marbleQueue[0] == "red":
                    marbPath = "marbleRed.png"
                elif marbleQueue[0] == "blue":
                    marbPath = "marbleBlue.png"
                elif marbleQueue[0] == "white":
                    marbPath = "marbleWhite.png"
                showMarble = False
            else:
                marbPath = "marbleUnknown.png"
            imageDraw(os.path.join('assets',marbPath), (960-marbleSize[0]/2,790-marbleSize[1]/2-(marbleSize[1]+10)*ind), marbleSize, 0) # Disp Marbles 

    def updateGameScreen():
        imageDraw(os.path.join('assets','gameBg.png'), (0,0), (1920,1080), 0) # Display background
        if "double" in Effects and turn == 0:
            imageDraw(os.path.join('assets','items','03_double.png'), (760,680), (100,100), 0)
        if "double" in Effects and turn == 1:
            imageDraw(os.path.join('assets','items','03_double.png'), (1050,680), (100,100), 0)
        updateDispMarbles()
        updateDispItems()
        updateHoverItem(hover[0],hover[1])
        updateScore()

        pygame.display.flip() # Display all new changes made

    def updateScore():
        #printD("P1Score: "+str(P1Score)+", P2Score: "+str(P2Score))
        textDraw(str(P2Score), "OpenSans-Bold.ttf", 150, (255,255,255), (175,840), "center")
        textDraw(str(P1Score), "OpenSans-Bold.ttf", 150, (255,255,255), (1750,840), "center")

    def swapTurn():
        swapCmd = "swapTurns"
        ser.write(swapCmd.encode("utf-8"))
        printD("Swapping turns")

    def dispRoundSplash(): # Show next round and the # of each marble in queue
        nonlocal marbleQueue
        nonlocal turn
        printD("Round num splash screen")
        imageDraw(os.path.join('assets','roundSplashScreen.png'), (0,0), (1920,1080), 0) # Display background
        textDraw("Round "+str(roundNum), "OpenSans-Bold.ttf", 400, (255,255,255), (960,40), "center")
        textDraw("x"+str(marbleCount("blue")), "OpenSans-Bold.ttf", 100, (255,255,255), (540,700), "center")
        textDraw("x"+str(marbleCount("red")), "OpenSans-Bold.ttf", 100, (255,255,255), (1180,700), "center")
        textDraw("x"+str(marbleCount("white")), "OpenSans-Bold.ttf", 100, (255,255,255), (1780,700), "center")

        resetCmd = "updateMenu P1 ready\n"
        ser.write(resetCmd.encode("utf-8"))

        pygame.display.flip() # Display all new changes made
        time.sleep(5)
        if turn == 0:
            initTurnCmd = "updateTurn P1\n"
        elif turn == 1:
            initTurnCmd = "updateTurn P2\n"
        ser.write(initTurnCmd.encode("utf-8"))
    
    def dispCleanUp(P1Ready, P2Ready): # Cleanup between rounds
        imageDraw(os.path.join('assets','blueBg.png'), (0,0), (1920,1080), 0) # Display background
        textDraw("Next round!", "OpenSans-Bold.ttf", 300, (255,255,255), (960,40), "center")
        textDraw("Give all marbles to the bank", "OpenSans-Bold.ttf", 50, (255,255,255), (960,600), "center")

        if P1Ready: # Ready
            textDraw("Ready!", "OpenSans-Bold.ttf", 50, (0, 255,0), (250,900), "left")
        else:
            textDraw("Ready?", "OpenSans-Bold.ttf", 50, (255,0,0), (250,900), "left")
        if P2Ready:
            textDraw("Ready!", "OpenSans-Bold.ttf", 50, (0,255,0), (1920-250,900), "right")
        else:
            textDraw("Ready?", "OpenSans-Bold.ttf", 50, (255,0,0), (1920-250,900), "right")
            
        pygame.display.flip()

    def dispGameEnd():
        printD("Game over")
        if P1Score > P2Score:
            winner = "Player 1 wins!"
        elif P1Score < P2Score:
            winner = "Player 2 wins!"
        else:
            winner = "It's a Tie!"
        imageDraw(os.path.join('assets','blueBg.png'), (0,0), (1920,1080), 0) # Display background
        textDraw("Game Over", "OpenSans-Bold.ttf", 300, (255,255,255), (960,80), "center")
        textDraw(winner, "OpenSans-Bold.ttf", 200, (255,255,255), (960,600), "center")
        pygame.display.flip() # Display all new changes made
        time.sleep(5000)

    # ------- GAME START --------- #

    roundNum = 0
    newRound = True

    turn = random.randint(0,1)

    if turn == 0: # Randomize who goes first
        printD("P1 goes first")
    else: 
        printD("P2 goes first")


    while True:
        # Start of every new round do this
        maxItem = 7 #max-1
        maxRounds = 4

        if len(marbleQueue) == 0:
            if roundNum == maxRounds:
                printD("Game Finished")
                return 0
            else:
                roundNum += 1

                if not roundNum == 1:
                    P1Ready = False
                    P2Ready = False
                    dispCleanUp(P1Ready, P2Ready)

                    resetCmd = "updateMenu P1 ready\n"
                    ser.write(resetCmd.encode("utf-8"))

                    while not (P1Ready and P2Ready):
                        if not cmdQueue.empty():
                            cmd = cmdQueue.get()
                            if cmd[0] == 'P1Ready':
                                P1Ready = True
                                dispCleanUp(P1Ready, P2Ready)
                            elif cmd[0] == 'P2Ready':
                                P2Ready = True
                                dispCleanUp(P1Ready, P2Ready)
                            cmd = None
                    newRound = True

        if newRound: 
            newRound = False
            marbleQueue = genMarbles(roundNum+3) # Roundnum plus whatever initial number of marbles
            dispRoundSplash()

            if roundNum == 1:
                giveNum = 4
            else:
                giveNum = 2 
            for i in range(giveNum):
                giveItem("P1", weightedRandomItem())
                giveItem("P2", weightedRandomItem())
            #P1Items = [1,2,3,4,5,6,7,1]
            #P2Items = [1,2,3,4,5,6,7,1]
            updateGameScreen()
                                    
        # Command ingestion
        if not cmdQueue.empty():
            cmd = cmdQueue.get()
            if cmd[0] == 'useItem':
                useItem(cmd[1], cmd[2]) # player, itemId
                updateGameScreen()
            elif cmd[0] == 'dispense':
                if len(marbleQueue) > 0:
                    if "double" in Effects:
                        multiplier = 2
                    else:
                        multiplier = 1
                    Effects = []
                    if turn == 0: # P1 turns
                        if cmd[1] == "P1": # P1 actually is P2 cause I fucked up
                            if marbleQueue[0] == "blue":
                                P1Score += 1*multiplier
                                if multiplier != 1:
                                    swapTurn()
                                Buzzer.rightGuess()
                            if marbleQueue[0] == "red":
                                P1Score -= 1*multiplier
                                Buzzer.wrongGuess()
                                swapTurn()
                            else:
                                swapTurn()
                        elif cmd[1] == "P2":
                            if marbleQueue[0] == "blue":
                                P2Score += 1*multiplier
                                Buzzer.rightGuess()
                            if marbleQueue[0] == "red":
                                P2Score -= 1*multiplier
                                Buzzer.wrongGuess()
                            swapTurn()
                        elif cmd[1] == "B":
                            if marbleQueue[0] == "white":
                                Buzzer.rightGuess()
                                for i in range(multiplier):
                                    giveItem("P1", weightedRandomItem()) 
                            swapTurn()
                        turn = 1
                    else: # P2 turns
                        if cmd[1] == "P1":
                            if marbleQueue[0] == "blue":
                                P1Score += 1*multiplier
                                Buzzer.rightGuess()
                            if marbleQueue[0] == "red":
                                P1Score -= 1*multiplier
                                Buzzer.wrongGuess()
                            swapTurn()
                        elif cmd[1] == "P2":
                            if marbleQueue[0] == "blue":
                                P2Score += 1*multiplier
                                if multiplier != 1:
                                    swapTurn()
                                Buzzer.rightGuess()
                            if marbleQueue[0] == "red":
                                P2Score -= 1*multiplier
                                Buzzer.wrongGuess()
                                swapTurn()
                            else:
                                swapTurn()
                        elif cmd[1] == "B":
                            if marbleQueue[0] == "white":
                                Buzzer.rightGuess()
                                for i in range(multiplier):
                                    giveItem("P2", weightedRandomItem())
                            swapTurn()
                        turn = 0

                    showMarble = True
                    printD(marbleQueue)
                    updateGameScreen()
                    callDispense(marbleQueue[0], cmd[1]) # next marble in queue and player to give to player
                    marbleQueue.pop(0)
                else:
                    printD("No marbles left in queue!")
            elif cmd[0] == 'hoverItem':
                printD("Hovering over "+str(cmd[1])+" itemPos: "+str(cmd[2]))
                hover = [cmd[1],cmd[2]]
                updateGameScreen()
            elif cmd[0] == 'hoverExit':
                printD("Exiting hover mode")
                hover = ["0","0"]
                updateGameScreen()
            elif cmd[0] == 'updateItemsArd':
                sendItems()
                
            cmd = None

        key = ""
        if keyboard.kbhit(): #Get keyboard input
            key = keyboard.getch()
        if key == "a":
            print("FARTING")

# ------ MAIN LOOP BEGINS ------- #

if __name__ == "__main__":
    import keyboard

    Debug = False

    pygame.init()
    pygame.font.init()

    Buzzer = sound.pBuzzer()

    ser = serial.Serial("/dev/ttyACM0", 9600)
    printD("Waiting for serial connection....")
    time.sleep(3)

    set_start_method('fork')
    
    cmdQueue = SimpleQueue() # This is a godsend how did I not know about this

    serialProc = Process(target=pollSerial, args=(cmdQueue,))
    serialProc.start()

    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN) #Screen size is 1080p 1920x1080
    clock = pygame.time.Clock()

    #Startup the sorting background process
    sortProc = Process(target=startSorter)
    sortProc.start()

    keyboard = keyboard.KBHit()

    #Variables to be used by every menu screen
    menu = 0
    lcdMenu = 0 # Sam's lcd menu value (different from ^)

    while menu != 100:
        if menu == 0:
            menu = startScreenLoop(cmdQueue)
        if menu == 1:
            menu = tutorialLoop(cmdQueue)
        if menu == 2:
            menu = inGameLoop(cmdQueue)

    print("End")
