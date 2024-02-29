import random
import time
from termcolor import colored

#adds a new flour or milk in grid at any random empty cell
def add_new_2(mat): 
	size = len(mat)
	flours = 0
	milks = 0
	for i in range(size):
		for j in range(size):
			if mat[i][j] == '🍞': flours += 1
			if mat[i][j] == '🥛': milks += 1

	# ensures that no one ingredient would be generated 3x in a row
	if abs(flours - milks) <= 2: 
		basicItems = ['🥛', '🥛','🍞','🍞','🍞']
		item = random.choice(basicItems)
	else:
		if flours > milks: item = '🥛'
		else: item = '🍞'

	# chooses a random index for row and column.
	r = random.randint(0, size - 1)
	c = random.randint(0, size - 1)

	# while loop will break as the random cell chosen will be empty (or contains zero)
	while (mat[r][c] != '🟦'):
		r = random.randint(0, size - 1)
		c = random.randint(0, size - 1)

	# we will place a milk or flour at that empty random cell.
	mat[r][c] = item
	

# initializes game / grid at the start
def start_game(size):

	# declaring an empty list then appending 4 list each with four elements as 0.
	mat =[]
	for i in range(size): mat.append(['🟦'] * size)

	# calling the function to add a new 2 in grid after every step
	add_new_2(mat)
	return mat

# # function to get the current state of game
def get_current_state(mat):
    size = len(mat)

    # if we are still left with at least one empty cell, the game is not yet over
    for i in range(size):
        for j in range(size):
            if mat[i][j] == '🟦':  # change 0 to whatever is the default empty cell
                return 'GAME NOT OVER'
            if i + 1 < size and ((mat[i][j] == '🍞' and mat[i + 1][j] == '🥛') or (mat[i][j] == '🥛' and mat[i + 1][j] == '🍞') or (mat[i][j] == '🍞' and mat[i + 1][j] == '🧈') or (mat[i][j] == '🧈' and mat[i + 1][j] == '🍞')):
                return 'GAME NOT OVER'
            if j + 1 < size and ((mat[i][j] == '🍞' and mat[i][j + 1] == '🥛') or (mat[i][j] == '🥛' and mat[i][j + 1] == '🍞') or (mat[i][j] == '🍞' and mat[i][j + 1] == '🧈') or (mat[i][j] == '🧈' and mat[i][j + 1] == '🍞')):
                return 'GAME NOT OVER'

    # else we have lost the game
    return 'GAME OVER'

def board_full(mat):
	size = len(mat)
	is_full = True
	for i in range(size):
		for j in range(size):
			if(mat[i][j] == '🟦'):
				is_full = False
	return is_full
# all the functions defined below are for left swap initially.

# compresses the grid after every step before andafter merging cells.
def compress(mat):
	size = len(mat)

	# bool variable to determine any change happened or not
	changed = False

	# empty grid 
	new_mat = []

	# with all cells empty
	for i in range(size):
		new_mat.append(['🟦'] * size)
		
	# here we will shift entries of each cell to it's extreme
	# left row by row loop to traverse rows
	for i in range(size):
		pos = 0

		# loop to traverse each column in respective row
		for j in range(size):
			if(mat[i][j] != '🟦'):
				
				# if cell is non empty then
				# we will shift it's number to
				# previous empty cell in that row
				# denoted by pos variable
				new_mat[i][pos] = mat[i][j]
				
				if(j != pos):
					changed = True
				pos += 1

	# returning new compressed matrix and the flag variable.
	return new_mat, changed

# merges the cells in matrix after compressing
def merge(mat):
	size = len(mat)
	
	changed = False
	buttersmade = 0
	cakesmade = 0
	for i in range(size):
		for j in range(size - 1):
			

			# if current cell has same value as next cell in the row and they
			# are non empty then
			if(mat[i][j] == '🍞' and mat[i][j + 1] == '🥛' and mat[i][j] != '🟦') or (mat[i][j] == '🥛' and mat[i][j + 1] == '🍞' and mat[i][j] != '🟦'):

				# double current cell value and empty the next cell
				mat[i][j] = '🧈'
				mat[i][j + 1] = '🟦'
				buttersmade += 1
			
			if(mat[i][j] == '🍞' and mat[i][j + 1] == '🧈' and mat[i][j] != '🟦') or (mat[i][j] == '🧈' and mat[i][j + 1] == '🍞' and mat[i][j] != '🟦'):

				# double current cell value and empty the next cell
				mat[i][j] = '🎂'
				mat[i][j + 1] = '🟦'
				cakesmade += 1

				# make bool variable True indicating the new grid
				# after merging is different.
				changed = True

	if buttersmade > 0 or cakesmade > 0:
		print(f'+{50*buttersmade+100*cakesmade} pts')
	return mat, changed, buttersmade, cakesmade

# removes the row if all cells are cakes, and adds points 
def remove_cakes(mat):
		
	size = len(mat)
	for i in range(size):
		for j in range(size):
			if all(mat[i][j] == '🎂' for j in range(size)):
				for j in range(size):
					mat[i][j] = '🟦'
				print('Cakes matched!')
				print('+500 pts')
				return True



# reverses the matrix means reversing the content of
# each row (reversing the sequence)
def reverse(mat):
	size = len(mat)
	new_mat =[]
	for i in range(size):
		new_mat.append([])
		for j in range(size):
			new_mat[i].append(mat[i][size - 1 - j]) ###*****
	return new_mat

# gets the transpose of matrix means interchanging
# rows and column
def transpose(mat):
	size = len(mat)
	new_mat = []
	for i in range(size):
		new_mat.append([])
		for j in range(size):
			new_mat[i].append(mat[j][i])
	return new_mat

