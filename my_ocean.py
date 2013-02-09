from random import choice
from random import randint
from array import array

def near(place):
	x = place[0]
	y = place[1]
	moves = set()
	array_x = array('l', [1,1,1,0,0,-1,-1,-1])
	array_y = array('l', [1,0,-1,1,-1,-1,0,1])
	for i in xrange(8):
		moves.add((x + array_x[i], y + array_y[i]))
	return moves
		

class Prey(object):
	def __init__(self, current_time):
		self.reproduction_interval = 100
		self_old = 200
		self.last_reproduction = current_time - randint(0, self.reproduction_interval)
	def reproducable(self, current_time):
		return current_time - self.last_reproduction > self.reproduction_interval	
	def too_old(self, current_time):
		return current_time - self.last_reproduction > self.old		

class Predator(object):
	def __init__(self, current_time):
		self.reproduction_interval = 150
		self.last_reproduction = current_time - randint(0, self.reproduction_interval)
		self.becomes_hungry = 10
		self.starves_to_death = 50
		self.last_feeding = current_time - randint(0, self.becomes_hungry)
	def reproducable(self, current_time):
		return current_time > self.last_reproduction + self.reproduction_interval	
	def hungry(self, current_time):
		return current_time > self.last_feeding + self.becomes_hungry 
	def starved(self, current_time):
		return current_time > self.last_feeding + self.starves_to_death 
	
class Obstacle(object):
	def __init__(place):
		self.place = set()
		self.place.add(place)
	
class Ocean(object):

	def find_places_to_move(self, place):
		places_to_move = set()
		positions_near = near(place)
		for i in positions_near:
			if i not in self.obstacles and i not in self.prey and i not in self.predators:	
				if i[0] >= 0 and i[0] < self.size and i[1] >= 0 and i[1] < self.size:
					places_to_move.add(i)
		return places_to_move
	
	def __init__(self, size, prey_number, predators_number, obstacles_number):
		self.time = 0
		self.size = size
		self.predators = {}
		self.prey = {}
		self.obstacles = {}
		available_place = set()
		for i in xrange(self.size):
			for j in xrange(self.size):
				available_place.add((i, j))
		for predator_index in xrange(predators_number):
			position = choice(list(available_place))
			available_place.discard(position)
			self.predators[position] = Predator(self.time)
		for prey_index in xrange( prey_number,):
			position = choice(list(available_place))
			available_place.discard(position)
			self.prey[position] = Prey(self.time)
		for obstacle_index in xrange(obstacles_number):
			position = choice(list(available_place))
			available_place.discard(position)
			self.obstacles.add(position)
		
	def life_tact(self):
		self.time += 1
		temp_prey = dict(self.prey)
		temp_predators = dict(self.predators)
		for place, prey in self.prey.iteritems():
			places_to_move = self.find_places_to_move(place)
			if places_to_move:
				next_move = choice(list(places_to_move))
				if prey.reproducable(self.time):
					temp_prey[next_move] = Prey(self.time)
		self.prey = temp_prey			
		for place, predator in self.predators.iteritems():
			places_to_move = near(place)
			prey_to_eat = [prey for prey in places_to_move if prey in self.prey]
			if predator.starved(self.time):
				del temp_predators[place]
			elif predator.hungry(self.time) and prey_to_eat:
				fall_prey = choice(list(prey_to_eat))
				del self.prey[fall_prey]
				predator.last_feeding = self.time
				temp_predators[fall_prey] = predator
				del temp_predators[place]
			else:
				free_places = self.find_places_to_move(place)
				if free_places:
					next_place = choice(list(free_places))
					if predator.reproducable(self.time):
						temp_predators[next_place] = Predator(self.time)
					else:
						del temp_predators[place]
						temp_predators[next_place] = predator
		self.predators = temp_predators				
			
		
ocean = Ocean(100, 30, 20, 0) 
for i in xrange(100):
	ocean.life_tact() 
	print len(ocean.prey), len(ocean.predators)