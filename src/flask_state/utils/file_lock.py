import os
import platform

from .constants import OperatingSystem

SYSTEM = (
    OperatingSystem.WINDOWS_SYSTEM
    if platform.system() == OperatingSystem.WINDOWS_SYSTEM
    else OperatingSystem.UNIX_SYSTEM
)
if SYSTEM == OperatingSystem.UNIX_SYSTEM:
    import fcntl


class Lock:
    @staticmethod
    def get_file_lock():
        return FileLock()


class FileLock:
    def __init__(self):
        lock_file = "821e9dab54fec92e3d054b3367a50b70d328caed"
        if SYSTEM == OperatingSystem.WINDOWS_SYSTEM:
            lock_dir = os.environ["tmp"]
        else:
            lock_dir = "/tmp"

        self.file = "{}{}{}".format(lock_dir, os.sep, lock_file)
        self._fn = None
        self.release()

    def acquire(self):
        if SYSTEM == OperatingSystem.WINDOWS_SYSTEM:
            if os.path.exists(self.file):
                return

            with open(self.file, "w") as f:
                f.write("1")
        else:
            self._fn = open(self.file, "w")
            fcntl.flock(self._fn.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            self._fn.write("1")

    def release(self):
        if SYSTEM == OperatingSystem.WINDOWS_SYSTEM:
            if os.path.exists(self.file):
                os.remove(self.file)
        else:
            if self._fn:
                try:
                    self._fn.close()
                except Exception as e:
                    raise e
