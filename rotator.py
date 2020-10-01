import sys


def main():
    inputs = sys.argv

    # input processing
    firstInput = inputs[1]
    if len(inputs) == 3:
        currState = State(inputs[2])
    else:
        currState = State()

    # print command processing
    if firstInput == "print":
        print(currState)

    # goal command processing
    if firstInput == "goal":
        print(currState.is_goal())

    # actions command processing
    if firstInput == "actions":
        possActions = currState.listOfActions
        for i in range(len(possActions)):
            print(possActions[i])

    if firstInput[:4] == "walk":
        walkNum = int(firstInput[4:])
        currState.walk(walkNum)


    if firstInput == "test":
        print(currState)

        Action1 = Action("rotate",2,1)
        currState.execute(Action1)
        print(currState)

        Action2 = Action("slide", 4, 2, 4, 1)
        currState.execute(Action2)
        print(currState)

        Action3 = Action("rotate", 2, -1)
        currState.execute(Action3)
        print(currState)

        Action4 = Action("slide", 3, 1, 3, 2)
        currState.execute(Action4)
        print(currState)

        Action5 = Action("rotate", 1, 1)
        currState.execute(Action5)
        print(currState)

        Action6 = Action("slide", 4, 2, 4, 1)
        currState.execute(Action6)
        print(currState)

        Action7 = Action("rotate", 1, -1)
        currState.execute(Action7)
        print(currState)

        print(currState.is_goal())


        # ask prof,
        # - for ending the walk loop should we check if we're at goal or not?
        # - any more examples?


class State:
    def __init__(self, stringForm="12345|1234 |12354"):
        self.form = self.convertStringToArray(stringForm)
        self.blankY, self.blankX = self.findBlankLocation(self.form)
        self.rows = len(self.form)
        self.cols = len(self.form[0])
        self.listOfActions = self.actions()
        self.prevStates = []

    def __str__(self):
        return self.convertArrayToString(self.form)

    def convertStringToArray(self, inputString):
        split = inputString.split("|")
        formArray = []
        for i in range(0, len(split)):
            formArray.append(list(split[i]))

        return formArray

    def convertArrayToString(self, inputArray):
        formString = ""
        for i in range(0, len(inputArray)):
            for j in range(0,len(inputArray[i])):
                formString += str(inputArray[i][j])
            formString += str("|")

        formString = formString[:-1]

        return formString

    def is_goal(self):
        isGoal = True
        # is at goal if indices of every array level equal each other or blank
        currCol = []
        rows = len(self.form)
        for j in range(len(self.form[0])):
            currCol = []
            for i in range(len(self.form)):
                currCol.append(self.form[i][j])

            currCol.sort() # sorts the blank to first
            # all same
            if currCol.count(currCol[0]) == len(currCol):
                continue
            # blank gets checked first and then if the other two are the same
            elif currCol[0] == " " and currCol.count(currCol[1]) == len(currCol)-1:
                continue
            else:
                isGoal = False
                return isGoal
        return isGoal

    def findBlankLocation(self, arrayForm):
        for i in range(len(arrayForm)):
            for j in range(len(arrayForm[0])):
                if arrayForm[i][j] == " ":
                    return i,j

    def actions(self):
        listOfActions = []

        #appends all rotations
        for i in range(self.rows):
            listOfActions.append(Action("rotate", i, -1))
            listOfActions.append(Action("rotate", i, 1))

        #appends up to two slides
        if self.blankY != 0:
            listOfActions.append(Action("slide", self.blankX, self.blankY - 1, self.blankX, self.blankY))
        if self.blankY != self.rows -1:
            listOfActions.append(Action("slide", self.blankX, self.blankY + 1, self.blankX, self.blankY))

        return listOfActions

    def __eq__(self, other):
        return str(self) == str(other)

    def clone(self):
        clonedState = State(str(self))
        clonedState.prevStates = self.prevStates
        return clonedState

    def walk(self, walkNum):
        while str(self) not in self.prevStates:
            # prints current state
            print(self)
            # resets possible actions
            self.blankY, self.blankX = self.findBlankLocation(self.form)
            self.listOfActions = self.actions()
            # executes
            self.execute(self.listOfActions[walkNum])

    def execute(self, action):
        tempObj = self.clone()
        action.executeAction(self)
        self.prevStates.append(str(tempObj))


class Action:
    def __init__(self, type, i1, i2, i3=" ", i4=" "):
        self.type = type
        self.input1 = i1
        self.input2 = i2
        self.input3 = i3
        self.input4 = i4

    def __str__(self):
        if self.type == "rotate":
            return self.type+"({},{})".format(self.input1, self.input2)
        elif self.type == "slide":
            return self.type+"({},{},{},{})".format(self.input1, self.input2, self.input3, self.input4)

    def executeAction(self, stateObj):
        if self.type == "rotate":
            if self.input2 == 1:
                tempRow = stateObj.form[self.input1]
                newRow = list(tempRow[-1]) + tempRow[:-1]
                stateObj.form[self.input1] = newRow
            elif self.input2 == -1:
                tempRow = stateObj.form[self.input1]
                newRow = tempRow[1:] + list(tempRow[0])
                stateObj.form[self.input1] = newRow
        elif self.type == "slide":
            stateObj.form[self.input4][self.input3] = stateObj.form[self.input2][self.input1]
            stateObj.form[self.input2][self.input1] = " "


if __name__ == "__main__":
    main()

