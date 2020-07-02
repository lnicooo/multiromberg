import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from threading import Thread, Lock
from scipy import integrate


mutex = Lock()

gaussian = lambda x: 1/np.sqrt(np.pi) * np.exp(-x**2)

class Romberg:
  def __init__ (self,f,a,b,eps,nmax):

    self.f = f
    self.a = a
    self.b = b
    self.eps = eps
    self.nmax = nmax

  # trapezoidal rule
  def trapezoid(self,N):

    f = self.f
    a = self.a
    b = self.b

    h   = (b-a)/N
    xi  = np.linspace(a,b,N+1)
    fi  = f(xi)

    s=np.sum(fi[1:-1])

    s = (h/2)*(fi[0] + fi[N]) + h*s

    return s

  def romberg_thread(self,Q,Q_act,Q_lst,i,k):

    #print(Q_lst)

    if(k==0):

      N = 2**i
      q = self.trapezoid(N)
      
    else:

      #m = (k + 2)-1
      q = 1.0/(4**(k)-1) * (4**(k) *(Q_act - Q_lst))

    
    print("k:%d q:%f i:%d"%(k,q,i))

    mutex.acquire()
    Q[k] = q
    mutex.release()
  
  def run(self):

    Q = np.zeros((self.nmax,self.nmax),float)

    for i in range(0,self.nmax):

      threads=[]

      for k in range(0,i):
        
        thread = Thread(target = self.romberg_thread, 
            args = (Q[i],Q[i,k-1],Q[i-1,k-1],i,k))
        
        thread.start()
        #print("Thread[%d][%d]inited"%(i,k))
        #print("Value Q[%d][%d]:%f sended"%(i,k,Q[i-1,k]))
        threads.append(thread)

      for thread in threads:
        thread.join()
    
    for i in range(self.nmax):
      for k in range(i):
        print("%.4f"%Q[i,k],end =" ")  
      print()
        
    #print (Q[-2,0]) 


if __name__ == '__main__':
  # main program
  a  = 0.0;b = 1.0  # integration interval [a,b]
  R = Romberg(gaussian,a,b,1.0e-12,10)
  R.run()
  integrate.romberg(gaussian, a, b, show=True)
