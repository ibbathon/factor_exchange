#!/usr/bin/env python3
# Factor Exchange game solver
#
# Author: Ibb Marsh
# Created: 2018-07-10
#
# Description: Solves the game, as opposed to a player's choices during the game. This program
# calculates all possible plays of a given Factor Exchange board and outputs the
# "perfect play" choices that perfect-knowledge players would make, along with the final scores.

import sys, argparse, copy, json
import logic

class GameSolver:

	DEFAULT_PARAMS = {
		'maxcardvalue': 10,
		'numplayers': 1,
		'withoutsink': False,
		'evengain': False,
		'screenwidth': 80,
		'debug': False,
		'discardunplayable': False,
	}

	def __init__ (self, argv):
		parser = self.build_parser()
		args = parser.parse_args(argv[1:])

		if args.evengain:
			distribution = [
				[i+1 for i in range(args.numplayers-1)],
				[1 for i in range(args.numplayers-1)]
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
			distribution = distribution,
			discard_unplayable = args.discard_unplayable
		)

	def build_parser (self):
		parser = argparse.ArgumentParser(description="Solves the game, as opposed to a player's"+ \
			" choices during the game. This program calculates all possible plays of a given Factor"+ \
			" Exchange board and outputs the 'perfect play' choices that perfect-knowledge players"+ \
			" would make, along with the final scores.")
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
		parser.add_argument('--discard-unplayable',action='store_true',
			help="Discard (do not distribute points for) any cards which are no longer a factor or multiple of another "+ \
				"card on the board (default: do distribute unplayable points)")
		parser.add_argument('-d','--debug',action='store_true',
			help="Print debug statements (default: don't)")
		parser.add_argument('-sw','--screenwidth',default=self.DEFAULT_PARAMS['screenwidth'],type=int,
			help="Sets screen width (for debug statements) (default: {})".format(
				self.DEFAULT_PARAMS['screenwidth']))
		return parser

	def run (self):
		current_play = []
		scores,solution = self.recursive_play(copy.deepcopy(self.logicstore),current_play)
		if self.debug:
			print()
		print(scores)
		print(solution)
		winner = -1
		best_score = 0
		for i in range(len(scores)):
			if scores[i] > best_score:
				best_score = scores[i]
				winner = i
			elif scores[i] == best_score:
				winner = -1
		print("The winner is {}".format(winner))

	def recursive_play (self, store, curr_play):
		# If the game is over, return the score and an empty choice list
		if store.is_game_over():
			if self.debug:
				print("\r{}\r{}".format(" "*self.screen_width,str(curr_play)),end="")
			return store.scores(),[]
		# Otherwise, kick off the recursion of each possible play in turn
		poss_moves = store.cards()[1]
		player = store.current_player()
		best_scores = [0 for i in range(self.num_players)]
		best_choices = None
		for move in poss_moves:
			newstore = copy.deepcopy(store)
			newstore.take_turn(move)
			curr_play.append(move)
			scores,choices = self.recursive_play(newstore,curr_play)
			curr_play.pop()
			if scores[player] > best_scores[player]:
				best_scores = scores
				best_choices = [move]+choices
		return best_scores,best_choices


if __name__ == '__main__':
	gs = GameSolver(sys.argv)
	gs.run()
