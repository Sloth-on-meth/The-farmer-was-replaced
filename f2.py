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

def check_pumpkin_tile():
	global pumpkin_ready
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
			pumpkin_ready = False
			if not in_list(watch, x, y):
				watch.append((x, y))
	else:
		harvest()
		if get_ground_type() == Grounds.Grassland:
			till()
		plant(Entities.Pumpkin)
		pumpkin_ready = False
		if not in_list(watch, x, y):
			watch.append((x, y))

good = []
watch = []

while True:
	size = get_world_size()

	while get_pos_x() > 0:
		move(West)
	while get_pos_y() < size - 1:
		move(North)

	pumpkin_active = num_items(Items.Carrot) >= 50
	pumpkin_ready = True

	for row in range(size):
		if row % 2 == 0:
			forward = East
			backward = West
		else:
			forward = West
			backward = East

		streak = 0

		for col in range(size):
			

			if pumpkin_active:
				check_pumpkin_tile()
			else:
				
				if can_harvest():
					harvest()
					water_tile()
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
					check_pumpkin_tile()
				for i in range(lookback):
					move(forward)

				return_x = get_pos_x()
				return_y = get_pos_y()
				watch_copy = list(watch)
				for i in range(len(watch_copy)):
					wx, wy = watch_copy[i]
					move_to(wx, wy)
					water_tile()
					check_pumpkin_tile()
				move_to(return_x, return_y)

				streak = 0

			if col < size - 1:
				move(forward)

		if row < size - 1:
			move(South)

	if pumpkin_active and pumpkin_ready:
		harvest()
		good = []
		watch = []
