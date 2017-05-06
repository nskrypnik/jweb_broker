import asyncio
from .worker import Worker

WAIT_TIMEOUT = 0.5

class WorkersPool:

    def __init__(self, num_of_workers, tasks_lookout, tool_inventory):
        # create workers
        self.workers_queue = asyncio.Queue()
        for i in range(num_of_workers):
            worker = Worker(tasks_lookout, tool_inventory)
            self.workers_queue.put_nowait(worker)

    async def get_worker(self):
        return await self.workers_queue.get()

    def release(self, worker):
        self.workers_queue.put_nowait(worker)
