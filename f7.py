quick_print("Starting carrot program f7")

def wear_work_hat():
	change_hat(Hats.Traffic_Cone)

def wear_grow_hat():
	change_hat(Hats.Carrot_Hat)

def wear_harvest_hat():
	change_hat(Hats.Wizard_Hat)

def water_tile():
	if get_water() < 0.2:
		if num_items(Items.Water) > 0:
			use_item(Items.Water)

def carrot_range(start_x, end_x):
	size = get_world_size()
	while True:
		while get_pos_x() < start_x:
			move(East)
		while get_pos_x() > start_x:
			move(West)
		while get_pos_y() > 0:
			move(South)

		width = end_x - start_x + 1

		for row in range(size):
			if row % 2 == 0:
				forward = East
			else:
				forward = West

			for col in range(width):
				water_tile()
				if can_harvest():
					wear_harvest_hat()
					harvest()
				if get_ground_type() == Grounds.Grassland:
					wear_work_hat()
					till()
				if get_entity_type() == None:
					wear_grow_hat()
					plant(Entities.Carrot)
				if col < width - 1:
					move(forward)

			if row < size - 1:
				move(North)

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
	spawn_drone(carrot_range, s, e)

s0, e0 = ranges[0]
carrot_range(s0, e0)
