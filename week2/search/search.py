# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    #starting position
    state = problem.getStartState()

    #fringe
    fringe = util.Stack()
    path=[]  #empty path
    fringe.push((state,path))

    #closed set
    closed=set()

    # Visited set
    found= False # booleen to represent if the goal is pop from the fring

    #main loop, we loop until the fring is empty
    while(not fringe.isEmpty()):
        #current state
        current,path = fringe.pop()

        #if the node is goal declare success
        if(problem.isGoalState(current)):
            return path

        #if not expand the node is (not in the closed set)
        if( not current in closed):
            #Expand the node by adding the path and the state on the fringe
            for state,action,cost in problem.getSuccessors(current):
                fringe.push((state,path+[action]))
            #put the node on the closed set
            closed.add(current)
    
    #if empty return none path
    return None
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #starting position
    state = problem.getStartState()

    #fringe
    fringe = util.Queue()
    path=[]  #empty path
    fringe.push((state,path))

    #closed set
    closed=set()

    # Visited set
    found= False # booleen to represent if the goal is pop from the fring

    #main loop, we loop until the fring is empty
    while(not fringe.isEmpty()):
        #current state
        current,path = fringe.pop()

        #if the node is goal declare success
        if(problem.isGoalState(current)):
            return path

        #if not expand the node is (not in the closed set)
        if( not current in closed):
            #Expand the node by adding the path and the state on the fringe
            for state,action,cost in problem.getSuccessors(current):
                fringe.push((state,path+[action]))
            #put the node on the closed set
            closed.add(current)
    
    #if empty return none path
    return None

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    #starting position
    state = problem.getStartState()

    #fringe
    fringe = util.PriorityQueue()
    path=[]  #empty path
    fringe.push((state,path,0),0)

    #closed set
    closed=set()

    # Visited set
    found= False # booleen to represent if the goal is pop from the fring

    #main loop, we loop until the fring is empty
    while(not fringe.isEmpty()):
        #current state
        current,path,nodeCost= fringe.pop()

        #if the node is goal declare success
        if(problem.isGoalState(current)):
            return path

        #if not expand the node is (not in the closed set)
        if( not current in closed):
            #Expand the node by adding the path and the state on the fringe
            for state,action,cost in problem.getSuccessors(current):
                fringe.push((state,path+[action],nodeCost+cost),nodeCost+cost)
            #put the node on the closed set
            closed.add(current)
    
    #if empty return none path
    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #starting position
    state = problem.getStartState()

    #fringe
    fringe = util.PriorityQueue()
    path=[]  #empty path
    h0=heuristic(state,problem)
    fringe.push((state,path,h0),h0)

    #closed set
    closed=set()


    #main loop, we loop until the fring is empty
    while(not fringe.isEmpty()):
        #current state
        current,path,nodeCost= fringe.pop()

        #if the node is goal declare success
        if(problem.isGoalState(current)):
            return path

        #if not expand the node is (not in the closed set)
        if( not current in closed):
            #Expand the node by adding the path and the state on the fringe
            for state,action,cost in problem.getSuccessors(current):
                #cost on the node
                C=nodeCost+cost+heuristic(state,problem)-heuristic(current,problem)
                fringe.push((state,path+[action],C),C)
            #put the node on the closed set
            closed.add(current)
    
    #if empty return none path
    return None


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
