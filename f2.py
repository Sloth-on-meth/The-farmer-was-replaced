def move_to(x, y):
	while get_pos_x() < x:
		move(East)
	while get_pos_x() > x:
		move(West)
	while get_pos_y() < y:
		move(North)
	while get_pos_y() > y:
		move(South)

def water_tile():
	if get_water() < 0.6:
		if num_items(Items.Water) > 0:
			use_item(Items.Water)

def check_pumpkin_tile_here():
	entity = get_entity_type()
	if entity == Entities.Pumpkin:
		return not can_harvest()
	harvest()
	if get_ground_type() == Grounds.Grassland:
		till()
	plant(Entities.Pumpkin)
	return True

def farm_pass(start_x, end_x):
	pumpkin_active = num_items(Items.Carrot) >= 50

	while get_pos_x() < start_x:
		move(East)
	while get_pos_x() > start_x:
		move(West)
	while get_pos_y() < size - 1:
		move(North)

	width = end_x - start_x + 1

	if not pumpkin_active:
		for row in range(size):
			if row % 2 == 0:
				forward = East
			else:
				forward = West

			for col in range(width):
				water_tile()
				if can_harvest():
					harvest()
				if get_ground_type() == Grounds.Grassland:
					till()
				if get_entity_type() == None:
					plant(Entities.Carrot)
				if col < width - 1:
					move(forward)

			if row < size - 1:
				move(South)

		return pumpkin_active

	watch = []
	for row in range(size):
		if row % 2 == 0:
			forward = East
		else:
			forward = West

		for col in range(width):
			water_tile()
			if check_pumpkin_tile_here():
				watch.append((get_pos_x(), get_pos_y()))
			if col < width - 1:
				move(forward)

		if row < size - 1:
			move(South)

	while len(watch) > 0:
		next_watch = []
		while len(watch) > 0:
			x, y = watch.pop()
			move_to(x, y)
			water_tile()
			if check_pumpkin_tile_here():
				next_watch.append((x, y))
		watch = next_watch

	return pumpkin_active

while True:
	size = get_world_size()
	count = max_drones()
	if count < 1:
		count = 1
	if count > size:
		count = size

	chunk_size = size // count
	ranges = []
	start = 0
	for i in range(count):
		end = start + chunk_size - 1
		if i == count - 1:
			end = size - 1
		ranges.append((start, end))
		start = end + 1

	helpers = []
	for i in range(1, count):
		rs, re = ranges[i]
		helper = spawn_drone(farm_pass, rs, re)
		helpers.append(helper)

	primary_start, primary_end = ranges[0]
	pumpkin_active = farm_pass(primary_start, primary_end)

	for i in range(len(helpers)):
		h = helpers[i]
		if h != None:
			wait_for(h)

	if pumpkin_active:
		harvest()
