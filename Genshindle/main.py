import random
import os
import sys

history = []
cats = ["boss", "region", "vision", "weapon", "version"]
Everything = [["\033[11mName\033[0m", "\033[11mBoss\033[0m", "\033[11mRegion\033[0m", "\033[11mVision\033[0m", "\033[11mWeapon\033[0m", "\033[11mVersion\033[0m"]]

class Character:
    def __init__(self, vision, weapon, region, version, boss):
        self.data = {"region": region, "weapon": weapon, "vision": vision, "boss": boss, "version": version}
    def getVal(self, val, defaultR):
        return self.data.get(val, defaultR)
    def checkType(self, val, curChar):
        return True if self.getVal(val, "Checked 1") == curChar.getVal(val, "Checked 2") else False # differing defaults to prevent False == False

def loadData(filename) -> dict[str, Character]:
    toReturn = {}
    with open(filename, "r") as fl:
        lines = fl.readlines()
        for line in lines:
            line = line.strip()
            name = line.split(":")[0]
            charData = line.split(":")[1].split("-")
            toReturn[name.lower()] = Character(charData[0].lower(), charData[1].lower(), charData[2].lower(), charData[3].lower(), charData[4].lower())
    return toReturn
#VARS
characters = loadData("assets.gns")
defaultCharacter = Character("mondstadt", "sword", "anemo", "dvalin", "0.0")

def logic(toCheck: str, curChar: str, value: str):
    return True if characters.get(toCheck, defaultCharacter).checkType(value, characters.get(curChar)) else False

def coolStrings(txt, col: bool, ver: bool = False, highlow: bool = False):
    if col:
        return f"\033[32m{txt}\033[0m"
    elif not ver:
        return f"\033[31m{txt}\033[0m"
    elif ver:
        if not highlow:
            return f"\033[31m{txt}↑\033[0m"
        else:
            return f"\033[31m{txt}↓\033[0m"



def updateHist(hist, curCharacter):
    global Everything
    for i in hist:
        # if i not in characters.keys():
        if True:
            curCharacterColored = []
            if i.lower() == curCharacter:
                curCharacterColored.append(coolStrings(i, True))
            else:
                curCharacterColored.append(coolStrings(i, False))
            for j in cats:
                if j == "version":
                    curCharacterColored.append(coolStrings(f"{characters.get(i, defaultCharacter).getVal(j, 'error')}", logic(i, curCharacter, j), True, True if characters.get(i, defaultCharacter).getVal("version", "0.0") > characters.get(curCharacter, defaultCharacter).getVal("version", "0.0") else False))
                else:
                    curCharacterColored.append(coolStrings(f"{characters.get(i, defaultCharacter).getVal(j, 'error')}", logic(i, curCharacter, j)))
            Everything.append(curCharacterColored)


def getNewChar():
    return random.choice([k for k, _ in characters.items()])

def lister():
    reset = "\033[0m"
    charRegions = {"mondstadt": [], "liyue": [], "inazuma": [], "sumeru": [], "fontaine": [], "natlan": [], "snezhnaya": []}
    for n, c in characters.items():
        color = "\033[0m"
        weapon = f"[{c.getVal('weapon', 'sword')}]"

        match c.getVal("vision", "anemo"):
            case "anemo":
                color = "\033[1;37m"
            case "cryo":
                color = "\033[0;36m"
            case "hydro":
                color = "\033[0;34m"
            case "electro":
                color = "\033[0;35m"
            case "geo":
                color = "\033[1;33m"
            case "dendro":
                color = "\033[0;32m"
            case "pyro":
                color = "\033[1;31m"
        match c.getVal("region", "mondstadt"):
            case "mondstadt":
                charRegions["mondstadt"].append(f"{color}{n}{weapon}{reset}")
            case "liyue":
                charRegions["liyue"].append(f"{color}{n}{weapon}{reset}")
            case "inazuma":
                charRegions["inazuma"].append(f"{color}{n}{weapon}{reset}")
            case "sumeru":
                charRegions["sumeru"].append(f"{color}{n}{weapon}{reset}")
            case "fontaine":
                charRegions["fontaine"].append(f"{color}{n}{weapon}{reset}")
            case "natlan":
                charRegions["natlan"].append(f"{color}{n}{weapon}{reset}")
            case "snezhnaya":
                charRegions["snezhnaya"].append(f"{color}{n}{weapon}{reset}")
    for n, v in charRegions.items():
        print(f"{reset}{n.upper()}: ")
        for i in v:
            print(i, sep="", end="  ", flush=True)
        print("\n")

def printer():
    global Everything
    try:
        if sys.platform.lower() == "linux" or sys.platform.lower() == "darwin":
            os.system("clear")
        else:
            os.system("cls")

    except:
        print("Unable to clear console :(")

    for row in Everything:
        print('\033[0m| {:^24} | {:^24} | {:^24} | {:^24} | {:^24} | {:^24} |'.format(*row))

def reset(h):
    global Everything, history, score
    if h:
        history = []
    Everything = [["\033[11mName\033[0m", "\033[11mBoss\033[0m", "\033[11mRegion\033[0m", "\033[11mVision\033[0m", "\033[11mWeapon\033[0m", "\033[11mVersion\033[0m"]]

def main(selectedChar):
    global win, lose
    round = 1
    while (inp := input(f"\033[36mGuess a Character({round}/5): ").lower()) != "exit":
        # print(inp)
        reset(False)
        if inp.lower() == "list":
            lister()
            continue
        if inp.lower() in characters.keys():
            history.append(inp)
        else:
            print("\033[31mInvalid Character!\033[0m")
            continue
        updateHist(history, selectedChar)
        printer()
        if inp.lower() == selectedChar: #wins
            print(f"\033[35mYou won the game in {round} rounds!")
            win += 1
            break
        if round >= 5:
            print(f"\033[34mYou lost the game! The character was {selectedChar}")
            lose += 1
            break
        round += 1
    reset(True)

finished = False
win, lose = 0, 0
while not finished:
    main(getNewChar())
    if (pa := input("Play again(Y/N)?: ").lower()) == "n":
        finished = True
    elif pa == "y":
        continue
    else:
        print("\033[31mInvalid Option!")
        break
print(f"\033[35mYou won {win} rounds and lost {lose} rounds!\033[0m")
