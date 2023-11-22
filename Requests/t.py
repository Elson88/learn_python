import sys


if __name__ == '__main__': # This line checks if the script is being run as the main program and not imported as a module.
    N = int(input())       # Reads an integer N from the user. This value is used to determine how many iterations the subsequent loop will run.
    l = []                 #  Initializes an empty list l. This list will be modified based on the user's input.
    for i in range(N):     # A loop that iterates N times. In each iteration, the user is prompted for input.
        s = list(input().split()) # Reads a line from the user, splits it into a list of strings using spaces, and assigns it to the variable s.
        # Example
        #User input: insert 0 5
        # s will be ['insert', '0', '5']
        # Conditional statements (if statements) that check the value of s[0] (the first element of the list).
        if s[0]=='insert':      # Inserts an element into the list at a specified index
            l.insert(int(s[1]),int(s[2]))
        if s[0]=='remove':      # Removes the first occurrence of a specified value from the list.
            l.remove(int(s[1]))
        if s[0]=='append':      # Appends a specified value to the end of the list.
            l.append(int(s[1]))
        if s[0]=='sort':        # Sorts the list in ascending order.
            l.sort()
        if s[0]=='pop':         # Removes and returns the last element from the list.
            l.pop()
        if s[0]=='reverse':     # Reverses the elements of the list.
            l.reverse()     
        if s[0]=='print':       # Prints the current state of the list.
            print(l)
            
        # EXAMPLE
        # If s = ['insert', '0', '5']:
        # l will be modified based on the 'insert' operation.