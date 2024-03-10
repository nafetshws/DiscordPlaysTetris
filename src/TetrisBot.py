from PIL import Image, ImageFilter
import random

class TetrisBot:

	def __init__(self):
		self.board = []
		self.current_block_pos = {"RotationPoint": [], "RelativePoints": []}
		self.number = 0
		self.can_go_down_further = True
		self.current_count = 0
		self.res_path = "../res/"
		self.sprites_path = self.res_path + "sprites/"
		self.init_board()

	def init_board(self):
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

	def convert_rel_to_con(self, points=None, rotation=None):
		concrete_values = []
		if points == None:
			points = self.current_block_pos["RelativePoints"]
		if rotation == None:
			rotation = self.current_block_pos["RotationPoint"]
		for relative_point in points:
			col = relative_point[0] + rotation[0]		
			row = (rotation[1] - relative_point[1])
			concrete_values.append([col, row])
		return concrete_values

	def check_ground(self):
		for pos in self.convert_rel_to_con():
			row_index = pos[1]
			column_index = pos[0]
			is_in_current = False

			if row_index == (len(self.board) - 1):
				return False

			if self.board[row_index + 1][column_index] != 0:
				for pos_2 in self.convert_rel_to_con():
					if pos_2[1] == row_index + 1 and pos_2[0] == column_index:
						is_in_current = True
						break
				if not is_in_current:
					return False

		return True

	def move_left(self):
		can_move_left = True
		for pos in self.convert_rel_to_con():
			if pos[0] <= 0:
				can_move_left = False
				break

		if can_move_left:
			for pos in self.convert_rel_to_con():
				if self.board[pos[1]][pos[0] - 1] != 0: 
					for pos_2 in self.convert_rel_to_con():
						if self.board[pos_2[1]][pos_2[0]] == self.board[pos[1]][pos[0] - 1]:
							can_move_left = True
							break
						else:
							can_move_left = False
					if not can_move_left:
						break

		#adjust to relative
		if can_move_left:
			for pos in self.convert_rel_to_con():
				self.board[pos[1]][pos[0]] = 0
			if len(self.current_block_pos["RotationPoint"]) != 0:
				self.current_block_pos["RotationPoint"][0] = self.current_block_pos["RotationPoint"][0] - 1
			for pos in self.convert_rel_to_con():
				self.board[pos[1]][pos[0]] = self.number

	def move_right(self):
		can_move_right = True
		for pos in self.convert_rel_to_con():
			if pos[0] >= 9:
				can_move_right = False
				break
		if can_move_right:
			for pos in self.convert_rel_to_con():
				if self.board[pos[1]][pos[0] + 1] != 0: 
					for pos_2 in self.convert_rel_to_con():
						if self.board[pos_2[1]][pos_2[0]] == self.board[pos[1]][pos[0] + 1]:
							can_move_right = True
							break
						else:
							can_move_right = False
					if not can_move_right:
						break							
		if can_move_right:
			for pos in self.convert_rel_to_con():
				self.board[pos[1]][pos[0]] = 0
			if len(self.current_block_pos["RotationPoint"]) != 0:
				self.current_block_pos["RotationPoint"][0] = self.current_block_pos["RotationPoint"][0] + 1
			for pos in self.convert_rel_to_con():		
				self.board[pos[1]][pos[0]] = self.number

	def check_if_movement_is_ok(self, old, new):
		board = self.board	
		old_values = self.convert_rel_to_con(rotation=old)
		for value in old_values:
			board[value[1]][value[0]] = 0
		new_values = self.convert_rel_to_con(rotation=new)
		for value in new_values:
			if value[0] < 10 and value[0] >= 0:
				if board[value[1]][value[0]] != 0:
					return False
			else:
				return False
		return True

	def move_down_current_block(self, amount):
		if len(self.current_block_pos["RelativePoints"]) > 0:
			for n in range(amount):
				if self.check_ground():
					for pos in self.convert_rel_to_con():
						number = self.board[pos[1]][pos[0]]
						self.board[pos[1]][pos[0]] = 0
					self.current_block_pos["RotationPoint"] = [self.current_block_pos["RotationPoint"][0], self.current_block_pos["RotationPoint"][1] + 1]
					self.can_go_down_further = True
				else:
					self.can_go_down_further = False
					break
			for pos in self.convert_rel_to_con():
				row = pos[1]
				col = pos[0]
				self.board[row][col] = self.number

		if not self.can_go_down_further:
			self.update_board()
			self.spawn_new_block()
	

	def delete_current_pos(self):
		for i in range(len(self.convert_rel_to_con())):
			row = self.convert_rel_to_con()[i][1]
			col = self.convert_rel_to_con()[i][0]
			self.board[row][col] = 0

	def update_block_position(self):
		for i in range(len(self.convert_rel_to_con())):
			row = self.convert_rel_to_con()[i][1]
			col = self.convert_rel_to_con()[i][0]
			self.board[row][col] = self.number

	def check_if_fits(self, new_points):
		abs_points = self.convert_rel_to_con(points=new_points)
		for point in abs_points:
			if point[1] > len(self.board[0]) - 1 or point[1] < 0:
				return False
			if point[0] >= len(self.board) or point[0] < 0:
				return False
			if not point[0] >= 10:
				if self.board[point[1]][point[0]] != 0:
					return False
			else:
				return False
		return True

	def rotate(self):
		new_points = []
		self.delete_current_pos()
		for point in self.current_block_pos["RelativePoints"]:
			new_points.append([point[1], -point[0]])
		if self.check_if_fits(new_points):
			self.current_block_pos["RelativePoints"] = new_points
			self.update_block_position()
		else:
			self.update_block_position()
			self.move_down_current_block(1)

				
	def update_board(self):
		trash = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, "13": 0, "14": 0, "15": 0}
		for row in range(len(self.board)):
			for column in range(len(self.board[row])):
				if self.board[row][column] != 0:
					index_str = str(row)
					trash[index_str] += 1
		for i in range(16):
			i_str = str(i)
			if trash[i_str] == 10:
				self.delete_row(i)

	def delete_row(self, list_index):
		self.board.pop(list_index)
		a = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.board.insert(0, a)

	def spawn_new_block(self):
		number = random.randint(1, 5)
		self.current_block_pos["RelativePoints"].clear()
		self.current_block_pos["RotationPoint"].clear()
		is_valid = True
		self.number = number

		if number == 1:
			#L-form 
			is_valid = True
			for n in range(len(self.board[0])):
				if self.board[0][n] != 0 or self.board[1][n] != 0:
					self.game_over()
					is_valid = False
					self.init_board()
					self.start_game()	
					break
			if is_valid:
				for n in range(len(self.board[0])):
					if n == 4 or n == 5 or n == 6:
						self.board[0][n] = number
						if n == 4:
							self.board[1][n] = number
				self.current_block_pos["RelativePoints"] = [[-1, -1],[-1, 0],[0, 0], [1, 0]]
				self.current_block_pos["RotationPoint"] = [5,0]
		elif number == 2:
			#block-form 
			is_valid = True
			for n in range(len(self.board[0])):
				if self.board[0][n] != 0 or self.board[1][n] != 0:
					self.game_over()
					is_valid = False
					self.init_board()
					self.start_game()	
					break
			if is_valid:
				for n in range(len(self.board[0])):
					if n == 5 or n == 6:
						self.board[0][n] = number
						self.board[1][n] = number

				self.current_block_pos["RelativePoints"] = [[0, 1],[0, 0], [1, 0], [1, 1]]
				self.current_block_pos["RotationPoint"] = [5,1]
		elif number == 3:
			#I-Form 
			is_valid = True
			for n in range(len(self.board[0])):
				if self.board[0][n] != 0:
					is_valid = False
					self.game_over()
					self.init_board()
					self.start_game()	
					break
			if is_valid:
				for n in range(len(self.board[0])):
					if n == 4 or n == 5 or n == 6 or n == 7:
						self.board[0][n] = number

				self.current_block_pos["RelativePoints"] = [[-1, 0],[0, 0], [1, 0], [2, 0]]
				self.current_block_pos["RotationPoint"] = [5,0]

		elif number == 4:
			#s-form
			is_valid = True
			for n in range(len(self.board[0])):
				if self.board[0][n] != 0 or self.board[1][n]:
					is_valid = False
					self.game_over()
					self.init_board()
					self.start_game()	
					break
			if is_valid:
				for n in range(len(self.board[0])):
					if n == 6 or n == 7:
						self.board[0][n] = number
						if n == 6:
							self.board[1][n] = number
					elif n == 5:
						self.board[1][n] = number 
				
				self.current_block_pos["RelativePoints"] = [[-1, 0],[0, 0], [0, 1], [1, 1]]
				self.current_block_pos["RotationPoint"] = [6,1]

		elif number == 5:
			#T-form 
			is_valid = True
			for n in range(len(self.board[0])):
				if self.board[0][n] != 0 or self.board[1][n] != 0:
					self.game_over()
					is_valid = False
					self.init_board()
					self.start_game()	
					break
			if is_valid:
				for n in range(len(self.board[0])):
					if n == 4 or n == 5 or n == 6:
						self.board[0][n] = number
						if n == 5:
							self.board[1][n] = number

				self.current_block_pos["RelativePoints"] = [[-1, 1],[0, 0], [0, 1], [1, 1]]
				self.current_block_pos["RotationPoint"] = [5,1]
		else:
			print("Error when gernerating random number")


	def game_over(self):
		board = Image.open(self.res_path + "current_board.png").convert("RGBA")
		board = board.filter(ImageFilter.BLUR)
		board = board.filter(ImageFilter.BLUR)
		board = board.filter(ImageFilter.BLUR)
		sign = Image.open(self.sprites_path + "game_over.png").convert("RGBA")
		sign = sign.resize((512, 256))
		board.paste(sign, (80, 380), sign)
		#TOOD: change back to current board
		board.save(self.res_path + "current_board_over.png", "PNG")
		
	def update_picture(self):
		total_height = (len(self.board))*64
		total_width = (len(self.board[0]))*64
		#open sprites
		cyan = Image.open("sprites/cyan.png")
		yellow = Image.open("sprites/yellow.png")
		purple = Image.open("sprites/purple.png")
		green = Image.open("sprites/green.png")
		orange = Image.open("sprites/orange.png")
		blank = Image.open("sprites/blank.png")
		#resize sprites
		cyan = cyan.resize((64, 64))
		yellow = yellow.resize((64, 64))
		purple = purple.resize((64, 64))
		green = green.resize((64, 64))
		orange = orange.resize((64, 64))
		blank = blank.resize((64, 64))
		image_size = cyan.size
		new_image = Image.new("RGB", (total_width, total_height), (250, 250, 250))
		for i in range(len(self.board)):
			for n in range(len(self.board[0])):
				if self.board[i][n] == 0:
					new_image.paste(blank, (n*64, i*64))
				elif self.board[i][n] == 1:
					new_image.paste(orange, (n*64, i*64))
				elif self.board[i][n] == 2:
					new_image.paste(yellow, (n*64, i*64))
				elif self.board[i][n] == 3:
					new_image.paste(cyan, (n*64, i*64))
				elif self.board[i][n] == 4:
					new_image.paste(green, (n*64, i*64))					
				elif self.board[i][n] == 5:
					new_image.paste(purple, (n*64, i*64))
				else:
					print("Error: list is wrong")
		self.current_count += 1		
		new_image.save("sprites/current_board.png", "PNG")

	def show_board(self):
		image = Image.open("sprites/current_board.png")
		image.show()
			
	def start_game(self):
		self.spawn_new_block()
		self.update_picture()

if __name__ == "__main__":
	bot = TetrisBot()
	bot.game_over()



	#bot.start_game()
	