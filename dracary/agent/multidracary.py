from dracary.agent.base import BaseAgent
import json
from typing import Dict, Any, List, Union
from dracary.prompt.dracary import SYSTEM_PROMPT, NEXT_STEP_PROMPT
from litellm import completion as litellm_completion
import os
import logging

# logging.basicConfig(filename='./workspace/demo.log', filemode="a", encoding="utf-8", level=logging.DEBUG)

class Dracary(BaseAgent):
    """Dracary Agent: Capable of using multiple tools to execute tasks."""
    
    def __init__(self):
        super().__init__()  # Call the base class initializer
        self.system_prompt = SYSTEM_PROMPT
        self.NEXT_STEP_PROMPT = NEXT_STEP_PROMPT
    
    async def reason(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Reasoning and response with support for conversation history"""
        # 确保包含系统提示
        if messages[0]["role"] != "system":
            messages = [{"role": "system", "content": self.system_prompt}] + messages
        
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            tools=self.toolkit.get_tools(),
        )
        print(response)
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
        
        # 使用action_results创建观察消息
        observation_content = "Tool execution results:\n"
        for result in action_results:
            observation_content += f"- {result['tool']}: {result['response']}\n"
        
        # 返回观察结果
        return {
            "role": "system",
            "content": observation_content,
            "reasoning": reason,
            "action_results": action_results
        }
    
    async def litellm_reason(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Reasoning and response with support for conversation history"""
        # 确保包含系统提示
        if messages[0]["role"] != "system":
            messages = [{"role": "system", "content": self.system_prompt}] + messages
        
        response = litellm_completion(
            model=self.litellm_model, 
            messages=messages,
        )
        print(response)
        return response

    async def run(self, messages: Union[str, List[Dict[str, str]]]) -> Dict[str, Any]:
        """
        Perform reasoning and action, then generate an observation.
        支持单条消息或多轮对话消息列表

        Args:
            messages (Union[str, List[Dict]]): 用户消息或完整的对话历史

        Returns:
            Dict[str, Any]: 包含推理、动作和结果的观察
        """
        # 统一输入格式为消息列表
        if isinstance(messages, str):
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": messages}
            ]
        
        if self.type == "openai":
            return await self.openai_run(messages)
        elif self.type == "litellm":
            os.environ['DEEPSEEK_API_KEY'] = self.litellm_key
            return await self.litellm_run(messages)
        else:
            raise ValueError(f"Unsupported LLM type: {self.type}")
    
    async def openai_run(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Perform reasoning and action, then generate an observation.

        Args:
            messages (List[Dict]): 完整的对话历史

        Returns:
            Dict[str, Any]: 包含推理、动作和结果的观察
        """
        print("=== REASONING PHASE ===")
        reason = await self.reason(messages)
        print(f"Reasoning Result: {reason}")

        print("\n=== ACTION PHASE ===")
        action_results = await self.action(reason)
        print(f"Action Results: {action_results}")

        print("\n=== OBSERVE PHASE ===")
        observe_results = await self.observe(reason, action_results)
        print(f"Observation Results: {observe_results}")

        return observe_results

    async def litellm_run(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Perform reasoning and action, then generate an observation.

        Args:
            messages (List[Dict]): 完整的对话历史

        Returns:
            Dict[str, Any]: 包含推理、动作和结果的观察
        """
        print("=== REASONING PHASE ===")
        reason = await self.litellm_reason(messages)
        print(f"Reasoning Result: {reason}")

        # 对于litellm，简化处理 - 直接返回推理结果
        return {
            "role": "assistant",
            "content": reason.choices[0].message["content"],
            "reasoning": reason
        }