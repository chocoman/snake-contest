from tkinter import *
from board import Board
from snake import Snake, BotSnake

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
        80,
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
