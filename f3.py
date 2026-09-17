def move_to(x, y):
	while get_pos_x() < x:
		move(East)
	while get_pos_x() > x:
		move(West)
	while get_pos_y() < y:
		move(North)
	while get_pos_y() > y:
		move(South)

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

def water_tile():
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
	if get_entity_type() != None:
		record_companion()

def check_cactus_tile_here():
	if get_entity_type() != Entities.Cactus:
		if get_entity_type() != None:
			harvest()
		if get_ground_type() == Grounds.Grassland:
			till()
		plant(Entities.Cactus)
		return True

	record_companion()

	if not can_harvest():
		return True

	x = get_pos_x()
	y = get_pos_y()
	value = measure()
	if value == None:
		return True

	if x > 0:
		other = measure(West)
		if other != None and value < other:
			swap(West)
			return True
	if y > 0:
		other = measure(South)
		if other != None and value < other:
			swap(South)
			return True
	if x < size - 1:
		other = measure(East)
		if other != None and value > other:
			swap(East)
			return True
	if y < size - 1:
		other = measure(North)
		if other != None and value > other:
			swap(North)
			return True

	return False

def cactus_band(y_start, y_end):
	x_start = 0
	x_end = 3

	while get_pos_x() < x_start:
		move(East)
	while get_pos_x() > x_start:
		move(West)
	while get_pos_y() < y_start:
		move(North)
	while get_pos_y() > y_start:
		move(South)

	width = x_end - x_start + 1
	height = y_end - y_start + 1
	watch = []

	for row in range(height):
		if row % 2 == 0:
			forward = East
		else:
			forward = West

		for col in range(width):
			water_tile()
			if check_cactus_tile_here():
				watch.append((get_pos_x(), get_pos_y()))
			if col < width - 1:
				move(forward)

		if row < height - 1:
			move(North)

	while len(watch) > 0:
		next_watch = []
		while len(watch) > 0:
			x, y = watch.pop()
			move_to(x, y)
			water_tile()
			if check_cactus_tile_here():
				next_watch.append((x, y))
		watch = next_watch

	return True

def dispatch_tile():
	x = get_pos_x()
	y = get_pos_y()

	if x % 2 == 0 and y % 2 == 0:
		grow(Entities.Tree)
	elif x % 2 == 1 and y % 2 == 1:
		grow(Entities.Carrot)
	else:
		requested = take_companion_request(x, y)
		if requested != None:
			grow(requested)
		else:
			if can_harvest():
				harvest()
			if get_ground_type() == Grounds.Soil:
				till()

def farm_pass(start_x, end_x):
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
		else:
			forward = West

		for col in range(width):
			water_tile()
			dispatch_tile()
			if col < width - 1:
				move(forward)

		if row < size - 1:
			move(South)

	return True

def check_pumpkin_tile_here():
	entity = get_entity_type()
	if entity == Entities.Pumpkin:
		return not can_harvest()
	harvest()
	if get_ground_type() == Grounds.Grassland:
		till()
	plant(Entities.Pumpkin)
	return True

def pumpkin_band(y_start, y_end):
	x_start = size - 4
	x_end = size - 1

	while get_pos_x() < x_start:
		move(East)
	while get_pos_x() > x_start:
		move(West)
	while get_pos_y() < y_start:
		move(North)
	while get_pos_y() > y_start:
		move(South)

	width = x_end - x_start + 1
	height = y_end - y_start + 1
	watch = []

	for row in range(height):
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

		if row < height - 1:
			move(North)

	while len(watch) > 0:
		next_watch = []
		while len(watch) > 0:
			x, y = watch.pop()
			move_to(x, y)
			water_tile()
			if check_pumpkin_tile_here():
				next_watch.append((x, y))
		watch = next_watch

	return True

def sunflower_pass(y_start, y_end):
	x_start = 4
	x_end = 7

	while get_pos_x() < x_start:
		move(East)
	while get_pos_x() > x_start:
		move(West)
	while get_pos_y() < y_start:
		move(North)
	while get_pos_y() > y_start:
		move(South)

	width = x_end - x_start + 1
	height = y_end - y_start + 1
	found = []

	for row in range(height):
		if row % 2 == 0:
			forward = East
		else:
			forward = West

		for col in range(width):
			water_tile()
			entity = get_entity_type()
			if entity != None and entity != Entities.Sunflower:
				harvest()
				entity = get_entity_type()
			if get_ground_type() == Grounds.Grassland:
				till()
			if entity == None:
				plant(Entities.Sunflower)
			elif entity == Entities.Sunflower and can_harvest():
				petals = measure()
				found.append((petals, get_pos_x(), get_pos_y()))
			if col < width - 1:
				move(forward)

		if row < height - 1:
			move(North)

	return found

