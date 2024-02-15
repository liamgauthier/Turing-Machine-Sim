# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 11:09:29 2019
Turing Machine
@author: Liam Gauthier
"""
        
import datetime
from collections import defaultdict

class InvalidMovement(Exception):
    pass
class InvalidTimeType(Exception):
    pass

class condition(object):
    """
    A condition object is used to determine what instruction is to be implemented.
    It stores the single character the machine could be reading and the machine's potential
    current state. A program will look for an instruction whose condition matches the
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
        """
        returns the character the condition is assciated with
        """
        return self.character
    
    def stateRead(self):
        """
        returns the state the condition is assciated with        
        """
        return self.state
        
    def __str__(self):
        return self.character + "|" + self.state
    
    def __eq__(self, other):
        return str(self) == str(other)
    
    def __hash__(self) -> int:
        return (str(self).__hash__())
        

class instruction(object):
    """
    An instruction object is used to determine how to modify the tape.
    It stores the single character the machine will replace the currently observed
    character with, the state the machine will be changed to, and whether the tape
    will be moved right, left, or not at all.
    """
    def __init__(self, newCharacter, newState, move):
        """
        newCharacter: a string of length 1. If the character should remain the same, set ne character to "*"
        newState: a string
        move: an int representing the direction the tape will be moved by the instruction. Takes values of
        -1, 0, or 1 signifying left/tape index decrease, halt, or right/tape index increase respectively. 
        """
        self.newCharacter = str(newCharacter)[0]
        self.newState = str(newState)
        if move in ["<", "_", ">"]:
            move = {"<": -1, "_": 0, ">": 1}[move]
        if move not in [-1, 0, 1]:
            raise InvalidMovement
        self.move = move
    
    def characterChange(self, prev_char):
        """
        returns the character change the instruction is assciated with or previous character
        if the 
        """
        if self.newCharacter != "*":
            return self.newCharacter
        else:
            return prev_char
        
    def stateChange(self):
        """
        returns the state change the instruction is assciated with
        """
        return self.newState
    
    def indexChange(self):
        """
        returns the tape movement the instruction is assciated with
        as the numerical change of the tapes observed index
        """
        return self.move
    
    def __str__(self):
        return (self.newCharacter + "|" + {1:">", 0: "_", -1: "<"}[self.move] +\
    "|" + self.newState)
    def __eq__(self, other):
        return str(self) == str(other)


class tape(object):
    """
    The input data for a program.  A tape is one dimensional list of
    characters with no upper bound on length and a state that helps the machine
    determine how to update the tape.
    """
    def __init__(self, state="initial_state", cells=" ", index=0, default_char=" "):
        """
        state: a string representing the tapes starting state
        startToRight: A string containing all characters to the right of the initially
            read character with the initially read character at index 0
        leftOfStart: All characters to the left of the initially read character
            as read from left to right
        """
        self.state = str(state)
        assert index in range(len(cells))
        self.index = index
        self.tape = list(cells)
        self.default_char = default_char
    
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
        self.tape[self.index] = instruction.characterChange(self.tape[self.index])
        self.index += instruction.indexChange()
        if self.index not in range(len(self.tape)):
            if instruction.indexChange() == 1:
                self.tape.append(self.default_char)
            else:
                self.tape.insert(0, self.default_char)
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
        self.recipe = defaultdict(lambda: instruction("*", "done", "_"))
        self.description = description
        
    def addLine(self, condition, instruction):
        """
        Add a line of code containing a condition and an instruction.  When the
        machine encounters this condition when running the program on a tape, the
        tape is updated according to this instruction.
        MULTIPLE LINES OF CODE SHOULD NOT CONTAIN THE SAME CONDITION OBJECT
        """
        self.recipe[condition] = instruction
        
    def showProgram(self):
        return [(str(cond) + " --> " + str(self.recipe[cond])) for cond in self.recipe]
        
    def describeProgram(self):
        return self.description
            
    def replaceInstruction(self, sameCondition, newInstruction):
        """
        Replaces the instruction object associated sameCondition with
        newInstruction.
        """
        self.recipe[sameCondition] = newInstruction
                
    def deleteLine(self, condition):
        """
        Deletes all lines with condition.
        """
        self.recipe.pop(condition)
            
    def clearProgram(self):
        self.recipe = defaultdict(lambda: instruction("*", "done", "_"))

    def run(self, tape: tape):
        """
        Uses the programed lines to continually update the tape until the tape
        is in a condition for which no instruction was programed.
        """
        while True:
            next_instruction = self.recipe[tape.currentCondition()]
            tape.update(next_instruction)
            if next_instruction.indexChange() == 0:
                break

        return tape.listToStr()
    
    def controlled_run(self, tape, time, timeType="s"):
        """
        Uses the programed condition -> instruction mappings to continually update the tape until the tape
        is in a condition for which no instruction was programed or it is programmed to halt.  Will end early
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
            def counter_constructor():
                stepNum = 0
                while True:
                    yield stepNum < time
                    stepNum += 1
            counter = counter_constructor()
            truth = lambda: counter.__next__()
        else:
            raise InvalidTimeType
        while truth():
            next_instruction = self.recipe[tape.currentCondition()]
            tape.update(next_instruction)
            if next_instruction.indexChange() == 0:
                break
        return tape.listToString()


def compileProgram(fileName):
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