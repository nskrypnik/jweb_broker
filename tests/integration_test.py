import asyncio
from jweb_broker import Broker, BaseReportHandler
from jweb_broker.tools import BaseToolInventory
from jweb_broker.tasks import BaseTaskLookout, BaseTask
from jweb_broker.job_states import IDLE
from jweb_broker.defaults import JOBS_COLLECTION_NAME
from motor.motor_asyncio import AsyncIOMotorClient


class DummyTask(BaseTask):
    async def do(self):
        print('I\'m dummy task #%s' % self.context['id'])

class TaskLookout(BaseTaskLookout):
    def find(self, job_data):
        return DummyTask(job_data)

class ReportHandler(BaseReportHandler):
    async def handle(self, report):
        print('Got report %s' % report.success)

async def create_jobs():
    db = AsyncIOMotorClient()['test']
    await db.drop_collection(JOBS_COLLECTION_NAME)
    await db.create_collection(JOBS_COLLECTION_NAME)
    jobs_collection = db[JOBS_COLLECTION_NAME]

    for i in range(10):
        job_data = dict(state=IDLE, data=dict(id=i))
        await jobs_collection.insert_one(job_data)
    print('Jobs are created in %s' % JOBS_COLLECTION_NAME)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_jobs())

    broker = Broker(
        loop=loop,
        db_name='test',
        task_lookout=TaskLookout(),
        tool_inventory_class=BaseToolInventory,
        report_handler_class=ReportHandler
    )
    broker.run()


if __name__ == '__main__':
    main()
