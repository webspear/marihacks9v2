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
        ypts[i] = ypts[i-1]+(1/(1+i*stepSize*i*stepSize))
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

fig, ax = plt.subplots()
ax.set_xlabel('t')

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

Line, = ax.plot(x, y, lw=2)

def update(val):
    initEuler(step_slider.val)

    
    global steps
    global stepSize
    global x
    global y
    x = np.arange(0, maximum, stepSize)
    y = np.arange(float(steps))

    for i in range(steps):
        y[i] = ypts[i]-math.atan(i*stepSize)
    global Line
    Line.set_data(x,y)

    global ax
    ax.set_ylim(min(np.min(ypts),np.min(y)), max(np.max(ypts),np.max(y)))
    fig.canvas.draw_idle()
    print("local error: ", ypts[1]-y[1])

step_slider.on_changed(update)

plt.show()