import os
import random
import time
from multiprocessing import Process, Queue
from loguru import logger

import job


class TranslationWorker(Process):
    gpu_filepath = "./gpu.txt"

    def __init__(
        self, job_queue: Queue, result_queue: Queue, min_delay: int, max_delay: int
    ):
        super(TranslationWorker, self).__init__()

        assert min_delay > 0 and max_delay > min_delay

        self._job_queue = job_queue
        self._result_queue = result_queue

        self._min_delay = min_delay
        self._max_delay = max_delay

    def perform_translate(self, job_to_run: job.Job) -> job.Job:
        """Simulate performing an expensive translation job on a GPU."""

        assert (
            job_to_run.status == job.PENDING
        ), f"Job status: {job_to_run.status}, expected PENDING"
        assert job_to_run.output is None

        # Set the job status to in progress
        job_to_run.status = job.INPROGRESS
        self._result_queue.put(job_to_run)
        logger.info(f"Set job {job_to_run.id} to IN PROGRESS")

        # A file acts as a proxy for a system resource, i.e. the GPU
        with open(TranslationWorker.gpu_filepath, "w") as fp:
            delay = random.randint(self._min_delay, self._max_delay)
            time.sleep(delay)
            job_to_run.output = job_to_run.text.upper()
            job_to_run.status = job.COMPLETE
            logger.info(f"Set job {job_to_run.id} to COMPLETE")

        os.remove(TranslationWorker.gpu_filepath)

        return job_to_run

    def run(self):
        while True:
            job = self._job_queue.get()
            processed_job = self.perform_translate(job)
            self._result_queue.put(processed_job)
