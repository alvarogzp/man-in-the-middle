import threading

from mitm.config import KILL_THREADS_WHEN_MAIN_ENDS


class Thread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Thread, self).__init__(*args, **kwargs)
        self.daemon = KILL_THREADS_WHEN_MAIN_ENDS
