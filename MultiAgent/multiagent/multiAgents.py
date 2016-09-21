# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
from fractions import Fraction as F
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        foodScore = 1.0
        scaredGhostScore = 0.0
        ghostScore = -1.0
        newFoodList = newFood.asList()
        if newFoodList:
            closestFoodDist = min([util.manhattanDistance(newPos, food) for food in newFoodList])
            if closestFoodDist != 0:
                    foodScore = (1.0 / closestFoodDist)
        if newGhostStates:   
            closestGhostDist = min([util.manhattanDistance(newPos, newGost.getPosition()) for newGost in newGhostStates])
            if closestGhostDist != 0:
                    ghostScore = (1.0 / closestGhostDist)
           
        if  max(newScaredTimes) >= closestGhostDist:
                scaredGhostScore = 1.0
      
        newScore = successorGameState.getScore() + foodScore - ghostScore + scaredGhostScore
        return newScore
    
#         successorGameState = currentGameState.generatePacmanSuccessor(action)
#         newPos = successorGameState.getPacmanPosition()
#         newFood = successorGameState.getFood()
#         newGhostStates = successorGameState.getGhostStates()
#         newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
# 
#     newFoodList = newFood.asList()
#         if newFoodList:
#             closestFoodDist = min([util.manhattanDistance(newPos, food) for food in newFoodList])
#         else:
#             closestFoodDist = 0
# 
#         if newGhostStates:   
#             closestGhostDist = min([util.manhattanDistance(newPos, newGost.getPosition()) for newGost in newGhostStates])
#         else: 
#             closestGhostDist = -1
#            
#     if  max(newScaredTimes) >= closestGhostDist:
#             closestScaredGhostDist = 1.0
#     else:
#             closestScaredGhostDist =  0
#         
#         
#         if closestFoodDist != 0:
#             closestFoodDist = (1.0 / closestFoodDist)
#         else: 
#             closestFoodDist = 1
# 
#         if closestGhostDist != 0:
#             closestGhostDist = (1.0 / closestGhostDist)
#         else: 
#             closestGhostDist = 1
# 
#             
#         newScore = successorGameState.getScore() + closestFoodDist -  closestGhostDist + closestScaredGhostDist
#         return newScore

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        
        def getMaxValue(gameState, depth):
            maxAgentActions = gameState.getLegalActions(0)
            maxVal = float('-inf')
            if depth > self.depth or gameState.isWin() or not maxAgentActions:
                return self.evaluationFunction(gameState)
            else:
                successors = [gameState.generateSuccessor(0, action) for action in maxAgentActions]
                for successor in successors:
                        maxVal = max(maxVal, getMinValue(successor, depth, 1))
                return maxVal 
        
        def getMinValue(gameState, depth, ghostAgentIndex):
            minVal = float('inf')
            minAgentActions = gameState.getLegalActions(ghostAgentIndex)        
            if depth > self.depth or gameState.isLose() or not minAgentActions:
                return self.evaluationFunction(gameState)
            else:
                successors = [gameState.generateSuccessor(ghostAgentIndex, action) for action in minAgentActions]
                for successor in successors:
                    if ghostAgentIndex == gameState.getNumAgents() - 1:
                        minVal = min(minVal, getMaxValue(successor, depth + 1))
                    else:
                        minVal = min(minVal, getMinValue(successor, depth, ghostAgentIndex + 1))
                return minVal
        
        legalMoves = gameState.getLegalActions(0)
        defaultAction = Directions.STOP
        defaultValue = float('-inf')
        for action in legalMoves:
            successor = gameState.generateSuccessor(0, action)
            bestScore = getMinValue(successor, 1, 1)
            if bestScore > defaultValue:
                defaultValue = bestScore
                defaultAction = action
        return defaultAction
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        def getMaxValue(gameState, depth, a, b):
            maxAgentActions = gameState.getLegalActions(0)
            defaultAction = Directions.STOP
            maxVal = float('-inf')
            if depth > self.depth or gameState.isWin() or not maxAgentActions:
                return self.evaluationFunction(gameState), defaultAction
            else:
                for action in maxAgentActions:
                    successor = gameState.generateSuccessor(0, action)
                    tempValue = getMinValue(successor, depth, 1, a, b)[0]
                    if tempValue > maxVal:
                        maxVal = tempValue
                        defaultAction = action
                    if maxVal > b:
                        return maxVal, defaultAction 
                    else:
                        a = max(a, maxVal)
                             
                return maxVal, defaultAction
        
        def getMinValue(gameState, depth, ghostAgentIndex, a, b):
            minVal = float('inf')
            defaultAction = Directions.STOP
            minAgentActions = gameState.getLegalActions(ghostAgentIndex)
                    
            if depth > self.depth or gameState.isLose() or not minAgentActions:
                return self.evaluationFunction(gameState), defaultAction
            else:
                for action in minAgentActions:
                    successor = gameState.generateSuccessor(ghostAgentIndex, action)
                    if ghostAgentIndex == gameState.getNumAgents() - 1:
                        tempValue = getMaxValue(successor, depth + 1, a, b)[0]
                    else:
                        tempValue = getMinValue(successor, depth, ghostAgentIndex + 1, a, b)[0]

                    if tempValue < minVal:
                        minVal = tempValue
                        defaultAction = action
                    if minVal < a:
                        return minVal, defaultAction
                    else:
                        b = min(b, minVal)    
            return minVal, defaultAction
        
        bestScore = getMaxValue(gameState, 1, float('-inf') , float('inf'))
        return bestScore[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        def getMaxValue(gameState, depth):
            maxAgentActions = gameState.getLegalActions(0)
            maxVal = float('-inf')
            if depth > self.depth or gameState.isWin() or not maxAgentActions:
                return self.evaluationFunction(gameState)
            else:
                successors = [gameState.generateSuccessor(0, action) for action in maxAgentActions]
                for successor in successors:
                        maxVal = max(maxVal, getMinValue(successor, depth, 1))
                return maxVal 
        
        def getMinValue(gameState, depth, ghostAgentIndex):
            minAgentActions = gameState.getLegalActions(ghostAgentIndex)        
            if depth > self.depth or gameState.isLose() or not minAgentActions:
                return self.evaluationFunction(gameState)
            else:
                expctVals = 0.0
                len = 0
                successors = [gameState.generateSuccessor(ghostAgentIndex, action) for action in minAgentActions]
                for successor in successors:
                    if ghostAgentIndex == gameState.getNumAgents() - 1:
                        expctVals += getMaxValue(successor, depth + 1)
                        len += 1
                    else:
                        expctVals += getMinValue(successor, depth, ghostAgentIndex + 1)
                        len += 1
                return float(expctVals) / float(len)
        
        legalMoves = gameState.getLegalActions(0)
        defaultAction = Directions.STOP
        defaultValue = float('-inf')
        for action in legalMoves:
            successor = gameState.generateSuccessor(0, action)
            bestScore = getMinValue(successor, 1, 1)
            if bestScore > defaultValue:
                defaultValue = bestScore
                defaultAction = action
        return defaultAction

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      Finding the closest food and ghost and adding the reciprocal of food
      score and subtracting the reciprocal of ghost score from the current score
      Also additional point of 1 if the closest ghost lies within the no.of times
      for which ghost is scared.
      
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    foodScore = 1.0
    scaredGhostScore = 0.0
    ghostScore = -1.0
    newFoodList = newFood.asList()
    if newFoodList:
        closestFoodDist = min([util.manhattanDistance(newPos, food) for food in newFoodList])
        if closestFoodDist != 0:
            foodScore = (1.0 / closestFoodDist)
    if newGhostStates:   
        closestGhostDist = min([util.manhattanDistance(newPos, newGost.getPosition()) for newGost in newGhostStates])
        if closestGhostDist != 0:
                ghostScore = (1.0 / closestGhostDist)
           
    if  max(newScaredTimes) >= closestGhostDist:
            scaredGhostScore = 1.0
      
    newScore = currentGameState.getScore() + foodScore - ghostScore + scaredGhostScore
    return newScore

# Abbreviation
better = betterEvaluationFunction

