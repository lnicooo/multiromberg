import numpy as np
import matplotlib.pyplot as plt

func = lambda x: (np.log(np.exp(x*np.log(x)))/np.log(4)) * np.sin(x) 

gaussian = lambda x: 1/np.sqrt(np.pi) * np.exp(-x**2)

# trapezoidal rule
def trapezoid(f,a,b,N):
    h   = (b-a)/N
    xi  = np.linspace(a,b,N+1)
    fi  = f(xi)
    s   = 0.0
    for i in range(1,N):
        s = s + fi[i]
    s = (h/2)*(fi[0] + fi[N]) + h*s
    return s

# romberg method
def romberg(f,a,b,eps,nmax):
# f     ... function to be integrated
# [a,b] ... integration interval
# eps   ... desired accuracy
# nmax  ... maximal order of Romberg method
    Q         = np.zeros((nmax,nmax),float)
    converged = 0
    for i in range(0,nmax):
        N      = 2**i
        Q[i,0] = trapezoid(f,a,b,N)
        print("i:%d q:%f"%(i,Q[i,0]))
        
        for k in range(0,i):
            n        = k + 2
            Q[i,k+1] = 1.0/(4**(n-1)-1)*(4**(n-1)*Q[i,k] - Q[i-1,k])
            
    for x in range(0,nmax):
      for k in range(0,x+1):
        print("i:%d k:%d %.8f"%(x,k,Q[x,k]),end =" ")  
      print()

    print("The final result is %.8f"%Q[-1,-1])
   
    

# main program
a  = 0.0;b = 1.0  # integration interval [a,b]
romberg(gaussian,a,b,1.0e-12,10)

