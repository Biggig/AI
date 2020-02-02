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
import copy
import types




class node:
    def __init__(self, state, res, cost, f):
        self.state = state
        self.res = list(res)
        self.cost = cost
        self.f = f

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
    ##  run:      python pacman.py -l tinyMaze -p SearchAgent
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    n = Directions.NORTH
    e = Directions.EAST

    start = problem.getStartState()
    def myDFS(location, res, direction):
    	if problem.isGoalState(location):
    		return True
    	successors = problem.getSuccessors(location)
    	for nextLoc in successors:
    		pos = nextLoc[0]
    		val = pos[0] * 10 + pos[1]
    		if val in marked:
    			continue
    		else:
    			marked[val] = 1
    		res.append(nextLoc[1])
    		if myDFS(pos, res, nextLoc[1]):
    			return True

    	if direction != None:
    		if direction == s:
	    		res.append(n)
	    	elif direction == n:
	    		res.append(s)
	    	elif direction == e:
	    		res.append(w)
	    	else:
	    		res.append(e)
    	return False

    res = []
    marked = {}
    marked[start[0] * 10 + start[1]] = 1
    if myDFS(start, res, None):
   		print("reach goal")
    print(res)
    return res
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    start = problem.getStartState()
    allNode = []
    allNode.append(node(start, [], 0, heuristic(start, problem)))
    start = allNode[0]
    marked_ = []

    def cur_aStarSearch(point, cost, marked_):
        pos = point.state
        if len(pos) == 1:
            marked_.append(pos)
        else:
            if isinstance(pos[1], list):
                num = pos[1].count(True)
                marked_.append((pos[0], num))           
            else:
                marked_.append(pos)  # marked

        if problem.isGoalState(pos):
            return point.res

        suc = problem.getSuccessors(pos)

        if problem.isGoalState(pos):
            return point.res
        for sta in suc:
            pos_ = sta[0]

            if len(pos_) == 1:
                pos_ = pos_
            else:
                if isinstance(pos_[1], list):
                    num = pos_[1].count(True)
                    pos_ = (pos_[0], num)
                else:
                    pos_ = pos_

            cost_ = sta[2] + cost  # total cost
            if pos_ not in marked_:
                res_ = []
                res_ = list(point.res)
                res_.append(sta[1])
                point_ = node(sta[0], res_, cost_,
                              cost_ + heuristic(sta[0], problem))
                existed = False
                for m in allNode:
                    if point_.state == m.state:
                        existed = True
                        if point_.f < m.f:
                            m.res = list(point_.res)
                            m.cost = point_.cost
                            m.f = point_.f
                if not existed:
                    allNode.append(point_)


        min_ = 10000
        next_node = []
        end = True
        for m in allNode:
            position = m.state

            if len(position) == 1:
                position = position
            else:
                if isinstance(position[1], list):
                    num = position[1].count(True)
                    position = (position[0], num)                   
                else:
                    position = position

            if position not in marked_:
                if m.f < min_:
                    end = False
                    min_ = m.f
                    next_node = node(m.state, m.res, m.cost, m.f)
        if not end:
            return cur_aStarSearch(next_node, next_node.cost, marked_)
        else:
            return None
    all_res = []
    all_res = list(cur_aStarSearch(start, 0, marked_))
    return all_res
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch



