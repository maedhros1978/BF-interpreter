from __future__ import print_function
from readchar import readchar
import sys

def get_end_of_loop(instructions, ip):
    """ip must be the address of an open square brackets in instructions
    list. Search for the corresponding closed square bracket"""
    n_parenthesis = 1
    index = ip + 1
    while n_parenthesis != 0:
        if instructions[index] == ']':
            n_parenthesis -= 1
        elif instructions[index] == '[':
            n_parenthesis += 1
        index += 1
    return index

def interpreter(instructions):
    """Brainfuck interpreter"""
    stack, dp, ip, mem = [], 0, 0, 256 * [0] # Initialization of loop stack, memory 
    while ip < len(instructions):            # pointer, instruction pointer, and memory
        if instructions[ip] == "+":          # Increment memory slot
            mem[dp] += 1
            ip += 1
        elif instructions[ip] == "-":        # Decrement memory slot
            mem[dp] -= 1
            ip += 1
        elif instructions[ip] == "<":        # Increment memory pointer
            if dp > 0:
                dp -= 1
            else: dp = 255
            ip += 1
        elif instructions[ip] == ">":        # Decrement memory pointer
            if dp < 255:
                dp += 1
            else: dp = 0
            ip += 1
        elif instructions[ip] == ".":        # Output character at current memory slot
            print(str(unichr(mem[dp])), end="")
            ip += 1
        elif instructions[ip] == ",":        # Input character
            char = readchar()
            mem[dp] = ord(char)
            ip += 1
        elif instructions[ip] == "[":        # Loop start
            if mem[dp] == 0:
                ip = get_end_of_loop(instructions, ip)
            else:
                stack.append(ip)
                ip += 1
        elif instructions[ip] == "]":        # Loop end
            if mem[dp] == 0:
                stack.pop()
                ip += 1
            else:
                ip = stack.pop()

def run(instructions):
    """Remove characters different from [].,<>+- and concatenate command
    line arguments. Then send acutal brainfuck code to interpreter"""
    cleaned = filter(lambda s: s in "[],.+-<>", ''.join(instructions))
    interpreter(cleaned)
    return

def main():
    """ A simple python interpreter for the brainfuck programming language.
    Usage: python bf.py "<YOUR BRAINFUCK PROGRAM>"
    use quotes around your program to avoid problems with square brackets.
    
    An example of a brainfuck program:
    
    python bf.py '>+[[>],.-------------[+++++++++++++[<]]>]<<[<]++++++++++.>>[.>][>]++++++++++.'
    
    This program wait for user input, and then prints it on screen.
    
    Another example:
    
    python bf.py ">++++++++++>+>+[[+++++[>++++++++<-]>.<++++++[>--------<-]+<<<]>.>>[[-]<[>+<-]>>[<<+>+>-]<[>+<-[>+<-[>+<-[>+<-[>+<-[>+<-[>+<-[>+<-[>+<-[>[-]>+>+<<<-[>+<-]]]]]]]]]]]+>>>]<<<]"
    
    This program prints the Fibonacci sequence (needs to be stopped with Ctrl + c or equivalent).
    I don't know for how long it's completely reliable, since the memory of this interpreter
    is set to be 255 characters, and it could be the program needs more than that relatively
    soon to produce the right numbers.
    The examples come (with small modification) from http://www.bf.doleczek.pl/
    """
    input_lines = []
    if len(sys.argv) >= 1:
        input_lines = sys.argv[1:]
    if len(input_lines) == 0:
        print("""Usage: - python bf.py "<YOUR BRAINFUCK PROGRAM>" to run a program
       - python --help to see a detailed help""")
    elif input_lines[0] == '--help' or input_lines[0] == '-h':
        help(main)
        return
    else:
        run(input_lines)
        return

if __name__ == '__main__':
  main()