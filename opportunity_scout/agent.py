import time
import anthropic
from config import MODEL, ANTHROPIC_API_KEY, SYSTEM_PROMPT
from tools import TOOLS, execute_tool


def run_agent(student_info: dict) -> str:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    user_message = (
        f"Please find internships, fellowships, and grants that match my profile:\n\n"
        f"- Name: {student_info['name']}\n"
        f"- Field of Study: {student_info['field_of_study']}\n"
        f"- Skills: {student_info['skills']}\n"
        f"- Year of Study: {student_info['year_of_study']}\n\n"
        f"Search for multiple types of opportunities. Run separate searches for internships, "
        f"fellowships, and grants so you cover all categories. Present the best matches with "
        f"deadlines and application links."
    )

    messages = [{"role": "user", "content": user_message}]

    print("\n🔍 Opportunity Scout is searching the web for opportunities...\n")

    while True:
        for attempt in range(3):
            try:
                response = client.messages.create(
                    model=MODEL,
                    max_tokens=4096,
                    system=SYSTEM_PROMPT,
                    tools=TOOLS,
                    messages=messages,
                )
                break
            except anthropic.RateLimitError:
                if attempt == 2:
                    raise
                wait = 60 * (attempt + 1)
                print(f"  ⏳ Rate limit reached. Waiting {wait}s before retrying...")
                time.sleep(wait)

        if response.stop_reason == "end_turn":
            # Collect the final text response
            final_text = ""
            for block in response.content:
                if hasattr(block, "text"):
                    final_text += block.text
            return final_text if final_text else "Search complete, but no text response was generated."

        if response.stop_reason == "tool_use":
            # Append the full assistant response (including tool_use blocks) to history
            messages.append({"role": "assistant", "content": response.content})

            # Execute every tool call and collect results
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    query = block.input.get("query", "")
                    print(f"  🌐 Searching: {query}")
                    result = execute_tool(block.name, block.input)
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        }
                    )

            # Feed all tool results back to the model in a single user turn
            messages.append({"role": "user", "content": tool_results})

        else:
            # Unexpected stop reason — return whatever text exists
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text
            return f"Agent stopped with unexpected reason: {response.stop_reason}"
