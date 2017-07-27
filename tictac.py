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
x_moves = set()
o_moves = set()
wins = (set([0, 1, 2]), set([3, 4, 5]), 
		set([8, 6, 7]), set([0, 3, 6]), 
		set([1, 4, 7]), set([8, 2, 5]), 
		set([0, 4, 8]), set([2, 4, 6]))

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
		win = list(win)
		if grid[win[0]] != " " and \
			grid[win[0]] == grid[win[1]] == grid[win[2]]:
			return grid[win[0]]
	return "~"


def get_winning_move(moves):
	winning_moves = []
	for win in wins:
		if win.intersection(moves):
			winning_moves = list(win.difference(moves))
			if len(winning_moves) == 1 and valid_move(winning_moves[0]):
				return winning_moves[0]
	return None	

def play():
	empty_cells = get_empty_cells()
	if not empty_cells: 
		return -1

	# see if there's an immediate winning move at hand.
	winning_move = get_winning_move(o_moves)		
	if winning_move:
		return winning_move

	#find winning options for human and block them
	blocking_move = get_winning_move(x_moves)
	if blocking_move:		
		return blocking_move	

	#fall back to a random move if there isn't an immediate win or block.	
	#TODO: can optimise this to pick a move that's closer to a winning combination.
	rand = random.randrange(0,len(empty_cells))
	return empty_cells[rand]

def draw_start_screen(screen):
	#decide who should play first
	bot_first = random.randint(0,100)%2
	if bot_first:
		bot_move = play()
		if bot_move != -1:
			grid[bot_move] = "O"
			o_moves.add(bot_move)
	screen.erase()	
	screen.addstr(0,0,draw_grid.format(*grid))
	screen.addstr(7,0,"Use arrow keys to play.")
	

def main_loop():
	screen = init_curses()
	x = 2
	y = 1
	game_over = False
	try:
		draw_start_screen(screen)
		while True: 
			char = screen.getch()
			if char == ord('q'):
				break

			if game_over:
				screen.addstr(7,0,"Press 'q' to exit\nPress 'r' to replay")
				if char == ord('r'):
					game_over = False
					x_moves.clear()
					o_moves.clear()
					for i in range(len(grid)):
						grid[i] = " "
					draw_start_screen(screen)
				continue
			
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
				x_moves.add(human_move)
				bot_move = play()
				if bot_move != -1:
					grid[bot_move] = "O"
					o_moves.add(bot_move)
			if is_game_over():	
				game_over = True
				winner = get_winner()
				if winner == "~":
					screen.addstr(7,0,"Game Over - Its a Draw.   ")
				elif winner == "X":
					screen.addstr(7,0,"Game Over - You Win!      ")
				elif winner == "O":
					screen.addstr(7,0,"Game Over - I Win!!!!     ")
		
			#render changes.
			screen.addstr(0,0,draw_grid.format(*grid))
			screen.move(y,x)

	finally:
    	# shut down cleanly
		curses.nocbreak(); screen.keypad(0); curses.echo()
		curses.endwin()

if __name__ == '__main__':
	main_loop()


