This is my first project excluding course work, daily coding challenges, and the like.  I would appreciate any feedback you can provide.

# Turing-Machine-Sim
This software simulates a Turing Machine in your python console.  A turing machine is a machine that uses Alan Turing's six primitives to
perform calculations on a tape of theoreticaly infinite length.  A Turing Machine program is comprized of lines which check the tape's
current character being scanned and the tape's current state.  If a line of code corresponds to the tape's 'condition' the 'instruction'
associated with that condition is enacted on the tape moving the tape.  An instruction will change the following:
  -the character being read by the machine is erased and a new character is written in it's place
  -the tape is moved left, right, or not at all, changing the character that is read by the machine
  -the machine's state is changed.

To use the machine a program object and a tape object must be created.  An instance of the program class is initialized using program()
with the optional string argument for a program description; the program object has an empty list of lines of code.  Lines of code are
written usin the addLine(condition, instruction) method where condition is a condition object which determines when the instruction is
implemented and instruction is an instruction object which determines how the tape is altered.  An instance of the condition class is
created using condition(character, state) where character is a string of length 1 refering to the character the machine is currently
reading and state is a string refering to the tape's current state.  An instance of the instruction class is created using
instruction(newCharacter, newState, move) where newCharacter is a string with length one that machine will replace the character its
currently reading with, newState is a string that will become the tape's new state, and move is any of the three following strings: "<"
which denotes the machine will read the character to the left of the current one after this instuction is implemented, ">" denotes the
machine will read the character to the right, and "_" means the machine will not move to a new character.  To run a program use the
run(tape) method where tape is an instance of the tape class initialized using tape(state, startToRight, leftOfStart) where state is the
tape's initial state, start to right is a string containg all characters to the right of the initially read character with the initially
read character at the 0th index, and leftOfStart is an optional string argument containing all characters to the left of the initially read
character as read from left to right.

# Writing lines in a .txt
Each line of code for a Turing Machine program takes three lines in the text file: the condition, the instruction, the blank line.

condition: this is the condition the tape must be in for the instruction to take place.  It is written as: the character you expect to see,
followed by a vertical bar, |, followed by the state you are expecting.  e.g. '5|add1'
instruction: this is how you want the tape to be changed.  It is written as: the character replacing the current character, a vertical bar,
the character denoting the movement, a vertical bar, and the new state of the tape.  e.g. '6|>|iterateRight'
blank line: The third line is not read by the machine and can be left blank or used for notes.  ALWAYS REMEMBER TO ADD THE BLANK LINE,
forgeting the caridge return after last instruction will cause the machine to ignore the last character of the new state which may break
the program.  This program imported into the console using the callProgram(fileName) function.

e.g. copy the following code into your console:
calculator = callprogram("Add.txt")
equation = tape("iterateRight", "12+34")#the two intergers in the second string can be replaced with any other positive intergers. Try it!
calculator.run(equation)
