import csv
import numpy as np
import matplotlib.pyplot as plt

N = 100

X = np.abs( np.random.normal (0.7, 4.0, N) )
Y = np.abs( np.random.normal (0.5, 2.1, N) )
S = np.abs( np.random.laplace(0.0, 10 , N) )
C = np.abs( np.random.normal (3.5, 3.5, N) )

X = np.concatenate( (X, np.abs(np.random.normal (9.7, 3.0, N))) )
Y = np.concatenate( (Y, np.abs(np.random.normal (8.5, 3.5, N))) )
S = np.concatenate( (S, np.abs(np.random.laplace(0.0, 10 , N))) )
C = np.concatenate( (C, np.abs(np.random.normal (7.5, 1.5, N))) )

writeObject = zip(X, Y, S, C)
with open("bakeries.csv", "w") as hFile :
    writer = csv.writer(hFile)

    writer.writerow(["sugar in %", "fat in %", "avg. units bought per day", "price per unit"])
    for line in writeObject :
        writer.writerow(line)



