import asyncio
from dracary.agent.planning import execute_planning

async def main():
    # Get the task description from the console input
    user_prompt = input("Please enter the task description：\n")

    # Execute the planning task
    result = await execute_planning(prompt=user_prompt, output_file="plan.txt")
    print("\nThe task plan has been saved. The result is as follows:")
    print(result)

# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())