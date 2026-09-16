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
	if get_water() < 0.6:
		if num_items(Items.Water) > 0:
			use_item(Items.Water)

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

def farm_pass(start_x, end_x, good, watch):
	pumpkin_active = num_items(Items.Carrot) >= 50

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

			if pumpkin_active:
				check_pumpkin_tile(good, watch)
			else:
				if can_harvest():
					harvest()
				if get_ground_type() == Grounds.Grassland:
					till()
				if get_entity_type() == None:
					plant(Entities.Carrot)

			streak += 1

			if streak == 10 and pumpkin_active:
				lookback = min(10, col)
				for i in range(lookback):
					move(backward)
					water_tile()
					check_pumpkin_tile(good, watch)
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

	return good, watch, pumpkin_active

chunk_goods = []
chunk_watches = []

while True:
	size = get_world_size()
	count = max_drones()
	if count < 1:
		count = 1
	if count > size:
		count = size

	if len(chunk_goods) != count:
		chunk_goods = []
		chunk_watches = []
		for i in range(count):
			chunk_goods.append([])
			chunk_watches.append([])

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
		helper = spawn_drone(farm_pass, rs, re, chunk_goods[i], chunk_watches[i])
		helpers.append(helper)

	primary_start, primary_end = ranges[0]
	primary_good, primary_watch, pumpkin_active = farm_pass(primary_start, primary_end, chunk_goods[0], chunk_watches[0])
	chunk_goods[0] = primary_good
	chunk_watches[0] = primary_watch

	all_ready = pumpkin_active
	if len(primary_watch) > 0:
		all_ready = False
	any_grown = len(primary_good) > 0

	for i in range(len(helpers)):
		h = helpers[i]
		idx = i + 1
		if h != None:
			h_good, h_watch, h_pumpkin_active = wait_for(h)
			chunk_goods[idx] = h_good
			chunk_watches[idx] = h_watch
			if not h_pumpkin_active:
				all_ready = False
			if len(h_watch) > 0:
				all_ready = False
			if len(h_good) > 0:
				any_grown = True

	if all_ready and any_grown:
		harvest()
		for i in range(count):
			chunk_goods[i] = []
			chunk_watches[i] = []
