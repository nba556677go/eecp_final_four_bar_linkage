

import matplotlib.pyplot as plt
import numpy as np
import sys

from matplotlib import patches
import matplotlib.animation as animation


    

def calc_th_b(a,b,c,d,th_a,show_angle=False):
    '''
    Calculates theta b using Freuedenstein equations
    '''
    K1 = d/a
    K4 = d/b
    K5 = (-a**2-b**2+c**2-d**2)/(2*a*b)
    D = np.cos(th_a) - K1 + K4*np.cos(th_a) + K5
    E = -2*np.sin(th_a)
    F = K1 + (K4-1)*np.cos(th_a) + K5
    disc = (E**2)-4*D*F 
    #Checks if non-grashoff, and extracts the valid angles
    if not(np.greater_equal(disc,0).all()):
        print("It's Non grashoff!!!")
        #This extracts the th_a elements with discriminants > 0 and reruns the function.
        condition = np.greater_equal(disc,0)
        th_a = np.extract(condition, th_a)
#        condition = np.less_equal(th_a, np.pi)
#        th_a= np.extract(condition,th_a)
        th_a=np.append(th_a,th_a[-2::-1])
        _,th_b=calc_th_d(a,b,c,d,th_a)
    else:
        th_b=2*np.arctan((-E - np.sqrt(disc) )/(2*D)) 
    if show_angle:
        plt.plot(th_a,th_b)
        plt.show()    
    return th_a,th_b    

def calc_th_d(a,b,c,d,th_a,show_angle=False):
    '''
    Calculates theta d using Freuedenstein equations
    '''
    K1 = d/a
    K2 = d/c
    K3 = (a**2-b**2+c**2+d**2)/(2*a*c)
    A = np.cos(th_a) - K1 - K2*np.cos(th_a) + K3
    B = -2*np.sin(th_a)
    C = K1 - (K2+1)*np.cos(th_a) + K3
    #Grashoff condition
    disc = (B**2)-4*A*C 
    #Checks if non-grashoff, and extracts the valid angles
    if not(np.greater_equal(disc,0).all()):
        #This extracts the th_a elements with discriminants > 0 and reruns the function.
        condition = np.greater_equal(disc,0)
      
        th_a = np.extract(condition, th_a)
      
#        condition = np.less_equal(th_a, np.pi)
#        th_a= np.extract(condition,th_a)
        th_a=np.append(th_a,th_a[-2::-1])#Full range of non-grashoff motion
        _,th_d=calc_th_d(a,b,c,d,th_a)
    else:
        th_d=2*np.arctan((-B - np.sqrt(disc) )/(2*A)) 
    if show_angle:
        plt.plot(th_a,th_d)
        plt.show()
    return th_a,th_d
    
def generate_th_a(rotation='cw',step=0.01):
    return np.arange(2*np.pi,0,-step*np.pi) if rotation=='cw' else np.arange(0,2*np.pi+0.0001,step*np.pi)

def calc_joint_position(a,b,c,d,th_a):
    '''
    Calculates the position of the joints 
    '''
    th_a,th_d=calc_th_d(a,b,c,d,th_a, show_angle= False)
#    print(th_a)
#    print(th_d)
    x1,x4 = 0,d
    y1,y4 = 0,0
    x2,x3 = a*np.cos(th_a), d + c*np.cos(th_d)
    y2,y3 = a*np.sin(th_a), c*np.sin(th_d)
    
    return x1,x2,x3,x4,y1,y2,y3,y4
def animate_linkage_motion(x1,x2,x3,x4,y1,y2,y3,y4,save_animation=False,animation_name='FourBarLinkage'):
    def animate(i,x1,x2,x3,x4,y1,y2,y3,y4):#for funcanimation

        thisx = [x1, x2[i],x3[i],x4]
        #print(thisx)
        thisy = [y1, y2[i],y3[i],y4]
        line.set_data(thisx, thisy)
        
        return line,#patch1,patch2,patch4,ang_text,arrow2,#arrow3,arrow1

    #Defining xandylims of the plot
    temp = x1,x2,x3,x4
    #print(temp)
    xmin = np.amin([np.amin(mini) for mini in temp])
    #print(xmin)
    xmax = np.amax([np.amax(mini) for mini in temp])
    temp = y1,y2,y3,y4
    ymin = np.amin([np.amin(mini) for mini in temp])
    ymax = np.amax([np.amax(mini) for mini in temp])
    #xmin,xmax
    
    fig = plt.figure()
    fig.set_size_inches(6,4.8,True)
    plt.axis('off')
    plt.tight_layout()
    bord = 200 #FBL an offset
    ax = fig.add_subplot(111, autoscale_on=True,
                         xlim=(xmin-bord, xmax+bord), ylim=(ymin-bord, ymax+bord))
    ax.grid()
    #Draw linkages
    line, = ax.plot([], [], marker = 'o',c = 'k',lw = 6,ms = 10)

 
    
    #Animate the FBL
    ani = animation.FuncAnimation(fig, animate, frames=len(y2),fargs=(x1,x2,x3,x4,y1,y2,y3,y4),
                              interval=30, blit=True)
    """                          
    if save_animation:
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps = 30,extra_args=['-vcodec', 'libx264'],bitrate = 3000)
        dpi = 100
        ani.save('{}.mp4'.format(animation_name), writer = writer,dpi = dpi)
    """
    return ani

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
if __name__=='__main__':
    a = int(input("Enter input(100/100) : ") )
    b = int(input("Enter coupler(200/250) : "))
    c = int(input("Enter output(200/300) : "))
    d = int(input("Enter frame(350/200) : ") )
    #case= decide_grashoff(a,b,c,d)
    #if case=='ng':
    #Non-grashoff a,b,c,d = 100,200,200,350
    #Grashoff a,b,c,d = 100,250,300,200  
    checkgra = [a ,b ,c ,d]
    checkgra.sort()
    if checkgra[0]+checkgra[3] > checkgra[1] + checkgra[2]:
        print("Non grashoff!!!")
    else:
        print("It is grashoff!!!")
    th_a=generate_th_a(step=1E-2)
    x1,x2,x3,x4,y1,y2,y3,y4=calc_joint_position(a,b,c,d,th_a)
    anim1=animate_linkage_motion(x1,x2,x3,x4,y1,y2,y3,y4)
    plt.show()
