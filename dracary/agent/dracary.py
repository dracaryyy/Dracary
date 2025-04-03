from dracary.agent.base import BaseAgent
import json
from typing import Dict, Any, List
from dracary.prompt.dracary import SYSTEM_PROMPT, NEXT_STEP_PROMPT

class Dracary(BaseAgent):
    """Dracary Agent: Capable of using multiple tools to execute tasks."""
    
    def __init__(self):
        super().__init__()  # Call the base class initializer
        self.system_prompt = SYSTEM_PROMPT
        self.NEXT_STEP_PROMPT = NEXT_STEP_PROMPT

    async def reason(self, user_prompt: str) -> Dict[str, Any]:
        """Generate a task plan."""
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            tools=self.toolkit.get_tools(),
        )
        return response.choices[0].message

    async def action(self, plan, file_path: str = "plan.txt"):
        """Execute the task plan using multiple tools and save the results."""
        results = []
        for tool_call in plan.tool_calls:
            function_name = tool_call.function.name
            function_to_call = self.available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)

            print(f"Executing Tool: {function_name}")
            print(f"Arguments: {function_args}")

            function_response = await function_to_call(**function_args)
            results.append({
                "tool": function_name,
                "response": function_response
            })

        return results
    
