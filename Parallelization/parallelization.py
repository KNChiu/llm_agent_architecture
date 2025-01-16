import os
import asyncio
import openai
from typing import List
from openai import AsyncOpenAI
from openai import RateLimitError
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def run_llm(user_prompt : str, model : str, system_prompt : str = None):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    messages.append({"role": "user", "content": user_prompt})
    
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=1000,        
    )

    return response.choices[0].message.content

# The function below will call the reference LLMs in parallel
async def run_llm_parallel(user_prompt : str, model : str, system_prompt : str = None):
    """使用參考模型執行單個 LLM 呼叫。"""
    async_client = AsyncOpenAI()
    for sleep_time in [1, 2, 4]:
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            messages.append({"role": "user", "content": user_prompt})

            response = await async_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
            )
            break
        except RateLimitError as e:
            print(e)
            await asyncio.sleep(sleep_time)
    return response.choices[0].message.content


async def parallel_workflow(prompt : str, proposer_models : List[str], aggregator_model : str, aggregator_prompt: str):
    """Run a parallel chain of LLM calls to address the `input_query` 
    using a list of models specified in `models`.

    Returns output from final aggregator model.
    """

    # Gather intermediate responses from proposer models
    proposed_responses = await asyncio.gather(*[run_llm_parallel(prompt, model) for model in proposer_models])
    
    # Aggregate responses using an aggregator model
    final_output = run_llm(user_prompt=prompt,
                           model=aggregator_model,
                           system_prompt=aggregator_prompt + "\n" + "\n".join(f"{i+1}. {str(element)}" for i, element in enumerate(proposed_responses)
           ))
    
    return final_output, proposed_responses


reference_models = [
    "gpt-3.5-turbo",
    "gpt-4o-mini",
    "gpt-4o-mini",
    "gpt-4o",
]

user_prompt = """Jenna and her mother picked some apples from their apple farm. 
Jenna picked half as many apples as her mom. If her mom got 20 apples, how many apples did they both pick?"""

aggregator_model = "gpt-4o-mini"

aggregator_system_prompt = """You have been provided with a set of responses from various open-source models to the latest user query.
Your task is to synthesize these responses into a single, high-quality response. It is crucial to critically evaluate the information
provided in these responses, recognizing that some of it may be biased or incorrect. Your response should not simply replicate the
given answers but should offer a refined, accurate, and comprehensive reply to the instruction. Ensure your response is well-structured,
coherent, and adheres to the highest standards of accuracy and reliability.

Responses from models:"""

async def main():
    answer, intermediate_reponses = await parallel_workflow(prompt = user_prompt, 
                                                            proposer_models = reference_models, 
                                                            aggregator_model = aggregator_model, 
                                                            aggregator_prompt = aggregator_system_prompt)

    for i, response in enumerate(intermediate_reponses):
        print(f"Intermetidate Response {i+1}:\n\n{response}\n")

    print(f"Final Answer: {answer}\n")


asyncio.run(main())