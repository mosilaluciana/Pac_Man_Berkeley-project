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
from Node import Node
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
    def getSuccessorActionCost(self,successor, action, stepCost, list):
        successor = list[0][0]
        action = list[0][1]
        stepCost = list[0][2]
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

def depthFirstSearch(problem: SearchProblem):
    stackDFS = util.Stack()
    state = Node(problem.getStartState(), [], 0)
    stackDFS.push(state)

    visited = set()

    while not stackDFS.isEmpty():
        current_node = stackDFS.pop()

        current_state = current_node.state
        actions = current_node.actions
        cost = current_node.cost

        if current_state in visited:
            continue

        visited.add(current_state)

        if problem.isGoalState(current_state):
            return actions

        for successor_state, action, step_cost in problem.getSuccessors(current_state):
            if successor_state not in visited:
                next_node = Node(successor_state, actions + [action], cost + step_cost)
                stackDFS.push(next_node)

    return []


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    stackBFS = util.Queue()
    state = Node(problem.getStartState(), [], 0)
    stackBFS.push(state)
    visited = set()

    while not stackBFS.isEmpty():
        current_node = stackBFS.pop()

        current_state = current_node.state
        actions = current_node.actions
        cost = current_node.cost

        if current_state in visited:
            continue

        visited.add(current_state)

        if problem.isGoalState(current_state):
            return actions

        for next_state, next_action, added_cost in problem.getSuccessors(current_state):
            if next_state not in visited:
                next_node = Node(next_state, actions + [next_action], cost + added_cost)
                stackBFS.push(next_node)

    return []
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    priorityQueue = util.PriorityQueue()
    startState = problem.getStartState()
    start_node = Node(startState, [], 0)
    priorityQueue.push(start_node, 0)

    visited = set()

    while not priorityQueue.isEmpty():
        current_node = priorityQueue.pop()

        current_state = current_node.state
        actions = current_node.actions
        cost = current_node.cost

        if current_state in visited:
            continue

        visited.add(current_state)

        if problem.isGoalState(current_state):
            return actions

        for next_state, next_action, added_cost in problem.getSuccessors(current_state):
            if next_state not in visited:
                next_cost = cost + added_cost
                next_node = Node(next_state, actions + [next_action], next_cost)
                priorityQueue.push(next_node, next_cost)

    return []
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    priorityQueue = util.PriorityQueue()
    startState = problem.getStartState()
    start_node = Node(startState, [], 0)
    priorityQueue.push(start_node, 0 + heuristic(startState, problem))

    visited = set()

    while not priorityQueue.isEmpty():
        current_node = priorityQueue.pop()

        current_state = current_node.state
        actions = current_node.actions
        cost = current_node.cost
        if current_state in visited:
            continue

        visited.add(current_state)

        if problem.isGoalState(current_state):
            return actions

        for next_state, next_action, added_cost in problem.getSuccessors(current_state):
            if next_state not in visited:
                next_cost = cost + added_cost
                priority = next_cost + heuristic(next_state, problem)
                next_node = Node(next_state, actions + [next_action], next_cost)
                priorityQueue.push(next_node, priority)

    return []
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
