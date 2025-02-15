import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from json import load, dump
from RTSearchEngine import googlesearch

# Load API keys (Try `.env` first, then `st.secrets`)
load_dotenv()
GroqAPIKey = os.getenv("GroqAPIKey", "")
CohereAPIKey = os.getenv("CohereAPIKey", "")

try:
    # Use `st.secrets` if running on Streamlit Cloud
    if not GroqAPIKey or not CohereAPIKey:
        GroqAPIKey = st.secrets["GroqAPIKey"]
        CohereAPIKey = st.secrets["CohereAPIKey"]
        print("Running on Streamlit Cloud (Using st.secrets)")
    else:
        print("Running Locally (Using .env)")
except Exception:
    print("No `secrets.toml` found, using `.env` instead.")

# Ensure API keys exist before proceeding
if not GroqAPIKey or not CohereAPIKey:
    raise ValueError("❌ Missing API keys! Add them to `.env` (Local) or Streamlit Secrets (Cloud).")

# Initialize Groq client
client = Groq(api_key=GroqAPIKey)

# Define system behavior
System = """Hello! You are SolarAI, a specialized AI chatbot that assists with Wattmonk services, solar industry queries, and competitive analysis.
*** Only respond to solar and Wattmonk-related questions. If the user asks unrelated topics, reply: 'I can only assist with Wattmonk and solar energy-related queries.' ***
*** Provide comparisons between Wattmonk and other solar service providers if asked. ***
*** Always reply in English. ***
"""

SystemChatbot = [{"role": "system", "content": System}]

# Load or create chat log (limit to last 10 messages)
try:
    with open("Data/chatLog.json", "r") as f:
        messages = load(f)
        messages = messages[-10:]  # Keep only the last 10 messages
except FileNotFoundError:
    with open("Data/chatLog.json", "w") as f:
        dump([], f)

def Chatbot(Query):
    """Handles user queries with Groq API and Google Search results"""

    # Allowed topics for chatbot
    allowed_topics = ["solar", "wattmonk", "permit", "survey", "PE review", "interconnection", 
                      "sales proposal", "planset", "compare", "competition", "versus", "better than"]

    # Handling general greetings
    if Query.lower() in ["how are you", "who are you", "tell me about yourself"]:
        responses = {
            "how are you": "I’m here to assist you with Wattmonk and solar-related queries. How can I help?",
            "who are you": "I am SolarAI, an assistant specializing in solar energy and Wattmonk’s services.",
            "tell me about yourself": "I provide insights on solar energy, installation, permits, and Wattmonk services."
        }
        return responses[Query.lower()]

    # Competitive analysis responses
    competitors = {
        "tesla solar": "Tesla Solar focuses on home solar and battery storage with premium pricing.",
        "sunrun": "Sunrun offers leasing options but has longer contract terms compared to Wattmonk.",
        "sunnova": "Sunnova provides solar financing but may not be as fast in processing permits as Wattmonk."
    }
    
    for competitor in competitors.keys():
        if competitor in Query.lower():
            return f"Wattmonk vs {competitor.capitalize()}: {competitors[competitor]} Wattmonk specializes in fast, technology-driven solar permitting and interconnection services."

    # Reject off-topic queries
    if not any(topic in Query.lower() for topic in allowed_topics):
        return "I can only assist with Wattmonk and solar-related queries."

    # Fetch relevant search results
    search_results = googlesearch(Query)

    try:
        with open("Data/chatLog.json", "r") as f:
            messages = load(f)
            messages = messages[-10:]  # Keep only last 10 messages

        messages.append({"role": "user", "content": Query})

        #  Call Groq API with limited tokens (Prevent "Request too large" error)
        completion = client.chat.completions.create(
            model="llama3-70b-8192",  #  Uses a smaller model to reduce token usage
            messages=SystemChatbot + [{"role": "system", "content": search_results}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True
        )

        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        messages.append({"role": "assistant", "content": Answer})

        # Save last 10 messages only (prevents large file size)
        with open("Data/chatLog.json", "w") as f:
            dump(messages[-10:], f, indent=4)

        return Answer.strip()

    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    while True:
        user_input = input("Ask about Wattmonk, solar energy, or competition: ")
        print(Chatbot(user_input))
