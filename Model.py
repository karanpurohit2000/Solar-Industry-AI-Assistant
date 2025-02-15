import cohere
from dotenv import dotenv_values

env_vars = dotenv_values(".env")
CohereAPIKey = env_vars.get("CohereAPIKey")

co = cohere.Client(api_key=CohereAPIKey)

def categorize_query(prompt: str):
    system_prompt = """You are a decision-making model. Only return 'solar' if the query is about solar energy, else return 'reject'."""

    response = co.generate(prompt=system_prompt + " " + prompt, model="command-r-plus", max_tokens=5)
    return response.generations[0].text.strip()
