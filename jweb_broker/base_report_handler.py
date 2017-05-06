
class BaseReportHandler:

    def __init__(self, loop, db, jobs_collection, *args, **kw):
        self.db = db
        self.jobs_collection = jobs_collection

    def add_new_job(self, job_data):
        pass

    def handle(self, report):
        pass
