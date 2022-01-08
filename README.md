# cpu-scheduling-algorithm

The main criteria for
judging CPU scheduling algorithms are:
1. CPU Utilisation: CPU should be used all times
to get good results, i.e, CPU utilisation should be
high.

2. Throughput: The number of processes that are ex-
ecuted completely per unit time should be high.

3. Waiting Time: The time for which a process waits
for execution should be low.
4. Turnaround Time: The time taken by the CPU to
completely execute a process should be low.
5. Response Time: The total amount of time CPU
takes to respond to a request should be low.


## Composite Scheduling Algorithms 

#### Shortest Job First (SJF): 
In this scheduling algo-
rithm, the processes are executed in the increasing order of their burst time. However, it may face a
problem when there are processes with large burst
time in the ready queue, as such process may not

get executed leading to “Starvation.” This algo-
rithm gives the most optimized values in all param-
eters like waiting, turnaround, and context switch-
ing.

#### Priority Scheduling: 
This scheduling assigns every

process with a priority number. CPU then exe-
cutes the processes in decreasing order of priority

regardless of their burst time. This type of schedul-
ing may also lead to starvation.

#### Round Robin Scheduling (RR): 
In this algorithm,

a time quantum is set which permits the pro-
cess to utilize the CPU to its full extent, thereby

giving equal importance to all the elements in
the ready queue. Starvation is eliminated in this
manner. The waiting times, context switching
and turnaround times are not optimised but the

throughput of the system is increased and the re-
sponse time decreases.


##  Proposed Algorithm

The proposed model works by combining aspects of
three existing algorithms (SJF, Round Robin, Priority)
into one. In addition to this, to overcome the problem
of choosing an appropriate quantum time that is not too

long or too short for the given processes, we dynami-
cally calculate the quantum time at every second. We

also evaluate whether the remaining CPU burst time of

a process is less than the quantum time and if so, con-
tinue to let it run in the CPU. This is done to minimise

the context switching. The algorithm is detailed below
and the proposed workflow is on the next page.
1. Input the number of processes.
2. Input the Process ID, Arrival Time, CPU Burst,
I/O Burst and Priority for each process.
3. Initialise timer to zero.
4. Check if any processes arrive in the Ready Queue
(Ready State) and sort them in ascending order of

their CPU Burst Time (note that this is an imple-
mentation of the Shortest Job First Algorithm).

5. Calculate the mean of the burst times of the pro-
cesses in the ready queue and equate the Quantum

Time(QT) to this value.
6. Sort the processes in the Ready Queue into three
groups based on their Priority - LOW, MEDIUM
and HIGH (note that this is an implementation of
the Priority Algorithm).
7. Check if there is a process in CPU. If there isn’t,
allot the CPU to the first process in the Ready
Queue (i.e, the one with the shortest CPU Burst
Time) - Running State. Assign a new Quantum
Time to this process based on the Priority flag of
this process -
• LOW: QT L = 0.8 ∗ QT
• MEDIUM: QT M = QT
• HIGH: QT H = 1.2 ∗ QT
8. Let this process run for the assigned quantum time

(simultaneously increase the timer) or till the pro-
cess is over. If the process is not completed before

the quantum time is over, then compare the re-
maining CPU Burst Time with the Quantum Time

and if the Quantum Time is greater, then let the

process continue running in the CPU till it com-
pletes itself. However, if the Quantum Time is

lesser than the CPU Burst Time, then send the
process to the Ready Queue and begin again from
Step 5.
9. Once the process is completed, if there is a non-zero
I/O Burst Time, send it to the I/O Queue (Waiting

State) where it will follow FCFS Algorithm. How-
ever, if the I/O Burst Time is zero, then the process

enters the Terminated State.
10. Once the I/O processes are completed, the process
is put back into Ready Queue (Ready State) and
we begin again from Step 5.


![flowchart](https://drive.google.com/file/d/1P7pnzfyw2yirqPf32sPzi3kW3ubsrQq7/view?usp=sharing)