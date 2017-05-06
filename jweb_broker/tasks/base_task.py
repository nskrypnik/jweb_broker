from .task_report import TaskReport

class BaseTask:
    '''The interface class for a basic task. Other tasks should be subclassed
       from this one.
    '''

    tools = []

    def __init__(self, context):
        self.tool_box = None
        self.report = None
        self.context = context

    def set_tool_box(self, tool_box):
        self.tool_box = tool_box

    async def perform(self):
        self.report = TaskReport()
        await self.do()
        if not self.report.error:
            self.report.success = True

    async def do(self):
        raise NotImplemented('Should be implemented in subclass')
