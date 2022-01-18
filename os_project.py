 
# All processes have three stages, CPU Burst 1, I/O Burst, CPU Burst 2
# The variable stage takes care of which stage to do computation on
# Hence stage can be cpu_burst1, io_burst, or cpu_burst2
 
# Prints a generic list, elements separated by \n
def print_list(list1):
	for i in range(len(list1)):
		print(list1[i])
 
def update_time_quantum(ready_queue):
	if len(ready_queue) == 0:
		return 1
	new_time_quantum = 0
	for i in range(len(ready_queue)):
         new_time_quantum = new_time_quantum + ready_queue[i][ready_queue[i]['current_stage']]
	new_time_quantum = new_time_quantum/len(ready_queue)
	return new_time_quantum
 
def push_into_ready_queue(ready_queue, ready_process):
	#print("push into ready queue works")
	for i in range(len(ready_queue)):
		if ready_process['priority'] < ready_queue[i]['priority']:
			ready_queue.insert(i, ready_process)
			return
		if ready_process['priority'] == ready_queue[i]['priority'] and ready_process[ready_process['current_stage']] <= ready_queue[i][ready_queue[i]['current_stage']]:
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
def check_if_new_process(processes, ready_queue, io_queue, cur_time):
	#print("check if new process works")
	processes_to_delete = []
	io_queue_delete = []
	for i in range(len(processes)):
		if cur_time >= processes[i]['arrival_time']:
			ready_process = {}
			ready_process['pid'] = processes[i]['pid']
			ready_process['arrival_time'] = processes[i]['arrival_time']
			ready_process['cpu_burst1'] = processes[i]['cpu_burst1']
			ready_process['io_burst'] = processes[i]['io_burst']
			ready_process['cpu_burst2'] = processes[i]['cpu_burst2']
			ready_process['priority'] = processes[i]['priority']
			ready_process['current_stage'] = 'cpu_burst1'
			ready_process['cpu_burst2_time'] = 0
			ready_process['started_executing'] = 0
			processes_to_delete.append(processes[i])
			push_into_ready_queue(ready_queue, ready_process)
				
	for i in range(len(io_queue)):
		if cur_time >= io_queue[i]['cpu_burst2_time']:
			ready_process = {}
			ready_process['pid'] = io_queue[i]['pid']
			ready_process['arrival_time'] = io_queue[i]['arrival_time']
			ready_process['cpu_burst1'] = io_queue[i]['cpu_burst1']
			ready_process['io_burst'] = io_queue[i]['io_burst']
			ready_process['cpu_burst2'] = io_queue[i]['cpu_burst2']
			ready_process['priority'] = io_queue[i]['priority']
			ready_process['current_stage'] = 'cpu_burst2'
			ready_process['cpu_burst2_time'] = 0
			ready_process['started_executing'] = 1
			io_queue_delete.append(io_queue[i])
			push_into_ready_queue(ready_queue, ready_process)
 
	for process in processes_to_delete:
		processes.remove(process)
 
	for process in io_queue_delete:
		io_queue.remove(process)
 
 
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
 
def do_computation(ready_queue, time_quantum, cur_time, io_queue):
	time_taken = 0
	waiting_time = 0 
	if ( ready_queue[0]['started_executing'] == 0):
	    ready_queue[0]['started_executing'] = 1
	    waiting_time = cur_time - ready_queue[0]['arrival_time']
	temp_time_quantum = three_time_quantum(time_quantum, ready_queue[0]['priority'])
	total_turn_around_time = 0
	while temp_time_quantum > 0:
		ready_queue[0][ready_queue[0]['current_stage']] = ready_queue[0][ready_queue[0]['current_stage']] - 1
		time_taken = time_taken + 1
		temp_time_quantum = temp_time_quantum - 1
		if ( ready_queue[0][ready_queue[0]['current_stage']] == 0):
			if ( ready_queue[0]['current_stage'] == 'cpu_burst2'):
				print("Process",ready_queue[0]['pid'],"finished executing at",cur_time+time_taken)
				total_turn_around_time =  cur_time + time_taken - ready_queue[0]['arrival_time'] 
				del ready_queue[0]
				break
			ready_queue[0]['cpu_burst2_time'] = cur_time + time_taken + ready_queue[0]['io_burst']
			ready_queue[0]['current_stage'] = 'io_burst'
			io_queue.append(ready_queue[0])
			del ready_queue[0]
			break
	return time_taken , total_turn_around_time, waiting_time
		
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
 
initial_time = processes[0]['arrival_time']
cur_time = initial_time
 
total_waiting_time = 0
total_turn_around_time = 0
 
 
# Now to begin processing of the first CPU Burst
while(True):
    
    check_if_new_process(processes, ready_queue, io_queue,cur_time)
 
    if not ready_queue:
        if not io_queue:
            break
        cur_time = cur_time + 1
        continue
    
    time_quantum = update_time_quantum(ready_queue)
    time_taken , turnAround, waiting_time = do_computation(ready_queue, time_quantum, cur_time, io_queue)

    total_turn_around_time = total_turn_around_time + turnAround
    cur_time = cur_time + time_taken
    total_waiting_time = total_waiting_time + waiting_time
 
 
 
 
# avg_throughput = len(ready_queue) / ready_queue[len(ready_queue)-1]['ready_time_for_io']
# print("\nAverage Throughput: ", avg_throughput)
 
avg_turnaround = total_turn_around_time / 6
 
print("\nAverage Turnaround time: ", avg_turnaround)
avg_wait = total_waiting_time / 6
 
print("\nAverage Waiting time: ", avg_wait)
print("\n")
