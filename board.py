import os
from datetime import *
from random import randint, shuffle
from snake import Snake, BotSnake

class Board:
  def __init__(self, height, width):
    self.height = height
    self.width = width
    self.game_ended = False
    self.snakes = []
    self.dead = []
    self.food = []
    self.create_food()
    self.turn_number = 0

  def add_snake(self, snake):
    self.snakes.append(snake)

  def create_food(self):
    col = randint(0, self.width - 1)
    row = randint(0, self.height - 1)
    if (self.is_occupied(row, col)):
      self.create_food()
      return
    self.food.append([row, col])
    print(f'new food at {(row, col)}')

  def evaluate_state(self):
    self.game_ended = False
    for snake in self.snakes:
      if (snake.points < -10):
        print(f'Player {snake.name} lost because they are below -30 points')
        self.snakes.remove(snake)
        snake.death()
        self.dead.append(snake)
      if (snake.points > 10):
        print(f'Game ended because {snake.name} reached 30 points.')
        self.game_ended = True
    if (len(self.snakes) == 0):
      print(f'Game ended because all snakes died.')
      self.game_ended = True

    if (self.game_ended):
      self.write_summary()

  def write_summary(self):
    if not os.path.exists('results'):
      os.makedirs('results')
    file_name = 'results/result' + str(datetime.now().strftime('%Y-%m-%d_%H_%M_%S')) + '.txt'
    with open(file_name,'w') as file:
      file.write(file_name + '\n')
      for snake in self.dead:
        file.write(str(snake.name) + ': ' + str(snake.points) + '\n')
      for snake in self.snakes:
        file.write(str(snake.name) + ': ' + str(snake.points) + '\n')
        print(str(snake.name) + ': ' + str(snake.points))
      print('Konec hry. Vysledek zapsan do ' + file_name)

  def update(self):
    self.turn_number = self.turn_number + 1
    # All snakes move in random order based on their decision from before.
    execution_order = list(range(len(self.snakes)))
    shuffle(execution_order)
    for i in execution_order:
      self.snakes[i].action()
    self.evaluate_state()
    # All all snakes decide what to do in next round.
    for snake in self.snakes:
      if(isinstance(snake, BotSnake)):
        snake.update(self.export_fields(snake))

  def export_fields(self, focused_snake):
    fields = []
    for i in range(self.height):
      row = []
      for j in range(self.width):
        row.append('')
      fields.append(row)
    for snake in self.snakes:
      for i in range(len(snake.tail)):
        row, col = snake.tail[i]
        fields[row][col] = f'{i}-{snake.name}'
    for row, col in self.food:
      fields[row][col] = 'f'
    head_row, head_col = focused_snake.tail[0]
    fields[head_row][head_col] = 'h'
    return fields

  def is_occupied(self, row, col):
    if col >= self.width:
      return True
    if col < 0:
      return True
    if row >= self.height:
      return True
    if row < 0:
      return True
    for snake in self.snakes:
      for field in snake.tail:
        if (field == [row, col]):
          return True
    return False
