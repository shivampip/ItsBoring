import tkinter as tk
from pynput import mouse
from pynput import keyboard
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller as KeyController
import time
import pickle

root= tk.Tk()
root.title("Testing")
#####################################################################################

data= []
ptime= time.time()
live= True
speedx = 1




#############################################################

import pyautogui
from pyscreeze import ImageNotFoundException

#####################################################################################

def stopPlay():
    global live 
    print("Stopping play")
    live= False 


def verifyOutput():
    statusTv['text']= 'Trying to verify output'
    name= nameE.get()
    
    print("Testing")
    fname= "imgs/{}_0_out.png".format(name)
    try:
        print("Trying to locate {}".format(fname))
        loc = pyautogui.locateOnScreen(fname, confidence= 0.65)
        print("Image Found: {}".format(loc))
        if(loc is not None):
            statusTv['fg']= 'green'
            statusTv['text']= "Test Success"
            print("TEST SUCCESS")
        else:
            statusTv['fg']= 'red'
            statusTv['text']= "Test Failed"
            print("TEST FAILED")
    except ImageNotFoundException:
        print("Image not found")
        statusTv['fg']= 'red'
        statusTv['text']= "Test Failed"
        print("TEST FAILED")

    print("Done")





def play(data, mouse, keyc):
    global live 
    for dd in data:
        type= dd['type']
        dur= dd['dur']/ float(speedx)
        time.sleep(dur)
        if(not live):
            break 
        if(type=='mouse'):
            x, y = dd['pos']
            btn= dd['btn']
            pressed= dd['pressed']
            print("X "+str(x)+" Y "+str(y)+ "delay "+str(dur))
            mouse.position = (x, y)
            if(pressed):
                mouse.press(btn)
            else:
                mouse.release(btn)
            #mouse.click(btn)
        if(type=='keypress'):
            key= dd['key']
            print("Keypress "+str(key))
            keyc.press(key)
        if(type=='keyrelease'):
            key= dd['key']
            print("Keyrelease "+str(key))
            keyc.release(key)
  
        #if(type=='scroll'):
        #    x, y= dd['pos']
        #    dx, dy = dd['amount']
        #    mouse.scroll(dx, dy)
    
    # Input Played
    # Now verify output
    verifyOutput()

def playRec():
    statusTv['text']= "Playing"
    statusTv['fg']= 'green'
    root.update()

    name= nameE.get()
    fname= "data/{}_0_input.p".format(name)

    data = pickle.load( open( fname, "rb" ) )
    mouse = Controller()
    keyc= KeyController()
    play(data, mouse, keyc) 




def on_slider(value):
    global speedx
    speedx= value
    statusTv['text']= "Speed: {}x".format(speedx)
    statusTv['fg']= "green"


def just_play(nn):
    nameE.delete(0,END)
    nameE.insert(0,nn)
    playRec()


#####################################################################################
statusTv= tk.Label(root, text= "READY", fg= 'green', font = "Verdana 12 bold")
statusTv.pack()
nameE= tk.Entry(root)
nameE.pack()

slider= tk.Scale(root, from_= 1, to= 25, command= on_slider, orient= 'horizontal', label= "Speed", length= 200)
slider.pack()

playB= tk.Button(root, text= "Test", width= 25, command= playRec)
playB.pack() 


import glob 
import os
from tkinter import END

for ff in glob.glob("data/*.p"):
    nn= os.path.basename(ff)
    nn= nn[: nn.find("_")]
    playB= tk.Button(root, text= str(nn), width= 25, command= lambda: just_play(nn))
    playB.pack() 


pilsB= tk.Button(root, text= "Stop Testing", width= 25, command= stopPlay)
pilsB.pack() 
exitB= tk.Button(root, text= "Close", width= 25, command= root.destroy)
exitB.pack() 

#root.attributes('-topmost', True)
#root.update()

root.mainloop()  