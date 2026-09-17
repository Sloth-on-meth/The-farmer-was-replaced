quick_print("Starting mixed crop farm program f1")

def move_to(x, y):
	while get_pos_x() < x:
		move(East)
	while get_pos_x() > x:
		move(West)
	while get_pos_y() < y:
		move(North)
	while get_pos_y() > y:
		move(South)

def in_list(coords, x, y):
	for i in range(len(coords)):
		cx, cy = coords[i]
		if cx == x and cy == y:
			return True
	return False

def water_tile():
	if get_water() < 0.2:
		if num_items(Items.Water) > 0:
			use_item(Items.Water)
	if get_entity_type() != None and not can_harvest() and num_items(Items.Fertilizer) > 0:
		use_item(Items.Fertilizer)

def has_companion_request(x, y):
	for i in range(len(companion_requests)):
		rx, ry, re = companion_requests[i]
		if rx == x and ry == y:
			return True
	return False

def record_companion():
	if len(companion_requests) >= 50:
		return
	info = get_companion()
	if info == None:
		return
	comp_entity, comp_pos = info
	cx, cy = comp_pos
	if cx < 0 or cx >= size or cy < 0 or cy >= size:
		return
	if not has_companion_request(cx, cy):
		companion_requests.append((cx, cy, comp_entity))

def take_companion_request(x, y):
	for i in range(len(companion_requests)):
		rx, ry, re = companion_requests[i]
		if rx == x and ry == y:
			companion_requests.pop(i)
			return re
	return None

def grow(entity):
	if can_harvest():
		harvest()
	if get_ground_type() == Grounds.Grassland:
		till()
	if get_entity_type() == None:
		plant(entity)
	if get_entity_type() != None:
		record_companion()

def cactus_tile():
	x = get_pos_x()
	y = get_pos_y()

	if get_entity_type() != Entities.Cactus:
		if get_ground_type() == Grounds.Grassland:
			till()
		plant(Entities.Cactus)
		return

	record_companion()

	if not can_harvest():
		return

	value = measure()
	if value == None:
		return

	if x > 0:
		other = measure(West)
		if other != None and value < other:
			swap(West)
			return
	if y > 0:
		other = measure(South)
		if other != None and value < other:
			swap(South)
			return
	if x < size - 1:
		other = measure(East)
		if other != None and value > other:
			swap(East)
			return
	if y < size - 1:
		other = measure(North)
		if other != None and value > other:
			swap(North)
			return

	harvest()

def check_pumpkin_tile(good, watch):
	x = get_pos_x()
	y = get_pos_y()
	if in_list(good, x, y):
		return

	entity = get_entity_type()
	if entity == Entities.Pumpkin:
		if can_harvest():
			good.append((x, y))
			if in_list(watch, x, y):
				watch.remove((x, y))
		else:
			if not in_list(watch, x, y):
				watch.append((x, y))
	else:
		harvest()
		if get_ground_type() == Grounds.Grassland:
			till()
		plant(Entities.Pumpkin)
		if not in_list(watch, x, y):
			watch.append((x, y))

def dispatch_tile(good, watch):
	x = get_pos_x()
	y = get_pos_y()

	if x < 4:
		cactus_tile()
	elif x >= size - 4:
		check_pumpkin_tile(good, watch)
	elif x % 2 == 0 and y % 2 == 0:
		grow(Entities.Tree)
	elif x % 2 == 1 and y % 2 == 1:
		grow(Entities.Carrot)
	elif x % 2 == 0:
		grow(Entities.Bush)
	else:
		requested = take_companion_request(x, y)
		if requested != None:
			grow(requested)
		else:
			if can_harvest():
				harvest()
			if get_ground_type() == Grounds.Soil:
				till()

def farm_pass(start_x, end_x, good, watch):
	while get_pos_x() < start_x:
		move(East)
	while get_pos_x() > start_x:
		move(West)
	while get_pos_y() < size - 1:
		move(North)

	width = end_x - start_x + 1

	for row in range(size):
		if row % 2 == 0:
			forward = East
			backward = West
		else:
			forward = West
			backward = East

		streak = 0

		for col in range(width):
			water_tile()
			dispatch_tile(good, watch)
			streak += 1

			if streak == 10:
				lookback = min(10, col)
				for i in range(lookback):
					move(backward)
					water_tile()
					dispatch_tile(good, watch)
				for i in range(lookback):
					move(forward)

				return_x = get_pos_x()
				return_y = get_pos_y()
				watch_copy = list(watch)
				for i in range(len(watch_copy)):
					wx, wy = watch_copy[i]
					move_to(wx, wy)
					water_tile()
					check_pumpkin_tile(good, watch)
				move_to(return_x, return_y)

				streak = 0

			if col < width - 1:
				move(forward)

		if row < size - 1:
			move(South)

	harvested = False
	if end_x >= size - 4 and len(watch) == 0 and len(good) > 0:
		move_to(end_x, get_pos_y())
		harvest()
		good = []
		watch = []
		harvested = True

	return good, watch, harvested

companion_requests = []
pumpkin_good = []
pumpkin_watch = []

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
		if i == count - 1:
			helper = spawn_drone(farm_pass, rs, re, pumpkin_good, pumpkin_watch)
		else:
			helper = spawn_drone(farm_pass, rs, re, [], [])
		helpers.append(helper)

	primary_start, primary_end = ranges[0]
	if count == 1:
		primary_good, primary_watch, harvested = farm_pass(primary_start, primary_end, pumpkin_good, pumpkin_watch)
	else:
		primary_good, primary_watch, harvested = farm_pass(primary_start, primary_end, [], [])

	for i in range(len(helpers)):
		h = helpers[i]
		if h != None:
			h_good, h_watch, h_harvested = wait_for(h)
			if i == len(helpers) - 1:
				pumpkin_good = h_good
				pumpkin_watch = h_watch
			if h_harvested:
				harvested = True

	if count == 1:
		pumpkin_good = primary_good
		pumpkin_watch = primary_watch

	if harvested:
		pumpkin_good = []
		pumpkin_watch = []
