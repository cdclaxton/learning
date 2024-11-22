from flask import Flask, request
from multiprocessing import Lock, Manager, Queue
from loguru import logger

from job import Job
from manager import JobManager
from worker import TranslationWorker


app = Flask(__name__)

manager = Manager()
job_storage = manager.dict()
job_storage_lock = Lock()


@app.route("/submit", methods=["POST"])
def submit():

    # Extract the job configuration from the request's JSON body
    job_data = request.get_json()
    source = job_data.get("source", None)
    target = job_data.get("target", None)
    text = job_data.get("text", None)

    # Check the JSON is valid
    if source is None or target is None or text is None:
        return "Invalid job config", 400

    # Create the Job object
    new_job = Job(source, target, text)

    # Add the job to the job storage
    job_storage_lock.acquire()
    logger.info(f"Created new job {new_job.id}")
    job_storage[new_job.id] = new_job
    job_storage_lock.release()

    # Return the job ID
    return new_job.id


@app.route("/job/<id>", methods=["GET"])
def get_job(id):

    # Try to retrive the job given its ID from the job storage
    job_storage_lock.acquire()
    fetched_job = job_storage.get(id, None)
    job_storage_lock.release()

    # Return a response based on whether the job could be found
    if fetched_job is None:
        return "Job not found", 404
    else:
        return fetched_job.to_dict()


if __name__ == "__main__":

    timeout = 1
    min_delay = 2
    max_delay = 10

    # Make the two queues
    job_queue = Queue()
    result_queue = Queue()

    # Make and start the Manager process
    job_manager = JobManager(
        job_storage, job_storage_lock, job_queue, result_queue, timeout
    )
    job_manager.start()

    # Make and start the Translation Worker process
    worker = TranslationWorker(job_queue, result_queue, min_delay, max_delay)
    worker.start()

    # Run the API
    app.run()
