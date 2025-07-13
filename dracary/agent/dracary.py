from dracary.agent.base import BaseAgent
import json
from typing import Dict, Any, List
from dracary.prompt.dracary import SYSTEM_PROMPT, NEXT_STEP_PROMPT
from litellm import completion as litellm_completion
import os
import logging

logging.basicConfig(filename='./workspace/state-demo.log', filemode="a", encoding="utf-8", level=logging.DEBUG)

class Dracary(BaseAgent):
    """Dracary Agent: Capable of using multiple tools to execute tasks."""
    
    def __init__(self):
        super().__init__()  # Call the base class initializer
        self.system_prompt = SYSTEM_PROMPT
        self.NEXT_STEP_PROMPT = NEXT_STEP_PROMPT
        self.State = ""
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
        print(response)
        # 记录问答到State
        self.State += f"\n用户: {user_prompt}\n助手: {response.choices[0].message['content'] if isinstance(response.choices[0].message, dict) else response.choices[0].message}\n"
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
        print(results)
        return results
    
    async def observe(self, reason: Dict[str, Any], action_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Perform reasoning and action, then generate an observation.

        Args: 
            reason (Dict[str, Any]): The reasoning result.
            action_results (List[Dict[str, Any]]): The results of the actions performed.

        Returns:
            Dict[str, Any]: The observation containing the reasoning, actions, and results.
        """
        print("=== OBSERVATION PHASE ===")
        

        # Query the LLM to determine if the task is complete
        try:
            llm_response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "Determine if the task is complete based on the following context."},
                    {"role": "user", "content":  self.State}
                ]
            )
            completion_status = llm_response.choices[0].message["content"]
        except Exception as e:
            print(f"Error querying LLM for observation: {e}")
            completion_status = "Error determining task completion."
    
    async def litellm_reason(self, user_prompt: str) -> Dict[str, Any]:
        """Reasoning and response."""
        response = litellm_completion(
            model=self.litellm_model, 
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ],
)
        print(response)
        # 记录问答到State
        answer = response['choices'][0]['message']['content'] if isinstance(response, dict) else str(response)
        self.State += f"\n用户: {user_prompt}\n助手: {answer}\n"
        return response

    async def run(self, user_prompt: str) -> Dict[str, Any]:
        """
        Perform reasoning and action, then generate an observation.

        Args:
            user_prompt (str): The task description provided by the user.

        Returns:
            Dict[str, Any]: The observation containing the reasoning, actions, and results.
        """
        if self.type == "openai":
            return await self.openai_run(user_prompt)
        elif self.type == "litellm":
            os.environ['DEEPSEEK_API_KEY'] = self.litellm_key
            return await self.litellm_run(user_prompt)
        else:
            raise ValueError(f"Unsupported LLM type: {self.type}")
    
    async def openai_run(self, user_prompt: str) -> Dict[str, Any]:
        """
        Perform reasoning and action, then generate an observation.

        Args:
            user_prompt (str): The task description provided by the user.

        Returns:
            Dict[str, Any]: The observation containing the reasoning, actions, and results.
        """
        print("=== REASONING PHASE ===")
        reason = await self.reason(user_prompt)
        print(f"Reasoning Result: {reason}")

        print("\n=== ACTION PHASE ===")
        action_results = await self.action(reason)
        print(f"Action Results: {action_results}")

        print("\n=== OBSERVE PHASE ===")
        observe_results = await self.observe(reason, action_results)
        print(f"Observation Results: {observe_results}")
        # 运行结束后将State添加到log文件中
        logging.info("State Log:\n" + self.State)
        return observe_results

    async def litellm_run(self, user_prompt: str) -> Dict[str, Any]:
        """
        Perform reasoning and action, then generate an observation.

        Args:
            user_prompt (str): The task description provided by the user.

        Returns:
            Dict[str, Any]: The observation containing the reasoning, actions, and results.
        """
        print("=== REASONING PHASE ===")
        reason = await self.litellm_reason(user_prompt)
        print(f"Reasoning Result: {reason}")
        print("State" + self.State)
        # 运行结束后将State添加到log文件中
        logging.info("State Log:\n" + self.State)
        return reason