from multiprocessing import Process
from time import sleep
from random import randint


class ElevatorCaller(Process):
    def __init__(self, calls, ascensore):
        super().__init__()
        self.calls = calls
        
    
    def run(self):
        while True:
            self.calls.put(randint(0, 5))
            sleep(5)