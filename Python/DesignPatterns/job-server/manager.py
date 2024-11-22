from multiprocessing import Lock, Process, Queue
from loguru import logger

import job
import queue
import time


class JobManager(Process):

    def __init__(
        self,
        job_storage,
        job_storage_lock,
        job_queue: Queue,
        result_queue: Queue,
        timeout: int,
    ):
        super(JobManager, self).__init__()

        assert timeout > 0

        self._job_storage = job_storage
        self._job_storage_lock = job_storage_lock
        self._job_queue = job_queue
        self._result_queue = result_queue
        self._timeout = timeout

    def place_jobs_on_queue(self):

        # Find jobs that are new, change their status to pending and place them
        # on the job queue
        for job_id in self._job_storage.keys():

            if self._job_storage[job_id].status == job.NEW:

                # Get the lock on the job storage
                self._job_storage_lock.acquire()

                # Change the status to pending (note that the next three lines
                # ensure the Manager can 'see' the changes to the Job object)
                job_to_process = self._job_storage[job_id]
                job_to_process.status = job.PENDING
                self._job_storage[job_id] = job_to_process

                logger.info(f"Set job {job_id} to PENDING")
                assert self._job_storage[job_id].status == job.PENDING

                # Place the pending job on the queue
                logger.info(f"Placing job {job_id} on the queue")
                self._job_queue.put(self._job_storage[job_id])

                # Release the lock on the job storage
                self._job_storage_lock.release()

    def retrieve_jobs_from_queue(self):
        """Retrieve in-progress or finished jobs from the results queue."""

        try:
            result = self._result_queue.get(block=False)
            assert type(result) == job.Job
            logger.info(f"Received update for job {result.id} (status={result.status})")

            # Get the lock on the job storage
            self._job_storage_lock.acquire()

            # Store the updated job
            self._job_storage[result.id] = result

            # Release the lock on the job storage
            self._job_storage_lock.release()

        except queue.Empty:
            pass

    def run(self):
        while True:
            self.retrieve_jobs_from_queue()
            self.place_jobs_on_queue()
            time.sleep(self._timeout)
