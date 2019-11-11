from django.conf import settings
from queue import Queue, Full
from threading import Thread
from backend.thumbnail.thumbnail_queue_image_object import ThumbQueueImageObject
from logging import getLogger


logger = getLogger(__name__)


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

            try:
                image_obj.generate_image_thumbnails()
            # TODO: add specific exception
            except Exception as error:
                logger.error('Could not generate thumbnail for {}, reason: {}'.format(image_obj.get_full_image_path(),
                                                                                      error))
            finally:
                self._queue.task_done()

    def add(self, work):
        self._pool.append(work)

    def stop(self):
        for thread in self._pool:
            thread.join()


class ThumbQueue():
    _THUMB_QUEUE = Queue()
    _WORKER = _ThumbWorker(_THUMB_QUEUE)

    for _ in range(settings.THUMB_QUEUE_THREAD_COUNT):
        thread = Thread(target=_WORKER.work)
        thread.setDaemon(True)
        thread.start()
        _WORKER.add(thread)

    @staticmethod
    def add_image_obj(image_obj):
        '''
        Add an ThumbQueueImageObject object to the queue.
        :param image_obj: type ThumbQueueImageObject
        '''
        try:
            ThumbQueue._THUMB_QUEUE.put_nowait(image_obj)
        except Full:
            logger.error('ThumbQueue FULL, not able to append new task: {}'.format(image_obj))
            # TODO: update image object for noting failed thumbnail generation

    @staticmethod
    def add_image_metadata(image_metadata):
        '''
        Add an ImageMetadata object to the queue after creating ThumbQueueImageObject based on it.
        :param image_metadata: type ImageMetadata
        '''
        image_obj = ThumbQueueImageObject(image_metadata)
        ThumbQueue.add_image_obj(image_obj)

    @staticmethod
    def is_empty():
        return ThumbQueue._THUMB_QUEUE.empty()

    @staticmethod
    def stop():
        ThumbQueue._THUMB_QUEUE.join()

        # Notify threads in thread-pool in _WORKER of death
        for _ in range(settings.THUMB_QUEUE_THREAD_COUNT):
            ThumbQueue._THUMB_QUEUE.put(None)

        ThumbQueue._WORKER.stop()
