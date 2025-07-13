import asyncio
from dracary.agent.dracary import Dracary
import logging

logging.basicConfig(filename='./workspace/session-demo.log', filemode="a", encoding="utf-8", level=logging.INFO)

async def main():
    # 初始化代理
    dracary_agent = Dracary()
    
    print("开始提问（输入'exit'退出）...")
    logging.info("Session Log")

    while True:
        # 获取用户输入
        user_input = input("\n[用户]: ")
        logging.info("user: " + user_input)
        # 检查退出条件
        if user_input.lower() in ['exit', 'quit']:
            print("结束")
            break
        
        try:
            # 直接单次提问，不处理历史
            result = await dracary_agent.run(user_input)
            print(f"\n[代理]: {result}")
            logging.info("assistant: " + str(result))

        except Exception as e:
            print(f"处理出错: {str(e)}")

# 运行异步主函数
if __name__ == "__main__":
    asyncio.run(main())