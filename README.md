connect four player

so far, this has these classes:

class_board:
  represents the board. can identify winning runs, winning tokens.

class_player_basic:
  very naive. plays the first legal move.

class_player_thinking(class_player_basic):
  an "abstract" class, in that it's never direction instanciated.
  this is just here to provide a way to get the legal moves.

class_player_random(class_player_thinking):
  chooses a random legal move

class_player_winChooser(class_player_random):
  if there's a move that immediately wins, do that!
  otherwise, random.

class_player_winChooserLossAvoider(class_player_winChooser):
  if there's a move that immediately wins, do that!
  if there's a move that (could) lose next turn, don't do that !
  otherwise, random.
