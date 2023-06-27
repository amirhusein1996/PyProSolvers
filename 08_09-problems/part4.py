#part 1

class Item :
    
    def __init__(self,name, characteristic, magnitude, consumable):
        self.name=name
        self.characteristic=characteristic
        self.magnitude=magnitude
        self.consumable=consumable 
      
    def __str__(self):
        if self.consumable==True:
            return f' {self.name }(+{self.magnitude} {self.characteristic},consumable)'
        else :
            return f' {self.name }(+{self.magnitude} {self.characteristic},permanent)'
items = []
items.append( Item("Holy Hendgrenade of Anitoch", "strength", 10, True) )
items.append( Item("Berret", "charisma", 3, False) )
# for item in items :
#     print(item)

#part 2 , updating to part3

from random import randint
class Player :
    backpack_limit=3

    baseHealth = 10
    baseStrength = 5
    baseIntelligence = 5
    baseSpeed = 5
    baseCharisma = 5

    fluctuationHealth = 5
    fluctuationStrength = 2
    fluctuationIntelligence = 2
    fluctuationSpeed = 2
    fluctuationCharisma = 2
    def __init__ (self, name) :
        self.name=name
        self.backpack=[]
        self.step_toward_succuss=0
        
        self.characteristics={"health":randint(Player.baseHealth-Player.fluctuationHealth,Player.baseHealth+Player.fluctuationHealth)
                                ,"strength":randint(Player.baseStrength-Player.fluctuationStrength,Player.baseStrength+Player.fluctuationStrength)
                                ,"intelligence":randint(Player.baseIntelligence-Player.fluctuationIntelligence,Player.baseIntelligence+Player.fluctuationIntelligence)
                                ,"speed":randint(Player.baseSpeed-Player.fluctuationSpeed,Player.baseSpeed+Player.fluctuationSpeed)
                                ,"charisma":randint(Player.baseCharisma-Player.fluctuationCharisma,Player.baseCharisma+Player.fluctuationCharisma)
                                }
    
    def add_item(self,item):
        dublicate=False
        
        if len(self.backpack)<Player.backpack_limit and item.consumable==True:
            self.backpack.append(item)
        elif len(self.backpack)<Player.backpack_limit and item.consumable== False:
            for object in self.backpack:
                if object.name==item.name:
                    dublicate=True
            if dublicate:
                print('This permanent item is already in your backpack')      
            
            else:
                self.backpack.append(item)
                dublicate=False
        else:
            print('Your backpack is full.\nWhich item do you want to leave behind?')
            self.backpack.insert(0,item)
            for i in self.backpack:
                print(self.backpack.index(i),f') {i}')    
            print('Please enter the number of the item to discard now:  2')
            input_discard=2
            self.backpack.pop(input_discard)


    def get(self,parameter):
        for item in self.backpack:
            if item.characteristic==parameter and item.consumable==False:
                self.characteristics[parameter]+=item.magnitude
                self.backpack.remove(item)  #after item took the effect, should be remove from backpack to avoid reusing
                return self.characteristics[parameter] 
        return self.characteristics[parameter]
            
    def __str__ (self) :
        if len(self.backpack)==0:
            return f'''PLAYER\n\tname\t\t\t: {self.name}\n\tsteps toward success\t: {self.step_toward_succuss}
        health\t\t\t: {self.characteristics["health"]}\n\tstrength\t\t: {self.characteristics["strength"]}
        intelligence:\t\t: {self.characteristics["intelligence"]}\n\tspeed\t\t\t: {self.characteristics["speed"]}
        charisma\t\t: {self.characteristics["charisma"]}
        in their backpack:\n\t(nothing)'''
        
        elif len(self.backpack)==1:
            return f'''PLAYER\n\tname\t\t\t: {self.name}\n\tsteps toward success\t: {self.step_toward_succuss}
        health\t\t\t: {self.characteristics["health"]}\n\tstrength\t\t: {self.characteristics["strength"]}
        intelligence:\t\t: {self.characteristics["intelligence"]}\n\tspeed\t\t\t: {self.characteristics["speed"]}
        charisma\t\t: {self.characteristics["charisma"]}
        in their backpack:\n\t{self.backpack[0].name}'''
    
        elif len(self.backpack)==2:
            return f'''PLAYER\n\tname\t\t\t: {self.name}\n\tsteps toward success\t: {self.step_toward_succuss}
        health\t\t\t: {self.characteristics["health"]}\n\tstrength\t\t: {self.characteristics["strength"]}
        intelligence:\t\t: {self.characteristics["intelligence"]}\n\tspeed\t\t\t: {self.characteristics["speed"]}
        charisma\t\t: {self.characteristics["charisma"]}
        in their backpack:\n\t{self.backpack[0].name},{self.backpack[1].name}'''
    
        elif len(self.backpack)==3:
            return f'''PLAYER\n\tname\t\t\t: {self.name}\n\tsteps toward success\t: {self.step_toward_succuss}
        health\t\t\t: {self.characteristics["health"]}\n\tstrength\t\t: {self.characteristics["strength"]}
        intelligence:\t\t: {self.characteristics["intelligence"]}\n\tspeed\t\t\t: {self.characteristics["speed"]}
        charisma\t\t: {self.characteristics["charisma"]}
        in their backpack:\n\t{self.backpack[0].name},{self.backpack[1].name},{self.backpack[2].name}'''

        else:
            return f'{len(self.backpack)}'
                    
            
    
      
items = [Item("Holy Hendgrenade of Anitoch" , "strength", 10, True),
Item("Berret" , "charisma", 3 , False),
Item("Bullwhip" , "strength" , 1 , False),
Item("Dune - The Desert Planet (book)", "intelligence", 3 , False)
]

player = Player("Dusky Joe")

print("Base strength:", player.get("strength"))
player.add_item( items[0] ) # Holy Hendgrenade -- okay
player.add_item( items[1] ) # Berret -- okay
player.add_item( items[2] ) # Bullwhip -- okay




print("With items:", player.get("strength"))
