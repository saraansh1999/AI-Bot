import numpy as np
import time as tp
import random


class Team17:

	def __init__(self):
		
		self.grids = np.chararray((3, 3, 3, 3, 2))
		self.grids[:] = '-'
		self.ret = []
		self.bot_symbol = ''
		self.opp_symbol = ''
		self.unavailable = np.chararray((3, 3, 2))
		self.unavailable[:] = '-'
		self.stack = []
		self.small_win =100
		self.big_win = 1000
		self.small_lose = -self.small_win
		self.big_lose = -self.big_win
		self.small_draw = 45
		self.double_move = 10
		self.single_move=2
		self.single_single=1
		self.utility = 0
		self.depth=2
		self.move_no=0
		self.depth_no=8
		self.repitition = 0
		self.time = 3
		self.start =0
		self.total_time =23
		self.prev = 0
		# self.no_victory = 1
		# self.no_lose = 1
		# self.util = 0

		# # 'x' plays first
		# self.player = int(input("Bot is player: "))
		# if self.player == 1:
		# 	self.bot_symbol = 'x'
		# 	self.opp_symbol = 'o'
		# 	self.next_row, self.next_col = self.set(random.randint(0, 1), random.randint(0, 8), random.randint(0, 8), self.bot_symbol)			#random first move
		# 	self.turn = 2
		# else:
		# 	self.bot_symbol = 'o'
		# 	self.opp_symbol = 'x'
		# 	self.turn = 1
		# self.printer()
	
	# def getRep(self, symbol):
	# 	return (1 if symbol == 'x' else 2)

	def calc_time(self):
		print (tp.time()-self.start)

	def stop_run(self):
		if tp.time() - self.start > 22:
			return self.ret
	def getOppSymbol(self, symbol):
		return ('x' if symbol == 'o' else 'o')

	def calc_small_util(self, bot_occur, opp_occur):
		if bot_occur == 3:
			self.utility += 500
		elif opp_occur == 3:
			self.utility -= 500
		elif bot_occur == 2 and opp_occur == 1:
			self.utility -= 50
		elif opp_occur == 2 and bot_occur == 1:
			self.utility += 50
		elif bot_occur == 2 and opp_occur == 0:
			self.utility += 80
		elif bot_occur == 0 and opp_occur == 2:
			self.utility -= 80
		elif bot_occur == 1 and opp_occur == 0:
			self.utility += 2
		elif opp_occur == 1 and bot_occur == 0:
			self.utility -= 2
		# elif bot_occur == 1 and opp_occur == 1:
		# 	self.utility += 1

	def calc_big_util(self, bot_occur, opp_occur):
		if bot_occur == 3:
			self.utility += 5000000
		elif opp_occur == 3:
			self.utility -= 5000000
		elif bot_occur == 2 and opp_occur == 1:
			self.utility -= 25000
		elif opp_occur == 2 and bot_occur == 1:
			self.utility += 25000
		elif bot_occur == 2 and opp_occur == 0:
			self.utility += 30000
		elif bot_occur == 0 and opp_occur == 2:
			self.utility -= 30000
		elif bot_occur == 1 and opp_occur == 0:
			self.utility += 20
		elif opp_occur == 1 and bot_occur == 0:
			self.utility -= 20

	def get_utility(self):
		self.utility = 0
		
		for vals in self.stack:			#check only for all that has changed
			
			#row small
			bot_occur = 0
			opp_occur = 0
			for i in range(3):
				if self.grids[vals[0]][i][vals[2]][vals[3]][vals[4]] == self.bot_symbol:
					bot_occur += 1
				if self.grids[vals[0]][i][vals[2]][vals[3]][vals[4]] == self.opp_symbol:
					opp_occur += 1
			#assign
			self.calc_small_util(bot_occur, opp_occur)

			#col small
			bot_occur = 0
			opp_occur = 0
			for i in range(3):
				if self.grids[i][vals[1]][vals[2]][vals[3]][vals[4]] == self.bot_symbol:
					bot_occur += 1
				if self.grids[i][vals[1]][vals[2]][vals[3]][vals[4]] == self.opp_symbol:
					opp_occur += 1
			#assign
			self.calc_small_util(bot_occur, opp_occur)

			#diag\ small
			if vals[0] == vals[1]:
				bot_occur = 0
				opp_occur = 0
				for i in range(3):
					if self.grids[i][i][vals[2]][vals[3]][vals[4]] == self.bot_symbol:
						bot_occur += 1
					if self.grids[i][i][vals[2]][vals[3]][vals[4]] == self.opp_symbol:
						opp_occur += 1
				#assign
				self.calc_small_util(bot_occur, opp_occur)				

			#diag/ small
			if vals[0] == 2 - vals[1]:
				bot_occur = 0
				opp_occur = 0
				for i in range(3):
					if self.grids[i][2 - i][vals[2]][vals[3]][vals[4]] == self.bot_symbol:
						bot_occur += 1
					if self.grids[i][2 - i][vals[2]][vals[3]][vals[4]] == self.opp_symbol:
						opp_occur += 1
				#assign
				self.calc_small_util(bot_occur, opp_occur)


			# if vals[5] == 1:			#free hand so choose best possible block
				# need to add some value on the free hand
			#row big
			bot_occur = 0
			opp_occur = 0
			for i in range(3):
				if self.unavailable[vals[2]][i][vals[4]] == self.bot_symbol:
					bot_occur += 1
				if self.unavailable[vals[2]][i][vals[4]] == self.opp_symbol:
					opp_occur += 1
			#assign
			self.calc_big_util(bot_occur, opp_occur)

			#col big
			bot_occur = 0
			opp_occur = 0
			for i in range(3):
				if self.unavailable[i][vals[3]][vals[4]] == self.bot_symbol:
					bot_occur += 1
				if self.unavailable[i][vals[3]][vals[4]] == self.opp_symbol:
					opp_occur += 1
			#assign
			self.calc_big_util(bot_occur, opp_occur)

			#diag\ big
			if vals[2] == vals[3]:
				bot_occur = 0
				opp_occur = 0
				for i in range(3):
					if self.unavailable[i][i][vals[4]] == self.bot_symbol:
						bot_occur += 1
					if self.unavailable[i][i][vals[4]] == self.opp_symbol:
						opp_occur += 1
				#assign
				self.calc_big_util(bot_occur, opp_occur)

			#diag/ big
			if vals[2] == 2 - vals[3]:
				bot_occur = 0
				opp_occur = 0
				for i in range(3):
					if self.unavailable[i][2 - i][vals[4]] == self.bot_symbol:
						bot_occur += 1
					if self.unavailable[i][2 - i][vals[4]] == self.opp_symbol:
						opp_occur += 1
				#assign
				self.calc_big_util(bot_occur, opp_occur)

		return self.utility


	def check_big_win(self, mid_row, mid_col, board, symbol):

		#row
		occur = 0
		for i in range(3):
			if self.unavailable[mid_row][i][board] == symbol:
				occur += 1
		if occur == 3:
			return 1

		#col
		occur = 0
		for i in range(3):
			if self.unavailable[i][mid_col][board] == symbol:
				occur += 1
		if occur == 3:
			return 1		

		#diag\
		if mid_row == mid_col:
			occur = 0
			for i in range(3):
				if self.unavailable[i][i][board] == symbol:
					occur += 1
			if occur == 3:
				return 1

		#diag/
		if mid_row == 2 - mid_col:
			occur = 0
			for i in range(3):
				if self.unavailable[i][2 - i][board] == symbol:
					occur += 1
			if occur == 3:
				return 1

		return 0

	def check_small_win(self, small_row, small_col, mid_row, mid_col, board, symbol, rep):
		#row
		occurences = 0
		for j in range(3):
			if self.grids[small_row][j][mid_row][mid_col][board] == symbol:
				occurences = occurences + 1
		if occurences == 3:
			self.unavailable[mid_row][mid_col][board] = rep
			if self.check_big_win(mid_row, mid_col, board, symbol) == 1:
				return 'V'
			else:
				return rep

		#col
		occurences = 0
		for j in range(3):
			if self.grids[j][small_col][mid_row][mid_col][board] == symbol:
				occurences = occurences + 1
		if occurences == 3:
			self.unavailable[mid_row][mid_col][board] = rep
			if self.check_big_win(mid_row, mid_col, board, symbol) == 1:
				return 'V'
			else:
				return rep

		#diagonal\
		if small_row == small_col:
			occurences = 0
			for j in range(3):
				if self.grids[j][j][mid_row][mid_col][board] == symbol:
					occurences = occurences + 1
			if occurences == 3:
				self.unavailable[mid_row][mid_col][board] = rep
				if self.check_big_win(mid_row, mid_col, board, symbol) == 1:
					return 'V'
				else:
					return rep

		#diagonal/
		if small_row == 2 - small_col:
			occurences = 0
			for j in range(3):
				if self.grids[j][2 - j][mid_row][mid_col][board] == symbol:
					occurences = occurences + 1
			if occurences == 3:
				self.unavailable[mid_row][mid_col][board] = rep
				if self.check_big_win(mid_row, mid_col, board, symbol) == 1:
					return 'V'
				else:
					return rep
		
		#draw
		occurences = 0
		for small_row in range(3):
			for small_col in range(3):
				if self.grids[small_row][small_col][mid_row][mid_col][board] != '-':
					occurences += 1
		if occurences == 9:
			self.unavailable[mid_row][mid_col][board] = 'd'
			return 'd'

		#none
		return 'N'

	def maximize(self, mid_row, mid_col, alpha, beta, d, symbol, first, consecutive):
		if tp.time()-self.start > self.total_time:
			# 'previous layer'
			self.prev = 1
			return self.ret
		else:
			if d == 0 :
				#print self.get_utility(),
				
				return [0, 0, 0, 0, 0, self.get_utility()]			#cutoff			
			else:
				d = d - 1
				

			ret = []
			maximum = float("-inf")
			for board in range(2):
				if (not first) and self.unavailable[mid_row][mid_col][board] == '-' :		#check availability
					for small_row in range(3):
						for small_col in range(3):
							if self.grids[small_row][small_col][mid_row][mid_col][board] != '-' :		#check availability
								continue
							else:

								# print "1tests", small_row, small_col, mid_row, mid_col, board
								self.stack.append([small_row, small_col, mid_row, mid_col, board, 0])
								self.grids[small_row][small_col][mid_row][mid_col][board] = symbol			#testing on this
								sym = self.check_small_win(small_row, small_col, mid_row, mid_col, board, symbol, symbol)
								# print sym, consecutive, "      *******************************************************"
								
								if  sym == symbol and consecutive == 0:
									b, mr, mc, sr, sc, util = self.maximize(small_row, small_col, alpha, beta, d, symbol, False, 1)	
								elif sym == 'V':
									b, mr, mc, sr, sc, util = self.minimize(small_row, small_col, alpha, beta, 0, self.getOppSymbol(symbol), 0)
									# print "-------------------------------------------------------"
									# self.printer()
									# print "VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV"
									# print util
									# print "-------------------------------------------------------"
								else:
									b, mr, mc, sr, sc, util = self.minimize(small_row, small_col, alpha, beta, d, self.getOppSymbol(symbol), 0)
								# 
								# self.printer()
								# self.calc_time()
								# print "util:::::::::::: ", util, alpha, beta
								self.grids[small_row][small_col][mid_row][mid_col][board] = '-'			#restoring
								self.unavailable[mid_row][mid_col][board] = '-'
								self.stack.pop()
								if util > maximum :			#choose the best
									maximum = util
									ret = [board, mid_row, mid_col, small_row, small_col, util]
								if util >= beta:			#check if to be pruned
									# print util, "  ::::::::pruned"
									return [b, mr, mc, sr, sc, util];
								if maximum > alpha:			#update constraints for pruning
									alpha = maximum
				else :
					if (not first) and board == 0:
						continue		#check the other board for availability
					elif (not first) and maximum != float("-inf"):
						continue
					for board in range(2):
						for mid_row in range(3):
							for mid_col in range(3):
								if self.unavailable[mid_row][mid_col][board] != '-' :		#check availability
									continue
								for small_row in range(3):
									for small_col in range(3):
										if self.grids[small_row][small_col][mid_row][mid_col][board] != '-' :		#check availability
											continue
										else:
											# print "2tests", small_row, small_col, mid_row, mid_col, board
											self.stack.append([small_row, small_col, mid_row, mid_col, board, 1])
											self.grids[small_row][small_col][mid_row][mid_col][board] = symbol			#testing on this
											sym = self.check_small_win(small_row, small_col, mid_row, mid_col, board, symbol, symbol)
											# print sym, consecutive, "      *******************************************************"
											
											if  sym == symbol and consecutive == 0:
												b, mr, mc, sr, sc, util = self.maximize(small_row, small_col, alpha, beta, d, symbol, False, 1)
											elif sym == 'V':					
												b, mr, mc, sr, sc, util = self.minimize(small_row, small_col, alpha, beta, 0, self.getOppSymbol(symbol), 0)
												# print "---------------------------------------------------------------"
												# self.printer()
												# print "VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV"
												# print util
												# print "---------------------------------------------------------------"
											else:
												b, mr, mc, sr, sc, util = self.minimize(small_row, small_col, alpha, beta, d, self.getOppSymbol(symbol), 0)
											# 
											# self.printer()
											# print "util:::::::::::: ", util, alpha, beta
											self.grids[small_row][small_col][mid_row][mid_col][board] = '-'			#restoring
											self.unavailable[mid_row][mid_col][board] = '-'
											self.stack.pop()
											if util > maximum :			#choose the best
												maximum = util
												ret = [board, mid_row, mid_col, small_row, small_col, util]
											if util >= beta:			#check if to be pruned
												# print util, "  ::::::::pruned"
												return [b, mr, mc, sr, sc, util];
											if maximum > alpha:			#update constraints for pruning
												alpha = maximum
			# print ret, "0"Winner: P1

			return ret

	def minimize(self, mid_row, mid_col, alpha, beta, d, symbol, consecutive):
		if tp.time() - self.start >self.total_time:
			# print 'previous layer'
			self.prev =1
			return self.ret
		else:
			if d == 0 :
				return [0, 0, 0, 0, 0, self.get_utility()]			#cutoff(except for utility the rest don't matter)
			else:
				d = d - 1
				

			ret = []
			minimum = float("inf")
			for board in range(2):
				if self.unavailable[mid_row][mid_col][board] == '-' :		#check availability
					for small_row in range(3):
						for small_col in range(3):
							if self.grids[small_row][small_col][mid_row][mid_col][board] != '-' :		#check availability
								continue
							else:
								# print "3tests", small_row, small_col, mid_row, mid_col, board
								self.stack.append([small_row, small_col, mid_row, mid_col, board, 0])
								self.grids[small_row][small_col][mid_row][mid_col][board] = symbol			#testing on this
								sym = self.check_small_win(small_row, small_col, mid_row, mid_col, board, symbol, symbol)
								# print sym, consecutive, "      *******************************************************"
								
								if  sym == symbol and consecutive == 0:
									b, mr, mc, sr, sc, util = self.minimize(small_row, small_col, alpha, beta, d, symbol, 1)	
								elif sym == 'V':								
									b, mr, mc, sr, sc, util = self.maximize(small_row, small_col, alpha, beta, 0, self.getOppSymbol(symbol), False, 0)
									# print "------------------------------------------------------------"
									# self.printer()
									# print "VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV"
									# print util
									# print "------------------------------------------------------------"
								else:
									b, mr, mc, sr, sc, util = self.maximize(small_row, small_col, alpha, beta, d, self.getOppSymbol(symbol), False, 0)
									# print util
								# self.printer()
								# print "util:::::::::::: ", util, alpha, beta
								
								self.grids[small_row][small_col][mid_row][mid_col][board] = '-'			#restoring
								self.unavailable[mid_row][mid_col][board] = '-'
								self.stack.pop()
								if util < minimum :			#choose the best
									minimum = util
									ret = [board, mid_row, mid_col, small_row, small_col, util]
								if util <= alpha:			#check if to be pruned
									# print util, "  ::::::::pruned"
									return [b, mr, mc, sr, sc, util];
								if minimum < beta:			#update constraints for pruning
									beta = minimum
				else :
					if board == 0:
						continue		#check the other board for availability
					elif minimum != float("inf"):
						continue
					for board in range(2):
						for mid_row in range(3):		#free hand given to choose mid_level_box
							for mid_col in range(3):
								if self.unavailable[mid_row][mid_col][board] != '-' :		#check availability			
									continue
								for small_row in range(3):
									for small_col in range(3):
										if self.grids[small_row][small_col][mid_row][mid_col][board] != '-' :		#check availability
											continue
										else:
											# print "4tests", small_row, small_col, mid_row, mid_col, board
											self.stack.append([small_row, small_col, mid_row, mid_col, board, 1])
											self.grids[small_row][small_col][mid_row][mid_col][board] = symbol			#testing on this
											sym = self.check_small_win(small_row, small_col, mid_row, mid_col, board, symbol, symbol)
											
											# print sym, consecutive, "      *******************************************************"
											if  sym == symbol and consecutive == 0:
												b, mr, mc, sr, sc, util = self.minimize(small_row, small_col, alpha, beta, d, symbol, 1)	
											elif sym == 'V':							
												b, mr, mc, sr, sc, util = self.maximize(small_row, small_col, alpha, beta, 0, self.getOppSymbol(symbol), False, 0)
												# print "-----------------------------------------------------"
												# self.printer()
												# print "VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV"
												# print util
												# print "-----------------------------------------------------"
											else:
												b, mr, mc, sr, sc, util = self.maximize(small_row, small_col, alpha, beta, d, self.getOppSymbol(symbol), False, 0)
											# self.printer()
											# print "util:::::::::::: ", util, alpha, beta
											
											self.grids[small_row][small_col][mid_row][mid_col][board] = '-'			#restoring
											self.unavailable[mid_row][mid_col][board] = '-'
											self.stack.pop()
											if util < minimum :				#choose the best
												minimum = util
												ret = [board, mid_row, mid_col, small_row, small_col, util]
											if util <= alpha:				#check if to be pruned
												# print util, "  ::::::::pruned"
												return [b, mr, mc, sr, sc, util];
											if minimum < beta:				#update constraints for pruning
												beta = minimum
										# print ret
			return ret




	def printer(self):
		print ("\n\n"),
		for mid_board_row in range(3):
			for small_board_row in range(3):
				for big_board in range(2):
					for mid_board_col in range(3):
						for small_board_col in range(3):
							print (self.grids[small_board_row][small_board_col][mid_board_row][mid_board_col][big_board]),
						print (" "),
					print ("     "),
				print ("\n"),
			print ("\n\n"),

		for k in range(2):
			for j in range(3):
				for i in range(3):
					print self.unavailable[j][i][k],
					print " ",
				print "\n",
			print "\n\n",

		# print self.stack


	# def set(self, board, row, col, symbol):
	# 	mid_row = row/3;
	# 	small_row = row%3;
	# 	mid_col = col/3;
	# 	small_col = col%3;
	# 	if self.unavailable[mid_row][mid_col][board] != 0 or self.grids[small_row][small_col][mid_row][mid_col][board] != '-' :			#check if already occupied
	# 		print "Invalid Move2"
	# 		return [-1, -1]
	# 	self.grids[small_row][small_col][mid_row][mid_col][board] = symbol;
	# 	self.check_small_win(small_row, small_col, mid_row, mid_col, board, symbol, symbol)						#1 represents won by X, 2 represents won by O, -1 represents draw(for small wins)
	# 	return [small_row, small_col]

	def move(self, board, old_move, flag):
		self.start=tp.time()
		occupied = 0
		for k in range(2):
			for j in range(9):
				for i in range(9):
					self.grids[i%3][j%3][i/3][j/3][k] = board.big_boards_status[k][i][j]
					if self.grids[i%3][j%3][i/3][j/3][k] != '-':
						occupied += 1
		for k in range(2):
			for j in range(3):
				for i in range(3):
					self.unavailable[i][j][k] = board.small_boards_status[k][i][j]
		self.bot_symbol = flag
		self.opp_symbol = self.getOppSymbol(flag)
		mid_row = old_move[1]%3
		mid_col = old_move[2]%3
		mid = tp.time()
		c=0
		new =0
		end_new=tp.time() + 3
		self.ret =[]
		self.prev = 0
		while 1:
			new = tp.time()
			if occupied == 0:
				movein_board, mid_row, mid_col, small_row, small_col, util = self.maximize(mid_row, mid_col, float("-inf"), float("inf"), self.depth+c, self.bot_symbol, True, self.repitition);	
				
			else:
				movein_board, mid_row, mid_col, small_row, small_col, util = self.maximize(mid_row, mid_col, float("-inf"), float("inf"), self.depth+c, self.bot_symbol, False, self.repitition);
			
			# print([movein_board, mid_row, mid_col, small_row, small_col, util],self.ret,self.prev)
			if self.prev:
				movein_board, mid_row, mid_col, small_row, small_col, util = self.ret
			else:
				self.ret= [movein_board, mid_row, mid_col, small_row, small_col, util]
			# if i choose self.time then it plays well else really stupid
			# print([movein_board, mid_row, mid_col, small_row, small_col, util],self.ret,self.prev)
			if tp.time()-self.start >self.total_time:
			 	break
			print(util,tp.time()-new,self.depth+c)
			c += 1
			
			# self.ret =[]
			#self.calc_time()
			
			
			
		# self.util = util
		self.grids[small_row][small_col][mid_row][mid_col][movein_board] = self.bot_symbol
		sym = self.check_small_win(small_row, small_col, mid_row, mid_col, movein_board, self.bot_symbol, self.bot_symbol)				#move in our copy	
		# print sym, "   ++++++++++++++++++++++++++++++++++++++++++++++++++++="
		if self.repitition == 0 and (sym == self.bot_symbol or sym == 'V'):
			self.repitition = 1
			# print "change"
		else:
			self.repitition = 0
			# print "no change"
		print movein_board, mid_row, mid_col, small_row, small_col, "   :::::::  ", util
		self.move_no +=1
		# if self.move_no %self.depth_no ==0 and self.depth <5:
		# 	self.depth +=1
		print self.depth+c,self.move_no
		# self.set(board, mid_row*3 + small_row, mid_col*3 + small_col, self.bot_symbol)
		# print old_move
		# print movein_board, mid_row*3 + small_row, mid_col*3 + small_col
		self.calc_time()
		return (movein_board, mid_row*3 + small_row, mid_col*3 + small_col)


# game = Team()


# while 1:	

# 	#player
# 	board, row, col = [int(i) for i in input("Enter board, row, col: ").split()]
# 	if game.turn != 1 and (row/3 != game.next_row or col/3 != game.next_col) and (game.unavailable[game.next_row][game.next_col][0] == 0 or game.unavailable[game.next_row][game.next_col][1] == 0) :			#check if according to rules
# 		print "Invalid move1"
# 		continue
# 	mid_row, mid_col = game.set(board, row, col, game.opp_symbol)	
# 	if mid_row == -1:
# 		continue
# 	game.printer()

# 	print "=============================================================================="

# 	#bot
# 	game.next_row, game.next_col = game.move(mid_row, mid_col)
# 	if game.next_row == -1:
# 		exit
# 	game.printer()

# 	if game.turn == 1:
# 			game.turn = game.turn + 1

