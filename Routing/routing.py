from pydantic import BaseModel, Field
from typing import Literal, Dict
import json
from pydantic import ValidationError

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

def JSON_llm(user_prompt: str, schema, system_prompt: str = None):
    try:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        # 修改提示詞，明確要求 JSON 格式輸出
        schema_str = json.dumps(schema.model_json_schema(), ensure_ascii=False)
        user_prompt_with_format = f"{user_prompt}\n請以 JSON 格式回答，並符合以下 Schema：\n{schema_str}"
        messages.append({"role": "user", "content": user_prompt_with_format})

        extract = openai.chat.completions.create(
            messages=messages,
            model="gpt-4o-mini",
        )
        # 解析 JSON 字串
        return json.loads(extract.choices[0].message.content)

    except ValidationError as e:
        error_message = f"Failed to parse JSON: {e}"
        print(error_message)
    except json.JSONDecodeError as e:
        error_message = f"Failed to decode JSON from LLM response: {e}"
        print(error_message)
    except Exception as e:
        print(f"呼叫 OpenAI API 時發生錯誤：{e}")
        return None

def router_workflow(input_query: str, routes: Dict[str, str]) -> str:
    """Given a `input_query` and a dictionary of `routes` containing options and details for each.
    Selects the best model for the task and return the response from the model.
    """
    ROUTER_PROMPT = """Given a user prompt/query: {user_query}, select the best option out of the following routes:
    {routes}. Answer only in JSON format, adhering to the provided schema."""

    # Create a schema from the routes dictionary
    class Schema(BaseModel):
        route: Literal[tuple(routes.keys())]

        reason: str = Field(
            description="Short one-liner explanation why this route was selected for the task in the prompt/query."
        )

    # Call LLM to select route
    selected_route = JSON_llm(
        ROUTER_PROMPT.format(user_query=input_query, routes=routes), Schema
    )

    if selected_route:
        print(
            f"Selected route:{selected_route['route']}\nReason: {selected_route['reason']}\n"
        )

        # Use LLM on selected route.
        # Could also have different prompts that need to be used for each route.
        response = run_openai_llm(prompt=input_query, model=selected_route["route"])
        print(f"Response: {response}\n")

        return response
    else:
        return "路由選擇失敗。"

prompt_list = [
    "Produce python snippet to check to see if a number is prime or not.",
    "Plan and provide a short itenary for a 2 week vacation in Europe.",
    "Write a short story about a dragon and a knight.",
]

model_routes = {
    "gpt-3.5-turbo": "Best model choice for code generation tasks.",
    "gpt-4o-mini": "Best model choice for story-telling, role-playing and fantasy tasks.",
    "gpt-4o": "Best model for reasoning, planning and multi-step tasks",
}

for i, prompt in enumerate(prompt_list):
    print(f"Task {i+1}: {prompt}\n")
    print(20 * "==")
    router_workflow(prompt, model_routes)