from statistics import mean
from typing import List, Dict

class SchedulingAlgorithm:
	_timeline = 0 
	_average_time = {}
	io_time=0
	def __init__(self, dataset: List[Dict]):
		self._dataset: List[Dict] = dataset 

	def _non_preemptive_execution(self):

		for i,p in enumerate(self._dataset):
			self._dataset[i].update({'response_time': self._timeline}) ##time taken for CPU to respond stored
			self._dataset[i].update({'waiting_time': self._timeline}) ##complete waiting time for the process stored
			#print(self.io_burst_calc(self,i))
			if (self.io_burst_calc(self,i)<self._timeline):	
				self._timeline += self._dataset[i]['cpu_burst']
				self._dataset[i]['io_burst']=0 
				self._dataset[i]['turnaround_time']= self._timeline -self._dataset[i]['arrival_time']##process completion time stored
			else:
				self._timeline=self._timeline+self._dataset[i]['io_burst']+self._dataset[i]['cpu_burst']
				self._dataset[i]['io_burst']=0 
				self._dataset[i]['turnaround_time']= self._timeline -self._dataset[i]['arrival_time']

		self._average_time = {
            'response_time': mean([t['response_time'] for t in self._dataset]),
            'waiting_time': mean([t['waiting_time'] for t in self._dataset]),
            'turnaround_time': mean([t['turnaround_time'] for t in self._dataset]),
        }
		return sorted(self._dataset, key=lambda t: t['process']), self._average_time

	def fcfs(self):
		self._dataset = sorted(self._dataset, key=lambda t: t['arrival_time'])
		return self._non_preemptive_execution()

	def sjfs(self):
		self._dataset = sorted(self._dataset, key=lambda t: (t['arrival_time'], t['cpu_burst']))
		return self._non_preemptive_execution()

	def priority(self):
		self._dataset = sorted(self._dataset, key=lambda t: (t['arrival_time'], t['priority']))
		return self._non_preemptive_execution()

	def io_burst_calc(self,n, i):
		self.io_time = self.io_time + self._dataset[i]['io_burst']	
		return self.io_time

if __name__ == '__main__':dataset1 = [
		{'process': '0', 'cpu_burst': 21,'io_burst': 5, 'arrival_time': 1, 'priority': 2},
		{'process': '1', 'cpu_burst': 24,'io_burst': 2, 'arrival_time': 1, 'priority': 3},
		{'process': '2', 'cpu_burst': 34,'io_burst': 2, 'arrival_time': 1, 'priority': 2},
		{'process': '3', 'cpu_burst': 12,'io_burst': 7, 'arrival_time': 1, 'priority': 2},
        {'process': '4', 'cpu_burst': 15,'io_burst': 2, 'arrival_time': 2, 'priority': 3},
	]

scheduling_algorithm = SchedulingAlgorithm(dataset=dataset1)
updated, average_time = scheduling_algorithm.fcfs() ##updated dataset and average_time are return values 

#updated_dateset, average_time = scheduling_algorithm.sjfs()

#updated, average_time = scheduling_algorithm.priority()
print('Priority Scheduling')
print('Average:', average_time)
print()