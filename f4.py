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

def wall_follow_left(max_steps, starting_gold):
	facing = North
	steps = 0
	while steps < max_steps and num_items(Items.Gold) == starting_gold:
		side = turn_left(facing)
		if can_move(side):
			facing = side
			move(facing)
		elif can_move(facing):
			move(facing)
		else:
			facing = turn_right(facing)

		if get_entity_type() == Entities.Treasure:
			harvest()
			return

		steps += 1

def move_towards_treasure(max_steps, starting_gold):
	tiles = {}
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

		if pos not in tiles:
			tiles[pos] = walls

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
				if next_pos not in tiles:
					free_dirs.append(d)

		if len(free_dirs) > 0:
			move(pick_random(free_dirs))
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

while True:
	if not create_maze():
		continue

	size = get_world_size()
	max_steps = size * size * 8
	starting_gold = num_items(Items.Gold)

	count = max_drones()
	if count < 1:
		count = 1

	helpers = []
	for i in range(1, count):
		if i == 1:
			helper = spawn_drone(wall_follow_right, max_steps, starting_gold)
		elif i == 2:
			helper = spawn_drone(wall_follow_left, max_steps, starting_gold)
		else:
			helper = spawn_drone(move_towards_treasure, max_steps, starting_gold)
		helpers.append(helper)

	move_towards_treasure(max_steps, starting_gold)

	for i in range(len(helpers)):
		h = helpers[i]
		if h != None:
			wait_for(h)

	clear()
