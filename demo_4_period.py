

import matplotlib.pyplot as plt
import numpy as np
import cmath
import math
import sys




#Linkage notation
#      . 
#     / \  
#    b    \
#   / thb   \ thc
#  .----      c----
#   \           \
#    a            \
#     \  tha        \ thd
#      .______d_______.----
#for demo , T should = 6s

T = float(input("please type in Time period: "))
while True:
    pen_pos = input('please type in pen type (coupler/center): ')
    if pen_pos == 'coupler' or pen_pos == 'center':
        break
T_animation = T*1000*(0.01/2)*0.81 #2*pi/0.01pi = T/T_animation(unit 1000 ms = 1s)

a,b,c,d = 100,250,300,200
assert(b + c >= d + a)


#Change follower parameters
#Degrees
Angle = 40
Angle_cg = Angle- 20

#Relative magnitude, NOT ABSOLUTE LENGTH
Len = 1
Len_cg = 0.7

ROTATION = ''
MODE = 'negative'

#Lengths of the linkages, 
#a,b,c,d represent linkages starting from left fixed and going clockwise
#makes sure that the grashoff condition is satisfied
#Since linkage a is the driving linkage, b+c must be greater than a+d



#the angle that the linkages make wrt xaxis of the fixed points a,d
#step controls how fast the linkage drives

step = 0.01
runtime = 6
if ROTATION == 'cw':
    th_a = np.arange(runtime*np.pi,0,-step*np.pi)
else:
    th_a = np.arange(0,runtime*np.pi,step*np.pi)

#Degrees, used for drawing arcs
th_a_d = th_a * 180/np.pi

#Freudenstein equation

K1 = d/a
K2 = d/c
K3 = (a**2-b**2+c**2+d**2)/(2*a*c)
A = np.cos(th_a) - K1 - K2*np.cos(th_a) + K3
B = -2*np.sin(th_a)
C = K1 - (K2+1)*np.cos(th_a) + K3

#Grashoff condition
disc = (B**2)-4*A*C 

#Checks if the four_bar linkage is grashoff
if np.greater_equal(disc,0).all() == False:
    print("not grashoff!!")
    assert(0)

if MODE =='negative':
    th_c = 2*np.arctan((-B - np.sqrt(disc) )/(2*A))
else:
    th_c = 2*np.arctan((-B + np.sqrt(disc) )/(2*A))
    

#Degrees, used for drawing arcs
th_c_d = th_c * 180/np.pi

#the other point of ground
th_d = -np.pi*np.ones(len(th_c))


#cos+ jsin
phase1 = [cmath.exp(1j*i) for i in th_a]
#print(phase1)
phase3 = [cmath.exp(1j*i) for i in th_c]
phase4 = [cmath.exp(1j*i) for i in th_d]


R1 = a*np.array(phase1)
R3 = c*np.array(phase3)
R4 = -d*np.array(phase4)




x1,y1 = np.zeros(len(R1)),np.zeros(len(R1))
x2,y2 = np.real(R1),np.imag(R1)
x3,y3 = np.real(R3+R4),np.imag(R3+R4)
x4,y4 = np.real(R4),np.imag(R4) 
#print(R4)



th_b = np.arctan2((y3-y2),(x3-x2))
# th_b = (th_b + 2*np.pi ) % 2*np.pi

phase2 = [cmath.exp(1j*i) for i in th_b]
R2 = b*np.array(phase2)




# '''
# This is to sketch a follower(F)
# '''
# 
"""
plt.plot(x1,y1)
plt.plot(x3,y3)
for num in range(5,10):
    f_d = 45*np.pi/180*np.ones(len(th_a))
    f = 0.1*num*b
    phasef = [cmath.exp(1j*i) for i in f_d]
    Rf = R1+ f*(np.array(phasef)+np.array(phase2))
    xf,yf = np.real(Rf),np.imag(Rf)

    _=plt.plot(xf,yf)
"""



#Creating angle of the follower wrt ground

f_d = Angle*np.pi/180*np.ones(len(th_a))
f_d += th_b

f_dCG = Angle_cg*np.pi/180*np.ones(len(th_a))
f_dCG += th_b
#Follower size
f = Len*b
fCG = Len_cg*b




#Phase of follower 
phasef = [cmath.exp(1j*i) for i in f_d]
Rf = R1+ f*(np.array(phasef))
xf,yf = np.real(Rf),np.imag(Rf)



#Phase of follower centre of gravity
xfg_list , yfg_list =[] ,[]
phasef_CG = [cmath.exp(1j*i) for i in f_dCG]
fCG = [i*b for i in [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]]
if pen_pos == 'center':
    Rf_CG = R1+ 0.5*b*(np.array(phasef_CG))
    xfg,yfg = np.real(Rf_CG),np.imag(Rf_CG)
    for eachpos in fCG:
        Rf_CG = R1+ eachpos*(np.array(phasef_CG))
        xfg_list.append(np.real(Rf_CG))
        yfg_list.append(np.imag(Rf_CG))
