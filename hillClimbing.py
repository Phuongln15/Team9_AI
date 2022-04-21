import gym
import numpy as np
import random
from os import system, name
import pygame
from time import sleep
import time
from IPython.display import clear_output




# Define function to clear console window.
def clear(): 
  
    # Clear on Windows.
    if name == 'nt': 
        _ = system('cls')
  
    # Clear on Mac and Linux. (os.name is 'posix') 
    else: 
        _ = system('clear')

# clear()
env = gym.make("Taxi-v3")
env.reset()

class AgentSearch:

    def __init__(self, env):
        self.env = env
        self.initialState = {'state': env.s, 'actions': [], 'isGoal': False, 'children': [] }
        self.actions = [0, 1, 2, 3, 4, 5]
        self.pickUpOptimal = []
        self.shortestPaths = {}
        self.lastState = False
        self.lastNode = None
        self.visitedNodes = 0
        self.hillClimbing(self.initialState, False)
        print(self.visitedNodes)
        print('end')

    def hillClimbing(self, currentNode, hasPickUp):
        self.getChildren(currentNode, hasPickUp)

        if len(currentNode['children']) == 0 or self.lastState:
            return

        # Keep finding the highest Utility - Hill Climbing
        if len(currentNode['actions']) > 0 and currentNode['actions'][-1] == 4:
            # self.visitedStates = []
            self.actionsTaken = currentNode['actions']
            self.shortestPaths = {}
            hasPickUp = True
            print('pickup', currentNode['actions'])
            currentNode['children'] = []
            currentNode['actions'] = []
            self.hillClimbing(currentNode, hasPickUp)

        if len(currentNode['actions']) > 0 and currentNode['actions'][-1] == 5:
            # self.visitedStates = []
            self.actionsTaken = self.actionsTaken + currentNode['actions']
            print(env.P[self.lastNode['state']])
            print('DropOff', self.actionsTaken)
            self.lastState = True
            return
        
        self.lastNode = currentNode
        for child in currentNode['children']:
            self.visitedNodes += 1
            self.hillClimbing(child, hasPickUp)

    def getChildren(self, currentNode, hasPickUp):
        children = []

        for action in self.actions:
            prob, nextState, reward, goal = env.P[currentNode['state']][action][0]
            if currentNode['state'] != nextState:

                if (hasPickUp and action == 5 and reward == 20) or action in [0,1,2,3,4]:
                    newPath = currentNode['actions'] + [action]
                    if nextState not in self.shortestPaths:
                        self.shortestPaths[nextState] = newPath
                        child = {'state': nextState, 'actions': newPath, 'isGoal': goal, 'children': [] }
                        currentNode['children'].append(child)
                    else:
                        if len(newPath) < len(self.shortestPaths[nextState]):
                            self.shortestPaths[nextState] = newPath
                            child = {'state': nextState, 'actions': newPath, 'isGoal': goal, 'children': [] }
                            currentNode['children'].append(child)                      


agent = AgentSearch(env)
actions = agent.actionsTaken

print(actions) 

for action in actions:
    state, reward, done, info = env.step(action)
    # clear()
    env.render()
    # print(f"State: {state}")
    # print(f"Action: {action}")
    # print(f"Reward: {reward}")
    sleep(0.15) # Sleep so the user can see the

