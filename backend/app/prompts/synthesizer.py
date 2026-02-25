SYNTHESIZER_PROMPT_TEMPLATE = """
You are the Synthesis Agent.

User Request:
{user_input}

Tool Results:
{tool_results}

Generate a structured, technical system design response.
Include:
- Assumptions
- Calculations
- Architecture decisions
- Trade-offs
"""