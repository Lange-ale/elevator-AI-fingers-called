from multiprocessing import Process, Queue

class DBSenderEvents(Process):
    def __init__(self, events_queue):
        super().__init__()
        self.events_queue = events_queue

    def run(self):
        while True:
            event = self.events_queue.get(block=True, timeout=None)
            print(event)