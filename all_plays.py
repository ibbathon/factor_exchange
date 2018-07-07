#!/usr/local/bin/python3
# Factor Exchange play printer
#
# Author: Ibb Marsh
# Created: 2018-07-07
#
# Description: Calculates all possible plays of a given Factor Exchange board and outputs all
#  plays along with their scores.

import sys, argparse, copy
import logic

class RecursivePlayPrinter:

  DEFAULT_PARAMS = {
    'maxcardvalue': 10,
    'numplayers': 1,
    'withoutsink': False,
    'evengain': False,
    'screenwidth': 80,
    'debug': False,
  }

  def __init__ (self, argv):
    parser = self.build_parser()
    args = parser.parse_args(argv[1:])

    if args.evengain:
      distribution = [
        [i+1 for i in range(args.numplayers-1)],
        [1 for i in range(args.numplayers)-1]
      ]
    else:
      distribution = [[1],[1]]

    self.screen_width = args.screenwidth
    self.debug = args.debug
    self.num_players = args.numplayers
    self.logicstore = logic.LogicStore(
      max_card_value = args.maxcardvalue,
      num_players = args.numplayers,
      include_sink = not args.withoutsink,
      distribution = distribution
    )

  def build_parser (self):
    parser = argparse.ArgumentParser(description='Calculates all possible plays of a given'+ \
      ' Factor Exchange board and outputs all plays along with their scores.')
    parser.add_argument('-m','--maxcardvalue',default=self.DEFAULT_PARAMS['maxcardvalue'],type=int,
      help="Sets the number of cards in play on the board (default: {})".format(
        self.DEFAULT_PARAMS['maxcardvalue']))
    parser.add_argument('-n','--numplayers',default=self.DEFAULT_PARAMS['numplayers'],type=int,
      help="Sets the number of players (default: {})".format(self.DEFAULT_PARAMS['numplayers']))
    parser.add_argument('-wos','--withoutsink',action='store_true',
      help="Play without a sink for factor points (default: play with sink)")
    parser.add_argument('-eg','--evengain',action='store_true',
      help="Factor points are distributed across all players (default: factor points go to"+ \
        " next player)")
    parser.add_argument('-d','--debug',action='store_true',
      help="Print debug statements (default: don't)")
    parser.add_argument('-sw','--screenwidth',default=self.DEFAULT_PARAMS['screenwidth'],type=int,
      help="Sets screen width (for debug statements) (default: {})".format(
        self.DEFAULT_PARAMS['screenwidth']))
    return parser

  def run (self):
    all_plays = []
    current_play = []
    self.recursive_play(copy.deepcopy(self.logicstore),current_play,all_plays)
    self.print_plays(all_plays)

  def print_plays (self, all_plays):
    if self.debug:
      print()
    for play in all_plays:
      print(",".join(str(v) for v in play[0])+", ,"+",".join(str(v) for v in play[1]))

  def recursive_play (self, store, curr_play, all_plays):
    # If the game is over, add a new play to the list
    if store.is_game_over():
      if self.debug:
        print("\r{}\r{}".format(" "*self.screen_width,str(curr_play)),end="")
      all_plays.append([store.scores(),curr_play[:]])
      return
    # Otherwise, kick off the recursion of each possible play in turn
    poss_moves = store.cards()[1]
    for move in poss_moves:
      newstore = copy.deepcopy(store)
      newstore.take_turn(move)
      curr_play.append(move)
      self.recursive_play(newstore,curr_play,all_plays)
      curr_play.pop()


if __name__ == '__main__':
  rpp = RecursivePlayPrinter(sys.argv)
  rpp.run()
