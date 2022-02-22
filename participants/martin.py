from direction import LEFT, UP, RIGHT, DOWN, direction_as_string
from random import randint

def update_coordinates(row, col, direction):
  if direction == LEFT: col -= 1
  elif direction == UP: row -= 1
  elif direction == RIGHT: col += 1
  elif direction == DOWN: row += 1
  return row, col

class AI:
  def __init__(self, search_steps=20):
    self.fields = [['']]
    self.height = 1
    self.width = 1
    self.search_steps=search_steps

  def is_free(self, row, col, direction=None):
    row, col = update_coordinates(row, col, direction)

    if row >= self.height: return False
    if row < 0: return False
    if col >= self.width: return False
    if col < 0: return False

    if self.fields[row][col] == '': return True
    if self.fields[row][col] == 'f': return True
    else: return False

  def update(self, fields):
    self.fields = fields
    self.height = len(fields)
    self.width = len(fields[0])
    self.head_r, self.head_c = 0, 0
    self.food_r, self.food_c = 0, 0
    self.opponent_heads = []
    for i in range(self.height):
      for j in range(self.width):
        if fields[i][j] == 'f':
          self.food_r, self.food_c = i, j
        if fields[i][j] == 'h':
          self.head_r, self.head_c = i, j
        if fields[i][j].startswith('0-'):
          self.opponent_heads.append([i,j])
    for opponent_head_row, opponent_head_col in self.opponent_heads:
      for direction in [UP, LEFT, RIGHT, DOWN]:
        danger_row, danger_col = update_coordinates(opponent_head_row, opponent_head_col, direction)
        if (self.is_free(danger_row, danger_col, direction)):
          fields[danger_row][danger_col] = 'd'


  def explorer_score(self, direction):
    row, col = update_coordinates(self.head_r, self.head_c, direction)
    previous_steps = [[row, col]]
    distance = 0
    search_depth = 20
    for i in range(search_depth):
      safe_directions = []
      for direction in [UP, LEFT, RIGHT, DOWN]:
        next_coordinates = update_coordinates(row, col, direction)
        if self.is_free(row, col, direction) and next_coordinates not in previous_steps:
          safe_directions.append(direction)
      if len(safe_directions) == 0:
        break
      random_direction = safe_directions[randint(0, len(safe_directions) - 1)]
      row, col = update_coordinates(row, col, random_direction)
      previous_steps.append((row, col))
      distance += 1
    if distance == search_depth:
      distance += 40 # bonus for reaching search depth - we assume that there are more free spaces
    return distance


  def snake_distance_score(self, direction):
    row, col = update_coordinates(self.head_r, self.head_c, direction)
    closest_head_distance = self.width + self.height
    for opponent_head in self.opponent_heads:
      opponent_r, opponent_c = opponent_head
      distance = abs(row - opponent_r) + abs(col - opponent_c)
      if distance < closest_head_distance:
        closest_head_distance = distance
    return closest_head_distance ** 0.5

  def food_distance_score(self, direction):
    row, col = update_coordinates(self.head_r, self.head_c, direction)
    distance = abs(row - self.food_r) + abs(col - self.food_c)
    return 1 / (distance + 1) ** 0.2

  def score_direction(self, direction):
    if not self.is_free(self.head_r, self.head_c, direction):
      return -float('inf')
    score = (
      5 * self.snake_distance_score(direction) +
      400 * self.food_distance_score(direction) +
      sum([self.explorer_score(direction) for i in range(self.search_steps)]) / self.search_steps
    )
    print(direction_as_string(direction), score)
    return score

  def decide_direction(self, fields):
    self.update(fields)
    best_score = -1000000
    best_direction = UP
    for direction in [UP, LEFT, RIGHT, DOWN]:
      score = self.score_direction(direction)
      if score > best_score:
        best_score = score
        best_direction = direction
    return best_direction