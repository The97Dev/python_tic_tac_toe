import tkinter as tk
import tkinter.font as font

valid_win_list = [
	[0,1,2],[3,4,5],
	[6,7,8],[0,3,6],
	[1,4,7],[2,5,8],
	[0,4,8],[2,4,6]
]

root = tk.Tk()
	
cells = []

my_font = font.Font(size=20)

def build_ui():
	column = tk.PanedWindow(orient=tk.VERTICAL)
	for x in range(1,4):
		row = tk.PanedWindow(orient=tk.HORIZONTAL)
		for i in range(1,4):
			cell = tk.Button(root)
			cell["width"] = 10
			cell["height"] = 5
			cell["font"] = my_font
			cells.append(cell)
			row.add(cell)
		row.pack()
	column.add(row)
	column.pack()

class Game :
	def __init__(self):
		self.board = Board()
	def start(self) :
		build_ui()
		for cell_index in range(len(cells)):
			cells[cell_index].configure(command = lambda i = cell_index: self.board.reserve_cell(i))

class Board :
	def __init__(self) : 
		self.reserved_cells =  [(0) for i in range(0,9)]
		self.board_ui_controller =  BoardUIController()
		self.first_player = Player("X","green")
		self.second_player =  Player("O","red")
		self.current_player = self.first_player

	def reserve_cell(self,cell_index) :
		if(not(self.is_cell_already_reserved(cell_index))) : 
			self.reserved_cells[cell_index] = 1
			self.board_ui_controller.update_cell(cell_index,self.current_player)
			self.current_player.reserve_cell(cell_index)
			self.check_winner()
		
	
	def switch_player(self) :
		if(self.current_player == self.first_player) :
			self.current_player = self.second_player
		else :
			self.current_player = self.first_player
		
	
	def check_winner(self):
		if(self.is_enough_reserved_cells_to_check()):
			player_state = self.current_player.check()
			if(player_state[0]):
				self.reserved_cells =  [(1) for i in range(0,9)]
				self.current_player.score += 1
				self.board_ui_controller.colorize_cells(player_state[1],self.current_player.color);
				# self.clean_board()
			# if(self.are_all_cells_reserved()):
				# self.clean_board()
		self.switch_player()


	def clean_board(self):
		self.reserved_cells =  [(0) for i in range(0,9)]
		self.first_player.clean_reserved()
		self.second_player.clean_reserved()
		self.board_ui_controller.clean_board()
	
	def is_enough_reserved_cells_to_check(self):
		return len(list(filter(lambda cell_value : cell_value == 1,self.reserved_cells))) > 4
	def is_cell_already_reserved(self,cell_index):
		return  self.reserved_cells[cell_index] == 1
	def are_all_cells_reserved(self):
		return len(list(filter(lambda cell_value : cell_value == 1,self.reserved_cells))) == len(self.reserved_cells)


class BoardUIController:
	def __init__(self):
		pass
	def update_cell(self,cell_index,player):
		cells[cell_index]["text"] = player.symbol

	def colorize_cells(self,cells_indices,color):
		for cell_index in cells_indices :
			cells[cell_index]["bg"] = color

	def clean_board(self):
		for cell in cells : 
			cell["text"] = ""
	
	



 
class Player:
	def __init__(self,symbol,color):
		self.color = color
		self.reserved_cells = []
		self.score = 0
		self.symbol = symbol
	
	def reserve_cell(self,cell_index):
		self.reserved_cells.append(cell_index)
	
	def check(self):
		if(len(self.reserved_cells) >= 3) :
			for list_ in valid_win_list :
				if(self.exist_on_reserved(list_[0]) and  self.exist_on_reserved(list_[1])and self.exist_on_reserved(list_[2])) :
					return [True,list_]
		return [False]
	
	def clean_reserved(self) :
		self.reserved_cells = []
	
	def exist_on_reserved(self,cell_index): 
		return self.reserved_cells.count(cell_index) > 0



game = Game()
game.start()
root.mainloop()

