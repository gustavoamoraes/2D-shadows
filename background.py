from essentials import *
import pygame, sys
from pygame.locals import *
import types

class Instance:

	#Start
	def __init__ (self,name,resolution,background_color):

		#Start
		pygame.init()

		self.screen = pygame.display.set_mode(resolution)

		#Title
		pygame.display.set_caption(name)

		#Game clock
		self.game_clock = pygame.time.Clock()

		#Time per frame
		self.delta_time = 0

		#Initializing array
		self.game_objects = []

		self.background_color = background_color


	#Start game
	def Start(self,game_objects,update_method):

		self.game_objects = game_objects
		self.Update = types.MethodType(update_method,self)
		self.Loop()

	#Background stuff
	def Loop(self):

		while True:

			#Frame rate
			self.game_clock.tick(0)

			#Background color
			self.screen.fill(self.background_color)

			#Game inputs
			self.keys = pygame.key.get_pressed()

			if self.game_clock.get_fps() > 0:
				self.delta_time = 1/self.game_clock.get_fps()
			#print(self.game_clock.get_fps())

			self.Update()

			for obj in self.game_objects:
				for draw_func in obj.draw_functions:
						draw_func.Draw(self.screen,obj)

			pygame.display.update()

			for event in pygame.event.get():
				if event.type == QUIT:
					sys.exit(0)
