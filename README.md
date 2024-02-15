# Turing Machine Simulator

This is an independent project I worked on in high school. It is my first project as an aspiring programmer. This Python script contains the classes required to simulate a turing machine in your own projects.

## What is a Turing Machine?

A turing machine is a theoretical machine that can perform any algorithm using only Alan Turing's six primitive methods. The six primitives are:

1. Move one position left in memory
2. Move one position right in memory
3. Read the symbol at the current position in memory
4. Write a symbol to the current position in memory, erasing the previous symbol if one was there
5. Change the state of the machine
6. "Halt" or terminate the program once it has finished

The theoretical machine described by Turing has a "tape" of infinite length which is a one-dimensional array of characters that acts as the machine's memory and display simultaneously. Additionally, the machine has a "reader" which can scan the character at the current position along the tape, write a new character to that position (erasing the character that was previously there), and move its position left or right. Finally, the machine has an internal "state" which tells it what set of instructions to follow.

When you execute a program on a turing machine, it loops through the following steps until the program halts. The machine scans the character at the current position of the tape and then the program uses the result of the scan operation and the machine's current state to fetch the instruction it will follow. If the instruction is not halt, then it writes a character to the tape at the current position, moves the tape left or right, and changes the state of the machine in accordance with that instruction.

One can think of a turing machine program as a mapping from (state, scanned character) pairs to (character to write, new state, move direction) triples where the move direction is "halt" for the instruction that is fetched once the program has finished.

