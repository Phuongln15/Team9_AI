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
        self.initialState = {'state': env.s,'prevState': None, 'actions': [], 'isGoal': False, 'children': [] }
        self.actions = [0, 1, 2, 3, 4, 5]
        self.actionsTaken = []
        self.visitedStates = []
        self.visitedNodes = 0
        self.hillClimbing(self.initialState)
        print(self.visitedNodes)

    def hillClimbing(self, currentNode):
        currentNode['children'] = self.getChildren(currentNode)

        if len(currentNode['children']) == 0:
            return

        # Keep finding the highest Utility - Hill Climbing
        if len(currentNode['actions']) > 0 and currentNode['actions'][-1] == 4:
            # self.visitedStates = []
            self.actionsTaken = currentNode['actions']
            print('pickup', currentNode['actions'])


        for child in currentNode['children']:
            idChild = str(child['prevState']['state']) + '-' + str(child['state'])
            if child['state'] not in self.visitedStates:
                self.visitedNodes += 1
                self.visitedStates.append(idChild)
                self.hillClimbing(child)



    def getActions(self, node):
        currentNode = node
        actions = []

        while True:

            if currentNode['prevState'] == None:
                break

            actions.append(currentNode['action'])
            currentNode = currentNode['prevState']

        actions.reverse()

        return actions

    def getChildren(self, currentNode):
        children = []

        for action in self.actions:
            prob, nextState, reward, goal = env.P[currentNode['state']][action][0]
            if currentNode['state'] != nextState:

                idChild = str(currentNode['state']) + '-' + str(nextState)

                if idChild not in self.visitedStates:
                    self.visitedStates.append(idChild)
                    actions = currentNode['actions'] + [action]
                    child = {'state': nextState,'prevState': currentNode, 'actions': actions, 'isGoal': goal, 'children': [] }
                    children.append(child)

        return children


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
