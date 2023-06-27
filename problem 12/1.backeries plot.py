import csv
import matplotlib.pyplot as plt
import numpy as np

suger=[]
fat=[]
bought_unit=[]
price_per_unit=[]
with open('bakeries.csv','r') as file:
    csv_r=csv.reader(file)
    for row in csv_r:
        try:
            suger.append(float(row[0]))
            fat.append(float(row[1]))
            bought_unit.append(float(row[2]))
            price_per_unit.append(float(row[3]))        
        except:
            continue
        
# suger=np.array(suger)
# fat=np.array(fat)
# bought_unit=np.array(bought_unit)
# price_per_unit=np.array(price_per_unit)

plt.scatter(x=fat,y=suger,c=price_per_unit,s=bought_unit)
plt.xlabel('fat in %')
plt.ylabel('suger in %')
plt.colorbar(label='price per unit',orientation="vertical")
plt.title("foo bar")
plt.show()