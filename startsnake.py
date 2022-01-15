from snake import SnakeGame
from participants import spanel

game = SnakeGame(20, 20, 30, 100)
#game.add_human_player('Human 1', '#bbff00', ['d','w','a','s'])
game.add_ai_player('Bot Spanel 1', '#ff0000', spanel.AI())
game.add_ai_player('Bot Spanel 2', '#ffffff', spanel.AI())
game.start()

