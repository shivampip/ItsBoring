import tkinter as tk
from pynput import mouse
from pynput import keyboard
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller as KeyController
import time
import pickle

root= tk.Tk()
root.title("Just Automate")
#####################################################################################

data= []
ptime= time.time()
live= True
speedx = 1
key_listener= None
mouse_listener= None


def on_click(x, y, button, pressed):
    global ptime
    #if(pressed):
    #    return 
    pos= [x,y]
    dur= time.time()- ptime
    data.append({'type': 'mouse', "dur":dur, "pos":pos, "btn": button, "pressed":pressed})
    print(str(x)+" , "+str(y)+ " with "+str(dur))
    ptime= time.time()
    return live
     
def on_scroll(x, y, dx, dy):
    global ptime 
    pos= [x,y]
    dur= time.time()- ptime
    amount= [dx, dy]
    data.append({'type':'scroll', 'dur': dur, 'pos': pos, 'amount': amount})
    print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up',(x, y)))
    return live 

def on_press(key):
    global ptime
    print("{} pressed".format(key))
    if key == keyboard.Key.esc:
        stopRec(last= False)
        return False
    if(key== keyboard.Key.home and not is_rec):
        stopPlay()
        return False 
    dur= time.time()- ptime
    data.append({'type':'keypress', 'dur': dur, 'key': key})
    print("Key "+str(key)+" with "+str(dur))
    ptime= time.time()
    return live 

def on_release(key):
    global ptime
    print('{0} released'.format(key))
    if key == keyboard.Key.esc:
        stopRec(last= False)
        return False
    if(key== keyboard.Key.home and not is_rec):
        stopPlay()
        return False 
    dur= time.time()- ptime
    data.append({'type':'keyrelease', 'dur': dur, 'key': key})
    print("Key "+str(key)+" with "+str(dur))
    ptime= time.time()
    return live 

def save():
    pickle.dump(data, open("data.p", "wb"))
    statusTv['text']= "Recording Saved Successfully"
    statusTv['fg']= 'green'

is_rec= False

def startRec():
    global key_listener, mouse_listener, ptime, is_rec
    key_listener = keyboard.Listener(on_press= on_press, on_release=on_release)
    key_listener.start()
    #mouse_listener= mouse.Listener(on_click= on_click, on_scroll= on_scroll)
    mouse_listener= mouse.Listener(on_click= on_click)
    mouse_listener.start()
    print("Recording Started")
    is_rec= True 
    ptime= time.time() 
    statusTv['text']= "Press ESC to Stop"
    statusTv['fg']= "red"

def stopRec(last= True):
    global is_rec
    if(last):
        del data[-1]
    save()
    key_listener.stop() 
    mouse_listener.stop()  
    is_rec= False 
    statusTv['text']= "Recording Stopped"
    statusTv['fg']= "green"

#####################################################################################

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




#####################################################################################
statusTv= tk.Label(root, text= "READY", fg= 'green', font = "Verdana 12 bold")
statusTv.pack()
startB= tk.Button(root, text= "Start Recording", width= 25, command= startRec)
startB.pack() 
stopB= tk.Button(root, text= "Stop Recording", width= 25, command= stopRec)
stopB.pack() 

slider= tk.Scale(root, from_= 1, to= 25, command= on_slider, orient= 'horizontal', label= "Speed", length= 200)
slider.pack()

playB= tk.Button(root, text= "Play", width= 25, command= playRec)
playB.pack() 
pilB= tk.Button(root, text= "Play in Loop", width= 25, command= playInLoop)
pilB.pack() 
pilsB= tk.Button(root, text= "Stop Playing", width= 25, command= stopPlay)
pilsB.pack() 
exitB= tk.Button(root, text= "Close", width= 25, command= root.destroy)
exitB.pack() 

#root.attributes('-topmost', True)
#root.update()

root.mainloop()  