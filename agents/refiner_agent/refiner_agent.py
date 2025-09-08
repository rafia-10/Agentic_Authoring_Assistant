from tools.refiner_tool import RefinerTool

class RefinerAgent:
    def __init__(self, llm=None):
        self.tool = RefinerTool(llm=llm)

    def refine(self, inputs):
        return self.tool.refine(inputs)
