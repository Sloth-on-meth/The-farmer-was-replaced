

def turn_left(direction):
	if direction == North:
		return West
	if direction == West:
		return South
	if direction == South:
		return East
	return North

def turn_right(direction):
	if direction == North:
		return East
	if direction == East:
		return South
	if direction == South:
		return West
	return North

def pick_random(options):
	r = random() * len(options) // 1
	return options[r]

def pick_biased(free_dirs, bias_order):
	roll = random()
	if roll < 0.15:
		return pick_random(free_dirs)
	for i in range(4):
		d = bias_order[i]
		if d in free_dirs:
			return d
	return free_dirs[0]

def wall_follow_right(max_steps, starting_gold):
	facing = North
	steps = 0
	while steps < max_steps and num_items(Items.Gold) == starting_gold:
		side = turn_right(facing)
		if can_move(side):
			facing = side
			move(facing)
		elif can_move(facing):
			move(facing)
		else:
			facing = turn_left(facing)

		if get_entity_type() == Entities.Treasure:
			harvest()
			return

		steps += 1

def explore(max_steps, starting_gold, bias_order):
	path = []

	steps = 0
	while steps < max_steps and num_items(Items.Gold) == starting_gold:
		x = get_pos_x()
		y = get_pos_y()
		pos = (x, y)

		if get_entity_type() == Entities.Treasure:
			harvest()
			return

		walls = {
			North: not can_move(North),
			East: not can_move(East),
			South: not can_move(South),
			West: not can_move(West)
		}

		if pos not in visited_tiles:
			visited_tiles[pos] = walls

		if len(path) == 0 or path[len(path) - 1] != pos:
			path.append(pos)

		free_dirs = []
		for d in [North, East, South, West]:
			if not walls[d]:
				dx = 0
				dy = 0
				if d == North:
					dy = 1
				elif d == South:
					dy = -1
				elif d == East:
					dx = 1
				elif d == West:
					dx = -1
				next_pos = (x + dx, y + dy)
				if next_pos not in visited_tiles:
					free_dirs.append(d)

		if len(free_dirs) > 0:
			chosen = pick_biased(free_dirs, bias_order)

			if len(free_dirs) > 1 and num_drones() < max_drones():
				alt_dirs = []
				for i in range(len(free_dirs)):
					if free_dirs[i] != chosen:
						alt_dirs.append(free_dirs[i])
				if len(alt_dirs) > 0:
					fork_dir = pick_random(alt_dirs)
					spawn_drone(explore_from_fork, max_steps, starting_gold, bias_order, fork_dir)

			move(chosen)
		else:
			if len(path) <= 1:
				return
			path.pop()
			px, py = path[len(path) - 1]
			if px > x:
				move(East)
			elif px < x:
				move(West)
			elif py > y:
				move(North)
			elif py < y:
				move(South)

		steps += 1

def explore_from_fork(max_steps, starting_gold, bias_order, first_dir):
	move(first_dir)
	explore(max_steps, starting_gold, bias_order)

def create_maze():
	clear()
	plant(Entities.Bush)

	while get_entity_type() == Entities.Bush:
		substance = get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
		if num_items(Items.Weird_Substance) >= substance:
			use_item(Items.Weird_Substance, substance)
			return True
		if can_harvest():
			harvest()
			plant(Entities.Bush)
		if num_items(Items.Fertilizer) == 0:
			return False
		use_item(Items.Fertilizer)

visited_tiles = {}

while True:
	if not create_maze():
		continue

	visited_tiles = {}

	size = get_world_size()
	max_steps = size * size * 8
	starting_gold = num_items(Items.Gold)

	count = max_drones()
	if count < 1:
		count = 1

	orders = []
	orders.append([North, East, South, West])
	orders.append([East, South, West, North])
	orders.append([South, West, North, East])
	orders.append([West, North, East, South])

	helper = None
	if count > 1:
		helper = spawn_drone(wall_follow_right, max_steps, starting_gold)

	explore(max_steps, starting_gold, orders[0])

	if helper != None:
		wait_for(helper)

	while num_drones() > 1:
		pass

	clear()
