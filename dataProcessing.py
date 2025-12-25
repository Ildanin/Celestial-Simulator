from collections.abc import Callable
from multiprocessing import Pipe, Process
from math import sqrt

def subprocess_loop(conn) -> None:
    while True:
        start, batch_size, force_equation, gravity_constant, dataset = conn.recv()
        conn.send(calculate_acceleration(start, batch_size, force_equation, gravity_constant, dataset))

def calculate_acceleration(start, batch_size, force_equation, gravity_constant, dataset) -> tuple[list[float], list[float], list[tuple[int, int]]]:
    X_accelerations: list[float] = [0 for _ in range(len(dataset))]
    Y_accelerations = X_accelerations.copy()
    Collisions: list[tuple[int, int]] = []
    #obj = [x, y, mass, radius]
    for i, obj1 in enumerate(dataset[:batch_size]):
        for j, obj2 in enumerate(dataset[i+1:]):
            distance = sqrt((obj1[0] - obj2[0])**2 + (obj1[1] - obj2[1])**2)
            force = force_equation(gravity_constant, obj1[2], obj2[2], distance)
            first_body_acceleration  = force / obj1[2]
            second_body_acceleration = force / obj2[2]
            radius_vector_x = ((obj1[0] - obj2[0]) / distance)
            radius_vector_y = ((obj1[1] - obj2[1]) / distance)
            X_accelerations[i] -= first_body_acceleration  * radius_vector_x
            Y_accelerations[i] -= first_body_acceleration  * radius_vector_y
            X_accelerations[i+j+1] += second_body_acceleration * radius_vector_x
            Y_accelerations[i+j+1] += second_body_acceleration * radius_vector_y
            if distance < obj1[3] + obj2[3]:
                Collisions.append((i + start, i+j+1 + start))
    for _ in range(start):
        X_accelerations.insert(0, 0)
        Y_accelerations.insert(0, 0)
    return(X_accelerations, Y_accelerations, Collisions)

class Pool:
    def __init__(self, pool_size: int):
        self.pool_size = pool_size
        self.pipes: list = []
        self.processes: list[Process] = []
        self.batching: list[int] = []
        self.dataset_length = -1
    
    def update_batchng(self) -> None:
        batch_size = self.dataset_length * (self.dataset_length - 1) // (2 * self.pool_size)
        self.batching = [0]
        counter = 0
        for n in range(self.dataset_length-1, 0, -1):
            counter += n
            if counter >= batch_size:
                counter = 0
                self.batching.append(self.dataset_length - n)
        if counter != 0:
            self.batching.append(self.dataset_length - 1)
        if len(self.batching) <= self.pool_size:
            for _ in range(self.pool_size - len(self.batching) + 1):
                self.batching.append(self.dataset_length - 1)

    def start(self) -> None:
        for _ in range(self.pool_size):
            parent_conn, child_conn = Pipe()
            self.pipes.append(parent_conn)
            self.processes.append(Process(target=subprocess_loop, args=(child_conn,)))
        for process in self.processes:
            process.start()
    
    def kill(self) -> None:
        for process in self.processes:
            process.kill()

    def send(self, data: tuple[Callable, float, list[tuple[float, float, float, float]]]) -> None:
        force_equation, gravity_constant, dataset = data
        if self.dataset_length != len(dataset):
            self.dataset_length = len(dataset)
            self.update_batchng()
        for i, pipe in enumerate(self.pipes):
            pipe.send((self.batching[i], self.batching[i+1] - self.batching[i], force_equation, gravity_constant, dataset[self.batching[i]:]))

    def recv(self) -> tuple[list[float], list[float], list[tuple[int, int]]]:
        X_accelerations: list[float] = [0 for _ in range(self.dataset_length)]
        Y_accelerations = X_accelerations.copy()
        Collisions: list[tuple[int, int]] = []
        for pipe in self.pipes:
            x_a, y_a, colls = pipe.recv()
            X_accelerations = [a1 + a2 for a1, a2 in zip(X_accelerations, x_a)]
            Y_accelerations = [a1 + a2 for a1, a2 in zip(Y_accelerations, y_a)]
            Collisions += colls
        return(X_accelerations, Y_accelerations, Collisions)
    
    def process(self, data: tuple[Callable, float, list[tuple[float, float, float, float]]]) -> tuple[list[float], list[float], list[tuple[int, int]]]:
        self.send(data)
        return(self.recv())