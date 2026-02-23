import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

SYSTEM_PROMPT = """
You are ArchLily, an expert System Design Interview Coach.
Always ask clarifying questions first.
Think about scale, database, caching, load balancing and tradeoffs.
"""


def generate_response(messages):
    response = client.responses.create(
        model="gpt-4o-mini",
        input=messages,
    )

    return response.output_text
