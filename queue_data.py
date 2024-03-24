# -*- config: utf8 -*-
import random
import time
from collections import defaultdict
import threading
import queue


class Table:

    def __init__(self, number):
        self.number = number
        self.is_busy = True


class Cafe:

    def __init__(self, tables):
        super().__init__()
        self.queue = queue.Queue(maxsize=2)
        self.tables = tables
        self.table = None
        self.list_thread = []

    def serve_customer(self, customer):
        # Поиск свободного стола
        for table in self.tables:
            if table.is_busy:
                self.table = table
                break
        # Запуск потока посетителя, если есть свободный стол
        if self.table is not None and self.table.is_busy is True:
            custom = Customer(customer=customer, table=self.table, queue=self.queue, list_thread=self.list_thread)
            self.list_thread.append(custom)
            custom.start()
        else:
            self.queue.put(customer)
            print(f'Посетитель номер {customer} ожидает свободный стол')

    def customer_arrival(self):
        for visitor in range(1, 21):
            print(f'Посетитель номер {visitor} прибыл')
            self.serve_customer(customer=visitor)
            time.sleep(1)
        for item_thread in self.list_thread:
            item_thread.join()


class Customer(threading.Thread):

    def __init__(self, customer, table, queue, list_thread):
        super().__init__()
        self.customer = customer
        self.table = table
        self.queue = queue
        self.list_thread = list_thread

    def run(self):
        # Обслуживание посетителя
        self.table.is_busy = False
        print(f'Посетитель номер {self.customer} сел за стол {self.table.number}')
        time.sleep(5)
        print(f'Посетитель номер {self.customer} покушал и ушёл')
        self.table.is_busy = True
        # Запуск потока посетителя, если освобождается стол
        late_customer = self.queue.get()
        self.table.is_busy = False
        custom = Customer(customer=late_customer, table=self.table, queue=self.queue, list_thread=self.list_thread)
        self.list_thread.append(custom)
        custom.start()


table1 = Table(1)
table2 = Table(2)
table3 = Table(3)

global_tables = [table1, table2, table3]

cafe = Cafe(global_tables)

customer_arrival_threads = threading.Thread(target=cafe.customer_arrival)

customer_arrival_threads.start()

customer_arrival_threads.join()

