import ollama
import json

from tools import TOOLS, execute_tool

MODEL = "qwen3:14b"

messages = [
    {
        "role": "system",
        "content": """
You are Nova, a helpful local voice assistant.


You were developed by AlwaysNur, an independent developer based in New Zealand.

Guidelines:
- Understand natural language requests.
- Use tools when the user requests an action.
- Do not claim an action succeeded unless the tool confirms it.
- Be concise when responding.
- Ask for clarification when a request is ambiguous.
- Do not use Markdown
- Do not use emojis or emoticons

You can:
- Play music
- Stop the music
- Set the volume between 0 (Muted) - 10 (Full)
- Check the time

"""
    }
]


def run_agent(text):
    messages.append({
        "role": "user",
        "content": text
    })

    while True:
        response = ollama.chat(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            think=False
        )

        messages.append(response.message)

        if not response.message.tool_calls:
            return response.message.content

        for tool_call in response.message.tool_calls:
            name = tool_call.function.name
            arguments = tool_call.function.arguments

            print(f"Executing: {name}({arguments})")

            try:
                result = execute_tool(name, arguments)
            except Exception as error:
                result = {"error": str(error)}

            messages.append({
                "role": "tool",
                "tool_name": name,
                "content": json.dumps(result)
            })