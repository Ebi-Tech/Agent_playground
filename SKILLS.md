# SKILLS.md — The Agent Builder's Guide
# Reusable scaffolding for any Python AI agent project.
# Read this file before writing any code.

---

## 0. CLAUDE CODE SETUP

# Claude Code runs in any terminal — VS Code, CMD, Mac Terminal, Linux bash.
# Check if it is already installed before trying to install it.

```
STEP 1 — Check if Claude Code is installed
- Run: claude --version
- If found: ✅ Claude Code is ready.
  Navigate to your project folder and type: claude
  That is all you need to do. Skip the rest of this section.

STEP 2 — If not found, check Node.js
- Run: node --version
- If found: skip to Step 3
- If not found:
    macOS:   brew install node
         OR  download LTS from https://nodejs.org
    Windows: download LTS installer from https://nodejs.org
             check "Add to PATH" during installation
    Linux:   sudo apt update && sudo apt install nodejs npm
- Verify: node --version

STEP 3 — Install Claude Code
- Run: npm install -g @anthropic/claude-code
- Verify: claude --version
- If verified: ✅ Claude Code installed successfully

STEP 4 — Start a session
- Navigate to your project folder in the terminal
- Run: claude
- Claude Code will start in that directory and read any .md files present
```

---

## 1. API KEY ACQUISITION

Before anything else, make sure you have the following keys:

### Anthropic API Key
- Go to: https://console.anthropic.com
- Sign up or log in
- Navigate to "API Keys" and create a new key
- Copy it immediately — it will not be shown again
- Free tier includes $5 in credits to start

### Tavily API Key (for web search)
- Go to: https://app.tavily.com
- Sign up for a free account
- Your API key is on the dashboard immediately after signup
- Free tier: 1000 searches/month

### Other tool keys (if not using Tavily)
# Replace Tavily with any of the following depending on your agent's purpose:
# - OpenWeatherMap (weather data): https://openweathermap.org/api
# - NewsAPI (news search): https://newsapi.org
# - Serper (Google search): https://serper.dev
# - Alpha Vantage (stock data): https://www.alphavantage.co
# - Notion API (notes/database): https://developers.notion.com
# - Airtable API (structured data): https://airtable.com/developers

---

## 2. SYSTEM CHECK

Run these checks in order before creating any files.
Print the result of each check clearly to the terminal.

```
STEP 1 — Check Python
- Run: python3 --version
- If found: print "✅ Python X.X.X found"
- If not found:
    macOS:   install via Homebrew — brew install python3
    Windows: download from https://www.python.org/downloads/ — check "Add to PATH"
    Linux:   sudo apt update && sudo apt install python3
- After install, verify again with python3 --version

STEP 2 — Check Python version
- Must be 3.8 or higher
- If lower: upgrade using the same method as Step 1
- Print "✅ Python version OK"

STEP 3 — Check pip
- Run: pip3 --version
- If not found: run python3 -m ensurepip --upgrade
- Print "✅ pip available"

STEP 4 — Check git
- Run: git --version
- If not found:
    macOS:   brew install git
    Windows: download from https://git-scm.com
    Linux:   sudo apt install git
- Print "✅ git available"
```

---

## 3. VIRTUAL ENVIRONMENT SETUP

# WHY: macOS (and some Linux systems) block pip install on system Python (PEP 668).
# A virtual environment isolates your project's packages from the system.
# Always create a virtual environment before installing anything.

```
STEP 1 — Create the virtual environment
- Run: python3 -m venv .venv
- Print "✅ Virtual environment created at .venv/"

STEP 2 — Confirm it exists
- Check that .venv/ directory exists in the project root
- If it doesn't exist, retry Step 1

STEP 3 — Install dependencies
- Run: .venv/bin/pip install -r requirements.txt        (macOS/Linux)
-  OR: .venv\Scripts\pip install -r requirements.txt    (Windows)
- Print "✅ All dependencies installed"

STEP 4 — Confirm installation
- Run: .venv/bin/pip list    (macOS/Linux)
-  OR: .venv\Scripts\pip list (Windows)
- Verify all packages from requirements.txt appear in the list
```

# WINDOWS NOTE:
# On Windows, always use .venv\Scripts\python and .venv\Scripts\pip
# On macOS/Linux, always use .venv/bin/python3 and .venv/bin/pip
# Never use the system python3 or pip directly after the venv is created

---

## 4. FILE NAMING CONVENTIONS

# Breaking these rules will cause import errors.

