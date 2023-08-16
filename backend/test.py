from Othello.game_info_functions import *
import time
import cProfile
import threading

counter = 0

def increment_counter():
    global counter
    temp = counter
    temp += 1
    counter = temp


thread1 = threading.Thread(target=increment_counter)
thread2 = threading.Thread(target=increment_counter)

thread1.start()
thread2.start()

thread1.join()
thread2.join()

a = thread1+thread2
print(a)