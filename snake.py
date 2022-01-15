# -*- coding: utf-8 -*-
from tkinter import *
from random import randint, shuffle
from datetime import *
import os
import traceback

from direction import RIGHT, UP, LEFT, DOWN, direction_as_string

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
      if (snake.points < -30):
        print(f'Player {snake.name} lost because they are below -30 points')
        self.snakes.remove(snake)
        snake.death()
        self.dead.append(snake)
      if (snake.points > 30):
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

class SnakeGame:
  def __init__(self, field_size, height, width, delay):
    self.field_size = field_size
    self.width = width
    self.height = height
    self.delay = delay
    self.window = Tk()
    self.window.title('snake')
    self.canvas=Canvas(
      self.window,
      width = (self.width) * self.field_size,
      height = (self.height) * self.field_size,
      bg = '#000000'
    )
    self.canvas.pack()
    self.keys = []
    self.window.bind('<KeyPress>', self.key_press)
    self.window.bind('<KeyRelease>', self.key_release)

    self.board = Board(height, width)

  def start(self):
    print('Starting game')
    self.update_loop()
    mainloop()


  def update_loop(self):
    self.board.update()
    self.rerender()
    if (not self.board.game_ended):
      self.window.after(self.delay, self.update_loop)

  def add_human_player(self, name, color, controls):
    snake = Snake(self.board, 5, color, name, control_keys=controls)
    self.board.add_snake(snake)

  def add_ai_player(self, name, color, ai):
    snake = BotSnake(self.board, 5, color, name, ai)
    self.board.add_snake(snake)

  def key_press(self, event):
    if not event.keysym in self.keys:
      self.keys.append(event.keysym)
    for snake in self.board.snakes:
      snake.handle_key_pressed(self.keys)

  def key_release(self, event):
    self.keys.remove(event.keysym)

  def rerender(self):
    self.canvas.delete(ALL)
    for snake in self.board.snakes:
      self.render_snake(snake)
    self.render_food()
    self.render_state()

  def render_food(self):
    for coordinates in self.board.food:
      row, col = coordinates
      field_size = self.field_size
      self.canvas.create_rectangle(
        col * field_size,
        row * field_size,
        (col+1) * field_size, (row + 1) * field_size,
        fill='#eeee88',
      )

  def render_state(self):
    sorted_snakes = sorted(
      self.board.snakes,
      key = lambda snake: -snake.points, # sort decreasing by points
    )
    for i in range(len(sorted_snakes)):
      snake = sorted_snakes[i]
      self.canvas.create_text(
        20,
        (i + 1) * self.field_size,
        text = str(snake.name) + ' ' + str(snake.points),
        fill=snake.color,
      )

  def render_snake(self, snake):
    for row, col in snake.tail:
      size = self.field_size
      self.canvas.create_rectangle(
        col * size, row * size,
        (col + 1) * size, (row + 1) * size,
        fill = snake.color,
      )


class Snake(object):
  def __init__(self, board, length, color, name, control_keys=[None, None, None, None]):
    self.board = board
    self.length = length
    self.color=color
    self.name=name
    self.control_keys = control_keys
    self.points = 0
    self.time_of_death = -1
    self.revive()

  def collision(self):
    print(f'{self.name} collided. -10 points.')
    self.points = self.points - 10
    self.revive()

  def move(self, direction):
    if direction == RIGHT and self.col < self.board.width - 1:
      self.col = self.col + 1
    elif direction == UP and self.row > 0:
      self.row = self.row - 1
    elif direction == LEFT and self.col > 0:
      self.col = self.col - 1
    elif direction == DOWN and self.row < self.board.height - 1:
      self.row = self.row + 1
    else:
      self.collision()
      return
    if (self.board.is_occupied(self.row, self.col)):
      self.collision()
      return
    self.tail.insert(0, [self.row, self.col])
    for i in range(len(self.board.food)):
      field = self.board.food[i]
      if (field == [self.row, self.col]):
        self.food_eaten(i)
        return
    while(len(self.tail) > self.length):
      self.tail.pop()

  def food_eaten(self,i):
    self.length = self.length + 3
    self.points = self.points + 1
    print(f'{self.name} ate food. +1 point.')

    self.board.food.pop(i)
    self.board.create_food()
  
  def revive(self):
    self.col = randint(0, self.board.width - 1)
    self.row = randint(0, self.board.height - 1)
    self.direction = randint(0, 3)
    if (self.board.is_occupied(self.row, self.col)):
      self.revive()
      return
    self.tail = [[self.row, self.col]]
    self.length = 5

  def handle_key_pressed(self, keys):
    for i in range(4):
        if (self.control_keys[i] in keys):
          self.direction = i

  def action(self):
    self.move(self.direction)
  
  def death(self):
    self.time_of_death = self.board.turn_number

class BotSnake(Snake):
  def __init__(self, board, length, color, name, ai):
    Snake.__init__(self, board, length, color, name)
    self.ai = ai

  def update(self, board):
      print(f'{self.name} is deciding...')
      try:
        self.direction = self.ai.decide_direction(board)
      except Exception as e:
        print(f'{self.name} crashed when deciding.')
        print(traceback.format_exc())
      print(f'{self.name} decided: {direction_as_string(self.direction)}')
