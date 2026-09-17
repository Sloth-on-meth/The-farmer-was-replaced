print("Starting sunflower farm program f5")

def water_tile():
	if get_water() < 0.2:
		if num_items(Items.Water) > 0:
			use_item(Items.Water)

def sunflower_loop(start_x, end_x):
	while True:
		size = get_world_size()

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
				if can_harvest():
					harvest()
				if get_ground_type() == Grounds.Grassland:
					till()
				if get_entity_type() == None:
					plant(Entities.Sunflower)
				if col < width - 1:
					move(forward)

			if row < size - 1:
				move(South)

size = get_world_size()
count = max_drones()
if count < 1:
	count = 1

ranges = []
chunk = size // count
rem = size % count
start = 0
for i in range(count):
	w = chunk
	if i < rem:
		w += 1
	if w < 1:
		w = 1
	end = start + w - 1
	ranges.append((start, end))
	start = end + 1

for i in range(1, count):
	s, e = ranges[i]
	spawn_drone(sunflower_loop, s, e)

s0, e0 = ranges[0]
sunflower_loop(s0, e0)
