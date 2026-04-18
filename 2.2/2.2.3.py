import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.widgets import Slider

yintercept = 0
maximum = 16
steps = int(8)
stepSize = float(maximum)/float(steps)

xpts = np.linspace(0, maximum, num=steps, endpoint=False)

ypts = np.arange(float(yintercept), yintercept + steps)

def EulersMethod():
    global steps
    global xpts
    global ypts
    for i in range(1, steps):
        ypts[i] = ypts[i-1]+ypts[i-1]-(i*stepSize*i*stepSize)+1
EulersMethod()


def initEuler(val):
    global steps
    global stepSize
    global xpts
    global ypts
    steps = math.floor(val)
    stepSize = float(maximum)/float(steps)
    xpts = np.linspace(0, maximum, num=steps, endpoint=False)
    ypts = np.arange(float(yintercept), yintercept + steps)
    EulersMethod()

fig, ax = plt.subplots(2,2, sharey=False)
eulerLine, = ax[0][1].plot(xpts, ypts, lw=2)
eulerLine2, = ax[1][0].plot(xpts, ypts, lw=2)
ax[0][0].set_xlabel('t')
ax[0][0].set_ylabel('x')
ax[1][1].set_xlabel('t')
ax[1][1].set_ylabel('x')
ax[0][0].set_xlabel('t')
ax[0][0].set_ylabel('x')
ax[1][0].set_xlabel('t')
ax[1][0].set_ylabel('x')
ax[0][0].set_title("Accurate Function")
ax[1][0].set_title("Euler's Method's")
ax[0][1].set_title("Accurate Function vs Euler's Method")
ax[1][1].set_title("Euler's Method's Error")

axStep = fig.add_axes([0.25, 0.1, 0.65, 0.03])
step_slider = Slider(
    ax=axStep,
    label='Steps',
    valmin=0,
    valmax=128,
    valinit=steps,
)

fig.subplots_adjust(bottom=0.25)



x = np.arange(0, maximum, stepSize)
y = np.arange(float(steps))

for i in range(steps):
    y[i] = math.atan(i*stepSize)

Line, = ax[0][1].plot(x, y, lw=2)
Line.set_color("orange")
AccurateLine, = ax[0][0].plot(x, y, lw=2)
AccurateLine.set_color("orange")
ax[0][1].legend(["Euler's Method", 'Accurate Function'])


x2 = np.arange(0, maximum, stepSize)
y2 = np.arange(float(steps))
global Line2
Line2, = ax[1][1].plot(x2, y2, lw=2)

def update(val):
    global ypts
    initEuler(step_slider.val)
    global eulerLine
    global eulerLine2
    eulerLine.set_data(xpts,ypts)
    eulerLine2.set_data(xpts,ypts)

    
    global steps
    global stepSize
    global x
    global y
    x = np.arange(0, maximum, stepSize)
    y = np.arange(float(steps))

    for i in range(steps):
        t=i*stepSize
        y[i] = pow(t+1, 2)-0.5*pow(math.e, t)
    Line.set_data(x,y)
    AccurateLine.set_data(x,y)


    x2 = np.arange(0, maximum, stepSize)
    y2 = np.arange(float(steps))

    for i in range(steps):
        y2[i] = ypts[i]-y[i]

    Line2.set_data(x2,y2)

    global ax
    ax[0][1].set_ylim(min(np.min(ypts),np.min(y)), max(np.max(ypts),np.max(y)))
    ax[1][1].set_ylim(np.min(y2), np.max(y2))
    ax[1][0].set_ylim(np.min(ypts), np.max(ypts))
    ax[0][0].set_ylim(np.min(y), np.max(y))
    fig.canvas.draw_idle()

step_slider.on_changed(update)

plt.show()