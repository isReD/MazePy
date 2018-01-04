# -*-coding:Utf-8 -*
""" Ths module contains functions which allow to store the player profile and results
"""
import os
import pickle
from random import choice

scoreFileName="scores"

def loadScores():
    """ This functions load players'scores as a dictionnary from a file (if any).
    """    
    if os.path.exists(scoreFileName): # make sure the file exists
        # Load the file
        scoresFile = open(scoreFileName, "rb")
        scoresDepickler = pickle.Unpickler(scoresFile)
        scores = scoresDepickler.load()
        scoresFile.close()
    else: # If a score sheet is not available, create one
        scores = {} #empty dictionnary
    return scores

def saveScores(scores):
    """This function allows to save the scoresheet of players
    In this basic version of the game: the score is simply defined
    as the number of attempts by the player until exit
    """
    scoresFile = open(scoreFileName, "wb") # Overwrite/update existing results
    scorePickler = pickle.Pickler(scoresFile)
    scorePickler.dump(scores)
    scoresFile.close()

def getPlayer():
    """This functions allows to choose a player profile
    """
    PlayerName = input("Enter your name: ")
    # Typeset      
    if not PlayerName.isalnum() or len(PlayerName)<4:
        print("""Invalid Name - Minimum lenght is 4 
             - Advice: Remember your ID (Case-Sensitive)""")
        # recursive call until a correct name is entered
        return getPlayer()
    else:
        return PlayerName