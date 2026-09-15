size = get_world_size()
pumpkin_split = size // 2

while True:
	for row in range(size):
		for col in range(size):

			#if num_items(Items.Fertilizer) > 0:
			#		use_item(Items.Fertilizer)
			if get_water() < 0.2:
				if num_items(Items.Water) > 0:
					use_item(Items.Water)

			if can_harvest():
				harvest()

			if get_entity_type() == Entities.Dead_Pumpkin:
				harvest()

			if col >= pumpkin_split:
				if get_ground_type() == Grounds.Grassland:
					till()

				if get_entity_type() == None:
					plant(Entities.Pumpkin)
			else:
				is_tree_tile = row % 2 == 0 and col % 2 == 0
				is_carrot_tile = row % 2 == 1 and col % 2 == 1

				if is_tree_tile or is_carrot_tile:
					if get_ground_type() == Grounds.Grassland:
						till()

					if get_entity_type() == None:
						if is_tree_tile:
							plant(Entities.Tree)
						else:
							plant(Entities.Carrot)

			if col < size - 1:
				if row % 2 == 0:
					move(East)
				else:
					move(West)

		if row < size - 1:
			move(South)