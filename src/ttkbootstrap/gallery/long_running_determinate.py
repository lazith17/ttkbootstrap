from queue import Queue
from random import randint
from threading import Thread
from time import sleep
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialog import messagebox


class Application(ttk.Application):

    def __init__(self):
        super().__init__(title='Long Running - Determinate', theme='lumen')

        self.lr = LongRunning(self)
        self.lr.pack(fill=BOTH, expand=YES, padx=10, pady=10)


class LongRunning(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(padding=20)
        self.task_queue = Queue()

        # instructions
        lbl = ttk.Label(self, text="Click the START button to begin a long-running task that will last approximately 5 and 10 seconds", wraplength=275, justify=LEFT)
        lbl.pack(fill=X)

        # start button
        self.btn = ttk.Button(self, text="START", command=self.start_task)
        self.btn.pack(pady=(5, 10))

        # determinate progress bar (for know number of steps)
        self.progressbar = ttk.Progressbar(self, maximum=10, style=INFO)
        self.progressbar.pack(fill=X)

    def simulated_blocking_io_task(self, thread_num):
        """A simulated IO operation to run for a random time interval between 5 and 10 seconds"""
        seconds_to_run = randint(5, 15)
        sleep(seconds_to_run)
        self.task_queue.task_done()
        print('Finished task on Thread:', thread_num)

    def start_task(self):
        """Start the progressbar and run the task in another thread"""
        self.btn.configure(state=DISABLED)
        for i in range(1, 11):
            self.task_queue.put(Thread(target=self.simulated_blocking_io_task, args=[i], daemon=True).start())
        self.listen_for_complete_task()

    def listen_for_complete_task(self):
        """Check to see if task is complete; if so, stop the progressbar and show and alert"""
        if self.task_queue.unfinished_tasks == 0:
            self.progressbar.value = 10
            messagebox.showinfo(parent=self, title='alert', message="process complete")
            self.btn.configure(state=NORMAL)
            return
        tasks_completed = self.progressbar.maximum - self.task_queue.unfinished_tasks
        self.progressbar.value = tasks_completed
        self.after(500, self.listen_for_complete_task)


if __name__ == '__main__':
    Application().run()
