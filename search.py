# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html


#Hampton Terry
#4-19-2013
#CSE 473
#Homework 1
"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
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
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"
  from game import Directions
  startState = problem.getStartState()

  #nodes waiting to be visited  
  nodes = util.Stack()
  
  #nodes we have already visited
  visited = set([startState])
  
  #Used to keep track of known path between nodes
  path = {}
  
  #start case
  if(not problem.isGoalState(problem.getStartState())):
    successors = problem.getSuccessors(startState)
    for successor in successors:
	  util.Stack.push(nodes, successor)    
	  path[successor] = startState

  #depthFirstSearch case
  currentNode = util.Stack.pop(nodes);
  while (not problem.isGoalState(currentNode[0])): #TODO empty stack case
    if not currentNode[0] in visited:
    	successors = problem.getSuccessors(currentNode[0])
        for successor in successors:
          util.Stack.push(nodes, successor)  
          path[successor] = currentNode
        visited.add(currentNode[0])
    currentNode = util.Stack.pop(nodes)
  
  #find path from end node to start
  directions = [currentNode[1]]
  while not (path[currentNode] == startState):
    directions.append(path[currentNode][1])
    currentNode = path[currentNode]
  
  s = Directions.SOUTH
  w = Directions.WEST
  e = Directions.EAST
  n = Directions.NORTH
  
  #Convert Strings into enum values
  for i in range(len(directions)):
    dir = directions[i]
    if dir == 'North':
	  directions[i] = n
    elif dir == 'East':
	  directions[i] = e
    elif dir == 'South':
	  directions[i] = s
    else: #West
	  directions[i] = w
	  
  #Need to reverse list to give directions from start to end	  
  return directions[::-1]  

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  "*** YOUR CODE HERE ***"
  from game import Directions
  startState = problem.getStartState()

  #nodes waiting to be visited  
  nodes = util.Stack()
  
  #nodes we have already visited
  visited = set([startState])
  
  #Used to keep track of known path between nodes
  path = {}
  
  #start case
  if(not problem.isGoalState(problem.getStartState())):
    successors = problem.getSuccessors(startState)
    for successor in successors:
	  util.Stack.push(nodes, successor)    
	  path[successor] = startState

  #depthFirstSearch case
  currentNode = util.Stack.pop(nodes);
  while (not problem.isGoalState(currentNode[0])): #TODO empty stack case
    if not currentNode[0] in visited:
    	successors = problem.getSuccessors(currentNode[0])
        for successor in successors:
          util.Stack.push(nodes, successor)  
          path[successor] = currentNode
        visited.add(currentNode[0])
    currentNode = util.Stack.pop(nodes)
  
  #find path from end node to start
  directions = [currentNode[1]]
  while not (path[currentNode] == startState):
    directions.append(path[currentNode][1])
    currentNode = path[currentNode]
  
  s = Directions.SOUTH
  w = Directions.WEST
  e = Directions.EAST
  n = Directions.NORTH
  
  #Convert Strings into enum values
  for i in range(len(directions)):
    dir = directions[i]
    if dir == 'North':
	  directions[i] = n
    elif dir == 'East':
	  directions[i] = e
    elif dir == 'South':
	  directions[i] = s
    else: #West
	  directions[i] = w
	  
  #Need to reverse list to give directions from start to end	  
  return directions[::-1]  
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  from game import Directions
  startState = problem.getStartState()

  #nodes waiting to be visited  
  nodes = util.PriorityQueue()
  
  #nodes we have already visited
  visited = set([startState])
  
  #Used to keep track of known path between nodes
  path = {}
  
  #start case
  if(not problem.isGoalState(problem.getStartState())):
    successors = problem.getSuccessors(startState)
    for successor in successors:
	  priority = successor[2]
	  util.PriorityQueue.push(nodes, successor, priority)    
	  path[successor] = startState

  #depthFirstSearch case
  currentNode = util.PriorityQueue.pop(nodes);
  while (not problem.isGoalState(currentNode[0])): #TODO empty stack case
    if not currentNode[0] in visited:
    	successors = problem.getSuccessors(currentNode[0])
        for successor in successors:
          priority = currentNode[2] + successor[2]
          util.PriorityQueue.push(nodes, successor, priority)  
          path[successor] = currentNode
        visited.add(currentNode[0])
    currentNode = util.PriorityQueue.pop(nodes)
  
  #find path from end node to start
  directions = [currentNode[1]]
  while not (path[currentNode] == startState):
    directions.append(path[currentNode][1])
    currentNode = path[currentNode]
  
  s = Directions.SOUTH
  w = Directions.WEST
  e = Directions.EAST
  n = Directions.NORTH
  
  #Convert Strings into enum values
  for i in range(len(directions)):
    dir = directions[i]
    if dir == 'North':
	  directions[i] = n
    elif dir == 'East':
	  directions[i] = e
    elif dir == 'South':
	  directions[i] = s
    else: #West
	  directions[i] = w
	  
  #Need to reverse list to give directions from start to end	  
  return directions[::-1]  

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  from game import Directions
  startState = problem.getStartState()

  #nodes waiting to be visited  
  nodes = util.PriorityQueue()
  
  #nodes we have already visited
  visited = set([startState])
  
  #Used to keep track of known path between nodes
  path = {}
  
  #start case
  if(not problem.isGoalState(problem.getStartState())):
    successors = problem.getSuccessors(startState)
    for successor in successors:
	  priority = successor[2] + heuristic(successor[0], problem);
	  util.PriorityQueue.push(nodes, successor, priority)    
	  path[successor] = startState

  #depthFirstSearch case
  currentNode = util.PriorityQueue.pop(nodes);
  while (not problem.isGoalState(currentNode[0])): #TODO empty stack case  
    if not currentNode[0] in visited:
    	successors = problem.getSuccessors(currentNode[0])
        for successor in successors:
          priority = currentNode[2] + successor[2] + heuristic(successor[0], problem)
          util.PriorityQueue.push(nodes, successor, priority)  
          print "push", successor[0], " ", heuristic(successor[0], problem)  
          path[successor] = currentNode
        visited.add(currentNode[0])
    currentNode = util.PriorityQueue.pop(nodes)
  
  #find path from end node to start
  directions = [currentNode[1]]
  while not (path[currentNode] == startState):
    directions.append(path[currentNode][1])
    currentNode = path[currentNode]
  
  s = Directions.SOUTH
  w = Directions.WEST
  e = Directions.EAST
  n = Directions.NORTH
  
  #Convert Strings into enum values
  for i in range(len(directions)):
    dir = directions[i]
    if dir == 'North':
	  directions[i] = n
    elif dir == 'East':
	  directions[i] = e
    elif dir == 'South':
	  directions[i] = s
    else: #West
	  directions[i] = w
	  
  #Need to reverse list to give directions from start to end	  
  return directions[::-1]  
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch