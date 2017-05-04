
class ToolBox:

    def __init__(self, tool_inventory):
        self.tools = {}
        self.tool_inventory

    async def update(self, list_of_tools):
        self.tools = {}
        for tool_name in list_of_tools:
            self.tools[tool_name] = await self.tool_inventory.get_tool(tool_name)

    def get(self, tool_name):
        return self.tools[tool_name]
