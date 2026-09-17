def sunflower_pass(start_x, end_x):
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

	return True

while True:
	size = get_world_size()
	count = max_drones()
	if count < 1:
		count = 1

	min_job_size = 3
	job_count = size // min_job_size
	if job_count < 1:
		job_count = 1

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

	next_job = 0

	primary_job = None
	if next_job < len(ranges):
		primary_job = ranges[next_job]
		next_job += 1

	slots = []
	for i in range(worker_count):
		slots.append(None)

	active_count = 0
	for i in range(worker_count):
		if next_job < len(ranges):
			s, e = ranges[next_job]
			next_job += 1
			slots[i] = spawn_drone(sunflower_pass, s, e)
			if slots[i] != None:
				active_count += 1

	if primary_job != None:
		sunflower_pass(primary_job[0], primary_job[1])

	while active_count > 0:
		for i in range(worker_count):
			if slots[i] != None and has_finished(slots[i]):
				wait_for(slots[i])
				slots[i] = None
				active_count -= 1

				if next_job < len(ranges):
					s, e = ranges[next_job]
					next_job += 1
					slots[i] = spawn_drone(sunflower_pass, s, e)
					if slots[i] != None:
						active_count += 1
