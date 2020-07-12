import numpy as np
from State import State
from MinStateHeap import MinStateHeap


def generateStates():
    txt_path = 'arrs/backTrackerMazes/01.txt'  # path maze data file
    f = open(txt_path)  # open file
    data_lists = f.readlines()  # read file data
    dataset = []

    # convert data in file to list
    for data in data_lists:
        data1 = data.strip('\n')
        data2 = data1.split(' ')
        dataset.append(data2)
    # convert list to states list and return
    return [[State(x, y, int(dataset[x][y])) for y in range(len(dataset[0]))] for x in range(len(dataset))]


# heuristic function (Manhattan distance)
def heuristic(s1: State, s2: State):
    return abs(s1.location[0] - s2.location[0]) + abs(s1.location[1] - s2.location[1])


# generate a list of possible actions for current state
# 1: down; 2: up; 3: right; 4: left
def generateActionList(state: State):
    possibleActions = []
    # print("State location: %s" % state.location)
    row = state.location[0]
    column = state.location[1]

    #   Check possible actions
    #   Check down
    if row + 1 <= len(states) - 1:
        if (states[row + 1][column].discoveredBlockStatus == 0) & (not closedHeap.contains(states[row + 1][column])):
            possibleActions.append(1)
        # else:
        # print("\tState [%d %d] is blocked: states[%d][%d].isBlocked = %d" % (x + 1, y, x + 1, y, states[x + 1][y].isBlocked))
    #   Check up
    if row - 1 >= 0:
        if (states[row - 1][column].discoveredBlockStatus == 0) & (not closedHeap.contains(states[row - 1][column])):
            possibleActions.append(2)
        # else:
        # print("\tState [%d %d] is blocked: states[%d][%d].isBlocked = %d" % (x - 1, y, x - 1, y, states[x - 1][y].isBlocked))
    #   Check right
    if column + 1 <= len(states) - 1:
        if (states[row][column + 1].discoveredBlockStatus == 0) & (not closedHeap.contains(states[row][column + 1])):
            possibleActions.append(3)
        # else:
        # print("\tState [%d %d] is blocked: states[%d][%d].isBlocked = %d" % (x, y + 1, x, y + 1, states[x][y + 1].isBlocked))
    #   Check left
    if column - 1 >= 0:
        if (states[row][column - 1].discoveredBlockStatus == 0) & (not closedHeap.contains(states[row][column - 1])):
            possibleActions.append(4)
        # else:
        # print("\tState [%d %d] is blocked: states[%d][%d].isBlocked = %d" % (x, y - 1, x, y - 1, states[x][y - 1].isBlocked))
    # print("\tPossible action: %s" % possibleActions)

    return possibleActions


# return a state after moving to a direction
def stateAfterMoving(state, action):
    row = state.location[0]
    column = state.location[1]
    # down
    if action == 1:
        return states[row + 1][column]
    # up
    elif action == 2:
        return states[row - 1][column]
    # right
    elif action == 3:
        return states[row][column + 1]
    # left
    elif action == 4:
        return states[row][column - 1]
    else:
        return None


def checkNearbyBlock(s: State):
    row = s.location[0]
    column = s.location[1]
    # Check down
    if row + 1 <= len(states) - 1:
        states[row + 1][column].discoveredBlockStatus = states[row + 1][column].actualBlockStatus
    # Check up
    if row - 1 >= 0:
        states[row - 1][column].discoveredBlockStatus = states[row - 1][column].actualBlockStatus
    # Check right
    if column + 1 <= len(states) - 1:
        states[row][column + 1].discoveredBlockStatus = states[row][column + 1].actualBlockStatus
    # Check left
    if column - 1 >= 0:
        states[row][column - 1].discoveredBlockStatus = states[row][column - 1].actualBlockStatus


