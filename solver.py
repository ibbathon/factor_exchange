#!/usr/local/bin/python3
# Factor Exchange solver
#
# Author: Ibb Marsh
# Created: 2018-07-03
#
# Description: Attempts all plays of a given Factor Exchange board and outputs the optimal plays
#  for players, as well as expected score.

import sys, argparse, copy
import logic

class RecursiveSolver:

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
    parser = argparse.ArgumentParser(description='Attempts all plays of a given Factor Exchange'+ \
      ' board and outputs the optimal plays for players, as well as expected score.')
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
    best_scores = [0 for _ in range(self.num_players)]
    best_plays = [[] for _ in range(self.num_players)]
    current_play = []
    self.recursive_solve(copy.deepcopy(self.logicstore),current_play,best_scores,best_plays)
    self.print_solution(best_scores,best_plays)

  def print_solution (self, best_scores, best_plays):
    if self.debug:
      print()
    print("Best scores: {}".format(", ".join([str(s) for s in best_scores])))
    print("Best plays: {}".format("; ".join([str(s) for s in best_plays])))

  def recursive_solve (self, store, curr_play, best_scores, best_plays):
    # If the game is over, check if this game's scores are better than the best
    if store.is_game_over():
      if self.debug:
        print("\r{}\r{}".format(" "*self.screen_width,str(curr_play)),end="")
      game_scores = store.scores()
      for i in range(self.num_players):
        if game_scores[i] > best_scores[i]:
          if self.debug:
            print("\nNew best score: {}".format(game_scores[i]))
          best_scores[i] = game_scores[i]
          best_plays[i] = []
        if game_scores[i] == best_scores[i]:
          dup = False
          for play in best_plays[i]:
            if sorted(curr_play) == sorted(play):
              dup = True
              break
          if not dup:
            if self.debug:
              print("\nNew best play")
            best_plays[i].append(curr_play[:])
      return
    # Otherwise, kick off the recursion of each possible play in turn
    poss_moves = store.cards()[1]
    for move in poss_moves:
      newstore = copy.deepcopy(store)
      newstore.take_turn(move)
      curr_play.append(move)
      self.recursive_solve(newstore,curr_play,best_scores,best_plays)
      curr_play.pop()


if __name__ == '__main__':
  solv = RecursiveSolver(sys.argv)
  solv.run()
