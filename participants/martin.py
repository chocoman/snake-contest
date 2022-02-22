from direction import LEFT, UP, RIGHT, DOWN, direction_as_string

def update_coordinates(row, col, direction):
  if direction == LEFT: col -= 1
  elif direction == UP: row -= 1
  elif direction == RIGHT: col += 1
  elif direction == DOWN: row += 1
  return row, col

class AI:
  def __init__(self):
    self.fields = [['']]
    self.height = 1
    self.width = 1

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
    opponent_names = []
    snake_names = []
    for i in range(self.height):
      for j in range(self.width):
        if fields[i][j] == 'f':
          self.food_r, self.food_c = i, j
        if fields[i][j] == 'h':
          self.head_r, self.head_c = i, j
        if fields[i][j].startswith('0-'):
          name = fields[i][j][2:]
          opponent_names.append(name)
          self.opponent_heads.append([i,j])
        if fields[i][j].startswith('1-'):
          name = fields[i][j][2:]
          snake_names.append(name)
    for name in snake_names:
      if name not in opponent_names:
        self.my_name = name

  def snake_distance_score(self, direction):
    row, col = update_coordinates(self.head_r, self.head_c, direction)
    closest_head_distance = self.width + self.height
    for opponent_head in self.opponent_heads:
      opponent_r, opponent_c = opponent_head
      distance = abs(row - opponent_r) + abs(col - opponent_c)
      if distance < closest_head_distance:
        closest_head_distance = distance
    print(f'closest snake: {closest_head_distance}')
    return closest_head_distance

  def food_distance_score(self, direction):
    row, col = update_coordinates(self.head_r, self.head_c, direction)
    distance = abs(row - self.food_r) + abs(col - self.food_c)
    return 1 / (distance + 1) ** 0.2

  def wall_distance_score(self, direction):
    row, col = update_coordinates(self.head_r, self.head_c, direction)
    if not self.is_free(row, col):
      return -1000000
    closest_wall_distance = min(
      row,
      col,
      self.width - col,
      self.height - row,
    )
    for i in range(self.height):
      for j in range(self.width):
        if self.is_free(i, j):
          continue # skip fields that are not walls
        if (self.fields[i][j] == 'h'):
          continue
        distance = abs(row - i) + abs(col - j)
        if (self.fields[i][j].endswith('-' + self.my_name)):
          piece_number = int(self.fields[i][j][:-len(self.my_name)-1])
          if piece_number <= distance + 1:
            # don't count pieces from my own neck.
            # If distant parts of my neck are close to my head, they count
            continue 
        if distance < closest_wall_distance:
          closest_wall_distance = distance
    return closest_wall_distance

  def score_direction(self, direction):
    if not self.is_free(self.head_r, self.head_c, direction):
      return -float('inf')
    opponents_count = len(self.opponent_heads)
    score = (
      opponents_count * self.snake_distance_score(direction) +
      (opponents_count + 0.1) * self.wall_distance_score(direction) +
      50 * self.food_distance_score(direction)
    )
    print(direction_as_string(direction), score)
    return score



  # Funkce dostane seznam seznamů stringů fields. Záznam fields[i][j] říká,
  # co je na políčku na řádku i ve sloupci j. Možné hodoty jsou 'f', což značí jídlo,
  # prázdný string '' což značí prázdné pole, 'h' značí hlavu hada, pro nějž se rozhodujete
  # a cokoli dalšího znamená tělo nějakého hada. To je záznam ve formátu '4-arnost'.
  # Číslo před pomlčkou značí, o kolikátý díl těla se jedná (hlava je 0) a zbytek za pomlčkou
  # je jméno daného hada.
  # Tuto funkci můžete libovolně upravit. Jenom zachovejte její název a vstupní parametry
  # a vracejte jedině jednu z hodnot LEFT, UP, RIGHT, DOWN
  # Můžete přidat jakékoli další funkce.
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