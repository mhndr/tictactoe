import curses
import random

grid = [" "," "," "," "," "," ", " "," "," "]
draw_grid = "+---+---+---+\
	  		\n| {0} | {1} | {2} |\
			\n+---+---+---+\
	  		\n| {3} | {4} | {5} |\
			\n+---+---+---+\
	  		\n| {6} | {7} | {8} |\
			\n+---+---+---+"
x_moves = []
o_moves = []
wins = ((0, 1, 2), (3, 4, 5), (6, 7, 8), 
		(0, 3, 6), (1, 4, 7), (2, 5, 8), 
		(0, 4, 8), (2, 4, 6)) 


def init_curses():
	# get the curses screen window
	screen = curses.initscr()
 
	# turn off input echoing
	curses.noecho()
 
	# respond to keys immediately (don't wait for enter)
	curses.cbreak()
 
	# map arrow keys to special values
	screen.keypad(True)
	return screen

def get_grid_index(x,y):
	x = (x-2)/4
	y = (y-1)/2
	i = (y*3) + x
	return i	

def is_game_over():
	if is_grid_full() or is_there_winner():
		return True
	return False
	
def is_grid_full():
	for i in range(len(grid)):
		if grid[i] == " ":
			return False
	return True

def get_empty_cells():
	empty_cells = []
	for i in range(len(grid)):
		if grid[i] == " ":
			empty_cells.append(i)
	return empty_cells 

def valid_move(move):
	empty_cells = get_empty_cells()
	if move in empty_cells:
		return True
	return False 

def is_there_winner():
	winner = get_winner()
	if winner == "~":
		return False
	return True

	
def get_winner():
	for win in wins:
		if grid[win[0]] != " " and \
			grid[win[0]] == grid[win[1]] == grid[win[2]]:
			return grid[win[0]]
	return "~"


def play():
	empty_cells = get_empty_cells()
	if not empty_cells or is_game_over():
		return -1
	if empty_cells == 8:
		rand = random.randrange(0,len(empty_cells))
		return empty_cells[rand]

	# see if there's an immediate winning move at hand.
	win_options = []		
	for win in wins:
		for move in o_moves:
			if move in win:
				win_options.append(win)
	for win in win_options:
		winning_move = [i for i in win if i not in o_moves]
		if len(winning_move) == 1 and valid_move(winning_move[0]):
			return int(winning_move[0])			
	
	#find winning options for human and block them
	block_options = []
	for win in wins: 
		for move in x_moves:
			if move in win:
				block_options.append(win)
	#if human is one move away from winning, take it ;-)
	for block in block_options:
		blocking_move = [i  for i in block if i not in x_moves]		
		if len(blocking_move) == 1 and valid_move(blocking_move[0]):
			return int(blocking_move[0])


	#fall back to a random move if there isn't an immediate win or block.	
	rand = random.randrange(0,len(empty_cells))
	return empty_cells[rand]


def print_grid():
	screen = init_curses()
	x = 2
	y = 1
	game_over = False
	try:
		#decide who should play first
		bot_first = random.randint(0,100)%2
		if bot_first:
			bot_move = play()
			if bot_move != -1:
				grid[bot_move] = "O"
				o_moves.append(bot_move)
		screen.addstr(0,0,draw_grid.format(*grid))
		screen.move(y,x)
		while True: 
			char = screen.getch()
			if char == ord('q'):
				break
			if game_over:
				screen.addstr(8,0,"Press 'q' to exit")
				continue
			#move the cursor
			if char == curses.KEY_RIGHT:
				x = x + 4
				if x>10:x = 10
			elif char == curses.KEY_LEFT:
				x = x - 4
				if x<0: x = 2
			elif char == curses.KEY_UP:
				y = y - 2 
				if y<0: y = 1
			elif char == curses.KEY_DOWN:
				y = y + 2
				if y>5: y = 5 

			elif char == curses.KEY_ENTER or char == 10 or char == 13:
				#change the grid entries here
				human_move = get_grid_index(x,y)
				if not valid_move(human_move): 
					continue
				grid[human_move] = "X"
				x_moves.append(human_move)
				bot_move = play()
				if bot_move != -1:
					grid[bot_move] = "O"
					o_moves.append(bot_move)
			if is_game_over():	
				game_over = True
				winner = get_winner()
				if winner == "~":
					screen.addstr(7,0,"Game Over - Its a Draw.")
				elif winner == "X":
					screen.addstr(7,0,"Game Over - You Win!")
				elif winner == "O":
					screen.addstr(7,0,"Game Over - I Win!!!!")
		
			#render changes.
			screen.addstr(0,0,draw_grid.format(*grid))
			screen.move(y,x)
	finally:
    	# shut down cleanly
		curses.nocbreak(); screen.keypad(0); curses.echo()
		curses.endwin()

if __name__ == '__main__':
	print_grid()


