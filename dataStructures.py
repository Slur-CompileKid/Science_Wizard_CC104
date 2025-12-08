# Abstract Data Structure 1: Queue (for managing words to be spelled)
class Queue:
    def __init__(self):
        self.items = []  # initializes an empty lis, Internal list to store items o kat word ngato sa dictionary

    def enqueue(self, item):
        self.items.append(item)  # Add item to the end, kung gadugang euman it additional words

    def dequeue(self):   #para if magskip maproceed sa next word
        if not self.is_empty():
            return self.items.pop(0)  # Remove and return from the front, kung maproceed eon sa next word

    def is_empty(self):
        return len(self.items) == 0  # Check if empty, kung may habilin pabang words nga napaspell nana

#  Ro first word nga una mapush sa list, dato ro una nanang idisplay para ispell

# Abstract Data Structure 2: Stack (for tracking user attempts)
class Stack:
    def __init__(self):
        self.items = []  # Internal list to store items, kung nakasabat eon imaw kara masueod ra attempts it pagsabat either tama o mali

    def push(self, item):
        self.items.append(item)  # Add item to the top, After each spelling attempt, the result is stored.

    def pop(self):
        if not self.is_empty():
            return self.items.pop()  # Remove and return from the top, To undo or review the last attempt.

    def is_empty(self):
        return len(self.items) == 0  # Check if empty, if wa eon syempre bawas eon sa attempts

    def peek(self):
        if not self.is_empty():
            return self.items[-1]  # View the top item without removing, nacheck do last answer without changing the stack