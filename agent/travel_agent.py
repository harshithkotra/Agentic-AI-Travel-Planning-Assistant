
import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from tools.travel_tools import ALL_TRAVEL_TOOLS

load_dotenv()

def build_travel_agent():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing. Please add it to your .env file.")

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        api_key=api_key
    )

    agent = create_agent(
        model=llm,
        tools=ALL_TRAVEL_TOOLS,
        system_prompt="""
You are an intelligent AI Travel Planning Assistant.

Your job is to help users plan trips based on their preferences,
destination, travel dates, budget, and duration.

Instructions:
1. Understand the user's travel request.
2. Use the available tools to search for flights, hotels,
   attractions, weather, and calculate budgets.
3. Never invent flight or hotel details that are not in the dataset.
4. Recommend suitable options considering cost, rating and preferences.
5. Create a practical day-wise itinerary.
6. Clearly explain why you selected the recommendations.
7. Mention when information is unavailable.
8. Format the final response neatly using headings and bullet points.
9. Include a budget breakdown and estimated total.
10. Keep the response easy to understand.

Always use tools when relevant instead of guessing.
"""
    )

    return agent


def plan_trip(user_query: str):
    agent = build_travel_agent()

    response = agent.invoke({
        "messages": [
            {"role": "user", "content": user_query}
        ]
    })

    messages = response.get("messages", [])

    if messages:
        return messages[-1].content

    return "Unable to generate a travel plan."
