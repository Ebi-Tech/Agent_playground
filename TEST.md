# TEST.md — The Agent Verification Suite
# Reusable test suite for any Python AI agent project.
# Run this after building all four files to confirm everything works.
# Claude Code: read this file and execute every check in order.
# Fix any failure before moving on. Do not skip checks.

---

## HOW TO USE THIS FILE

When you reach Prompt 4, Claude Code will read this file and run all checks automatically.
If you want to run checks manually at any point:
- Each section has the exact command or code to run
- Fix each failure before proceeding to the next check
- A passing suite means your agent is ready to run

---

## CHECK 1 — ENVIRONMENT

```
1a. Confirm virtual environment exists
    - Check that .venv/ directory exists in the project root
    - If missing: run python3 -m venv .venv

1b. Confirm correct Python is being used
    - Run: .venv/bin/python3 --version   (macOS/Linux)
    -  OR: .venv\Scripts\python --version (Windows)
    - Must be 3.8 or higher
    - If wrong version: recreate the venv with the correct Python

1c. Confirm all packages are installed
    - Run: .venv/bin/pip list   (macOS/Linux)
    -  OR: .venv\Scripts\pip list (Windows)
    - Must include: anthropic, tavily-python, python-dotenv
    - If any are missing: run .venv/bin/pip install -r requirements.txt

1d. Confirm .env file exists
    - Check that .env exists in the project root (not just .env.example)
    - If missing: run cp .env.example .env
    - Remind the user to add their API keys if the values are still placeholders

PASS condition: venv exists, Python 3.8+, all packages installed, .env present
```

---

## CHECK 2 — API KEY VALIDATION

```
2a. Validate Anthropic key
    Run this Python snippet inside the venv:

    from dotenv import load_dotenv
    import os
    import anthropic

    load_dotenv()
    key = os.getenv("ANTHROPIC_API_KEY")

    if not key or key == "your_anthropic_api_key_here":
        print("❌ ANTHROPIC_API_KEY is missing or still a placeholder.")
        print("   Open .env and add your real key.")
    else:
        try:
            client = anthropic.Anthropic(api_key=key)
            client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=10,
                messages=[{"role": "user", "content": "hi"}]
            )
            print("✅ Anthropic API key is valid and working.")
        except anthropic.AuthenticationError:
            print("❌ Anthropic API key is invalid. Check the key at https://console.anthropic.com")
        except anthropic.RateLimitError:
            print("⚠️  Anthropic key is valid but rate limit reached. Wait 60 seconds and retry.")

2b. Validate Tavily key
    Run this Python snippet inside the venv:

    from dotenv import load_dotenv
    import os
    from tavily import TavilyClient

    load_dotenv()
    key = os.getenv("TAVILY_API_KEY")

    if not key or key == "your_tavily_api_key_here":
        print("❌ TAVILY_API_KEY is missing or still a placeholder.")
        print("   Open .env and add your real key from https://app.tavily.com")
    else:
        try:
            client = TavilyClient(api_key=key)
            result = client.search(query="test", max_results=1)
            print("✅ Tavily API key is valid and working.")
        except Exception as e:
            print(f"❌ Tavily key failed: {str(e)}")
            print("   Check your key at https://app.tavily.com")

PASS condition: both keys return valid responses
```

---

## CHECK 3 — TOOL ISOLATION TEST

# Test your tool independently before connecting it to the agent.
# This catches tool errors before they get buried inside the loop.

```
Run this Python snippet inside the venv:

import sys
sys.path.insert(0, '.')
from tools import search_opportunities

print("Testing tool in isolation...")
result = search_opportunities("software engineering internship Africa 2025")

if not result:
    print("❌ Tool returned empty result. Check your Tavily key and quota.")
elif "Search failed" in result:
    print(f"❌ Tool returned an error: {result}")
else:
    print("✅ Tool is working. Sample output:")
    print(result[:500])  # Print first 500 chars to confirm it looks right

PASS condition: tool returns a non-empty string with no error message
```

---

## CHECK 4 — DRY RUN (no API tokens spent)

# Verify the agent loop structure works without calling the real Anthropic API.
# This catches import errors, logic errors, and structural issues for free.

```
Run this Python snippet inside the venv:

import sys
sys.path.insert(0, '.')
from unittest.mock import MagicMock, patch
from tools import TOOLS

print("Running dry run test...")

# Mock the Anthropic client so no real API call is made
mock_response = MagicMock()
mock_response.stop_reason = "end_turn"
mock_response.content = [MagicMock(text="Dry run successful.", type="text")]
mock_response.content[0].text = "Dry run successful."

with patch("anthropic.Anthropic") as mock_client:
    mock_instance = mock_client.return_value
    mock_instance.messages.create.return_value = mock_response

    from agent import run_agent
    result = run_agent("test message")

    if "Dry run successful" in result:
        print("✅ Agent loop structure is working correctly.")
    else:
        print(f"❌ Unexpected result from dry run: {result}")

PASS condition: agent loop runs and returns the mocked response without errors
```

---

## CHECK 5 — RATE LIMIT HANDLING

# Confirm the retry logic in agent.py is in place and works correctly.

