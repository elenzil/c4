#!/usr/bin/python

import copy
import random

# cells are numbered left to right, bottom to top.
# so column 0 row 0 is the lower left.


BOARD_COLS = 7
BOARD_ROWS = 6
RUN_LENGTH = 4

TOKEN_EMPTY = "-"
TOKEN_P1    = "X"
TOKEN_P2    = "O"

###############################################################################
# board class

class class_board:
	def __init__(self, w, h):
		self.cells = [[0 for blah in range(h)] for x in range(w)]
		self.cols = w
		self.rows = h
		self.clear()


	def clear(self):
		self.moveNumber = 0
		for r in range(self.rows):
			for c in range(self.cols):
				self.cells[c][r] = TOKEN_EMPTY


	def show(self):
		s = ""
		s += "move number: %s" % (self.moveNumber)
		for r in reversed(range(self.rows)):
			s += "\n"
			for c in range(self.cols):
				if c > 0:
					s += " "
				s += self.cells[c][r]
		return s

	def isLegalMove(self, col):
		return (self.cells[col][self.rows - 1] == TOKEN_EMPTY)

	def legalMoves(self):
		legalCols = []

		# check if board currently has a winner.
		# if there's a winner, there's no legal move.
		if self.winningToken() == TOKEN_EMPTY:
			for c in range(self.cols):
				if self.isLegalMove(c):
					legalCols.append(c)

		return legalCols


	def hasLegalMove(self):
		return len(self.legalMoves()) > 0

	def dropToken(self, col, token):
		if not self.isLegalMove(col):
			print "error: cheater in the house!"
			return

		# go from the bottom row up, finding the first open cell
		for row in range(self.rows):
			if self.cells[col][row] == TOKEN_EMPTY:
				self.cells[col][row] = token
				self.moveNumber += 1
				# print self.show()
				return

		print "error: something is wrong: move is legal but did not find a spot. stop the game!"

	def isCellInRange(self, col, row):
		if (col < 0) or (col >= self.cols):
			return False
		if (row < 0) or (row >= self.rows):
			return False
		return True


	def isRun(self, col, row, dCol, dRow):
		token = self.cells[col][row]

		if token == TOKEN_EMPTY:
			return False

		for n in range(RUN_LENGTH - 1):
			col += dCol
			row += dRow

			if not self.isCellInRange(col, row):
				print "error: cell out of range: %s %s" % (col, row)
				return False

			if self.cells[col][row] != token:
				return False

		return True

	def lowercaseBoard(self):
		for r in range(self.rows):
			for c in range(self.cols):
				self.cells[c][r] = self.cells[c][r].lower()

	def uppercaseRun(self, col, row, dCol, dRow):
		for n in range(RUN_LENGTH):
			self.cells[col][row] = self.cells[col][row].upper()
			col += dCol
			row += dRow


	# return winning run, if any.
	# returns a 5-value tuple:
	# 1. boolean is there a winning run or not
	# 2. column where the winning run begins
	# 3. row where the winning run begins
	# 4. delta-column of the run
	# 5. delta-row of the run
	def winningRun(self):
		# look for all horizontal runs
		for row in range(self.rows):
			for col in range(self.cols - RUN_LENGTH + 1):
				if self.isRun(col, row, 1, 0):
					return True, col, row, 1, 0

		# look for vertical runs					
		for row in range(self.rows - RUN_LENGTH + 1):
			for col in range(self.cols):
				if self.isRun(col, row, 0, 1):
					return True, col, row, 0, 1

		# look for up-and-to-the-right runs
		for row in range(self.rows - RUN_LENGTH + 1):
			for col in range(self.cols - RUN_LENGTH + 1):
				if self.isRun(col, row, 1, 1):
					return True, col, row, 1, 1

		# look for down-and-to-the-right runs
		for row in range(RUN_LENGTH, self.rows):
			for col in range(self.cols - RUN_LENGTH + 1):
				if self.isRun(col, row, 1, -1):
					return True, col, row, 1, -1

		return False, 0, 0, -1, -1

	def winningToken(self):
		hasWin, col, row, dCol, dRow = self.winningRun()
		if not hasWin:
			return TOKEN_EMPTY
		else:
			return self.cells[col][row]


