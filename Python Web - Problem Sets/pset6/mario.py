import cs50
import sys

def main():
    block = '#'
    space  = ' '
    intInput = 0
    while True:
        print("Please enter a number: ", end="")
        intInput = cs50.get_int()
        if intInput >= 0 and intInput <= 23:
            break
        else:
            continue
        
    for x in range(intInput):
        for t in range(intInput - x):
            print(space, end="")
        for y in range(x + 1):
            print(block, end="")
        print("  ", end="")
        for r in range(x + 1):
            print(block, end="")

        print("")
        
        
        
if __name__ == "__main__":
    main()