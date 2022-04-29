Students: Aidan McKnight, Fabio Yeboles Chen, Klaida Azizi, Phuong Linh Nguyen 

# Project - Self-Driving Taxi (Team 9) 

## Overview

Technology has disrupted the traditional Taxi model in the past 5 years by introducing mobility as a service provider. Companies like Uber or Lift have transformed the transportation market using computing platforms to connect customers and drivers. This movement eliminated the bureaucracy and costs involved in the traditional model, where customers had to only use services from licensed drivers and companies. Increasing the competition and eliminating the “middle-man”, made costs more affordable, and improved the quality of services as well. 

### Problem
The disruption of innovation triggered by the car sharing model, without any doubt played a significant role in the democratization of the services. According to public information, in 2021 Uber had 101 million monthly active users worldwide. Considering the size of the global population, this is a huge improvement, however there is still a lot of room for growth. The largest cost and what prevents this model from growing more is the human component represented by the drivers.  Removing the human resource costs involved would commoditize the services to the point that public transportation represents nowadays.  

### Goal
Our goal is to eliminate the human component by designing an agent that can pick up customers and effectively/safely drop them off in their desired locations. 

### Scope
The scope of this project is to create a proof-of-concept agent by using the AI (Artificial Intelligence) concepts learned in class. We have no desire to develop a fully functional application. 

## Algorithms Implementations

### A-Star algorithm
for my parts, Phuong Nguyen
"""Code uses gym-0.9.7 and heapq for priority queue's data container.

Main goal is to find out the best optimized solution for taxi-v2 problem in gym. 
This is performed using search problem for the open AI game taxi.

The state space is a 5x5 grid (open AI represents this grid and the states with numbers from 0-499).
I set the number representation to a coordinate system, with (1,1) at the bottom left, and (5,5) at the top right.

I used A-Star Algorithm to search the state space and get the reward value for each actions.
 A* search is used to compute the optimal path from the start state of the game.

For A-Start search, priority queue is used as data structure to sort open list. 
Manhattan Distance is used as h(heuristic)function.
While searching, if the search point reachs out the goal position then it returns the actions.

For each iteration, it solves taxi-v2 game based on initial gamestate observation.
isPickingUp function determines if it is needed to pick up or drop off. 
CalcActionSeq(X1, X2, pos) function computes optimal action sequence starting at pos, picking up X1, and dropping off at X2."""


### Genetic Algorithm
Solving OpenAI taxi V3 environment with Genetic Search

Two different possible solutions types can be evolved. 
The first solution type is an action path where each action is executed sequentially to get the agent from the start state to te goal state.
The second solution type is a state action policy that informs the agent which action to take in each possible state.

The genetic evolution algorithm is the same for each solution type and has 5 main steps.
Those steps are:
1- Initialization 
2- Evaluation
3- Selection 
4- Crossover 
5- Mutation 

steps 2 - 5 are iterated as many times as needed or allowed by time 

#### Results
Path evolution fails to reliably find a solution. This is due to the dynamic objective function being solved. The start, pick up, and drop off destinations are all variable, so there is no one optimal path that the genetic algorithm can find. Ocassionaly it will get lucky and get initalized in a location with pick up and drop off locations that lie along the evolved path, but as soon as the conditions chage the solution is no longer valid.

Policy evolution fails in other ways. A general policy of state action pairs should be able produce a solution even with a dynamic goal because the goal information is contained within the state. However, with the random initial state a policy that evaluated well once isn't garunteed to perfrom well the next time. Common traps that evolved policies fall into during testing are being initalized into a state that was not previously tested during evolution. this results in suboptimal behavior such as pick ups or drop offs where there is no passenger which causes no state change so the action is repeated indefinetly or looping between two states (move north, move south, repeat). There are potnetial solutions to this problem such as averaging the performance of policies across multiple initalizations during evolution to evluate a policy. However, even without running each policy multiple times during each evaluation, the evolution of policies is too slow to be applied to realistically be effectively applied to a taxi that needs to operate even close to real time.

### Q-Learning/SARSA algorithm

We seek a policy that maximizes the total reward per episode. There are 500 possible states: 25 squares, 5 locations for the passenger and 4 destinations.
In Q learning, a model-free off-policy reinforcement learning algorithm, the agent (Taxi) initally explores the enviornment by taking random actions and populating the Q table using the rewards and penalties that the environment has. The initial phase is Exploration. After a while, the agent starts to use the updated Q table to take actions that will maximize the future reward. After the reward is received, then the agent will again update the Q table and so on. One of the hyper parameters responsible for balancing between exploration and exploitation is the epsilon, where as epsilon decreases, the agent will take more exploitation actions rather than exploration. In the beginning the epsilon value is high hence more exploration but over time, the agent will need to explore less, and start exploiting what it knows instead to secure the maximum reward possible.

Meanwhile SARSA is an on-policy algorithm, meaning the agent's update depends on the next action and as the agent gets trained and the Q table gets updated, the new policy might produce a different next action for the same state s'. In SARSA, the agent can't use past experiences to improve its actions, instead it uses each experience once to update the q-values.

While Q learning and SARSA perform relatively similar comparing to each other, they are much faster and more efficient algorithms than the other search algorithms that explore all possible actions, since the agent is continuously learning and improving.


### Hill Climbing algorithm

The implementation of the Hill Climbing algorithm relies on a breadth first search agent, which creates a tree by looking for valid action that the car can take in each state. The recursion process looks for child states to explore and checks if the current state has reached the goal. If there are no child states, the recursion reaches its base state, whereas if the current state is the goal, the algorithm logs the actions taken to traverse this path.  

The Hill Climbing algorithm comes to play when a goal state is reached. The utility function is looking for optimal paths, which means paths with less actions. Therefore, the search agent keeps memory of the latest optimal path, and it compares the newly found state. If it has a higher utility score (less actions), it saves as the optimal path. Since the environment used in our project can be easily traversed to find the global optimal, Hill Climbing will always find the best solution. In a more realistic scenario, the algorithm would need to implement limits on the iterations to find a good enough solution. 
