from elevator_motor import ElevatorMotor
from time import time


class Elevator():
    def __init__(self, max_plan, time_switch_plan, time_stop, 
                 pins_motor, send_to_db):
        self.max_plan = max_plan
        self.plan = max_plan
        self.plans_to_go = set()
        self.direction = 0 # 1 = up, -1 = down, 0 = free (no plans to go)
        self.stopped = True
        self.time_switch_plan = time_switch_plan
        self.time_stop = time_stop
        self.time_start_switch_plan = 0
        self.time_start_stop = 0
        self.motor = ElevatorMotor(pins_motor["forward"], pins_motor["backward"])
        self.send_to_db = send_to_db
        self.send_to_db.put({"plan": self.plan, 
                             "direction": self.direction, 
                             "stopped": self.stopped,
                            })


    def call(self, plan):
        self.plans_to_go.add(plan)

    def is_free(self):
        return len(self.plans_to_go) == 0

    def update(self):
        if self.stopped:
            if self.plan in self.plans_to_go:
                self.plans_to_go.remove(self.plan)
            if self.is_free():
                self.direction = 0
                return
            if time() - self.time_start_stop > self.time_stop:
                self.stopped = False
                if self.direction == 0:
                    self.direction = 1 if self.plan < min(self.plans_to_go) else -1
                self.motor.go_up() if self.direction == 1 else self.motor.go_down()

        elif time() - self.time_start_switch_plan > self.time_switch_plan:
            self.time_start_switch_plan = time()
            self.plan += self.direction
            if self.plan in self.plans_to_go:
                self.motor.stop()
                self.time_start_stop = time()
                self.stopped = True
                self.plans_to_go.remove(self.plan)
            
            if self.is_free():
                self.direction = 0
            elif ((self.plan < min(self.plans_to_go) and self.direction == -1)
                 or (self.plan > max(self.plans_to_go) and self.direction == 1)):
                    self.direction *= -1
            
            self.send_to_db.put({"plan": self.plan, 
                                 "direction": self.direction, 
                                 "stopped": self.stopped,
                                })
                