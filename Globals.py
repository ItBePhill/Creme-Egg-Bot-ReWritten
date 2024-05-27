#Globals.py 
#Written by Phillip Wood
variables = {}
def Set(name, value):
    global variables
    variables[name] = value

def Get(name):
    return variables[name]

def GetAll():
    return variables