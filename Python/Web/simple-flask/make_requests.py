import requests
from threading import Thread


class WorkerThread(Thread):
    def __init__(self, url):
        Thread.__init__(self)
        self.url = url
    
    def run(self):
        print(f"Sending request to {url}")
        response = requests.get(url)
        print(f"Response: {response}")

if __name__ == '__main__':

    num_requests = 20
    url = "http://localhost:5000/"

    workers = [WorkerThread(url) for _ in range(num_requests)]
    for idx in range(num_requests):
        workers[idx].daemon = True
        workers[idx].start()

    for w in workers:
        w.join()

    print("Finished")