size = get_world_size()

while True:
	for row in range(size):
		for col in range(size):
			if get_water() < 0.8:
				if num_items(Items.water) > 0:
					use_item(Items.water)
			if can_harvest():
				harvest()

			entity_type = get_entity_type()

			if entity_type == None:
				if (row + col) % 2 == 0:
					#till()
					plant(Entities.Tree)
				else:
					if row % 2 == 0:
						plant(Entities.Tree)
					else:
						if get_ground_type() == Grounds.Grassland:
							till()
						if get_ground_type() == Grounds.Soil:
							plant(Entities.Carrot)

			if col < size - 1:
				if row % 2 == 0:
					move(East)
				else:
					move(West)

		if row < size - 1:
			move(South)