# updates the matrix if we move / swipe left
def move_left(grid):

	# first compress the grid
	new_grid, changed1 = compress(grid)

	# then merge the cells.
	new_grid, changed2, butters, cakes = merge(new_grid)
	
	changed = changed1 or changed2

	# again compress after merging.
	new_grid, temp = compress(new_grid)


	# return new matrix and bool changed
	# telling whether the grid is same
	# or different
	return new_grid, changed

# updates the matrix if we move / swipe right
def move_right(grid):

	# to move right we just reverse the matrix 
	new_grid = reverse(grid)

	# then move left
	new_grid, changed = move_left(new_grid)

	# then again reverse matrix will give us desired result
	new_grid = reverse(new_grid)
	return new_grid, changed

# updates the matrix if we move / swipe up
def move_up(grid):

	# to move up we just take transpose of matrix
	new_grid = transpose(grid)

	# then move left (calling all included functions) then
	new_grid, changed = move_left(new_grid)

	# again take transpose will give desired results
	new_grid = transpose(new_grid)
	return new_grid, changed

# updates the matrix if we move / swipe down
def move_down(grid):

	# to move down we take transpose
	new_grid = transpose(grid)

	# move right and then again
	new_grid, changed = move_right(new_grid)

	# take transpose will give desired results.
	new_grid = transpose(new_grid)
	return new_grid, changed

# counts points based on current number of butter and cakes in board
def count_points(mat):
	cakes = 0
	butters = 0
	size = len(mat)
	for i in range(size):
		for j in range(size):
			if mat[i][j] == '🧈':
				butters += 1
			if mat[i][j] == '🎂':
				cakes += 1
	return cakes*150 + butters*50


#prints board, to create representations for diff tiers
def print_board(board): 
	tempBoard = []
	for i in board:
		tempBoard2 = []
		for j in i:
			tempBoard2.append(j)
		tempBoard.append(tempBoard2)
	print('─'*(len(board)*3 + 1))
	for row in tempBoard:
		print('|'+ '|'.join([str(_) for _ in row]) + '|')
		print('─'*(len(board)*3 + 1))
		
# gets the current elapsed time when called 
def timer(start_time):
	return time.time() - start_time

def display_logo():
	print(colored('''
  /$$$$$$            /$$                          /$$$$$$            /$$                
 /$$__  $$          | $$                         /$$__  $$          | $$                
| $$  \__/  /$$$$$$ | $$   /$$  /$$$$$$         | $$  \__/  /$$$$$$ | $$   /$$  /$$$$$$ 
| $$       |____  $$| $$  /$$/ /$$__  $$ /$$$$$$| $$       |____  $$| $$  /$$/ /$$__  $$
| $$        /$$$$$$$| $$$$$$/ | $$$$$$$$|______/| $$        /$$$$$$$| $$$$$$/ | $$$$$$$$
| $$    $$ /$$__  $$| $$_  $$ | $$_____/        | $$    $$ /$$__  $$| $$_  $$ | $$_____/
|  $$$$$$/|  $$$$$$$| $$ \  $$|  $$$$$$$        |  $$$$$$/|  $$$$$$$| $$ \  $$|  $$$$$$$
 \______/  \_______/|__/  \__/ \_______/         \______/  \_______/|__/  \__/ \_______/
                                                                                        
                                                                                        
                                                                                        
                   /$$                                                                  
                  | $$                                                                  
                  | $$        /$$$$$$  /$$   /$$ /$$$$$$$   /$$$$$$                     
                  | $$       /$$__  $$| $$  | $$| $$__  $$ /$$__  $$                    
                  | $$      | $$$$$$$$| $$  | $$| $$  \ $$| $$  \ $$                    
                  | $$      | $$_____/| $$  | $$| $$  | $$| $$  | $$                    
                  | $$$$$$$$|  $$$$$$$|  $$$$$$/| $$  | $$|  $$$$$$$                    
                  |________/ \_______/ \______/ |__/  |__/ \____  $$                    
                                                           /$$  \ $$                    
                                                          |  $$$$$$/                    
                                                           \______/                           
''', 'light_red'))


def print_game_over():
	lines = [
		" ██████╗  █████╗ ███╗   ███╗███████╗    ",
		"██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ",
		"██║  ███╗███████║██╔████╔██║█████╗      ",
		"██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ",
		"╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ",
		" ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝    ",
		"                                        ",
		" ██████╗ ██╗   ██╗███████╗██████╗       ",
		"██╔═══██╗██║   ██║██╔════╝██╔══██╗      ",
		"██║   ██║██║   ██║█████╗  ██████╔╝      ",
		"██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗      ",
		"╚██████╔╝ ╚████╔╝ ███████╗██║  ██║      ",
		" ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝      ",
		"                                        "
	]

	for line in lines:
		for char in line:
			print(char, end='', flush=True)
			time.sleep(0.02)
		print()
		time.sleep(0.2)

# printing controls for user
def print_controls(size):
	print('\n' + colored("Commands are as follows: ", "red", attrs=["bold"]))
	print("'W' or 'w': Move Up")
	print("'S' or 's': Move Down")
	print("'A' or 'a': Move Left")
	print("'D' or 'd': Move Right")
	print("'q' : Exit")
	print('\n' + colored('Possible combinations: ', "red", attrs=["bold"]))
	print('🍞 + 🥛 = 🧈 or 🍞 + 🧈 = 🎂')
	print('\n' + colored('Points system: ', "red", attrs=["bold"]))
	print('50 points for making butter 🧈')
	print('100 points for making cake 🎂')
	print(f"500 points for matching {size} cakes horizontally {'🎂' * size}")
	