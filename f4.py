def in_list(coords, x, y):
	for i in range(len(coords)):
		cx, cy = coords[i]
		if cx == x and cy == y:
			return True
	return False

def opposite_direction(direction):
	if direction == North:
		return South
	if direction == South:
		return North
	if direction == East:
		return West
	return East

def solve_maze(directions, max_steps, starting_gold):
	visited = []
	path = []
	visited.append((get_pos_x(), get_pos_y()))

	steps = 0
	while steps < max_steps and num_items(Items.Gold) == starting_gold:
		x = get_pos_x()
		y = get_pos_y()

		moved = False
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

			if not in_list(visited, nx, ny):
				if move(d):
					path.append(d)
					visited.append((nx, ny))
					moved = True
					if get_entity_type() == Entities.Treasure:
						harvest()
						return
					break

		if not moved:
			if len(path) == 0:
				return
			last = path.pop(len(path) - 1)
			move(opposite_direction(last))

		steps += 1

orders = []
orders.append([North, East, South, West])
orders.append([East, South, West, North])
orders.append([South, West, North, East])
orders.append([West, North, East, South])

while True:
	size = get_world_size()

	multiplier = 1
	level = num_unlocked(Unlocks.Mazes)
	for i in range(level - 1):
		multiplier = multiplier * 2
	maze_size = size * multiplier

	while num_items(Items.Weird_Substance) < maze_size:
		pass

	clear()
	if get_entity_type() != Entities.Bush:
		plant(Entities.Bush)
	use_item(Items.Weird_Substance, maze_size)

	max_steps = size * size * 8
	starting_gold = num_items(Items.Gold)

	count = max_drones()
	if count < 1:
		count = 1

	helpers = []
	for i in range(1, count):
		order = orders[i % 4]
		helper = spawn_drone(solve_maze, order, max_steps, starting_gold)
		helpers.append(helper)

	solve_maze(orders[0], max_steps, starting_gold)

	for i in range(len(helpers)):
		h = helpers[i]
		if h != None:
			wait_for(h)

	clear()
