def move_to(x, y):
	while get_pos_x() < x:
		move(East)
	while get_pos_x() > x:
		move(West)
	while get_pos_y() < y:
		move(North)
	while get_pos_y() > y:
		move(South)

def distance(x1, y1, x2, y2):
	return abs(x1 - x2) + abs(y1 - y2)

while True:
	size = get_world_size()
	pumpkin_active = num_items(Items.Carrot) >= 50

	if not pumpkin_active:
		while get_pos_x() > 0:
			move(West)
		while get_pos_y() < size - 1:
			move(North)

		for row in range(size):
			for col in range(size):
				if get_water() < 0.2:
					if num_items(Items.Water) > 0:
						use_item(Items.Water)
				if can_harvest():
					harvest()
				if get_ground_type() == Grounds.Grassland:
					till()
				if get_entity_type() == None:
					plant(Entities.Carrot)
				if col < size - 1:
					if row % 2 == 0:
						move(East)
					else:
						move(West)
			if row < size - 1:
				move(South)
	else:
		pending = []
		for y in range(size):
			for x in range(size):
				pending.append((x, y))

		while len(pending) > 0:
			cx = get_pos_x()
			cy = get_pos_y()

			best_index = 0
			best_dist = -1
			for i in range(len(pending)):
				px, py = pending[i]
				if px == cx and py == cy and len(pending) > 1:
					continue
				d = distance(cx, cy, px, py)
				if best_dist == -1 or d < best_dist:
					best_dist = d
					best_index = i

			x, y = pending[best_index]
			move_to(x, y)

			if get_water() < 0.2:
				if num_items(Items.Water) > 0:
					use_item(Items.Water)

			entity = get_entity_type()
			if entity == Entities.Pumpkin:
				if can_harvest():
					pending.pop(best_index)
			else:
				harvest()
				if get_ground_type() == Grounds.Grassland:
					till()
				plant(Entities.Pumpkin)

		harvest()
