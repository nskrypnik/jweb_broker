
class TaskReport:

    def __init__(self, task_info):
        self.task_info = task_info
        self.success = False
        self.failed = False
        self.error = None
        self.traceback = None
        self.data = {}
