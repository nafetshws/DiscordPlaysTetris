from PIL import Image, ImageFilter
import random
import os

class TetrisBot:

	def __init__(self):
		self.board = []
		self.current_block_pos = {"RotationPoint": [], "RelativePoints": []}
		self.tetromino_type = 0
		self.can_go_down_further = True
		self.image_count = 0

		#paths to sprites
		self.res_path = os.path.dirname(__file__) + "/../res/" 
		self.sprites_path = self.res_path + "sprites/"
		self.current_board_path = self.res_path + "current_board.png"

		#Constants
		self.TILE_SIZE = 64

		self.init_board()

	def init_board(self):
		# init a 10x20 board
		self.board =[
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]												

	'''
	The RotationPoint stores the absolute coordinates of the rotation point of the tetromino.
	The RelativePoints are relative coordinates to the rotation point
	The method converts all coordinates of the tetromino tiles to absolute coordinates
	'''
	def get_absolute_coordinates(self, points=None, rotation=None):
		absolute_coordinates = []

		#init values if no params were given
		if points == None:
			points = self.current_block_pos["RelativePoints"]
		if rotation == None:
			rotation = self.current_block_pos["RotationPoint"]

		# convert relative to absolute
		for relative_point in points:
			col = relative_point[0] + rotation[0]		
			row = (rotation[1] - relative_point[1])
			absolute_coordinates.append([col, row])

		return absolute_coordinates

	def move_left(self):
		#check if one tile is already in the leftmost position
		for pos in self.get_absolute_coordinates():
			if pos[0] <= 0:
				# Tetromino cannot be moved to the left
				return

		#check if every tile can move left
		for pos in self.get_absolute_coordinates():
			row = pos[1]
			col = pos[0]
			#check if tile on the left is not blank and is not part of the tetromino
			if self.board[row][col - 1] != 0 and [col - 1, row] not in self.get_absolute_coordinates():
				return

		#Move tetromino to the left
		self.remove_tetromino_from_board()

		if len(self.current_block_pos["RotationPoint"]) != 0:
			#Move the rotation point one tile to the left
			self.current_block_pos["RotationPoint"][0] -= 1 

		self.add_tetromino_to_board()

	def move_right(self):
		for pos in self.get_absolute_coordinates():
			if pos[0] >= 9:
				return

		#check if every tile can move right
		for pos in self.get_absolute_coordinates():
			row = pos[1]
			col = pos[0]
			#check if tile on the right is not blank and is not part of the tetromino
			if self.board[row][col + 1] != 0 and [col + 1, row] not in self.get_absolute_coordinates():
				return

		#Move tetromino to the right
		for pos in self.get_absolute_coordinates():
			#Make the tiles at the old coordinates blank
			self.board[pos[1]][pos[0]] = 0
		if len(self.current_block_pos["RotationPoint"]) != 0:
			#Move the rotation point one tile to the left
			self.current_block_pos["RotationPoint"][0] = self.current_block_pos["RotationPoint"][0] + 1
		for pos in self.get_absolute_coordinates():		
			#Set new tile positions
			self.board[pos[1]][pos[0]] = self.tetromino_type

	'''
	How to rotate by a degrees arround an origin (clockwise) 
	xNew = x * cos(a) - y * sin(a)
	yNew = x * sin(a) + y * cos(a)
	-> for 90 degrees:
	xNew = -y
	yNew = x
	'''
	def rotate(self):
		new_relative_points = []
		self.remove_tetromino_from_board()
		#rotate each tile of the tetromino arround the origin
		for point in self.current_block_pos["RelativePoints"]:
			new_relative_points.append([point[1], -point[0]])

		#check if rotation fits
		if self.check_if_tetromino_fits(new_relative_points):
			self.current_block_pos["RelativePoints"] = new_relative_points
			self.add_tetromino_to_board()
			return True

		#unable to rotate tetromino
		self.add_tetromino_to_board()
		return False
		#else:
		#	self.add_tetromino_to_board()
		#	self.move_down_current_block(1)

	def move_down_tetromino(self, distance):
		can_go_down_further = True

		#remove tetromino from board
		self.remove_tetromino_from_board()

		#Move tetromino at most <distance> blocks down
		for _ in range(distance):
			if self.can_tetromino_move_down():
				#move rotation point down by one
				self.current_block_pos["RotationPoint"] = [self.current_block_pos["RotationPoint"][0], self.current_block_pos["RotationPoint"][1] + 1]
				can_go_down_further = True
			else:
				can_go_down_further = False
				break

		#add tetromino to board again
		self.add_tetromino_to_board()

		return can_go_down_further

	#Sets tetromino positions on the board
	def add_tetromino_to_board(self):
		for coords in self.get_absolute_coordinates():
			row = coords[1]
			col = coords[0]
			self.board[row][col] = self.tetromino_type

	#Remove tetromino from board
	def remove_tetromino_from_board(self):
		for coord in self.get_absolute_coordinates():
			col = coord[0]
			row = coord[1] 
			self.board[row][col] = 0

	#takes new relative points of the tetromino and checks if it fits on the board
	def check_if_tetromino_fits(self, new_relative_points, new_rotation_point=None):
		for point in self.get_absolute_coordinates(points=new_relative_points, rotation=new_rotation_point):
			#check if rotated tetromino is out of map (y-axis) 
			if point[1] > len(self.board[0]) - 1 or point[1] < 0:
				return False
			#check if rotated tetromino is out of map (x-axis) 
			if point[0] >= len(self.board) or point[0] < 0:
				return False
			#check if tile position is blank			
			if self.board[point[1]][point[0]] != 0:
				return False

		return True

	#checks if tetromino has hit a tile or the bottom row
	def can_tetromino_move_down(self):
		for pos in self.get_absolute_coordinates():
			if pos[1] >= len(self.board)-1:
				return False

		#check if every tile can move down
		for pos in self.get_absolute_coordinates():
			row = pos[1]
			col = pos[0]
			#check if tile below is not blank and is not part of the tetromino
			if self.board[row + 1][col] != 0 and [row + 1, col] not in self.get_absolute_coordinates():
				return False

		return True

	#clears all full lines
	def clear_lines(self):
		#init dict
		elements_per_row = {}
		for i in range(len(self.board)):
			elements_per_row[i] = 0

		#count elements per row
		for row in range(len(self.board)):
			for col in range(len(self.board[row])):
				if self.board[row][col] != 0:
					elements_per_row[row] += 1

		#clear full lines
		for row in range(len(self.board)):
			if elements_per_row[row] >= 10:
				self.delete_row(row)

	#removes a line and placed an empty line on top
	def delete_row(self, list_index):
		self.board.pop(list_index)
		tmp = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.board.insert(0, tmp)

	def spawn_new_tetromino(self):
		new_tetromino_type = random.randint(1, 5)
		self.current_block_pos["RelativePoints"].clear()
		self.current_block_pos["RotationPoint"].clear()

		new_relative_points = [] 
		new_rotation_point = []

		if new_tetromino_type == 1:
			#L-form 
			new_relative_points = [[-1, -1],[-1, 0],[0, 0], [1, 0]]
			new_rotation_point = [4, 0]
		elif new_tetromino_type == 2:
			#O-form 
			new_relative_points = [[0, 1],[0, 0], [1, 0], [1, 1]]
			new_rotation_point = [4, 1]
		elif new_tetromino_type == 3:
			#I-Form 
			new_relative_points = [[-1, 0],[0, 0], [1, 0], [2, 0]]
			new_rotation_point = [4, 0]
		elif new_tetromino_type == 4:
			#S-form
			new_relative_points = [[-1, 0],[0, 0], [0, 1], [1, 1]]
			new_rotation_point = [4, 1]
		elif new_tetromino_type == 5:
			#T-form 
			new_relative_points = [[-1, 1],[0, 0], [0, 1], [1, 1]]
			new_rotation_point = [4, 1]
		else:
			print("Error when gernerating random number")

		#check if tetromino can be spawned without overlapping with another piece
		if not self.check_if_tetromino_fits(new_relative_points, new_rotation_point=new_rotation_point):
			return False

		#set values for the new tetromino 
		self.current_block_pos["RelativePoints"] = new_relative_points 
		self.current_block_pos["RotationPoint"] = new_rotation_point 
		self.tetromino_type = new_tetromino_type

		#spawn new tetromino on map
		self.add_tetromino_to_board()

		return True

	def game_over(self):
		board = Image.open(self.current_board_path).convert("RGBA")
		board = board.filter(ImageFilter.BLUR)
		board = board.filter(ImageFilter.BLUR)
		board = board.filter(ImageFilter.BLUR)
		sign = Image.open(self.sprites_path + "game_over.png").convert("RGBA")
		sign = sign.resize((512, 256))
		board.paste(sign, (80, 380), sign)
		board.save(self.current_board_path, "PNG")
		
	def update_image(self):
		width = (len(self.board[0])) * self.TILE_SIZE
		height = (len(self.board)) * self.TILE_SIZE 

		#open sprites
		cyan   = Image.open(self.sprites_path + "cyan.png")
		yellow = Image.open(self.sprites_path + "yellow.png")
		purple = Image.open(self.sprites_path + "purple.png")
		green  = Image.open(self.sprites_path + "green.png")
		orange = Image.open(self.sprites_path + "orange.png")
		blank  = Image.open(self.sprites_path + "blank.png")

		#resize sprites
		cyan   =   cyan.resize((self.TILE_SIZE, self.TILE_SIZE))
		yellow = yellow.resize((self.TILE_SIZE, self.TILE_SIZE))
		purple = purple.resize((self.TILE_SIZE, self.TILE_SIZE))
		green  =  green.resize((self.TILE_SIZE, self.TILE_SIZE))
		orange = orange.resize((self.TILE_SIZE, self.TILE_SIZE))
		blank  =  blank.resize((self.TILE_SIZE, self.TILE_SIZE))

		#create new image based on array
		new_image = Image.new("RGB", (width, height), (250, 250, 250))
		tile_dict = {
			0: blank,
			1: orange,
			2: yellow,
			3: cyan,
			4: green,
			5: purple
		}

		for row in range(len(self.board)):
			for col in range(len(self.board[0])):
				#calculate position of tile
				tile_position = (col * self.TILE_SIZE, row * self.TILE_SIZE)
				# paste tile at according grid position based on col and row 
				new_image.paste(tile_dict[self.board[row][col]], tile_position)

		self.image_count += 1		
		#save image
		new_image.save(self.current_board_path, "PNG")

	#opens the picture of the current board
	def show_board(self):
		image = Image.open(self.current_board_path)
		image.show()

	def run_game(self):
		self.start_game()
		while(True):
			action = int(input())

			if(action == 0):
				self.move_left()
			elif(action == 1):
				self.move_right()
			else:
				self.rotate()

			can_move_down_further = self.move_down_tetromino(1)
			if not can_move_down_further:
				can_be_spawned = self.spawn_new_tetromino()
				if not can_be_spawned:
					break

			self.update_image()

		self.game_over()
			
			
	def start_game(self):
		self.spawn_new_tetromino()
		self.update_image()

if __name__ == "__main__":
	bot = TetrisBot()
	bot.run_game()

	#bot.start_game()
	