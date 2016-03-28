#!/usr/bin/python


BOARD_COLS = 7
BOARD_ROWS = 6

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
		s += "move number: %s\n" % (self.moveNumber)
		for r in range(self.rows):
			if r > 0:
				s += "\n"
			for c in range(self.cols):
				if c > 0:
					s += " "
				s += self.cells[c][r]
		return s

	def isLegalMove(self, col):
		return (self.cells[col][0] == TOKEN_EMPTY)

	def hasLegalMove(self):
		for col in range(self.cols):
			if self.isLegalMove(col):
				return True

		return False

	def dropToken(self, col, token):
		if not self.isLegalMove(col):
			print "error: cheater in the house!"
			return

		# go from the bottom row up, finding the first open cell
		for row in reversed(range(self.rows)):
			if self.cells[col][row] == TOKEN_EMPTY:
				self.cells[col][row] = token
				self.moveNumber += 1
				return

		print "error: something is wrong: move is legal but did not find a spot. stop the game!"



class class_player:

	def __init__(self, token):
		self.style = "first legal move"
		self.token = token

	def makeMove(self, board):
		# find the first legal move and make it!
		for c in range(board.cols):
			if board.isLegalMove(c):
				board.dropToken(c, self.token)
				print board.show()
				return

		print "No Legal Move!"



def runGame():
	board = class_board(BOARD_COLS, BOARD_ROWS)
	plyr1 = class_player(TOKEN_P1)
	plyr2 = class_player(TOKEN_P2)

	gameOver = False

	while not gameOver:
		if board.hasLegalMove():
			print ""
			print "player 1 (%s) moves:" % (plyr1.token)
			plyr1.makeMove(board)
		else:
			gameOver = True

		if board.hasLegalMove():
			print ""
			print "player 2 (%s) moves:" % (plyr2.token)
			plyr2.makeMove(board)
		else:
			gameOver = True

	print ""
	

def main():
	runGame()


main()