elif pen_pos == 'coupler' :
    
    #for demostrate fCG = 0.5*coupler
    Rf_CG = R1+ 0.5*b*(np.array(phase2))
    xfg,yfg = np.real(Rf_CG),np.imag(Rf_CG)
    #print(Rf_CG)
    for eachpos in fCG:
        Rf_CG = R1+ eachpos*(np.array(phase2))
        xfg_list.append(np.real(Rf_CG))
        yfg_list.append(np.imag(Rf_CG))
        
    #print(len(xfg_list[1]))
    #test = math.sqrt(((xfg_list[i][j] - xfg_list[i][j+1])**2 + (yfg_list[i][j]- yfg_list[i][j+1])**2) )






#plt.show()


# Animation


temp = x1,x2,x3,x4
xmin = np.amin([np.amin(mini) for mini in temp])
xmax = np.amax([np.amax(mini) for mini in temp])
temp = y1,y2,y3,y4
ymin = np.amin([np.amin(mini) for mini in temp])
ymax = np.amax([np.amax(mini) for mini in temp])
#xmin,xmax

fig = plt.figure()
fig.set_size_inches(6,6,True)
plt.axis('off')
y_ticks = np.arange(0, 301, 50)
bord = 100 #give the animation an offset

ax = fig.add_subplot(221, autoscale_on=False,
                     xlim=(xmin-bord, xmax+bord), ylim=(ymin-bord, ymax+bord))
#ax.set_yticks(y_ticks)
ax1 = fig.add_subplot(222, autoscale_on=False,
                     xlim=(xmin-bord, xmax+bord), ylim=(ymin-bord, ymax+bord))
            
speedfig = fig.add_subplot(223, autoscale_on=True)
accefig = fig.add_subplot(224, autoscale_on=True)

ax.grid()



#Plot

import matplotlib.animation as animation



#plot location
for i in range(len(xfg_list)):
    ax1.plot(xfg_list[i],yfg_list[i], label = str(fCG[i]))
#ax1.set_xlabel('x_position')
ax1.set_title('pen location', fontsize = 8)
ax1.set_ylabel('y_position')
ax1.legend(loc = "upper right", prop={'size': 8})
#plt.show()


#plot speed

speedlist, totalspeed = [],[]
#get time period

t_step = T*0.01/2
x_t = np.arange(0,3*T-t_step, t_step)
#print(x_t.shape)
for i in range(len(xfg_list)):
    speedlist=[]
    for j in range(len(xfg_list[i])-1):
        distance = math.sqrt(((xfg_list[i][j] - xfg_list[i][j+1])**2 + (yfg_list[i][j]- yfg_list[i][j+1])**2) )
        speedlist.append(distance/t_step)
    speedlist=np.array(speedlist)
    totalspeed.append(speedlist)
    speedfig.plot(x_t , speedlist, label =  str(fCG[i]))
speedfig.set_xlabel('time (s)')
speedfig.set_title('speed for pen location', fontsize = 8)
speedfig.set_ylabel('speed')
speedfig.legend(loc = 'upper right', prop={'size': 8})

#plot accelaration fig
accelist = []
x_t = np.arange(0,3*T-2*t_step-0.001, t_step)
for i in range(len(totalspeed)):
    accelist=[]
    for j in range(len(totalspeed[i])-1):
        delta_v = (totalspeed[i][j+1] - totalspeed[i][j]) 
        accelist.append(delta_v/t_step)
    accelist=np.array(accelist)
    accefig.plot(x_t , accelist, label =  str(fCG[i]))
accefig.set_xlabel('time (s)')
accefig.set_title('acceleration for pen location', fontsize = 8)
accefig.set_ylabel('acceleration')
accefig.legend(loc = 'upper right', prop={'size': 8})


line, = ax.plot([], [], marker = 'o',c = 'k',lw = 6,ms = 10)
if pen_pos == 'center':
    line2, = ax.plot([], [], marker = 'o',c = 'b',lw = 6,ms = 4)
line3, = ax.plot([], [], marker = 'x',c = 'g',lw = 5,ms = 20)
_ = ax.plot(xfg,yfg , c ='sienna')





#Plotting follower CG path(static)



def init():
    line.set_data([],[])
    if pen_pos == 'center':
        line2.set_data([],[])
    line3.set_data([],[])

    if pen_pos == 'center':
        return line,line2,line3,
    return line,line3,

def animate(i):
    thisx = [x1[i],x2[i],x3[i],x4[i]]
    thisy = [y1[i],y2[i],y3[i],y4[i]]
    line.set_data(thisx,thisy)
    if pen_pos == 'center':
        thisx = [x2[i],xf[i],x3[i]]
        thisy = [y2[i],yf[i],y3[i]]
        line2.set_data(thisx,thisy)
    thisx = [x2[i],xfg[i]]
    thisy = [y2[i],yfg[i]]
    line3.set_data(thisx,thisy)
    if pen_pos == 'center':
        return line,line2,line3,
    return line,line3,




ani = animation.FuncAnimation(fig, animate, np.arange(1, len(y2)),
                              interval=T_animation, blit=True, init_func=init)
plt.show()




#To save animation, comment out the sys.exit()

sys.exit()

#Save animation
"""
Writer = animation.writers['ffmpeg']
writer = Writer(fps = 30,extra_args=['-vcodec', 'libx264'])
dpi = 100

ani.save('demo4.mp4', writer = writer,dpi = dpi)
"""