```
RULES:
- All Python files: lowercase, underscores only — config.py, tools.py, agent.py, main.py
- No spaces in file names — ever
- No hyphens in Python file names — my-agent.py will break imports
- No capital letters in Python file names
- The four core files must always be named: config.py, tools.py, agent.py, main.py
- Environment file: always .env (with the dot, no extension)
- Requirements file: always requirements.txt
- Markdown files: UPPERCASE is fine — SKILLS.md, TEST.md, README.md

FOLDER STRUCTURE:
your_project/
├── .env                  ← your actual keys (never commit this)
├── .env.example          ← template with empty values (safe to commit)
├── .gitignore
├── requirements.txt
├── config.py             ← brain
├── tools.py              ← hands
├── agent.py              ← loop
├── main.py               ← trigger
├── SKILLS.md             ← this file
├── TEST.md               ← test suite
└── memory/               ← optional, for persistent memory (see Section 7)
    └── history.json
```

---

## 5. ENVIRONMENT VARIABLES

# Create .env.example first (safe to commit to GitHub)
# Then copy it to .env and fill in real values (never commit .env)

```
# .env.example template — customize for your agent:
ANTHROPIC_API_KEY=your_anthropic_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

# Add any other keys your tools need, for example:
# NOTION_API_KEY=your_notion_key_here
# WEATHER_API_KEY=your_weather_key_here
```

# After creating .env, validate that keys loaded correctly:
```python
# Add this check to config.py after load_dotenv():
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY is missing. Check your .env file.")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is missing. Check your .env file.")
```

---

## 6. AGENT ARCHITECTURE TEMPLATE

# This is the skeleton for any agent. 
# Copy it, fill in the blanks, and you have a working agent structure.
# Comments explain what each section does and why.

### config.py — THE BRAIN
```python
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys — loaded from .env, never hardcoded
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
# Add more keys here as needed

# Validate keys loaded correctly
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY is missing. Check your .env file.")

# Model configuration
MODEL = "claude-sonnet-4-20250514"  # Always use this exact string
MAX_TOKENS = 1024  # Increase if agent responses are getting cut off

# System prompt — this is your agent's identity and instructions
# Be specific: tell it who it is, what it does, and how it should respond
SYSTEM_PROMPT = """
You are [AGENT NAME] — [one sentence description of what this agent does].

When given [describe the input], you will:
1. [First thing the agent should do]
2. [Second thing]
3. [How to format the output]

Always [important rule].
Never [important constraint].
"""
```

### tools.py — THE HANDS
```python
# Import your tool's SDK here
from tavily import TavilyClient  # Replace with your chosen tool
from config import TAVILY_API_KEY  # Replace with your key variable

# Initialise the tool client
client = TavilyClient(api_key=TAVILY_API_KEY)

# Define your tool function
# This is the actual Python function that does the work
def your_tool_name(parameter: str) -> str:
    """
    One sentence description of what this tool does.
    Claude reads this docstring when deciding whether to use the tool.
    """
    try:
        # Call your external API or service here
        result = client.search(query=parameter, max_results=5)
        # Format and return the result as a string
        return str(result)
    except Exception as e:
        return f"Tool failed: {str(e)}"

# Anthropic tool definition — this tells Claude the tool exists
# The description is critical: Claude uses it to decide when to call the tool
# Be specific and clear — vague descriptions lead to wrong tool calls
TOOLS = [
    {
        "name": "your_tool_name",  # Must exactly match the function name above
        "description": "Detailed description of what this tool does and when to use it.",
        "input_schema": {
            "type": "object",
            "properties": {
                "parameter": {
                    "type": "string",
                    "description": "Description of what this parameter should contain"
                }
                # Add more parameters here if needed
            },
            "required": ["parameter"]  # List all required parameters
        }
    }
]
```

### agent.py — THE LOOP
```python
import anthropic
import time
from config import ANTHROPIC_API_KEY, MODEL, MAX_TOKENS, SYSTEM_PROMPT
from tools import your_tool_name, TOOLS  # Import your tool function and definition

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def run_agent(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    while True:
        # Retry logic — handles rate limit errors automatically
        for attempt in range(3):
            try:
                response = client.messages.create(
                    model=MODEL,
                    max_tokens=MAX_TOKENS,
                    system=SYSTEM_PROMPT,
                    tools=TOOLS,
                    messages=messages
                )
                break
            except anthropic.RateLimitError:
                if attempt == 2:
                    raise
                wait = 60 * (attempt + 1)
                print(f"⏳ Rate limit reached. Waiting {wait}s before retrying...")
                time.sleep(wait)

        # Check why the model stopped
        if response.stop_reason == "end_turn":
            # Agent is done — extract and return the text
            return "\n".join(
                block.text for block in response.content
                if hasattr(block, "text")
            )

        elif response.stop_reason == "tool_use":
            # Agent wants to use a tool — run it and feed results back
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    print(f"🔧 Running tool: {block.name}({list(block.input.values())[0]})")
                    # Add more tool conditions here as you add more tools
                    if block.name == "your_tool_name":
                        result = your_tool_name(block.input["parameter"])
                    else:
                        result = f"Unknown tool: {block.name}"

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })

            messages.append({"role": "user", "content": tool_results})

        else:
            return f"Agent stopped unexpectedly: {response.stop_reason}"
```

