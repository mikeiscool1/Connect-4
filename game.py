from functools import reduce

# variables
RRED = '\033[91mO\033[39m' # Red Representation
RYEL = '\033[33mO\033[39m' # Yellow Representation
ROWS = 6
COLUMNS = 7

# constants
RYDEF = [0] * COLUMNS # Red/Yellow Default
FULL_COLUMN = (1 << ROWS) - 1
FULL_BOARD = FULL_COLUMN * COLUMNS
VERTICAL_WIN = (1 << 4) - 1
TURN_RED = 0
TURN_YELLOW = 1

class Game:
  def __init__(self, red=RYDEF.copy(), yellow=RYDEF.copy(), turn=TURN_RED):
    self.red: list[int] = red
    self.yellow: list[int] = yellow
    self.turn = turn

  def __repr__(self):
    printstr = ''
    for row in range(ROWS-1, -1, -1):
      printstr += '|  '
      for column in range(COLUMNS):
        bit = 1 << row
        if self.red[column] & bit:
          printstr += f'{RRED}  '
        elif self.yellow[column] & bit:
          printstr += f'{RYEL}  '
        else:
          printstr += '   '

        printstr += '|  '
    
      printstr += '\n' + ('-' * COLUMNS * 6) + '-\n'
    
    for i in range(1, COLUMNS + 1):
      istr = str(i)
      printstr += ' ' * (3 - len(istr) + 1) + istr + '  '

    return printstr
      
  def drop(self, column, auto_switch=False):
    if self.turn == TURN_RED:
      self.red[column] += self.red[column] + self.yellow[column] + 1
    else:
      self.yellow[column] += self.red[column] + self.yellow[column] + 1

    if auto_switch:
      self.switch_turn()

  def switch_turn(self):
    self.turn = int(not self.turn)

  def check_col_full(self, column):
    return self.red[column] + self.yellow[column] == FULL_COLUMN

  def check_tie(self):
    return reduce(lambda a, b: a + b, self.red + self.yellow) == FULL_BOARD

  def check_win(self, turn):
    # vertical
    l = self.red if turn == TURN_RED else self.yellow
    for column in range(COLUMNS):
      col = l[column]
      for i in range(ROWS - 4):
        if col >> i == VERTICAL_WIN:
          return True

    # horizontal
    for r in range(ROWS):
      row_bit = 1 << r
      row = 0
      for i in range(COLUMNS):
        if l[i] & row_bit:
          row += 1 << i

      for i in range(COLUMNS - 4):
        if row >> i == VERTICAL_WIN:
          return True
      
    # diagonal
    for row in range(ROWS - 1, -1 * COLUMNS, -1):
      diagonal = 0
      indiagonal = 0
      for i in range(ROWS - row):
        if i > COLUMNS - 1:
          break
        if row + i < 0: continue
        diagonal += l[i] & (1 << (row + i))
        indiagonal += l[COLUMNS - i - 1] & (1 << (row + i))

      for i in range(ROWS - row):
        if diagonal >> i == VERTICAL_WIN or indiagonal >> i == VERTICAL_WIN:
          return True


    return False