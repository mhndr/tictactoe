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
	#very bruteforce, very ugly :-(
	#look at rows
	for i in (0,3,6):
		if grid[i] != " ":
			if grid[i]==grid[i+1]==grid[i+2]:
				return grid[i]
	#look at cols
	for i in range(3):
		if grid[i] != " ":
			if grid[i]==grid[i+3]==grid[i+6]:
				return grid[i]
	
	#look at diagonals
	if grid[0] != " " and grid[0]==grid[4]==grid[8]:
		return grid [0]
	if grid[2] != " " and grid[2]==grid[4]==grid[6]:
		return grid[2]

	return "~"

def rank_moves(cell,grid):
	empty_cells = get_empty_cells()
	if not empty_cells:
		winner = get_winner()
		if winner == "X":
			return 10		
		elif winner == "O":
			return -10
		elif winner == "~":
			return 0
	else:
		for cell in empty_cells:
			grid[cell] = "X"
			ranked_cells[cell] = rank_moves(cell,grid_copy)
			

def play():
	empty_cells = get_empty_cells()
	if not empty_cells or is_game_over():
		return -1
#	if empty_cells == 8:
	rand = random.randrange(0,len(empty_cells))
	return empty_cells[rand]

#	ranked_cells = {k:0 for k in empty_cells}
#	grid_copy = grid

#	the idea here is to recursively go through all
#	possible moves and rank them 
#	for cell in empty_cells:
#		ranked_cells[cell] = rank_moves(cell,grid_copy)
	

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
				bot_move = play()
				if bot_move != -1:
					grid[bot_move] = "O"

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


