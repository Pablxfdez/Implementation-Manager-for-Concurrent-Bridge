import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value

SOUTH = 1
NORTH = 0

NCARS = 8
NPED = 7
TIME_CARS = 0.5  # a new car enters each 0.5s
TIME_PED = 5 # a new pedestrian enters each 5s
TIME_IN_BRIDGE_CARS = (1, 0.5) # normal 1s, 0.5s
TIME_IN_BRIDGE_PEDESTRIAN = (30, 10) # normal 1s, 0.5s

class Monitor():
    def __init__(self):
        self.mutex = Lock()
        self.patata = Value('i', 0)
        
        self.npedestrians = Value('i', 0)
        self.ncars_north = Value('i', 0)
        self.ncars_south = Value('i', 0)
        
        self.oktoN = Condition(self.mutex)
        self.oktoS = Condition(self.mutex)
        self.oktoP = Condition(self.mutex)

 
    
    def okpedestrians(self):
        return (self.ncars_north.value == 0) and (self.ncars_south.value == 0)
    
    def okcarsnorth(self):
        return (self.npedestrians.value == 0) and (self.ncars_south.value == 0)
    
    def okcarsnorth(self):
        return (self.npedestrians.value == 0) and (self.ncars_north.value == 0)
    

    def wants_enter_car(self, direction: int) -> None:
        self.mutex.acquire()
        self.patata.value += 1
        
        if direction == NORTH:
            self.oktoN.wait_for(self.okcarsnorth)
            self.ncars_north.value += 1
        else:
            self.oktoS.wait_for(self.okcarsnorth)
            self.ncars_south.value += 1
        
        self.mutex.release()

    def leaves_car(self, direction: int) -> None:
        self.mutex.acquire() 
        self.patata.value += 1
        if direction == NORTH:
            self.ncars_north.value -= 1
            
            if self.ncars_north.value == 0:
                self.oktoS.notify_all()
                self.oktoP.notify_all()                    
        else:
            self.ncars_south.value -= 1
            if self.ncars_south.value == 0:
                self.oktoN.notify_all()
                self.oktoP.notify_all()  
        self.mutex.release()
        

    def wants_enter_pedestrian(self) -> None:
        self.mutex.acquire()
        self.patata.value += 1
        self.oktoP.wait_for(self.okpedestrians)
        self.npedestrians.value += 1
        self.mutex.release()

    def leaves_pedestrian(self) -> None:
        self.mutex.acquire()
        self.patata.value += 1
        self.npedestrians.value -= 1

        if self.npedestrians.value == 0:
            self.oktoN.notify_all()
            self.oktoS.notify_all() 
            
        self.mutex.release()

    def __repr__(self) -> str:
        return f'Monitor: {self.patata.value}'

def delay_car_north(factor = 2) -> None:
    time.sleep(random.random()/factor)

def delay_car_south(factor = 2)-> None:
    time.sleep(random.random()/factor)

def delay_pedestrian(factor = 1) -> None:
    time.sleep(random.random()/factor)

def car(cid: int, direction: int, monitor: Monitor)  -> None:
    print(f"car {cid} heading {direction} wants to enter. {monitor}")
    monitor.wants_enter_car(direction)
    print(f"car {cid} heading {direction} enters the bridge. {monitor}")
    if direction==NORTH :
        delay_car_north()
    else:
        delay_car_south()
    print(f"car {cid} heading {direction} leaving the bridge. {monitor}")
    monitor.leaves_car(direction)
    print(f"car {cid} heading {direction} out of the bridge. {monitor}")

def pedestrian(pid: int, monitor: Monitor) -> None:
    print(f"pedestrian {pid} wants to enter. {monitor}")
    monitor.wants_enter_pedestrian()
    print(f"pedestrian {pid} enters the bridge. {monitor}")
    delay_pedestrian()
    print(f"pedestrian {pid} leaving the bridge. {monitor}")
    monitor.leaves_pedestrian()
    print(f"pedestrian {pid} out of the bridge. {monitor}")



def gen_pedestrian(monitor: Monitor) -> None:
    pid = 0
    plst = []
    for _ in range(NPED):
        pid += 1
        p = Process(target=pedestrian, args=(pid, monitor))
        p.start()
        plst.append(p)
        time.sleep(random.expovariate(1/TIME_PED))

    for p in plst:
        p.join()

def gen_cars(monitor) -> Monitor:
    cid = 0
    plst = []
    for _ in range(NCARS):
        direction = NORTH if random.randint(0,1)==1  else SOUTH
        cid += 1
        p = Process(target=car, args=(cid, direction, monitor))
        p.start()
        plst.append(p)
        time.sleep(random.expovariate(1/TIME_CARS))

    for p in plst:
        p.join()

def main():
    monitor = Monitor()
    gcars = Process(target=gen_cars, args=(monitor,))
    gped = Process(target=gen_pedestrian, args=(monitor,))
    gcars.start()
    gped.start()
    gcars.join()
    gped.join()


if __name__ == '__main__':
    main()