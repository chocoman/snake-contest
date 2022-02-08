from direction import LEFT, UP, RIGHT, DOWN

class AI:
  def __init__(self):
    self.fields = [['']]
    self.height = 1
    self.width = 1

  def is_free(self, row, col, direction=None, distance=1):
    if direction == LEFT: col -= distance
    elif direction == UP: row -= distance
    elif direction == RIGHT: col += distance
    elif direction == DOWN: row += distance

    if row >= self.height: return False
    if row < 0: return False
    if col >= self.width: return False
    if col < 0: return False

    if self.fields[row][col] == '': return True
    if self.fields[row][col] == 'f': return True
    else: return False

  def is_free_further(self, row, col, direction=None, distance=1):
    x = 1
    for i in range(1, distance):
      if self.is_free(row, col, direction, i): x += 1

    if x == distance: return True
    else: return False

  def check_food_next_to_wall(self, width, height, row, col, direction=None):
    width += 1
    height += 1

    if direction == LEFT:col -= 1
    elif direction == UP: row -= 1
    elif direction == RIGHT: col += 1
    elif direction == DOWN: row += 1

    if row >= self.height: return False
    if row < 0: return False
    if col >= self.width: return False
    if col < 0: return False
    if self.fields[row][col] != 'f': return False

    if direction == LEFT: col -= 1
    elif direction == UP: row -= 1
    elif direction == RIGHT: col += 1
    elif direction == DOWN: row += 1

    if self.fields[row] == -1 or self.fields[row] == width: return True
    if self.fields[col] == -1 or self.fields[col] == height: return True
    return False



  def random_safe_direction(self, head_row, head_col):
    if self.is_free(head_row, head_col, LEFT):
      return LEFT
    if self.is_free(head_row, head_col, UP):
      return UP
    if self.is_free(head_row, head_col, RIGHT):
      return RIGHT
    if self.is_free(head_row, head_col, DOWN):
      return DOWN

  def decide_direction(self, fields):
    self.fields = fields
    self.height = len(fields)
    self.width = len(fields[0])
    head_row, head_col = 0, 0
    food_row, food_col = 0, 0
    for i in range(self.height):
      for j in range(self.width):
        if fields[i][j] == 'f':
          food_row, food_col = i, j
        if fields[i][j] == 'h':
          head_row, head_col = i, j

    for a in range(4, 1, -1):
      if food_col < head_col:
        if self.is_free_further(head_row, head_col, LEFT, a) or self.check_food_next_to_wall(self.width, self.height, head_row, head_col, LEFT):
          return LEFT
      if food_row < head_row:
        if self.is_free_further(head_row, head_col, UP, a) or self.check_food_next_to_wall(self.width, self.height, head_row, head_col, UP):
          return UP
      if food_col > head_col:
        if self.is_free_further(head_row, head_col, RIGHT, a) or self.check_food_next_to_wall(self.width, self.height, head_row, head_col, RIGHT):
          return RIGHT
      if food_row > head_row:
        if self.is_free_further(head_row, head_col, DOWN, a) or self.check_food_next_to_wall(self.width, self.height, head_row, head_col, DOWN):
          return DOWN
    
    for b in range(3, 1, -1):
      if self.is_free_further(head_row, head_col, LEFT, b): return LEFT
      if self.is_free_further(head_row, head_col, UP, b): return UP
      if self.is_free_further(head_row, head_col, RIGHT, b): return RIGHT
      if self.is_free_further(head_row, head_col, DOWN, b): return DOWN

    return self.random_safe_direction(head_row, head_col)
