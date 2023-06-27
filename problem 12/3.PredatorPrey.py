from cProfile import label
import matplotlib.pyplot as plt
import numpy as np


# ∆x1 = 1/T*αx − βxy
# ∆y1 = 1/T*γxy − δy


def sim(x,y,a,b,s,T,Y):
    def delta_x():
        return (1/T)*(a*x - b*x*y)
    
    def delta_y():
        return (1/T)*(Y*x*y -s*y)
       
    result_x=x+delta_x()
    result_y=y+delta_y()
    return [result_x , result_y]

# x0 =10, y0 = 5, α = 1.0, β = 0.3, γ = 0.1, δ = 0.3, T1 = 0.0001

rabbits=[10] #x0
wolves=[5] #y0

for i in range(1_000_000):
    tup=sim(x=rabbits[i],y=wolves[i],a=1.0,b=0.3,Y=0.1,s=0.3,T=10_000)
    rabbits.append(tup[0])
    wolves.append(tup[1])


len_wolves=len(wolves)
xticks=np.linspace(0,100,len_wolves)

plt.plot(xticks,rabbits,label='rabbits')
plt.plot(xticks,wolves,label='wolves')

plt.xlabel("Time in years")
plt.ylabel("population")
plt.title("Lotka-Volterra Model")
# plt.xticks()
plt.legend(loc='upper right')

           
plt.show()
