# -*- coding: utf-8 -*-
import traceback
from random import randint, shuffle

from direction import RIGHT, UP, LEFT, DOWN, direction_as_string


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
    print(f'{self.name} collided. -5 points.')
    self.points = self.points - 5
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
