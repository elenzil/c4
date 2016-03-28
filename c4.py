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

	def hasLegalMove(self):
		# maybe somebody already won:
		if self.winningToken() != TOKEN_EMPTY:
			return False

		# nope, no winner.
		for col in range(self.cols):
			if self.isLegalMove(col):
				return True

		return False

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


class class_player:

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


class class_player_random(class_player):
	def __init__(self, token):
		class_player.__init__(self, token)
		self.style = "random move"

	def makeMove(self, board):
		# make a random legal move

		legalCols = []

		for c in range(board.cols):
			if board.isLegalMove(c):
				legalCols.append(c)

		if len(legalCols) == 0:
			print "error: No Legal Move, why are you asking me to move ?"

		chosenCol = random.choice(legalCols)
		board.dropToken(chosenCol, self.token)



def runGame():
	board = class_board(BOARD_COLS, BOARD_ROWS)
	plyr1 = class_player       (TOKEN_P1)
	plyr2 = class_player_random(TOKEN_P2)

	gameOver = False

	while not gameOver:
		if board.hasLegalMove():
			# print ""
			# print "player 1 (%s) moves:" % (plyr1.token)
			plyr1.makeMove(board)
		else:
			gameOver = True

		if board.hasLegalMove():
			# print ""
			# print "player 2 (%s) moves:" % (plyr2.token)
			plyr2.makeMove(board)
		else:
			gameOver = True

	print ""
	print "Game Over!"

	boardCopy = copy.deepcopy(board)
	boardCopy.lowercaseBoard()


	winning_token = board.winningToken()

	if winning_token == TOKEN_EMPTY:
		print "Nobody won."
	else:
		if winning_token == TOKEN_P1:
			winner = plyr1
		else:
			winner = plyr2
		print "Winner is %s - %s !" % (winner.token, winner.style)
		unused, col, row, dCol, dRow = board.winningRun()
		boardCopy.uppercaseRun(col, row, dCol, dRow)

	print boardCopy.show()
	

def main():
	runGame()


main()