```
Run this Python snippet inside the venv:

import sys
sys.path.insert(0, '.')
import inspect
import agent

source = inspect.getsource(agent.run_agent)

checks = [
    ("RateLimitError", "retry on rate limit"),
    ("time.sleep", "wait between retries"),
    ("attempt", "retry counter"),
]

all_passed = True
for keyword, description in checks:
    if keyword in source:
        print(f"✅ Found {description}")
    else:
        print(f"❌ Missing {description} — add retry logic to agent.py")
        all_passed = False

if all_passed:
    print("✅ Rate limit handling is in place.")
else:
    print("❌ Add the following to your API call in agent.py:")
    print("""
    for attempt in range(3):
        try:
            response = client.messages.create(...)
            break
        except anthropic.RateLimitError:
            if attempt == 2:
                raise
            wait = 60 * (attempt + 1)
            print(f"⏳ Rate limit reached. Waiting {wait}s...")
            time.sleep(wait)
    """)

PASS condition: all three keywords found in agent.py source
```

---

## CHECK 6 — TOKEN OVERFLOW HANDLING

# Confirms tool results are not too large to send back to Claude.
# Sending too much text in one message causes 429 token errors on the free tier.

```
Run this Python snippet inside the venv:

import sys
sys.path.insert(0, '.')
from tools import search_opportunities

result = search_opportunities("internship Africa 2025")
token_estimate = len(result) / 4  # rough estimate: 1 token ≈ 4 characters

print(f"Tool result length: {len(result)} characters (~{int(token_estimate)} tokens)")

if token_estimate > 3000:
    print("⚠️  Tool result is large. Risk of hitting token limit.")
    print("   Fix: reduce max_results in tools.py from 5 to 3")
    print("   Or truncate results: result = result[:4000]")
elif token_estimate > 6000:
    print("❌ Tool result is too large. Will likely cause 429 error.")
    print("   Fix: reduce max_results to 2 and add result[:3000] truncation")
else:
    print("✅ Tool result size is within safe limits.")

PASS condition: estimated tokens below 3000 per tool call
```

---

## CHECK 7 — RESPONSE QUALITY CHECK

# Confirms the agent returned something meaningful, not just a non-error.

```
Run this Python snippet inside the venv:
# NOTE: This check makes a real API call and will use tokens.
# Only run this if all previous checks have passed.

import sys
sys.path.insert(0, '.')
from agent import run_agent

print("Running live quality check (uses real API tokens)...")
test_message = "I am a 2nd year Computer Science student in Nigeria with Python and data analysis skills. Find me one internship I can apply to."

result = run_agent(test_message)

quality_checks = [
    (len(result) > 100, "Response has meaningful length"),
    (any(word in result.lower() for word in ["internship", "fellowship", "grant", "apply", "opportunity"]), "Response contains relevant content"),
    (any(char in result for char in ["http", "www", ".com", ".org"]), "Response contains at least one link"),
]

all_passed = True
for condition, description in quality_checks:
    if condition:
        print(f"✅ {description}")
    else:
        print(f"⚠️  {description} — response may be incomplete")
        all_passed = False

if all_passed:
    print("\n✅ Agent is returning quality responses.")
else:
    print("\n⚠️  Response quality issues detected. Check your SYSTEM_PROMPT in config.py.")
    print("   Make sure it instructs the agent to include links and specific opportunity names.")

print("\nSample response:")
print(result[:800])

PASS condition: response is over 100 chars, contains relevant keywords and at least one link
```

---

## CHECK 8 — GRACEFUL EXIT

# Confirms the agent handles Ctrl+C cleanly without crashing or leaving
# dangling processes.

```
Run this Python snippet inside the venv:

import sys
sys.path.insert(0, '.')
import inspect
import main

source = inspect.getsource(main.main)

if "KeyboardInterrupt" in source:
    print("✅ KeyboardInterrupt handler found in main.py")
else:
    print("❌ No KeyboardInterrupt handler found.")
    print("   Add this to your main() function in main.py:")
    print("""
    def main():
        try:
            user_message = get_user_input()
            result = run_agent(user_message)
            print(result)
        except KeyboardInterrupt:
            print("\\n\\nStopped by user. Goodbye.")
    """)

PASS condition: KeyboardInterrupt handling present in main.py
```

---

## CHECK 9 — COST AWARENESS

```
Print this reminder to the terminal:

💰 COST AWARENESS:
   - You are on the Anthropic free tier ($5 credit)
   - Each full agent run uses approximately 2000–5000 tokens
   - At current Sonnet pricing, that is roughly $0.01–$0.03 per run
   - Monitor your usage at: https://console.anthropic.com/usage
   - If you see unexpected charges, check for infinite loops in agent.py
   - To reduce token usage: lower MAX_TOKENS in config.py or reduce max_results in tools.py
```

---

## FINAL RESULT

```
If all checks passed, print:

✅ All checks passed.
🚀 Opportunity Scout is ready.
   Run it with: .venv/bin/python3 main.py   (macOS/Linux)
            OR: .venv\Scripts\python main.py  (Windows)

If any checks failed, print:

❌ X check(s) failed. Fix the issues above before running the agent.
   Do not proceed until all checks show ✅
```
