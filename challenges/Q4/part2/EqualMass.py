import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.widgets import Button, Slider
from matplotlib.animation import FuncAnimation

global x
global y
global m
global r
global v

global delta

delta = 1
acc = 1

# G = .000000000066743
G = 1024

x = np.array([[0.],[-8000.],[6000.]])
y = np.array([[-4000.],[0.],[5000.]])
m = np.array([100000,100000,100000])
r = np.array([32,16,16])

v = np.array([[30.,80.],[10.,200.],[-20.,100.]])

running = True

def normalVecTowards(start, end):
    dx=end[0]-start[0]
    dy=end[1]-start[1]
    magnitude = math.sqrt(dx*dx+dy*dy)
    return np.array([dx/magnitude, dy/magnitude])

def EulersMethod():
    global x
    global y
    TEMP = G*m[0]*m[1]/(pow(x[0][-1]-x[1][-1],2) + pow(y[0][-1]-y[1][-1],2))
    
    vec = normalVecTowards([x[0][-1],y[0][-1]],[x[1][-1],y[1][-1]])
    v[0][0] += (TEMP/m[0]*delta)*vec[0]
    v[0][1] += (TEMP/m[0]*delta)*vec[1]
    vec = normalVecTowards([x[1][-1],y[1][-1]],[x[0][-1],y[0][-1]])
    v[1][0] += (TEMP/m[1]*delta)*vec[0]
    v[1][1] += (TEMP/m[1]*delta)*vec[1]
    
    TEMP = G*m[0]*m[2]/(pow(x[0][-1]-x[2][-1],2) + pow(y[0][-1]-y[2][-1],2))
    vec = normalVecTowards([x[0][-1],y[0][-1]],[x[2][-1],y[2][-1]])
    v[0][0] += (TEMP/m[0]*delta)*vec[0]
    v[0][1] += (TEMP/m[0]*delta)*vec[1]
    vec = normalVecTowards([x[2][-1],y[2][-1]],[x[0][-1],y[0][-1]])
    v[2][0] += (TEMP/m[2]*delta)*vec[0]
    v[2][1] += (TEMP/m[2]*delta)*vec[1]
    
    TEMP = G*m[1]*m[2]/(pow(x[1][-1]-x[2][-1],2) + pow(y[1][-1]-y[2][-1],2))
    vec = normalVecTowards([x[1][-1],y[1][-1]],[x[2][-1],y[2][-1]])
    v[1][0] += (TEMP/m[1]*delta)*vec[0]
    v[1][1] += (TEMP/m[1]*delta)*vec[1]
    vec = normalVecTowards([x[2][-1],y[2][-1]],[x[1][-1],y[1][-1]])
    v[2][0] += (TEMP/m[2]*delta)*vec[0]
    v[2][1] += (TEMP/m[2]*delta)*vec[1]

    x = [np.append(x[0],[x[0][-1]+v[0][0]*acc]), np.append(x[1],x[1][-1]+v[1][0]*acc), np.append(x[2],x[2][-1]+v[2][0]*acc)]
    
    
    y = [np.append(y[0],y[0][-1]+v[0][1]*acc), np.append(y[1],y[1][-1]+v[1][1]*acc), np.append(y[2],y[2][-1]+v[2][1]*acc)]

EulersMethod()


def init():
    ax.set_xlim(x[0][0]-20000, x[0][0]+20000)
    ax.set_ylim(y[0][0]-20000, y[0][0]+20000)

    return plot0,
    

global ax
fig, ax = plt.subplots()
global plot0
global plot1
global plot2
plot0, = ax.plot(x[0], y[0])
plot1, = ax.plot(x[1], y[1])
plot2, = ax.plot(x[2], y[2])
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title("3-body problem | Equal Mass")
ax.legend(['Planet 1', 'Planet 2', 'Planet 3'])

axX0 = fig.add_axes([0.1, 0.2, .07, 0.03])
x0 = Slider(
    ax=axX0,
    label='X0',
    valmin=-15000,
    valmax=15000,
    valinit=x[0][0],
)
axX1 = fig.add_axes([0.4, 0.2, .07, 0.03])
x1 = Slider(
    ax=axX1,
    label='X1',
    valmin=-15000,
    valmax=15000,
    valinit=x[1][0],
)
axX2 = fig.add_axes([0.7, 0.2, .07, 0.03])
x2 = Slider(
    ax=axX2,
    label='X2',
    valmin=-15000,
    valmax=15000,
    valinit=x[2][0],
)

axY0 = fig.add_axes([0.25, 0.2, .07, 0.03])
y0 = Slider(
    ax=axY0,
    label='Y0',
    valmin=-15000,
    valmax=15000,
    valinit=y[0][0],
)
axY1 = fig.add_axes([0.55, 0.2, .07, 0.03])
y1 = Slider(
    ax=axY1,
    label='Y1',
    valmin=-15000,
    valmax=15000,
    valinit=y[1][0],
)
axY2 = fig.add_axes([0.85, 0.2, .07, 0.03])
y2 = Slider(
    ax=axY2,
    label='Y2',
    valmin=-15000,
    valmax=15000,
    valinit=y[2][0],
)


