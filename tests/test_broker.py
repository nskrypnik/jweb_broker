from utils import MockedDBClient, AsyncMock, MockedDriversPool

import asyncio
import unittest
from unittest.mock import MagicMock, patch
from jweb_broker import Broker
from jweb_broker.tasks import BaseTaskLookout
from jweb_broker.workers_pool import WorkersPool


class MockTasksLookout(BaseTaskLookout):
    pass


class MockedLoop:

    def __init__(self, *args, **kw):
        self.create_task = MagicMock()


class TestBroker(unittest.TestCase):

    @patch('motor.motor_asyncio.AsyncIOMotorClient.__new__', spec=MockedDBClient, return_value=MockedDBClient())
    @patch('jweb_driver.drivers_pool.DriversPool.__new__', spec=MockedDriversPool, return_value=MockedDriversPool(10))
    def setUp(self, *args):
        self.loop = asyncio.get_event_loop()
        self.broker = Broker(
            loop=self.loop,
            db_name='test',
            tasks_lookout=MockTasksLookout()
        )
        loop = MockedLoop()
        self.fake_loop_broker = Broker(
            loop=loop,
            db_name='test',
            tasks_lookout=MockTasksLookout(),
            drop_jobs_collection=True
        )
        self.fake_loop = loop

    def untest_init(self):
        # should throuw an exception when db_name is not provided
        try:
            Broker()
        except Exception as e:
            self.assertEqual(e.args[0], 'db_name parameter should be provided')

        # should throw an exception when tasks lookout is not provided
        try:
            Broker(db_name='test')
        except Exception as e:
            self.assertEqual(e.args[0], 'Tasks lookout object should be provided to broker constructor')

        broker = Broker(loop=self.loop, db_name='test', tasks_lookout=MockTasksLookout())
        self.assertTrue(isinstance(broker.db_client, MockedDBClient))

    def test_init_workers_pool(self):
        self.assertTrue(isinstance(self.broker.workers_pool, WorkersPool))


    def test_launch_jobs_manager(self):

        self.loop.run_until_complete(self.fake_loop_broker.launch_jobs_manager())
        self.fake_loop_broker.db.drop_collection.assert_called()
        self.fake_loop_broker.db.create_collection.assert_called()
        self.fake_loop_broker.jobs_collection.create_index.assert_called()
        self.fake_loop.create_task.assert_called()

    def test_run_jobs_manager(self):
        t = self.broker.update_job_state
        self.broker.update_job_state = AsyncMock(return_value=dict(test='test'))
        self.loop.create_task(self.broker.run_jobs_manager())

        async def check_job_data():
            job_data = await self.broker.jobs_queue.get()
            self.assertEqual(job_data['test'], 'test')

        self.loop.run_until_complete(check_job_data())
        self.broker.update_job_state = t
