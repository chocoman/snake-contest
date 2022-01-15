RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3

def direction_as_string(code):
    if code == RIGHT: return 'RIGHT'
    if code == UP: return 'UP'
    if code == LEFT: return 'LEFT'
    if code == DOWN: return 'DOWN'
    return f'invalid direction {code}'