def sort_descending(candidates):
	ranked = []
	while len(candidates) > 0:
		best_index = 0
		for i in range(1, len(candidates)):
			if candidates[i][0] > candidates[best_index][0]:
				best_index = i
		ranked.append(candidates.pop(best_index))
	return ranked

def harvest_batch(batch):
	for i in range(len(batch)):
		petals, x, y = batch[i]
		move_to(x, y)
		if get_entity_type() == Entities.Sunflower and can_harvest():
			harvest()

def opposite_direction(direction):
	if direction == North:
		return South
	if direction == South:
		return North
	if direction == East:
		return West
	return East

def in_list(coords, x, y):
	for i in range(len(coords)):
		cx, cy = coords[i]
		if cx == x and cy == y:
			return True
	return False

def solve_maze(max_steps, directions):
	visited = []
	path = []
	visited.append((get_pos_x(), get_pos_y()))

	steps = 0
	while get_entity_type() != Entities.Treasure and steps < max_steps:
		x = get_pos_x()
		y = get_pos_y()

		next_dir = None
		for i in range(4):
			d = directions[i]
			if d == North:
				nx = x
				ny = y + 1
			elif d == South:
				nx = x
				ny = y - 1
			elif d == East:
				nx = x + 1
				ny = y
			else:
				nx = x - 1
				ny = y

			if next_dir == None and not in_list(visited, nx, ny) and can_move(d):
				next_dir = d

		if next_dir != None:
			move(next_dir)
			path.append(next_dir)
			visited.append((get_pos_x(), get_pos_y()))
		else:
			if len(path) == 0:
				return
			last = path.pop(len(path) - 1)
			move(opposite_direction(last))

		steps += 1

	if get_entity_type() == Entities.Treasure:
		harvest()

def run_maze(maze_size):
	clear()
	if get_entity_type() != Entities.Bush:
		plant(Entities.Bush)
	use_item(Items.Weird_Substance, maze_size)

	max_steps = size * size * 8

	orders = []
	orders.append([North, East, South, West])
	orders.append([East, South, West, North])
	orders.append([South, West, North, East])
	orders.append([West, North, East, South])

	count = max_drones()
	if count < 1:
		count = 1

	helpers = []
	for i in range(1, count):
		order = orders[i % 4]
		helper = spawn_drone(solve_maze, max_steps, order)
		helpers.append(helper)

	solve_maze(max_steps, orders[0])

	for i in range(len(helpers)):
		h = helpers[i]
		if h != None:
			wait_for(h)

	clear()

companion_requests = []

