import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from app.tools.storage_estimator import estimate_storage
from app.tools.registry import TOOL_RESISTRY

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


TOOLS = [
    {
        "type": "function",
        "name": "estimate_storage",
        "description": "Estimate storage for any event-based system",
        "parameters": {
            "type": "object",
            "properties": {
                "events_per_day": {
                    "type": "integer",
                    "description": "Number of events per day",
                },
                "avg_event_size_kb": {
                    "type": "number",
                    "description": "Average size of each event in KB",
                },
                "retention_days": {
                    "type": "integer",
                    "description": "How many days data is stored",
                },
            },
            "required": ["events_per_day"],
        },
    }
]


SYSTEM_PROMPT = """
You are ArchLily, an advanced AI System Design Interview Coach.

Your responsibilities:
- Help users design scalable distributed systems.
- Explain trade-offs clearly.
- Think in terms of scale, consistency, latency, storage, caching, and cost.
- Use structured reasoning.

Tool Usage Policy:
- If a question requires numeric estimation or calculation,
  you MUST call the appropriate tool instead of guessing.
- Never fabricate numerical results.
- Use tools for deterministic computations.

RAG Usage Policy:
- Use the provided "Relevant knowledge" context when it is helpful.
- Do not repeat the context verbatim.
- Integrate it naturally into your reasoning.

Interaction Policy:
- Ask clarifying questions only if critical information is missing.
- If sufficient data is provided, proceed with structured analysis.

Response Style:
- Be concise but technically deep.
- Structure answers using sections where helpful.
- Explain assumptions explicitly.
"""


def run_agent(conversation):

    response = client.responses.create(
        model="gpt-4o-mini", input=conversation, tools=TOOLS
    )

    for item in response.output:
        if item.type == "function_call":
            print(f"Tool called ✅")    
            tool_name = item.name

            if tool_name not in TOOL_RESISTRY:
                raise Exception(f"Tool {tool_name} not registerd")

            args = item.arguments

            if isinstance(args, str):
                args = json.loads(args)

            tool_fn = TOOL_RESISTRY[tool_name]
            result = tool_fn(**args)

            # Send tool result back
            tool_response = client.responses.create(
                model="gpt-4o-mini",
                input=conversation
                + [
                    {
                        "type": "function_call",
                        "name": item.name,
                        "arguments": json.dumps(args),
                        "call_id": item.call_id,
                    },
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": str(result),
                    },
                ],
            )

            return tool_response.output_text

    # If no tool used
    return response.output_text

