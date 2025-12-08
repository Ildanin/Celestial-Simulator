from multiprocessing import Pipe, Process
from math import sqrt
import time

def dist_func(conn, force_equation):
    while True:
        results = []
        batch_size, data_list = conn.recv()
        for i, coord1 in enumerate(data_list[:batch_size]):
            intermidiate_results = []
            for coord2 in data_list[i+1:]:
                intermidiate_results.append(sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2))
            results.append(intermidiate_results)
        conn.send(results)

class Pool:
    def __init__(self, pool_size: int):
        self.pool_size = pool_size
        self.pipes = []
        self.processes = []
    
    def start(self, force_equation):
        for _ in range(self.pool_size):
            parent_conn, child_conn = Pipe()
            self.pipes.append(parent_conn)
            self.processes.append(Process(target=dist_func, args=(child_conn, force_equation)))
        for process in self.processes:
            process.start()
    
    def kill(self):
        for process in self.processes:
            process.kill()
    
    def send(self, dataset):
        batch_size = len(dataset) // self.pool_size
        for i, pipe in enumerate(self.pipes[:-1]):
            pipe.send((batch_size, dataset[(i * batch_size):]))
        self.pipes[-1].send((batch_size + len(dataset) % self.pool_size, dataset[((self.pool_size - 1) * batch_size):]))

    def recv(self):
        processed_data =[]
        for pipe in self.pipes:
            processed_data += pipe.recv()
        return(processed_data)
    
    def process(self, dataset):
        self.send(dataset)
        return(self.recv())