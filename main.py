import os
from process_gen.main import gen_processes

# All processes have three stages, CPU Burst 1, I/O Burst, CPU Burst 2
# The variable stage takes care of which stage to do computation on
# Hence stage can be cpu_burst1, io_burst, or cpu_burst2

# Prints a generic list, elements separated by \n
def print_list(list1):
	for i in range(len(list1)):
		print(list1[i])

def update_time_quantum(ready_queue, stage):
	#print("updating time quantum")
	if len(ready_queue) == 0:
		return 1
	new_time_quantum = 0
	for i in range(len(ready_queue)):
		new_time_quantum = new_time_quantum + ready_queue[i][stage]
	new_time_quantum = new_time_quantum/len(ready_queue)
	return new_time_quantum

def push_into_ready_queue(ready_queue, ready_process):
	#print("push into ready queue works")
	for i in range(len(ready_queue)):
		if ready_process['cpu_burst1'] < ready_queue[i]['cpu_burst1']:
			ready_queue.insert(i, ready_process)
			return
	ready_queue.append(ready_process)

def not_in_ready_queue(ready_queue, processes, i):
	check = True
	for j in range(len(ready_queue)):
		if ready_queue[j]['pid'] == processes[i]['pid']:
			check = False
			break
	return check

# This checks if any new process has arrived and if so returns True(else False) and
# adds the process to ready queue and pops it from processes
def check_if_new_process(processes, ready_queue, cur_time):
	#print("check if new process works")
	is_there_a_new_process = False
	for i in range(len(processes)):
		if cur_time >= processes[i]['arrival_time']:
			ready_process = {}
			ready_process['pid'] = processes[i]['pid']
			ready_process['arrival_time'] = processes[i]['arrival_time']
			ready_process['cpu_burst1'] = processes[i]['cpu_burst1']
			ready_process['io_burst'] = processes[i]['io_burst']
			ready_process['cpu_burst2'] = processes[i]['cpu_burst2']
			ready_process['priority'] = processes[i]['priority']
			if not_in_ready_queue(ready_queue, processes, i):
				push_into_ready_queue(ready_queue, ready_process)
				is_there_a_new_process = True

	return is_there_a_new_process

# Calculate different time_quantum for 3 different priorities
def three_time_quantum(time_quantum, priority):
	#print("three time quantum works")
	temp_time_quantum = time_quantum

	if priority == 1:
		temp_time_quantum = 1.2*temp_time_quantum

	elif priority == 3:
		temp_time_quantum = 0.8*temp_time_quantum

	else:
		temp_time_quantum = temp_time_quantum

	return temp_time_quantum

def do_computation(ready_queue, time_quantum, cur_time, stage, io_queue):
	for i in range(len(ready_queue)):
		result = check_if_new_process(processes, ready_queue, cur_time)
		if result == True:
			do_computation(ready_queue, time_quantum, cur_time, stage, io_queue)
			return

		#print("doing computation")
		temp_time_quantum = three_time_quantum(time_quantum, ready_queue[i]['priority'])

		while temp_time_quantum > 0:
			if ready_queue[i][stage] != 0:
				ready_queue[i][stage] = ready_queue[i][stage] - 1
				cur_time = cur_time + 1
				temp_time_quantum = temp_time_quantum - 1
			else:
				# I need some way to update processes along with ready_queue
				key = ready_queue[i]['pid']
				x = 0
				for x in range(len(processes)):
					if processes[x]['pid'] == key:
						processes[x]['ready_time_for_io'] = cur_time
						break
				io_queue.append(processes[x])
				ready_queue[i][stage] = 0
				break

		temp_time_quantum = three_time_quantum(time_quantum, ready_queue[i]['priority'])
		if ready_queue[i][stage] < temp_time_quantum:
			cur_time = cur_time + ready_queue[i][stage]
			ready_queue[i][stage] = 0
			ready_queue[i]['ready_time_for_io'] = cur_time
			io_queue.append(ready_queue[i])
			ready_queue[i][stage] = 0

def check_if_burst_is_finished(ready_queue, stage):
	check = True
	for i in range(len(ready_queue)):
		if ready_queue[i][stage] == 0:
			continue
		else:
			check = False
			break
	return check


# Execution begins here
# To change input method change the lines below
"""
t = int(input("Enter time frame: "))
processes = gen_processes(t)
print("\nPrinting all the randomized processes generated\n")
print_list(processes)
print("\n")

# Or use this input for custom input
"""
processes = [
			{'pid': 0, 'arrival_time': 1, 'cpu_burst1': 2, 'io_burst': 5, 'cpu_burst2': 19, 'priority': 2},
			{'pid': 1, 'arrival_time': 1, 'cpu_burst1': 16, 'io_burst': 2, 'cpu_burst2': 8, 'priority': 3},
			{'pid': 2, 'arrival_time': 1, 'cpu_burst1': 16, 'io_burst': 2, 'cpu_burst2': 18, 'priority': 2},
			{'pid': 3, 'arrival_time': 1, 'cpu_burst1': 7, 'io_burst': 2, 'cpu_burst2': 5, 'priority': 2},
			{'pid': 4, 'arrival_time': 2, 'cpu_burst1': 10, 'io_burst': 7, 'cpu_burst2': 5, 'priority': 3},
			{'pid': 5, 'arrival_time': 2, 'cpu_burst1': 20, 'io_burst': 6, 'cpu_burst2': 7, 'priority': 2}
			]
"""
"""

print("\nPrinting all the randomized processes generated\n")
print_list(processes)
print("\n")

# To calculate the comparision parameters, end times are noted here
# For pid# the corresponding dict is at # 
# The format will be {'cpu1_start', 'cpu1_end', 'io_start', 'io_end', 'cpu2_start', 'cpu2_end'}
n = len(processes)
end_times = []

# Three ready queues for the three stages
ready_queue = []

# To keep track of I/O systems
io_queue = []

# for the second cpu burst
ready_queue_2 = []

# To keep a track of current time
# CHANGE THIS LATER TO A DIFFERENT STARTING CURRRENT TIME
cur_time = processes[0]['arrival_time']

cur_time_io = 0

cur_time_finalcpu = 0

# Initializing time quantum
time_quantum = 1

# Stage for future use, i.e. IO and CPU burst2
stage = 'cpu_burst1'

# Now to begin processing of the first CPU Burst
while(True):

	time_quantum = update_time_quantum(ready_queue, stage)

	result = check_if_new_process(processes, ready_queue, cur_time)

	if result == True:
		time_quantum = update_time_quantum(ready_queue, stage)
	
	do_computation(ready_queue, time_quantum, cur_time, stage, io_queue)

	cur_time = cur_time + 1

	#print_list(ready_queue)

	# Fixed the condition already, never updated the above comment
	if check_if_burst_is_finished(ready_queue, stage):
		break


# Just printing stuff
print("\nThe order in which the processes finish executing:\n")
print_list(ready_queue)
print("\n")

avg_throughput = len(ready_queue) / ready_queue[len(ready_queue)-1]['ready_time_for_io']
print("\nAverage Throughput: ", avg_throughput)

avg_turnaround = 0

for i in ready_queue:
	current = i['ready_time_for_io'] - i['arrival_time']
	avg_turnaround = avg_turnaround + current

avg_wait = avg_turnaround
avg_turnaround = avg_turnaround / len(ready_queue)

print("\nAverage Turnaround time: ", avg_turnaround)

for i in processes:
	avg_wait = avg_wait - i['cpu_burst1']

avg_wait = avg_wait / len(ready_queue)

print("\nAverage Waiting time: ", avg_wait)
print("\n")
