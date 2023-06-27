import random

test_mode = True

# ============================================================================ #

class Item :
    def __init__ (self, name, characteristic, magnitude, consumable) :
        self.name           = name
        self.characteristic = characteristic
        self.magnitude      = magnitude
        self.consumable     = consumable

    def __str__ (self) :
        return self.name + \
            f" ({self.magnitude:+1} {self.characteristic}," + \
            f" {'consumable' if self.consumable else 'permanent'})"

# ============================================================================ #

class Player :
    base_health       = 10
    base_strength     =  5
    base_intelligence =  5
    base_speed        =  5
    base_charisma     =  5

    fluctuation_health       = 5
    fluctuation_strength     = 2
    fluctuation_intelligence = 2
    fluctuation_speed        = 2
    fluctuation_charisma     = 2

    backpack_limit = 3                      # may not be bigger than the number of items in game

    # ........................................................................ #

    def __init__ (self, name) :
        self.name = name

        self.characteristics = dict()

        attributes = [                                      # A list of strings, containing "health", "strength", ..., generated from ...
            base[ base.index('_') + 1 : ]                   # everyting after the first underscore in base, where base is ...
            for base in (                                   # a string that starts with 'base' that is a class attribute of class Player.
                x for x in Player.__dict__                  # almost all objects have a dunder __dict__, which lists all *instance* attributes.
                if type(x) == str and x.startswith('base')  # classes are objects, too, and their *instance* attriubes are the *class* attributes of their instances.
            )
        ]

        for attr in attributes :
            base  = Player.__dict__["base_"        + attr]
            fluct = Player.__dict__["fluctuation_" + attr]
            self.characteristics[attr] = base + random.randint(-fluct, +fluct)

        self.backpack = []

        self.progress   = 0
        self.skip_turns = 0

    # ........................................................................ #

    def __str__ (self) :
        reVal = "PLAYER:\n"
        reVal += "\tname                : " + self.name          + "\n"
        reVal += "\tsteps toward success: " + str(self.progress) + "\n"

        reVal += "".join( f"\t{characteristic:20}: {value}\n" for characteristic, value in self.characteristics.items() )

        reVal += "\tin their backpack:\n"
        reVal += "".join( "\t* " + str(item) + "\n" for item in self.backpack ) if self.backpack else "\t(nothing)\n"

        return reVal

    # ........................................................................ #

    def add_item (self, item) :
        if not item.consumable :
            if any(item.name == backpackitem.name for backpackitem in self.backpack) :
                print(f"This permanent item '{item.name}' is already in your backpack")
                return

        if len(self.backpack) == self.backpack_limit :
            print("Your backpack is full.")
            print("Which item do you want to leave behind?")
            for i, old_item in enumerate(self.backpack) :
                print(str(i) + ")", old_item)
            print(str(i+1) + ")", item)

            slot_id = int(input("Please enter the number of the item to discard now: "))

            if slot_id >= self.backpack_limit : return
            else                              : self.backpack[slot_id] = item

            return

        self.backpack.append(item)

    # ........................................................................ #

    def get (self, characteristic) :
        return self.characteristics[characteristic] + \
            sum(item.magnitude for item in self.get_permanent_items().values() if item.characteristic == characteristic)

    # ........................................................................ #

    def get_consumable_items (self) :
        return {slot : item for slot, item in enumerate(self.backpack) if item.consumable}

    # ........................................................................ #

    def get_permanent_items (self) :
        return {slot : item for slot, item in enumerate(self.backpack) if not item.consumable}

    # ........................................................................ #

    def face_peril (self, peril) :
        print( peril.text )

        # .................................................................... #

        while True :
            answer = input("").strip().upper()

            if answer == "YES" :
                task = peril.task_yes
                break

            elif answer == "NO" :
                task = peril.task_no
                break

            else :
                print("Invalid answer -- please enter 'yes' or 'no'.")

        # .................................................................... #

        print(task.text)
        print(f"Requirement: {task.characteristic}. Cost: {task.cost}")

        if task.characteristic == "skip turn" :
            self.skip_turns = task.cost
            return

        # .................................................................... #

        number_of_dice = self.get(task.characteristic)
        consumables = self.get_consumable_items()

        while len(consumables) :
            print(f"You may use {number_of_dice} dice.")
            print(f"Current health: {self.characteristics['health']}")
            print("Do you want to use an item? You could use...:")
            for ID, item in consumables.items() :
                print("   ", ID, ") ", str(item), sep="")
            print("   (or enter for nothing)")
            answer = input()

            if answer == "" :
                break
            else :
                answer = int(answer)
                if answer not in consumables :
                    print("invalid option")
                    continue

                used_item = self.backpack.pop(answer)
                number_of_dice += used_item.magnitude * (used_item.characteristic == task.characteristic)

                consumables = self.get_consumable_items()

        print(f"You may use {number_of_dice} dice.")

        # .................................................................... #

        passed = task_passed(number_of_dice, task.cost)

        if passed :
            print( task.text_pass )
            self.progress += 1
            self.add_item( random.choice(items) )
        else :
            print( task.text_fail )
            self.characteristics[task.characteristic] -= task.penalty

