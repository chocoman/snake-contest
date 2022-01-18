from direction import LEFT, UP, RIGHT, DOWN

class AI:
  def __init__(self):
    self.fields = [['']]
    self.height = 1
    self.width = 1

  def is_free(self, row, col, direction=None, number=1):
    if direction == LEFT: col -= number
    elif direction == UP: row -= number
    elif direction == RIGHT: col += number
    elif direction == DOWN: row += number
    
    if row >= self.height: return False
    if row < 0: return False
    if col >= self.width: return False
    if col < 0: return False

    if self.fields[row][col] == '': return True
    if self.fields[row][col] == 'f': return True
    else: return False

  def where_is_free(self, row, col):
    if (col - 1 == " "):
      return LEFT
    elif (col + 1 == " "):
      return RIGHT
    elif (row - 1 == " "):
      return UP
    elif (row + 1 == " "):
      return DOWN


  # Funkce dostane seznam seznamů stringů fields. Záznam fields[i][j] říká,
  # co je na políčku na řádku i ve sloupci j. Možné hodnoty jsou 'f', což značí jídlo,
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
    if food_row < head_row and self.is_free(head_row, head_col, UP, 3):
      return UP
    elif food_col < head_col and self.is_free(head_row, head_col, LEFT, 3):
      return LEFT
    elif food_row > head_row and self.is_free(head_row, head_col, DOWN, 3):
      return DOWN
    elif food_col > head_col and self.is_free(head_row, head_col, RIGHT, 3):
      return RIGHT


    if food_row < head_row and self.is_free(head_row, head_col, UP, 2):
      return UP
    elif food_col < head_col and self.is_free(head_row, head_col, LEFT, 2):
      return LEFT
    elif food_row > head_row and self.is_free(head_row, head_col, DOWN, 2):
      return DOWN
    elif food_col > head_col and self.is_free(head_row, head_col, RIGHT, 2):
      return RIGHT

    if food_row < head_row and self.is_free(head_row, head_col, UP):
      return UP
    elif food_col < head_col and self.is_free(head_row, head_col, LEFT):
      return LEFT
    elif food_row > head_row and self.is_free(head_row, head_col, DOWN):
      return DOWN
    elif food_col > head_col and self.is_free(head_row, head_col, RIGHT):
      return RIGHT

    # tady vymyslet novou funkci

    elif self.where_is_free(head_row, head_col):
      return self.where_is_free(head_row, head_col)


    print('PANIC!!!')
    
    # nejdřív se rozhodnout, kde je volno
    return LEFT
