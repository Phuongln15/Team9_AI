import gym
import heapq

class PriorityQ:
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)




def SuccState(pos):
  x, y = pos
  l, r, u, d = ((x-1,y), 3), ((x+1,y), 2), ((x,y+1), 1), ((x,y-1), 0)

  if x == 1:
    if y == 5:
      return [r, d]
    elif y == 1:
      return [u]
    elif y == 2:
      return [d, u]
    else:
      return [r, u, d]
  elif x == 2:
    if y == 5:
      return [l, d]
    elif y == 1:
      return [r, u]
    elif y == 2:
      return [r, u, d]
    else:
      return [l, r, u, d]
  elif x == 3:
    if y == 5:
      return [r, d]
    elif y == 1:
      return [l, u]
    elif y == 2:
      return [l, u, d]
    else:
      return [l, r, u, d]
  elif x == 4:
    if y == 5:
      return [l, r, d]
    elif y == 1:
      return [r, u]
    elif y == 2:
      return [r, u, d]
    else:
      return [l, r, u, d]
  else:
    if y == 5:
      return [l, d]
    elif y == 1:
      return [l, u]
    else:
      return [l, u, d]


def GetPos(obs):
  hundreds, tens = (obs - obs % 100) / 100, ((obs % 100) - (obs % 10)) / 10
  return (tens + 2) / 2, 5 - hundreds


#heuristic func
def manhattanDistance(p1, p2):
  return (abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]))

#A* search
def AStar_Search(pos, goal):
  f, visited, best_state = PriorityQ(), set(), {}
  f.push((pos, [], 0), manhattanDistance(pos, goal))

  while not f.isEmpty():

    curP, actions, total_cost = f.pop()

    if curP in visited or \
    (curP in best_state and best_state[curP] <= total_cost):
      continue

    visited.add(curP)
    best_state[curP] = total_cost

    # current vertex is a solution
    if curP == goal:
      return actions

    for (p, action) in SuccState(curP):
      if p not in visited:
        temp_actions = list(actions)
        temp_actions.append(action)
        cost = total_cost + 1
        f.push((p, temp_actions, cost), \
          cost + manhattanDistance(p, goal))

  raise Exception('Can not find path.')


def CalcActionSeq(X1, X2, pos):
  pup = AStar_Search(pos, X1)
  pup.append(4)
  dropoff = AStar_Search(X1, X2)
  dropoff.append(5)
  return pup + dropoff

def FindPickedUp(obs):
  ten_x, one_x = ((obs % 100) - (obs % 10)) / 10, obs % 10
  G, B, Y, R, pos = (5, 5), (4, 1), (1, 1), (1, 5), GetPos(obs)
  if (ten_x % 2) == 1:
    if one_x == 1:
      return (Y, B)
    if one_x == 2:
      return (B, R)
    if one_x == 3:
      return (B, G)
    if one_x == 4:
      return (B, Y)
    if one_x == 6:
      return (None, R)
    if one_x == 7:
      return (None, G)
    if one_x == 8:
      return (None, Y)
    if one_x == 9:
      return (None, B)
  else:
    if one_x == 1:
      return (R, G)
    if one_x == 2:
      return (R, Y)
    if one_x == 3:
      return (R, B)
    if one_x == 4:
      return (G, R)
    if one_x == 6:
      return (G, Y)
    if one_x == 7:
      return (G, B)
    if one_x == 8:
      return (Y, R)
    if one_x == 9:
      return (Y, G)


def Solve(obs):
  pickup, dropoff = FindPickedUp(obs)
  pos = GetPos(obs)
  return CalcActionSeq(pickup, dropoff, pos)


def isPickingUp(obs):
  tens, ones = ((obs % 100) - (obs % 10)) / 10, obs % 10
  if (tens % 2) == 1 and ones >= 5:
    return False
  else:
    return True

if __name__ == "__main__":
  env = gym.make('Taxi-v2')
  correct, iterations = 0, 100
  print("{} iterations".format(iterations))
  for _ in range(iterations):
    obs, rewards = env.reset(), 0
    actions = Solve(obs)
    print('=========')
    print('actions : ', actions)
    print('rewards : ', rewards)
    for action in actions:
      obs, reward, done, _ = env.step(action)
      rewards += reward
    if done and rewards > 0:
      correct += 1
    evn.render()
  print('{}% success'.format(correct*100.0/iterations))
