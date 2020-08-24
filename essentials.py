import numpy as np
from enum import Enum
import pygame
import math
import random
import copy
import concurrent.futures

class Vector2:
	
	def __init__(self,x,y):
		self.x = x
		self.y = y

	def dot(self,other):
		return (self.x * other.x) + (self.y * other.y)
	def magnitude(self):
		return math.sqrt(self.x * self.x + self.y * self.y)
	def Normalize(self):
		self.x = self.x/self.magnitude()
		self.y = self.y/self.magnitude()
	def normalized(self):
		if self.magnitude() > 1:
			return Vector2(self.x/self.magnitude(),self.y/self.magnitude())
		else:
			return self
	def cross (v1,v2):
		return (v1.x*v2.y) - (v1.y*v2.x)
	def perpendicular(self):
		t = np.array([[0,-1],[1,0]])
		vec = np.array([self.x,self.y])
		p = t.dot(vec)
		return Vector2(p[0],p[1])
	def __neg__(self):
		return Vector2(-self.x,-self.y)
	def __getitem__(self, item):
		if item == 0:
			return self.x
		else:
			return self.y

	def __setitem__(self, item, v):
		if item == 0:
			self.x = v
		else:
			self.y = v
	def __add__(self, other):
		return Vector2(self.x+other.x,self.y+other.y)
	def __sub__(self, other):
		return Vector2(self.x-other.x,self.y-other.y)
	def __truediv__(self, n):
		return Vector2(self.x/n,self.y/n)
	def __floordiv__(self, n):
		return Vector2(self.x//n,self.y//n)
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y
	def __mul__(self, n):
		return Vector2(self.x*n,self.y*n)

	def TupleToVector(tuple):
		return Vector2(tuple[0],tuple[1])
	def Sum(other):
		sum_vec = Vector2(0,0)
		for v in other:
			sum_vec += v
		return sum_vec

	def ToTuple(self):
		return (self.x,self.y)

class Tags(Enum):
	Default = 0
	Ground = 1
	Player = 2

class Surface:

	def __init__(self,color,rect,position):

		self.color = color
		self.rect = rect
		self.position = position

	def Draw (self,game_screen,gameObject):
		pygame.draw.rect(game_screen,self.color,((gameObject.transform.position+self.position - (self.rect/2 * gameObject.transform.size)).ToTuple(),(self.rect * gameObject.transform.size).ToTuple()))

class Line:
	
	def __init__(self,color,start,end,thickness):

		self.color = color
		self.start = start
		self.end = end
		self.thickness = thickness

	def Draw (self,game_screen,gameObject):
		pygame.draw.line(game_screen, self.color,(gameObject.transform.position+(self.start*gameObject.transform.size)).ToTuple(), (gameObject.transform.position+(self.end*gameObject.transform.size)).ToTuple(),self.thickness)

def Raycast(origin,diretion,lenght,line_points):

	endpoint = origin + (diretion.normalized()*lenght)
	clossest_point = None
	clossest_point_mag = 9999

	for i in range(0,len(line_points),2):
		try:
			t = Vector2.cross(line_points[i]-origin,line_points[i]-line_points[i+1])/Vector2.cross((endpoint-origin),line_points[i]-line_points[i+1])
			u = Vector2.cross(line_points[i]-origin,(endpoint-origin))/Vector2.cross((endpoint-origin),line_points[i+1]-line_points[i])
			if t <= 1 and t >= 0 and u >= 0 and u <= 1:
				point = origin + ((endpoint-origin)*t) # origin + ((endpoint-origin)*t) - origin
				point_mag = (point-origin).magnitude()
				if point_mag < clossest_point_mag:					
					clossest_point = point
					clossest_point_mag = point_mag
		except: 
			continue

	if type(clossest_point) != type(None):
		return clossest_point

class Polygon:

	def __init__(self,points,color):

		self.points = points
		self.color = color

	def Draw (self,game_screen,gameObject):

		if len(self.points) > 2:
			pygame.draw.polygon(game_screen,self.color,[(gameObject.transform.position+(point*gameObject.transform.size)).ToTuple() for point in self.points])

class Circle ():

	def __init__(self,radius,color,local_position):

		self.radius = radius
		self.color = color
		self.local_position = local_position

	def Draw (self,game_screen,gameObject):
		pygame.draw.circle(game_screen,self.color,(int(((gameObject.transform.position + self.local_position)*gameObject.transform.size).x),int(((gameObject.transform.position + self.local_position)*gameObject.transform.size).y)),self.radius)

class Transform:

	def __init__ (self,position,size):

		self.position = position
		self.size = 1
		self.angle = 0
		self.axis = Vector2(0,0)

	def Translate(self,vector):
		self.position = self.position + vector	

class GameObject:

	def __init__(self,draw_functions,game_instance):
		self.transform = Transform(Vector2(0,0),Vector2(1,1))
		self.tag = Tags.Default
		self.draw_functions = draw_functions
		game_instance.game_objects.append(self)

	def CopyObject (game_instance,obj):

		newObject = copy.deepcopy(obj)
		game_instance.game_objects.append(newObject)
		return newObject