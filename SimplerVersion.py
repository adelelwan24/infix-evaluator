from decimal import Decimal as D
class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def Push(self, value):
        self.items.insert(len(self.items),value)

    # Pre: Check if the stack not empty.
    def Pop(self):
        popped = self.items[-1]
        del(self.items[-1])
        return popped

    # Pre: Check if the stack not empty.
    def Peak(self):
        return self.items[-1]
    def Size(self):
        return len(self.items)
    def Print(self):
        for i in (self.items):
            print(i)


def doMath(op, opr2, opr1):
    if op == '+':
        return D(opr1) + D(opr2)
    elif op == '-':
        return D(opr1) - D(opr2)
    elif op == '*':
        return D(opr1) * D(opr2)
    elif op == '/':
        if opr2 == '0':
            print("MATH ERROR")
            exit()
        return D(opr1) / D(opr2)
    else:
        return D(opr1) ** D(opr2)

def math(op,num):
    return doMath(op.Pop(), num.Pop(), num.Pop())

# A function to evaluate infix expression.
def infixEval(strinput):
    strinput = strinput.split()
    # initializing stackes
    num = Stack()
    op = Stack()
    precd = {
        '^': 4,
        '*': 3,
        '/': 3,
        '+': 2,
        '-': 2,
        '(': 1,
        ')': 1
    }
    # Doing operations
    for i in strinput:
        if i not in '+-*/^()':
            num.Push(i)
        
        # This line was removed as we assume we put perfect input 

        elif op.isEmpty():
            op.Push(i)
        # Special case (parenthesis)
        elif i == ')':
            while not op.Peak() == '(':
                num.Push(math(op,num))
            op.Pop() #to pop the ')'
        # General case (Left to right)
        # i kept the == ^ as i can get some thing like this right 2 ^ 3.2 ^ 2
        elif precd[i] > precd[op.Peak()] or i == '(' or i == '^':
            op.Push(i)
        else:
            while not op.isEmpty() and precd[i] <= precd[op.Peak()]:
                num.Push(math(op,num))
            op.Push(i)
    

    # Calculating remaining operations.
    while not op.isEmpty():
        num.Push(math(op,num))
    return num.Pop()

if __name__ == '__main__':
    print(infixEval("( ( 2 + 4 ) + 5 ^ 2 ) - 4 * 2 "))                 #23
    print(infixEval(" 5 * 2 - 5 * 3 + 1 "))                            #-4 in left to right <==> -6 in right to left ( evidince that the program runs LTR)
    print(infixEval("4 ^ 6 / 2 - 4"))                                  #2044
    print(infixEval("-5 - 2"))                                         #-7
    print(infixEval("2 - ( -5 - 2 ) * -2"))                            #-12
    print(infixEval("-10 + ( 20 - 50 * 10 ) * 2 ^ 2"))                 #-1930
    print(infixEval("-10 * 2 ^ 2 + ( 20 - 50 * 10 )"))                 #-520
    print(infixEval("( 20 - 2 ^ 5 ) * 12 - 10"))                       #-154
    print(infixEval("2 * 8 ^ 2 ^ 1  - 2"))                             #126
    print(infixEval("2 + 1 - 2"))                                      #1
    print(infixEval("2.4 +  2.3"))                                     #4.7 != 4.69999999 as we used round function on the output
    print(infixEval("2 ^ 3.2 ^ 2"))                                    #1209.3364853
    print(infixEval("1.11111 - -1.8632"))                              #2.97431
    print(infixEval("2 - -2 - 2 + 4"))                                 # 6 in left to right <==> 10 in right to left 


    """
    while True:
        inputb = input('Please enter your infix: ')

        print(infixEval(inputb))
    """