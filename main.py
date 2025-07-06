import asyncio
from dracary.agent.dracary import Dracary

async def main():
    # Get the task description from the console input
    user_prompt = input("Please enter the task description：\n")
    
    dracary_agent = Dracary()

    result = await dracary_agent.run(user_prompt)
    print(result)

    return result

# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())