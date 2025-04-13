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
        """Reasoning and response."""
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            tools=self.toolkit.get_tools(),
        )
        return response.choices[0].message

    async def action(self, reason, file_path: str = "plan.txt"):
        """Execute the reasoning using multiple tools."""
        results = []
        # Check if reason or tool_calls is empty
        if not reason or not hasattr(reason, "tool_calls") or not reason.tool_calls:
            print("No tool calls found in the reasoning. Execution aborted.")
            return results

        for tool_call in reason.tool_calls:
            function_name = tool_call.function.name
            function_to_call = self.available_functions.get(function_name)

            # Check if the function exists in available_functions
            if not function_to_call:
                print(f"Tool '{function_name}' is not available. Skipping.")
                continue

            function_args = json.loads(tool_call.function.arguments)

            print(f"Executing Tool: {function_name}")
            print(f"Arguments: {function_args}")

            # Execute the tool and collect the response
            try:
                function_response = await function_to_call(**function_args)
                results.append({
                    "tool": function_name,
                    "response": function_response
                })
            except Exception as e:
                print(f"Error executing tool '{function_name}': {e}")
                results.append({
                    "tool": function_name,
                    "response": f"Error: {e}"
                })

        return results
    
