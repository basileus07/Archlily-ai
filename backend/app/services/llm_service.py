import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.responses.response_output_message import Content
from sqlalchemy import false
from app.tools.storage_estimator import estimate_storage
from app.tools.registry import TOOL_REGISTRY
from app.prompts.planner import PLANNER_PROMPT
from app.prompts.synthesizer import SYNTHESIZER_PROMPT_TEMPLATE
from app.prompts.system import SYSTEM_PROMPT

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


TOOLS = [
    {
        "type": "function",
        "name": "estimate_storage",
        "description": "Estimate storage for event-based systems",
        "parameters": {
            "type": "object",
            "properties": {
                "events_per_day": {"type": "integer"},
                "avg_event_size_kb": {"type": "number"},
                "retention_days": {"type": "integer"},
            },
            "required": ["events_per_day"],
        },
    },
    {
        "type": "function",
        "name": "estimate_qps",
        "description": "Estimate average and peak QPS",
        "parameters": {
            "type": "object",
            "properties": {
                "events_per_day": {"type": "integer"},
            },
            "required": ["events_per_day"],
        },
    },
    {
        "type": "function",
        "name": "estimate_infra_cost",
        "description": "Estimate yearly infrastructure cost",
        "parameters": {
            "type": "object",
            "properties": {
                "storage_gb": {"type": "number"},
                "cost_per_gb_per_month": {"type": "number"},
            },
            "required": ["storage_gb"],
        },
    },
]


def run_planner(user_input):
    prompt = f"""
    
    {PLANNER_PROMPT}

    User Request:
    {user_input}
    """
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": [{"type": "input_text", "text": prompt}],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": user_input}],
            },
        ],
    )

    return response.output_text


def execute_plan(plan_json):

    results = {}

    for step in plan_json["steps"]:

        tool_name = step["tool"]
        args = step["arguments"]

        if tool_name not in TOOL_REGISTRY:
            raise Exception(f"Tool {tool_name} not  registered")

        tool_fn = TOOL_REGISTRY[tool_name]
        result = tool_fn(**args)

        results[tool_name] = result
    return results


def run_synthesizer(user_input, tool_results):
    SYNTHESIZER_PROMPT = f"""
    {SYNTHESIZER_PROMPT_TEMPLATE}

    User Request:
    {user_input}

    Tool Results:
    {tool_results}
    """
    response = client.responses.create(model="gpt-4o-mini", input=SYNTHESIZER_PROMPT)

    return response.output_text


def run_agent(user_input):

    # planning phase
    plan_text = run_planner(user_input)
    plan_json = json.loads(plan_text)

    # Execution phase
    tool_results = execute_plan(plan_json)

    # synthesis phase
    final_answer = run_synthesizer(user_input, tool_results)

    return final_answer


# old one before orchestrator pattern
# def run_agent(conversation, max_step=5):

#     current_conversation = conversation.copy()

#     for step in range(max_step):
#         print(f"\n---Agent step: {step+1}---")

#         response = client.responses.create(
#             model="gpt-4o-mini", input=current_conversation, tools=TOOLS
#         )

#         tool_called = False

#         for item in response.output:

#             # if model want to call tool
#             if item.type == "function_call":

#                 print(f"Tool called ✅")
#                 tool_called = True
#                 tool_name = item.name

#                 print(f"Request tool: {tool_name}")

#                 if tool_name not in TOOL_RESISTRY:
#                     raise Exception(f"Tool {tool_name} not registerd")

#                 args = item.arguments
#                 if isinstance(args, str):
#                     args = json.loads(args)

#                 tool_fn = TOOL_RESISTRY[tool_name]
#                 result = tool_fn(**args)

#                 print(f"Tool result: {result}")

#                 # Append tool call + tool output in converstion
#                 current_conversation.append(
#                     {
#                         "type": "function_call",
#                         "name": item.name,
#                         "arguments": json.dumps(args),
#                         "call_id": item.call_id,
#                     }
#                 )

#                 current_conversation.append(
#                     {
#                         "type": "function_call_output",
#                         "call_id": item.call_id,
#                         "output": str(result),
#                     }
#                 )

#                 break
#         if not tool_called:
#             return response.output_text

#     # If no tool used
#     return response.output_text
