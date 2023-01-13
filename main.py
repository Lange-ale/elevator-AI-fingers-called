from elevator import Elevator
from elevator_caller import ElevatorCaller
from db_sender_events import DBSenderEvents
from multiprocessing import Queue

max_plan = 5
time_switch_plan = 2
time_stop = 5
pins_motor = {"forward": 17, "backward": 18}

if __name__ == "__main__":
    send_to_db = Queue()
    calls = Queue()
    elevator = Elevator(max_plan, time_switch_plan, time_stop, pins_motor, send_to_db)
    elevator_caller = ElevatorCaller(calls, elevator)
    db_sender_events = DBSenderEvents(send_to_db)
    elevator_caller.start()
    db_sender_events.start()
    
    while True:
        elevator.update()
        if not calls.empty():
            elevator.call(calls.get())
            print("call", elevator.plans_to_go)
        