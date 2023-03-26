"""
Coding: UTF-8

Pablo Fernández del Amo.     Práctica 2: Puente Ambite.     Programación Paralela 22/23.
"""


from multiprocessing import Process, Condition, Lock, Value, current_process
import time, random


NCars_N = 16
NCars_S = 12
N_Ped= 10

def delay(d=4):
    time.sleep(random.random()/d)

    
class Monitor():
    def __init__(self):
        """
        Initialize the monitor object with all necessary variables.
        """

        # Number of cars heading south
        self.ncars_south = Value('i', 0)

        # Number of cars heading north
        self.ncars_north = Value('i', 0)

        # Number of pedestrians waiting to cross the street
        self.npedestrians = Value('i', 0)

        # Number of cars waiting to cross the street from south
        self.ncars_south_waiting = Value('i', 0)

        # Number of cars waiting to cross the street from north
        self.ncars_north_waiting = Value('i', 0)

        # Number of pedestrians waiting to cross the street
        self.npedestrians_waiting = Value('i', 0)

        # Current turn: 0 for cars heading north, 1 for cars heading south, 2 for pedestrians
        self.turn = Value('i', 0)

        # Mutex lock to synchronize access to shared variables
        self.mutex = Lock()

        # Condition variables for each direction and pedestrians
        self.oktoN = Condition(self.mutex)
        self.oktoS = Condition(self.mutex)
        self.oktoP = Condition(self.mutex)

    def are_no_rest(self, direction):
        """
        Check if there are no restrictions for a given direction.

        Args:
            direction: A string representing the direction (N, S, P).

        Returns:
            True if there are no restrictions, False otherwise.
        """
        if direction == 'N':
            # North direction
            return self.ncars_south.value == 0 and self.npedestrians.value == 0 and \
                (self.turn.value == 0 or (self.ncars_south_waiting.value == 0 and self.npedestrians_waiting.value == 0))
        elif direction == 'S':
            # South direction
            return self.ncars_north.value == 0 and self.npedestrians.value == 0 and \
                (self.turn.value == 1 or (self.ncars_north_waiting.value == 0 and self.npedestrians_waiting.value == 0))
        else:
            # Pedestrians
            return self.ncars_north.value == 0 and self.ncars_south.value == 0 and \
                (self.turn.value == 2 or (self.ncars_south_waiting.value == 0 and self.ncars_north_waiting.value == 0))

    def wantN_cross(self):
        """
        Method called by a car heading north that wants to cross the intersection
        """
        self.mutex.acquire()  # Acquire the mutex to ensure exclusive access to shared variables
        self.ncars_north_waiting.value += 1  # Increase the number of cars waiting to cross
        self.oktoN.wait_for(lambda: self.are_no_rest('N'))  # Wait until it's safe for the car to cross
        self.ncars_north_waiting.value -= 1  # Decrease the number of cars waiting to cross
        self.ncars_north.value += 1  # Increase the number of cars that have crossed
        self.mutex.release()  # Release the mutex

    def wantS_cross(self):
        """
        Method called by a car heading south that wants to cross the intersection
        """
        self.mutex.acquire()  # Acquire the mutex to ensure exclusive access to shared variables
        self.ncars_south_waiting.value += 1  # Increase the number of cars waiting to cross
        self.oktoS.wait_for(lambda: self.are_no_rest('S'))  # Wait until it's safe for the car to cross
        self.ncars_south_waiting.value -= 1  # Decrease the number of cars waiting to cross
        self.ncars_south.value += 1  # Increase the number of cars that
        self.mutex.release()

    def wantP_cross(self):
        self.mutex.acquire() # Acquire the mutex to ensure exclusive access to shared variables
        self.npedestrians_waiting.value += 1 # Increase the number of waiting pedestrians
        self.oktoP.wait_for(lambda: self.are_no_rest('P')) # Wait for the intersection to be free of any cars
        self.npedestrians_waiting.value -= 1
        self.npedestrians.value += 1 # Decrease the number of waiting pedestrians and increase the number of pedestrians crossing
        self.mutex.release()    # Release the mutex

    def exitN(self):
        """
        Decrements the number of cars waiting to cross from the north direction and updates the turn value based on the 
        number of cars waiting from the south direction. If there are no cars waiting to cross from the north direction,
        notifies all pedestrians and cars from the south and pedestrian directions that they can cross.
        """
        self.mutex.acquire()
        self.ncars_north.value -= 1
        if self.ncars_south_waiting.value > 0: 
            self.turn.value = 1
        else:
            self.turn.value = 2
        if self.ncars_north.value == 0:
            self.oktoS.notify_all()
            self.oktoP.notify_all()
        self.mutex.release()

    def exitS(self):
        """
        Decrements the number of cars waiting to cross from the south direction and updates the turn value based on the 
        number of pedestrians waiting to cross. If there are no cars waiting to cross from the south direction, waits for a
        delay and then notifies all pedestrians and cars from the north and pedestrian directions that they can cross.
        """
        self.mutex.acquire()
        self.ncars_south.value -= 1
        if self.npedestrians_waiting.value > 0: 
            self.turn.value = 2
        else:
            self.turn.value = 0
        if self.ncars_south.value == 0:
            delay()
            self.oktoP.notify_all()
            self.oktoN.notify_all()
        self.mutex.release()

    def exitP(self):
        """
        Decrements the number of pedestrians waiting to cross and updates the turn value based on the number of cars
        waiting to cross from the north direction. If there are no pedestrians waiting to cross, waits for a delay and then
        notifies all pedestrians and cars from the north and south directions that they can cross.
        """
        self.mutex.acquire()
        self.npedestrians.value -= 1
        if self.ncars_north_waiting.value > 0: 
            self.turn.value = 0
        else:
            self.turn.value = 1
        if self.npedestrians.value == 0:
            delay()
            self.oktoN.notify_all()
            self.oktoS.notify_all()
        self.mutex.release()

    def __str__(self):
        """
        CS -> Cars crossing the bridge heading south.
        CN -> Cars crossing th ebridge heading north.
        P -> Pedestrians crossing the bridge.
        When a 'w' is added at the end, represents the waiting ones.
        """
        return f"CS:{self.ncars_south.value}, CN:{self.ncars_north.value}, P:{self.npedestrians.value}, CSW:{self.ncars_south_waiting.value}, CNW:{self.ncars_north_waiting.value}, PW:{self.npedestrians_waiting.value}"

