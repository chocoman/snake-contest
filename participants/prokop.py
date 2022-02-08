from direction import LEFT, UP, RIGHT, DOWN

class AI:
  def __init__(self):
    self.fields = [['']]
    self.height = 1
    self.width = 1

  def is_free(self, row, col, direction=None):
    if direction == LEFT: col -= 1
    elif direction == UP: row -= 1
    elif direction == RIGHT: col += 1
    elif direction == DOWN: row += 1

    if row >= self.height: return False
    if row < 0: return False
    if col >= self.width: return False
    if col < 0: return False

    if self.fields[row][col] == '': return True
    if self.fields[row][col] == 'f': return True
    else: return False
    
  def free_tiles_count(self, row, col, direction=None):
    if direction == LEFT: col -= 1
    elif direction == UP: row -= 1
    elif direction == RIGHT: col += 1
    elif direction == DOWN: row += 1
    
    directions = [LEFT, RIGHT, UP, DOWN]
    count = 0
    
    for examined_direction in directions:
      examined_row = row
      examined_col = col
      if self.is_free(examined_row, examined_col, examined_direction):count+= 1
    #print(count)
    return count

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
    self.fields = fields
    self.height = len(fields)
    self.width = len(fields[0])
    
    nearby_tiles =  []
    snake_heads = []    
    
    head_row, head_col = 0, 0
    food_row, food_col = 0, 0
    snake_head_row, snake_head_col = 0,0
    
    for i in range(self.height):
      for j in range(self.width):
        if fields[i][j] == 'f':
          food_row, food_col = i, j
          
        elif fields[i][j] == 'h':
          head_row, head_col = i, j
          
          for i in range(-1,2):
            for j in range (-1,2):
              nearby_tiles.append([i, j])
        elif fields[i][j].startswith("0"):
          snake_heads.append([i,j])
    print(self.free_tiles_count(head_row, head_col, UP))      
      
    if self.food_close(head_row, head_col,food_row, food_col):
      return self.seek_food(head_row, head_col, food_row, food_col)
    return self.idle(head_row, head_col)
    
    

  def seek_food(self, head_row, head_col,food_row, food_col):
    print('seek food')
    for free_tiles in range(3, -1, -1):
      for direction in [LEFT, RIGHT, UP, DOWN]:
        is_direction_good = (
          self.is_food_in_direction(head_row, head_col, food_row, food_col, direction)
          and self.is_free(head_row, head_col, direction)
          and self.free_tiles_count(head_row, head_col, direction) == free_tiles
        )
        #print(free_tiles)
        if is_direction_good: return direction
    return self.idle(head_row, head_col)

    
  def idle(self, head_row, head_col):
    print("idle")
    for free_tiles in range(3, -1, -1):
      for direction in [LEFT, RIGHT, UP, DOWN]:
        is_direction_good = (
          self.is_free(head_row, head_col, direction)
          and self.free_tiles_count(head_row, head_col, direction) == free_tiles
        )
        print(free_tiles)
        if is_direction_good: return direction
      
    print('PANIC!!!')
    return RIGHT
  
  
  def closest(self, head_row, head_col, snake_heads):
    closest = snake_heads[0]
    for snake in snake_heads:
      if (self.distance(head_row, head_col, snake[0], snake[1]) < self.distance(head_row, head_col, closest[0], closest[1])):
        closest = snake
    return closest
        
  def food_close(self, head_row, head_col, food_row, food_col):
    if (self.distance(head_row, head_col, food_row, food_col) < 10):
      return True
    else:
      return False
      
  def is_food_in_direction(self, head_row, head_col, food_row, food_col, direction):
    if direction == UP:
      if (food_row < head_row):
        return True
    if direction == DOWN: 
      if (food_row > head_row):
        return True
    if direction == LEFT:
      if (food_col < head_col):
        return True
    if direction == RIGHT: 
      if (food_col > head_col):
        return True
    return False
      
  def snakes_close(self, head_row, head_col, snake_heads):
    for snake in snake_heads:
      if (self.distance(head_row, head_col, snake[0], snake[1]) < 20):
        return True
    else:
      return False
      
  def distance(self, a_row, a_col, b_row, b_col):
    return ((a_row - b_row)**2 + (a_col-b_col)**2)**0.5
'''
    if self.snakes_close(head_row, head_col, snake_heads):
      snake_head_row, snake_head_col = self.closest(head_row, head_col, snake_heads)[0],self.closest(head_row, head_col, snake_heads)[1]
      if snake_head_row < head_row and self.is_free(head_row, head_col, UP):
        return UP
      elif snake_head_col < head_col and self.is_free(head_row, head_col, LEFT):
        return LEFT
      elif snake_head_row > head_row and self.is_free(head_row, head_col, DOWN):
        return DOWN
      elif snake_head_col > head_col and self.is_free(head_row, head_col, RIGHT):
        return RIGHT
        '''
