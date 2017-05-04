import asyncio
from jweb_driver import DriversPool
from .defaults import NUM_OF_WORKERS

class ToolInventoryError(Exception):
    pass


class BaseToolInventory:
    '''Base tools inventory class - a container of all available tools for
       workers which implement asyncio access to tools
    '''

    def __init__(self, loop):
        self.loop = loop

    async def get_tool(self, tool_name):
        '''Get a tool from tool inventory
        '''
        getter = 'get_%s' % tool_name
        if not hasattr(self, getter):
            err_msg = 'Tool \'%s\' cannot be located in inventory' % tool_name
            raise ToolInventoryError(err_msg)
        return await getter()

    def return_tool(self, tool_name, tool):
        '''Return tool back to tool inventory
        '''
        func = 'return_%s' % tool_name
        if hasattr(self, func):
            func(tool)


class ToolInventory(BaseToolInventory):
    '''Default tool inventory which contains 'db' tool - an object to access
       database and jweb_driver pool
    '''

    def __init__(self, loop, db=None, num_of_drivers=NUM_OF_WORKERS):
        super(ToolInventory, self).__init__(loop)
        self.db = db
        self.jweb_drivers_pool = DriversPool(num_of_drivers, loop)
        self.jweb_drivers_pool.run()
        self.id_to_driver = {
            id(driver): driver for driver in self.jweb_drivers_pool.drivers
        }
        self._available_drivers = list(self.id_to_driver.keys())

    def get_db(self):
        return self.db

    async def get_jweb_driver(self):
        while True:
            if len(self._available_drivers):
                driver_id = self._available_drivers.pop()
                return self.id_to_driver[driver_id]
            asyncio.sleep(1)

    def return_jweb_driver(self, driver):
        self._available_drivers.insert(0, id(driver))
