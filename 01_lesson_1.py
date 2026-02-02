from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

def llm(input):
    chat = ChatOpenAI(model="gpt-4o-mini")
    response = chat.invoke([{"role": "user", "content": input}])    
    return response.content

if __name__ == "__main__":
    print(llm("Hello from learnlangchain!"))