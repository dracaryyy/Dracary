from litellm import completion
import os

os.environ['DEEPSEEK_API_KEY'] = "sk-d563ba96cb3f4ce7bfc99415e3a2e117"
response = completion(
    model="deepseek/deepseek-chat", 
    messages=[
        {"role": "user", "content": "hello from litellm"}
    ],
)
print(response)