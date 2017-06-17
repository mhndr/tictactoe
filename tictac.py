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

win_configs = [	'010010010', '001001001', 
				'100010001', '100100100', 
				'001010100', '111000000', 
				'000111000', '000000111']

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
	curr_cfg = ""
	for i in range(len(grid)):
		if grid[i] == "X":
			curr_cfg += "1"
		else:
			curr_cfg +="0"
	if curr_cfg in win_configs:
		return "X"

	curr_cfg = ""
	for i in range(len(grid)):
		if grid[i] == "O":
			curr_cfg += "1"
		else:
			curr_cfg +="0"
	if curr_cfg in win_configs:
		return "O"
	
	return "~"


def play():
	"""
	I'm thinking of a logic to make this computer play this game. 
	
		1. 	Have a bitmap of victory configs and use those to 
		   	know when the game is over and also to know which
			victory case to play for, given the current config.
	
		2. 	This is a tad too ambitious, here I'm thinking of
			using this oppurtunity to teach myself machine learning
			Can I use the principles of mach-learn.. to avoid 	
			having to think up of a algorithm for playing this 
			game?
	"""
	#for now the moves are random
	empty_cells = get_empty_cells()
	if not empty_cells:
		return -1
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
		screen.addstr(0,0,draw_grid.format(*grid))
		screen.move(y,x)
		while True: 
			char = screen.getch()
			if char == ord('q'):
				break
			if game_over:
				continue
			#move the cursor
			elif char == curses.KEY_RIGHT:
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
				bot_move = play()
				if bot_move != -1:
					grid[bot_move] = "O"

			#render changes.
			screen.addstr(0,0,draw_grid.format(*grid))
			screen.move(y,x)

			if is_game_over():	
				game_over = True
				winner = get_winner()
				if winner == "~":
					screen.addstr(7,0,"Game Over - Its a Draw.")
				elif winner == "X":
					screen.addstr(7,0,"Game Over - You Win!")
				elif winner == "O":
					screen.addstr(7,0,"Game Over - I Win!!!!")
			

	finally:
    	# shut down cleanly
		curses.nocbreak(); screen.keypad(0); curses.echo()
		curses.endwin()

if __name__ == '__main__':
	print_grid()

