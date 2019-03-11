from pynput import mouse
from pynput import keyboard
import time
import pickle


data= []
ptime= time.time()
live= True

def save():
    pickle.dump(data, open("data.p", "wb"))
    print("Files Saved Successfully")
    key_listener.stop() 
    mouse_listener.stop()  
    print("DONE")


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
    global live
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        save()
        live= False
        return False

key_listener = keyboard.Listener(on_release=on_release)
key_listener.start()


mouse_listener= mouse.Listener(on_click= on_click)
mouse_listener.start()

#with mouse.Listener(on_click=on_click) as listener:
#    listener.join()

while(live):
    pass 