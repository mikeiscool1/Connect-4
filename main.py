import sys
from game import Game, COLUMNS, TURN_RED
import os

game = Game()

while True:
  print(game)
  try:
    c = int(input(f'{"Red" if game.turn == TURN_RED else "Yellow"} >>> ')) - 1
  except ValueError:
    print('Invalid integer.')
    continue

  if not c in range(COLUMNS):
    print('Column is out of game bounds.')
    continue

  if game.check_col_full(c):
    print('Column is full.')
    continue

  game.drop(c)

  if game.check_tie():
    print(game)

    print('Game over! It\'s a tie!')
    break

  if game.check_win(game.turn):
    ## os.system('clear')
    print(game)

    print(f'Game over! {"Red" if game.turn == TURN_RED else "Yellow"} won the game!')
    break

  game.switch_turn()