while True:
	size = get_world_size()
	count = max_drones()
	if count < 1:
		count = 1

	quick_print("cycle start, drones:", count)

	if count < 2:
		farm_pass(8, size - 5)
		quick_print("farm done")
		cactus_band(0, size - 1)
		quick_print("cactus done")
		sunflower_found = sunflower_pass(0, size - 1)
		quick_print("sunflowers found:", len(sunflower_found))
		pumpkin_band(0, size - 1)
		quick_print("pumpkin done")
		move_to(0, 0)
		harvest()
		move_to(size - 1, 0)
		harvest()
		harvest_batch(sort_descending(sunflower_found))
		quick_print("cycle done")
		continue

	worker_count = count - 1

	farm_x_start = 8
	farm_x_end = size - 5
	if farm_x_end < farm_x_start:
		farm_x_end = farm_x_start
	farm_width_total = farm_x_end - farm_x_start + 1

	cactus_job_count = worker_count
	if cactus_job_count < 1:
		cactus_job_count = 1
	if cactus_job_count > size:
		cactus_job_count = size
	pumpkin_job_count = worker_count
	if pumpkin_job_count < 1:
		pumpkin_job_count = 1
	if pumpkin_job_count > size:
		pumpkin_job_count = size
	sunflower_job_count = worker_count
	if sunflower_job_count < 1:
		sunflower_job_count = 1
	if sunflower_job_count > size:
		sunflower_job_count = size
	farm_job_count = worker_count
	if farm_job_count < 1:
		farm_job_count = 1
	if farm_job_count > farm_width_total:
		farm_job_count = farm_width_total
	if farm_job_count < 1:
		farm_job_count = 1

	farm_ranges = []
	chunk = farm_width_total // farm_job_count
	rem = farm_width_total % farm_job_count
	start = farm_x_start
	for i in range(farm_job_count):
		w = chunk
		if i < rem:
			w += 1
		if w < 1:
			w = 1
		end = start + w - 1
		farm_ranges.append((start, end))
		start = end + 1

	pumpkin_ranges = []
	pchunk = size // pumpkin_job_count
	prem = size % pumpkin_job_count
	ystart = 0
	for i in range(pumpkin_job_count):
		w = pchunk
		if i < prem:
			w += 1
		if w < 1:
			w = 1
		yend = ystart + w - 1
		pumpkin_ranges.append((ystart, yend))
		ystart = yend + 1

	cactus_ranges = []
	cchunk = size // cactus_job_count
	crem = size % cactus_job_count
	ystart = 0
	for i in range(cactus_job_count):
		w = cchunk
		if i < crem:
			w += 1
		if w < 1:
			w = 1
		yend = ystart + w - 1
		cactus_ranges.append((ystart, yend))
		ystart = yend + 1

	sunflower_ranges = []
	schunk = size // sunflower_job_count
	srem = size % sunflower_job_count
	ystart = 0
	for i in range(sunflower_job_count):
		w = schunk
		if i < srem:
			w += 1
		if w < 1:
			w = 1
		yend = ystart + w - 1
		sunflower_ranges.append((ystart, yend))
		ystart = yend + 1

	jobs = []
	for i in range(len(farm_ranges)):
		s, e = farm_ranges[i]
		jobs.append((0, s, e))
	for i in range(len(pumpkin_ranges)):
		s, e = pumpkin_ranges[i]
		jobs.append((1, s, e))
	for i in range(len(cactus_ranges)):
		s, e = cactus_ranges[i]
		jobs.append((2, s, e))
	for i in range(len(sunflower_ranges)):
		s, e = sunflower_ranges[i]
		jobs.append((3, s, e))

	next_job = 0
	slots = []
	slot_types = []
	for i in range(worker_count):
		slots.append(None)
		slot_types.append(-1)

	sunflower_found = []

	active_count = 0
	for i in range(worker_count):
		if next_job < len(jobs):
			jtype, a, b = jobs[next_job]
			next_job += 1
			slot_types[i] = jtype
			if jtype == 0:
				slots[i] = spawn_drone(farm_pass, a, b)
			elif jtype == 1:
				slots[i] = spawn_drone(pumpkin_band, a, b)
			elif jtype == 2:
				slots[i] = spawn_drone(cactus_band, a, b)
			else:
				slots[i] = spawn_drone(sunflower_pass, a, b)
			if slots[i] != None:
				active_count += 1

	quick_print("jobs queued:", len(jobs))

	while active_count > 0:
		for i in range(worker_count):
			if slots[i] != None and has_finished(slots[i]):
				result = wait_for(slots[i])
				if slot_types[i] == 3:
					for j in range(len(result)):
						sunflower_found.append(result[j])
				slots[i] = None
				active_count -= 1

				if next_job < len(jobs):
					jtype, a, b = jobs[next_job]
					next_job += 1
					slot_types[i] = jtype
					if jtype == 0:
						slots[i] = spawn_drone(farm_pass, a, b)
					elif jtype == 1:
						slots[i] = spawn_drone(pumpkin_band, a, b)
					elif jtype == 2:
						slots[i] = spawn_drone(cactus_band, a, b)
					else:
						slots[i] = spawn_drone(sunflower_pass, a, b)
					if slots[i] != None:
						active_count += 1

	quick_print("queue drained, sunflowers found:", len(sunflower_found))

	move_to(0, 0)
	harvest()
	move_to(size - 1, 0)
	harvest()

	quick_print("pumpkin+cactus harvested")

	ranked = sort_descending(sunflower_found)

	quick_print("sunflowers sorted")

	batch_size = len(ranked) // count
	batch_rem = len(ranked) % count
	batches = []
	idx = 0
	for i in range(count):
		b = batch_size
		if i < batch_rem:
			b += 1
		batch = []
		for j in range(b):
			batch.append(ranked[idx])
			idx += 1
		batches.append(batch)

	harvest_helpers = []
	for i in range(1, count):
		h = spawn_drone(harvest_batch, batches[i])
		harvest_helpers.append(h)

	harvest_batch(batches[0])

	quick_print("cycle done")

	for i in range(len(harvest_helpers)):
		h = harvest_helpers[i]
		if h != None:
			wait_for(h)
