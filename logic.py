# Factor Exchange logic
#
# Author: Ibb Marsh
# Created: 2018-07-02
#
# Description: Handles all the logic of turn-taking and tracking points.

class LogicStore:
  # Give all the factor points to the next player (or sink, if there is only one player)
  DEFAULT_DISTRIBUTION = [[1],[1]]

  def __init__ (self, max_card_value=50, randomize_max_card_value=False, distribution=DEFAULT_DISTRIBUTION, num_players=1, include_sink=True):
    # Parameter-derived attributes
    self._max_card_value = max_card_value
    self._distribution = distribution
    self._num_players = num_players
    self._include_sink = include_sink

    # Other internal attributes
    self._scores = [0 for _ in range(self._num_players)]
    self._sink_score = 0
    self._remaining_cards = [i+1 for i in range(self._max_card_value)]
    self._available_cards = [i+1 for i in range(1,self._max_card_value)]
    self._current_player = 0

  def take_turn (self, choice):
    if choice not in self._available_cards:
      return False

    self._scores[self._current_player] += choice
    self._remaining_cards.remove(choice)
    self._available_cards.remove(choice)

    total_points = self._remove_and_total_factors(choice)
    self._distribute_factor_points(total_points)

    self._current_player = (self._current_player+1) % self._num_players
    return True

  def _remove_and_total_factors (self, choice):
    total_points = 0

    # First, gather up all the factors of the choice that remain
    factors = self._factors_of(choice)
    for f in factors:
        total_points += f
        self._remove_card(f)

    # Run through all available cards and determine if they still have any factors remaining
    for c in self._available_cards[:]:
      if len(self._factors_of(c)) == 0:
        # Do not score them yet, but remove them from available
        self._available_cards.remove(c)

    # Run through all remaining cards and score/remove any without any multiples or factors
    max_card = max(self._remaining_cards) if len(self._remaining_cards) > 0 else 0
    for c in self._remaining_cards[:]:
      max_multiplier = max_card // c
      factors_remaining = len(self._factors_of(c)) != 0
      multiples_remaining = len(self._multiples_of(c,max_multiplier)) != 0
      if not factors_remaining and not multiples_remaining:
        total_points += c
        self._remove_card(c)

    return total_points

  def _factors_of (self, card):
    factors = []
    for c in range(1,card//2+1):
      if card % c == 0 and c in self._remaining_cards:
        factors.append(c)
    return factors

  def _multiples_of (self, card, max_multiplier):
    multiples = []
    for i in range(2,max_multiplier+1):
      if card*i in self._remaining_cards:
        multiples.append(card*i)
    return multiples

  def _remove_card (self, value):
    self._remaining_cards.remove(value)
    if value in self._available_cards:
      self._available_cards.remove(value)

  def _distribute_factor_points (self, total_points):
    divisor = sum(self._distribution[1])
    split_points = total_points / divisor
    for i in range(len(self._distribution[0])):
      pindex = self._distribution[0][i]
      mult = self._distribution[1][i]
      if pindex >= self._num_players and self._include_sink:
        self._sink_score += split_points * mult
      else:
        pindex = (self._current_player+pindex) % self._num_players
        self._scores[pindex] += split_points * mult

  def is_game_over (self):
    return len(self._remaining_cards) == 0

  def scores (self):
    if self._include_sink:
      return self._scores[:]+[self._sink_score]
    else:
      return self._scores[:]

  def cards (self):
    return [self._remaining_cards[:]]+[self._available_cards[:]]
