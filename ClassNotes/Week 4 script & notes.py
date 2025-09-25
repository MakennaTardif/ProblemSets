# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 14:40:36 2025

@author: tinne
"""

#A python script saves as .py (this is my first comment)

myVar="hello world"    #writing hello to myVar

#For Loops runs for a preset number of times (i.e., if I know I have 100 trials, I would want it to run 100 times)

#While loops repeat as long as ann expression is true (as soon as it is false, the loop will stop)

#For Loops


for i in range(1,5):             #Has to end in a colon
    print ("I am in the loop")   #Everything after needs to be indented
    print(i)           
    
print ("I am out of the loop")

#What happened after we ran the above? It created a variable (i) with a value of 4 (i.e., ranges are non-inclusive)

for i in range(1,5):
    print ("I am in the loop")
print ("what is this")
    print(i)
    
    #We got an unexpected intent syntax error (print(what is this) was the end of the loop)
    
for i in range(1,5):
    print ("I am in the loop")
print ("what is this")           # Non indented line again stops the loop
print(i)                         # Exists as 4 after the loop 

print ("I am out of the loop")

#New loop
mylist= ["apple", "banana", "cherry"]  #this is my list I created
for x in mylist:                       #x will take the name of each thing in the loop (i.e., values x iderates over)
    print(x)
    
mylist= ["apple", "banana", "cherry"]  
for x in range(len(mylist))            #based on the existence of a separate list
    print(mylist[x])
    
#While loops

i = 1
while i < 6:
    print(i)
    i += 1        #Incredmented by 1 each time (i.e., take current value of variable and add __)
    
                  #This printed (i) 6 times (1+1 =2, 2 is less than 6, run again, etc)
                  #You could get stuck in an infite loop 
               
i = 1            #Do not run this (control c in terminal will get your out the infinite loop)
while i < 2:
    print(i)    
    

if i ==3:         #Exit of the loop entirely 
    break         #If this happens, exit loop (even if the conditions have not been met) 
    
i = 0             #Continue command: This skipped 3 and printed 1,2,4,5,6
while i < 6:     
    i += 1
    if i == 3:      
        continue  #Fast forward to the next ideration of the loop
    print(i)
    
#Scope of a variable

     #area of the code that a variable is visible and accessible (i.e., at what level can  we access that information)
     #if variables are declared within a while or for loop, their scope exists inside the loop and nothing above it (i.e., local scope)
     #In global scope, all entities are visible throughout the entire program
     
#Python libraries

       #Adding libraries to our scripts, we can expand on it's capabilities
       #Most come from packaged libraries(e.g., PsychoPy)
       #Adds them into the  exitsing ideration
       
import numpy           #imports the library (i.e., nothing happens when you do this in the console)
numpy.sqrt             #Calling method/function within the package
import numpy as np     #Changes the name (i.e., shorthand)

from math import cos, pi   #This imports parts of the library you specify
print('cos(pi) is', cos(pi))

#Random library method

     #This is the most common libraries we will use
     # E.g., randomizing stimuli, simulating data, conditions, time, etc.
     # Random number generators (RNGs) - tied to a seed
     # Can set your seed to a specific value or get the 'state' of the RNG at a particular point in time
     
# Exercise as a class

import random          #importing random library
help(random)           #help files here too

help(random.randint)    #help on method
       
random.randint(0,10)    #everytime you do this in the console, you get different numbers
   
print(random.getstate())   #gives state of my current RNG

myState = random.getstate()  #creates a tuple

random.setstate(myState)   

random.seed(1)          #Can seed your RNG (replicating things that are otherwise random)
 
random.(tab)            # Will autocomplete the commands (i.e., it knows what exists within that library)

random.normalvariate    #Random instance. Normal distribution (,u is the mean, and sigman is the SD)


#Functions

       # Increase efficiency by repeating blocks of code
       # Modular bits of code that carry out a task or peration
       # Can be called repeatedly throughout your code
       # Can take arguments (inputs) and can return values 
       
print()     #Is a function we know already

def nameprintfunc(name):           #brackets are the arguments does this function take (i.e., name does not need to exist/we are defining it)
    
    print('The name is' + name)
    return name                    #This does nothing 
                                   #But if you type name and tab, it will now recognize it as a function

nameprintfunc('Steve')            

myName = nameprintfunc('Steve')    

def adderFunc(val):            #Made a new function (saved and exists)
    x = val + val              # x = value plus value
    print(x)
    
      #scope applys to functions (x is local to this function)(unreadable outside this function)
      # if you try to print x (i.e., create a variable and print it), you will get "none"
      #because it does not exist outside the function
    
def adderFunc(val):            
x = val + val              
    print(x)
    return x          #until I return x and assign it to a variable, it only exists locally
                      #once you do this, you can access it globally 
    
     #can also make some arguments optional
     
def adderFunc(val1, val2 =4):
    x = val1 + val2            #value 1 is optional, and if a second is not added - automatically add 4)
    return x


    #can also return multiple values 
    
def adderFunc(val1, val2 =4):
    x = val1 + val2 
    y = (val1 + val2) * 2
    return(x, y)

#Help Function directly in your code

def adderFunc(val1, val2 =4):         #adds a help functiom right into your code (triple quotes for a multi comment)
    """ Adds two numbers together
    
    
    
    """
    x = val1 + val2 
    y = (val1 + val2) * 2
    return(x, y)

# Classes

     #Way of combining data and functionality 
     #Flexibility in code and reuse common procedures
     #A class has attributes(data) and methods(operations that can be performed on the data
     #Can create multiple instances of that class (in each has attributes and methods)
     
class car: 
    
    def __init__(self, color='white'):    #initialize attributes of every instance of the class
        self.speed = 0                    #self allows you to access variable from anywhere else in class
        self. color = color               #color is defined as an (option input)
    
    def drive(self):                       #a method for the object
        self.speed = self.speed + 1
        
    def breaking(self):
        self.speed = self.speed -1
        
vw = car()                              #creating an instance of car -own special variable (only on object cars)
toyota = car ('green')

carList = [car() for x in range (0,5)]

carList[2].color 

      #Classes can be created in a separate file (i.e., then import/call that into another script)
      #You can do this with the convent below
      
from filename import class 

