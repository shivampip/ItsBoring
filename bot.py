import tkinter as tk
from pynput import mouse
from pynput import keyboard
from pynput.mouse import Button, Controller
import time
import pickle

root= tk.Tk()
root.title("Let me do it")
#####################################################################################

data= []
ptime= time.time()
live= True
key_listener= None
mouse_listener= None


def on_click(x, y, button, pressed):
    global ptime
    if(pressed):
        return 
    pos= [x,y]
    dur= time.time()- ptime
    data.append({"dur":dur, "pos":pos})
    print(str(x)+" , "+str(y)+ " with "+str(dur))
    ptime= time.time()
    return live

def on_release(key):
    print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        stopRec(last= False)
        return False
    if(key== keyboard.Key.space):
        stopPlay()
        return False 

def save():
    pickle.dump(data, open("data.p", "wb"))
    statusTv['text']= "Recording Saved Successfully"
    statusTv['fg']= 'green'



def startRec():
    global key_listener, mouse_listener, ptime
    key_listener = keyboard.Listener(on_release=on_release)
    key_listener.start()
    mouse_listener= mouse.Listener(on_click= on_click)
    mouse_listener.start()
    print("Recording Started")
    ptime= time.time() 
    statusTv['text']= "Press ESC to Stop"
    statusTv['fg']= "red"


def stopRec(last= True):
    if(last):
        del data[-1]
    save()
    key_listener.stop() 
    mouse_listener.stop()  
    statusTv['text']= "Recording Stopped"
    statusTv['fg']= "green"

#####################################################################################

def stopPlay():
    global live 
    print("Stopping play")
    live= False 

    
def playRec():
    statusTv['text']= "Playing"
    statusTv['fg']= 'green'
    root.update()
    data = pickle.load( open( "data.p", "rb" ) )
    mouse = Controller()
    for dd in data:
        dur= dd['dur']
        x, y = dd['pos']
        print("X "+str(x)+" Y "+str(y)+ "delay "+str(dur))
        time.sleep(dur)
        mouse.position = (x, y)
        mouse.click(Button.left)
    statusTv['text']= "Played Successfully"


def playInLoop():
    global live, key_listener
    live= True
    key_listener = keyboard.Listener(on_release=on_release)
    key_listener.start()
    statusTv['text']= "Press SPACE to Stop"
    statusTv['fg']= 'red'
    while(live):
        data = pickle.load( open( "data.p", "rb" ) )
        mouse = Controller()
        for dd in data:
            if(not live):
                break 
            dur= dd['dur']
            x, y = dd['pos']
            print("X "+str(x)+" Y "+str(y)+ "delay "+str(dur))
            time.sleep(dur)
            mouse.position = (x, y)
            mouse.click(Button.left)
    statusTv['text']= "Stopped Successfully"
    statusTv['fg']= "green"





#####################################################################################
statusTv= tk.Label(root, text= "READY", fg= 'green', font = "Verdana 12 bold")
statusTv.pack()
startB= tk.Button(root, text= "Start Recording", width= 25, command= startRec)
startB.pack() 
stopB= tk.Button(root, text= "Stop Recording", width= 25, command= stopRec)
stopB.pack() 
playB= tk.Button(root, text= "Play", width= 25, command= playRec)
playB.pack() 
pilB= tk.Button(root, text= "Play in Loop", width= 25, command= playInLoop)
pilB.pack() 
pilsB= tk.Button(root, text= "Stop Playing", width= 25, command= stopPlay)
pilsB.pack() 
exitB= tk.Button(root, text= "Close", width= 25, command= root.destroy)
exitB.pack() 

root.attributes('-topmost', True)
root.update()
root.mainloop()  