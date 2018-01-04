# -*-coding:Utf-8 -*
""" This module contains several classes related to the maze appearance and behaviour """

import os
import pickle


#####################################################################################################################
######## ROBOT AND OBSTACLES
#####################################################################################################################

#class#
class Robot:
    "This class defines the object/robot which moves in the maze"
    
    name = "robot"
    symbol ="X"
      
    def __init__(self, x, y):
        # (x,y) defines the position of the robot
        self.x = x  
        self.y = y

    def __repr__(self):
        return "<Robot x={} y={}>".format(self.x, self.y)

    def __str__(self):
        return "Robot {}.{}".format(self.x, self.y)


#class#
class Obstacle:
    """ This class defines generic obstacle properties  
    name: the name of the obstacle
    symbol: each obstacle is defined by a special character as defined in the specifications
    canGo: a boolean which specify whether the robot can go trhough a an obstacle (ie if the obstacle is a door or a wall)
    ex: obstacle.canGo=True means the obstacle can be crossed 
    """
    name = "obstacle"
    symbol =" "
    canGo = True #by default we assume any obstacle can be crossed/passed
   
    def __init__(self, x, y):
        # (x,y) defines the position of the obstacle
        self.x = x  
        self.y = y

    def __repr__(self):
        return "<{name} (x={x}, y={y})>".format(name=self.name, x=self.x, y=self.y)

    def __str__(self):
        return "{name} ({x}.{y})".format(name=self.name, x=self.x, y=self.y)


#class#
class Wall(Obstacle):
    "This class defines a wall in the maze's map"
    name = "wall"
    symbol ="O"
    canGo = False #The wall cannot be crossed over by the robot

#class#
class Door(Obstacle):
    "This class defines an opened door/gate "
    name = "Door"
    symbol ="."
    canGo = True #The robot can always go through this door

#class#
class Exit(Obstacle):
    "This class defines the exit (the end of the game)" 
    name = "Exit"
    symbol ="U"
    canGo = True #The robot can go through the exit when it reaches 

    def out(self):                
        print("The robot is OUT \n")
       
        

#####################################################################################################################
######## MAP PROPERTIES
#####################################################################################################################

class Map:
    """ This class creates/loads a map from file """  

    def __init__(self, name, gridMap):
        self.name=name
        self.grid=self.createGrid(gridMap)          
        self.robot=Robot(self.grid[0][0],self.grid[0][1])       
        self.hidden = []
        self.solved = False

    def __repr__(self):
        return "map <{}".format(self.name)


    def createGrid(self,gridMap):       
        """a function which creates a map from a list of characters:    
        the map gives the positions of the obstacles and the robot
        "0": Wall | "X":Robot | ".": Door | "U": Exit  """     
        obstaclesClasses= {"O":Wall,
                           "X":Robot,
                           ".":Door,
                           "U":Exit}
        # initialization of cursors and containers to read through the gridMap and store values
        curX = 0
        curY = 0
        robot = None
        obstacles = []        
        
        newLine=0
        for symbol in gridMap:         
            if symbol is "\n":
                newLine+=1

                curX=0 
                curY+=1
                continue
            
            elif symbol==" ":
                pass          
            elif symbol in gridMap:
                # identify the type of symbol-symbol from the predefined list 
                obtacleType=obstaclesClasses[symbol]  # wall, robot, door or exit                
                #create a new instance of the obstacle type recognized
                obstacleFound=obtacleType(curX,curY) #get the actual obstacle position              
                #
                if type(obstacleFound) is Robot:
                    if robot:
                        raise ValueError("Only one robot is allowed")
                    #overwrite existing value of robot if any
                    robot = obstacleFound
                else:
                    obstacles.append(obstacleFound)
            else:
                raise ValueError("Undefined obstacle {}".format(symbol))
            curX += 1            
            max_x=newLine
            max_y = curY
            self.max_x = newLine
            self.max_y = curY        

        #create/update the final grid the map
        #the grid holds the position of the robot and the obstacles, as follows   
        ObstaclesMap={}
        for obstacle in obstacles:
            if (obstacle.x, obstacle.y) in ObstaclesMap:
                raise ValueError("This object is already added to the grid x={} y={}".format(obstacle.x,obstacle.y))
            if obstacle.x > self.max_y or obstacle.y > self.max_y:
                raise ValueError("Error - Obstacle out of box ".format(obstacle))
            ObstaclesMap[(obstacle.x, obstacle.y)] = obstacle
        #add the robot to the grid        
        self.grid=[(robot.x,robot.y),ObstaclesMap.copy()]    
        return self.grid


    def displayGrid(self):
        print("\n")
        """Display the maze in the console.
        In a future version pygame will be used to design a gui 
        """ 
        obstacles = self.grid[1] 
        obstacles[(self.grid[0][0],self.grid[0][1])]=self.robot
              
        gridDisplay=""
        #remember grid is a list and contains the robot at index 0, followed by a dictionnary of obstacles at index 1
        y=0 #new line
        while y < self.max_y: 
            x = 0 #new column
            while x < self.max_x:              
                pos = obstacles.get((x, y))              
                if pos and str(pos) != " ":                    
                    gridDisplay += pos.symbol
                else:
                    gridDisplay += " "
                x += 1
            gridDisplay += "\n"
            y += 1
        print(gridDisplay, end="")
        print("\n")


    def displayGrid2(self,gridMap):
        """Display the maze in the console.
        In a future version, we will learn/use pygame library for a better UI display
        """    
        print(gridMap)       

        
    def updateGrid(self):
        """This methods allows to refresh the grid"""        
        for obstacle in list(self.hidden):
            print(list(self.hidden))
            if (obstacle.x, obstacle.y) not in (self.grid[1]):#check by key, note that the key is a tupe (x,y) of the obstacle
                self.grid[1][obstacle.x, obstacle.y] = obstacle
                self.hidden.remove(obstacle)


    def moveRobot(self, direction, steps):
        """This method allows to move the robot"""
        robot = self.robot        
        coords = [robot.x, robot.y]
        if direction == "north":# haut 
            coords[1] -= steps
        elif direction == "east":# droite
            coords[0] += steps
        elif direction == "south":# bas
            coords[1] += steps
        elif direction == "west": # gauche
            coords[0] -= steps
        else:
            raise ValueError("Unknow {} direction".format(direction))       
       
       #robot coordinates
        x, y = coords
        if x >= 0 and x < self.max_x and y >= 0 and y < self.max_y:
            # attempt to move the robot
            # Make sure there is no obstacle on the road
            obstacle = (self.grid[1]).get((x, y))           
            if obstacle is None or obstacle.canGo:
                
                if obstacle:
                    self.hidden.append(obstacle)
                # Delete old robot position               
                del self.grid[1][(robot.x, robot.y)]
                # Update robot position
                self.robot=Robot(x,y)
                self.grid[0]=(self.robot.x,self.robot.y);
                          
            if type(obstacle) is Wall:
                print("Warning: impossible move - There is an obstacle")
                print(obstacle)

            # call the exit function if it applies (if the robot is in the exit position)
            if type(obstacle) is Exit:
                obstacle.out()
                self.solved=True
                self.endGame()

            #correct move
            return True

        else:
            print("Warning: wrong move - Out of bundaries")
            #wrong move (not counted)
            return False
        
        self.updateGrid()
        self.displayGrid()


    def endGame(self):
        """This method ends the game and saves the scores (if any)"""
        if self.solved is True:
            print("Congratulation! You solved the maze!")