# A* algorithm
def ComputePath():
    while goalState.gValue > openHeap.peek().fValue:
        # print(openHeap.toString())
        minState = openHeap.pop()  # Remove a state s with the smallest f-value g(s) + h(s) from openHeap
        # print(openHeap.toString())
        closedHeap.push(minState)
        actionList = generateActionList(minState)  # Generate action list for the state
        for action in actionList:
            searchedState = stateAfterMoving(minState, action)  # Get the state after taking a specific action
            if searchedState.searchValue < counter:
                searchedState.gValue = 99999
                searchedState.searchValue = counter
            if searchedState.gValue > minState.gValue + 1:
                searchedState.gValue = minState.gValue + 1  # Update the cost
                searchedState.treePointer = minState    # Build a forward link pointing to the last state

                # print("openHeap: %s" % openHeap.toString())  # print openHeap

                if openHeap.contains(searchedState):
                    # print("openHeap contains %d: %s" % (searchedState.fValue, searchedState.location))
                    openHeap.remove(searchedState)  # Remove existed state from opehHeap

                # insert succ(s, a) into OPEN with f-value g(succ(s, a)) + h(succ(s, a))
                searchedState.hValue = heuristic(searchedState, goalState)
                searchedState.updateFValue()
                # print("searchedState.gValue = %d" % searchedState.gValue)
                # print("searchedState.hValue = %d" % searchedState.hValue)
                # print("searchedState.fValue = %d" % searchedState.fValue)
                # print("searchedState.location = %s" % searchedState.location)
                openHeap.push(searchedState)
                # print("openHeap: %s" % openHeap.toString())  # print openHeap
                # print("")


# main function
if __name__ == "__main__":
    counter = 0  # A star counter
    agentPath = []  # Path recorder
    print("Initializing states...", end="")
    states = generateStates()  # initialize states
    print("done!")

    # initialize start state and goal state randomly
    print("Randomly setting start location and goal location...", end="")
    statesEdgeSize = len(states)    # Size of states list
    # print(statesEdgeSize)

    # Randomly set start location and goal location
    startLocation = np.random.randint(0, statesEdgeSize, 2)
    goalLocation = np.random.randint(0, statesEdgeSize, 2)
    # print(start, goal)
    # print(states[start[0]][start[1]].isBlocked)
    # print(states[goal[0]][goal[1]].isBlocked)

    # Check if the random start location and goal location is available
    # If not, re-generate a new random one
    while (states[startLocation[0]][startLocation[1]].actualBlockStatus == 1) | (
            states[goalLocation[0]][goalLocation[1]].actualBlockStatus == 1) | all(startLocation == goalLocation):
        startLocation = np.random.randint(0, statesEdgeSize, 2)
        goalLocation = np.random.randint(0, statesEdgeSize, 2)
        # print(start, goal)
        # print(states[start[0]][start[1]].isBlocked)
        # print(states[goal[0]][goal[1]].isBlocked)
    print("done!")

    # Respectively label the states at start location and at goal location as start state and goal state
    startState = states[startLocation[0]][startLocation[1]]
    goalState = states[goalLocation[0]][goalLocation[1]]

    agentPath.append(startLocation)     # Add the start location to the path
    print("Start location: %s" % startState.location)   # Print the start location
    print("Goal location: %s" % goalState.location)     # Print the goal location
    print("")

    print("Starting iteration...")
    while startState != goalState:
        counter += 1

        startState.gValue = 0  # record cost for start state to reach start state, which is 0
        startState.searchValue = counter  #
        goalState.gValue = 99999  # record cost for goal state to reach start state, which uses 999 as infinity
        goalState.searchValue = counter  #

        # initialize open heap and closed heap
        openHeap = MinStateHeap()
        closedHeap = MinStateHeap()

        # calculate h and f value
        startState.hValue = heuristic(startState, goalState)
        startState.updateFValue()
        # print("State f Value: %d" % startState.fValue)

        checkNearbyBlock(startState)
        openHeap.push(startState)  # insert start state into open heap

        ComputePath()  # run A*

        # if open heap is empty, report that can't reach the target
        if openHeap.size() == 0:
            print("I cannot reach the target...o(╥﹏╥)o")
            exit()

        # A star search finds the start state and move start location according to the tree pointer
        # Track the tree pointers from goal state to start state
        tempState = goalState
        print("Time Step %d: " % counter)
        print("\tTree path: %s" % tempState.location, end="")
        while (tempState.treePointer is not None) & (tempState != startState):
            print("→%s" % tempState.treePointer.location, end="")
            if tempState.treePointer == startState:
                startState = tempState  # Move the start state
                agentPath.append(startState.location)   # Record the move of agent
                continue
            tempState = tempState.treePointer
        print("")
        print("\tAgent Moves To: %s" % startState.location)
        print("\tGoal Location: %s" % goalState.location)
        print("")

    print("I reached the target!╰(*°▽°*)╯")
    print("Search Statistics:")
    print("\tStart Location: %s" % startLocation)
    print("\tGoal Location: %s" % goalLocation)
    print("\tAgent Path: ", end="")
    for i in range(len(agentPath)):
        if i == 0:
            print(agentPath[0], end="")
            continue
        print("→%s" % agentPath[i], end="")
    print("\t")
    print("\tTotal Time Step: %d" % counter)
    print("\tActual Cost: %d" % (len(agentPath) - 1))
    exit()
