from tkinter import *
import math 

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


root = Tk()
root.title("Calculator")
root.geometry("230x270+350+100")
root.config(bg="#aaa",relief=RAISED)
root.resizable(False,False)
# root.iconbitmap(r"C:\Users\DELL\Downloads\keys.ico")
root.minsize(230,270)

root.columnconfigure(0,pad = 10,weight=1)
root.columnconfigure(1,pad = 10,weight=1)
root.columnconfigure(2,pad = 10,weight=1)
root.columnconfigure(3,pad = 30,weight=1)
root.columnconfigure(4,pad = 10,weight=1)


root.rowconfigure(0,pad = 3,weight=10)
root.rowconfigure(1,pad = 3,weight=1)
root.rowconfigure(2,pad = 3,weight=1)
root.rowconfigure(3,pad = 3,weight=1)
root.rowconfigure(4,pad = 3,weight=1)
root.rowconfigure(5,pad = 3,weight=1)
root.rowconfigure(6,pad = 3,weight=1)
root.rowconfigure(7,pad = 0,weight=1)


text = Entry(root,relief=FLAT,font=(20),bg="#fff")
text.grid(row=0,columnspan=4,sticky=W+E+N+S,pady=(8,5),padx=5)
text.bind("<Key>", lambda e: "break")

def write_number(number):
    current = text.get()
    text.delete(0,END)
    text.insert(-1,current + str(number))

def  clear_function():
    text.delete(0,END)

def delete_one():
    data = len(text.get())
    text.delete(data-1,END)

def print_onscreen(data):
    text.delete(0,END)
    text.insert(0,data)
#================================================================ Evaluator ===================================================================

def SqrRoot_value():
    value = text.get()
    text.delete(0,END)
    text.insert(0,math.sqrt(float(value)))

def fact():
    data = math.factorial(int(text.get()))
    text.delete(0,END)
    text.insert(0,data)
    # data = int(text.get())
    # count = data
    # while data > 1:
    #     data = -1
    #     cout = count * data
    # text.delete(0,END)
    # text.insert(0,count)

def Evaluator():
    infix = spaces(list(text.get())).split()
    opStack = Stack()                                                       # Operation stack 
    valueStack = Stack()                                                    # operand stack
    # Dic to give every operation a value so we can compare them
    op={ ")" : 4,"^" : 3,"%" : 2,"*" : 2,"/" : 2,"-" : 1,"+" : 1,"(" : 0 }
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
    text.delete(0,END)
    text.insert(0,round(valueStack.pop(),10))                                       # To prevent results like this 2.3+2.4 = 4.6999999999999

def calculation(op,n1,n2):                                                  # just to do the math
    if op == "+":
        return(n1 + n2)
    elif op == "-":
        return(n1 - n2)
    elif op == "*":
        return(n1 * n2)
    elif op == "/":
        assert n2 != 0 ,print_onscreen("Zero Divition Error: Can`t divide by zero")
        return(n1 / n2)
    elif op == "^":
        return(n1 ** n2)
    elif op == "%":
        return(n1 % n2)
# function that cheak the input spaces and cheak for input errors
def spaces(eq):
    eq.insert(0," ")                                                        # As we dont want index out of range error at the beiginning of list
    eq.append(" ")                                                          # As we dont want index out of range error at the end of list
    output=[]                                                               # The list where we are gonna save our output
    num=[]                                                                  # Where we will save numbers which in sequance until we get the number as entered
    for i in range(len(eq)):
        if eq[i] == "(" and eq[i+1] != ")" and not eq[i+1] in "+*/^%" :      # prevent having empty parantheses =>() and prevent having operations like this=> (*2)
            cond = False
            for z in range(i+1,len(eq)-1):                                  # Prevent having one paranthese without its other part
                if eq[z] == ")":
                    cond = True
                    if eq[i-1] in ".0123456789":                            # Aplling the 2(2-1) operatin as its consider as multiplicatin operation
                        output.append("* (")
                    else:
                        output.append("(")
                    break
            assert cond , print_onscreen("Parantheses Error: Can`t run your code please,write it correct.")
        elif eq[i] == ")" and eq[i-1] != "(" and not eq[i-1] in "+*/^%":
            cond = False
            for z in range(1,i):                                            # Prevent having one paranthese without its other part
                if eq[z] == "(":
                    cond = True
                    output.append(")")
                    break
            assert cond , print_onscreen("Parantheses Error: Can`t run your code please,write it correct.")
        elif eq[i] in "-.0123456789":
            if eq[i] == "-" :
                if  eq[i+1] in ".0123456789" and not eq[i-1] in ".0123456789)":
                    num.append("-")                                         # Treat it as sign value
                elif eq[i-1] in ".0123456789)" and eq[i+1] in "-.0123456789(":
                    output.append("-")                                      # Treat it as an operation
                else:                                                       # Prevent having some thing like this 2---2
                    assert False , print_onscreen("Error: Can`t run your code please,write it correct.")
            elif eq[i] in "0123456789":
                num.append(eq[i])
            elif eq[i] == "." and eq[i+1] != "." and eq[i-1] != ".":        # Prevent having some thing like this 2..5 :: 2.....5
                num.append(eq[i])
            if not eq[i+1] in ".0123456789":
                a= "".join(num)                                             # if the next index isn`t number or . join the numbers in num list
                output.append(a)                                            # Then add it to the output list as one number
                num.clear()                                                 # Clear the list for the next full number
        elif eq[i] in "*/+^%" and (eq[i+1] in "-.0123456789" or eq[i+1] == "(") and (eq[i-1] in ".0123456789" or eq[i-1] == ")"):
            output.append(eq[i])                                            # add the operation to the output list
        elif eq[i] == " ":
            continue
        else:
            assert False , print_onscreen("Error: Can`t run your code please,write it correct.")
    return checkvalidity(" ".join(output))