See [here](https://en.wikipedia.org/wiki/Turing_machine) for more information.



## Getting Started

### Import Classes

Since this is not a Python library, you will need to put Turing_Machine.py into the same directory as any Python script in which you want to use these classes so you can import the turing machine classes. you can import them with:

```
import Turing_Machine as tm
```

The general workflow with these classes will be to initialize a `program`, add `codition`->`instruction` mappings to the `program`, initialize a `tape` with initial memory and an initial state, then run the `program` using the `run` method or the `controlled_run` method with a `tape` as the argument.

### Create a Program

Create a program object using the `Turing_Machine.program` constructor. It takes only one optional argument, `description`, which is a string that describes the program and has no effect on how the program will run.

```
my_turing_machine_program = tm.program(description="A program using Turing_Machine.py")
```

Next, we will add `condition`->`instruction` mappings to the program. First, we will create a `condition`, then we will create an `instruction`. Finally, we will add the mapping to the program with the `program.addLine()` method.

A `condition` has two arguments, `character` and `state`. `character` is a string with length 1 which the turing machine could read off the tape. `state` is a string representing potential state of the machine.

An `instruction` has three arguments, `newCharacter`, `newState`, and `move`. `newCharacter` is a string with length 1 which the turing machine will write to the tape. If `newCharacter` is "*", then a new character will not be written to the tape and the previous character will not be erased. `newState` is a string which the state of the turing machine will be changed to. `move` is a string of length 1, taking values of "<", "\_", or ">". "<" causes the reader to move 1 spot to the left in memory, ">" causes the reader to move one spot right in memory, and "\_" causes the program to halt.

The `program.addLine()` method takes two arguments, the first one is a condition and the second is an instruction.

```
cond_1 = tm.condition("h", "Check first letter")
inst_1 = tm.instruction("H", "Done", "_")
my_turing_machine_program.addLine(cond_1, inst_1)
```

### Create a Tape

Create a tape using the `Turing_Machine.tape` constructor. Tape has four optional arguments, `state`, `cells`, `index`, and `default_char`. `state` is a string used as the machine's initial state and defaults to "initial_state". `cells` is a string containing all the characters on the tape and defaults to " ". `index` is the initial spot in memory the reader is at, i.e the index the reader is at on the string, `cells`, and defaults to 0. `default_char` is the character that the reader will read if it is moved left of index 0 on `cells` or right of index `len(cells)` and defaults to " ".

```
hello_world_tape = tm.tape(state="check first letter", cells="hello, World!", index=0)
```

### Run a Program

Once you have initialized a program and a tape, there are two ways to run the program. You can use the `program.run()` method or the `program.controlled_run()` method. `run()` takes a `tape` as an argument and runs until the process halts. `controlled_run()` has three arguments, `tape`, `time`, and `timeType`. `tape` is the `tape` object you want to execute the program on. `time` is the length of time, in units of `timeType`, that the program will run for before being pre-emptively halted. `timeType` takes one of "h", "m", "s", "ms", or "u" where "h" means units of hours, "m" means units of minutes, "s" means units of seconds, "ms" means units of milliseconds, and "u" is a number of times an instruction will be applied to the `tape`. `controlled_run()` is preferable while debugging if you are unsure that your program will halt. However, It adds extra time complexity, so if you know your program will halt then `run()` is better.

```
print(my_turing_machine_program.run(hello_word_tape))
>>> "Hello, World!"
```


## Tutorial

Let's make a script that simulates a turing machine program which, given a tape containing a binary number with the index at the least significant digit and the initial state being "initial_state", will erase each digit and write "e" if the number is even and "o" if the number is odd. This is quite simple for us to determine since a binary number is even if and only if its last digit is 0.

The first step is to import `Turing_Machine.py` into our main script. and initialize our program object.

```
# main.py

import Turing_Machine as tm

description = "determine whether the tape is an even or odd number"

even_or_odd = tm.program(description)
```

Next, we will add the `condition`->`instruction` mappings to the program.

```
even_or_odd.addLine(
    tm.condition("0", "initial_state"),
    tm.instruction(" ", "del_even" "<")
)
even_or_odd.addLine(
    tm.condition("0", "del_even"),
    tm.instruction(" ", "del_even", "<")
)
even_or_odd.addLine(
    tm.condition("1", "del_even"),
    tm.instruction(" ", "del_even", "<")
)
even_or_odd.addLine(
    tm.condition(" ", "del_even"),
    tm.instruction("e", "final_state", "_")
)
even_or_odd.addLine(
    tm.condition("1", "initial_state"),
    tm.instruction(" ", "del_odd" "<")
)
even_or_odd.addLine(
    tm.condition("0", "del_odd"),
    tm.instruction(" ", "del_odd", "<")
)
even_or_odd.addLine(
    tm.condition("1", "del_odd"),
    tm.instruction(" ", "del_odd", "<")
)
even_or_odd.addLine(
    tm.condition(" ", "del_odd"),
    tm.instruction("o", "final_state", "_")
)
```

Lastly, we will initialize a few tapes and run the program on them.

```
num1 = tm.tape("initial_state", "101011", 5)
num2 = tm.tape("initial_state", "100100", 5)
num3 = tm.tape("initial_state", "100001", 5)

print(even_or_odd.run(num1))
print(even_or_odd.run(num2))
print(even_or_odd.run(num3))

>>> "o"
>>> "e"
>>> "o"
```

## Writing a Turing Machine Program in a .txt File

Turing_Machine.py includes a function, `compileProgram()` which converts a text file into a `program` object with all `condition`->`instruction` mappings that were described in the text file.

### How to right a program.txt

Each mapping uses 3 lines in the text file. The first line contains the arguments for a condition, the second contains the arguments for the instruction the condition is mapped to, and the third is ignored by the function and can be used for commenting.

The format for the condition line is: `"character"|"state"`. The format for the instruction line is `"newCharacter"|"direction: one of '<', '_', '>'"|"newState"`. For example, the even or odd program above could have been written in a text file like this:

```
0|initial_state
 |<|del_even
begin deleting the characters of the tape while remembering that the least significant digit is 0
1|initial_state
 |<|del_odd
begin deleting the characters of the tape while remembering that the least significant digit is 1
0|del_even
 |<|del_even

1|del_even
 |<|del_even
continue deleting while there are still digits in the number
0|del_odd
 |<|del_odd

1|del_odd
 |<|del_odd
continue deleting while there are still digits in the number
 |del_even
e|_|final_state
write "e" to an empty tape
 |del_odd
o|_|final_state
write "o" to an empty tape
```

### How to compile a program.txt

A program.txt is compiled using the `compileProgram()` function. This function takes the file's relative path as a string as the argument and the function returns a `program` with all the mappings from the text file. For example, you can run the program compiled from the provided "Add.txt" with the following code:

```
import Turing_Machine as tm

calculator = tm.compileProgram("Add.txt")

equation = tm.tape("iterateRight", "12+34")
# the two integers in the second string can be replaced with any other positive integers. Try it!

print(calculator.run(equation))
>>>  46
```
