# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 11:09:29 2019
Turing Machine
@author: Liam Gauthier
"""
        
import datetime

class InvalidMovement(Exception):
    pass
class InvalidTimeType(Exception):
    pass

class condition(object):
    """
    A condition object is used to determine what instruction is to be implemented.
    It stores the single character the machine is reading and the machine's current
    state.  A program will look for an instruction whose condition matches the
    tapes current condition when updating the tape.
    """
    def __init__(self, character, state):
        """
        character: a string of length 1
        state: a string
        """
        self.character = str(character)[0]
        self.state = str(state)
        
    def characterRead(self):
        return self.character
        #returns the character the condition is assciated with
    
    def stateRead(self):
        return self.state
        #returns the state the condition is assciated with
        
    def __str__(self):
        return self.character + "|" + self.state
    def __eq__(self, other):
        return str(self) == str(other)
        

class instruction(object):
    """
    An instruction object is used to determine how to alter and move the tape.
    It stores the single character the machine will replace the currently observed
    character with, the state the machine will be changed to, and whether the tape
    will be moved right, left, or not at all.
    """
    def __init__(self, newCharacter, newState, move):
        """
        newCharacter: a string of length 1
        newState: a string
        move: a string of length 1, containing any of the following characters:
        '<', '_', or '>'.
        """
        self.newCharacter = str(newCharacter)[0]
        self.newState = str(newState)
        if move not in ["<", "_", ">"]:
            raise InvalidMovement
        else:
            self.move = {"<": -1, "_": 0, ">": 1}[move]
    
    def characterChange(self):
        return self.newCharacter
        #returns the character change the instruction is assciated with
    def stateChange(self):
        return self.newState
        #returns the state change the instruction is assciated with
    def indexChange(self):
        return self.move
        #returns the tape movement the instruction is assciated with
        #as the numerical change of the tapes observed index
    
    def __str__(self):
        return (self.newCharacter + "|" + {1:">", 0: "_", -1: "<"}[self.move] +\
    "|" + self.newState)
    def __eq__(self, other):
        return str(self) == str(other)

class tape(object):
    """
    The input data for a program.  A tape is comprized of a consecutive list of
    characters with no upper bound on length and a state that helps the machine
    determine how to update the tape.
    """
    def __init__(self, state, startToRight=" ", leftOfStart=""):
        """
        state: a string representing the tapes starting state
        startToRight: A string containing all characters to the right of the initially
            read character with the initially read character at index 0
        leftOfStart: All characters to the left of the initially read character
            as read from left to right
        """
        self.state = str(state)
        self.index = len(leftOfStart)
        self.tape = list(leftOfStart) + list(startToRight)
    
    def changeState(self, newState):
        self.state = newState
    
    def currentCondition(self):
        return condition(self.tape[self.index], self.state)
    
    def currentIndex(self):
        return self.index
    
    def update(self, instruction):
        """
        changes any attributes of the tape as per the characterChange, stateChange,
        and indexChange attributes of instruction, an instruction object.
        """
        self.tape[self.index] = instruction.characterChange()
        self.index += instruction.indexChange()
        if self.index not in range(len(self.tape)):
            if instruction.indexChange() == 1:
                self.tape.append(" ")
            else:
                self.tape.insert(0, " ")
                self.index = 0
        self.state = instruction.stateChange()
        
    def listToStr(self):
        """
        returns all characters the tape holds as read from left to right as a
        string
        """
        string = ""
        for i in self.tape:
            string += i
        return string
    
    def __str__(self):
        return "state: " + self.state +\
    "\n" + self.listToStr()[0:self.index] +\
    "\n> " + self.tape[self.index] + " <\n"\
    + (self.listToStr()[self.index + 1:] if self.index + 1 < len(self.tape) else "")

    
class program(object):
    """
    A list of condition/instruction pairs that can be run on a tape object and
    print out the tape after the programs conclusion.  Currently, a list of tuples
    is used because a condition object can't be used as a dictionary key (idk?)
    and I haven't yet debugged that.
    """
    def __init__(self, description=""):
        self.recipe = []
        self.description = description
        
    def addLine(self, condition, instruction):
        """
        Add a line of code containing a condition and an instruction.  When the
        machine encounters this condition when running the program on a tape, the
        tape is updated according to this instruction.
        MULTIPLE LINES OF CODE SHOULD NOT CONTAIN THE SAME CONDITION OBJECT
        """
        self.recipe.append((condition, instruction))
        
    def showProgram(self):
        for a in self.recipe:
            print(str(a[0]) + " --> " + str(a[1]))
        
    def describeProgram(self):
        print(self.description)
        return self.description
            
    def replaceInstruction(self, sameCondition, newInstruction):
        """
        Replaces the instruction object associated sameCondition with
        newInstruction.
        """
        for a in range(len(self.recipe)):
            if self.recipe[a][0] == sameCondition:
                self.recipe[a] = (sameCondition, newInstruction)
                
    def replaceCondition(self, newCondition, sameInstruction):
        """
        Replaces the condition object associated samesameInstruction with
        newCondition.  Be careful the sameInstruction instruction object is not
        corresponding to multiple different conditions.
        """
        for a in range(len(self.recipe)):
            if self.recipe[a][1] == sameInstruction:
                self.recipe[a] = (newCondition, sameInstruction)
                
    def deleteLine(self, condition, usingInstruction=False, usingIndex=False):
        """
        Deletes all lines with condition.  If usingInstruction is True, condition,
        must be an instruction object instead of a condition object.  If usingIndex
        is True, condition must be an interger (regardless of usingInstruction).
        """
        if not usingIndex:
            for a in self.recipe:
                if a[usingInstruction] == condition:
                #the boolean values for usingInstruction handily corresponds to
                #the tuple index in question
                    self.recipe.remove(a)
        else:
            self.recipe.pop(condition)
            
    def clearProgram(self):
        self.recipe = []

    def run(self, tape):
        """
        Uses the programed lines to continually update the tape until the tape
        is in a condition for which no instruction was programed.
        """
        while True:
            for item in self.recipe:
                if item[0] == tape.currentCondition():
                    tape.update(item[1])
                    break
            else:
                break
        print(tape)
    
    def ControlledRun(self, tape, time, timeType="s"):
        """
        Uses the programed lines to continually update the tape until the tape
        is in a condition for which no instruction was programed.  Will end early
        depending on length of time, time, and the unit of time, timeType.
        The time types are:
            'h': hours
            'm': minutes
            's': seconds
            'ms': milliseconds
            'u': number of calls to update for the tape object
        """
        types = {"h":datetime.timedelta(hours=1), "m":datetime.timedelta(minutes=1),\
                 "s":datetime.timedelta(seconds=1), "ms":datetime.timedelta(milliseconds=1)}
        if timeType in types:
            startTime = datetime.datetime.now()
            totalTime = types[timeType] * time
            truth = lambda: datetime.datetime.now() - startTime <= totalTime
        elif timeType == "u":
            def steps():
                stepNum = 0
                while True:
                    yield stepNum
                    stepNum += 1
            totalSteps = steps()
            truth = lambda: totalSteps.__next__() < time
        else:
            raise InvalidTimeType
        while truth():
            for item in self.recipe:
                if item[0] == tape.currentCondition():
                    tape.update(item[1])
                    break
            else:
                break
        print(tape)
        
def callProgram(fileName):
    """
    Initializes a program object from the program written in fileName.  See 'README.txt'
    for instructions on how to write a Turing Machine program in a .txt file
    """
    stringToCondition = lambda string: condition(string[0], string[2:-1])
    stringToInstruction = lambda string: instruction(string[0], string[4:-1], string[2])
    tempfile = open(fileName)
    file = tempfile.readlines()
    tempfile.close()
    fileProgram = program(fileName)
    fileCondition = file[0::3]
    fileInstruction = file[1::3]
    for line in range(len(fileCondition)):
        fileProgram.addLine(stringToCondition(fileCondition[line]),\
                            stringToInstruction(fileInstruction[line]))
    return fileProgram