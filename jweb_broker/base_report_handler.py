from .job_states import IDLE

class BaseReportHandler:

    def __init__(self, loop, db, jobs_collection, *args, **kw):
        self.db = db
        self.jobs_collection = jobs_collection

    async def add_new_job(self, job_data):
        await self.jobs_collection.insert_one(dict(data=job_data, state=IDLE))

    async def handle(self, report):
        pass
