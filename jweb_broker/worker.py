from .tools.toolbox import ToolBox

class Worker:
    def __init__(self, tasks_lookout, tool_inventory):
        self.tasks_lookout = tasks_lookout
        self.tool_inventory = tool_inventory
        self.job_data = None
        self.tool_box = ToolBox(tool_inventory)
        self.report = None

    def set_job(self, job_data):
        self.job_data = self.job_data
        self.task = self.tasks_lookout.find(job_data)

    async def do_job(self):
        await self.tool_box.update(self.task.tools)
        self.task.set_tool_box(self.tool_box)
        await self.task.perform()
        self.report = self.task.report