### main.py — THE TRIGGER
```python
from agent import run_agent

def get_user_input() -> str:
    print("Welcome to [AGENT NAME]")
    print("")
    # Collect whatever input your agent needs
    field = input("Your input prompt here: ")
    # Add more inputs as needed
    return f"Formatted message using {field} to send to the agent."

def main():
    try:
        user_message = get_user_input()
        print("")
        result = run_agent(user_message)
        print("")
        print("Result:")
        print(result)
    except KeyboardInterrupt:
        print("\n\nStopped by user. Goodbye.")

if __name__ == "__main__":
    main()
```

---

## 7. MEMORY AND CONTEXT GUIDANCE

# By default, agents have no memory between runs.
# Each time you run main.py, the agent starts fresh.
# If your agent needs to remember past conversations, use one of these approaches:

### Option A — Simple file-based memory (recommended for beginners)
```python
# Add to agent.py — saves and loads conversation history from a JSON file
import json
import os

MEMORY_FILE = "memory/history.json"

def load_history():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(messages):
    os.makedirs("memory", exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(messages, f, indent=2)

# In run_agent(), replace:
# messages = [{"role": "user", "content": user_message}]
# With:
# messages = load_history()
# messages.append({"role": "user", "content": user_message})
# And after the agent finishes, call save_history(messages)
```

### Option B — In-session memory only
# Pass the full messages list between function calls within the same run.
# Memory resets when the program exits. Good for multi-turn conversations
# within a single session.

### Option C — Database (for production agents)
# Use SQLite for local persistence or PostgreSQL for deployed agents.
# Only needed if you are building something that serves multiple users.

---

## 8. MODEL REFERENCE

# Current Claude models and their limits:
# claude-sonnet-4-20250514  — recommended, best balance of speed and quality
# claude-opus-4-20250514    — most capable, slower, higher cost
# claude-haiku-4-5-20251001 — fastest, lowest cost, good for simple tasks

# Free tier limits (as of 2025):
# - 10,000 tokens per minute
# - If you hit this: the retry logic in agent.py handles it automatically
# - To avoid it: reduce MAX_TOKENS or reduce the number of tool results returned

# Token tips:
# - 1 token ≈ 4 characters of English text
# - A typical agent response uses 500–1000 tokens
# - Each Tavily search result is roughly 500–1000 tokens
# - If you run 4 searches, that is up to 4000 tokens before Claude even responds
# - Keep max_results in your tool to 3–5 to stay within limits

---

## 9. FRONTEND BLOCK

# Use this section when you are ready to take your agent out of the terminal
# and build a web interface. Uncomment the stack you want to use.

# ── OPTION A: Plain HTML + CSS + JavaScript (simplest) ────────────────────────
# No install needed. Create index.html in your project root.
# Use fetch() to call a simple Python backend (Flask or FastAPI).
# Good for: quick demos, simple interfaces, no framework experience needed.
#
# To scaffold:
#   Create index.html manually
#   Install Flask: .venv/bin/pip install flask
#   Create app.py as your backend server

# ── OPTION B: React (component-based, popular) ────────────────────────────────
# Requirements: Node.js installed (https://nodejs.org — download LTS version)
# macOS:   brew install node
# Windows: download installer from https://nodejs.org
# Linux:   sudo apt install nodejs npm
#
# To scaffold:
#   npx create-react-app frontend
#   cd frontend
#   npm start
#
# Connect to your Python backend via fetch() or axios

# ── OPTION C: Next.js (React + routing + API routes) ─────────────────────────
# Requirements: Node.js installed (same as above)
#
# To scaffold:
#   npx create-next-app@latest frontend
#   cd frontend
#   npm run dev
#
# You can write your agent API route directly in Next.js under /app/api/
# which removes the need for a separate Python backend

# ── OPTION D: TypeScript + React (typed, production-grade) ────────────────────
# Requirements: Node.js installed
#
# To scaffold:
#   npx create-react-app frontend --template typescript
#   cd frontend
#   npm start

# ── BRAND AND COLOR ASSETS ────────────────────────────────────────────────────
# Add your brand colors and fonts here before building the frontend.
# Uncomment and fill in your values.
#
# PRIMARY_COLOR = "#000000"
# SECONDARY_COLOR = "#ffffff"
# ACCENT_COLOR = "#ff6b35"
# FONT_FAMILY = "Inter, sans-serif"
# LOGO_PATH = "assets/logo.png"
# BRAND_NAME = "Your Agent Name"
