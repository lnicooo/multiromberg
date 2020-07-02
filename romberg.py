import numpy as np
import matplotlib.pyplot as plt

def f1(x):
   f1 = x**4.0
   return f1;

def f2(x):
   f2 = np.exp(-x*x)
   return f2;

def f3(x):
   tau   = 1.0e-8
   f3    = np.where(np.abs(x)<tau,1.0,np.sin(x)/x)
   return f3;

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
        for k in range(0,i):
            n        = k + 2
            Q[i,k+1] = 1.0/(4**(n-1)-1)*(4**(n-1)*Q[i,k] - Q[i-1,k])
        if (i > 0) and (abs(Q[i,k+1] - Q[i,k]) < eps):
            if (abs(Q[i,k+1] - Q[i,k]) < eps):
               converged = 1
               break
    for i in range(nmax):
      for k in range(i):
        print("%.4f"%Q[i,k],end =" ")  
      print()

    print (Q[i,k+1])
    return Q[i,k+1],N,converged

# main program
a  = 0.0;b = 1.0  # integration interval [a,b]
romberg(gaussian,a,b,1.0e-12,10)

