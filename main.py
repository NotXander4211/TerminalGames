import os
games = ["Genshindle"]
print("Welcome to the Game Launcher!")
for c, i in enumerate(games):
    print(f"{c}: {i}")
play = int(input("Which game would you like to play: "))
if play < len(games):
    os.system("cls")
    print(f"Starting {games[play]}...")
    print(f"PLAYING {games[play].upper()}\n\n")
    os.system(f"python ./{games[play]}/main.py")
else:
    print("Invalid game.")
