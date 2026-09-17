quick_print("Starting cactus farm program f6")
clear()
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

def plant_column():
	global world_size
	for i in range(world_size):
		if get_ground_type() == Grounds.Grassland:
			till()
		plant(Entities.Cactus)
		move(North)

def plant_columns():
	global world_size
	move_to_x(0)
	move_to_y(0)
	drones = []
	for x in range(world_size):
		if x > 0:
			move_to_x(x)
			move_to_y(0)
		drone = spawn_drone(plant_column)
		if drone != None:
			drones.append(drone)
		else:
			plant_column()
	for drone in drones:
		wait_for(drone)

def sort_column():
	global world_size
	changed = False
	for i in range(world_size - 1):
		current = measure()
		above = measure(North)
		if above != None and current > above:
			swap(North)
			changed = True
		move(North)
	return changed

def sort_columns():
	global world_size
	move_to_x(0)
	move_to_y(0)
	drones = []
	changed = False
	for x in range(world_size):
		if x > 0:
			move_to_x(x)
			move_to_y(0)
		drone = spawn_drone(sort_column)
		if drone != None:
			drones.append(drone)
		else:
			if sort_column():
				changed = True
	for drone in drones:
		if wait_for(drone):
			changed = True
	return changed

def sort_row():
	global world_size
	changed = False
	for i in range(world_size - 1):
		current = measure()
		right = measure(East)
		if right != None and current > right:
			swap(East)
			changed = True
		move(East)
	return changed

def sort_rows():
	global world_size
	move_to_x(0)
	move_to_y(0)
	drones = []
	changed = False
	for y in range(world_size):
		if y > 0:
			move_to_y(y)
			move_to_x(0)
		drone = spawn_drone(sort_row)
		if drone != None:
			drones.append(drone)
		else:
			if sort_row():
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
