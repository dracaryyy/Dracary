import asyncio
from dracary.agent.multidracary import Dracary

async def main():
    # 初始化代理
    dracary_agent = Dracary()
    
    print("开始对话（输入'exit'退出）...")
    conversation_history = []
    
    while True:
        # 获取用户输入
        user_input = input("\n[用户]: ")
        
        # 检查退出条件
        if user_input.lower() in ['exit', 'quit']:
            print("对话结束")
            break
        
        try:
            # 添加用户消息到对话历史
            conversation_history.append({"role": "user", "content": user_input})
            
            # 执行任务（传入完整对话历史）
            result = await dracary_agent.run(conversation_history)
            
            # 添加代理回复到对话历史
            conversation_history.append({"role": "assistant", "content": result})
            print(f"\n[代理]: {result}")
            
        except Exception as e:
            print(f"处理出错: {str(e)}")
            # 如果出错，移除最后一条用户输入（因为处理失败）
            if conversation_history and conversation_history[-1]["role"] == "user":
                conversation_history.pop()

    return conversation_history

# 运行异步主函数
if __name__ == "__main__":
    asyncio.run(main())