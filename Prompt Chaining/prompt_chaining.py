from typing import List
from dotenv import load_dotenv
import openai
import os

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def run_openai_llm(prompt: str, model: str) -> str:
    """使用 OpenAI API 執行 LLM 呼叫。"""
    try:
        completion = openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"呼叫 OpenAI API 時發生錯誤：{e}")
        return ""

def serial_chain_workflow(input_query: str, prompt_chain : List[str]) -> List[str]:
    """執行一系列的 LLM 呼叫，以使用 `prompt_chain` 中指定的提示列表來處理 `input_query`。"""
    response_chain = []
    response = input_query
    for i, prompt in enumerate(prompt_chain):
        print(f"Step {i+1}")
        response = run_openai_llm(f"{prompt}\nInput:\n{response}", model='gpt-3.5-turbo')
        response_chain.append(response)
        print(f"{response}\n")
    return response_chain

# Example
question = "Sally earns $12 an hour for babysitting. Yesterday, she just did 50 minutes of babysitting. How much did she earn?"

prompt_chain = ["""Given the math problem, ONLY extract any relevant numerical information and how it can be used.""",
                """Given the numberical information extracted, ONLY express the steps you would take to solve the problem.""",
                """Given the steps, express the final answer to the problem."""]

responses = serial_chain_workflow(question, prompt_chain)

final_answer = responses[-1]