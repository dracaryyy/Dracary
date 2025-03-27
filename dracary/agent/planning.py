from dracary.agent.base import BaseAgent
import json
from typing import Dict, Any
from dracary.prompt.planning import SYSTEM_PROMPT, USER_PROMPT

class PlanningAgent(BaseAgent):
    """Planning Agent: Responsible for generating task plans and saving them to a file."""
    
    def __init__(self):
        super().__init__()  # Call the base class initializer
        self.system_prompt = SYSTEM_PROMPT
        self.user_prompt = USER_PROMPT

    async def think(self, user_input: str) -> Dict[str, Any]:
        """Generate a task plan."""
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": self.user_prompt + user_input}
            ],
            tools=self.toolkit.get_tools(),
        )
        return response.choices[0].message

    async def action(self, plan, file_path: str = "plan.txt"):
        """Save the task plan to a file."""
        # Retrieve the tool name
        function_name = plan.tool_calls[0].function.name
        function_to_call = self.available_functions[function_name]
        function_args = json.loads(plan.tool_calls[0].function.arguments)

        print(f"Function Name: {function_name}")
        print(f"Function Arguments: {function_args}")

        function_response = await function_to_call(**function_args)

        return function_response
    

async def execute_planning(prompt: str, output_file: str = "plan.txt"):
    """
    Execute the planning task and save the result to a file.

    Args:
        prompt (str): The task description provided by the user.
        output_file (str): The file path where the task plan will be saved.

    Returns:
        str: The result of saving the task plan.
    """
    planning_agent = PlanningAgent()

    # Generate the task plan
    print("=== PLANNING PHASE ===")
    plan = await planning_agent.think(prompt)
    print(f"Generated Plan: {plan}")  # Output the generated plan
    
    # Save the task plan to a file
    print("\n=== SAVING PLAN TO FILE ===")
    result = await planning_agent.action(plan, file_path=output_file)
    return result