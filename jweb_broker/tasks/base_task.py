from .task_report import TaskReport

class BaseTask:
    '''The interface class for a basic task. Other tasks should be subclassed
       from this one.
    '''

    def __init__(self):
        self.tool_box = None
        self.report = None

    def set_tool_box(self, tool_box):
        self.tool_box = tool_box

    async def perform(self):
        self.report = TaskReport()
        await self.do()

    async def do(self):
        raise NotImplemented('Should be implemented in subclass')
