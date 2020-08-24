from background import *
from essentials import * 
import copy
import math
import time 

screen_size = Vector2(800,600)
game = Instance("Raycast",screen_size.ToTuple(),(50,70,90))
screen_boundaries = [Vector2(0,0),Vector2(800,0),Vector2(800,0),Vector2(800,600),Vector2(800,600),Vector2(0,600),Vector2(0,600),Vector2(0,0)]

light_mesh = GameObject([Polygon([],(150,150,150))],game)
circle = GameObject([Circle(20,(150,100,50),Vector2(0,0))],game)
cube_size = 50
grid_size = (screen_size.x//cube_size,screen_size.y//cube_size)
cube_grid = [[None]*grid_size[1] for _ in range(grid_size[0])]
cube_surface = Surface((0,0,0),Vector2(cube_size,cube_size),Vector2(0,0))
cubes = GameObject([],game)

class EdgeSide(Enum):
	Up = 0
	Right = 1
	Down = 2
	Left = 3

class Edge:
	def __init__(self,start,end):
		self.start = start
		self.end = end

edge_pool = []
points_test = []

class Block:
	def __init__(self,position):
		points = []
		points.append(position - Vector2(cube_size,cube_size)/2) #Up Left
		points.append(position - Vector2(-cube_size,cube_size)/2) # Up Right
		points.append(position - Vector2(-cube_size,-cube_size)/2) #Down Right
		points.append(position - Vector2(cube_size,-cube_size)/2) #Down Left
		self.verts = points
		self.edges = [-1,-1,-1,-1]

def UpdateEdges():

	global edge_pool
	edge_pool = []

	for y in range(grid_size[1]):
		for x in range(grid_size[0]):

			cube = cube_grid[x][y]
			if cube == None:
				continue

			cube.edges = [-1,-1,-1,-1]	

			#boundaries
			down_b = y < grid_size[1]-1
			right_b = x < grid_size[0]-1
			up_b = y > 0 
			left_b = x > 0

			#neighbors info
			if up_b:
				up = cube_grid[x][y-1]
			if right_b:
				right = cube_grid[x+1][y] 
			if down_b:
				down = cube_grid[x][y+1] 
			if left_b:
				left = cube_grid[x-1][y] 
	
			
			if up_b and up == None:
				if left_b and left != None and left.edges[EdgeSide.Up.value] > -1:
					edge_pool[left.edges[EdgeSide.Up.value]].end = cube.verts[1]
					cube.edges[EdgeSide.Up.value] = left.edges[EdgeSide.Up.value]
				else:
					cube.edges[EdgeSide.Up.value] = len(edge_pool)
					edge_pool.append(Edge(cube.verts[0],cube.verts[1]))
			
			if right_b and right == None:
				if up_b and up != None and up.edges[EdgeSide.Right.value] > -1:
					edge_pool[up.edges[EdgeSide.Right.value]].end = cube.verts[2]
					cube.edges[EdgeSide.Right.value] = up.edges[EdgeSide.Right.value]
				else:
					cube.edges[EdgeSide.Right.value] = len(edge_pool)
					edge_pool.append(Edge(cube.verts[1],cube.verts[2]))	
			
			if down_b and down == None:
				if left_b and left != None and left.edges[EdgeSide.Down.value] > -1:
					print(len(edge_pool))
					print(edge_pool[left.edges[EdgeSide.Down.value]])
					edge_pool[left.edges[EdgeSide.Down.value]].end = cube.verts[2]
					cube.edges[EdgeSide.Down.value] = left.edges[EdgeSide.Down.value]
				else:
					cube.edges[EdgeSide.Down.value] = len(edge_pool)
					edge_pool.append(Edge(cube.verts[3],cube.verts[2]))
			
			if left_b and left == None:
				if up_b and up != None and up.edges[EdgeSide.Left.value] > -1:
					edge_pool[up.edges[EdgeSide.Left.value]].end = cube.verts[3]
					cube.edges[EdgeSide.Left.value] = up.edges[EdgeSide.Left.value]
				else:
					cube.edges[EdgeSide.Left.value] = len(edge_pool)
					edge_pool.append(Edge(cube.verts[0],cube.verts[3]))
			
points_test += screen_boundaries 
def Update(self):

	global parameter
	global vec
	global points_test

	direction = Vector2(self.keys[K_RIGHT] - self.keys[K_LEFT],self.keys[K_DOWN] - self.keys[K_UP])

	mouse_pos = pygame.mouse.get_pos()
	mouse_pos_vec = Vector2(mouse_pos[0],mouse_pos[1])
	mouse_state = pygame.mouse.get_pressed()
	mouse_grid_index = (mouse_pos_vec//cube_size)
	circle.transform.position += direction*200*self.delta_time
	polygon = []

	
	if mouse_state[0] == 1 and cube_grid[mouse_grid_index.x][mouse_grid_index.y] == None:
		new_cube = copy.copy(cube_surface)
		new_cube.position = (mouse_grid_index+Vector2(1,1))*cube_size - Vector2(cube_size,cube_size)/2
		cube_grid[mouse_grid_index.x][mouse_grid_index.y] = Block(new_cube.position)
		cubes.draw_functions.append(new_cube)
		UpdateEdges()
		points_test = sum([[edge.end,edge.start] for edge in edge_pool],[]) + screen_boundaries 

	angle_pool = []
	
	for point in points_test:

		diff = point - circle.transform.position
		angle = math.degrees(math.atan2(diff.y,diff.x))
		desvio1 = Vector2(math.cos(math.radians(angle+1/1000)),math.sin(math.radians(angle+1/1000)))
		desvio2 = Vector2(math.cos(math.radians(angle-1/1000)),math.sin(math.radians(angle-1/1000)))

		if len([x for x in angle_pool if abs(angle-x) < 0.01]) > 0:
			continue
		else:
			angle_pool.append(angle)
		
		rays = [(Raycast(circle.transform.position,desvio1,1000,points_test),angle+1/1000),
				(Raycast(circle.transform.position,diff,1000,points_test),angle),
				(Raycast(circle.transform.position,desvio2,1000,points_test),angle-1/1000)]

		polygon += [ray for ray in rays if type(ray[0]) != type(None)]
		
		#pygame.draw.circle(self.screen,(255,255,255),(int(point.x),int(point.y)),5)

	#print(len(polygon),len(points_test*3))
	center = circle.transform.position
	polygon.sort(key=lambda x: x[1])
	light_mesh.draw_functions[0].points = [x[0] for x in polygon ]

	
#Start game
game.Start(game.game_objects,Update)