# ============================================================================ #

class Task :
    def __init__ (self, characteristic, cost, penalty, text, text_pass, text_fail) :
        self.characteristic = characteristic
        self.cost           = cost
        self.penalty        = penalty
        self.text           = text
        self.text_pass      = text_pass
        self.text_fail      = text_fail

    def __str__ (self) :
        result  = "TASK:\n"
        result += "category: " + self.characteristic + "\n"
        result += "cost    : " + str(self.cost) + "\n"
        result += "penalty : " + str(self.penalty) + "\n"
        result += "text    : " + self.text + "\n"
        result += "on pass : " + self.text_pass + "\n"
        result += "on fail : " + self.text_fail + "\n"
        return result

# ============================================================================ #

class Peril :
    def __init__ (self, text, task_yes, task_no) :
        self.text     = text
        self.task_yes = task_yes
        self.task_no  = task_no

    def __str__ (self) :
        result  = "PERIL:\n"
        result += "text: " + self.text + "\n"
        result += str(self.task_yes)
        result += str(self.task_no )
        return result

# ============================================================================ #

def task_passed (number_of_dice, cost) :
    success = 0
    last_roll = 1

    while last_roll :
        dice = [random.randint(1, 6) for i in range(number_of_dice)]
        last_roll = sum(1 for die in dice if die >= 5)
        success += last_roll

        print("You rolled:", dice, "=> number of successes:", last_roll, "=> total success:", success)

        if success >= cost : return True

    return False

# ============================================================================ #

def get_winnners (players, max_rounds) :
    return [p for p in players if p.progress >= max_rounds]

# ============================================================================ #
# test codes

if test_mode :
    print("#" * 80)
    print("###" + f"{'CODEBASE TESTS':^74}" + "###")
    print("#" * 80)
    print()

    # ........................................................................ #
    print("Items test")
    print("~~~~~~~~~~\n")

    items = [
        Item("Holy Hendgrenade of Anitoch"    , "strength",     10, True),
        Item("Berret"                         , "charisma",     3 , False),
        Item("Bullwhip"                       , "strength"    , 1 , False),
        Item("Dune - The Desert Planet (book)", "intelligence", 3 , False)
    ]

    for item in items :
        print(item)
    print()

    # ........................................................................ #
    print("Player __init__ and __str__ test")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

    players = []
    players.append( Player("Dusky Joe") )
    players.append( Player("Petra van Chameleon") )

    for player in players :
        print(player)

    # ........................................................................ #
    print("Player add_item test")
    print("~~~~~~~~~~~~~~~~~~~~\n")

    player = Player("Dusky Joe")

    player.add_item( items[0] )   # okay
    player.add_item( items[1] )   # okay
    player.add_item( items[2] )   # okay

    player.add_item( items[1] )   # test: duplicate permanent item
    player.add_item( items[0] )   # test: too many items in backpack

    print(player)

    # ........................................................................ #
    print("Player get test")
    print("~~~~~~~~~~~~~~~\n")

    player = Player("Dusky Joe")

    print( f"{'plain strength (no items)':30}", player.get("strength") )

    player.add_item( items[0] )
    player.add_item( items[1] )
    player.add_item( items[2] )

    print( f"{'strength with items':30}", player.get("strength") )
    print()

    # ........................................................................ #
    print("Peril and Task test")
    print("~~~~~~~~~~~~~~~~~~~\n")

    perils = [
        Peril("The deep jungle suddenly ends on a cliff. In front of you, a chasm opens " + \
              "up and a deep gorge stands between you and the temple. There is a narrow " + \
              "and shaky suspension bridge over the gorge.\n" + \
              "Do you step on the bridge?",
              Task("speed", 16, 3,
                   "Half way over the bridge, you hear the hissing sound of ropes " + \
                   "disintegrating: one of the ropes holding the bridge is about to snap!\n" + \
                   "Run for your life!",
                   "You dash forward as fast as you can. By a hair's breadth you make it to " + \
                   "the other side before the bridge collapses. You are safe... for now...",
                   "In spite of your best effort you cannot make it to the other side before " + \
                   "the bridge collapses. You fall down into the water. The fall hurts a lot."
              ),
              Task("skip turn", 1, 0,
                   "You try to find another way across the gorge, which takes a lot of time.\n" + \
                   "Skip one turn.",
                   "", ""
              )
        )
    ]

    print( perils[0] )

    # ........................................................................ #
    print("task_passed test")
    print("~~~~~~~~~~~~~~~~\n")

    print( task_passed(3, 0) )
    print( task_passed(3, 100) )

    # ........................................................................ #
    print("Face Peril test")
    print("~~~~~~~~~~~~~~~\n")

    player.face_peril( perils[0] )


