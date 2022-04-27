# Team9_AI
Team 9 for AI taxi algo 

## A-Star
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


## Genetic Algorithm
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

### Results
Path evolution fails to reliably find a solution. This is due to the dynamic objective function being solved. The start, pick up, and drop off destinations are all variable, so there is no one optimal path that the genetic algorithm can find. Ocassionaly it will get lucky and get initalized in a location with pick up and drop off locations that lie along the evolved path, but as soon as the conditions chage the solution is no longer valid.

Policy evolution fails in other ways. A general policy of state action pairs should be able produce a solution even with a dynamic goal because the goal information is contained within the state. However, with the random initial state a policy that evaluated well once isn't garunteed to perfrom well the next time. Common traps that evolved policies fall into during testing are being initalized into a state that was not previously tested during evolution. this results in suboptimal behavior such as pick ups or drop offs where there is no passenger which causes no state change so the action is repeated indefinetly or looping between two states (move north, move south, repeat). There are potnetial solutions to this problem such as averaging the performance of policies across multiple initalizations during evolution to evluate a policy. However, even without running each policy multiple times during each evaluation, the evolution of policies is too slow to be applied to realistically be effectively applied to a taxi that needs to operate even close to real time.

## Q-Learning/SARSA algorithm


