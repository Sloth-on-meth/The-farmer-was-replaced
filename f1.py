while True:
	size = get_world_size()

	while get_pos_x() > 0:
		move(West)
	while get_pos_y() < size - 1:
		move(North)

	pumpkin_active = num_items(Items.Carrot) >= 50
	pumpkin_ready = True

	for row in range(size):
		for col in range(size):
			if get_water() < 0.2:
				if num_items(Items.Water) > 0:
					use_item(Items.Water)

			if pumpkin_active:
				entity = get_entity_type()
				if entity == Entities.Pumpkin:
					if not can_harvest():
						pumpkin_ready = False
				else:
					harvest()
					if get_ground_type() == Grounds.Grassland:
						till()
					plant(Entities.Pumpkin)
					pumpkin_ready = False
			else:
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

	if pumpkin_active and pumpkin_ready:
		harvest()
