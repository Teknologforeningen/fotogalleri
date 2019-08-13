from django.conf.settings import THUMB_QUEUE_THREAD_COUNT
from queue import Queue, Full
from threading import Thread


class _ThumbWorker():
    def __init__(self, thumb_queue):
        self._queue = thumb_queue
        self._pool = []

    def work(self):
        while True:
            image_obj = self._queue.get()

            # None indicates that the thread should die
            if image_obj is None:
                break

            # TODO: add actual thumbnail generation
            self._queue.task_done()

    def add(self, work):
        self._pool.append(work)

    def stop(self):
        for thread in self._pool:
            thread.join()


class ThumbQueue():
    _THUMB_QUEUE = Queue()
    _WORKER = _ThumbWorker(_THUMB_QUEUE)

    for _ in range(THUMB_QUEUE_THREAD_COUNT):
        thread = Thread(target=_WORKER.work)
        thread.start()
        _WORKER.add(thread)

    @staticmethod
    def add_image_obj(image_obj):
        try:
            ThumbQueue._THUMB_QUEUE.put_nowait(image_obj)
        except Full:
            # TODO: log or raise an exception in case of error
            pass

    @staticmethod
    def is_empty():
        return ThumbQueue._THUMB_QUEUE.empty()

    @staticmethod
    def stop():
        ThumbQueue._THUMB_QUEUE.join()

        # Notify threads in thread-pool in _WORKER of death
        for _ in range(THUMB_QUEUE_THREAD_COUNT):
            ThumbQueue._THUMB_QUEUE.put(None)

        ThumbQueue._WORKER.stop()
