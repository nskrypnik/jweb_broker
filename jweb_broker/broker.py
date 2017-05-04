import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from .defaults import MONGO_HOST, MONGO_PORT, JOBS_COLLECTION_NAME, \
                      POLL_JOBS_DELAY, NUM_OF_WORKERS
from .job_states import IDLE, OPENED, IN_PROGRESS, FAILED
from .workers_pool import WorkersPool
from .tools.tool_inventory import ToolInventory

# magic strings:
STATE = 'state'

class Broker:

    def __init__(self, **kw):
        # create a main loop
        self.loop = kw.get('loop') or asyncio.get_event_loop()
        self._get_options(**kw)
        self._init_db_connection()
        self.jobs_queue = asyncio.Queue()
        self._init_tool_inventory()
        self._init_workers_pool()

    def _get_options(self, **kw):
        '''Extract all options from key-word arguments
        '''
        try:
            self.db_name = kw['db_name']
        except KeyError:
            raise Exception('db_name parameter should be provided')
        try:
            self.tasks_lookout  = kw['tasks_lookout']
        except KeyError:
            raise Exception('Tasks lookout object should be provided to broker constructor')
        self.db_host = kw.get('db_host', MONGO_HOST)
        self.db_port = kw.get('db_port', MONGO_PORT)
        self.jobs_collection_name = kw.get('jobs_collection_name', JOBS_COLLECTION_NAME)
        self.drop_jobs_collection = kw.get('drop_jobs_collection', False)
        self.num_of_workers = kw.get('num_of_workers', NUM_OF_WORKERS)
        self.poll_jobs_delay = kw.get('poll_jobs_delay', POLL_JOBS_DELAY)
        self.tool_inventory_class = kw.get('tool_inventory_class', ToolInventory)
        self.tool_inventory_extra_kw = kw.get('tool_inventory_extra_kw', {})

    def _init_workers_pool(self):
        self.workers_pool = WorkersPool(
            self.num_of_workers,
            self.tasks_lookout,
            self.tool_inventory
        )

    def _init_tool_inventory(self):
        kw = dict(db=self.db, num_of_workers=self.num_of_workers)
        kw.update(self.tool_inventory_extra_kw)
        self.tool_inventory = self.tool_inventory_class(self.loop, **kw)

    def _init_db_connection(self):
        '''Initialize connection to db
        '''
        self.db_client = AsyncIOMotorClient(self.db_host, self.db_port)
        self.db = self.db_client[self.db_name]
        self.jobs_collection = self.db[self.jobs_collection_name]

    async def launch_jobs_manager(self):
        if self.drop_jobs_collection:
            await self.db.drop_collection(self.jobs_collection_name)
            await self.db.create_collection(self.jobs_collection_name)
            # reassign self.jobs_collection
            self.jobs_collection = self.db[self.jobs_collection_name]
            # create an index on job state property for optimization
            await self.jobs_collection.create_index(STATE)

        # Start jobs manager
        self.loop.create_task(self.run_jobs_manager())

    async def run_jobs_manager(self):
        '''This function is our jobs managers which simply checks jobs collection
           and put jobs to do into jobs queue
        '''
        while True:
            cursor = self.jobs_collection.find({STATE: IDLE})
            jobs = await cursor.to_list(None)
            for job_data in jobs:
                await self.put_job_to_queue(job_data)
            await asyncio.sleep(self.poll_jobs_delay)

    async def put_job_to_queue(self, job_data):
        job_data = await self.update_job_state(job_data, OPENED)
        self.jobs_queue.put_nowait(job_data)

    async def run_scheduler(self):
        '''This function is a scheduler itself and it listens to jobs queue and if
           some job has to be done it acquires a worker from a worker pool and assign
           job to him
        '''
        while True:
            job_data = await self.jobs_queue.get()
            worker = await self.workers_pool.get_worker()
            self.loop.create_task(self.launch_worker_operation(worker, job_data))

    async def launch_worker_operation(self, worker, job_data):
        worker.set_job(job_data)
        await self.update_job_state(job_data, IN_PROGRESS)
        await worker.do_job()
        if worker.report.success:
            await self.update_job_state(job_data, DONE)
        else:
            await self.update_job_state(job_data, FAILED)
        self.workers_pool.release(worker)

    async def update_job_state(self, job_data, state):
        return await self.jobs_collection.update(
            {'_id': job_data['_id']},
            {'$set': {STATE: state}}
        )

    def run(self, is_internal_loop=True):
        '''Start I/O loop
        '''
        self.loop.create_task(self.launch_jobs_manager())
        self.loop.create_task(self.run_scheduler())
        if is_internal_loop:
            self.loop.run_forever()
