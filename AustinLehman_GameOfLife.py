# Austin Lehman
# Game Of Life
# CSC470 - Automata & Complexity Theory
# Dr. Lang
# 11/22/22
# 
# This program runs conways game of life. When ran it will run
# the immigration(red/blue) variation of game of life. In this variation
# when a cell comes to life its color depends on the majority of
# its  neighbors colors(red/blue). This this game will track the generations/total alive/
# and who is winning in a current generation. If all cells die it will show the final generation
# count and which color was the last alive. 
# if a single cell is the last cell alive it will be "presented" on the screen as the winner
# The following keys can be pressed to control the game
# q             -> quits the game
# space button  -> restart game
# left arrow    -> slows down game on press not hold minimum is 1
# right arrow   -> speeds up game on press not hold  max is 20

#import tools for use in game. Numpy for array management and pygame for display
import numpy as np
import pygame as pg

#colors values in functions Black = 0, Red = 1, Blue = 2
#setting RGB for colors
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)

#settings for w/h of screen
width = 1000
height = width

#setting for speed of game
speed = 3.5

#track number of generations
gen = 1

#track total and number of color
#set winning to default black(off)
totalAlive = 0
totalRed = 0
totalBlue = 0
winning = "black"


#Grid size(how many squares 50x50 default)
grid = 150

#arraysize make matrix to store values with a distro of 0-2 with 0(dead cell) 
#having greatest weight of 80% 
arr = np.random.choice([0,1,2],size = (grid,grid),p=[0.8,0.1,0.1])

#count the total red/blue and total alive
totalRed = np.count_nonzero(arr == 1)
totalBlue = np.count_nonzero(arr == 2)
totalAlive = totalRed + totalBlue



#see who is winning when random array is first created
if(totalRed > totalBlue):
	winning = "Red"
elif(totalRed < totalBlue):
	winning = "Blue"
else:
	winning = "Tie"

#set prevgen/winner to initial gen,used in tracking generation stats
prevGen = gen
prevWinner = winning

#this function checks and returns how many neighbors, and how many of each color neighbor a cell has
def check_neighbors(arr,x,y):
	#track how many of each color surround neighbors
	red = 0
	blue = 0

	#These will increment the count of blue/red if that cell is alive with that color
	#Checking the 8 cells surrounding the x,y coordinates passed to function

	#check current row
	if(arr[x,(y-1)%grid] == 1):
		red +=1
	elif(arr[x,(y-1)%grid]== 2):
		blue += 1

	if(arr[x,(y+1)%grid] == 1):
		red +=1
	elif(arr[x,(y+1)%grid] == 2):
		blue += 1


	#check bottom row
	if(arr[(x+1)%grid,(y-1)%grid]== 1):
		red +=1
	elif (arr[(x+1)%grid,(y-1)%grid]== 2):
		blue += 1

	if( arr[(x+1)%grid,y] == 1):
		red +=1
	elif(arr[(x+1)%grid,y]  == 2):
		blue += 1

	if(arr[(x+1)%grid,(y+1)%grid] == 1):
		red +=1
	elif(arr[(x+1)%grid,(y+1)%grid] == 2):
		blue += 1


	#check top row
	if( arr[(x-1)%grid,(y-1)%grid]== 1):
		red +=1
	elif(arr[(x-1)%grid,(y-1)%grid]== 2):
		blue += 1

	if( arr[(x-1)%grid,y] == 1):
		red +=1
	elif( arr[(x-1)%grid,y] == 2):
		blue += 1

	if(arr[(x-1)%grid,(y+1)%grid] == 1):
		red +=1
	elif(arr[(x-1)%grid,(y+1)%grid] == 2):
		blue += 1

	#calculate total ammount of living cells and return 
	#3 tuple with living cells total, red total, and blue total
	return blue+red,red,blue

#this function will update a cell if needed
def update_cell(arr,x,y):
	#state of cell to be returned
	state = arr[x,y]
	#check neighbor count of current cell
	count = check_neighbors(arr,x,y)
	
	#if cell is alive
	if(arr[x,y] > 0):
		#cell will be dead
		if(count[0] > 3 or count[0] < 2):
			state = 0


	#cell is coming to life
	elif (count[0] == 3):
		#if red neighbors outweigh blue or are equal to set state to red
		if (count[1] > count[2]):
			state = 1
		#if blue outweighs red set state blue
		else:
			state = 2
	#return state of cell
	return state

