import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from threading import Thread, Lock

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
  

# romberg method
# f     ... function to be integrated
# [a,b] ... integration interval
# eps   ... desired accuracy
# nmax  ... maximal order of Romberg method

def romberg_thread(f,a,b,Q,i):

  N = 2**i
  
  mutex.acquire()
  Q[i,0] = trapezoid(f,a,b,N)
  mutex.release()

  for k in range(0,i):

    if(k<=0):

      Q[i,k] = trapezoid(f,a,b,N)

    else:

      print("a")

      n = k + 2
      
      mutex.acquire()

      Q[i,k] = 1.0/(4**(n-1)-1) * (4**(n-1) *Q[i,k] - Q[i-1,k])
      
      mutex.release()
  

def romberg(f,a,b,eps,nmax):    

    Q = np.zeros((nmax,nmax),float)

    for i in range(0,nmax):

      t = Thread(target = romberg_thread, args = (f,a,b,Q,i))
      t.start()
      
    print (Q[-2,0]) 
    #return Q[i,k+1],N,converged



# main program
a  = 0.0;b = 1.0  # integration interval [a,b]
romberg(gaussian,a,b,1.0e-12,10)
integrate.romberg(gaussian, a, b, show=True)