from direction import LEFT, UP, RIGHT, DOWN

class AI:
  def __init__(self):
    self.fields = [['']]
    self.height = 1
    self.width = 1

  def within(self, row, col, direction, fields):
   

    if row >= self.height: return False
    if row < 0: return False
    if col >= self.width: return False
    if col < 0: return False
    else: return True

  def within_end(self, row, col, direction):
    if direction == LEFT: col -= 1
    elif direction == UP: row -= 1
    elif direction == RIGHT: col += 1
    elif direction == DOWN: row += 1


    if row >= self.height: return False
    if row < 0: return False
    if col >= self.width: return False
    if col < 0: return False
    else: return True

  def is_free(self, row, col, direction=None):
    

    if direction == LEFT: col -= 1
    elif direction == UP: row -= 1
    elif direction == RIGHT: col += 1
    elif direction == DOWN: row += 1
    
    
    
    try:
      if self.fields[row][col] == '': return True
      if self.fields[row][col] == 'f': return True
      else: return False
    except:
      return False

  # Funkce dostane seznam seznamů stringů fields. Záznam fields[i][j] říká,
  # co je na políčku na řádku i ve sloupci j. Možné hodoty jsou 'f', což značí jídlo,
  # prázdný string '' což značí prázdné pole, 'h' značí hlavu hada, pro nějž se rozhodujete
  # a cokoli dalšího znamená tělo nějakého hada. To je záznam ve formátu '4-arnost'.
  # Číslo před pomlčkou značí, o kolikátý díl těla se jedná (hlava je 0) a zbytek za pomlčkou
  # je jméno daného hada.
  # Tuto funkci můžete libovolně upravit. Jenom zachovejte její název a vstupní parametry
  # a vracejte jedině jednu z hodnot LEFT, UP, RIGHT, DOWN
  # Můžete přidat jakékoli další funkce.

  def check(self, head_row, head_col, dir, fields):
  
    self.fields = fields
    next_one ={UP:[-2,0,-1,0],LEFT:[0,-2,0,-1], DOWN:[2,0,1,0], RIGHT:[0,2,0,1]}
    aw2row=head_row+next_one[dir][0]
    aw2col=head_col+next_one[dir][1]
    one_away_row=head_row+next_one[dir][2]
    one_away_col=head_col+next_one[dir][3]


    if self.within(head_row,head_col, dir, fields)==True and self.is_free(head_row, head_col, dir)==True:
        
        if self.within( aw2row, aw2col, dir, fields) == True:
          if self.is_free(aw2row, aw2col)==True and self.is_free(one_away_row, one_away_col, dir)==True:
             return True 
          else: return self.fields[one_away_row][one_away_col]
        else: 
          if self.within( one_away_row,one_away_col, dir, fields)==True:
            if self.is_free(one_away_row, one_away_col, dir)==True:
              return True
    else:
            return False




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
    
    if food_row < head_row:
        option = self.check(head_row, head_col, UP, fields)
        if option == True:
            return UP
        else:
            print(option)
    elif food_col < head_col:
        option = self.check(head_row, head_col, LEFT,fields)
        if option == True:
            return LEFT
        else:
            print(option)
    elif food_row > head_row:
        option = self.check(head_row, head_col, DOWN,fields)
        if option == True:
            return DOWN
        else:
            print(option)
    elif food_col > head_col:
        option = self.check(head_row, head_col, RIGHT,fields)
        if option == True:
            return RIGHT
    
    for i in [UP, DOWN, LEFT, RIGHT]:
        if self.within_end(head_row, head_col, i)==True and self.is_free(head_row, head_col, i)==True:
            print(i) 
            return i
        else: continue

    