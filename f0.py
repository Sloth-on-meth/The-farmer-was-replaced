size = get_world_size()
split = size // 2
still_growing = True

def sweep(action):
	for row in range(size):
		for col in range(size):
			action(row, col)
			if col < size - 1:
				if row % 2 == 0:
					move(East)
				else:
					move(West)
		if row < size - 1:
			move(South)

def water_and_fertilize():
	if get_water() < 0.2:
		if num_items(Items.Water) > 0:
			use_item(Items.Water)
	if get_entity_type() != None and not can_harvest() and num_items(Items.Fertilizer) > 0:
		use_item(Items.Fertilizer)

def grow(entity):
	if can_harvest():
		harvest()
	if get_ground_type() == Grounds.Grassland:
		till()
	if get_entity_type() == None:
		plant(entity)

def pumpkin_tile(row, col):
	global still_growing
	if col < split:
		return
	entity = get_entity_type()
	if entity == Entities.Dead_Pumpkin or entity == None:
		if get_ground_type() == Grounds.Grassland:
			till()
		plant(Entities.Pumpkin)
		still_growing = True
	elif not can_harvest():
		still_growing = True

def harvest_pumpkins(row, col):
	if col < split:
		return
	if get_entity_type() == Entities.Dead_Pumpkin:
		harvest()
	elif can_harvest():
		harvest()

def farm_tile(row, col):
	water_and_fertilize()
	if col >= split:
		pumpkin_tile(row, col)
	elif row % 2 == 0 and col % 2 == 0:
		grow(Entities.Tree)
	elif row % 2 == 1 and col % 2 == 1:
		grow(Entities.Carrot)
	elif row % 2 == 0:
		grow(Entities.Bush)
	else:
		if can_harvest():
			harvest()

while True:
	confirmed = 0
	attempts = 0
	while confirmed < 2 and attempts < 8:
		still_growing = False
		sweep(farm_tile)
		attempts += 1
		if still_growing:
			confirmed = 0
		else:
			confirmed += 1

	sweep(harvest_pumpkins)
