import asyncio
from unittest.mock import MagicMock


class AsyncMock(MagicMock):
    async def __call__(self, *args, **kwargs):
        return super(AsyncMock, self).__call__(*args, **kwargs)


class MockedBrowserDriver:
    pass


class MockCursor:
    def __init__(self, *args, **kw):
        self.to_list = AsyncMock(return_value=[{}, ])


class MockedDriversPool:
    def __init__(self, num_of_workers, *args, **kw):
        self.drivers = map(lambda i: MockedBrowserDriver(), range(num_of_workers))
        self.run = MagicMock()


class MockedDBCollection:
    def __init__(self, *args, **kw):
        self.create_index = AsyncMock()

    def find(self, *args, **kw):
        return MockCursor()


class MockedDB(dict):

    def __init__(self, *args, **kw):
        self.drop_collection = AsyncMock()
        self.create_collection = AsyncMock()

    def __getitem__(self, name):
        return MockedDBCollection()


class MockedDBClient(dict):

    def __init__(self, *args, **kw):
        pass

    def __getitem__(self, name):
        return MockedDB()
