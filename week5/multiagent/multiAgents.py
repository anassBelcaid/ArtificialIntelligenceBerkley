# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import numpy as np   #have to use the unrefutable package
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
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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

        "*** YOUR CODE HERE ***"
        ###########################
        #  Put your featurs here  #
        ###########################
        
        #remaining food
        remFood = len(newFood.asList())
        ghostsDist= np.array([manhattanDistance(newPos, gost.getPosition())
            for gost in newGhostStates])
        foodDist = np.array([manhattanDistance(newPos,food) for food in
            newFood.asList()])

        # is a ghost close
        distGhost= 1 if( np.min(ghostsDist)<=2) else 0
        minFood = np.min(foodDist)+0.001 if (len(foodDist)>0) else 0.001;


        #vector of features
        features = np.array([successorGameState.getScore() ,
            remFood, distGhost,1/minFood])

        #coefficient
        coef = np.array([1,-40,-40000,1])

        score  = np.sum(features*coef)

        return score
        

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
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
        #num agents
        num_agents = gameState.getNumAgents()

        #possible actions
        actions = gameState.getLegalActions(0)

        scores=np.array([self.gameValue(gameState.generateSuccessor(0,action),1,self.depth)
                for action in actions] )

        return actions[np.argmax(scores)]
         

    def gameValue(self,state,agentIndex,depth):
        """
        compute the game value of an agent indexed by agentIndex
        """

        #basic case
        if(state.isLose() or state.isWin()):
            return self.evaluationFunction(state)

        if(depth==0):
            return self.evaluationFunction(state)

        #common actions (independant of agent)
        actions =state.getLegalActions(agentIndex)
        states = [state.generateSuccessor(agentIndex,action) for action in
                actions]
        num_ghosts=state.getNumAgents()

        #pacman case
        if(agentIndex==0):
            return max([self.gameValue(St,1,depth) for St in states])
        #ghost but not the last one
        elif(agentIndex<num_ghosts-1):
            return min([self.gameValue(St,agentIndex+1,depth) for St in states])
        else:
            return min([self.gameValue(St,0,depth-1) for St in states])


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #num agents
        num_agents = gameState.getNumAgents()

        #alpha beta values
        alpha,beta = -np.inf, np.inf

        #possible actions
        actions = gameState.getLegalActions(0) 

        #max val
        maxVal=-np.inf
        bestAction = None
        depth=self.depth

        for action in actions:
            #evaluate the sate for this action
            state=gameState.generateSuccessor(0,action)
            V = self.min_value(state,1,depth,alpha,beta)
            if(V>maxVal):
                maxVal,bestAction=V,action
            if(beta<alpha):
                break
            alpha=max(alpha,maxVal)
        return bestAction

    def max_value(self,state,depth,alpha,beta):
        """
        max value for Pacman
        """
        
        #terminal state
        if(depth==0 or state.isWin() or state.isLose()):
            return self.evaluationFunction(state)

        #loop over the actions
        max_val=-np.inf
        actions=state.getLegalActions(0) 

        for action in actions:
            newState=state.generateSuccessor(0,action)
            max_val=max(max_val,self.min_value(newState,1,depth,alpha,beta))
            #beta pruning
            if( max_val>beta):
                return max_val

            alpha=max(alpha,max_val)
        return max_val

    def min_value(self,state,agent,depth,alpha,beta):
        """
        max value for Pacman
        """
        
        #terminal state
        if(depth==0 or state.isWin() or state.isLose()):
            return self.evaluationFunction(state)

        num_agents=state.getNumAgents()
        nextAgent= agent+1 if(agent<num_agents-1) else 0
        #loop over the actions
        min_val=np.inf
        actions=state.getLegalActions(agent) 

        for action in actions:
            newState=state.generateSuccessor(agent,action)
            #check if next agent is pacman
            if(nextAgent==0):
                min_val=min(min_val,self.max_value(newState,depth-1,alpha,beta))
            else:
                min_val=min(min_val,self.min_value(newState,nextAgent,depth,alpha,beta))
            #alpha pruning
            if(min_val<alpha):
                return min_val
            beta=min(beta,min_val)
        return min_val

            



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
        "*** YOUR CODE HERE ***"
        #num agents
        num_agents = gameState.getNumAgents()

        #possible actions
        actions = gameState.getLegalActions(0)

        scores=np.array([self.gameValue(gameState.generateSuccessor(0,action),1,self.depth)
                for action in actions] )

        return actions[np.argmax(scores)]
    
    def gameValue(self,state,agentIndex,depth):
        """
        compute the game value of an agent indexed by agentIndex
        """

        #basic case
        if(state.isLose() or state.isWin()):
            return self.evaluationFunction(state)

        if(depth==0):
            return self.evaluationFunction(state)

        #common actions (independant of agent)
        actions =state.getLegalActions(agentIndex)
        states = [state.generateSuccessor(agentIndex,action) for action in
                actions]
        num_ghosts=state.getNumAgents()

        #pacman case
        if(agentIndex==0):
            return np.max(np.array([self.gameValue(St,1,depth) for St in
                states]))
        #ghost but not the last one
        elif(agentIndex<num_ghosts-1):
            return np.mean(np.array([self.gameValue(St,agentIndex+1,depth) for
                St in states]))
        else:
            return np.mean(np.array([self.gameValue(St,0,depth-1) for St in
                states]))

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    # Useful information you can extract from a GameState (pacman.py)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    #remaining food
    remFood = len(newFood.asList())
    ghostsDist= np.array([manhattanDistance(newPos, gost.getPosition()) for gost in newGhostStates])
    foodDist = np.array([manhattanDistance(newPos,food) for food in newFood.asList()])

    # is a ghost close
    distGhost= 1 if( np.min(ghostsDist)<=1) else 0
    minFood = np.min(foodDist)+0.001 if (len(foodDist)>0) else 0.001;


    #vector of features
    features = np.array([currentGameState.getScore() ,remFood, distGhost,1/minFood])

    #coefficient
    coef = np.array([1,-40,-400,1])

    score  = np.sum(features*coef)

    return score

# Abbreviation
better = betterEvaluationFunction

