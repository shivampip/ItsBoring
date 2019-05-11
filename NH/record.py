import tkinter as tk
from pynput import mouse
from pynput import keyboard
from pynput.mouse import Button, Controller
from pynput.keyboard import Key, Controller as KeyController
import time
import pickle

root= tk.Tk()
root.title("Recorder")
#####################################################################################

data= []
ptime= time.time()
live= True
speedx = 1
key_listener= None
mouse_listener= None
counter= 0

ywait= "none"
out_cap= {}


#############################################################

import pyautogui
import pyautogui


def capture_area(data, name):
    reg= (data['left'], data['top'], data['width'], data['height'])
    ss= pyautogui.screenshot(region= reg)
    ss.save(name)
    statusTv['Output Saved']
    return name 

def capture():
    fname= nameE.get()
    screenWidth, screenHeight = pyautogui.size()
    x, y = pyautogui.position()
    width, height = (100, 60)
    sx, sy= width/2, height/2
    
    left= x- sx 
    if(left<0):
        left= 0
    top= y- sy 
    if(top<0):
        top= 0

    if(x+sx>screenWidth):
        width= x+sx- screenWidth

    if(y+sy>screenHeight):
        height= y+ sy- screenHeight

    reg= ( left, top, width, height)
    ss= pyautogui.screenshot(region= reg)

    name= "imgs/{}__{}_{}.png".format(fname, x, y)
    ss.save(name)
    return name 


#############################################################





def on_click(x, y, button, pressed):
    print("PRessed is {}".format(pressed))
    global ywait, out_cap, counter
    if(ywait=='out_br' and pressed):
        out_cap['width']= x - out_cap['left']
        out_cap['height']= y - out_cap['top']
        statusTv['text']= "Done"
        ywait= 'none'
        capture_area(out_cap, "imgs/{}_{}_out.png".format(nameE.get(), counter))
        counter+= 1
        return live

    if(ywait=='out_tl' and pressed):
        out_cap['left']= x
        out_cap['top']= y 
        statusTv['text']= "Select Bottom Right"
        ywait= 'out_br'
        return live 



    #ss= capture()
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
        return False 
    dur= time.time()- ptime
    data.append({'type':'keyrelease', 'dur': dur, 'key': key})
    print("Key "+str(key)+" with "+str(dur))
    ptime= time.time()
    return live 

def save():
    fname= nameE.get()
    name= "data/{}_{}_input.p".format(fname, counter)
    pickle.dump(data, open(name, "wb"))
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



def captureOutput():
    global mouse_listener, ywait
    statusTv['text']= "Select Top-Left"
    ywait= "out_tl"
    mouse_listener= mouse.Listener(on_click= on_click)
    mouse_listener.start()






#####################################################################################
statusTv= tk.Label(root, text= "READY", fg= 'green', font = "Verdana 12 bold")
statusTv.pack()
nameE= tk.Entry(root)
nameE.pack()
startB= tk.Button(root, text= "Start Recording", width= 25, command= startRec)
startB.pack() 
stopB= tk.Button(root, text= "Stop Recording", width= 25, command= stopRec)
stopB.pack() 

playB= tk.Button(root, text= "Record Input", width= 25, command= startRec)
playB.pack() 

playB= tk.Button(root, text= "Capture Output", width= 25, command= captureOutput)
playB.pack() 



exitB= tk.Button(root, text= "Close", width= 25, command= root.destroy)
exitB.pack() 

#root.attributes('-topmost', True)
#root.update()

root.mainloop()  