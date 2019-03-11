import pickle
import time
from pynput.mouse import Button, Controller

data = pickle.load( open( "data.p", "rb" ) )

mouse = Controller()
aa= str(input("Press enter to start"))

n= len(data)
for dd in data:
    dur= dd['dur']
    x, y = dd['pos']
    print("X "+str(x)+" Y "+str(y)+ "delay "+str(dur))
    time.sleep(dur)
    mouse.position = (x, y)
    mouse.click(Button.left)

