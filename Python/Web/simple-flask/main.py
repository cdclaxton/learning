import random
import time

from flask import Flask, redirect, url_for, session
from threading import Thread
from queue import Queue

app = Flask(__name__)
app.secret_key = "super secret key"

num_workers = 2

class Worker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
    
    def run(self):
        item = self.queue.get(block=True)
        print(f"Got: {item}")
        time.sleep(10)
        print(f"Finished: {item}")        

# Make the queue
q = Queue()

# Start the workers
workers = [Worker(q) for _ in range(num_workers)]
for idx, worker in enumerate(workers):
    print(f"Starting worker {idx}")
    workers[idx].daemon = True
    workers[idx].start()

@app.route("/")
def index():
    r = random.randint(0, 100)
    q.put(r)

    session['r'] = r

    #return redirect(url_for('waiting'))
    return redirect("/waiting")

@app.route("/waiting")
def waiting():
    r = session.get('r', None)
    return f"Hello from waiting ... ({r})"

app.run(host='0.0.0.0', port=5000)