#this function will make a copy of an array and then update for new generation. 
#returns an updated version of the array
def update_generation(arg):

	#make a copy of array
	newarr = np.copy(arg)

	#loop through copy and check cell and neighbors
	for row in range(grid):
		for column in range(grid):
			#update cell of coppied array
			newarr[row,column] = update_cell(arg,row,column)

	#return updated array
	return newarr

#returns the color of a cell to be drawn 
#values maped are red==1, blue ==2
def map_color(arr,x,y):
	#set default color to black
	color = "black"
	#if the cell is 1 its color is red
	if(arr[x,y]==1):
		color = "red"
	#if the cell is 2 the color is blue
	elif(arr[x,y]==2):
		color = "blue"
	#return the color of the cell
	return color

#Draws grid on surface
def draw_rect(screen,arr,height,width,grid):
	#dimensions of rect	
	pxHeight = height/grid
	#for grid draw rectangles
	for row in range(grid):
		for column in range(grid):
			#create a rectangle with dimens and start points 
			rect = pg.Rect(column*(width/grid),row*(width/grid),pxHeight-1,pxHeight-1)
			#draw the rectangle and its color if alivexs
			pg.draw.rect(screen,map_color(arr,row,column),rect)



##main prog start
#initialize game
pg.init()
#set size of screen from global variables
size = (width,height)
#set screensize
screen = pg.display.set_mode(size)
#set initial caption for game
pg.display.set_caption("GOL Generation:%s\tAlive:%s\tRed:%s\tBlue:%s\tWinning: %s" %(gen,totalAlive,totalRed,totalBlue,winning))
#create clock
clock = pg.time.Clock()

#set flag to false for done
done = False

#while done is false continue running the game
while done == False:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			done = True
		elif event.type == pg.KEYDOWN:
			#quit game on q
			if event.key == pg.K_q:
				done = True
			#slow down game with left arrow(press not hold)
			elif event.key == pg.K_LEFT:
				if(speed > 1):
					speed -= 0.3
			#speed up game with right arrow(press not hold)
			elif event.key == pg.K_RIGHT:
				if(speed < 20):
					speed += 0.3
			#start game over
			elif event.key == pg.K_SPACE:

				#recreate game state setting new array and gen to 0

				gen = 0

		    	#arraysize make matrix to store values with a distro of 0-2 with 0 having greatest weight
				arr = np.random.choice([0,1,2],size = (grid,grid),p=[0.9,0.05,0.05])

				#count the total red/blue and total alive
				totalRed = np.count_nonzero(arr == 1)
				totalBlue = np.count_nonzero(arr == 2)
				totalAlive = totalRed + totalBlue

				#see who is winning when random array is first created
				if(totalRed > totalBlue):
					winning = "Red"
				elif(totalRed < totalBlue):
					winning = "Blue"
				else:
					winning = "Tie"

				#set prevgen/winner to initial gen,used in tracking generation stats
				prevGen = gen
				prevWinner = winning

				

	#fill the initial screen with black
	screen.fill(black)


	#display gen to screen
	draw_rect(screen,arr,width,height,grid)
	#update to next gen and adjust generation tracker
	
	
	#update caption with total alive and generation
	if(totalAlive > 1):
		prevWinner = winning
		prevGen = gen
		arr = update_generation(arr)

		#adjust Trackers
		totalRed = np.count_nonzero(arr == 1)
		totalBlue = np.count_nonzero(arr == 2)
		totalAlive = totalRed + totalBlue
		gen += 1
		
		#see who is winning
		if((totalRed > totalBlue) and (totalAlive > 0)):
			winning = "Red"
		elif((totalRed < totalBlue) and (totalAlive > 0)):
			winning = "Blue"
		elif((totalRed == totalBlue) and (totalAlive > 0)):
			winning = "Tie"
		pg.display.set_caption("GOL Generation:%s\tAlive:%s\tRed:%s\tBlue:%s\tWinning: %s" %(gen,totalAlive,totalRed,totalBlue,winning))
	#show final if all cells die, displays last cell	
	else:
		pg.display.set_caption("GAME OVER! GOL Final Generation: %s\t Winner!: %s " %(prevGen,prevWinner))



	#update display
	pg.display.update()

	#wait time between generations
	clock.tick(speed)

#quit the game
pg.quit()
