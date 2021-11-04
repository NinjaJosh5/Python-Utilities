from math import sqrt
import matplotlib.pyplot as plt
import termplotlib as tpl
from tkinter import *
from threading import Thread
import time
import random
import concurrent.futures
import sys, signal

def calculate_restitution(**kwargs):
    h0 = kwargs.get('h0', 10)         # m/s
    v = 0          # m/s, current velocity
    g = 9.81         # m/s/s
    t = 0          # starting time
    dt = 0.01     # time step
    rho = kwargs.get('rho', 0.8)     # coefficient of restitution
    tau = 0.95     # contact time for bounce (squish time), time delta while kinetic energy is converted into potential and back
    hmax = h0      # keep track of the maximum height
    h = h0
    hstop = 0.01   # stop when bounce is less than 1 cm
    freefall = True # state: freefall or in contact
    t_last = -sqrt(2*h0/g) # time we would have launched to get to h0 at t=0
    vmax = sqrt(2 * hmax * g)
    H = []
    T = []
    V = []
    while(hmax > hstop):
        if(freefall):
            hnew = h + v*dt - 0.5*g*dt*dt
            if(hnew<0):
                t = t_last + 2*sqrt(2*hmax/g)
                freefall = False
                t_last = t + tau
                h = 0
            else:
                t = t + dt
                v = v - g*dt
                h = hnew
        else:
            t = t + tau
            vmax = vmax * rho
            v = vmax
            freefall = True
            h = 0
        hmax = 0.5*vmax*vmax/g
        H.append(h)
        T.append(t)
        V.append(v)
    print("stopped bouncing at t=%.3f\n"%(t))
    return T, H, V, t

def plot():
    T, H, V, t = calculate_restitution()
    plt.figure()
    plt.plot(T, H, T, V)
    plt.xlabel('time')
    plt.ylabel('height & velocity')
    plt.title('bouncing ball')
    plt.show()

class Ball():
    def __init__(self, **kwargs):
        self.canvas = kwargs["canvas"]
        self.canvas_padding = int(kwargs["canvas_padding"])
        self.gui = kwargs["gui"]
        self.master = self.gui
        color = kwargs.get('color', "red")
        height_minus_padding = int(self.canvas["height"]) - (2 * self.canvas_padding)
        width_minus_padding = int(self.canvas["width"]) - (2 * self.canvas_padding)
        startx = random.randint((self.canvas_padding * 2), width_minus_padding)
        starty = random.randint((self.canvas_padding * 2), height_minus_padding)
        self.ball = canvas.create_oval(395,90,405,100, fill=color)


    def animate(self):
        T, H, V, t = calculate_restitution(h0=400)
        factor = 1
        x_last = H[0]
        time.sleep(.5)
        for count, x in enumerate(H):
            if(x > x_last):
                var = (x - x_last) * factor
                self.canvas.move(self.ball, 0, -var)
                #print("+" + str(var))
            else:
                var = (x_last - x) * factor
                self.canvas.move(self.ball, 0, +var)
                #print("-" + str(var))
            #pos = self.canvas.coords(self.ball)
            #print(str(pos[1]) + "\n")
            x_last = x
            self.gui.update()
            time.sleep(.001)
    
        
if __name__ == "__main__":
    gui = Tk()
    gui.geometry("800x800")
    gui.title("Animation")
    padding = 5
    width = 800
    height = 800
    canvas = Canvas(gui, width=width,height=height, bg="black")
    #                               x1,y1,x2,y2
    # outer border
    line1 = canvas.create_rectangle(padding, padding, (height-padding), (width-padding), fill="red")
    # inner border
    line2 = canvas.create_rectangle(padding*2, padding*2, height-(2*padding), height-(2*padding), fill="black")
    # generate balls - using thread pattern, but threading is not necessecary
    thread_list = []
    thread_list.append(Thread(target=Ball(gui=gui, canvas=canvas, canvas_padding=5, size=15, xspeed=1, yspeed=1).animate))

    thread_list.reverse()
    canvas.pack()

    # start threads
    print(len(thread_list))
    for th in thread_list:
        time.sleep(0.1)
        th.start()
        time.sleep(0.1)


    gui.mainloop()
