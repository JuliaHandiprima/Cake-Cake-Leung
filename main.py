import operations #file where all necessary functions are defined
from termcolor import colored

operations.display_logo()

#taking user inputs
print(colored('Choose your board size. ', "red", attrs=["bold"]))

while True:
	try: 
		size = int(input('Size (4-8): '))
		if 8 >= size >= 4: 
			break
	except: continue
	
print('\n' + colored('Choose between classic (c) or time attack (t) game mode ', "red", attrs=["bold"]))
while True:
	try:
		game_mode = input('Game mode: ')
		if game_mode == 'c' or game_mode == 't': 
			break
	except: continue

#initializing variables
totalSquares = size**2

emojis = {'Cake':'🎂','Butter':'🧈','Milk':'🥛','Flour':'🍞'} #empty cell: 🟦
removecount = 0
print('\n' + colored('Emoji signifier: ', "red", attrs=["bold"]))
print(emojis)

operations.print_controls(size)

points = 0
timeLimit = None
stillTime = True
elapsedTime = 0

operations.time.sleep(1) #delays display of instructions
mat = operations.start_game(size)

operations.time.sleep(4) 
if game_mode == 't':
	print('''
Choose time limit:
	a - 1 minute
	b - 3 minutes
	c - 5 minutes ''')

	while True:
		try:
			timer = input('Time Limit: ')
			if timer == 'a': timeLimit = 60
			elif timer == 'b': timeLimit = 180
			elif timer == 'c': timeLimit = 300
			if timer == 'a' or timer == 'b' or timer == 'c': break
		except: continue

print()
startTime = operations.time.time()
operations.print_board(mat)

while stillTime:
	if game_mode == 't':
		if operations.timer(startTime) > timeLimit:
			print('Remaining time: 0. Make one last move')
			stillTime = False

		else: 
			print(f'Remaining time: {timeLimit - int(operations.timer(startTime))}')

	# taking the user input for next step
	try: 
		while True: 
			x = input("Press the command: ")
			if x.lower() in [_ for _ in 'wasdq']:
				break
	except: 
		continue
	
	if x == 'q':
		break

	# we have to move up
	if(x == 'W' or x == 'w'):

		# call the move_up function
		mat, flag = operations.move_up(mat)

	# to move down
	elif(x == 'S' or x == 's'):
		mat, flag = operations.move_down(mat)

	# to move left
	elif(x == 'A' or x == 'a'):
		mat, flag = operations.move_left(mat)

	# to move right
	elif(x == 'D' or x == 'd'):
		mat, flag = operations.move_right(mat)
	else:
		print("Invalid Key Pressed")

	# get the current state and print it
	status = operations.get_current_state(mat)

	#checks if board is already full
	if operations.board_full(mat): 
		break
	
	# if game not over then continue and add a new two
	if(status == 'GAME NOT OVER'): 
		operations.add_new_2(mat)

	# else break the loop 
	else: 
		break

	
	points = operations.count_points(mat) + removecount*(150*size + 500)

	if operations.remove_cakes(mat) == True:
		points += (500)
		removecount += 1
		
	print(f'Total points: {points}')
	# print the matrix after each move.
	operations.print_board(mat)

	status = operations.get_current_state(mat)
	if(status != 'GAME NOT OVER'):
		break

print(f'Total points: {points}' + '\n')
operations.print_game_over()

