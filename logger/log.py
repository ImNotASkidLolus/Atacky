import os
class log():
    def __init__(self):
        self.save_file = os.path.expanduser("~/log.txt")
    def log_message(log_type, message, self):
        fd = 0
        if not os.path.exists(self.save_file):
            fd = os.open(self.save_file, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        else:
            fd = os.open(self.save_file, os.O_WRONLY, os.O_APPEND)
        if fd:
            os.write(fd, f"[LOG level {log_type}] {message}\n".encode("utf-8"))
        os.close(fd)