axXV0 = fig.add_axes([0.1, 0.17, .07, 0.03])
Vx0 = Slider(
    ax=axXV0,
    label='Vy0',
    valmin=-256,
    valmax=256,
    valinit=v[0][0],
)
axXV1 = fig.add_axes([0.4, 0.17, .07, 0.03])
Vx1 = Slider(
    ax=axXV1,
    label='Vy1',
    valmin=-256,
    valmax=256,
    valinit=v[1][0],
)
axXV2 = fig.add_axes([0.7, 0.17, .07, 0.03])
Vx2 = Slider(
    ax=axXV2,
    label='Vy2',
    valmin=-256,
    valmax=256,
    valinit=v[2][0],
)

axYV0 = fig.add_axes([0.25, 0.17, .07, 0.03])
Vy0 = Slider(
    ax=axYV0,
    label='Vy0',
    valmin=-256,
    valmax=256,
    valinit=v[0][1],
)
axYV1 = fig.add_axes([0.55, 0.17, .07, 0.03])
Vy1 = Slider(
    ax=axYV1,
    label='Vy1',
    valmin=-256,
    valmax=256,
    valinit=v[1][1],
)
axYV2 = fig.add_axes([0.85, 0.17, .07, 0.03])
Vy2 = Slider(
    ax=axYV2,
    label='Vy2',
    valmin=-256,
    valmax=256,
    valinit=v[2][1],
)


axM0 = fig.add_axes([0.17, 0.14, .07, 0.03])
M0 = Slider(
    ax=axM0,
    label='M0',
    valmin=10000,
    valmax=1000000,
    valinit=m[0],
)
axM1 = fig.add_axes([0.47, 0.14, .07, 0.03])
M1 = Slider(
    ax=axM1,
    label='M1',
    valmin=10000,
    valmax=1000000,
    valinit=m[1],
)
axM2 = fig.add_axes([0.77, 0.14, .07, 0.03])
M2 = Slider(
    ax=axM2,
    label='M2',
    valmin=10000,
    valmax=1000000,
    valinit=m[2],
)


axG = fig.add_axes([0.47, 0.11, .07, 0.03])
GS = Slider(
    ax=axG,
    label='G',
    valmin=0,
    valmax=1024,
    valinit=G,
)
axDT = fig.add_axes([0.47, 0.08, .07, 0.03])
DT = Slider(
    ax=axDT,
    label='delta Time',
    valmin=0,
    valmax=1024,
    valinit=delta,
)

fig.subplots_adjust(bottom=0.35)


def update(i):
    if not running: return
    for i in range(16):
        global x
        global y
        EulersMethod()
        plot0.set_data(x[0],y[0])
        plot1.set_data(x[1],y[1])
        plot2.set_data(x[2],y[2])


        ax.set_xlim(x[0][-1]-20000, x[0][-1]+20000)
        ax.set_ylim(y[0][-1]-20000, y[0][-1]+20000)
        return plot0,
    


def updateVal(val):
    global x
    global y
    global m
    global v

    global delta
    global running
    running = False
    delta = DT.val

    # G = .000000000066743
    G = GS.val

    x = np.array([[x0.val],[x1.val],[x2.val]])
    y = np.array([[y0.val],[y1.val],[y2.val]])
    m = np.array([M0.val,M1.val,M2.val])

    v = np.array([[Vx0.val,Vy0.val],[Vx1.val,Vy1.val],[Vx2.val,Vy2.val]])
    
    fig.canvas.draw_idle()

x0.on_changed(updateVal)
x1.on_changed(updateVal)
x2.on_changed(updateVal)
y0.on_changed(updateVal)
y1.on_changed(updateVal)
y2.on_changed(updateVal)

Vx0.on_changed(updateVal)
Vx1.on_changed(updateVal)
Vx2.on_changed(updateVal)
Vy0.on_changed(updateVal)
Vy1.on_changed(updateVal)
Vy2.on_changed(updateVal)

M0.on_changed(updateVal)
M1.on_changed(updateVal)
M2.on_changed(updateVal)

GS.on_changed(updateVal)
DT.on_changed(updateVal)

# Play Button
playax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(playax, 'Play', hovercolor='0.975')


def play(event):
    global x
    global y
    global m
    global v

    global delta
    global running
    running = True
    delta = DT.val

    # G = .000000000066743
    G = GS.val

    x = np.array([[x0.val],[x1.val],[x2.val]])
    y = np.array([[y0.val],[y1.val],[y2.val]])
    m = np.array([M0.val,M1.val,M2.val])

    v = np.array([[Vx0.val,Vy0.val],[Vx1.val,Vy1.val],[Vx2.val,Vy2.val]])
button.on_clicked(play)


ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128), init_func=init, blit=False)

plt.show()
