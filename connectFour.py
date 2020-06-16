# Keith Galli (https://github.com/KeithGalli/Connect4-Python)
# How to Program a Connect 4 AI (implementing the minimax algorithm) (https://www.youtube.com/watch?v=MMLtza3CZFM)


import numpy as np
import random
import pygame
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREY = (160, 160, 160)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
BLOCKER_PIECE = 3

WINDOW_LENGTH = 4

VICTORY_CONDITION = 5

def create_board(blockers = False):
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))

	if blockers:
		totalPositions = ROW_COUNT * (COLUMN_COUNT - 1)
		totalBlocks = round(0.20 * totalPositions) # 20% das posicoes
		positionsOfBlocks = []
		for x in range(totalBlocks):
			positionsOfBlocks.append(random.randint(0, totalPositions - 2))
		for i in positionsOfBlocks:
			board.flat[i] = 3

	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece, n):
	count = 0
	# Check horizontal locations for win
	for c in range(ROW_COUNT):
		for r in range(ROW_COUNT):
			for i in range(n):
				if(c + i < ROW_COUNT):
					if(board[r][c + i] == piece):
						count += 1
			if count == n:
				return True
			else:
				count = 0
	

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(n):
			for i in range(n):
				if(r + i < ROW_COUNT):
					if(board[r + i][c] == piece):
						count += 1
			if(count == n):
				return True
			else:
				count = 0

	# Check positively sloped diaganols
	for c in range(n):
		for r in range(n):
			for i in range(n):
				if(r + i < ROW_COUNT and c + i < ROW_COUNT):
					if(board[r + i][c + i] == piece):
						count += 1
			if(count == n):
				return True
			else:
				count = 0

	# Check negatively sloped diaganols
	for c in range(n):
		for r in range(n):
			for i in range(n):
				if(r + i < ROW_COUNT and c + i < ROW_COUNT):
					if(board[r - i][c + i] == piece):
						count += 1
			if count == n:
				return True
			else:
				count = 0

def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score posiive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

def is_terminal_node(board, condition):
	return winning_move(board, AI_PIECE, condition) or winning_move(board, PLAYER_PIECE, condition) or len(get_valid_locations(board)) == 0

# Minimax com poda
def minimaxAB(board, depth, alpha, beta, maximizingPlayer, condition):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board, condition)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE, condition):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE, condition):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimaxAB(b_copy, depth-1, alpha, beta, False, condition)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimaxAB(b_copy, depth-1, alpha, beta, True, condition)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

# Minimax sem poda    
def minimax(board, depth, maximizingPlayer, condition):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board, condition)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE, condition):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE, condition):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, False, condition)[1]
			if new_score > value:
				value = new_score
				column = col
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, True, condition)[1]
			if new_score < value:
				value = new_score
				column = col
		return column, value

# Negamax sem poda
def negamax(board, depth, piece, condition):
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE
	
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board, condition)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, piece, condition):
				return (None, 100000000000000)
			elif winning_move(board, opp_piece, condition):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, piece))
			
	value = -math.inf
	column = random.choice(valid_locations)

	for col in valid_locations:
		row = get_next_open_row(board, col)
		b_copy = board.copy()
		drop_piece(b_copy, row, col, piece)
		if piece == PLAYER_PIECE:
			new_score = -negamax(b_copy, depth-1, AI_PIECE, condition)[1]
		else:
			new_score = -negamax(b_copy, depth-1, PLAYER_PIECE, condition)[1]
		if new_score > value:
			value = new_score
			column = col
	return column, value

# Negamax com poda
def negamaxAB(board, depth, piece, alpha, beta, condition):
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE
	
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board,condition)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, piece, condition):
				return (None, 100000000000000)
			elif winning_move(board, opp_piece, condition):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, piece))
			
	value = -math.inf
	column = random.choice(valid_locations)

	for col in valid_locations:
		row = get_next_open_row(board, col)
		b_copy = board.copy()
		drop_piece(b_copy, row, col, piece)
		if piece == PLAYER_PIECE:
			new_score = -negamaxAB(b_copy, depth-1, AI_PIECE, -beta, -alpha, condition)[1]
		else:
			new_score = -negamaxAB(b_copy, depth-1, PLAYER_PIECE, -beta, -alpha, condition)[1]
		if new_score > value:
			value = new_score
			column = col
		alpha = max(alpha, value)
		if alpha >= beta:
			break
	return column, value

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == AI_PIECE: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == BLOCKER_PIECE:
				pygame.draw.circle(screen, GREY, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			
	pygame.display.update()

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Lig-4")

myfont = pygame.font.SysFont("monospace", 75)


def start(value, criterion, difficulty=0):
	block = False
	depth = 5
	if difficulty == 1:
		depth = 3

	elif difficulty == 2:
		depth = 5
		
	elif difficulty == 3:
		depth = 5
		block = True

	board = create_board(block)
	print_board(board)
	draw_board(board)
	pygame.display.update()
	game_over = False
	turn = random.randint(PLAYER, AI)
	
	while not game_over:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.display.quit()
				pygame.quit()
				sys.exit()

			if event.type == pygame.MOUSEMOTION:
				pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
				posx = event.pos[0]
				if turn == PLAYER:
					pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

				pygame.display.update()
		
		if value == 1:
			# AI with Minimax with pruning
			if turn == PLAYER and not game_over:				
				col, minimax_score = minimaxAB(board, depth, -math.inf, math.inf, True, criterion)

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, PLAYER_PIECE)

					if winning_move(board, PLAYER_PIECE, criterion):
						label = myfont.render("MINIMAX VENCEU!!!", 1, RED)
						screen.blit(label, (40,10))
						game_over = True

					print_board(board)
					draw_board(board)

					turn += 1
					turn = turn % 2
					
			# AI with Negamax with pruning
			if turn == AI and not game_over:				
				col, minimax_score = negamaxAB(board, depth, AI_PIECE, -math.inf, math.inf, criterion)

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, AI_PIECE)

					if winning_move(board, AI_PIECE, criterion):
						label = myfont.render("NEGAMAX VENCEU!!!", 1, YELLOW)
						screen.blit(label, (40,10))
						game_over = True

					print_board(board)
					draw_board(board)

					turn += 1
					turn = turn % 2
		else:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.time.wait(3000)
					pygame.quit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if turn == PLAYER:
						pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					if turn == PLAYER:
						posx = event.pos[0]
						col = int(math.floor(posx/SQUARESIZE))

						if is_valid_location(board, col):
							row = get_next_open_row(board, col)
							drop_piece(board, row, col, PLAYER_PIECE)

							if winning_move(board, PLAYER_PIECE, criterion):
								label = myfont.render("HUMANO VENCEU!!!", 1, RED)
								screen.blit(label, (40,10))
								game_over = True

							turn += 1
							turn = turn % 2

							print_board(board)
							draw_board(board)


		# AI Negamax turn
		if turn == AI and not game_over:
			print('negamax depth', depth)
			col, minimax_score = negamaxAB(board, depth, AI_PIECE, -math.inf, math.inf, criterion)
			# col, minimax_score = minimaxAB(board, 5, -math.inf, math.inf, True)

			if is_valid_location(board, col):
				row = get_next_open_row(board, col)
				drop_piece(board, row, col, AI_PIECE)

				if winning_move(board, AI_PIECE, criterion):
					label = myfont.render("NEGAMAX VENCEU!!!", 1, YELLOW)
					screen.blit(label, (40,10))
					game_over = True

				print_board(board)
				draw_board(board)

				turn += 1
				turn = turn % 2

		if game_over:
			pygame.quit()
			quit()