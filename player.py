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

def on_release(key):
    global ptime
    print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        return False
    if(key== keyboard.Key.home):
        stopPlay()
        return False 
    dur= time.time()- ptime
    data.append({'type':'keyrelease', 'dur': dur, 'key': key})
    print("Key "+str(key)+" with "+str(dur))
    ptime= time.time()
    return live 


def stopPlay():
    global live 
    print("Stopping play")
    live= False 


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

def playRec():
    statusTv['text']= "Playing"
    statusTv['fg']= 'green'
    root.update()
    data = pickle.load( open( "data.p", "rb" ) )
    mouse = Controller()
    keyc= KeyController()
    play(data, mouse, keyc) 
    statusTv['text']= "Played Successfully"


def playInLoop(): 
    global live, key_listener
    live= True
    key_listener = keyboard.Listener(on_release=on_release)
    key_listener.start()
    statusTv['text']= "Press HOME to Stop"
    statusTv['fg']= 'red'
    data = pickle.load( open( "data.p", "rb" ) )
    mouse = Controller()
    keyc= KeyController()
    while(live):
        play(data, mouse, keyc)
    statusTv['text']= "Stopped Successfully"
    statusTv['fg']= "green"


def on_slider(value):
    global speedx
    speedx= value
    statusTv['text']= "Speed: {}x".format(speedx)
    statusTv['fg']= "green"



def just_play(nn):
    nameE.delete(0,END)
    nameE.insert(0,nn)
    #playRec()


#####################################################################################
statusTv= tk.Label(root, text= "READY", fg= 'green', font = "Verdana 12 bold")
statusTv.pack()
nameE= tk.Entry(root)
nameE.pack()

slider= tk.Scale(root, from_= 1, to= 25, command= on_slider, orient= 'horizontal', label= "Speed", length= 200)
slider.pack()



import glob 
import os
from tkinter import END



playB= tk.Button(root, text= "Play", width= 25, command= playRec)
playB.pack() 
pilB= tk.Button(root, text= "Play in Loop", width= 25, command= playInLoop)
pilB.pack() 
pilsB= tk.Button(root, text= "Stop Playing", width= 25, command= stopPlay)
pilsB.pack() 
exitB= tk.Button(root, text= "Close", width= 25, command= root.destroy)
exitB.pack() 

statusTv= tk.Label(root, text= "Recordings", fg= 'gray', font = "Verdana 10")
statusTv.pack()

for ff in glob.glob("recordings/*.p"):
    nn= os.path.basename(ff)
    nn= nn[: nn.find("_")]
    playB= tk.Button(root, text= str(nn), width= 25, command= lambda nn=nn: just_play(nn))
    playB.pack() 



#root.attributes('-topmost', True)
#root.update()

root.mainloop()  