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
import random, util

from game import Agent
from pacman import GameState


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        successorGameState = currentGameState.generatePacmanSuccessor(
            action)  # generează starea urmatoare cu actiunea action
        newPos = successorGameState.getPacmanPosition()  # obtine pozitia noua a lui pacman
        listNewFood = successorGameState.getFood().asList()  # generaza o lista de poz. ale mancarii ramase din starea urmatoare
        listNewGhostPositions = successorGameState.getGhostPositions()  # lista poz. fantomelor in starea urmatoare

        minFoodDistance = float(999999)

        # Toate poz. mancarii ramase sunt parcurse, calculeaza distanta minima pana la una dintre ele
        for food in listNewFood:
            minFoodDistance = min(minFoodDistance, util.manhattanDistance(newPos, food))

        # Verifica daca sunt fantome in apropiere, daca este o fantoma mai mica decat 2 celule se returenaza
        # un scor mic pentru evitare
        for ghost in listNewGhostPositions:
            if util.manhattanDistance(newPos, ghost) < 2:
                return -float(999999)  # Avoid ghosts by assigning a very low score

        # Returning the evaluation based on the reciprocal of the minimum food distance
        return successorGameState.getScore() + 1.0 / minFoodDistance if minFoodDistance != float(
            999999) else successorGameState.getScore()


def scoreEvaluationFunction(currentGameState: GameState):
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
        return self.maxval(gameState, 0, 0)[0]

    def minimax(self, gameState, agentIndex, depth):
        if depth is self.depth * gameState.getNumAgents() \
                or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            return self.maxval(gameState, agentIndex, depth)[1]
        else:
            return self.minval(gameState, agentIndex, depth)[1]

    def maxval(self, gameState, agentIndex, depth):
        bestValue = float("-inf")
        bestAction = None

        for action in gameState.getLegalActions(agentIndex):
            successorState = gameState.generateSuccessor(agentIndex, action)
            value = self.minimax(successorState, (depth + 1) % gameState.getNumAgents(), depth + 1)

            if value > bestValue:
                bestValue = value
                bestAction = action

        return bestAction, bestValue

    def minval(self, gameState, agentIndex, depth):
        bestValue = float("inf")
        bestAction = None

        for action in gameState.getLegalActions(agentIndex):
            successorState = gameState.generateSuccessor(agentIndex, action)
            value = self.minimax(successorState, (depth + 1) % gameState.getNumAgents(), depth + 1)

            if value < bestValue:
                bestValue = value
                bestAction = action

        return bestAction, bestValue

        util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.
        """
        return self.maxval(gameState, 0, 0, float("-inf"), float("inf"))[0]

    def alphabeta(self, gameState, agentIndex, depth, alpha, beta):
        if depth == self.depth * gameState.getNumAgents() or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState)

        if agentIndex == 0:
            return self.maxval(gameState, agentIndex, depth, alpha, beta)[1]
        else:
            return self.minval(gameState, agentIndex, depth, alpha, beta)[1]

    def maxval(self, gameState, agentIndex, depth, alpha, beta):
        bestValue = float("-inf")
        bestAction = None

        for action in gameState.getLegalActions(agentIndex):
            successorState = gameState.generateSuccessor(agentIndex, action)
            value = self.alphabeta(successorState, (depth + 1) % gameState.getNumAgents(), depth + 1, alpha, beta)

            if value > bestValue:
                bestValue = value
                bestAction = action

            if bestValue > beta:
                return bestAction, bestValue

            alpha = max(alpha, bestValue)

        return bestAction, bestValue

    def minval(self, gameState, agentIndex, depth, alpha, beta):
        bestValue = float("inf")
        bestAction = None

        for action in gameState.getLegalActions(agentIndex):
            successorState = gameState.generateSuccessor(agentIndex, action)
            value = self.alphabeta(successorState, (depth + 1) % gameState.getNumAgents(), depth + 1, alpha, beta)

            if value < bestValue:
                bestValue = value
                bestAction = action

            if bestValue < alpha:
                return bestAction, bestValue

            beta = min(beta, bestValue)

        return bestAction, bestValue


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.

          The expectimax function returns a tuple of (actions,
        """
        "*** YOUR CODE HERE ***"

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
