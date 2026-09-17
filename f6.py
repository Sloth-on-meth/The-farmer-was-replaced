print("Starting cactus farm program f6")
#clear()
world_size = get_world_size()

def _shortest_delta(curr, dest):
	global world_size
	d = (dest - curr) % world_size
	if d > world_size / 2:
		d -= world_size
	return d

def move_to_x(x_target):
	d = _shortest_delta(get_pos_x(), x_target)
	if d > 0:
		dir = East
	else:
		dir = West
	for i in range(abs(d)):
		move(dir)

def move_to_y(y_target):
	d = _shortest_delta(get_pos_y(), y_target)
	if d > 0:
		dir = North
	else:
		dir = South
	for i in range(abs(d)):
		move(dir)

def water_tile():
	if get_water() < 0.2:
		if num_items(Items.Water) > 0:
			use_item(Items.Water)

def plant_column(x):
	global world_size
	move_to_x(x)
	move_to_y(0)
	for i in range(world_size):
		water_tile()
		if get_ground_type() == Grounds.Grassland:
			till()
		plant(Entities.Cactus)
		move(North)

def plant_columns():
	global world_size
	drones = []
	for x in range(world_size):
		drone = spawn_drone(plant_column, x)
		if drone != None:
			drones.append(drone)
		else:
			plant_column(x)
	for drone in drones:
		wait_for(drone)

def sort_column(x):
	global world_size
	move_to_x(x)
	changed = False
	low = 0
	high = world_size - 1

	while low < high:
		move_to_y(low)
		last_swap = low
		y_curr = low
		while y_curr < high:
			water_tile()
			current = measure()
			above = measure(North)
			if above != None and current > above:
				swap(North)
				changed = True
				last_swap = y_curr
			move(North)
			y_curr += 1
		high = last_swap
		if low >= high:
			break

		move_to_y(high)
		last_swap = high
		y_curr = high
		while y_curr > low:
			water_tile()
			current = measure()
			below = measure(South)
			if below != None and below > current:
				swap(South)
				changed = True
				last_swap = y_curr
			move(South)
			y_curr -= 1
		low = last_swap

	return changed

def sort_columns():
	global world_size
	drones = []
	changed = False
	for x in range(world_size):
		drone = spawn_drone(sort_column, x)
		if drone != None:
			drones.append(drone)
		else:
			if sort_column(x):
				changed = True
	for drone in drones:
		if wait_for(drone):
			changed = True
	return changed

def sort_row(y):
	global world_size
	move_to_y(y)
	changed = False
	left = 0
	right = world_size - 1

	while left < right:
		move_to_x(left)
		last_swap = left
		x_curr = left
		while x_curr < right:
			water_tile()
			current = measure()
			east = measure(East)
			if east != None and current > east:
				swap(East)
				changed = True
				last_swap = x_curr
			move(East)
			x_curr += 1
		right = last_swap
		if left >= right:
			break

		move_to_x(right)
		last_swap = right
		x_curr = right
		while x_curr > left:
			water_tile()
			current = measure()
			west = measure(West)
			if west != None and west > current:
				swap(West)
				changed = True
				last_swap = x_curr
			move(West)
			x_curr -= 1
		left = last_swap

	return changed

def sort_rows():
	global world_size
	drones = []
	changed = False
	for y in range(world_size):
		drone = spawn_drone(sort_row, y)
		if drone != None:
			drones.append(drone)
		else:
			if sort_row(y):
				changed = True
	for drone in drones:
		if wait_for(drone):
			changed = True
	return changed

while True:
	plant_columns()
	changed = True
	while changed:
		changed = False
		if sort_columns():
			changed = True
		if sort_rows():
			changed = True
	move_to_x(0)
	move_to_y(0)
	harvest()
