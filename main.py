import asyncio
from dracary.agent.dracary import Dracary

async def main():
    # Get the task description from the console input
    user_prompt = input("Please enter the task description：\n")
    dracary_agent = Dracary()

    # Generate the task plan
    print("=== PLANNING PHASE ===")
    plan = await dracary_agent.think(user_prompt)
    print(f"Generated Plan: {plan}")  # Output the generated plan
    
    # Save the task plan to a file
    print("\n=== SAVING PLAN TO FILE ===")
    result = await dracary_agent.action(plan, file_path="plan.txt")
    print("\nThe task plan has been saved. The result is as follows:")
    return result

# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())