def delay(d=3):
    time.sleep(random.random()/d)
def delay_car():
    time.sleep(random.randrange(2, 4)/2)
def delay_pedestrian():
    time.sleep(random.randrange(2, 3))

def car_N(monitor):
    delay()
    print(f"Car heading north {current_process().name} requests to cross. Monitor state: {monitor}")
    monitor.wantN_cross()
    print(f"Car heading north {current_process().name} crossing. Monitor state: {monitor}")
    delay_car()
    print(f"Car heading north {current_process().name} exits. Monitor state: {monitor}")
    monitor.exitN()
    print(f"Car heading north {current_process().name} exited. Monitor state: {monitor}")

def car_S(monitor):
    delay()
    print(f"CarS {current_process().name} requests to cross. Monitor state: {monitor}")
    monitor.wantS_cross()
    print(f"CarS {current_process().name} crossing. Monitor state: {monitor}")
    delay_car()
    print(f"CarS {current_process().name} exits. Monitor state: {monitor}")
    monitor.exitS()
    print(f"CarS {current_process().name} exited. Monitor state: {monitor}")

def pedestrian(monitor):
    delay()
    print(f"Pedestrian {current_process().name} requests to cross. Monitor state: {monitor}")
    monitor.wantP_cross()
    print(f"Pedestrian {current_process().name} crossing. Monitor state: {monitor}")
    delay_pedestrian()
    print(f"Pedestrian {current_process().name} exits. Monitor state: {monitor}")
    monitor.exitP()
    print(f"Pedestrian {current_process().name} exited. Monitor state: {monitor}")
    

def main():

    monitor = Monitor()
    # Create processes for cars coming from the north
    carN = [Process(target=car_N, name=f"N{i}", args=(monitor,)) \
            for i in range(NCars_N)]
    # Create processes for cars coming from the south
    carS = [Process(target=car_S, name=f"S{i}", args=(monitor,)) \
            for i in range(NCars_S)]
    # Create processes for pedestrians
    pedestrians = [Process(target=pedestrian, name=f"P{i}", args=(monitor,)) \
            for i in range(N_Ped)]

    # Start all processes in the simulation
    for x in carS + pedestrians + carN:
        x.start()
    # Wait for all processes to finish before exiting the simulation
    for x in carS + pedestrians + carN:
        x.join()


if __name__ == '__main__':
    main()
