def move_to(x, y):
	while get_pos_x() < x:
		move(East)
	while get_pos_x() > x:
		move(West)
	while get_pos_y() < y:
		move(North)
	while get_pos_y() > y:
		move(South)

def water_tile():
	if get_water() < 0.6:
		if num_items(Items.Water) > 0:
			use_item(Items.Water)

def plant_pass(start_x, end_x):
	while get_pos_x() < start_x:
		move(East)
	while get_pos_x() > start_x:
		move(West)
	while get_pos_y() < size - 1:
		move(North)

	width = end_x - start_x + 1
	done = True

	for row in range(size):
		if row % 2 == 0:
			forward = East
		else:
			forward = West

		for col in range(width):
			water_tile()
			entity = get_entity_type()
			if entity == None:
				if get_ground_type() == Grounds.Grassland:
					till()
				plant(Entities.Pumpkin)
				done = False
			elif entity == Entities.Pumpkin:
				if not can_harvest():
					done = False
			if col < width - 1:
				move(forward)

		if row < size - 1:
			move(South)

	return done

def search_pass(start_x, end_x):
	while get_pos_x() < start_x:
		move(East)
	while get_pos_x() > start_x:
		move(West)
	while get_pos_y() < size - 1:
		move(North)

	width = end_x - start_x + 1
	clean = True

	for row in range(size):
		if row % 2 == 0:
			forward = East
		else:
			forward = West

		for col in range(width):
			if get_entity_type() == Entities.Dead_Pumpkin:
				harvest()
				if get_ground_type() == Grounds.Grassland:
					till()
				plant(Entities.Pumpkin)
				clean = False
			if col < width - 1:
				move(forward)

		if row < size - 1:
			move(South)

	return clean

while True:
	size = get_world_size()
	count = max_drones()
	if count < 1:
		count = 1

	job_count = count * 3
	if job_count < 1:
		job_count = 1
	if job_count > size:
		job_count = size

	ranges = []
	chunk = size // job_count
	rem = size % job_count
	start = 0
	for i in range(job_count):
		w = chunk
		if i < rem:
			w += 1
		if w < 1:
			w = 1
		end = start + w - 1
		ranges.append((start, end))
		start = end + 1

	worker_count = count - 1
	if worker_count < 0:
		worker_count = 0

	round_clean = False

	while not round_clean:
		jobs = []
		for i in range(len(ranges)):
			s, e = ranges[i]
			jobs.append((0, s, e))
		for i in range(len(ranges)):
			s, e = ranges[i]
			jobs.append((1, s, e))

		all_mature = True
		all_clean = True

		next_job = 0
		slots = []
		slot_types = []
		for i in range(worker_count):
			slots.append(None)
			slot_types.append(-1)

		active_count = 0
		for i in range(worker_count):
			if next_job < len(jobs):
				jtype, a, b = jobs[next_job]
				next_job += 1
				slot_types[i] = jtype
				if jtype == 0:
					slots[i] = spawn_drone(plant_pass, a, b)
				else:
					slots[i] = spawn_drone(search_pass, a, b)
				if slots[i] != None:
					active_count += 1

		if next_job < len(jobs):
			jtype, a, b = jobs[next_job]
			next_job += 1
			if jtype == 0:
				if not plant_pass(a, b):
					all_mature = False
			else:
				if not search_pass(a, b):
					all_clean = False

		while active_count > 0:
			for i in range(worker_count):
				if slots[i] != None and has_finished(slots[i]):
					result = wait_for(slots[i])
					if slot_types[i] == 0:
						if not result:
							all_mature = False
					else:
						if not result:
							all_clean = False
					slots[i] = None
					active_count -= 1

					if next_job < len(jobs):
						jtype, a, b = jobs[next_job]
						next_job += 1
						slot_types[i] = jtype
						if jtype == 0:
							slots[i] = spawn_drone(plant_pass, a, b)
						else:
							slots[i] = spawn_drone(search_pass, a, b)
						if slots[i] != None:
							active_count += 1

		round_clean = all_mature and all_clean

	move_to(0, 0)
	harvest()
