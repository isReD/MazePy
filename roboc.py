
# -*-coding:Utf-8 -*
"""This file is the entry point of the maze game"""
import os
from maze import *
from player import *

###################################################################################
# Load existing maps
maps = []
gridMaps =[]
for fileName in os.listdir("maps"):    
    if fileName.endswith(".txt"):
        pathFile = os.path.join("maps", fileName)       
        mapName = fileName[:-4].lower()        
        with open(pathFile, "r") as activeFile:
            gridMap = activeFile.read()   
            gridMaps.append(gridMap);            
            try:
                map = Map(mapName, str(gridMap))
            except ValueError as err:
                print("Unable to read specified file {} : {}.".format(pathFile, str(err)))
            else:
                maps.append(map)	                
##################################################################################


##################################################################################
newGame=True
mazeOn=False
# Load scoresheet/player profile
print("====================================================================")
print("""Hello welcome to the basic maze game.
>> To start, enter your pseudonym """)
scores=loadScores()
# Get player name
# Check whether there is an active game for the current player
player = getPlayer()
if player in scores.keys():
    
    if int(scores[player][1]) > 0 and scores[player][0].solved==False:
        turns=int(scores[player][1])
        print("====================================================================")
        print("\n Hey {} - you have an active maze to finish".format(player))
        print("Your score is: {}".format(int(scores[player][1])))
        print("Do you want to continue or restart? (Y or any key to continue - N for new game)")
        answer = input(">> ")
        if answer.lower() == "n":
            newGame=True
            mazeOn=False                   
        else:#start a new game
            newGame=False
            mazeOn=True 

    if int(scores[player][1]) > 0 and scores[player][0].solved==True:
        print("\n Hey {} - no active maze - Start a new game \n".format(player))
        turns=0
            
else:   
    print("\n --- Welcome {} (new player) \n".format(player))
    scores[player]=["",str(0)]
    turns=0
##################################################################################



##################################################################################
while newGame==True and mazeOn==False:
    # Show Existing Maps/Levels 
    print("Existing Maps :")
    for i, map in enumerate(maps):
        print("{} - {}".format(i + 1, map.name))
    
    # Level selection (the user selects a map)
    if mazeOn is False:
        level = input("\n Choose the map (difficulty level) to start: ")        
        try:
            level = int(level) # expecting a number
        except ValueError:
            print("Wrong value : {}".format(level))
        else:
            if level < 1 or level > len(maps):
                print("Wrong value: ".format(choice))
                continue
            map = maps[level - 1]
            mazeOn=True;

if newGame==False and mazeOn==True:
    #load the active map
    map = scores[player][0]
         
#display the map
map.displayGrid(); 
##################################################################################


##################################################################################
#Display the maze and play the game
while not map.solved:
    move = input("move ==> ")
    if move == "":
        continue
    elif move.lower() == "q":
        # exit
        break
    elif move[0].lower() in "nseo": #nsew = north_south_east_west
        moveType = move[0].lower()
        if moveType == "e":
            direction = "east"
        elif moveType == "s":
            direction = "south"
        elif moveType == "o":
            direction = "west"
        else:# 
            direction = "north"
        # Apply the move 
        steps = move[1:]
        if steps == "":
            steps = 1
        else:
            try:
                steps = int(steps)
            except ValueError:
                print("Invalid Number: {}".format(steps))
                continue
        turns+=1
        scores[player]=[map,str(turns)]               
        map.moveRobot(direction, steps)
        map.displayGrid();  
        saveScores(scores)  
        print("-------------------")
        print("Your current score is {} \n".format(int(scores[player][1])) )
       

    else:
        print("Allowed keys :")
        print("  Q to exit the game")
        print("  E to move the robot to the east (right)")
        print("  O to move the robot to the west (left)")
        print("  N to move the robot to the north (up)")
        print("  S to move the robot to the south (down)")
        print("Cue: Type Xn to move the robot n times in X direction (X in {NSEO})")