def checkvalidity(sourcefile):                                              # cheack the balance of prantheses
    
    s= Stack()
    for token in sourcefile:
        if token == "(":
            s.push(token)
        elif token == ")":
            print_onscreen("prantheses are no balanced") if s.isEmpty() else s.pop()
    return sourcefile if s.isEmpty() else print_onscreen("prantheses are no balanced")
        
        
# ================================================================= end of evaluation ===========================================================

oas = Button(root,text="^",font =("serial",10),bg="#430",fg="#fff",command =lambda:write_number('^')).grid(row=1,column=0,sticky=W+E)
factorial_val = Button(root,text="!",font =("serial",10),bg="#430",fg="#fff",command = fact).grid(row=1,column=2,sticky=W+E)
rooot = Button(root,text="Root",font =("serial",10),bg="#430",fg="#fff",command = SqrRoot_value).grid(row=1,column=1,sticky=W+E)
back = Button(root,text="back",font =("serial",10),bg="#333",fg="#fff",command = delete_one).grid(row=1,column=3,padx=(5,0),sticky=W+E)

pran_left = Button(root,text="(",font =("serial",10),bg="#430",fg="#fff",command =lambda:write_number('(')).grid(row=2,column=0,sticky=W+E)
pranrigh = Button(root,text=")",font =("serial",10),bg="#430",fg="#fff",command =lambda:write_number(')')).grid(row=2,column=1,sticky=W+E)
modulus = Button(root,text="  %  ",font =("serial",10),bg="#430",fg="#fff",command = lambda:write_number("%")).grid(row=2,column=2,sticky=W+E)
clear = Button(root,text="CLS ",font =("serial",10),bg="#333",fg="#fff",command =clear_function).grid(row=2,column=3,padx=(5,0),sticky=W+E)

num7 = Button(root,text="  7  ",font =("serial",10),bg="#234",fg="#fff",command =lambda:write_number(7)).grid(row=3,column=0,sticky=W+E)
num8 = Button(root,text="8",font =("serial",10),bg="#234",fg="#fff",command =lambda:write_number(8)).grid(row=3,column=1,sticky=W+E)
num9 = Button(root,text="9",font =("serial",10),bg="#234",fg="#fff",command =lambda:write_number(9)).grid(row=3,column=2,sticky=W+E)
mul = Button(root,text="*",font =("serial",10),bg="#784",fg="#fff",command =lambda:write_number('*')).grid(row=3,column=3,padx=(5,0),sticky=W+E)

num4 = Button(root,text="4",font =("serial",10),bg="#234",fg="#fff",command =lambda:write_number(4)).grid(row=4,column=0,sticky=W+E)
num5 = Button(root,text="5",font =("serial",10),bg="#234",fg="#fff",command =lambda:write_number(5)).grid(row=4,column=1,sticky=W+E)
num6 = Button(root,text="6",font =("serial",10),bg="#234",fg="#fff",command =lambda:write_number(6)).grid(row=4,column=2,sticky=W+E)
div = Button(root,text="/",font =("serial",10),bg="#784",fg="#fff",command =lambda:write_number('/')).grid(row=4,column=3,padx=(5,0),sticky=W+E)

num1 = Button(root,text="1",font =("serial",10),bg="#234",fg="#fff",command =lambda:write_number(1)).grid(row=5,column=0,sticky=W+E)
num2 = Button(root,text="2",font =("serial",10),bg="#234",fg="#fff",command =lambda:write_number(2)).grid(row=5,column=1,sticky=W+E)
num3 = Button(root,text="3",font =("serial",10),bg="#234",fg="#fff",command =lambda:write_number(3)).grid(row=5,column=2,sticky=W+E)
plus = Button(root,text="+",font =("serial",10),bg="#784",fg="#fff",command =lambda:write_number('+')).grid(row=5,column=3,padx=(5,0),sticky=W+E)

point = Button(root,text=".",font =("serial",10),bg="#789",fg="#fff",command =lambda:write_number('.')).grid(row=6,column=0,sticky=W+E)
num0 = Button(root,text="0",font =("serial",10),bg="#234",fg="#fff",command =lambda:write_number(0)).grid(row=6,column=1,sticky=W+E)
pi = Button(root,text="pi",font =("serial",10),bg="#789",fg="#fff",command =lambda:write_number(3.14)).grid(row=6,column=2,sticky=W+E)
minus = Button(root,text="-",font =("serial",10),bg="#784",fg="#fff",command =lambda:write_number('-')).grid(row=6,column=3,padx=(5,0),sticky=W+E)


equal = Button(root,text="=",borderwidth=5,font =("serial",10),bg="#432",fg="#fff",command = Evaluator).grid(row=7,columnspan=4,sticky=W+E)

root.mainloop()
