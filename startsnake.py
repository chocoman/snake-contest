from game import SnakeGame

from participants import martin

game = SnakeGame(20, 20, 30, 50)
#game.add_human_player('Human 1', '#bbff00', ['d','w','a','s'])
game.add_ai_player('Martin', '#ff0000', martin.AI())
game.add_ai_player('Taky Martin', '#ffffff', martin.AI())
game.start()