# ============================================================================ #
# the game (I loose...)

items = [
    Item("Holy Hendgrenade of Anitoch"    , "strength",     10, True),
    Item("Berret"                         , "charisma",     3 , False),
    Item("Bullwhip"                       , "strength"    , 1 , False),
    Item("Dune - The Desert Planet (book)", "intelligence", 3 , False)
]

players = [
    Player("Dusky Joe"),
    Player("Petra van Chameleon")
]

perils = [
    Peril("The deep jungle suddenly ends on a cliff. In front of you, a chasm opens " + \
          "up and a deep gorge stands between you and the temple. There is a narrow " + \
          "and shaky suspension bridge over the gorge.\n" + \
          "Do you step on the bridge?",
          Task(characteristic = "speed",
               cost = 16,
               penalty = 3,
               text = "Half way over the bridge, you hear the hissing sound of ropes " + \
                   "disintegrating: one of the ropes holding the bridge is about to snap!\n" + \
                   "Run for your life!",
               text_pass = "You dash forward as fast as you can. By a hair's breadth you make it to " + \
                   "the other side before the bridge collapses. You are safe... for now...",
               text_fail = "In spite of your best effort you cannot make it to the other side before " + \
                   "the bridge collapses. You fall down into the water. The fall hurts a lot."
          ),
          Task(characteristic = "skip turn",
               cost = 1,
               penalty = 0,
               text = "You try to find another way across the gorge, which takes a lot of time.\n" + \
                   "Skip one turn.",
               text_pass = "",
               text_fail = ""
          )
    ),

    Peril("A tribe of natives discovered you on their sacred cerimonial grounds.\n"
          "Do you try to appease them (yes) or run away (no)?",
          Task("charisma", 25, 1,
               "The natives appear to be rather upset by your sacrilege. Can your charisma win them over?",
               "You kneel down and gesticulate wildly, desperately trying to show you meant no harm.\n" + \
               "The natives are hardly pleased but show mercy. They shoo you away but harm you not.",
               "Not knowing their language, you have no chance convincing the natives that you did not want to insult them." + \
               "They start chasing you and throw rocks after you. You barely escape, but get quite beaten up in the process."
          ),
          Task("speed", 10, 5,
               "Run for your life!",
               "The natives start laughing as you dash away back into the jungle. Looking back at the weapons they carry, you reckon yourself lucky.",
               "In the thick jungle you have no chance escaping the natives on their home ground. They catch you and give you the beating of a lifetime."
          )
    ),

    Peril("An avalanche of pebbles has gone down, and now a boulder blocks your way.\n" + \
          "Will you try to thrust away the boulder (yes) or can you think of something more sophisticated (no)?",
          Task(characteristic = "strength",
               cost = 20,
               penalty = 1,
               text = "You roll up the sleeves of your shirt and push against the boulder. Are you strong enough?",
               text_pass = "Going to the gym finally pays off! With a mighty thrust, the obstacle is removed!",
               text_fail = "No way, it's not moving. You exhaust yourself before looking for another way forward..."
          ),
          Task(characteristic = "intelligence",
               cost = 20,
               penalty = 3,
               text = "You try to remember all the episodes of MacGyver you've ever seen. Can you remember a good trick?",
               text_pass = "You remember how to generate hydrogen gas from salty water and scrap metal and use that to build a makeshift mini bomb.\n" + \
                   "It shatters the bouler and frees the path for you.",
               text_fail = "You do remember how to get hydrogen from salty water and scrap metal, but not how easily hydrogen gas explodes.\n" + \
                   "In the detonation, shards of your metal deposit fly around and cut into your flesh, but the boulder does not move a bit."
               )
    )
]

track_length = 2
winners = []
while len(winners) == 0 :
    for player in players :
        if player.skip_turns :
            print(f"{player.name} skips a turn.")
            player.skip_turns -= 1
        else :
            peril = random.choice(perils)
            player.face_peril(peril)

    winners = get_winnners(players, track_length)

if len(winners) == 1 :
    print( winners[0].name, "wins the game!" )
else :
    print( ", ".join(winners[:-1]) )
    print("and", winners[-1], "all arrive at the central artefact at the same time!")
    print("they all win!")
