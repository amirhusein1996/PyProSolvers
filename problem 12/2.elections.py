import csv
import matplotlib.pyplot as plt


years=[]
cdu_csu=[]
spd=[]
fdp=[]
gr=[]
ba_gr=[]
pds=[]
afd=[]
sonstige=[]
with open('elections.csv','r') as file:
    elections=csv.DictReader(file)
    
    for row in elections:

        years.append(row['Jahr'])
        cdu_csu.append(row['CDU/CSU'])
        spd.append(row['SPD'])
        fdp.append(row['FDP'])
        gr.append(row['Die GrÃ¼nen'])
        ba_gr.append(row['BÃ¼ndnis 90/Die GrÃ¼nen'])
        pds.append(row['Die Linke. PDS'])
        afd.append(row['AfD'])
        sonstige.append(row['Sonstige'])
				
def correction(lst:list):

    for item in lst:
        indx=lst.index(item)
        if not item.replace('.','').isnumeric():
            lst[indx]=0
        else:
            lst[indx]=float(item)
    return lst



gr=correction(gr)
ba_gr=correction(ba_gr)
afd=correction(afd)
pds=correction(pds)

mycolors = ["black", "red", "yellow", "green",'#00FF00','#8B0000','#6495ED','#A9A9A9']
mylabes=['CDU/CSU','SPD','FDP','Die Grünen','Bündnis 90/Die Grünen','Die Linke. PDS','AfD','Sonstige']
for i in range(len(years)):
    res=[]
    r=0.05*i
    res.append(cdu_csu[i])
    res.append(spd[i])
    res.append(fdp[i])
    res.append(gr[i])
    res.append(ba_gr[i])
    res.append(pds[i])
    res.append(afd[i])
    res.append(sonstige[i])
    
    if i == 0:
        plt.pie(res,radius=1.25-r,colors=mycolors,wedgeprops=dict(width=0.05, edgecolor='#696969'),labels=mylabes)
        continue
    plt.pie(res,radius=1.25-r,colors=mycolors,wedgeprops=dict(width=0.05, edgecolor='#696969'))

plt.title('Deutsche Bunderstagswahlen, 1949-2021')

plt.show()