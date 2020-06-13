# Keith Galli (https://github.com/KeithGalli/Connect4-Python)
# How to Program a Connect 4 AI (implementing the minimax algorithm) (https://www.youtube.com/watch?v=MMLtza3CZFM)


import numpy as np
import random
import pygame
import sys
import math
# from aulaPygame import menu_choices

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

def create_board(blockers = False):
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))

	if blockers:
		totalPositions = ROW_COUNT * (COLUMN_COUNT - 1)
		totalBlocks = round(0.20 * totalPositions) # 20% das posicoes
		positionsOfBlocks = []
		for x in range(totalBlocks):
			positionsOfBlocks.append(random.randint(0, totalPositions - 1))
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

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

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

def is_terminal_node(board):
	return winning_move(board, AI_PIECE) or winning_move(board, PLAYER_PIECE) or len(get_valid_locations(board)) == 0

# Minimax com poda
def minimaxAB(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE):
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
			new_score = minimaxAB(b_copy, depth-1, alpha, beta, False)[1]
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
			new_score = minimaxAB(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

# Minimax sem poda    
def minimax(board, depth, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE):
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
			new_score = minimax(b_copy, depth-1, False)[1]
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
			new_score = minimax(b_copy, depth-1, True)[1]
			if new_score < value:
				value = new_score
				column = col
		return column, value

# Negamax sem poda
def negamax(board, depth, piece):
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE
	
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, piece):
				return (None, 100000000000000)
			elif winning_move(board, opp_piece):
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
			new_score = -negamax(b_copy, depth-1, AI_PIECE)[1]
		else:
			new_score = -negamax(b_copy, depth-1, PLAYER_PIECE)[1]
		if new_score > value:
			value = new_score
			column = col
	return column, value

# Negamax sem poda
def negamaxAB(board, depth, piece, alpha, beta):
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE
	
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, piece):
				return (None, 100000000000000)
			elif winning_move(board, opp_piece):
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
			new_score = -negamaxAB(b_copy, depth-1, AI_PIECE, -math.inf, -math.inf)[1]
		else:
			new_score = -negamaxAB(b_copy, depth-1, PLAYER_PIECE, -math.inf, -math.inf)[1]
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


def start(value, difficulty=0):
	if difficulty == 2:
		board = create_board(True)
	else:
		board = create_board()
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
				col, minimax_score = minimaxAB(board, 5, -math.inf, math.inf, True)

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, PLAYER_PIECE)

					if winning_move(board, PLAYER_PIECE):
						label = myfont.render("ALPHA BETA venceu!!", 1, RED)
						screen.blit(label, (40,10))
						game_over = True

					print_board(board)
					draw_board(board)

					turn += 1
					turn = turn % 2
					print("turn:", turn)
					
			# AI with Minimax without pruning
			if turn == AI and not game_over:				
				col, minimax_score = minimax(board, 5, True)

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, AI_PIECE)

					if winning_move(board, AI_PIECE):
						label = myfont.render("AI SEM PODA VENCEU!!!", 1, YELLOW)
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

							if winning_move(board, PLAYER_PIECE):
								label = myfont.render("HUMANO VENCEU!!", 1, RED)
								screen.blit(label, (40,10))
								game_over = True

							turn += 1
							turn = turn % 2

							print_board(board)
							draw_board(board)


		# # Human turn
		if turn == AI and not game_over:
			col, minimax_score = negamaxAB(board, 5, AI_PIECE, -math.inf, math.inf)
			# col, minimax_score = minimaxAB(board, 5, -math.inf, math.inf, True)

			if is_valid_location(board, col):
				row = get_next_open_row(board, col)
				drop_piece(board, row, col, AI_PIECE)

				if winning_move(board, AI_PIECE):
					label = myfont.render("NEGAMAX VENCEU!!!", 1, YELLOW)
					screen.blit(label, (40,10))
					game_over = True

				print_board(board)
				draw_board(board)

				turn += 1
				turn = turn % 2

		if game_over:
			print('entrou')
			pygame.quit()
			quit()