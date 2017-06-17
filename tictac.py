import curses
import sys
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
	for i in range(len(grid)):
		if grid[i] == " ":
			return False
	return True

def play(human_move):
	pass

def print_grid():
	screen = init_curses()
	x = 2
	y = 1
	game_over = False
	try:
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
				bot_move = play(human_move)
				if grid[human_move] == "X":
					grid[human_move] = "O"
				else:
					grid[human_move] = "X"				

			#render changes.
			screen.addstr(0,0,draw_grid.format(*grid))
			if not is_game_over():	
				screen.move(y,x)
			else:
				game_over = True
				screen.addstr(7,0,"Game Over")
	finally:
    	# shut down cleanly
		curses.nocbreak(); screen.keypad(0); curses.echo()
		curses.endwin()

if __name__ == '__main__':
	print_grid()

