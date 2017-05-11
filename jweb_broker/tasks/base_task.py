import traceback
from .task_report import TaskReport

class BaseTask:
    '''The interface class for a basic task. Other tasks should be subclassed
       from this one.
    '''

    tools = []
    info = {} # additional task info for Report Handler

    def __init__(self, context):
        self.tool_box = None
        self.report = None
        self.context = context

    def set_tool_box(self, tool_box):
        self.tool_box = tool_box

    async def perform(self):
        self.report = TaskReport(self.info)
        try:
            await self.do()
            if not self.report.failed:
                self.report.success = True
        except Exception as e:
            self.report.failed = True
            self.report.error = e
            self.report.traceback = traceback.format_exc()


    async def do(self):
        raise NotImplemented('Should be implemented in subclass')
