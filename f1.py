size = get_world_size()

while True:
	for row in range(size):
		for col in range(size):
			if get_water() < 0.2:
				if num_items(Items.Water) > 0:
					use_item(Items.Water)
			if get_ground_type() == Grounds.Grassland:
				till()

			if can_harvest():
				harvest()
			elif get_entity_type() == Entities.Dead_Pumpkin:
				harvest()

			if get_entity_type() == None:
				plant(Entities.Pumpkin)

			if col < size - 1:
				if row % 2 == 0:
					move(East)
				else:
					move(West)

		if row < size - 1:
			move(South)
