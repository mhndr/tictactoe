import curses

grid = (" "," "," "," "," "," ", " "," "," ")
#grid = ("1","2","3","4","5","6", "7","8","9")
draw_grid = "+---+---+---+\n| {0} | {1} | {2} |\n+---+---+---+\
	  \n| {3} | {4} | {5} |\n+---+---+---+\
	  \n| {6} | {7} | {8} |\n+---+---+---+".format(*grid)

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



def print_grid():
	screen = init_curses()
	x = 2
	y = 1
	try:
		screen.addstr(0,0,draw_grid)
		screen.addstr(y,x,"X")
		while True:
			char = screen.getch()
			if char == ord('q'):
				break
			#move the cursor
			elif char == curses.KEY_RIGHT:
				x = x + 3
			elif char == curses.KEY_LEFT:
				x = x - 3
			elif char == curses.KEY_UP:
				y = y - 2 
			elif char == curses.KEY_DOWN:
				y = y + 2
			screen.addstr(0,0,draw_grid)
			screen.addstr(y,x,"X")
	finally:
    # shut down cleanly
		curses.nocbreak(); screen.keypad(0); curses.echo()
		curses.endwin()


if __name__ == '__main__':
	print_grid()