###############################################################################
# player classes


class class_player_basic:

	def __init__(self, token):
		self.style = "first possible move"
		self.token = token

	def makeMove(self, board):
		# find the first legal move and make it!
		for c in range(board.cols):
			if board.isLegalMove(c):
				board.dropToken(c, self.token)
				return

		print "error: No Legal Move, why are you asking me to move ?"

	def otherPlayerToken(self):
		if self.token == TOKEN_P1:
			return TOKEN_P2
		else:
			return TOKEN_P1


class class_player_thinking(class_player_basic):
	def __init__(self, token):
		class_player_basic.__init__(self, token)
		self.style = "abstract base class for players who want to think about different moves"


class class_player_random(class_player_thinking):
	def __init__(self, token):
		class_player_thinking.__init__(self, token)
		self.style = "random move"

	def makeMove(self, board):
		# make a random legal move

		moves = board.legalMoves()

		if len(moves) == 0:
			print "error: No Legal Move, why are you asking me to move ?"

		chosenCol = random.choice(moves)
		board.dropToken(chosenCol, self.token)


class class_player_winChooser(class_player_random):
	def __init__(self, token):
		class_player_random.__init__(self, token)
		self.style = "choose moves that win right now, otherwise random"

	def makeMove(self, board):

		moves = board.legalMoves()

		if len(moves) == 0:
			print "error: No Legal Move, why are you asking me to move ?"

		for col in moves:
			newBoard = copy.deepcopy(board)
			newBoard.dropToken(col, self.token)
			if newBoard.winningToken() == self.token:
				board.dropToken(col, self.token)
				return

		class_player_random.makeMove(self, board)


class class_player_winChooserLossAvoider(class_player_winChooser):
	def __init__(self, token):
		class_player_winChooser.__init__(self, token)
		self.style = "choose moves that win right now, avoid moves that lose next turn, otherwise random"

	def makeMove(self, board):

		# see if we can just win

		newBoard = copy.deepcopy(board)
		class_player_winChooser.makeMove(self, newBoard)
		if newBoard.winningToken() == self.token:
			# make the same move on our board
			class_player_winChooser.makeMove(self, board)
			return


		# nope, ok. avoid losing for one round:
		moves = board.legalMoves()
		nonLosingMoves = []
		for col in moves:
			if not self.isLosingMove(board, col):
				nonLosingMoves.append(col)

		if len(nonLosingMoves) > 0:
			board.dropToken(random.choice(nonLosingMoves), self.token)
		else:
			# all choices equally bad!
			class_player_random.makeMove(self, board)

	def isLosingMove(self, board, col):
		boardMyMove = copy.deepcopy(board)
		boardMyMove.dropToken(col, self.token)
		if not boardMyMove.hasLegalMove():
			# other player cannot move - we do not lose!
			return False
		else:
			otherPlayerLegalMoves = boardMyMove.legalMoves()
			for oplm in otherPlayerLegalMoves:
				boardTheirMove = copy.deepcopy(boardMyMove)
				boardTheirMove.dropToken(oplm, self.otherPlayerToken())
				if boardTheirMove.winningToken() == self.otherPlayerToken():
					# so sad - they win.
					return True

		return False


###############################################################################
# game management


def runGame():
	board = class_board(BOARD_COLS, BOARD_ROWS)

	players = []

	players.append(class_player_winChooser           (TOKEN_P1))
	players.append(class_player_winChooserLossAvoider(TOKEN_P2))

	while board.hasLegalMove():
		for plyr in players:
			if board.hasLegalMove():
				plyr.makeMove(board)

	boardCopy = copy.deepcopy(board)
	boardCopy.lowercaseBoard()

	winningToken = board.winningToken()

	if winningToken == TOKEN_EMPTY:
		print "Nobody won."
	else:
		winner = None
		for plyr in players:
			if winningToken == plyr.token:
				winner = plyr

		print "Winner is '%s' - %s !" % (winner.token, winner.style)
		unused, col, row, dCol, dRow = board.winningRun()
		boardCopy.uppercaseRun(col, row, dCol, dRow)

	print boardCopy.show()
	

def main():
	# optionally this could get input for number of rows/cols, number of iterations, etc.
	runGame()


main()