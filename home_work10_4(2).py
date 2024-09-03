import queue
import threading
from threading import Thread
import random
import time
from queue import Queue

class Table:
    def __init__(self, number, guest=None):
        self.number = number
        self.guest = guest
class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
    def run(self):
        time.sleep(random.randint(3, 10))
class Cafe:
    def __init__(self, *tables):
        self.tables = tables
        self.queue = queue.Queue()
    def guest_arrival(self, *guests):
        self.guests = list(guests)
        [setattr(x, 'guest', y.name) for x, y in zip(self.tables, self.guests) if x.guest == None]
        self.thread_guest = self.guests[:len(self.tables)]
        self.queve_guest = self.guests[len(self.tables):]
        for x in self.thread_guest:
            table_occupy = next(filter(lambda y: y.guest == x.name, self.tables), None)
            print(f'{x.name} сел(-а) за стол номер {table_occupy.number}')
            thguest = x
            thguest.start()
        for x in self.queve_guest:
            self.queue.put(x)
            print(f'{x.name} в очереди')
    def discuss_guests(self):
        while self.thread_guest:
            for x in self.thread_guest:
                if not x.is_alive():
                    free_table = next(filter(lambda y: y.guest == x.name, self.tables), None)
                    print(f'{x.name} покушал(-а) и ушёл(ушла)')
                    print(f'Стол номер  свободен {free_table.number}')
                    self.thread_guest.remove(x)
                    free_table.guest = None
                    if not self.queue.empty():
                        wait_guest = self.queue.get()
                        free_table.guest = wait_guest.name
                        self.thread_guest.append(wait_guest)
                        thguest = next(filter(lambda y: y.name == wait_guest.name, self.guests), None)
                        thguest.start()
                        print(f'{thguest.name} вышел(-ла) из очереди и сел(-а) за стол {free_table.number}')




# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
cafe.discuss_guests()
