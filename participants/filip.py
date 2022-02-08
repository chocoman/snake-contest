from direction import LEFT, UP, RIGHT, DOWN
from participants import martin, filip

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
    head_row, head_col = 0, 0
    food_row, food_col = 0, 0
    for i in range(self.height):
      for j in range(self.width):
        if fields[i][j] == 'f':
          food_row, food_col = i, j
        if fields[i][j] == 'h':
          head_row, head_col = i, j
    self.participants_counter(fields)
    if self.participants_counter == "evade":
      if self.is_free(head_row, head_col, UP) and self.is_free (head_row+1, head_col+1, UP):
        return UP
      elif self.is_free(head_row, head_col, LEFT) and self.is_free (head_row+1, head_col+1, LEFT):
        return LEFT
      elif self.is_free(head_row, head_col, DOWN) and self.is_free (head_row+1, head_col+1, DOWN):
        return DOWN
      elif self.is_free(head_row, head_col, RIGHT) and self.is_free (head_row+1, head_col+1, RIGHT):
        return RIGHT
      print('PANIC!!!')
      return LEFT
    else:
      if self.is_free(head_row, head_col, UP) and self.is_free (head_row-1, head_col, UP):
        return UP
      elif  self.is_free(head_row, head_col, LEFT) and self.is_free (head_row, head_col-1, LEFT):
        return LEFT
      elif  self.is_free(head_row, head_col, DOWN) and self.is_free (head_row+1, head_col, DOWN):
        return DOWN
      elif self.is_free(head_row, head_col, RIGHT) and self.is_free (head_row, head_col+1, RIGHT):
        return RIGHT
      print('PANIC!!!')
      return LEFT
  def participants_counter(self,fields):
    remaining = 0
    participants_list = ["Filip","Test","Trubi"]
    self.height = len(fields)
    self.width = len(fields[0])
    for i in range(self.height):
      for j in range(self.width):
        for x in participants_list:
          if fields[i][j] == "0"+ x:
            remaining =+1
    if remaining > 2:
      return "evade"
    else:
      return "go"
  """def self_control(self,fields, height, width):
    body = []
    for i in range (self.height):
      for j in range (self.width):
        if fields[i][j]"""
