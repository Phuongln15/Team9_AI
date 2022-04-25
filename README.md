# Team9_AI
Team 9 for AI taxi algo 
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
