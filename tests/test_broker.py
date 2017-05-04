from utils import patch_all, MockedDBClient
patch_all()

import asyncio
import unittest
from cefpython3 import cefpython as cef
from jweb_broker import Broker
from jweb_broker.tasks import BaseTasksLookout


class MockTasksLookout(BaseTasksLookout):
    pass


class TestBroker(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def tearDown(self):
        self.loop.close()

    def test_init(self):
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
