from statistics import mean
from typing import List, Dict

class SchedulingAlgorithm:
	_timeline = 0 
	_average_time = {}
	io_time=0
	def __init__(self, dataset: List[Dict]):
		self._dataset: List[Dict] = dataset 

	def round_robin(self, time_quantum: int = 4):
		self._timeline = 0
		self._dataset = sorted(self._dataset, key=lambda t: t['arrival_time'])
		process_list = [p['cpu_burst'] for p in self._dataset]

		while (1):
			done=True
			for i, p in enumerate(process_list):
				if(process_list[i]==self._dataset[i]['cpu_burst']):
					self._dataset[i]['response_time']=self._timeline

				if (process_list[i]> 0):
					done=False
				
					if process_list[i]>time_quantum:
						self._timeline=self._timeline+time_quantum
						process_list[i]=process_list[i]-time_quantum
					else:
						#self._timeline=self._timeline+process_list[i]
						process_list[i]=0
						self._dataset[i]['waiting_time']=self._timeline - self._dataset[i]['cpu_burst'] - self._dataset[i]['arrival_time']
						
						if (self.io_burst_calc(self,i)<self._timeline):	
							self._timeline += process_list[i]
							self._dataset[i]['io_burst']=0 
							self._dataset[i]['turnaround_time']= self._timeline -self._dataset[i]['arrival_time']##process completion time stored
						else:
							self._timeline=self._timeline+self._dataset[i]['io_burst']+process_list[i]
							self._dataset[i]['io_burst']=0 
							self._dataset[i]['turnaround_time']= self._timeline -self._dataset[i]['arrival_time']

			if(done==True):
				break

		self._average_time = {
			'response': mean([t['response_time'] for t in self._dataset]),
			'turnaround': mean([t['turnaround_time'] for t in self._dataset]),
			'waiting': mean([t['waiting_time'] for t in self._dataset]),
				
			}
		return sorted(self._dataset, key=lambda t: t['process']), self._average_time

	def io_burst_calc(self,n, i):
		self.io_time = self.io_time + self._dataset[i]['io_burst']	
		return self.io_time


if __name__ == '__main__':dataset1 = [
		{'process': '0', 'cpu_burst': 21,'io_burst': 12, 'arrival_time': 3, 'priority': 2},
		{'process': '1', 'cpu_burst': 11,'io_burst': 9, 'arrival_time': 0, 'priority': 3},
		{'process': '2', 'cpu_burst': 5,'io_burst': 4, 'arrival_time': 4, 'priority': 1},
		{'process': '3', 'cpu_burst': 3,'io_burst': 3, 'arrival_time': 3, 'priority': 2},
		{'process': '4', 'cpu_burst': 25,'io_burst': 14, 'arrival_time': 1, 'priority': 2},
	]

scheduling_algorithm = SchedulingAlgorithm(dataset=dataset1)
updated_dateset, average_time = scheduling_algorithm.round_robin()
print('Round Robin Scheduling')
print('Average:', average_time)
print() 