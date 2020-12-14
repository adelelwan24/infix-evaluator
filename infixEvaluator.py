
class Stack:                                # can be replaced by instaling pythonds library ==> from pythonds.basic.stack import Stack
    def __init__(self):
        self.items=[]
    def isEmpty(self):
        return self.items == []
    def push(self,item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()
    def peek(self):
        return self.items[-1]
    def size(self):
        return len(self.items)

def infixEvaluator(infix):
    infix = spaces(infix).split()
    opStack = Stack()                                                       # Operation stack 
    valueStack = Stack()                                                    # operand stack
    # Dic to give every operation a value so we can compare them
    op={ ")" : 4,"^" : 3,"*" : 2,"/" : 2,"-" : 1,"+" : 1,"(" : 0 }
    for token in infix:
        if token not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+-/^!@#$%&*()_=":          # Take numbers only what ever they were
            # The numbers saved as str in the tokenlist so we have to change them to float so we can do operations on them and can`t set them as int as some data may be lost
            valueStack.push(float(token))                                   
        elif token in "+-*/^()":
            opStack.push(token)

    valueList=[]                                                           # Emty list to store the unused values
    opList=[]                                                              # Emty list to store the unused operations
    while not opStack.isEmpty() and not valueStack.isEmpty():              # cheack The stacks
        op1 = opStack.pop()                                                # Pop one op to compare its order
        v2 = valueStack.pop()     # Pop one value in case the compare was false as we can pop the other values which is gonna be calculated

        # the first part of comparison is in case we are comparing the last operation so it have to be true to get done 
        #  > this comparison make program work from left to right ===> if it was >= the program works from right to left  
        if opStack.isEmpty() or op[op1] > op[opStack.peek()] :
            if op1 == ")" :
                if opStack.peek() == "(":                                   # To see the next operation and act on that info
                    valueStack.push(v2)                                     # get the poped value back to stack so we can do true operation on it
                    opStack.pop()                                           # To get rid of the "(" and continue the program
                    while len(opList) != 0:opStack.push(opList.pop())                                    
                    while len(valueList) != 0:valueStack.push(valueList.pop())    
                else:
                    valueStack.push(v2)                                     # get the poped value back to stack so we can do true operation on it
                    opList.append(op1)                                      # save the ")" in the list as we will use it again until the operation in () are done
            else:
                valueStack.push(calculation(op1,valueStack.pop(),v2))       # Push back the result to the value stack so it can be used again
                # As the condition was true we have to get every op and value back to its stack as we can run again
                while len(opList) != 0:opStack.push(opList.pop())                                    
                while len(valueList) != 0:valueStack.push(valueList.pop())
        else:
            if op1 =="^" and opStack.peek() == "^":                         # So we can get this right 4^2^3 =>> 4^(2^3) =>>65536
                valueStack.push(calculation(op1,valueStack.pop(),v2))       # Push back the result to the value stack so it can be used again
                while len(opList) != 0:opStack.push(opList.pop())                                    
                while len(valueList) != 0:valueStack.push(valueList.pop())
            else:                                                              
                opList.append(op1)                                             
                valueList.append(v2)

    return round(valueStack.pop(),10)                                       # To prevent results like this 2.3+2.4 = 4.6999999999999

def calculation(op,n1,n2):                                                  # just to do the math
    if op == "+":
        return(n1 + n2)
    elif op == "-":
        return(n1 - n2)
    elif op == "*":
        return(n1 * n2)
    elif op == "/":
        assert n2 != 0 ,"Zero DIvition Error: Can`t divide by zero"
        return(n1 / n2)
    elif op == "^":
        return(n1 ** n2)
# function that cheak the input spaces and cheak for input errors
def spaces(eq):
    eq = list(eq.replace(" ",""))                                           # to remove any white_spaces in case the use entered mush spaces
    eq.insert(0," ")                                                        # As we dont want index out of range error at the beiginning of list
    eq.append(" ")                                                          # As we dont want index out of range error at the end of list
    output=[]                                                               # The list where we are gonna save our output
    num=[]                                                                  # Where we will save numbers which in sequance until we get the number as entered
    for i in range(len(eq)):
        if eq[i] == "(" and eq[i+1] != ")" and not eq[i+1] in "+*/^" :      # prevent having empty parantheses =>() and prevent having operations like this=> (*2)
            cond = False
            for z in range(i+1,len(eq)-1):                                  # Prevent having one paranthese without its other part
                if eq[z] == ")":
                    cond = True
                    if eq[i-1] in ".0123456789":                            # Aplling the 2(2-1) operatin as its consider as multiplicatin operation
                        output.append("* (")
                    else:
                        output.append("(")
                    break
            assert cond , "Parantheses Error: Can`t run your code please,write it correct."
        elif eq[i] == ")" and eq[i-1] != "(" and not eq[i-1] in "+*/^":
            cond = False
            for z in range(1,i):                                            # Prevent having one paranthese without its other part
                if eq[z] == "(":
                    cond = True
                    output.append(")")
                    break
            assert cond , "Parantheses Error: Can`t run your code please,write it correct."
        elif eq[i] in "-.0123456789":
            if eq[i] == "-" :
                if  eq[i+1] in ".0123456789" and not eq[i-1] in ".0123456789)":
                    num.append("-")                                         # Treat it as sign value
                elif eq[i-1] in ".0123456789)" and eq[i+1] in "-.0123456789(":
                    output.append("-")                                      # Treat it as an operation
                else:                                                       # Prevent having some thing like this 2---2
                    assert False , "Error: Can`t run your code please,write it correct."
            elif eq[i] in "0123456789":
                num.append(eq[i])
            elif eq[i] == "." and eq[i+1] != "." and eq[i-1] != ".":        # Prevent having some thing like this 2..5 :: 2.....5
                num.append(eq[i])
            if not eq[i+1] in ".0123456789":
                a= "".join(num)                                             # if the next index isn`t number or . join the numbers in num list
                output.append(a)                                            # Then add it to the output list as one number
                num.clear()                                                 # Clear the list for the next full number
        elif eq[i] in "*/+^" and (eq[i+1] in "-.0123456789" or eq[i+1] == "(") and (eq[i-1] in ".0123456789" or eq[i-1] == ")"):
            output.append(eq[i])                                            # add the operation to the output list
        elif eq[i] == " ":
            continue
        else:
            assert False , "Error: Can`t run your code please,write it correct."
    return " ".join(output)    
          
if __name__ == '__main__':

    print(infixEvaluator("( ( 2 + 4 ) + 5 ^ 2 ) - 4 * 2 "))                 #23
    print(infixEvaluator(" 5 * 2 - 5 * 3 + 1 "))                            #-4 in left to right <==> -6 in right to left ( evidince that the program runs LTR)
    print(infixEvaluator("4^6/2-4"))                                        #2044
    print(infixEvaluator("-5 - 2"))                                         #-7
    print(infixEvaluator("2-(-5-2 )* -2"))                                  #-12
    print(infixEvaluator("-10 +( 20- 50 * 10 ) * 2 ^ 2"))                   #-1930
    print(infixEvaluator("-10 * 2 ^ 2 + ( 20 - 50 * 10 )"))                 #-520
    print(infixEvaluator("( 20 - 2 ^ 5 ) * 12 - 10"))                       #-154
    print(infixEvaluator("2 * 8 ^ 2 ^ 1        - 2"))                       #126
    print(infixEvaluator("2 + 1 - 2"))                                      #1
    print(infixEvaluator("2.4 +                        2.3"))               #4.7 != 4.69999999 as we used round function on the output
    print(infixEvaluator("2 ^ 3.2 ^ 2"))                                    #1209.3364853
    print(infixEvaluator("2 ^ (3.2 ^ 2)"))                                  #1209.3364853
    print(infixEvaluator("1.11111--1.8632"))                                #2.97431
    print(infixEvaluator("2--2-2+4"))                                       # 6 in left to right <==> 10 in right to left 

    while True:
        inputs = input("Please enter your infix: ")
        print(infixEvaluator(inputs))      
        continuing = input("Continu!! => Enter Y  :::::::::::::::::::::::::::: Exit!! => Enter N ").strip().lower()
        if continuing == "y":
            continue
        elif continuing == " n" :
            break
