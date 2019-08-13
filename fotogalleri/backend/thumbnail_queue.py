from django.conf.settings import THUMB_QUEUE_THREAD_COUNT
import queue
import threading
import time


class _ThumbWorker():
    def __init__(self, thumb_queue):
        self._queue = thumb_queue
        self._pool = []

    def work(self):
        while True:
            image_obj = self._queue.get()

            if image_obj is None:
                break

            # TODO: add actual thumbnail generation
            self._queue.task_done()

    def append(self, work):
        self._pool.append(work)

    def stop(self):
        for thread in self._pool:
            thread.join()


class ThumbQueue():
    _THUMB_QUEUE = queue.Queue(maxsize=THUMB_QUEUE_THREAD_COUNT)
    worker = _ThumbWorker(_THUMB_QUEUE)

    for _ in range(THUMB_QUEUE_THREAD_COUNT):
        thread = threading.Thread(target=worker.work)
        thread.start()
        worker.append(thread)

    @staticmethod
    def add_image_obj(image_obj):
        ThumbQueue._THUMB_QUEUE.put(image_obj)

    @staticmethod
    def stop():
        ThumbQueue._THUMB_QUEUE.join()

        for _ in range(THUMB_QUEUE_THREAD_COUNT):
            ThumbQueue._THUMB_QUEUE.put(None)

        ThumbQueue.worker.stop()