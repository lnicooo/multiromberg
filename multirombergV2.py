import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from threading import Thread, Lock
from time import sleep

mutex = Lock()

gaussian = lambda x: 1/np.sqrt(np.pi) * np.exp(-x**2)

# trapezoidal rule
def trapezoid(f,a,b,N):

    h   = (b-a)/N
    xi  = np.linspace(a,b,N+1)
    fi  = f(xi)

    s=np.sum(fi[1:-1])

    s = (h/2)*(fi[0] + fi[N]) + h*s

    return s

def calc(f,a,b,N,Q_lst,Q_act,k):

  if(k<=0):

    q = trapezoid(f,a,b,N)

  else:
    n = k + 2
    q=1.0/(4**(n-1)-1) * (4**(n-1) * Q_act - Q_lst)

  mutex.acquire()
  Q[i,k] = q
  mutex.release()

# romberg method
# f     ... function to be integrated
# [a,b] ... integration interval
# eps   ... desired accuracy
# nmax  ... maximal order of Romberg method

def romberg_thread(f,a,b,eps,nmax,Q,k,i):

  N = 2**i
  
  mutex.acquire()
  #print("i:"+str(i)+"k:"+str(k)+"Q[i,k]:"+str(Q[i,k],Q[i-1,k])
  #print("i:%d k:%d Q[%d,%d]:%f Q[i-1,k]:%f"%(i,k,i,k,Q[i,k],Q[i-1,k]))
  calc(f,a,b,N,Q[i,k],Q[i-1,k],k)
  mutex.release()

  

def romberg(f,a,b,eps,nmax):    

    Q = np.zeros((nmax,nmax),float)

    for i in range(0,nmax):

      for k in range(0,i):

        t = Thread(target = romberg_thread, args = (f,a,b,eps,nmax,Q,k,i))
        t.start()
    
    for i in range(nmax):
      for k in range(i):
        print("%.4f"%Q[i,k],end =" ")  
      print()
        
    print (Q[-2,0]) 
    #return Q[i,k+1],N,converged



# main program
a  = 0.0;b = 1.0  # integration interval [a,b]
romberg(gaussian,a,b,1.0e-12,10)

